"""Exact 32-state joint rule/microstate Bayes filter under noisy observations.

Four known binary transition rules x eight hidden microstates, with symmetric
rule-hazard mixing. Forecasts precede observation of the next corrupted bit.
No true-state or true-rule labels enter the learner's filter.
"""

import itertools
import json
import numpy as np
from change_detection import RULES, deterministic, generate


STATES = list(itertools.product((0, 1), repeat=3))
LOOKUP = {s: i for i, s in enumerate(STATES)}
BITS = np.asarray([s[0] for s in STATES])
EPSILON = .1


def make_transition():
    matrices = np.zeros((4, 8, 8))
    for r, rule in enumerate(RULES):
        for i, (a,b,c) in enumerate(STATES):
            predicted = deterministic(rule,a,b,c)
            for z, p in ((predicted, 1-EPSILON), (1-predicted, EPSILON)):
                matrices[r,i,LOOKUP[(z,a,b)]] += p
    assert np.allclose(matrices.sum(axis=2), 1)
    return matrices


P = make_transition()


def initial(observed, sensor):
    prob = np.full((4,8), 1/32)
    for lag, value in enumerate(observed[:3]):
        matches=np.asarray([s[2-lag] == value for s in STATES])
        likelihood = np.where(matches, 1-sensor, sensor)
        prob *= likelihood[None,:]
        prob /= prob.sum()
    return prob


def exact_filter(true, observed, switch_t, sensor, hazard):
    """Track four-rule mixture and fixed-old-law 8-state sensor HMM.

    `true` is for scoring only; never used for predictive filtering.
    """
    joint=initial(observed, sensor)
    fixed=joint.sum(axis=0)
    records=[]
    for t in range(2,len(true)-1):
        rule_prior=(1-hazard)*joint+hazard*joint.sum(axis=0)[None,:]/4
        propagated=np.einsum('rs,rsn->rn',rule_prior,P)
        fixed_prop=fixed@P[0]
        p1=float(propagated[:, BITS==1].sum())
        p1fixed=float(fixed_prop[BITS==1].sum())
        outcome=int(true[t+1])
        obs=int(observed[t+1])
        likelihood=np.where(BITS==obs,1-sensor,sensor)
        joint=propagated*likelihood[None,:]
        joint/=joint.sum()
        fixed=fixed_prop*likelihood
        fixed/=fixed.sum()
        records.append((t, outcome, p1,p1fixed,float(joint[1].sum()),float(joint[0].sum()),
                        float(np.max(joint[1:].sum(axis=1)))))
    return records


def score(rows,switch):
    arr=np.asarray(rows)
    output={}
    for window,mask in (("pre",arr[:,0]<switch),
                        ("early",(arr[:,0]>=switch)&(arr[:,0]<switch+5)),
                        ("late",arr[:,0]>=switch+5)):
        y=arr[mask,1]
        output[window]={}
        for name,column in (("hybrid",2),("fixed",3)):
            p=np.clip(arr[mask,column],1e-9,1-1e-9)
            output[window][name]=(float(np.mean((p>=.5)==y)),float(np.mean(-(y*np.log(p)+(1-y)*np.log(1-p)))))
    streak=0; delay=None
    for row in rows:
        if row[0]<switch:continue
        streak = streak+1 if row[4]>.8 else 0
        if streak>=3:
            delay=int(row[0]-switch+1)
            break
    return output,delay


def run(seed,episodes=150,sensor=.1,hazard=.03):
    rng=np.random.default_rng(seed)
    totals={w:{m:[] for m in ("hybrid","fixed")} for w in ("pre","early","late")}
    delays=[]; false_alarms=[]; confirmed_alternative_alarms=[]
    for _ in range(episodes):
        switch=int(rng.integers(24,41))
        actual=generate(rng,64,switch,"xor3","inverse_xor3",EPSILON)
        observed=actual ^ (rng.random(64)<sensor).astype(np.int8)
        rows=exact_filter(actual,observed,switch,sensor,hazard)
        out,delay=score(rows,switch)
        delays.append(delay)
        for w in totals:
            for m in totals[w]: totals[w][m].append(out[w][m])
        original=generate(rng,64,64,"xor3","inverse_xor3",EPSILON)
        null_obs=original ^ (rng.random(64)<sensor).astype(np.int8)
        null_rows=exact_filter(original,null_obs,64,sensor,hazard)
        streak=0; alarm=False; alternative_streak=0; alternative_alarm=False
        for t,_,_,_,_,oldposterior,max_alternative in null_rows:
            if t<12:continue
            streak=streak+1 if oldposterior<.2 else 0
            alternative_streak=alternative_streak+1 if max_alternative>.8 else 0
            if streak>=3:alarm=True
            if alternative_streak>=3:alternative_alarm=True
        false_alarms.append(alarm)
        confirmed_alternative_alarms.append(alternative_alarm)
    aggregate={}
    for window,models in totals.items():
        aggregate[window]={name:{"accuracy":round(float(np.mean(np.asarray(values)[:,0])),5),
                                  "logloss":round(float(np.mean(np.asarray(values)[:,1])),5)}
                           for name,values in models.items()}
    found=[x for x in delays if x is not None]
    aggregate.update({"sensor":sensor,"hazard":hazard,"seed":seed,"episodes":episodes,
                      "detection_fraction":round(len(found)/episodes,4),
                      "median_delay":float(np.median(found)) if found else None,
                      "no_change_broad_old_rule_rejection":round(float(np.mean(false_alarms)),4),
                      "no_change_confirmed_alternative_alarm":round(float(np.mean(confirmed_alternative_alarms)),4)})
    return aggregate


if __name__=="__main__":
    results=[run(seed,episodes=150,sensor=sensor,hazard=hazard)
             for sensor in (0.,.1) for hazard in (.003,.03,.15) for seed in (7,17,29)]
    print(json.dumps({"model":"exact joint 4-rule x 8-microstate filter", "results":results},indent=2))
