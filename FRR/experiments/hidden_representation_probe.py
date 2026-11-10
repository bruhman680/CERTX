"""Linear readouts of hidden GRU states in the noisy 8-state parity world.

Decoding from hidden state is correlational, not evidence for causal storage.
Train/evaluation streams are independently generated; probe labels are never
used to train the GRU, only its original next-bit prediction task is.
"""

import copy
import json

import torch
from torch import nn
from eight_state_nonlumpable_rnn import GRUPredictor, trajectories


def train_predictor(seed, steps=450):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    model = GRUPredictor()
    initial = copy.deepcopy(model)
    rng = torch.Generator().manual_seed(1999 + seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=.012)
    loss_fn = nn.BCEWithLogitsLoss()
    for _ in range(steps):
        x, target = trajectories(128, 24, .1, rng)
        optimizer.zero_grad()
        loss = loss_fn(model(x)[:, 2:], target[:, 2:])
        loss.backward()
        optimizer.step()
    return initial.eval(), model.eval()


@torch.no_grad()
def make_probe_data(model, rng_seed, nseq=768):
    x, y = trajectories(nseq, 24, .1, torch.Generator().manual_seed(rng_seed))
    hidden = model.gru(x)[0][:, 2:].reshape(-1, 16).detach()
    t0, t1, t2 = x[:, 2:], x[:, 1:-1], x[:, :-2]
    parity = ((t0 != t1) != t2).float()
    labels = torch.cat([t0, t1, t2, parity], -1).reshape(-1, 4)
    return hidden, labels


def linear_probe(train_x, train_y, eval_x, eval_y, seed, shuffled=False):
    torch.manual_seed(seed)
    probe = nn.Linear(16, 4)
    optimizer = torch.optim.Adam(probe.parameters(), lr=.035)
    if shuffled:
        indices = torch.randperm(train_y.shape[0])
        train_y = train_y[indices]
    criterion = nn.BCEWithLogitsLoss()
    for _ in range(350):
        optimizer.zero_grad()
        loss = criterion(probe(train_x), train_y)
        loss.backward()
        optimizer.step()
    with torch.no_grad():
        acc = ((probe(eval_x) >= 0).float() == eval_y).float().mean(0).tolist()
    return [round(v, 5) for v in acc]


def trial(seed):
    untrained, trained = train_predictor(seed)
    records = {}
    for tag, model in [('trained', trained), ('random_untrained', untrained)]:
        train_x, train_y = make_probe_data(model, 300000 + seed)
        eval_x, eval_y = make_probe_data(model, 700000 + seed)
        records[tag] = linear_probe(train_x, train_y, eval_x, eval_y, seed + 100)
        if tag == 'trained':
            records['shuffled_label_negative_control'] = linear_probe(
                train_x, train_y, eval_x, eval_y, seed + 200, shuffled=True)
    return {"seed": seed, "column_order": ["current", "previous_1", "previous_2", "parity"], **records}


if __name__ == '__main__':
    print(json.dumps({"trials": [trial(s) for s in [7, 17, 29]],
                      "interpretation": "Linear decodability only, no causal intervention"}, indent=2))
