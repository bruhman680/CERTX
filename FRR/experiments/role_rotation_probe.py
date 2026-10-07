"""Role-switching model: order is measurable; correctness remains separate.

No LLM reasoning evaluated. Auditor contracts toward a reference, executor takes
a task step, wanderer adds noise. Each intervention is explicitly programmed.
"""
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]

def run(seed,policy,initial,reference,budget=24):
    rng=np.random.default_rng(seed)
    n=48
    target=np.tile([-1.,1.],n//2)
    x=target.copy() if initial=='correct' else -target.copy()
    perturbation=rng.normal(0,1,n)
    x = perturbation.copy() if initial=='dispersed' else x+.12*perturbation
    draws=rng.normal(size=(120,n))
    random_times=set(rng.choice(np.arange(120),budget,replace=False).tolist())
    spent=0; roles=[]; hist=[]
    for t in range(120):
        # Sign-independent order parameter measures concentration, not warrant.
        alignment=float(abs(np.mean(x*target))/(np.mean(abs(x))+1e-12))
        residual=float(np.mean((x-target)**2))
        trigger=False
        if spent<budget:
            if policy=='scheduled': trigger=t%5==0
            elif policy=='random': trigger=t in random_times
            elif policy=='coherence_only': trigger=alignment>.9
            elif policy=='dispersion_only': trigger=alignment<.6
            elif policy=='spectrum': trigger=alignment<.6 or alignment>.9
            elif policy=='reference_residual': trigger=residual>.5
        role='AUDITOR' if trigger else 'EXECUTOR'
        if trigger:
            # Reference can be correct or wrong: auditing inherits this choice.
            ref=target if reference=='correct' else -target
            x=.65*x+.35*ref
            spent+=1
        else:
            # Weak task evidence competes with a fixed self-retention component.
            x=.985*x+.015*target+.05*draws[t]
        roles.append(role)
        hist.append(dict(step=t,alignment=alignment,task_mse=residual))
    return dict(seed=seed,policy=policy,initial=initial,reference=reference,
                interventions=spent,final_mse=float(np.mean((x-target)**2)),
                correct_fraction=float(np.mean(np.sign(x)==target)),
                final_alignment=float(abs(np.mean(x*target))/(np.mean(abs(x))+1e-12)),
                roles=roles,history=hist)

def main():
    rows=[run(s,p,i,r) for s in range(20)
          for p in ['fixed','scheduled','random','coherence_only','dispersion_only','spectrum','reference_residual']
          for i in ['correct','wrong','dispersed'] for r in ['correct','wrong']]
    summary=[]
    for p in ['fixed','scheduled','random','coherence_only','dispersion_only','spectrum','reference_residual']:
        for i in ['correct','wrong','dispersed']:
            for r in ['correct','wrong']:
                group=[a for a in rows if (a['policy'],a['initial'],a['reference'])==(p,i,r)]
                summary.append(dict(policy=p,initial=i,reference=r,
                    mean_mse=float(np.mean([a['final_mse'] for a in group])),
                    mean_correct_fraction=float(np.mean([a['correct_fraction'] for a in group])),
                    mean_interventions=float(np.mean([a['interventions'] for a in group]))))
    result=dict(kind='constructed role-switching control; no AI-agent evaluation',
       settings=dict(sites=48,steps=120,seeds=20,max_audit_interventions=24),summary=summary,rows=rows,
       limits=['Coherence reads a known target direction but discards its sign; it is deliberately unable to distinguish correct from inverted consensus.',
               'Residual controller receives direct target access; it is an oracle comparator, not an implemented factual evaluator.',
               'Audit maps explicitly encode reference contraction; gains do not independently validate auditing.',
               'Budget is a shared cap, not an equal realized intervention count; counts are reported.',
               'Thresholds are illustrative, not calibrated or universal.',
               'Wandering/thermal interventions and semantic reasoning are not evaluated.'])
    out=ROOT/'evaluation/results/role-rotation-probe.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
