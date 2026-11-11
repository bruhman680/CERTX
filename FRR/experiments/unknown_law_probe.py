"""Open-set rule challenge for a four-hypothesis parity tracker.

The unseen rule is c XOR (a AND b), a nonlinear eight-state transition.
All observations are true bits; each next-bit forecast precedes its feedback.
Threshold is calibrated solely on separate no-switch development episodes.
"""
import json
import numpy as np
from change_detection import RULES, deterministic, probability_one

EPS=.1
HAZARD=.03
LENGTH=96
W=12


def truth(rule,a,b,c):
    if rule=="nonlinear_and":
        return c ^ (a & b)
    return deterministic(rule,a,b,c)


def generate(rng, kind):
    bits=np.zeros(LENGTH,dtype=np.int8)
    bits[:3]=rng.integers(0,2,size=3)
    switch=int(rng.integers(30,51))
    for t in range(2,LENGTH-1):
        rule="xor3" if kind=="none" or t<switch else ("inverse_xor3" if kind=="known" else "nonlinear_and")
        bits[t+1]=truth(rule,int(bits[t]),int(bits[t-1]),int(bits[t-2])) ^ int(rng.random()<EPS)
    return bits,switch


def trajectory(bits):
    posterior=np.full(len(RULES),.25)
    forecast=[]
    losses=[]
    for t in range(2,LENGTH-1):
        a,b,c=map(int,(bits[t],bits[t-1],bits[t-2]))
        prior=(1-HAZARD)*posterior+HAZARD*.25
        candidates=np.array([probability_one(rule,a,b,c,EPS) for rule in RULES])
        p=float(prior @ candidates)
        y=int(bits[t+1])
        forecast.append(p)
        losses.append(-np.log(p if y else 1-p))
        likelihood=candidates if y else (1-candidates)
        posterior=prior*likelihood
        posterior/=posterior.sum()
    return np.array(forecast),np.array(losses)


def rolling_past(losses):
    # At index i the abstention decision uses *only* losses at earlier times.
    novelty=np.full(len(losses),np.nan)
    for i in range(W,len(losses)):
        novelty[i]=float(np.mean(losses[i-W:i]))
    return novelty


def assess(kind,seed,n,threshold):
    rng=np.random.default_rng(seed)
    rows=[]
    for _ in range(n):
        bits,switch=generate(rng,kind)
        prob,losses=trajectory(bits)
        novelty=rolling_past(losses)
        ys=bits[3:]
        valid=np.arange(len(prob))>=W
        # Match the pseudo-switch evaluation window even for never-change
        # controls: each arm has equal horizon exposure after a randomized
        # unannounced time, preventing warm-up length from confounding metrics.
        post=(np.arange(len(prob))+2)>=switch
        eligible=valid & post
        accepted=eligible & (novelty<=threshold)
        alarm=eligible & (novelty>threshold)
        correct=(prob>=.5)==ys
        rows.append((bool(np.any(alarm)),int(np.sum(eligible)),int(np.sum(accepted)),
                     int(np.sum(correct & accepted)),int(np.sum(correct & eligible)),
                     float(np.mean(losses[eligible]))))
    a=np.array(rows,dtype=float)
    return {"episodes":n,"episode_alarm_fraction":round(float(np.mean(a[:,0])),4),
            "coverage":round(float(a[:,2].sum()/a[:,1].sum()),4),
            "accepted_accuracy":round(float(a[:,3].sum()/a[:,2].sum()),4) if a[:,2].sum() else None,
            "raw_accuracy":round(float(a[:,4].sum()/a[:,1].sum()),4),
            "mean_logloss":round(float(np.mean(a[:,5])),4)}


def main():
    # Development calibration: 300 *independent* no-switch episodes. A 95th
    # percentile of maximum past-window surprise bounds event-level false alarms
    # only empirically for this generated known-rule null.
    rng=np.random.default_rng(312553)
    maxima=[]
    for _ in range(300):
        bits,_=generate(rng,"none")
        _,ll=trajectory(bits)
        maxima.append(float(np.nanmax(rolling_past(ll))))
    threshold=float(np.quantile(maxima,.95))
    results={kind:[assess(kind,seed,500,threshold) for seed in (7,17,29)] for kind in ("none","known","unknown")}
    print(json.dumps({"candidate_rules":RULES,"unseen_rule":"c XOR (a AND b)",
                      "threshold":round(threshold,6),"calibration":"95th percentile max 12-step past log-loss; 300 no-switch development episodes",
                      "results":results},indent=2))


if __name__=="__main__":
    main()
