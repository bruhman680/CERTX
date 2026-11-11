"""Explicit two-timescale 8-state observer: bit history + rule posterior.

This is a transparent algorithm, not a learned meta-cognitive controller.
It forecasts before receiving each realized next bit and updates afterward.
"""

import argparse
import json
import numpy as np

from change_detection import RULES, deterministic, generate, probability_one


def one_episode(bits, change_t, old="xor3", new="inverse_xor3", eps=.1, hazard=.03,
                alarm_threshold=.8, persistence=3):
    belief = np.ones(len(RULES))/len(RULES)
    committed_rule = old
    counter = 0
    pending_candidate = None
    events = []
    for t in range(2, len(bits)-1):
        # Fast explicit observation state: last three seen true bits.
        a,b,c = (int(bits[t]),int(bits[t-1]),int(bits[t-2]))
        true_rule = old if t<change_t else new
        actual = int(bits[t+1])
        p1 = np.array([probability_one(rule,a,b,c,eps) for rule in RULES])
        prior = (1-hazard)*belief + hazard/len(RULES)
        forecasts={
            "oracle": probability_one(true_rule,a,b,c,eps),
            "frozen": probability_one(old,a,b,c,eps),
            "soft_belief": float(prior @ p1),
            "committed": probability_one(committed_rule,a,b,c,eps),
        }
        # All causal: this update comes after scoring the forecast.
        likelihood = p1 if actual else 1-p1
        belief = prior*likelihood
        belief /= belief.sum()
        candidate=int(np.argmax(belief))
        candidate_rule=RULES[candidate]
        if candidate_rule!=committed_rule and belief[candidate]>alarm_threshold:
            counter = counter+1 if candidate_rule==pending_candidate else 1
            pending_candidate = candidate_rule
        else:
            counter = 0
            pending_candidate = None
        changed=False
        if counter >= persistence:
            committed_rule=candidate_rule
            changed=True
            counter=0
            pending_candidate=None
        events.append({"t":t,"actual":actual,"true_rule":true_rule,
                       "forecast":forecasts,"commit":committed_rule,
                       "changed":changed})
    return events


def measure(events, start, end):
    rows=[r for r in events if start<=r["t"]<end]
    out={}
    for key in ("oracle","frozen","soft_belief","committed"):
        ys=np.array([r["actual"] for r in rows]); ps=np.array([r["forecast"][key] for r in rows])
        out[key]={"accuracy":float(np.mean((ps>=.5)==ys)),
                  "log_loss":float(np.mean(-(ys*np.log(ps)+(1-ys)*np.log(1-ps))))}
    return out


def run(seed, n=500, length=64):
    generator=np.random.default_rng(seed)
    switched=[]; unchanged=[]
    for _ in range(n):
        cut=int(generator.integers(24,41))
        bits=generate(generator,length,cut,"xor3","inverse_xor3",.1)
        events=one_episode(bits,cut)
        changes=[r["t"] for r in events if r["changed"] and r["commit"]=="inverse_xor3" and r["t"]>=cut]
        switched.append({"pre":measure(events,2,cut),
                         "early":measure(events,cut,cut+5),
                         "late":measure(events,cut+5,length-1),
                         "delay":changes[0]-cut+1 if changes else None,
                         "false_precommit":sum(r["changed"] for r in events if r["t"]<cut)})
        clean=generate(generator,length,length,"xor3","inverse_xor3",.1)
        unch=one_episode(clean,length)
        unchanged.append(sum(r["changed"] for r in unch)>0)
    summary={"seed":seed,"episodes_per_condition":n,
             "no_switch_any_commit_rate":float(np.mean(unchanged)),
             "pre_switch_ever_committed":float(np.mean([s["false_precommit"]>0 for s in switched]))}
    for window in ("pre","early","late"):
        summary[window]={k:{metric:round(float(np.mean([s[window][k][metric] for s in switched])),6)
                            for metric in ("accuracy","log_loss")}
                         for k in ("oracle","frozen","soft_belief","committed")}
    delays=[s["delay"] for s in switched if s["delay"] is not None]
    summary["detection_fraction"]=len(delays)/n
    summary["median_commit_delay"]=float(np.median(delays)) if delays else None
    return summary


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--episodes",type=int,default=500)
    parser.add_argument("--seeds",type=int,nargs="+",default=[401,502,603])
    args=parser.parse_args()
    print(json.dumps({"description":"Explicit 3-bit observation history plus slow rule-belief/commit controller",
                      "results":[run(seed,args.episodes) for seed in args.seeds]},indent=2))
