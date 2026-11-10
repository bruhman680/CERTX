"""Eight-state transition-law transfer: fixed GRU trained on noisy XOR3.

All evaluated rules include the oldest bit c so the eight-state shift-register
transition is doubly stochastic (uniform stationary distribution). The model
is never updated after training. This isolates rule identity from noise level.
"""

import json
import torch
from torch import nn
from eight_state_nonlumpable_rnn import GRUPredictor, trajectories


def make_trajectories(batch, length, rule, generator, epsilon=.1):
    bits = torch.zeros(batch, length + 1, 1)
    bits[:, :3] = torch.randint(0, 2, (batch, 3, 1), generator=generator).float()
    noise = torch.rand(batch, length - 2, 1, generator=generator) < epsilon
    for t in range(2, length):
        a = bits[:, t].bool()
        b = bits[:, t - 1].bool()
        c = bits[:, t - 2].bool()
        if rule == "parity3":
            logical = a ^ b ^ c
        elif rule == "inverted_parity3":
            logical = ~(a ^ b ^ c)
        elif rule == "a_xor_c":
            logical = a ^ c
        elif rule == "b_xor_c":
            logical = b ^ c
        else:
            raise ValueError(rule)
        bits[:, t + 1] = (logical ^ noise[:, t - 2]).float()
    return bits[:, :-1], bits[:, 1:]


def run(seed, train_steps=450):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    model = GRUPredictor()
    opt = torch.optim.Adam(model.parameters(), lr=.012)
    criterion = nn.BCEWithLogitsLoss()
    rng = torch.Generator().manual_seed(1999 + seed)
    for _ in range(train_steps):
        inputs, targets = trajectories(128, 24, .1, rng)
        opt.zero_grad()
        loss = criterion(model(inputs)[:, 2:], targets[:, 2:])
        loss.backward()
        opt.step()
    model.eval()
    output = []
    with torch.no_grad():
        for j, rule in enumerate(["parity3", "inverted_parity3", "a_xor_c", "b_xor_c"]):
            rng_test = torch.Generator().manual_seed(990000 + seed * 100 + j)
            inputs, targets = make_trajectories(2048, 24, rule, rng_test)
            logits = model(inputs)[:, 2:]
            output.append({"rule": rule,
                           "accuracy": round(((logits >= 0).float() == targets[:, 2:]).float().mean().item(), 6),
                           "cross_entropy": round(criterion(logits, targets[:, 2:]).item(), 6)})
    return {"seed": seed, "test": output}


if __name__ == "__main__":
    print(json.dumps({"train_rule": "parity3", "transition_noise": .1,
                      "no_adaptation_at_test": True,
                      "results": [run(seed) for seed in [7, 17, 29]]}, indent=2))
