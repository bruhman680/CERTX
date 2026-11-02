from pathlib import Path
import json,math,os
os.environ['HF_HUB_OFFLINE']='1'
from io_utils import sha,dump_new
from study import ROOT,BASE,check_freeze,summarize
from probability import normalized
from design import cases,schedules,review,LABELS

def close(a,b,tol=1e-10):assert abs(a-b)<=tol,(a,b)
def main():
 from transformers import AutoTokenizer
 check_freeze();raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==len({p['run_id'] for p in raw})==189
 cs={c['id']:c for c in cases()};initial={p['case_id']:p for p in raw if p['kind']=='initial'};tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);labels=json.loads((ROOT/'TOKENIZATION.json').read_text())['label_tokens'];schedule=schedules()
 for p in raw:
  c=cs[p['case_id']];expected=c['prompt'] if p['kind']=='initial' else review(c,p['kind'],p['include_attempt'],initial[c['id']]['text'])
  assert p['messages']==[{'role':'user','content':expected}];assert p['expected']==c['expected'] and p['frame']==c['frame'] and p['state']==c['state']
  assert p['answer']==(p['text'].strip() if p['text'].strip() in LABELS else None);assert p['correct']==(p['answer']==c['expected'])
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids'];assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text'];assert p['cap']==16 and len(p['generated_token_ids'])<=16 and len(p['input_token_ids'])<=768
  assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id)
  score=p['scores'];assert score['scoring_forwards']==4 and set(score['candidates'])==set(LABELS)
  for label,r in score['candidates'].items():
   assert r['target_ids']==labels[label] and len(r['target_ids'])==len(r['token_logps'])==len(r['target_logits'])==len(r['log_normalizers'])
   for lp,z,norm in zip(r['token_logps'],r['target_logits'],r['log_normalizers']):close(lp,z-norm)
   close(r['sequence_logp'],sum(r['token_logps']));close(r['first_token_full_vocab_prob'],math.exp(r['token_logps'][0]))
  rel,den=normalized(score['candidates']);close(den,score['candidate_log_mass']);close(math.exp(den),score['candidate_mass']);close(sum(rel.values()),1)
  for label in LABELS:close(rel[label],score['candidate_normalized_mass'][label])
 reviews=[p for p in raw if p['kind']!='initial'];assert len(reviews)==len(schedule)==168
 for p,e in zip(reviews,schedule):assert p['case_id']==e['case_id'] and p['kind']==e['kind'] and p['include_attempt']==e['include_attempt']
 assert summarize(raw)==json.loads((ROOT/'run/SUMMARY.json').read_text())
 head=json.loads((ROOT/'run/HEAD_CHECK.json').read_text());assert head['status']=='pass' and head['model_forwards']==8 and all(x['max_absolute_logit_difference']<=1e-4 for x in head['rows'])
 m=json.loads((ROOT/'run/RUN_MANIFEST.json').read_text());assert m['status']=='complete' and m['candidate_score_forwards']==756 and m['generation_forward_steps']==sum(len(p['generated_token_ids']) for p in raw)
 old=json.loads(Path('/workspace/feedback-probe-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 resources=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
 dump_new(ROOT/'CHECKS.json',{'status':'pass','generation_probes':189,'candidate_scoring_forwards':756,'head_verification_forwards':8,'greedy_generation_forward_steps':m['generation_forward_steps'],'all_prompt_feedback_token_decode_score_arithmetic_schedule_and_summary_checks_pass':True,'full_logit_vectors_not_retained_and_scores_not_rerun':True,'weights_unchanged_verified_in_run':True,'old_files_unchanged_before_sync':len(old),'training_updates':0,'tool_actions':0,'sampled_working_bytes_max':max(x['working_estimate'] for x in resources),'sampled_rss_max':max(x['process_rss'] for x in resources)})
 print('Audit passes:189generations,756scoreforwards,8headchecks; oldfiles/weights unchanged')
if __name__=='__main__':main()
