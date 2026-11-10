"""Train on one transition-noise level, test on others without adaptation.

Uses eight-state parity process and GRU from eight_state_nonlumpable_rnn.py.
No observation noise: this is transition-law shift, not a sensor-noise test.
"""

import json
import torch
from torch import nn
from eight_state_nonlumpable_rnn import GRUPredictor, trajectories


def run(seed, train_eps=.1, train_steps=450):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    model = GRUPredictor()
    opt = torch.optim.Adam(model.parameters(), lr=.012)
    criterion = nn.BCEWithLogitsLoss()
    rng = torch.Generator().manual_seed(1999 + seed)
    for _ in range(train_steps):
        x, target = trajectories(128, 24, train_eps, rng)
        opt.zero_grad()
        loss = criterion(model(x)[:, 2:], target[:, 2:])
        loss.backward()
        opt.step()
    model.eval()
    outcomes = []
    with torch.no_grad():
        for idx, eps in enumerate([0., .05, .1, .25, .4, .5]):
            generator = torch.Generator().manual_seed(800000 + seed * 100 + idx)
            x, target = trajectories(2048, 24, eps, generator)
            logits = model(x)[:, 2:]
            acc = ((logits >= 0).float() == target[:, 2:]).float().mean().item()
            outcomes.append({"test_epsilon": eps, "accuracy": round(acc, 6),
                             "full_history_bayes_optimal": round(1-eps, 6)})
    return {"seed": seed, "train_epsilon": train_eps, "tests": outcomes}


if __name__ == "__main__":
    print(json.dumps({"results": [run(seed) for seed in [7,17,29]],
                      "scope": "Transition-distribution shift; no adaptation or new training in test"}, indent=2))
