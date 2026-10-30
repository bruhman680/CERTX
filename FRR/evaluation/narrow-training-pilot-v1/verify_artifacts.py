"""Post-run source/checkpoint/token/cache checks, no inference or training."""
from pathlib import Path
import hashlib,json,os
os.environ['HF_HUB_OFFLINE']='1'
import torch
from transformers import AutoTokenizer
from safetensors import safe_open
P=Path(__file__).resolve().parent;torch.set_num_threads(2)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
old=json.loads((P/'PRESERVATION_BEFORE.json').read_text())
assert all(sha(Path(k))==v for k,v in old['model_and_cache_sha256'].items())
for freeze in ('FREEZE.json','RAW_FREEZE.json'):
 assert all(sha(P/n)==h for n,h in json.loads((P/freeze).read_text())['sha256'].items())
manifest=json.loads((P/'TRAINING_MANIFEST.json').read_text());cp=Path(manifest['checkpoint_directory'])
assert all(sha(cp/n)==h for n,h in manifest['checkpoint_sha256'].items())
tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
rows=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
cases=json.loads((P/'EVAL_CASES.json').read_text());byid={c['id']:c for c in cases};g=json.loads((P/'GUIDANCE.json').read_text())
assert len(rows)==len({r['run_id'] for r in rows})==120
for row in rows:
 c=byid[row['record_id']];messages=[{'role':'user','content':g['instruction']+'\n\nRecord:\n'+c['source']+'\n\n'+g['question']}]
 assert row['messages']==messages
 assert tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)==row['rendered_prompt']
 assert tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)==row['input_token_ids']
 assert tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text']
 a=row['cache_artifact'];f=Path(a['local_path']);assert sha(f)==a['sha256'] and f.stat().st_size==a['bytes']
 ids=row['input_token_ids']+row['generated_token_ids'];assert ids==a['all_sequence_token_ids'] and a['cache_token_count']==len(ids)-1
 assert hashlib.sha256(json.dumps(ids[:a['cache_token_count']],separators=(',',':')).encode()).hexdigest()==a['cached_token_prefix_sha256']
 with safe_open(str(f),framework='pt',device='cpu') as opened:
  assert all(opened.get_slice(k).get_shape()[-2]==a['cache_token_count'] for k in opened.keys())
changed=0;maximum=0.;total=0
with safe_open('/workspace/cache_backend_models/smollm2-135m/model.safetensors',framework='pt',device='cpu') as original,safe_open(str(cp/'model.safetensors'),framework='pt',device='cpu') as adapted:
 assert set(original.keys())==set(adapted.keys())
 for k in original.keys():
  a=original.get_tensor(k).float();b=adapted.get_tensor(k).float();assert a.shape==b.shape and torch.isfinite(b).all()
  delta=float((a-b).abs().max());maximum=max(maximum,delta);changed+=int(delta>0);total+=1
assert manifest['completed_steps']>0 and changed>0
result={'pass':True,'actual_evaluation_calls':120,'old_model_and_cache_files_unchanged':len(old['model_and_cache_sha256']),'new_cache_byte_shape_prefix_checks':120,'prompt_output_tokenizer_checks':120,'checkpoint_and_optimizer_byte_hashes_match':True,'numeric_weight_comparison':{'changed_stored_tensors':changed,'total_stored_tensors':total,'max_abs_weight_change':maximum,'adapted_weights_all_finite':True},'freezes_unchanged':True,'scope':'coordinator artifact checks, not independent efficacy replication'}
with (P/'ARTIFACT_CHECKS.json').open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
