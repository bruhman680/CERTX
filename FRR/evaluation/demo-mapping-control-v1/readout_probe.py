"""Prospective secondary diagnostic: fixed literal candidate sequence scores, not confidence."""
from pathlib import Path
import hashlib,json,time,platform
import torch,transformers
from transformers import AutoTokenizer,AutoModelForCausalLM
P=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 assert not (P/'READOUT_SCORES.json').exists(), 'No silent rerun'
 f=json.loads((P/'READOUT_FREEZE.json').read_text())
 for n,h in f['sha256'].items(): assert sha(P/n)==h,n
 rows=[json.loads(x) for x in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
 torch.set_num_threads(2);torch.manual_seed(0)
 path='/workspace/cache_backend_models/smollm2-135m'
 tok=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager').eval()
 result=[];labels=['YES','NO','UNKNOWN']
 with torch.inference_mode():
  for row in rows:
   if row['condition']=='none':continue
   ids=torch.tensor([row['input_token_ids']]);begin=time.perf_counter()
   pre=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=False)
   first=pre.logits[0,-1].log_softmax(-1)
   scores={};token_ids={};first_scores={}
   for label in labels:
    tail=tok.encode(label,add_special_tokens=False);assert tail
    joined=torch.tensor([row['input_token_ids']+tail])
    out=model(input_ids=joined,attention_mask=torch.ones_like(joined),use_cache=False)
    lp=out.logits[0,ids.shape[1]-1:joined.shape[1]-1].log_softmax(-1)
    total=sum(float(lp[i,t]) for i,t in enumerate(tail))
    assert abs(total-float(first[tail[0]]))<1e-4 if len(tail)==1 else True
    scores[label]=total;token_ids[label]=tail;first_scores[label]=float(first[tail[0]])
   v=torch.tensor([scores[l] for l in labels],dtype=torch.float64).softmax(0)
   result.append({'run_id':row['run_id'],'literal_candidate_log_prob_sum':scores,'candidate_token_ids':token_ids,'first_token_log_prob':first_scores,'restricted_normalized_candidate_weight':dict(zip(labels,v.tolist())),'inference_seconds_excluding_load':time.perf_counter()-begin})
 (P/'READOUT_SCORES.json').write_text(json.dumps({'scope':'post-primary, prospectively frozen secondary diagnostic. Literal sequences omit EOS; three-way normalization is restricted candidate mass, not semantic confidence or unconstrained generation probability. Capitalization and tokenization matter. No generation/training/cache rewriting.','torch':torch.__version__,'transformers':transformers.__version__,'python':platform.python_version(),'rows':result},indent=2)+'\n')
 (P/'READOUT_RAW_FREEZE.json').write_text(json.dumps({'sha256':{'READOUT_SCORES.json':sha(P/'READOUT_SCORES.json'),'READOUT_RUN.log':sha(P/'READOUT_RUN.log')}},indent=2)+'\n')
if __name__=='__main__':run()
