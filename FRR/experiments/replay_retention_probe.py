"""Old-law replay vs new-only finetuning after a known parity-law change.

This is a bounded supervised retention/control experiment, not autonomous change
detection. New and replay labels are available only in each update batch.
"""

import copy
import json
import torch
from torch import nn
from eight_state_nonlumpable_rnn import GRUPredictor, trajectories
from rule_shift_probe import make_trajectories
from online_adaptation import accuracy


def run(seed, steps=80):
    torch.manual_seed(seed)
    torch.set_num_threads(2)
    net = GRUPredictor()
    lossfn = nn.BCEWithLogitsLoss()
    optim = torch.optim.Adam(net.parameters(), lr=.012)
    source = torch.Generator().manual_seed(1999 + seed)
    for _ in range(450):
        x, y = trajectories(128, 24, .1, source)
        optim.zero_grad()
        lossfn(net(x)[:,2:], y[:,2:]).backward()
        optim.step()

    new_only, mixed = copy.deepcopy(net), copy.deepcopy(net)
    opt_new = torch.optim.Adam(new_only.parameters(), lr=.012)
    opt_mixed = torch.optim.Adam(mixed.parameters(), lr=.012)
    new_source = torch.Generator().manual_seed(433000 + seed)
    old_source = torch.Generator().manual_seed(622000 + seed)
    checks=[]

    def evaluate(step):
        result={"step": step}
        for label, model in [("new_only", new_only), ("mixed_replay", mixed)]:
            result[label]={
                "inverted_accuracy": round(accuracy(model, 777000+seed, "inverted_parity3"),5),
                "original_accuracy": round(accuracy(model, 888000+seed, "parity3"),5)}
        return result

    checks.append(evaluate(0))
    for t in range(1,steps+1):
        x_new,y_new=make_trajectories(128,24,"inverted_parity3",new_source)
        x_old,y_old=trajectories(128,24,.1,old_source)
        opt_new.zero_grad()
        lossfn(new_only(x_new)[:,2:],y_new[:,2:]).backward()
        opt_new.step()

        opt_mixed.zero_grad()
        loss=.5*lossfn(mixed(x_new)[:,2:],y_new[:,2:]) + .5*lossfn(mixed(x_old)[:,2:],y_old[:,2:])
        loss.backward()
        opt_mixed.step()
        if t in (10,20,40,80):
            checks.append(evaluate(t))
    return {"seed":seed,"checkpoints":checks}


if __name__ == "__main__":
    print(json.dumps({"results":[run(s) for s in [7,17,29]],
                      "scope":"Known switch, supervised fresh and replayed synthetic batches; equal 80 update steps, replay arm sees twice as many labeled examples"},indent=2))
