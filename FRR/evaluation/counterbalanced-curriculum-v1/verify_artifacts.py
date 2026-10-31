from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(P))
from runtime import sha,messages
import torch
from transformers import AutoTokenizer
from safetensors import safe_open

def dump(p,x):
 with p.open('x') as f:f.write(json.dumps(x,indent=2)+'\n')
for fr in ('PREFLIGHT_FREEZE.json','FREEZE.json','RAW_FREEZE.json','ACQUISITION_FREEZE.json'):
 for n,v in json.loads((P/fr).read_text())['sha256'].items():assert sha(P/n)==v,n
old=R/'evaluation/lora-state-pilot-v1';external=json.loads((old/'PRESERVATION_BEFORE.json').read_text())['files_sha256'];tm=json.loads((old/'TRAINING_MANIFEST.json').read_text());pr=json.loads((old/'PROBE_RESULT.json').read_text())
for folder,hh in [(tm['adapter_checkpoint'],tm['checkpoint_sha256']),(tm['initial_adapter'],tm['initial_adapter_sha256']),(pr['separate_probe_checkpoint'],pr['probe_checkpoint_sha256'])]:external.update({str(Path(folder)/n):v for n,v in hh.items()})
for rootraw in [old/'RAW_OUTPUTS.jsonl',R/'evaluation/decision-loss-comparison-v1/run/RAW_OUTPUTS.jsonl']:
 for l in rootraw.read_text().splitlines():
  a=json.loads(l)['cache_artifact'];external[a['local_path']]=a['sha256']
for a in json.loads((R/'evaluation/decision-loss-comparison-v1/LOCAL_BINARY_INDEX.json').read_text())['files']:external[a['path']]=a['sha256']
assert len(external)==997 and all(sha(n)==v for n,v in external.items())
D=P/'fixtures/DATA';caseby={c['id']:c for n in ('DEV_CASES.json','PRIMARY_CASES.json','TRAIN.json') for c in json.loads((D/n).read_text())};g=json.loads((D/'GUIDANCE.json').read_text());rows=[json.loads(l) for l in (P/'run/RAW_OUTPUTS.jsonl').read_text().splitlines()];extra=[json.loads(l) for l in (P/'ACQUISITION_RAW.jsonl').read_text().splitlines()]
assert len(rows)==len({r['run_id'] for r in rows})==252 and len(extra)==12
torch.set_num_threads(2);tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
for row in rows+extra:
 msg=messages(caseby[row['record_id']],g);assert msg==row['messages']
 assert tok.apply_chat_template(msg,tokenize=False,add_generation_prompt=True)==row['rendered_prompt']
 assert tok.apply_chat_template(msg,tokenize=True,add_generation_prompt=True)==row['input_token_ids']
 assert tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text']
 a=row['cache_artifact'];f=Path(a['local_path']);assert sha(f)==a['sha256'] and f.stat().st_size==a['bytes']
 ids=row['input_token_ids']+row['generated_token_ids'];assert ids==a['all_sequence_token_ids'] and a['cache_token_count']==len(ids)-1
 assert hashlib.sha256(json.dumps(ids[:a['cache_token_count']],separators=(',',':')).encode()).hexdigest()==a['cached_token_prefix_sha256']
 with safe_open(str(f),framework='pt',device='cpu') as op:assert all(op.get_slice(k).get_shape()[-2]==a['cache_token_count'] for k in op.keys())
for folder in ('run','preflight'):
 m=json.loads((P/folder/'candidate/TRAINING_MANIFEST.json').read_text());assert m['frozen_base_before']==m['frozen_base_after'] and m['initialization_equal_to_control_reference']
 for n,v in m['checkpoint_files_sha256'].items():assert sha(Path(m['checkpoint'])/n)==v
 for n,v in m['initial_files_sha256'].items():assert sha(P/folder/'candidate/initial_adapter'/n)==v
 assert sha(m['optimizer'])==m['optimizer_sha256']
candidate=json.loads((P/'run/candidate/TRAINING_MANIFEST.json').read_text());assert candidate['completed_updates']==48 and candidate['completed_class_exposure']=={'YES':48,'NO':48,'WITHHOLD':48}
assert len(candidate['completed_example_ids'])==len(set(candidate['completed_example_ids']))==144
cap=json.loads((P/'CAPSULE_RECEIPT.json').read_text());assert sha(cap['output'])==cap['archive_sha256'];assert json.loads((P/'CAPSULE_VERIFY.json').read_text())['status']=='verified'
dump(P/'ARTIFACT_CHECKS.json',{'pass':True,'prior_runtime_files_unchanged':997,'main_generations_checked':252,'posthoc_seen_generations_checked':12,'new_cache_prompt_token_checks':264,'candidate_initial_equal_to_reused_control':True,'candidate_base_digest_unchanged':True,'candidate_updates':48,'candidate_unique_training_presentations':144,'candidate_class_exposures':{'YES':48,'NO':48,'WITHHOLD':48},'control_not_retrained':True,'checkpoint_optimizer_capsule_hashes_match':True,'capsule_is_off_workspace_backup':False,'frozen_inputs_raw_unchanged':True,'scope':'coordinatorconsistencychecks,notsource-truthorindependentreplication'})
print((P/'ARTIFACT_CHECKS.json').read_text())
