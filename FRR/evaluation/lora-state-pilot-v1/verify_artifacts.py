from experiment import *
from safetensors import safe_open
P=Path(__file__).resolve().parent
for n,h in json.loads((P/'PRESERVATION_BEFORE.json').read_text())['files_sha256'].items():assert sha(Path(n))==h,n
for freeze in ('PROBE_FREEZE.json','FREEZE.json','RAW_FREEZE.json'):
 for n,h in json.loads((P/freeze).read_text())['sha256'].items():assert sha(P/n)==h,n
probe=json.loads((P/'PROBE_RESULT.json').read_text());pd=Path(probe['separate_probe_checkpoint'])
assert all(sha(pd/n)==h for n,h in probe['probe_checkpoint_sha256'].items())
tm=json.loads((P/'TRAINING_MANIFEST.json').read_text());cp=Path(tm['adapter_checkpoint']);init=Path(tm['initial_adapter'])
assert all(sha(cp/n)==h for n,h in tm['checkpoint_sha256'].items())
assert all(sha(init/n)==h for n,h in tm['initial_adapter_sha256'].items())
assert tm['frozen_base_before']==tm['frozen_base_after'] and tm['probe_not_warmstart']
assert len(set(tm['completed_class_exposure'].values()))==1 and next(iter(tm['completed_class_exposure'].values()))==tm['completed_updates']
rows=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()];cases=json.loads((P/'EVAL_CASES.json').read_text());byid={c['id']:c for c in cases}
assert len(rows)==len({r['run_id'] for r in rows})==120
torch.set_num_threads(2)
tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
for r in rows:
 c=byid[r['record_id']];assert r['messages']==prompt(c)
 assert tok.apply_chat_template(r['messages'],tokenize=False,add_generation_prompt=True)==r['rendered_prompt']
 assert tok.apply_chat_template(r['messages'],tokenize=True,add_generation_prompt=True)==r['input_token_ids']
 assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text']
 a=r['cache_artifact'];f=Path(a['local_path']);assert sha(f)==a['sha256'] and f.stat().st_size==a['bytes']
 ids=r['input_token_ids']+r['generated_token_ids'];assert ids==a['all_sequence_token_ids'] and a['cache_token_count']==len(ids)-1
 assert hashlib.sha256(json.dumps(ids[:a['cache_token_count']],separators=(',',':')).encode()).hexdigest()==a['cached_token_prefix_sha256']
 with safe_open(str(f),framework='pt',device='cpu') as opened:
  assert all(opened.get_slice(k).get_shape()[-2]==a['cache_token_count'] for k in opened.keys())
changed=0;total=0;maximum=0.
with safe_open(str(init/'adapter.safetensors'),framework='pt',device='cpu') as old,safe_open(str(cp/'adapter.safetensors'),framework='pt',device='cpu') as new:
 assert set(old.keys())==set(new.keys())
 for k in old.keys():
  a=old.get_tensor(k);b=new.get_tensor(k);assert a.shape==b.shape and torch.isfinite(b).all();v=float((a-b).abs().max());changed+=int(v>0);total+=1;maximum=max(maximum,v)
manifest=json.loads((P/'RUN_MANIFEST.json').read_text());assert manifest['adapter_roundtrip_diagnostic_logits_exact']
records=[json.loads(l) for l in (P/'TRAINING_LOG.jsonl').read_text().splitlines()]
assert sum(r['completed'] for r in records)==tm['completed_updates']
for r in records:
 if r['completed']:assert len(r['example_ids'])==3 and {x.rsplit('_',1)[-1] for x in r['example_ids']}=={'positive','zero','missing'}
points=[q for r in records for q in r['points']]
result={'pass':True,'old_files_unchanged':len(json.loads((P/'PRESERVATION_BEFORE.json').read_text())['files_sha256']),'new_cache_prompt_output_checks':120,'probe_initial_final_checkpoint_hashes_match':True,'base_numeric_digest_unchanged':True,'completed_updates':tm['completed_updates'],'each_completed_update_has_all_three_classes':True,'max_recorded_training_working_memory':max(q['working_estimate'] for q in points),'max_recorded_process_rss':max(q['process_rss'] for q in points),'adapter_tensor_change':{'changed':changed,'total':total,'max_abs_change':maximum},'fresh_model_adapter_roundtrip_logits_exact':True,'frozen_inputs_and_raw_unchanged':True,'review':'coordinator consistencychecks,notindependentreplication'}
dump(P/'ARTIFACT_CHECKS.json',result);print(json.dumps(result))
