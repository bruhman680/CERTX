"""Reference gating with noisy observations and explicit source ancestry.

Synthetic task, not semantic reasoning. Truth is reserved for scoring; gate sees
only noisy observations and declared source independence. All policies get the
same scheduled audit opportunities and generated observation budget.
"""
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
POLICIES=['executor_only','blind_audit','evidence_gate','provenance_gate']

def run(seed,policy,quality,source):
    rng=np.random.default_rng(seed)
    n=48; steps=120
    old=rng.choice([-1.,1.],n)
    x=old+rng.normal(0,.1,n)
    # Same noise streams across policies; audit observation may share ref cause.
    live_noise=rng.normal(0,.5,(steps,n))
    audit_noise=rng.normal(0,.5,(steps,n))
    accepted=0; events=[]; errors=[]
    for t in range(steps):
        truth=-old if quality=='stale' and t>=60 else old
        reference=truth if quality=='correct' else -truth if quality=='wrong' else old
        measurement=truth+live_noise[t]
        x=.97*x+.03*measurement
        if t%5==0:
            independent=source=='independent'
            observation=(truth if independent else reference)+audit_noise[t]
            candidate=.65*x+.35*reference
            improvement=float(np.mean((x-observation)**2)-np.mean((candidate-observation)**2))
            accept=policy=='blind_audit' or (policy=='evidence_gate' and improvement>.02) or (policy=='provenance_gate' and independent and improvement>.02)
            if accept:x=candidate;accepted+=1
            events.append(dict(step=t,improvement=improvement,independent=independent,accepted=accept))
        errors.append(float(np.mean((x-truth)**2)))
    return dict(seed=seed,policy=policy,reference_quality=quality,audit_source=source,
                accepted_audits=accepted,attempts=24,final_mse=errors[-1],
                last20_mse=float(np.mean(errors[-20:])),events=events,trajectory_mse=errors)

def main():
    rows=[run(s,p,q,c) for s in range(30) for p in POLICIES
          for q in ['correct','wrong','stale'] for c in ['independent','shared_reference']]
    summary=[]
    for p in POLICIES:
        for q in ['correct','wrong','stale']:
            for c in ['independent','shared_reference']:
                group=[a for a in rows if (a['policy'],a['reference_quality'],a['audit_source'])==(p,q,c)]
                summary.append(dict(policy=p,reference_quality=q,audit_source=c,
                    mean_final_mse=float(np.mean([a['final_mse'] for a in group])),
                    mean_last20_mse=float(np.mean([a['last20_mse'] for a in group])),
                    mean_accepted=float(np.mean([a['accepted_audits'] for a in group]))))
    result=dict(kind='constructed noisy-evidence controller; no AI-agent reasoning test',
                settings=dict(seeds=30,sites=48,steps=120,audit_opportunities=24,improvement_margin=.02),
                summary=summary,rows=rows,limits=[
                'Known synthetic observations encode truth; no real-world evidence validity established.',
                'Source ancestry is explicitly supplied to provenance gate; inferred ancestry remains untested.',
                'Equal opportunities and observation budgets, different accepted mutations; actual accepted counts recorded.',
                'No threshold tuning or held-out semantic evaluation; outcomes exploratory.',
                'Stale condition changes truth at step60, distinct from static wrong-reference condition.',
                'All gates still depend on measurement quality and provenance accuracy.'])
    (ROOT/'evaluation/results/evidence-gated-rotation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
