"""Matched feedforward/recurrent baselines for a noisy 8-state parity process.

S_t=(x_t,x_(t-1),x_(t-2)), x_(t+1)=xor(S_t) xor eta_t.
With independent Bernoulli(.1) innovations, the uniform eight-state law is
stationary. This tests prediction on independent synthetic trajectories.
"""

import argparse
import itertools
import json

import torch
from torch import nn


def samples(batch, length, eps, gen):
    bits = torch.zeros(batch, length + 1, 1)
    bits[:, :3] = torch.randint(0, 2, (batch, 3, 1), generator=gen).float()
    noise = torch.rand(batch, length - 2, 1, generator=gen) < eps
    for t in range(2, length):
        parity = (bits[:, t] != bits[:, t - 1]) != bits[:, t - 2]
        bits[:, t + 1] = (parity != noise[:, t - 2]).float()
    return bits[:, :-1], bits[:, 1:]


def windows(x, k):
    # Compare all models on prediction times t >= 2, avoiding missing lags.
    return torch.cat([x[:, 2 - lag : x.shape[1] - lag] for lag in range(k)], dim=-1)


class FeedForward(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(width, 32), nn.Tanh(),
                                 nn.Linear(32, 32), nn.Tanh(), nn.Linear(32, 1))

    def forward(self, x):
        return self.net(x)


class Recurrent(nn.Module):
    def __init__(self, kind):
        super().__init__()
        layer = {"gru": nn.GRU, "lstm": nn.LSTM, "rnn": nn.RNN}[kind]
        self.core = layer(1, 16, batch_first=True)
        self.head = nn.Linear(16, 1)

    def forward(self, x):
        return self.head(self.core(x)[0])[:, 2:]


def fit(kind, seed, steps=450, eps=.1):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    gen = torch.Generator().manual_seed(11000 + seed)
    model = FeedForward(int(kind[-1])) if kind.startswith("ff") else Recurrent(kind)
    optimizer = torch.optim.Adam(model.parameters(), lr=.012)
    criterion = nn.BCEWithLogitsLoss()

    def logits(x):
        return model(windows(x, int(kind[-1]))) if kind.startswith("ff") else model(x)

    model.train()
    for _ in range(steps):
        x, target = samples(128, 24, eps, gen)
        optimizer.zero_grad()
        loss = criterion(logits(x), target[:, 2:])
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        x, target = samples(1024, 24, eps, torch.Generator().manual_seed(500000 + seed))
        predictions = logits(x)
        accuracy = ((predictions >= 0).float() == target[:, 2:]).float().mean().item()
        loss = criterion(predictions, target[:, 2:]).item()
    return {"architecture": kind, "seed": seed, "accuracy": round(accuracy, 6),
            "cross_entropy": round(loss, 6)}


def exact_bayes(eps):
    result = {}
    for window in (1, 2, 3):
        grouped = {}
        for bits in itertools.product((0, 1), repeat=3):
            key = bits[:window]
            p1 = (1 - eps) if sum(bits) % 2 else eps
            grouped.setdefault(key, []).append(p1)
        result[f"ff{window}"] = sum(max(sum(v) / len(v), 1 - sum(v) / len(v))
                                      for v in grouped.values()) / len(grouped)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=450)
    parser.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 29])
    parser.add_argument("--models", nargs="+", default=["ff1", "ff2", "ff3", "rnn", "gru", "lstm"])
    args = parser.parse_args()
    print(json.dumps({"noise_probability": .1,
                      "exact_bayes": exact_bayes(.1),
                      "heldout": [fit(model, seed, args.steps)
                                  for model in args.models for seed in args.seeds]}, indent=2))
