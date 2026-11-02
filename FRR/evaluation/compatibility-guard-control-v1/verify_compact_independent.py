"""Independent root audit of published vectors, supplied summary and saved inputs."""
import json,pathlib,hashlib
import numpy as np
r=pathlib.Path(__file__).resolve().parent
v=json.loads((r/'EVALUATIONS_COMPACT.json').read_text());summary=json.loads((r/'SUMMARY.json').read_text());by={(x['M'],x['world']):x for x in summary['rows']};print(list(v['cells'][0]))
n=0
for c in v['cells']:
 row=by[c['M'],c['world']];m=np.array(c['candidate_mask']);assert len(m)==1000
 # Inspect vector names from export, then validate labels independently below.
 vocab=v['label_vocabulary']
 labels=[vocab[x] for x in c['compatibility']]
 for mask,lab in zip(m,labels):
  expected='UNKNOWN' if mask==0 else {1:'IND',2:'DIFF',4:'SHARED'}.get(int(mask),'UNRESOLVED')
  assert lab==expected
 for label,fraction in row['compatibility']['fractions'].items():assert sum(x==label for x in labels)/1000==fraction
 n+=len(labels)
assert n==27000
print('Independent compatibility mask/label/rate audit passed',n)
