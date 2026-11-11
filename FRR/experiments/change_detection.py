"""Eight-state parity world: exact online rule tracking under abrupt change.

The true bit sequence is observed (no sensor noise). Four fixed candidate
transition laws have 10% flip noise. A Bayesian hypothesis tracker permits
rule switching with a declared per-step hazard and updates on true outcomes.
"""

import argparse
import json
import math
import numpy as np


RULES = ("xor3", "inverse_xor3", "a_xor_c", "b_xor_c")


def deterministic(rule, a, b, c):
    if rule == "xor3":
        return a ^ b ^ c
    if rule == "inverse_xor3":
        return 1 ^ a ^ b ^ c
    if rule == "a_xor_c":
        return a ^ c
    if rule == "b_xor_c":
        return b ^ c
    raise ValueError(rule)


def probability_one(rule, a, b, c, epsilon):
    return (1-epsilon) if deterministic(rule, a, b, c) else epsilon


def generate(generator, length, switch_t, old_rule, new_rule, epsilon):
    bits = generator.integers(0, 2, size=length, dtype=np.int8)
    for t in range(2, length - 1):
        rule = old_rule if t < switch_t else new_rule
        predicted = deterministic(rule, int(bits[t]), int(bits[t-1]), int(bits[t-2]))
        bits[t + 1] = predicted ^ int(generator.random() < epsilon)
    return bits


def score_sequence(bits, switch_t, old_rule, new_rule, epsilon=.1, hazard=.03):
    posterior = np.full(len(RULES), 1/len(RULES), dtype=float)
    records=[]
    for t in range(2, len(bits)-1):
        a,b,c = (int(bits[t]),int(bits[t-1]),int(bits[t-2]))
        actual = int(bits[t+1])
        true_rule = old_rule if t < switch_t else new_rule
        likelihood_p1 = np.array([probability_one(r,a,b,c,epsilon) for r in RULES])
        # Symmetric Markov hazard: with probability h resample a rule uniformly.
        prior = (1-hazard)*posterior + hazard/len(RULES)
        predictions={
            "oracle": probability_one(true_rule,a,b,c,epsilon),
            "fixed": probability_one(old_rule,a,b,c,epsilon),
            "bayes": float(np.dot(prior,likelihood_p1)),
        }
        likelihood = likelihood_p1 if actual else (1-likelihood_p1)
        posterior = prior*likelihood
        posterior = posterior/posterior.sum()
        records.append({"t":t,"actual":actual,"true_rule":true_rule,
                        "predictions":predictions,
                        "posterior_true":float(posterior[RULES.index(true_rule)]),
                        "posterior_new":float(posterior[RULES.index(new_rule)])})
    return records


def summarize(records, switch_t):
    windows={
        "pre": [v for v in records if v["t"]<switch_t],
        "post_early": [v for v in records if switch_t<=v["t"]<switch_t+5],
        "post_late": [v for v in records if v["t"]>=switch_t+5],
        "post_all": [v for v in records if v["t"]>=switch_t],
    }
    outcome={}
    for name,rows in windows.items():
        outcome[name]={}
        for predictor in ("oracle","fixed","bayes"):
            ps=np.array([r["predictions"][predictor] for r in rows])
            ys=np.array([r["actual"] for r in rows])
            correct=np.mean((ps>=.5)==ys) if len(rows) else float("nan")
            logloss=np.mean(-(ys*np.log(ps)+(1-ys)*np.log(1-ps))) if len(rows) else float("nan")
            outcome[name][predictor]={"accuracy":float(correct),"logloss":float(logloss)}
    streak=0
    outcome["detection_delay"]=None
    for r in records:
        if r["t"]<switch_t:
            continue
        streak = streak+1 if r["posterior_new"]>.8 else 0
        if streak>=3:
            outcome["detection_delay"]=r["t"]-switch_t+1
            break
    return outcome


def experiment(seed, episodes=500, switch_t=32, length=64,
               old_rule="xor3", new_rule="inverse_xor3", epsilon=.1, hazard=.03):
    generator=np.random.default_rng(seed)
    summaries=[]
    no_switch_false_alarms=[]
    for _ in range(episodes):
        actual_switch_t=int(generator.integers(24,41))
        bits=generate(generator,length,actual_switch_t,old_rule,new_rule,epsilon)
        rows=score_sequence(bits,actual_switch_t,old_rule,new_rule,epsilon,hazard)
        summaries.append(summarize(rows,actual_switch_t))
        # Null: no change for the entire episode; an alarm means the posterior
        # on the true old rule fell below 1/2 at any point after warm-up.
        null_bits=generate(generator,length,length,old_rule,new_rule,epsilon)
        null_rows=score_sequence(null_bits,length,old_rule,new_rule,epsilon,hazard)
        consecutive=0
        alarm=False
        for r in null_rows:
            if r["t"]<12:
                continue
            consecutive = consecutive+1 if r["posterior_true"]<.2 else 0
            if consecutive>=3:
                alarm=True
                break
        no_switch_false_alarms.append(alarm)
    out={"seed":seed,"episodes":episodes}
    for window in ("pre","post_early","post_late","post_all"):
        out[window]={}
        for predictor in ("oracle","fixed","bayes"):
            out[window][predictor]={key:round(float(np.mean([s[window][predictor][key] for s in summaries])),6)
                                    for key in ("accuracy","logloss")}
    detected=[s["detection_delay"] for s in summaries]
    out["detection_fraction"]=round(sum(v is not None for v in detected)/episodes,6)
    out["median_detected_delay"]=float(np.median([v for v in detected if v is not None])) if any(v is not None for v in detected) else None
    out["never_change_episode_false_alarm_fraction"]=round(float(np.mean(no_switch_false_alarms)),6)
    return out


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--episodes",type=int,default=500)
    parser.add_argument("--hazard",type=float,default=.03)
    parser.add_argument("--old-rule",choices=RULES,default="xor3")
    parser.add_argument("--new-rule",choices=RULES,default="inverse_xor3")
    args=parser.parse_args()
    assert args.old_rule!=args.new_rule
    print(json.dumps({"parameters":{"transition_noise":.1,"observation_noise":0,
                                     "switch_time":"uniform integer 24..40, unknown to tracker",
                                     "length":64,"hazard":args.hazard,
                                     "old_rule":args.old_rule,"new_rule":args.new_rule},
                      "seeds":[experiment(seed,episodes=args.episodes,hazard=args.hazard,
                                          old_rule=args.old_rule,new_rule=args.new_rule)
                               for seed in (7,17,29)]},indent=2))
