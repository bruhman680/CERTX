import os,json
from pathlib import Path
os.environ['HF_HUB_OFFLINE']='1'
from study import ROOT,BASE,ACQ,check_freeze,routes,summarize,LABELS
from design import cases
from verifier import verify,parse
from io_utils import sha,dump_new

def main():
 from transformers import AutoTokenizer
 check_freeze();raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];qs={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())};assert len(raw)==len(qs)==327 and len({p['run_id'] for p in raw})==327
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 for p in raw:
  q=qs[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}];assert p['role']==q['role'] and p['cap']==q['cap']
  assert p['answer']==(p['text'].strip() if p['text'].strip() in LABELS else None)
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids'];assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text'];assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id)
  assert len(p['generated_token_ids'])<=q['cap'] and len(p['input_token_ids'])<=768
 rs=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()];assert rs==routes(raw) and len(rs)==648;assert summarize(raw,rs)==json.loads((ROOT/'run/SUMMARY.json').read_text())
 for c in cases():
  for policy in ['strict','supported']:
   v=verify(c['source'],c['layout'],c['target'],policy);assert v['verdict']==c['expected_'+policy]
   if v['verdict']=='READY':
    assert v['state']==c['expected_state'];recs=parse(c['source'],c['layout']);assert v['witnesses'] and all(recs[i]=={'plot':c['target'],'status':v['state']} for i in v['witnesses'])
    assert v['canonical']==f"Plot: {c['target']}\nStatus: {v['state']}"
 old=json.loads(Path('/workspace/boundary-transfer-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];assert json.loads((ROOT/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
 res=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
 dump_new(ROOT/'CHECKS.json',{'status':'pass','actual_generations':327,'raw_generations':318,'selected_generations':9,'logical_case_policy_routes':648,'all_authored_contracts_and_source_index_witnesses_match':True,'old_files_unchanged_before_sync':len(old),'all_freezes_dependencies_transcripts_tokens_decodes_stops_scores_verified':True,'training_updates':0,'tool_actions':0,'sampled_working_bytes_max':max(x['working_estimate'] for x in res),'sampled_rss_max':max(x['process_rss'] for x in res)})
 print('Audit passes:327actualgenerations,648routes,allwitnessesandoldfileschecked')
if __name__=='__main__':main()
