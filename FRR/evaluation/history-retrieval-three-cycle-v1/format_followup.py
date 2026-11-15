"""One adaptive, declared format/topology decomposition after the first 14 replies."""
import run as r
import copy,json
import torch
from transformers import AutoModelForCausalLM
from runtime_reference import parameter_digest,Guard
ROOT=r.H
r.H=ROOT/'format-followup'
assert r.c.read(ROOT/'RESULTS.json')['actual_model_replies']==14
assert not (r.H/'PLAN.json').exists()
r.canonical=r.c.inventory()
r.save(r.Path('CANONICAL_BEFORE.json'),r.canonical)
r.tok=r.c.tokenizer()
source=r.c.read(r.OLD/'retrieval/jobs.json')[0]
base=r.fresh(source['messages'])
plain=json.loads(base[-1]['content'])['operator_task']
arrays={}
for topology in ['shell','merged']:
    for form in ['json','plain']:
        task=base[-1]['content'] if form=='json' else plain
        m=copy.deepcopy(base)
        if topology=='shell':m[-1]['content']=task
        else:m=[m[0],{'role':'user','content':m[1]['content']+'\n\n'+task}]
        arrays[topology+'_'+form]=m
r.save(r.Path('PLAN.json'),{'scope':'exploratory format/topology 2x2, one nonce, no generalization claim','trigger':'fresh role-shell echoed JSON task, inherited produced filename-as-JSON code','all_inputs_declared_before_new_inference':arrays,'reference':'../results/fresh_a_t1_raw.json','new_model_replies':3,'model_decoder_world':'same pinned body and physical prepared world; no main change','confounds':'task length, position, form and role topology differ; no single causal mechanism isolated','calls':['shell_plain','merged_json','merged_plain']})
assert arrays['shell_json']==r.c.read(ROOT/'results/fresh_a_t1_raw.json')['messages']
jobs=[r.job(name,source,arrays[name]) for name in ['shell_plain','merged_json','merged_plain']]
torch.set_num_threads(2)
r.model=AutoModelForCausalLM.from_pretrained(r.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
r.model.requires_grad_(False);r.model.eval()
r.digest=r.c.read(r.c.C/'run/MANIFEST.json')['tensor_digest']
assert parameter_digest(r.model,False)==r.digest
r.guard=Guard(5153960755,r.H/'RESOURCE.jsonl');r.rows=[]
for j in jobs:r.run(j)
r.save(r.Path('RESULTS.json'),{'rows':r.rows,'actual_model_replies':3,'reference_model_replies_reused':1,'canonical_unchanged':r.c.inventory()==r.canonical,'weights_unchanged':parameter_digest(r.model,False)==r.digest,'pending':False,'activation':False})
