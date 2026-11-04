"""Posthoc external deduplication for bounded attention; every step/raw remains retained."""
from pathlib import Path
import json,sys,collections
R=Path(__file__).resolve().parent;E=R.parent/'source-access-three-cycle-v1/cycle3/environment';end=int(sys.argv[1]);start=max(205,end-20);groups={}
for i in range(start,end):
 x=json.loads((E/'events'/f'{i:06d}.json').read_text());k=x['text'];g=groups.setdefault(k,dict(text=k,steps=[],host_kinds=[],stops=[]));g['steps'].append(i);g['host_kinds'].append(x['host_result']['kind']);g['stops'].append(x['stop'])
obj=dict(scope='Exact reply deduplication only, all step memberships and raw records retained; not semantic novelty scoring',start=start,end=end,groups=list(groups.values()))
with (R/f'{end:03}_UNIQUE_TEXTS.json').open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
print(json.dumps(obj,indent=2))
