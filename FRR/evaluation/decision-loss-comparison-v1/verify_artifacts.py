from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(P))
from runtime import sha, messages
import torch
from transformers import AutoTokenizer
from safetensors import safe_open

def dump(p,x):
 with p.open('x') as f:f.write(json.dumps(x,indent=2)+'\n')
for fr in ('PREFLIGHT_FREEZE.json','FREEZE.json','RAW_FREEZE.json'):
 for n,h in json.loads((P/fr).read_text())['sha256'].items():assert sha(P/n)==h,n
old=R/'evaluation/lora-state-pilot-v1';prep=R/'evaluation/decision-token-preparation-v1'
external=json.loads((old/'PRESERVATION_BEFORE.json').read_text())['files_sha256'];tm=json.loads((old/'TRAINING_MANIFEST.json').read_text());pr=json.loads((old/'PROBE_RESULT.json').read_text())
for folder,hashes in [(tm['adapter_checkpoint'],tm['checkpoint_sha256']),(tm['initial_adapter'],tm['initial_adapter_sha256']),(pr['separate_probe_checkpoint'],pr['probe_checkpoint_sha256'])]:external.update({str(Path(folder)/n):v for n,v in hashes.items()})
for line in (old/'RAW_OUTPUTS.jsonl').read_text().splitlines():
 a=json.loads(line)['cache_artifact'];external[a['local_path']]=a['sha256']
assert len(external)==628 and all(sha(n)==h for n,h in external.items())
casekeys={c['id']:c for c in json.loads((old/'EVAL_CASES.json').read_text())+json.loads((prep/'NEW_PRIMARY_CASES.json').read_text())+json.loads((P/'CHALLENGE_CASES.json').read_text())};guide=json.loads((old/'GUIDANCE.json').read_text())
rows=[json.loads(l) for l in (P/'run/RAW_OUTPUTS.jsonl').read_text().splitlines()];assert len(rows)==len({r['run_id'] for r in rows})==360
torch.set_num_threads(2);tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
for row in rows:
 msg=messages(casekeys[row['record_id']],guide);assert msg==row['messages']
 assert tok.apply_chat_template(msg,tokenize=False,add_generation_prompt=True)==row['rendered_prompt']
 assert tok.apply_chat_template(msg,tokenize=True,add_generation_prompt=True)==row['input_token_ids']
 assert tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text']
 a=row['cache_artifact'];f=Path(a['local_path']);assert sha(f)==a['sha256'] and f.stat().st_size==a['bytes']
 ids=row['input_token_ids']+row['generated_token_ids'];assert ids==a['all_sequence_token_ids'] and a['cache_token_count']==len(ids)-1
 assert hashlib.sha256(json.dumps(ids[:a['cache_token_count']],separators=(',',':')).encode()).hexdigest()==a['cached_token_prefix_sha256']
 with safe_open(str(f),framework='pt',device='cpu') as op:assert all(op.get_slice(k).get_shape()[-2]==a['cache_token_count'] for k in op.keys())
manifests=[]
for arm in ('sequence_mean','decision_balanced'):
 m=json.loads((P/'run'/arm/'TRAINING_MANIFEST.json').read_text());manifests.append(m)
 assert m['frozen_base_before']==m['frozen_base_after']
 assert m['completed_updates']==48 and m['completed_class_exposure']=={'YES':48,'NO':48,'WITHHOLD':48}
 for n,h in m['checkpoint_files_sha256'].items():assert sha(Path(m['checkpoint'])/n)==h
 for n,h in m['initial_files_sha256'].items():assert sha(P/'run'/arm/'initial_adapter'/n)==h
 assert sha(m['optimizer'])==m['optimizer_sha256']
assert manifests[0]['initial_adapter_digest']==manifests[1]['initial_adapter_digest']
assert manifests[0]['completed_example_ids']==manifests[1]['completed_example_ids']
priorbase={r['record_id']:r for r in [json.loads(l) for l in (old/'RAW_OUTPUTS.jsonl').read_text().splitlines()] if r['arm']=='original_test'}
regbase=[r for r in rows if r['arm']=='original' and r['subset']=='regression'];assert len(regbase)==48
same=sum(r['input_token_ids']==priorbase[r['record_id']]['input_token_ids'] and r['generated_token_ids']==priorbase[r['record_id']]['generated_token_ids'] for r in regbase)
pre=json.loads((P/'preflight/sequence_mean/TRAINING_MANIFEST.json').read_text());assert pre['completed_updates']==1
for n,h in pre['checkpoint_files_sha256'].items():assert sha(Path(pre['checkpoint'])/n)==h
assert sha(pre['optimizer'])==pre['optimizer_sha256']
dump(P/'ARTIFACT_CHECKS.json',{'pass':True,'prior_external_files_unchanged':628,'new_cache_token_prompt_checks':360,'both_initial_adapter_digests_equal':True,'both_base_digests_unchanged':True,'completed_data_order_equal':True,'balanced_exposures_per_arm':{'YES':48,'NO':48,'WITHHOLD':48},'checkpoints_optimizer_hashes_match':True,'old_regression_baseline_exact_token_repeats':same,'old_regression_baseline_total':48,'frozen_inputs_raw_unchanged':True,'scope':'coordinatorconsistencychecks,notindependentreplication'})
print((P/'ARTIFACT_CHECKS.json').read_text())
