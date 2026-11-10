"""Noisy eight-state parity register, with nonlumpable current-bit projection.

S_t=(a_t,b_t,c_t), observation a_t, next bit z=a_t XOR b_t XOR c_t XOR noise,
S_(t+1)=(z,a_t,b_t), noise ~ Bernoulli(epsilon). For epsilon=.1, next-bit
distributions from same-visible states with differing hidden parity have
total-variation distance .8. All eight microstates affect transition structure.
"""

import argparse
import json
import torch
from torch import nn


class GRUPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.gru = nn.GRU(1, 16, batch_first=True)
        self.head = nn.Linear(16, 1)

    def forward(self, obs):
        return self.head(self.gru(obs)[0])


def trajectories(batch, length, eps, generator):
    bits = torch.zeros(batch, length + 1, 1)
    bits[:, :3] = torch.randint(0, 2, (batch, 3, 1), generator=generator).float()
    noise = (torch.rand(batch, length - 2, 1, generator=generator) < eps)
    for t in range(2, length):
        parity = ((bits[:, t] != bits[:, t - 1]) != bits[:, t - 2])
        bits[:, t + 1] = (parity != noise[:, t - 2]).float()
    return bits[:, :-1], bits[:, 1:]


def trial(seed, eps=.1, steps=450):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    generator = torch.Generator().manual_seed(seed + 1999)
    model = GRUPredictor()
    optimizer = torch.optim.Adam(model.parameters(), lr=.012)
    criterion = nn.BCEWithLogitsLoss()
    model.train()
    for _ in range(steps):
        x, y = trajectories(128, 24, eps, generator)
        optimizer.zero_grad()
        loss = criterion(model(x)[:, 2:], y[:, 2:])
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        x, y = trajectories(1024, 24, eps, torch.Generator().manual_seed(999000 + seed))
        logits = model(x)[:, 2:]
        accuracy = ((logits >= 0).float() == y[:, 2:]).float().mean().item()
        reset_logits = model(x[:, 2:].reshape(-1, 1, 1)).reshape(-1)
        reset_accuracy = ((reset_logits >= 0).float() == y[:, 2:].reshape(-1)).float().mean().item()
    return {"seed": seed, "recurrent_accuracy": round(accuracy, 6),
            "reset_each_step_accuracy": round(reset_accuracy, 6)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=450)
    parser.add_argument("--seeds", nargs="+", type=int, default=[7, 17, 29])
    args = parser.parse_args()
    result = [trial(s, steps=args.steps) for s in args.seeds]
    print(json.dumps({"epsilon": .1, "one_step_lumpability_defect": .8,
                      "current_only_bayes_accuracy": .5, "two_bit_history_bayes_accuracy": .5,
                      "three_bit_history_bayes_accuracy": .9,
                      "results": result, "evaluation": "Independent held-out trajectories"}, indent=2))
