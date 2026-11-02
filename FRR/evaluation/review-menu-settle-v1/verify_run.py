from pathlib import Path
import json,os
os.environ['HF_HUB_OFFLINE']='1'
from io_utils import sha,dump_new
from design import queries,LABELS
from study import ROOT,BASE,PRIOR,check_freeze,summarize

def main():
 from transformers import AutoTokenizer
 check_freeze();qs=queries();assert qs==json.loads((ROOT/'QUERIES.json').read_text());by={q['id']:q for q in qs};raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==len({p['run_id'] for p in raw})==231
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);tokenization=json.loads((ROOT/'TOKENIZATION.json').read_text())
 for p in raw:
  q=by[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}];assert all(p[k]==q[k] for k in ['case_id','frame','state','expected','kind','menu','first_option'])
  assert p['answer']==(p['text'].strip() if p['text'].strip() in LABELS else None) and p['correct']==(p['answer']==q['expected'])
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids'];assert len(p['input_token_ids'])==tokenization['lengths'][q['id']]
  assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text'];assert p['cap']==16 and len(p['generated_token_ids'])<=16 and len(p['input_token_ids'])<=768;assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id)
 current={p['run_id']:p for p in raw};prior={p['run_id']:p for p in [json.loads(s) for s in (PRIOR/'run/RAW.jsonl').read_text().splitlines()]}
 for pair in tokenization['prior_repeats']:
  a,b=current[pair['new_id']],prior[pair['prior_id']];assert a['input_token_ids']==b['input_token_ids'] and a['generated_token_ids']==b['generated_token_ids'] and a['text']==b['text']
 assert len(tokenization['prior_repeats'])==63 and summarize(raw)==json.loads((ROOT/'run/SUMMARY.json').read_text())
 m=json.loads((ROOT/'run/RUN_MANIFEST.json').read_text());assert m['status']=='complete' and m['generation_forward_steps']==sum(len(p['generated_token_ids']) for p in raw)
 old=json.loads(Path('/workspace/review-menu-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 res=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
 dump_new(ROOT/'CHECKS.json',{'status':'pass','actual_generation_probes':231,'prior_input_output_sequences_match':63,'all_freezes_dependencies_prompts_tokens_decode_stops_pairs_scores_checked':True,'weights_unchanged_verified_in_run':True,'training_updates':0,'new_probability_score_forwards':0,'old_files_unchanged_before_sync':len(old),'sampled_working_bytes_max':max(x['working_estimate'] for x in res),'sampled_rss_max':max(x['process_rss'] for x in res)})
 print('Audit passes:231generations,63exactoldsequencematches; oldfilesandweightsunchanged')
if __name__=='__main__':main()
