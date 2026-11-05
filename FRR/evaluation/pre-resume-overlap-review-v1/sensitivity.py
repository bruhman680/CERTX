"""Descriptive threshold sensitivity, chosen after main5gramresult; no modelcalls."""
from pathlib import Path
import json
from analyze import words
R=Path(__file__).resolve().parent;E=R.parent/'source-access-three-cycle-v1/cycle3/environment';rows=[json.loads((E/'events'/f'{i:06d}.json').read_text()) for i in range(205,305)];result=[]
for n in (3,5,8):
 den=hit=eligible=0
 for x in rows:
  out=words(x['text']);inp=words(x['prompt'])
  if len(out)<n:continue
  eligible+=1;den+=len(out);gs={tuple(inp[i:i+n]) for i in range(len(inp)-n+1)};covered=set()
  for i in range(len(out)-n+1):
   if tuple(out[i:i+n]) in gs:covered.update(range(i,i+n))
  hit+=len(covered)
 result.append(dict(n=n,eligible_replies=eligible,eligible_words=den,matched_word_coverage=hit/den))
assert abs(result[1]['matched_word_coverage']-json.loads((R/'SUMMARY.json').read_text())['all']['input_word_coverage'])<1e-12
(R/'SENSITIVITY.json').write_text(json.dumps(dict(scope='Posthoc threshold sensitivity; varying eligibility/denominators, not interchangeable novelty scores',rows=result),indent=2)+'\n');print(json.dumps(result,indent=2))
