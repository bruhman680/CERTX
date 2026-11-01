from pathlib import Path
import json,os
os.environ['HF_HUB_OFFLINE']='1'
from io_utils import sha,dump_new
from study import ROOT,BASE,check_freeze

def main():
 from transformers import AutoTokenizer
 check_freeze();child=ROOT/'post-choice-notes';f=json.loads((child/'FREEZE.json').read_text());assert all(sha(child/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
 for s in [ROOT,child]:assert json.loads((s/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
 read=lambda p:[json.loads(s) for s in p.read_text().splitlines()]
 primary=read(ROOT/'run/RAW.jsonl');post=read(child/'run/RAW.jsonl');assert len(primary)==560 and len(post)==14
 qs={q['id']:q for q in json.loads((child/'QUERIES.json').read_text())};tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 for p in primary+post:
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids']
  assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text'];assert p['cap']==48 and len(p['generated_token_ids'])<=48
  assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id);assert len(p['input_token_ids'])<=768
 for p in post:
  q=qs[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}];assert all(p[k]==q[k] for k in ['source','state','recorded_answer','example'])
 assert len({p['messages'][0]['content'] for p in post})==14
 links=json.loads((child/'LINKS.json').read_text());assert len(links)==18
 for link in links:
  q=qs[link['query_id']];assert all(q[k]==link[k] for k in ['state','recorded_answer','example'])
  assert q['source']==(f"Plot: {link['name']}\nStatus: zero" if link['state']=='zero' else '(no visible record)')
 old=json.loads(Path('/workspace/unknown-notepad-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 entries=[]
 for p in primary:
  if p['decoded']['answer']!='UNKNOWN':continue
  entries.append({'id':p['run_id'],'name':p['name'] if p['present'] else None,'state':p['state'],'context':p['context'],'clarification':p['clarify'],'absence_clause':p['absence'],'note_requested':p['note_requested'],'raw_reply':p['text'],'model_note':p['decoded']['note_text'],'expected_worker_answer':p['expected'],'unknown_warranted_by_supplied_evidence':not p['present'],'audit_source':'literal authored worker grammar, not model self-assessment'})
 with (ROOT/'UNKNOWN_NOTEPAD.jsonl').open('x') as stream:
  for e in entries:stream.write(json.dumps(e,sort_keys=True)+'\n')
 assert all(not e['model_note'] and e['state']=='zero' and not e['unknown_warranted_by_supplied_evidence'] for e in entries)
 resources=read(ROOT/'run/RESOURCE.jsonl')+read(child/'run/RESOURCE.jsonl');allraw=primary+post
 checks={'status':'pass','actual_primary_generations':560,'actual_postchoice_generations':14,'actual_total_generations':574,'unique_prompt_strings':len({p['messages'][0]['content'] for p in allraw}),'primary_logical_links':672,'postchoice_logical_links':18,'unknown_notepad_entries':len(entries),'unknown_notepad_emitted_notes':sum(bool(e['model_note']) for e in entries),'no_primary_note_production':True,'old_files_unchanged_before_sync':len(old),'all_freezes_dependencies_tokens_decode_stops_links_verified':True,'training_updates':0,'tool_actions':0,'input_tokens':sum(len(p['input_token_ids']) for p in allraw),'output_tokens':sum(len(p['generated_token_ids']) for p in allraw),'generation_seconds_excluding_load':sum(p['seconds'] for p in allraw),'cap_stops':sum(p['stop']=='token_limit' for p in allraw),'sampled_working_bytes_max':max(x['working_estimate'] for x in resources),'sampled_rss_max':max(x['process_rss'] for x in resources)}
 dump_new(ROOT/'FINAL_CHECKS.json',checks);print(json.dumps(checks,indent=2))
if __name__=='__main__':main()
