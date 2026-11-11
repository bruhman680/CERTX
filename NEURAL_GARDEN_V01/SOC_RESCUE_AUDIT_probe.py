"""Adversarial long-horizon test of the hand-designed energy-rescue rule.

One research question: does energy-conditioned harvesting beat a well-chosen
constant threshold, or is its apparent gain baseline selection and horizon?
"""

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from garden import Garden


ROOT=Path(__file__).resolve().parent
SEEDS=tuple(range(36_000,36_012))
HORIZON=20_000
SIZE=16

POLICIES={f"fixed_{t:.3f}":{"kind":"fixed","threshold":t}
          for t in (.475,.485,.49,.495,.50,.505,.51,.515,.525)}
for discount in (.01,.025,.04):
    POLICIES[f"rescue_{discount:.3f}"]={"kind":"rescue","threshold":.51,
                                       "discount":discount,"low_energy":.12}
POLICIES["reverse_rescue"]={"kind":"rescue","threshold":.51,
                              "discount":-.025,"low_energy":.12}


def run(seed, policy):
    garden=Garden(seed=seed,size=SIZE,learning=False)
    resource,energy=garden.resource.copy(),garden.energy.copy()
    checkpoints={500,2000,5000,10000,20000}
    path={}
    tail_raw=[]
    low_energy_actions=[]
    high_energy_actions=[]
    conditional_actions=[]
    for t in range(1,HORIZON+1):
        before_r,before_e=resource,energy
        low=before_e<policy.get("low_energy",-.1)
        theta=np.full(garden.count,policy["threshold"])
        if policy["kind"]=="rescue":
            theta=np.where(low,theta-policy["discount"],theta)
        action=(before_r>theta).astype(float)
        resource=np.clip(before_r+.08*(garden._neighbors(before_r)-before_r)
                         +.06*(1-before_r)-.18*before_r*action,0,1)
        raw=.25*before_r*action-.03-.055*action+.008*(1-action)
        energy=np.clip(before_e+raw,0,1)
        if t>HORIZON-1000:
            tail_raw.append(float(raw.mean()))
            conditional_actions.append(float(action.mean()))
            if low.any():low_energy_actions.append(float(action[low].mean()))
            if (~low).any():high_energy_actions.append(float(action[~low].mean()))
        if t in checkpoints:
            path[str(t)]={"mean_energy":float(energy.mean()),
                          "mean_resource":float(resource.mean()),
                          "floor_fraction":float(np.mean(energy<=.01)),
                          "ceiling_fraction":float(np.mean(energy>=.99))}
    return {"seed":seed,"path":path,"raw_tail":float(np.mean(tail_raw)),
            "tail_harvest":float(np.mean(conditional_actions)),
            "low_energy_harvest_if_occupied":None if not low_energy_actions else float(np.mean(low_energy_actions)),
            "high_energy_harvest":float(np.mean(high_energy_actions))}


def main():
    rows=[]
    for name,policy in POLICIES.items():
        data=[run(seed,policy) for seed in SEEDS]
        rows.append({"name":name,"policy":policy,"runs":data,
                     "energy20k":float(np.mean([x["path"][str(HORIZON)]["mean_energy"] for x in data])),
                     "floor20k":float(np.mean([x["path"][str(HORIZON)]["floor_fraction"] for x in data])),
                     "raw_tail":float(np.mean([x["raw_tail"] for x in data])),
                     "harvest_tail":float(np.mean([x["tail_harvest"] for x in data]))})
    byname={x["name"]:x for x in rows}
    target=byname["rescue_0.025"]
    delta={}
    for arm in rows:
        diff=np.array([x["path"][str(HORIZON)]["mean_energy"]-
                      y["path"][str(HORIZON)]["mean_energy"]
                      for x,y in zip(target["runs"],arm["runs"])])
        delta[arm["name"]]={"mean_rescue_minus":float(diff.mean()),
                            "wins":int(np.sum(diff>0)),"losses":int(np.sum(diff<0)),
                            "seed_sd":float(diff.std(ddof=1))}
    payload={"study":"adversarial single research loop: energy-conditioned rescue vs nearby fixed thresholds",
             "world":{"size":SIZE,"horizon":HORIZON,"seeds":SEEDS,
                      "laws":"unchanged v0.1 resource/energy equations",
                      "source_sha256":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                           for f in ("garden.py",Path(__file__).name)},
                      "python":platform.python_version(),"numpy":np.__version__},
             "arms":rows,"rescue_paired_differences":delta,
             "limits":"Posthoc policy choices; same simulator generator; finite horizon; no neural learning, no independent biological replication."
            }
    outfile=ROOT/"SOC_RESCUE_AUDIT_results.json"
    outfile.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"arms":[{"name":x["name"],"energy20k":round(x["energy20k"],5),
                               "floor20k":round(x["floor20k"],5)} for x in rows],
                      "n":len(rows)*len(SEEDS)},indent=2))


if __name__=="__main__":main()
