"""Outcome-informed targeted check of an order-sensitive available-archive request."""
from pathlib import Path
from collections import Counter
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from io_utils import sha,dump_new,append
from decoder import decode_v1,decode_v2
from domain import render

def prepare():
    data=[]
    for name in ('Clover','Marigold','Sorrel'):
        for available in (True,False):
            for rotation in (0,5):
                case={'target':name,'visible_display':None,'archive_available':available}
                data.append({'id':f'q_{len(data):03d}','case':case,'name':name,'available':available,
                    'rotation':rotation,'prompt':render(case,'examples',rotation)})
    dump_new(ROOT/'QUERIES.json',data)
    acq=ROOT.parent.parent/'simple-readout-acquisition-v1/run/canonical'
    deps=[ROOT.parent/n for n in ('decoder.py','domain.py','task_reference.py','routing_reference.py','evidence.py',
        'generate.py','runtime_reference.py','lora_cpu.py','io_utils.py','run/ROUTER_RAW.jsonl')]
    deps += [acq/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    dump_new(ROOT/'FREEZE.json',{'sha256':{n:sha(ROOT/n) for n in ('check.py','PROTOCOL.md','QUERIES.json')},
        'dependencies':{str(p):sha(p) for p in deps},'timing':'after parent outcomes, before12transfer forwards',
        'selection':'candidate order5 versus original order0, selected from exposed parent data'})

def run():
    import os
    os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM
    from generate import generate
    from runtime_reference import Guard,parameter_digest
    from lora_cpu import inject_lora,load_adapter
    f=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in f['sha256'].items())
    assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
    queries=json.loads((ROOT/'QUERIES.json').read_text());out=ROOT/'run';out.mkdir()
    guard=Guard(5153960755,out/'RESOURCE.jsonl');torch.set_num_threads(2);torch.manual_seed(73103)
    base=Path('/workspace/cache_backend_models/smollm2-135m');acq=ROOT.parent.parent/'simple-readout-acquisition-v1/run/canonical'
    manifest=json.loads((acq/'MANIFEST.json').read_text());assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    guard.read('before_load')
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,acq/'final',base_pin=manifest['base_pin'])
    assert parameter_digest(model,True)==manifest['final_digest']
    rows=[]
    for q in queries:
        r=generate(model,tok,q['prompt'],24,guard,q['id'])
        r.update({'name':q['name'],'available':q['available'],'rotation':q['rotation'],
                  'strict_v1':decode_v1(r['text']),'declared_v2':decode_v2(r['text'])})
        append(out/'RAW.jsonl',r);rows.append(r)
    assert parameter_digest(model,True)==manifest['final_digest']
    assert parameter_digest(model,False)==manifest['base_digest_after']
    assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
    old=[json.loads(s) for s in (ROOT.parent/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    repeats=[]
    for r in rows:
        q=next(q for q in queries if q['id']==r['run_id'])
        assert r['messages']==[{'role':'user','content':render(q['case'],'examples',q['rotation'])}]
        assert r['input_token_ids']==tok.apply_chat_template(r['messages'],tokenize=True,add_generation_prompt=True)
        assert r['text']==tok.decode(r['generated_token_ids'],skip_special_tokens=True)
        assert r['declared_v2']==decode_v2(r['text']) and r['strict_v1']==decode_v1(r['text'])
        if r['name']=='Clover':
            same=[p for p in old if p['input_token_ids']==r['input_token_ids']]
            assert len(same)==1;repeats.append(same[0]['generated_token_ids']==r['generated_token_ids'])
    assert len(repeats)==4
    pairs=[]
    for name in ('Clover','Marigold','Sorrel'):
        for rotation in (0,5):
            yes=next(r for r in rows if (r['name'],r['available'],r['rotation'])==(name,True,rotation))
            no=next(r for r in rows if (r['name'],r['available'],r['rotation'])==(name,False,rotation))
            a,b=yes['declared_v2']['action'],no['declared_v2']['action']
            pairs.append({'name':name,'rotation':rotation,'available_action':a,'unavailable_action':b,
                'request_when_available_only':a in ('FULL','TARGET') and b not in ('FULL','TARGET'),
                'request_then_UNKNOWN':a in ('FULL','TARGET') and b=='UNKNOWN'})
    dump_new(out/'SUMMARY.json',{'pairs':pairs,'actions':dict(Counter(r['declared_v2']['action'] or 'INVALID' for r in rows)),
        'actual_generation_probes':12,'new_names':2,'baseline_replays':4,'baseline_matches':sum(repeats),
        'tool_requests_executed':0,'not_an_end_to_end_policy_replication':True})
    resources=[json.loads(s) for s in (out/'RESOURCE.jsonl').read_text().splitlines()]
    dump_new(ROOT/'CHECKS.json',{'status':'pass','rows_audited':12,'frozen_inputs_and_checkpoint_dependencies_match':True,
        'baseline_replays':4,'baseline_matches':sum(repeats),'input_tokens':sum(len(r['input_token_ids']) for r in rows),
        'output_tokens':sum(len(r['generated_token_ids']) for r in rows),'generation_seconds':sum(r['seconds'] for r in rows),
        'max_sampled_working_bytes':max(p['working_estimate'] for p in resources),
        'max_sampled_rss_bytes':max(p['process_rss'] for p in resources),
        'candidate_selection_and_limited_name_transfer_explicit':True})
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':12,'training_updates':0,'tool_requests_executed':0})
    print(json.dumps(pairs,indent=2))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);a=p.parse_args()
    prepare() if a.stage=='prepare' else run()
