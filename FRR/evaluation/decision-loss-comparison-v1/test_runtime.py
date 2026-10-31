"""Synthetic numerical/resource tests only; no pretrained model loads or inference."""
import json
from pathlib import Path
import tempfile
import unittest

import torch
from runtime import GuardStop, balanced_update, encode, make_order, objective


class Tokenizer:
    eos_token_id = 0
    def apply_chat_template(self, messages, **kwargs):
        return [5, 4, 5]
    def encode(self, label, **kwargs):
        return {'YES': [1], 'NO': [2], 'WITHHOLD': [3, 4]}[label]


GUIDANCE = {'instruction': 'classify', 'question': 'answer'}
CASES = [{'id': f'{label}_{i}', 'source': 'synthetic', 'label': label}
         for i in range(24) for label in ('YES', 'NO', 'WITHHOLD')]


class Guard:
    def __init__(self, fail=None):
        self.fail, self.points = fail, []
    def read(self, stage, **context):
        p = {'phase': stage, **context}; self.points.append(p)
        if stage == self.fail:
            raise GuardStop('synthetic_resource_trigger', p)
        return p


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.logits = torch.nn.Parameter(torch.arange(36, dtype=torch.float64).reshape(1, 6, 6)/100)
    def forward(self, input_ids, **kwargs):
        return type('Output', (), {'logits': self.logits[:, :input_ids.shape[1], :]})()


class ObjectiveTests(unittest.TestCase):
    def test_independent_values_gradients_prompt_mask_and_eos(self):
        labels = torch.tensor([[-100, -100, -100, 1, 2, 3]])
        base = torch.arange(30, dtype=torch.float64).reshape(1, 6, 5)/7
        for kind, weights in [('sequence_mean', [1/3]*3), ('decision_balanced', [.5, .25, .25])]:
            logits = base.clone().requires_grad_()
            loss, comp = objective(logits, labels, kind)
            # Independent scalar logsumexp reference and closed-form CE derivative.
            expected = 0.; gradient = torch.zeros_like(logits)
            ces = []
            for position, target, weight in zip((2, 3, 4), (1, 2, 3), weights):
                row = base[0, position]
                ce = torch.logsumexp(row, dim=0) - row[target]
                ces.append(float(ce)); expected += weight * ce
                gradient[0, position] = weight * torch.softmax(row, dim=0)
                gradient[0, position, target] -= weight
            loss.backward()
            torch.testing.assert_close(loss, expected, rtol=1e-13, atol=1e-13)
            torch.testing.assert_close(logits.grad, gradient, rtol=1e-13, atol=1e-13)
            self.assertEqual(comp['target_tokens_including_eos'], 3)
            self.assertAlmostEqual(comp['first_token_ce'], ces[0])
            self.assertAlmostEqual(comp['suffix_mean_ce'], sum(ces[1:])/2)
            changed = base.clone(); changed[0, 0] = 100; changed[0, 1] = -100; changed[0, 5] = 123
            self.assertEqual(float(objective(changed, labels, kind)[0]), float(loss))
            # Last supervised target is EOS: changing its predicted logit must matter.
            changed = base.clone(); changed[0, 4, 3] += 2
            self.assertNotEqual(float(objective(changed, labels, kind)[0]), float(loss))

    def test_single_label_token_plus_eos_objectives_identical(self):
        logits = torch.randn(1, 5, 6, dtype=torch.float64)
        labels = torch.tensor([[-100, -100, -100, 2, 0]])
        a = logits.clone().requires_grad_(); b = logits.clone().requires_grad_()
        la, _ = objective(a, labels, 'sequence_mean')
        lb, _ = objective(b, labels, 'decision_balanced')
        la.backward(); lb.backward()
        self.assertTrue(torch.equal(la, lb)); self.assertTrue(torch.equal(a.grad, b.grad))

    def test_encoding_masks_prompt_retains_terminal_eos(self):
        ids, labels = encode(Tokenizer(), CASES[2], GUIDANCE, True)
        self.assertEqual(ids, [5, 4, 5, 3, 4, 0])
        self.assertEqual(labels, [-100, -100, -100, 3, 4, 0])
        self.assertEqual(encode(Tokenizer(), {'source': 'no gold'}, GUIDANCE), [5, 4, 5])

    def test_reject_noncontiguous_targets(self):
        with self.assertRaises(ValueError):
            objective(torch.zeros(1, 5, 6), torch.tensor([[-100, 1, -100, 2, 0]]), 'decision_balanced')

    def test_order_same_complete_balanced_exposure(self):
        first, second = make_order(CASES, 73103), make_order(CASES, 73103)
        self.assertEqual(first, second); self.assertEqual(len(first), 48)
        ids = [c['id'] for g in first for c in g]
        self.assertTrue(all(ids.count(c['id']) == 2 for c in CASES))
        self.assertTrue(all({c['label'] for c in g} == {'YES', 'NO', 'WITHHOLD'} for g in first))

    def test_update_equal_three_independent_micro_gradients(self):
        for kind in ('sequence_mean', 'decision_balanced'):
            model, reference = Toy(), Toy()
            expected = torch.zeros_like(reference.logits)
            for case in CASES[:3]:
                ids, labels = encode(Tokenizer(), case, GUIDANCE, True)
                # Explicitly compute CE at the predicted positions, no objective() use.
                n = len(ids) - 3
                targets = labels[3:]
                for j, target in enumerate(targets):
                    pos = 2+j
                    weight = 1/n if kind == 'sequence_mean' else (.5 if j == 0 else .5/(n-1))
                    expected[0, pos] += torch.softmax(reference.logits.detach()[0, pos], dim=0)*weight/3
                    expected[0, pos, target] -= weight/3
            self.assertLess(float(expected.norm()), 1)
            before = reference.logits.detach().clone()
            optimizer = torch.optim.SGD(model.parameters(), lr=.1)
            record = balanced_update(model, Tokenizer(), optimizer, CASES[:3], GUIDANCE, kind, Guard(), 1)
            self.assertTrue(record['completed']); self.assertTrue(record['optimizer_applied'])
            self.assertEqual(len(record['micro_losses']), 3)
            torch.testing.assert_close(model.logits, before - .1*expected, rtol=1e-13, atol=1e-13)

    def test_guard_stop_preserves_trigger_and_discards_unapplied_gradients(self):
        for stage in ('before_forward', 'after_forward', 'before_backward', 'after_backward', 'before_optimizer'):
            model = Toy(); before = model.logits.detach().clone()
            optimizer = torch.optim.SGD(model.parameters(), lr=.1)
            guard = Guard(stage)
            record = balanced_update(model, Tokenizer(), optimizer, CASES[:3], GUIDANCE,
                                     'decision_balanced', guard, 1)
            self.assertFalse(record['completed']); self.assertFalse(record['optimizer_applied'])
            self.assertEqual(record['trigger'], guard.points[-1])
            self.assertEqual(record['trigger']['phase'], stage)
            self.assertTrue(torch.equal(before, model.logits)); self.assertIsNone(model.logits.grad)

    def test_after_optimizer_stop_counts_completed_update(self):
        model = Toy(); before = model.logits.detach().clone()
        record = balanced_update(model, Tokenizer(), torch.optim.SGD(model.parameters(), lr=.1),
                                CASES[:3], GUIDANCE, 'decision_balanced', Guard('after_optimizer'), 1)
        self.assertTrue(record['completed']); self.assertTrue(record['optimizer_applied'])
        self.assertFalse(torch.equal(before, model.logits))
        self.assertEqual(record['trigger']['phase'], 'after_optimizer')


if __name__ == '__main__':
    unittest.main(verbosity=2)
