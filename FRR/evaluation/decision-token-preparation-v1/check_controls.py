"""Tokenizer and exact-rational objective checks only; no model forward/update."""
from pathlib import Path
from fractions import Fraction as F
import json,os
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
P=Path(__file__).resolve().parent
T=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
labels={s:{'ids':T.encode(s,add_special_tokens=False),'target_length_with_eos':len(T.encode(s,add_special_tokens=False))+1} for s in ('YES','NO','WITHHOLD','A','B','C')}
assert all(len(labels[s]['ids'])==1 and T.decode(labels[s]['ids'])==s for s in ('A','B','C'))
mappings=[dict(zip(('positive','zero','missing'),seq)) for seq in [('A','B','C'),('B','C','A'),('C','A','B')]]
assert all(len(set(m.values()))==3 for m in mappings)
assert all({m[c] for m in mappings}=={'A','B','C'} for c in ('positive','zero','missing'))
weights={}
for name in labels:
 n=labels[name]['target_length_with_eos'];old=[F(1,n)]*n;new=[F(1,2)]+[F(1,2*(n-1))]*(n-1)
 assert sum(old)==sum(new)==1
 if name in ('A','B','C'):assert old==new
 weights[name]={'old_perexample':[str(x) for x in old],'decision_balanced_perexample':[str(x) for x in new],'old_first_per_effective_update':str(old[0]/3),'new_first_per_effective_update':str(new[0]/3),'illustration_first_ce2_other_ce0':{'old':str(2*old[0]),'new':str(2*new[0])}}
assert {weights[s]['new_first_per_effective_update'] for s in ('YES','NO','WITHHOLD')}=={'1/6'}
for n in range(2,9):
 for losses in ([F(2)]+[F(0)]*(n-1),[F(0)]+[F(1)]*(n-1),[F(i+1,7) for i in range(n)]):
  direct=F(1,2)*losses[0]+F(1,2)*sum(losses[1:])/(n-1)
  weighted=sum(v*w for v,w in zip(losses,[F(1,2)]+[F(1,2*(n-1))]*(n-1)))
  assert direct==weighted
result={'status':'passed','tokenizer_pin':'SmolLM2-135M-Instruct revision12fd25f77366fa6b3b4b768ec3050bf629380bac','labels':labels,'cyclic_alias_mappings':mappings,'weights':weights,'checks':{'aliases_exactly_one_token':True,'mapping_counterbalance':True,'weights_normalized':True,'decision_first_weight_equal':True,'alias_two_objectives_identical':True,'two_formula_evaluations_match_21_exact_examples':True},'scope':'exactobjective/tokenizer/mappingchecks,notlearningorsemantic-efficacyevidence','model_forwards':0,'optimizer_steps':0}
with (P/'CONTROL_CHECKS.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'passed','aliases':{s:labels[s]['ids'] for s in ('A','B','C')},'model_forwards':0,'optimizer_steps':0}))
