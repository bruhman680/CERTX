"""Outcome-informed plain-command follow-up; coded failures remain unchanged."""
from pathlib import Path
from collections import Counter
import gc
import hashlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
import torch
from routing import ACTIONS,observation,retrieve,terminal
from probe import probe
from runtime_reference import sha,dump_new,append_json,Guard,parameter_digest
from lora_cpu import inject_lora,load_adapter
from score import metrics

def first_action(text):
    m=re.match(r'^\s*(YES|NO|WITHHOLD|FULL|TARGET|UNKNOWN)\b',text,re.I)
    return m[1].upper() if m else None

def plain_prompt(case,order):
    desc={'YES':'answer positive','NO':'answer zero','WITHHOLD':'answer explicitly missing',
          'FULL':'request full source, cost2','TARGET':'request target record, cost1',
          'UNKNOWN':'report insufficient evidence'}
    seq=ACTIONS if order=='forward' else ACTIONS[::-1]
    menu='\n'.join(a+': '+desc[a] for a in seq)
    return ('Determine the target status. Choose your next action. Start your reply with one action word from the menu. '
            'You may add brief text afterward. At most one request is allowed. '
            'WITHHOLD is a recorded missing status; UNKNOWN means insufficient evidence.\n\n'+
            observation(case)+'\n\n'+menu+'\n\nAction:')

def prepare():
    parent=ROOT.parent
    assert json.loads((parent/'CHECKS.json').read_text())['status']=='pass'
    cases=json.loads((parent/'DATA.json').read_text())
    queries=[];links=[];seen={}
    for c in cases:
        for order in ('forward','reverse'):
            text=plain_prompt(c,order)
            if text not in seen:
                qid=f'q_{len(queries):03d}';seen[text]=qid;queries.append({'id':qid,'order':order,'prompt':text})
            links.append({'case_id':c['id'],'query_id':seen[text],'order':order})
    assert len(queries)==16 and len(links)==48
    dump_new(ROOT/'QUERIES.json',queries);dump_new(ROOT/'LINKS.json',links)
    acq=parent.parent/'simple-readout-acquisition-v1/run/canonical'
    deps=[parent/n for n in ('DATA.json','PLAN.json','CHECKS.json','run/ROUTER_RAW.jsonl','run/WORKER_RAW.jsonl',
                            'routing.py','probe.py','score.py','evidence.py','runtime_reference.py','lora_cpu.py')]
    deps += [acq/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    dump_new(ROOT/'FREEZE.json',{'sha256':{n:sha(ROOT/n) for n in ('plain.py','PROTOCOL.md','test_plain.py','QUERIES.json','LINKS.json')},
          'dependencies':{str(p):sha(p) for p in deps},
          'timing':'after coded results; before all plain-action forwards',
          'interface_change':'prefix command and optional text, not retroactive passing of strict coded output'})

def run():
    from transformers import AutoTokenizer,AutoModelForCausalLM
    parent=ROOT.parent;plan=json.loads((parent/'PLAN.json').read_text());freeze=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    cases={c['id']:c for c in json.loads((parent/'DATA.json').read_text())}
    queries=json.loads((ROOT/'QUERIES.json').read_text());links=json.loads((ROOT/'LINKS.json').read_text())
    out=ROOT/'run';out.mkdir();guard=Guard(plan['working_limit_bytes'],out/'RESOURCE.jsonl')
    base=Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base/'model.safetensors')==plan['base_weights_sha256']
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    torch.set_num_threads(2)
    acq=parent.parent/'simple-readout-acquisition-v1/run/canonical'
    manifest=json.loads((acq/'MANIFEST.json').read_text());probes={}
    for router in plan['routers']:
        torch.manual_seed(plan['seed']);guard.read('before_load',router=router)
        model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
            use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
        if router=='adapted':
            inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,acq/'final',base_pin=manifest['base_pin'])
            assert parameter_digest(model,True)==manifest['final_digest']
        for q in queries:
            row=probe(model,tok,q['prompt'],dict(zip(ACTIONS,ACTIONS)),guard,router+'__'+q['id'])
            row.update({'router':router,'query_id':q['id'],'order':q['order'],'parsed_action':first_action(row['text'])})
            append_json(out/'RAW.jsonl',row);probes[router,q['id']]=row
        if router=='adapted':
            assert parameter_digest(model,True)==manifest['final_digest']
            assert parameter_digest(model,False)==manifest['base_digest_after']
        del model;gc.collect();print(json.dumps({'router':router,'probes':16}),flush=True)
    # Worker responses were measured in the coded contact on these exact prompts
    # with the same fixed canonical checkpoint. This is explicit measured reuse,
    # not additional worker inference or an independent end-to-end replication.
    workers={r['worker_prompt_sha256']:r for r in (json.loads(s) for s in (parent/'run/WORKER_RAW.jsonl').read_text().splitlines())}
    routes=[]
    for router in plan['routers']:
        for link in links:
            c=cases[link['case_id']];p=probes[router,link['query_id']]
            for mode in ('free','forced'):
                action=p['parsed_action'] if mode=='free' else p['forced_key']
                tool=None;state=None;worker_id=None
                if action in ('FULL','TARGET'):
                    tool=retrieve(c,action)
                    if tool['available']:
                        mapping='; '.join(f'{s}={v}' for s,v in plan['worker_mapping'].items())
                        text=plan['worker_template'].format(mapping=mapping,source=tool['source'])
                        if tool['kind']=='full':text=plan['worker_full_prefix']+text
                        key=hashlib.sha256(text.encode()).hexdigest();w=workers[key]
                        assert w['messages']==[{'role':'user','content':text}]
                        worker_id=w['probe_id'];state=w['free_key']
                result=terminal(c,action,state,tool)
                row={'route_id':f'plain_{len(routes):04d}','case_id':c['id'],'kind':c['kind'],
                     'policy':router+'__'+mode,'router':router,'mode':mode,'order':link['order'],
                     'probe_id':p['probe_id'],**result,'tool':tool,'worker_probe_id':worker_id,
                     'worker_reused_from_coded_contact':worker_id is not None,'worker_cache_hit':worker_id is not None}
                append_json(out/'ROUTES.jsonl',row);routes.append(row)
    assert len(routes)==192
    summary={'routers':{},'policies':{}}
    for router in plan['routers']:
        rs=[p for p in probes.values() if p['router']==router]
        summary['routers'][router]={'n':16,'recognized_prefixes':sum(p['parsed_action'] is not None for p in rs),
            'exact_action_words':sum(p['free_key'] is not None for p in rs),
            'free_texts':dict(Counter(p['text'].strip() for p in rs)),
            'parsed_actions':dict(Counter(p['parsed_action'] or 'INVALID' for p in rs)),
            'forced_actions':dict(Counter(p['forced_key'] for p in rs))}
        for mode in ('free','forced'):
            rs=[r for r in routes if r['policy']==router+'__'+mode]
            summary['policies'][router+'__'+mode]={'total':metrics(rs),
                'by_order':{order:metrics([r for r in rs if r['order']==order]) for order in ('forward','reverse')}}
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    assert sha(base/'model.safetensors')==plan['base_weights_sha256']
    dump_new(out/'SUMMARY.json',summary)
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_action_generations':32,'choice_sequences':192,
        'new_worker_generations':0,'logical_policy_routes':192,'optimizer_updates':0,
        'coded_failures_unchanged':True,'measured_worker_reuse_explicit':True})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);a=p.parse_args()
    prepare() if a.stage=='prepare' else run()
