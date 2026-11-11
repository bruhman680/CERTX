"""Independent replication of frozen NEXT_GATE sources on reserved seeds.

Protocol and 10200–10211 seeds were frozen in NEXT_GATE_PLAN.md before outcomes.
No gate rule or learning hyperparameter is changed here.
"""
from __future__ import annotations
import hashlib
import json
import platform
from pathlib import Path
from NEXT_GATE_probe import run

ROOT=Path(__file__).parent

def audit():
    z=run(seeds=range(10200,10212),size=10,train_steps=1000,
          test_steps=3000,eval_steps=1500)
    assert len(z['rows'])==12 and len({r['seed'] for r in z['rows']})==12
    assert all(r['matched_initial'] for r in z['rows'])
    root_hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                 for f in ('NEXT_GATE_PLAN.md','NEXT_GATE_garden.py',
                           'NEXT_GATE_probe.py','NEXT_CREDIT_garden.py',
                           'NEXT_WELFARE_garden.py','garden.py',Path(__file__).name)}
    z['independent_audit']={'reserved_seeds_used':list(range(10200,10212)),
        'untouched_primary_seeds':list(range(10100,10112)),
        'protocol':'NEXT_GATE_PLAN.md',
        'source_sha256':root_hashes,
        'outcome_selection':False,
        'platform':{'python':platform.python_version()}}
    (ROOT/'NEXT_GATE_AUDIT_results.json').write_text(json.dumps(z,indent=2)+'\n')
    return z

if __name__=='__main__':
    z=audit()
    for name,s in z['summary'].items():
        print(name,round(s['energy'],5),round(s['floor'],5),
              round(s.get('raw_tail',0),7),s.get('paired_vs_sham_wins'))
