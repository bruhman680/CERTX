"""Observe real finite-menu choices, then execute one requested retrieval at most."""
from pathlib import Path
import gc
import hashlib
import json
import os

os.environ['HF_HUB_OFFLINE']='1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
import torch
from probe import probe
from routing import CODES, retrieve, simple_rule, terminal
from lora_cpu import inject_lora, load_adapter
from runtime_reference import sha, Guard, dump_new, append_json, parameter_digest

ROOT=Path(__file__).resolve().parent
BASE=Path('/workspace/cache_backend_models/smollm2-135m')
ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'

def main():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    plan=json.loads((ROOT/'PLAN.json').read_text())
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    assert sha(BASE/'model.safetensors')==plan['base_weights_sha256']
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    menus={m['id']:m for m in json.loads((ROOT/'MENUS.json').read_text())}
    queries=json.loads((ROOT/'QUERIES.json').read_text());links=json.loads((ROOT/'LINKS.json').read_text())
    out=ROOT/'run';out.mkdir()
    torch.set_num_threads(2)
    tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
    assert all(len(tok.encode(c,add_special_tokens=False))==1 for c in CODES)
    assert all(len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True))<=256 for q in queries)
    guard=Guard(plan['working_limit_bytes'],out/'RESOURCE.jsonl')
    manifest=json.loads((ACQ/'MANIFEST.json').read_text())
    router_rows={}
    model=None
    for router in plan['routers']:
        torch.manual_seed(plan['seed']);guard.read('before_model_load',router=router)
        model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,
            use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
        if router=='adapted':
            inject_lora(model,rank=4,alpha=8,dropout=0.)
            load_adapter(model,ACQ/'final',base_pin=manifest['base_pin'])
            assert parameter_digest(model,True)==manifest['final_digest']
            assert parameter_digest(model,False)==manifest['base_digest_after']
        for i,q in enumerate(queries):
            row=probe(model,tok,q['prompt'],dict(zip(CODES,CODES)),guard,router+'__'+q['id'])
            row.update({'router':router,'query_id':q['id'],'menu_id':q['menu_id']})
            append_json(out/'ROUTER_RAW.jsonl',row);router_rows[router,q['id']]=row
        print(json.dumps({'router':router,'unique_action_probes':len(queries)}),flush=True)
        if router=='original':
            del model;model=None;gc.collect()
    # The adapted router is also the fixed worker, in a fresh cache each probe.
    assert model is not None
    workers={};worker_count=0;routes=[]
    def execute(case,action,identity):
        nonlocal worker_count
        tool=None;state=None;worker_id=None;cache_hit=False
        if action in ('FULL','TARGET'):
            tool=retrieve(case,action)
            if tool['available']:
                mapping='; '.join(f'{s}={label}' for s,label in plan['worker_mapping'].items())
                text=plan['worker_template'].format(mapping=mapping,source=tool['source'])
                if tool['kind']=='full':text=plan['worker_full_prefix']+text
                key=hashlib.sha256(text.encode()).hexdigest()
                cache_hit=key in workers
                if not cache_hit:
                    worker_id=f'worker_{worker_count:03d}';worker_count+=1
                    answer=probe(model,tok,text,plan['worker_mapping'],guard,worker_id)
                    answer.update({'worker_prompt_sha256':key,'kind':tool['kind']})
                    append_json(out/'WORKER_RAW.jsonl',answer);workers[key]=answer
                answer=workers[key];worker_id=answer['probe_id'];state=answer['free_key']
        result=terminal(case,action,worker_state=state,tool=tool)
        record={'route_id':f'route_{len(routes):04d}','case_id':case['id'],'kind':case['kind'],
            **identity,**result,'tool':tool,'worker_probe_id':worker_id,'worker_cache_hit':cache_hit}
        append_json(out/'ROUTES.jsonl',record);routes.append(record)
    for router in plan['routers']:
        for link in links:
            row=router_rows[router,link['query_id']];menu=menus[link['menu_id']]
            for mode in plan['modes']:
                code=row['free_key'] if mode=='free' else row['forced_key']
                action=menu['mapping'].get(code)
                execute(cases[link['case_id']],action,{'policy':router+'__'+mode,'router':router,'mode':mode,
                    'menu_id':menu['id'],'router_probe_id':row['probe_id'],'chosen_code':code})
    for policy in plan['fixed_policies']:
        for case in cases.values():
            action={'always_target':'TARGET','always_full':'FULL','always_unknown':'UNKNOWN'}.get(policy)
            if policy=='observed_rule':action=simple_rule(case)
            execute(case,action,{'policy':policy,'router':None,'mode':'mechanical','menu_id':None,
                                 'router_probe_id':None,'chosen_code':None})
    assert len(routes)==480 and len(router_rows)==64 and worker_count==9
    assert parameter_digest(model,True)==manifest['final_digest']
    assert parameter_digest(model,False)==manifest['base_digest_after']
    assert sha(BASE/'model.safetensors')==plan['base_weights_sha256']
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_router_generations':64,
        'actual_worker_generations':worker_count,'router_choice_sequences':384,'worker_choice_sequences':27,
        'logical_policy_routes':len(routes),'optimizer_updates':0,'base_adapter_unchanged':True,
        'worker_cache_is_explicit_within_run':True,'free_invalid_actions_not_overridden':True})
    print(json.dumps({'complete':True,'router_generations':64,'worker_generations':worker_count,'routes':len(routes)}),flush=True)

if __name__=='__main__':
    main()
