"""Independent-sequence recurrent-memory probe on an eight-state shift register.

At t, the (unobserved) microstate is (x[t], x[t-1], x[t-2]), i.e. one of eight
binary states. Independent fair bits drive transitions. The current observation
is x[t]. The supervised outcome is XOR(x[t], x[t-delay]). For delay=1 this
outcome is a deterministic function of the eight-state microstate. For delay>2
it is NOT: the wider history is an explicit extension, not an eight-state claim.
"""

import argparse
import json

import torch
from torch import nn


class RNNPredictor(nn.Module):
    def __init__(self, hidden=16):
        super().__init__()
        self.rnn = nn.GRU(1, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 1)

    def forward(self, inputs):
        features, _ = self.rnn(inputs)
        return self.head(features)


def make_batch(batch, length, delay, generator):
    bits = torch.randint(0, 2, (batch, length, 1), generator=generator).float()
    target = torch.zeros_like(bits)
    target[:, delay:] = (bits[:, delay:] != bits[:, :-delay]).float()
    return bits, target


def train_trial(seed, delay=1, steps=500, length=24, batch=128):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    generator = torch.Generator().manual_seed(seed + 987)
    model = RNNPredictor()
    optimizer = torch.optim.Adam(model.parameters(), lr=.012)
    criterion = nn.BCEWithLogitsLoss()
    model.train()
    for _ in range(steps):
        x, target = make_batch(batch, length, delay, generator)
        optimizer.zero_grad()
        prediction = model(x)
        loss = criterion(prediction[:, delay:], target[:, delay:])
        loss.backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        test_gen = torch.Generator().manual_seed(700000 + seed)
        x, target = make_batch(1024, length, delay, test_gen)
        logits = model(x)[:, delay:]
        acc = ((logits >= 0).float() == target[:, delay:]).float().mean().item()
        loss = criterion(logits, target[:, delay:]).item()
        # Reset the trained GRU for each observation: its input then contains
        # only x_t, not any within-sequence historical information.
        reset_logits = model(x[:, delay:].reshape(-1, 1, 1)).reshape(-1)
        reset_acc = ((reset_logits >= 0).float() == target[:, delay:].reshape(-1)).float().mean().item()
        # Independently generated held-out sequences, not individual held-out
        # states. Feedforward current-only is Bayes-optimal at 50% in this toy.
    return {"seed": seed, "delay": delay, "accuracy": round(acc, 6), "loss": round(loss, 6),
            "hidden_reset_each_step_accuracy": round(reset_acc, 6)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=500)
    parser.add_argument("--delays", type=int, nargs="+", default=[1, 2, 3, 6])
    parser.add_argument("--seeds", type=int, nargs="+", default=[7, 17, 29])
    args = parser.parse_args()
    results = [train_trial(seed, delay, args.steps) for delay in args.delays for seed in args.seeds]
    print(json.dumps({"results": results, "feedforward_current_only_bayes_accuracy": .5,
                      "note": "Only delays 1 and 2 are eight-state target readouts; longer delays require extended history"}, indent=2))
