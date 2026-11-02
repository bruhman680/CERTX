import math,time
from design import LABELS

def normalized(records):
 top=max(r['sequence_logp'] for r in records.values());den=top+math.log(sum(math.exp(r['sequence_logp']-top) for r in records.values()))
 return {label:math.exp(r['sequence_logp']-den) for label,r in records.items()},den

def score(model,tok,prompt,guard,run_id):
 import torch
 prefix=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True)
 assert len(prefix)<=768;records={};began=time.perf_counter();guard.read('before_candidate_scores',run_id=run_id)
 with torch.inference_mode():
  for label in LABELS:
   target=tok.encode(label,add_special_tokens=False)+[tok.eos_token_id];ids=prefix+target[:-1];x=torch.tensor([ids])
   logits=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False,logits_to_keep=len(target)).logits[0]
   assert logits.shape[0]==len(target)
   z=logits.double();norm=torch.logsumexp(z,dim=-1);selected=z[torch.arange(len(target)),torch.tensor(target)];lps=(selected-norm).tolist()
   records[label]={'target_ids':target,'token_logps':lps,'target_logits':selected.tolist(),'log_normalizers':norm.tolist(),'sequence_logp':sum(lps),'first_token_full_vocab_prob':math.exp(lps[0])}
 guard.read('after_candidate_scores',run_id=run_id);relative,log_mass=normalized(records);assert log_mass<=1e-8
 return {'candidates':records,'candidate_normalized_mass':relative,'candidate_log_mass':log_mass,'candidate_mass':math.exp(log_mass),'scoring_forwards':4,'seconds':time.perf_counter()-began}

def check_heads(model,tok,prompt,guard):
 import torch
 prefix=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True);rows=[];guard.read('before_head_check')
 with torch.inference_mode():
  for label in LABELS:
   target=tok.encode(label,add_special_tokens=False)+[tok.eos_token_id];x=torch.tensor([prefix+target[:-1]])
   full=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False,logits_to_keep=0).logits[0,-len(target):]
   short=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False,logits_to_keep=len(target)).logits[0]
   diff=float((full-short).abs().max());assert diff<=1e-4,(label,diff)
   rows.append({'label':label,'target_ids':target,'max_absolute_logit_difference':diff})
 guard.read('after_head_check');return {'status':'pass','tolerance':1e-4,'model_forwards':8,'rows':rows}
