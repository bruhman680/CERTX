"""Outcome-informed lesson-order check, preserving facts and all original results."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from task import render,example_text,decode_action,finish_route
from routing_reference import retrieve
from generate import generate
from runtime_reference import sha,dump_new,append_json,Guard,parameter_digest

def prompt(case,rotation):
    blocks=example_text().split('\n\n');assert len(blocks)==6
    rotated='\n\n'.join(blocks[rotation:]+blocks[:rotation])
    return render(case,True,'direct8').replace(example_text(),rotated)

def prepare():
    parent=ROOT.parent;assert json.loads((parent/'CHECKS.json').read_text())['status']=='pass'
    data=json.loads((parent/'DATA.json').read_text());cases=[]
    for kind,state in [('selected_visible','positive'),('selected_visible','missing'),('none_available','positive'),('none_unavailable','positive')]:
        cases.append(next(c for c in data if c['kind']==kind and c['state']==state and c['style']=='lines'))
    assert len({c['id'] for c in cases})==4
    queries=[]
    labels=['YES','NO','WITHHOLD','TARGET','TARGET','UNKNOWN']
    for c in cases:
        inventory=Counter(prompt(c,0).split())
        for rotation in range(6):
            text=prompt(c,rotation);assert Counter(text.split())==inventory
            queries.append({'id':f'q_{len(queries):03d}','case_id':c['id'],'rotation':rotation,
                            'prompt':text,'last_example_action':labels[(rotation-1)%6]})
    dump_new(ROOT/'DATA.json',cases);dump_new(ROOT/'QUERIES.json',queries)
    acq=parent.parent/'simple-readout-acquisition-v1/run/canonical'
    deps=[parent/n for n in ('task.py','generate.py','routing_reference.py','evidence.py','runtime_reference.py','lora_cpu.py',
                           'DATA.json','CHECKS.json','run/ROUTER_RAW.jsonl','run/WORKER_RAW.jsonl')]
    deps += [acq/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    dump_new(ROOT/'FREEZE.json',{'sha256':{n:sha(ROOT/n) for n in ('check.py','PROTOCOL.md','DATA.json','QUERIES.json')},
        'dependencies':{str(p):sha(p) for p in deps},'timing':'after first factorial outcomes, before all24order-check forwards'})

def run():
    import os
    os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM
    from lora_cpu import inject_lora,load_adapter
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())};queries=json.loads((ROOT/'QUERIES.json').read_text())
    out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl')
    base=Path('/workspace/cache_backend_models/smollm2-135m');acq=ROOT.parent.parent/'simple-readout-acquisition-v1/run/canonical'
    manifest=json.loads((acq/'MANIFEST.json').read_text());assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    torch.set_num_threads(2);torch.manual_seed(73103)
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    guard.read('before_load')
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,acq/'final',base_pin=manifest['base_pin'])
    assert parameter_digest(model,True)==manifest['final_digest']
    worker_rows={w['prompt_sha256']:w for w in (json.loads(s) for s in (ROOT.parent/'run/WORKER_RAW.jsonl').read_text().splitlines())}
    probes=[];routes=[]
    for q in queries:
        p=generate(model,tok,q['prompt'],8,guard,q['id'])
        p.update({'case_id':q['case_id'],'rotation':q['rotation'],'last_example_action':q['last_example_action'],'decision':decode_action(p['text'])})
        append_json(out/'RAW.jsonl',p);probes.append(p)
        case=cases[q['case_id']];action=p['decision']['action'];tool=None;state=None;wid=None
        if action in ('FULL','TARGET'):
            tool=retrieve(case,action)
            if tool['available']:
                text='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+tool['source']
                if tool['kind']=='full':text='Read only the record for the target plot.\n'+text
                w=worker_rows[hashlib.sha256(text.encode()).hexdigest()]
                assert w['messages']==[{'role':'user','content':text}];wid=w['run_id'];state=w['state']
        result=finish_route(case,action,state,tool)
        row={'query_id':q['id'],'case_id':case['id'],'rotation':q['rotation'],**result,'tool':tool,
             'worker_id':wid,'measured_worker_reused':wid is not None}
        append_json(out/'ROUTES.jsonl',row);routes.append(row)
    assert parameter_digest(model,True)==manifest['final_digest']
    assert parameter_digest(model,False)==manifest['base_digest_after']
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    old=[json.loads(s) for s in (ROOT.parent/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    matched=[]
    for p in probes:
        if p['rotation']!=0:continue
        same=[x for x in old if x['examples'] and x['response']=='direct8' and x['input_token_ids']==p['input_token_ids']]
        assert len(same)==1;matched.append(same[0]['generated_token_ids']==p['generated_token_ids'])
    assert len(matched)==4
    summary={'n':24,'recognized':sum(p['decision']['action'] is not None for p in probes),
        'last_example_matches':sum(p['decision']['action']==p['last_example_action'] for p in probes),
        'resolved':sum(r['resolved_in_this_toy'] for r in routes),'grounded_answers':sum(r['grounded_answer'] for r in routes),
        'justified_unknown':sum(r['justified_unknown'] for r in routes),'requests':sum(r['requested'] for r in routes),
        'by_rotation':{str(k):{'last_example':next(q['last_example_action'] for q in queries if q['rotation']==k),
            'actions':dict(Counter(p['decision']['action'] or 'INVALID' for p in probes if p['rotation']==k)),
            'resolved':sum(r['resolved_in_this_toy'] for r in routes if r['rotation']==k)} for k in range(6)}}
    dump_new(out/'SUMMARY.json',summary)
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_router_generations':24,'new_worker_generations':0,
        'logical_routes':24,'training_updates':0,'measured_worker_reuse_explicit':True})
    # Basic transcript and receipt audit; no new model calls.
    for q,p,r in zip(queries,probes,routes):
        assert p['messages']==[{'role':'user','content':prompt(cases[q['case_id']],q['rotation'])}]
        assert p['input_token_ids']==tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)
        assert p['text']==tok.decode(p['generated_token_ids'],skip_special_tokens=True)
        assert p['decision']==decode_action(p['text'])
    resources=[json.loads(s) for s in (out/'RESOURCE.jsonl').read_text().splitlines()]
    dump_new(ROOT/'CHECKS.json',{'status':'pass','rows_audited':24,'frozen_inputs_and_dependencies_match':True,
        'baseline_replays':4,'baseline_replay_matches':sum(matched),'word_inventory_preserved':True,
        'input_tokens':sum(len(p['input_token_ids']) for p in probes),'output_tokens':sum(len(p['generated_token_ids']) for p in probes),
        'generation_seconds':sum(p['seconds'] for p in probes),
        'max_sampled_working_bytes':max(r['working_estimate'] for r in resources),
        'max_sampled_rss_bytes':max(r['process_rss'] for r in resources),
        'no_independent_replication_or_mechanism_claim':True})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);a=p.parse_args()
    prepare() if a.stage=='prepare' else run()
