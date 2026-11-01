from pathlib import Path
import json,os
os.environ['HF_HUB_OFFLINE']='1'
from io_utils import sha,dump_new
from study import ROOT,BASE,ACQ,check_freeze,summarize
from design import queries,MAP

def main():
 from transformers import AutoTokenizer
 check_freeze();expected={q['id']:q for q in queries()};saved=json.loads((ROOT/'QUERIES.json').read_text());assert saved==queries()
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==len({p['run_id'] for p in raw})==531
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 lengths=json.loads((ROOT/'TOKENIZATION.json').read_text())
 for p in raw:
  q=expected[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}]
  assert all(p[k]==q[k] for k in ['source_id','header','condition','kind','match','access','expected','state','name'])
  assert p['answer']==p['text'].strip();assert p['recognized']==(p['answer'] in MAP.values());assert p['correct']==(p['answer']==q['expected'])
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids'];assert len(p['input_token_ids'])==lengths['prompt_lengths'][q['id']]
  assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text'];assert p['cap']==12
  assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id)
  assert len(p['generated_token_ids'])<=12 and len(p['input_token_ids'])<=768
 by={p['run_id']:p for p in raw}
 for pair in lengths['control_pairs']:
  assert pair['relevant_tokens']==len(by[pair['relevant_id']]['input_token_ids']);assert pair['unrelated_tokens']==len(by[pair['unrelated_id']]['input_token_ids']);assert pair['equal_tokens']==(pair['relevant_tokens']==pair['unrelated_tokens'])
 summary=summarize(raw);assert summary==json.loads((ROOT/'run/SUMMARY.json').read_text());assert summary['paired_relevant_left_unrelated_right']['n']==252 and summary['paired_canonical_left_explicit_right']['n']==261 and summary['paired_yes_no_left_available_unavailable_right']['n']==216
 old=json.loads(Path('/workspace/worker-context-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 resources=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
 m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 assert json.loads((ROOT/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
 dump_new(ROOT/'CHECKS.json',{'status':'pass','actual_unique_generations':531,'token_equal_control_pairs':lengths['equal_length_pairs'],'control_pairs':252,'prior_files_unchanged_before_sync':len(old),'frozen_code_data_dependencies_transcripts_tokens_and_scores_verified':True,'training_updates':0,'tool_actions':0,'sampled_working_bytes_max':max(x['working_estimate'] for x in resources),'sampled_rss_max':max(x['process_rss'] for x in resources)})
 print('Audit passes:531unique generations, all tokens/scores/pairs/dependencies and old files checked')
if __name__=='__main__':main()
