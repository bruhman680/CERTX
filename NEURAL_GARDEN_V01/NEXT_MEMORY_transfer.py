"""Held-out distribution-shift pressure test of compressed-state temporal memory.

Fit all next-microstate models on baseline Garden worlds only. Test on new
baseline and changed-regrowth worlds, same eight-category label definition.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

import NEXT_MEMORY_probe as base
import SOC_MACRO_probe as macro

HERE=Path(__file__).parent
MAP3=base.MAPPING


def fit(train, mapping, history):
    x,y,k=macro.transition_data(train,mapping,history)
    counts=np.full((k,8),.5,dtype=float)
    np.add.at(counts,(x,y),1)
    return counts/counts.sum(axis=1,keepdims=True)


def score(test,mapping,history,p):
    x,y,_=macro.transition_data(test,mapping,history)
    per=-np.log(p[x,y]).reshape(test.shape[0],-1,test.shape[2])
    # t indexes refer to source tick; next category at tick+1.
    time=per.mean(axis=(0,2))
    t_start=history
    def window(a,b):
        idx=np.arange(t_start,t_start+len(time))
        mask=(idx>=a)&(idx<b)
        return float(time[mask].mean()) if mask.any() else None
    return {'overall_nll':float(per.mean()),'pre_shift':window(3,159),
            'during_shift':window(160,320),'post_shift':window(321,420),
            'per_seed_nll':per.mean(axis=(1,2)).tolist()}


def main():
    train,_=base.trajectories(base.TRAIN,False)
    tests={'baseline':base.trajectories(base.TEST,False)[0],
           'shifted':base.trajectories(base.TEST,True)[0]}
    configs=[('full8',np.arange(8,dtype=np.int8),0),
             ('coarse3',MAP3,0),('coarse3_history3',MAP3,3)]
    outcome={}
    for name,mapping,history in configs:
        p=fit(train,mapping,history)
        outcome[name]={key:score(test,mapping,history,p) for key,test in tests.items()}
    payload={'orientation':'Does history-enhanced macro prediction trained only in an unchanged world transfer to changed resource-regrowth physics?',
             'train_laws':'original baseline only','test_laws':'baseline or labeled regrowth .055 ticks161–320',
             'seeds_train':base.TRAIN,'seeds_test':base.TEST,
             'results':outcome,
             'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest()
                for f in ['NEXT_MEMORY_probe.py',Path(__file__).name,'SOC_MACRO_probe.py']},
             'cautions':['The original world is stationary in its laws but contains transients.',
                         'Model trained on baseline regime only; no adaptation or retraining during shifted test.',
                         'History reduces uncertainty but transfer can worsen when phase changes.',
                         'Same synthetic simulator family, small seed set.']}
    (HERE/'NEXT_MEMORY_transfer_results.json').write_text(json.dumps(payload,indent=2)+'\n')
    for name in outcome:
        print(name,'baseline',outcome[name]['baseline']['overall_nll'],
              'shifted',outcome[name]['shifted']['overall_nll'],
              'during',outcome[name]['shifted']['during_shift'])


if __name__=='__main__':main()
