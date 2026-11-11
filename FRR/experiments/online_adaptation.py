"""Predeclared online-feedback adaptation after a parity-rule inversion.

The experimental world is the noisy eight-state parity shift register. A
pretrained GRU is exposed to *independent inverted-rule episodes*. Predictions
are evaluated on fresh streams before each update; feedback from each training
episode updates parameters only for future predictions. Frozen, head-only,
and full-finetune arms start from identical pretrained weights.
"""

import copy
import json

import torch
from torch import nn

from eight_state_nonlumpable_rnn import GRUPredictor, trajectories
from rule_shift_probe import make_trajectories


CHECKPOINTS = [0, 1, 2, 5, 10, 20, 40, 80]


def accuracy(model, seed, rule, n=1024):
    generator = torch.Generator().manual_seed(seed)
    x, y = make_trajectories(n, 24, rule, generator)
    with torch.no_grad():
        predictions = (model(x)[:, 2:] >= 0).float()
        return (predictions == y[:, 2:]).float().mean().item()


def within_episode_switch_accuracy(model, seed, n=2048, length=24, switch_t=12):
    """Frozen model carries hidden state through a true mid-episode rule switch.

    At t=switch_t the rule generating x[t+1] changes, without signaling the
    model. No feedback or parameter updates are supplied in this diagnostic.
    """
    generator = torch.Generator().manual_seed(seed)
    bits = torch.zeros(n, length + 1, 1)
    bits[:, :3] = torch.randint(0, 2, (n, 3, 1), generator=generator).float()
    noise = torch.rand(n, length-2, 1, generator=generator) < .1
    for t in range(2, length):
        parity = bits[:, t].bool() ^ bits[:, t-1].bool() ^ bits[:, t-2].bool()
        logical = parity if t < switch_t else ~parity
        bits[:, t+1] = (logical ^ noise[:, t-2]).float()
    with torch.no_grad():
        # Exactly one forward pass; GRU hidden state is NOT reset at switch_t.
        pred = (model(bits[:, :-1]) >= 0).float()
        correct = (pred == bits[:, 1:]).float()
        before = correct[:, 2:switch_t].mean().item()
        after = correct[:, switch_t:].mean().item()
    return {"switch_at_prediction_t": switch_t, "pre_switch_accuracy": round(before, 5),
            "post_switch_accuracy": round(after, 5), "hidden_state_continuous": True,
            "adaptation_or_feedback": False}


def run(seed, pretrain_steps=450):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    loss_fn = nn.BCEWithLogitsLoss()
    model = GRUPredictor()
    optimizer = torch.optim.Adam(model.parameters(), lr=.012)
    pre_rng = torch.Generator().manual_seed(1999 + seed)
    for _ in range(pretrain_steps):
        x, y = trajectories(128, 24, .1, pre_rng)
        optimizer.zero_grad()
        loss = loss_fn(model(x)[:, 2:], y[:, 2:])
        loss.backward()
        optimizer.step()

    frozen = copy.deepcopy(model).eval()
    head_only = copy.deepcopy(model).train()
    full = copy.deepcopy(model).train()
    for parameter in head_only.gru.parameters():
        parameter.requires_grad_(False)

    head_opt = torch.optim.Adam(head_only.head.parameters(), lr=.012)
    full_opt = torch.optim.Adam(full.parameters(), lr=.012)
    train_rng = torch.Generator().manual_seed(433000 + seed)

    def measure(step):
        # These fixed external streams are never used for training or model
        # selection; same streams at all checkpoints and across arms.
        return {
            "after_feedback_batches": step,
            "frozen_inverted": round(accuracy(frozen, 777000 + seed, "inverted_parity3"), 5),
            "head_inverted": round(accuracy(head_only, 777000 + seed, "inverted_parity3"), 5),
            "full_inverted": round(accuracy(full, 777000 + seed, "inverted_parity3"), 5),
            "head_original": round(accuracy(head_only, 888000 + seed, "parity3"), 5),
            "full_original": round(accuracy(full, 888000 + seed, "parity3"), 5),
        }

    shock = within_episode_switch_accuracy(frozen, 999000+seed)
    outcomes = [measure(0)]
    for t in range(1, max(CHECKPOINTS) + 1):
        # Update on newly revealed labels only after the current episode has
        # occurred. No future evaluation labels enter this optimization.
        x, y = make_trajectories(128, 24, "inverted_parity3", train_rng)
        for learner, opt in [(head_only, head_opt), (full, full_opt)]:
            opt.zero_grad()
            loss = loss_fn(learner(x)[:, 2:], y[:, 2:])
            loss.backward()
            opt.step()
        if t in CHECKPOINTS:
            outcomes.append(measure(t))
    return {"seed": seed, "within_episode_frozen_switch": shock, "checkpoints": outcomes}


if __name__ == "__main__":
    print(json.dumps({"results": [run(s) for s in [7, 17, 29]],
                      "rule_switch": "parity3 to inverted_parity3",
                      "epsilon": .1,
                      "scope": "Supervised post-shift feedback with online parameter updates; known rule-switch point"}, indent=2))
