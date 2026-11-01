"""Read-only audit of prompts, decoders, controllers, tools and receipts."""
from pathlib import Path
import json
from io_utils import sha,dump_new
from study import ROOT,check_freeze,summarize,TASKS
from design import render,visible_facts,action_from_facts,decode_fact
from decoder import decode_v2
from routing_reference import retrieve
from task_reference import finish_route

def main():
 check_freeze();data={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())};qs={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())}
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];probes={p['run_id']:p for p in raw}
 workers={p['run_id']:p for p in [json.loads(s) for s in (ROOT/'run/WORKER_RAW.jsonl').read_text().splitlines()]}
 rows=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
 assert len(raw)==len(probes)==len(qs)==192 and len(rows)==576
 for p in raw:
  q=qs[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}]
  assert p['proposal']==(decode_v2(p['text'])['action'] if q['task']=='action' else decode_fact(p['text'],q['task']))
  assert p['cap']==q['cap'] and len(p['generated_token_ids'])<=p['cap']
 for r in rows:
  c=data[r['case_id']];e=visible_facts(c);f={k:probes[r['queries'][k]]['proposal'] for k in ('role','status','access')}
  assert e==r['visible_facts'] and f==r['fact_proposals']
  for k,qid in r['queries'].items():assert qs[qid]['prompt']==render(c,r['vocab'],k)
  assert r['corrections']==[k for k in f if f[k]!=e[k]]
  expected=probes[r['queries']['action']]['proposal'] if r['policy']=='direct' else action_from_facts(f) if r['policy']=='proposed_facts' else action_from_facts(e)
  assert r['action']==expected
  tool=retrieve(c,expected) if expected in ('TARGET','FULL') else None
  assert tool==r['tool']
  state=None
  if r['worker_id']:
   w=workers[r['worker_id']];state={'YES':'positive','NO':'zero','WITHHOLD':'missing'}.get(w['text'].strip());assert w['state']==state
   prompt='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+tool['source']
   if tool['kind']=='full':prompt='Read only the record for the target plot.\n'+prompt
   assert w['messages']==[{'role':'user','content':prompt}]
  terminal=finish_route(c,expected,state,tool)
  assert all(r[k]==v for k,v in terminal.items())
 assert summarize(raw,rows)==json.loads((ROOT/'run/SUMMARY.json').read_text())
 old=json.loads(Path('/workspace/fact-first-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 for v in ('shared_yes_no','distinct_words'):
  checked=[r for r in rows if r['vocab']==v and r['policy']=='checked_facts'];observed=[r for r in rows if r['vocab']==v and r['policy']=='observed_input']
  assert [r['action'] for r in checked]==[r['action'] for r in observed]
 dump_new(ROOT/'CHECKS.json',{'status':'pass','actual_probes':len(raw),'worker_probes':len(workers),'logical_routes':len(rows),'older_files_unchanged_before_sync':len(old),'freeze_dependencies_prompts_decoders_controller_tools_receipts_verified':True,'checked_controller_equals_visible_parser_by_construction':True,'no_training':True})
 print('All prompt/decoder/controller/tool/receipt checks pass; prior files unchanged')
if __name__=='__main__':main()
