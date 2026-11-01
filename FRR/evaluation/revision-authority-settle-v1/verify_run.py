import json,os
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1'
from study import ROOT,BASE,check_freeze,receipts,summarize,LABELS
from design import cases
from ledger import resolve
from io_utils import sha,dump_new

def main():
 from transformers import AutoTokenizer
 check_freeze();raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];qs={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())};assert len(raw)==len(qs)==len({p['run_id'] for p in raw})
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 for p in raw:
  q=qs[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}];assert p['role']==q['role'] and p['cap']==q['cap'];assert p['answer']==(p['text'].strip() if p['text'].strip() in LABELS else None)
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids'];assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text'];assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id);assert len(p['generated_token_ids'])<=q['cap'] and len(p['input_token_ids'])<=768
 rs=[json.loads(s) for s in (ROOT/'run/RECEIPTS.jsonl').read_text().splitlines()];assert rs==receipts(raw) and len(rs)==150;assert summarize(raw,rs)==json.loads((ROOT/'run/SUMMARY.json').read_text())
 for c in cases():
  v=resolve(c['events'],c['target']);assert (v['verdict'],v['state'])==(c['expected_verdict'],c['expected_state'])
  if v['verdict']=='KNOWN':
   events={e['id']:e for e in c['events'] if e.get('source')=='owner' and e.get('plot')==c['target']};assert all(events[i]['payload'].get('status')==v['state'] for i in v['status_events'])
   assert set(h['id'] for h in v['history'])==set(events)
  other=resolve(c['events'][::-1],c['target']);assert (v['verdict'],v['state'],v['heads'],v['status_events'])==(other['verdict'],other['state'],other['heads'],other['status_events'])
 old=json.loads(Path('/workspace/revision-settle-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items());assert json.loads((ROOT/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
 res=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
 dump_new(ROOT/'CHECKS.json',{'status':'pass','actual_generations':len(raw),'logical_cases':150,'all_authored_outcomes_and_source_origins_match':True,'reversal_invariant':True,'old_files_unchanged_before_sync':len(old),'freezes_dependencies_tokens_decode_stops_receipts_scores_verified':True,'training_updates':0,'tool_actions':0,'sampled_working_bytes_max':max(x['working_estimate'] for x in res),'sampled_rss_max':max(x['process_rss'] for x in res)})
 print('Bounded run audit passes; lineage and old files preserved')
if __name__=='__main__':main()
