"""Same-seed strong manually designed controls for deterministic welfare study."""
import hashlib
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import RuleGarden,score

SEEDS=tuple(range(9500,9512))
RULES=('fixed50','rescue','reverse','neighbor')

def run():
    rows=[]
    for seed in SEEDS:
        for regime in ('stable','mild'):
            for rule in RULES:
                g=RuleGarden(seed=seed+20_000,size=10,rule=rule)
                for t in range(1,3001):
                    g.regrowth=.055 if regime=='mild' and 1000<t<=2000 else .06
                    g.step()
                rows.append({'seed':seed,'regime':regime,'rule':rule,
                             'energy':float(g.energy.mean()),
                             'floor':float(np.mean(g.energy<=.01)),
                             'score':score(g)})
    summary={}
    for regime in ('stable','mild'):
        for rule in RULES:
            a=[r for r in rows if r['regime']==regime and r['rule']==rule]
            summary[regime+'/'+rule]={k:float(np.mean([r[k] for r in a]))
                                      for k in ('energy','floor','score')}
    return {'design':{'seeds':SEEDS,'size':10,'test_ticks':3000,'rules':RULES,
                      'strong_manual_controls_selected_before_this_test':True,
                      'world_regimes':['stable','mild .06-.055-.06']},
            'summary':summary,'rows':rows,
            'source_sha256':{f:hashlib.sha256((Path(__file__).parent/f).read_bytes()).hexdigest()
                 for f in ('garden.py','NEXT_WELFARE_study.py',Path(__file__).name)}}

if __name__=='__main__':
    z=run();Path(__file__).with_name('NEXT_WELFARE_rule_controls_results.json').write_text(json.dumps(z,indent=2)+'\n')
    print(json.dumps(z['summary'],indent=2))
