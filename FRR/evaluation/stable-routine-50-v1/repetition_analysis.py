"""Posthoc descriptive literal recurrence check, prompted by145packet; no model input changes."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;E=R.parent/'source-access-three-cycle-v1/cycle3/environment'
rows=[json.loads((E/'events'/f'{i:06d}.json').read_text()) for i in range(105,155)]
index=[dict(step=x['step'],exact_your_f_lines=sum(line.strip()=='YOUR F' for line in x['text'].splitlines()),cap=x['stop']=='token_limit') for x in rows];blocks=[]
for start in range(105,155,10):
 xs=[x for x in index if start<=x['step']<start+10];blocks.append(dict(start=start,end=start+10,replies_with_three_or_more_exact_your_f_lines=sum(x['exact_your_f_lines']>=3 for x in xs),exact_your_f_lines=sum(x['exact_your_f_lines'] for x in xs),caps=sum(x['cap'] for x in xs)))
result=dict(status='descriptive_posthoc',selection='Chosen after145packet showed repeated fragments. Literal threshold>=3 arbitrary; all50retained/used. Not a preregistered endpoint, mechanism test or general semantic novelty/degeneration score. Fixed96outputcaps censor continuations.',blocks=blocks,index=index)
with (R/'REPETITION.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(blocks,indent=2))
