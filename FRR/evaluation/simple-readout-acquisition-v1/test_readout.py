"""Checks that matter to interpretation: no key leakage; class/token/metric distinctions."""
import json
from pathlib import Path
import unittest
from run import prompt, summarize_rows

ROOT = Path(__file__).resolve().parent

class ReadoutTests(unittest.TestCase):
    def test_prompt_ignores_id_split_and_state_key(self):
        plan = {'prompt_template': '{mapping}\n{source}'}
        case = {'id': 'answer_bearing_id', 'split': 'seen', 'state': 'positive', 'source': 'Status: missing'}
        changed = {**case, 'id': 'other', 'state': 'zero', 'split': 'primary'}
        self.assertEqual(prompt(case, {'missing': 'C'}, plan), prompt(changed, {'missing': 'C'}, plan))

    def test_unresolved_and_wrong_first_token_do_not_become_success(self):
        r = {'arm': 'toy', 'phase': 'base', 'split': 'primary', 'state': 'missing',
             'free_correct': False, 'free_state': None, 'first_token_correct': True,
             'sum_correct': True, 'mean_correct': False, 'stop': 'token_limit'}
        s = summarize_rows([r])['toy']['base']['primary']
        self.assertEqual((s['n'], s['free_correct'], s['unresolved'], s['first_token_correct'], s['constrained_sum_correct']), (1, 0, 1, 1, 1))

    def test_frozen_curriculum_balance_disjoint_sources_and_mappings(self):
        cases = json.loads((ROOT / 'DATA.json').read_text())
        plan = json.loads((ROOT / 'PLAN.json').read_text())
        byid = {c['id']: c for c in cases}
        self.assertEqual(len(cases), 24)
        self.assertEqual(len({c['source'] for c in cases}), 24)
        self.assertEqual(len(plan['order']), 48)
        self.assertTrue(all({byid[c]['state'] for c in g} == {'positive', 'zero', 'missing'} for g in plan['order']))
        for state in ('positive', 'zero', 'missing'):
            self.assertEqual({plan['mappings'][f'alias_{i}'][state] for i in range(3)}, {'A', 'B', 'C'})

if __name__ == '__main__':
    unittest.main()
