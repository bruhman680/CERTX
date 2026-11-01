from pathlib import Path
import os,json
os.environ['HF_HUB_OFFLINE']='1'
from io_utils import sha,dump_new
from study import ROOT,BASE,PRIOR,ACQ,check_freeze,summarize
from design import decode,queries

def main():
 from transformers import AutoTokenizer
 check_freeze();qs={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())};raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==len(qs)==560
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);by={p['run_id']:p for p in raw};assert len(by)==560
 lengths=json.loads((ROOT/'TOKENIZATION.json').read_text())
 for p in raw:
  q=qs[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}]
  assert all(p[k]==q[k] for k in ['name','state','present','context','clarify','absence','note_requested','expected'])
  assert p['decoded']==decode(p['text']);assert p['correct']==(p['decoded']['answer']==q['expected']);assert p['strict_correct']==(p['decoded']['strict_whole_answer']==q['expected'])
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids'];assert len(p['input_token_ids'])==lengths['prompt_lengths'][q['id']]
  assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text'];assert p['cap']==48 and len(p['generated_token_ids'])<=48
  assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id)
 logical=queries();assert logical==json.loads((ROOT/'LOGICAL_QUERIES.json').read_text());links=json.loads((ROOT/'LINKS.json').read_text());assert len(links)==672
 for q,link in zip(logical,links):
  assert q['id']==link['logical_id'];assert q['prompt']==qs[link['unique_id']]['prompt'];assert q['expected']==qs[link['unique_id']]['expected']
 oldraw={p['run_id']:p for p in [json.loads(s) for s in (PRIOR/'run/RAW.jsonl').read_text().splitlines()]}
 for pair in lengths['prior_prompt_repeats']:
  a,b=by[pair['unique_id']],oldraw[pair['old_id']]
  assert a['input_token_ids']==b['input_token_ids'] and a['generated_token_ids']==b['generated_token_ids'] and a['text']==b['text']
 assert len(lengths['prior_prompt_repeats'])==126
 summary=summarize(raw);assert summary==json.loads((ROOT/'run/SUMMARY.json').read_text())
 for k in ['paired_answer_only_left_note_right','paired_no_absence_clause_left_clause_right','paired_no_clarification_left_clarification_right']:assert summary[k]['n']==280
 old=json.loads(Path('/workspace/unknown-notepad-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];assert json.loads((ROOT/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
 res=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
 dump_new(ROOT/'CHECKS.json',{'status':'pass','actual_unique_generations':560,'logical_query_links':672,'old_prompt_outputs_matching':126,'prior_files_unchanged_before_sync':len(old),'frozen_code_data_dependencies_transcripts_tokens_decoders_notes_scores_pairs_verified':True,'training_updates':0,'tool_actions':0,'sampled_working_bytes_max':max(x['working_estimate'] for x in res),'sampled_rss_max':max(x['process_rss'] for x in res)})
 print('Allchecks pass;560uniquegenerations,672links,126prioroutputsequal')
if __name__=='__main__':main()
