"""Observation-corruption robustness for a noisy three-bit parity world.

World: S_t=(x_t,x_(t-1),x_(t-2)), x_(t+1)=parity(S_t) XOR eta_t.
The model receives independently bit-flipped observations o_t=x_t XOR xi_t,
but the target remains the actual clean x_(t+1). Held-out worlds are generated
independently from training worlds; matching test batches compare checkpoints.
"""

import argparse
import json

import torch
from torch import nn


class Predictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.GRU(1, 16, batch_first=True)
        self.head = nn.Linear(16, 1)

    def forward(self, obs):
        states, _ = self.net(obs)
        return self.head(states)


def make_world(batch, length, transition_error, observation_error, generator):
    bits = torch.zeros(batch, length + 1, 1)
    bits[:, :3] = torch.randint(0, 2, (batch, 3, 1), generator=generator).float()
    eta = torch.rand(batch, length - 2, 1, generator=generator) < transition_error
    for t in range(2, length):
        parity = (bits[:, t] != bits[:, t - 1]) != bits[:, t - 2]
        bits[:, t + 1] = (parity != eta[:, t - 2]).float()
    obs_flip = torch.rand(batch, length, 1, generator=generator) < observation_error
    observations = (bits[:, :-1].bool() != obs_flip).float()
    return observations, bits[:, 1:]


def train(seed, observation_error, steps, length=24):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    model = Predictor()
    opt = torch.optim.Adam(model.parameters(), lr=.012)
    loss_fn = nn.BCEWithLogitsLoss()
    gen = torch.Generator().manual_seed(seed + 25000 + int(1000 * observation_error))
    for _ in range(steps):
        x, y = make_world(128, length, .1, observation_error, gen)
        opt.zero_grad()
        loss = loss_fn(model(x)[:, 2:], y[:, 2:])
        loss.backward()
        opt.step()
    return model.eval()


def evaluate(model, seed, observation_error, length=24):
    gen = torch.Generator().manual_seed(990000 + seed + int(1000 * observation_error))
    x, y = make_world(2048, length, .1, observation_error, gen)
    with torch.no_grad():
        pred = model(x)[:, 2:]
        score = ((pred >= 0).float() == y[:, 2:]).float().mean().item()
        # One-step calls remove recurrent access to past observations.
        reset_pred = model(x[:, 2:].reshape(-1, 1, 1)).reshape(-1)
        reset_score = ((reset_pred >= 0).float() == y[:, 2:].reshape(-1)).float().mean().item()
    return round(score, 6), round(reset_score, 6)


def run(steps=350, seeds=(7, 17, 29), observation_error=.1):
    rows = []
    for seed in seeds:
        clean = train(seed, 0, steps)
        noisy = train(seed, observation_error, steps)
        c0, reset_c0 = evaluate(clean, seed, 0)
        cn, reset_cn = evaluate(clean, seed, observation_error)
        nn, reset_nn = evaluate(noisy, seed, observation_error)
        rows.append({"seed": seed, "clean_train_clean_eval": c0,
                     "clean_train_noisy_eval": cn,
                     "noisy_train_noisy_eval": nn,
                     "hidden_reset_noisy_eval_clean_train": reset_cn,
                     "hidden_reset_noisy_eval_noisy_train": reset_nn,
                     "hidden_reset_clean_eval_clean_train": reset_c0})
    return {"transition_noise": .1, "observation_noise": observation_error,
            "steps_per_model": steps, "test_sequences": 2048,
            "results": rows, "scope": "Constructed eight-state world; no natural-memory or generalized-robustness claim"}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--steps", type=int, default=350)
    p.add_argument("--observation-error", type=float, default=.1)
    args = p.parse_args()
    print(json.dumps(run(steps=args.steps, observation_error=args.observation_error), indent=2))
