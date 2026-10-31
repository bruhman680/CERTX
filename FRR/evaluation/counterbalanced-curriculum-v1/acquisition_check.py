"""Posthoc seen-source diagnostic, no updates; separate from frozen primary."""
from pathlib import Path
import json,sys,hashlib
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
from runtime import Guard,generate,parameter_digest,sha
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
sys.path.insert(0,str(P.parents[1]/'evaluation/lora-state-pilot-v1'))
from lora_cpu import inject_lora,load_adapter
assert not (P/'ACQUISITION_RAW.jsonl').exists()
for n,v in json.loads((P/'ACQUISITION_FREEZE.json').read_text())['sha256'].items():assert sha(P/n)==v,n
train=json.loads((P/'fixtures/DATA/TRAIN.json').read_text());chosen=[]
for family in dict.fromkeys(c['structure_family'] for c in train):chosen.extend([c for c in train if c['structure_family']==family][:3])
assert len(chosen)==12 and len({c['id'] for c in chosen})==12
assert {l:sum(c['label']==l for c in chosen) for l in ('YES','NO','WITHHOLD')}=={'YES':4,'NO':4,'WITHHOLD':4}
g=json.loads((P/'fixtures/DATA/GUIDANCE.json').read_text());m=json.loads((P/'run/candidate/TRAINING_MANIFEST.json').read_text())
torch.set_num_threads(2);torch.manual_seed(73103);base='/workspace/cache_backend_models/smollm2-135m'
t=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False);model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,m['checkpoint'],base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_adapter_digest']
states=Path('/workspace/smollm_curriculum_acquisition_states_v1');states.mkdir(exist_ok=False);guard=Guard(int(.6*8589934592),P/'ACQUISITION_RESOURCE.jsonl');hits=0;labels={};rows=[]
for c in chosen:
 row=generate(model,t,c,g,'candidate','seen_acquisition',states,guard)
 row['expected']=c['label'];label=row['text'].strip().upper();row['label_match']=label==c['label'];hits+=int(row['label_match']);labels[label]=labels.get(label,0)+1
 with (P/'ACQUISITION_RAW.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 rows.append(row)
assert parameter_digest(model,True)==m['final_adapter_digest'] and parameter_digest(model,False)==m['frozen_base_after']
(P/'ACQUISITION_SUMMARY.json').write_text(json.dumps({'selected_seen_training_cases':12,'matches':hits,'outputs':labels,'perclass':{l:{'n':4,'matches':sum(r['label_match'] for r in rows if r['expected']==l)} for l in ('YES','NO','WITHHOLD')},'weight_updates':0,'same_final_candidate_digest':True,'scope':'posthocseen-sourceacquisitioncheck;notheldout/generalization,notreplacesprimary,notall144trainingcases'},indent=2)+'\n');print((P/'ACQUISITION_SUMMARY.json').read_text())
