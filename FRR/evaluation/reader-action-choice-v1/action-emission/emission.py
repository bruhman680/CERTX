"""Explicit action-word emission control, not an evidence-routing task."""
from pathlib import Path
from collections import Counter
import gc
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
import torch
from routing import ACTIONS
from probe import probe
from runtime_reference import sha,dump_new,append_json,Guard,parameter_digest
from lora_cpu import inject_lora,load_adapter

def prepare():
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('plain_control',ROOT.parent/'plain-actions/plain.py')
    m=module_from_spec(spec);spec.loader.exec_module(m)
    cases=[]
    for action in ACTIONS:
        for frame in ('repeat','return'):
            text=('Repeat the next word exactly. Reply with that word only.\n\n'+action if frame=='repeat' else
                  'Return only this action word, with no other text: '+action)
            cases.append({'id':f'copy_{action}_{frame}','prompt':text,'expected':action,'frame':frame})
    dump_new(ROOT/'DATA.json',cases)
    acq=ROOT.parent.parent/'simple-readout-acquisition-v1/run/canonical'
    deps=[ROOT.parent/n for n in ('PLAN.json','routing.py','probe.py','runtime_reference.py','lora_cpu.py')]
    deps += [ROOT.parent/'plain-actions/plain.py']
    deps += [acq/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    dump_new(ROOT/'FREEZE.json',{'sha256':{n:sha(ROOT/n) for n in ('emission.py','PROTOCOL.md','DATA.json')},
        'dependencies':{str(p):sha(p) for p in deps},'timing':'after both routing outcomes, before explicit-action control forwards'})

def run():
    from transformers import AutoTokenizer,AutoModelForCausalLM
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('plain_control',ROOT.parent/'plain-actions/plain.py')
    m=module_from_spec(spec);spec.loader.exec_module(m)
    freeze=json.loads((ROOT/'FREEZE.json').read_text());plan=json.loads((ROOT.parent/'PLAN.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    cases=json.loads((ROOT/'DATA.json').read_text());out=ROOT/'run';out.mkdir()
    base=Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base/'model.safetensors')==plan['base_weights_sha256']
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    torch.set_num_threads(2);guard=Guard(plan['working_limit_bytes'],out/'RESOURCE.jsonl')
    acq=ROOT.parent.parent/'simple-readout-acquisition-v1/run/canonical'
    manifest=json.loads((acq/'MANIFEST.json').read_text());rows=[]
    for router in plan['routers']:
        torch.manual_seed(plan['seed']);guard.read('before_load',router=router)
        model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
            use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
        if router=='adapted':
            inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,acq/'final',base_pin=manifest['base_pin'])
            assert parameter_digest(model,True)==manifest['final_digest']
        for c in cases:
            row=probe(model,tok,c['prompt'],dict(zip(ACTIONS,ACTIONS)),guard,router+'__'+c['id'])
            row.update({'router':router,'case_id':c['id'],'expected':c['expected'],'frame':c['frame'],
                'parsed_action':m.first_action(row['text']),
                'exact_correct':row['text'].strip()==c['expected'],
                'prefix_correct':m.first_action(row['text'])==c['expected'],
                'forced_correct':row['forced_key']==c['expected']})
            append_json(out/'RAW.jsonl',row);rows.append(row)
        if router=='adapted':
            assert parameter_digest(model,True)==manifest['final_digest']
            assert parameter_digest(model,False)==manifest['base_digest_after']
        del model;gc.collect()
    summary={}
    for router in plan['routers']:
        rs=[r for r in rows if r['router']==router]
        summary[router]={'n':12,'exact_correct':sum(r['exact_correct'] for r in rs),
            'prefix_correct':sum(r['prefix_correct'] for r in rs),'forced_correct':sum(r['forced_correct'] for r in rs),
            'by_action':{a:{'n':2,'exact_correct':sum(r['expected']==a and r['exact_correct'] for r in rs),
                'prefix_correct':sum(r['expected']==a and r['prefix_correct'] for r in rs)} for a in ACTIONS}}
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    assert sha(base/'model.safetensors')==plan['base_weights_sha256']
    dump_new(out/'SUMMARY.json',summary)
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':24,'candidate_sequences':144,
        'optimizer_updates':0,'tool_requests_executed':0,'no_evidence_policy_claim':True})
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run']);a=p.parse_args()
    prepare() if a.stage=='prepare' else run()
