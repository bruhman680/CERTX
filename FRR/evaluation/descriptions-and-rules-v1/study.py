"""Prospective declared decoder and order-balanced rule/example contact."""
from pathlib import Path
from collections import Counter
import hashlib
import json
from io_utils import sha,dump_new,append
from decoder import fixtures,decode_v1,decode_v2
from domain import render,finish_route,observed_rule
from routing_reference import retrieve
from evidence import STATES,parse

ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent/'planning-and-examples-v1'
ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'

def prepare():
    cases=[]
    for i,state in enumerate(STATES):
        for order in range(2):
            recs=[('Clover',state),('Heather',STATES[(i+1)%3])]
            if order:recs.reverse()
            body='\n\n'.join(f'Record {j+1}:\nPlot: {n}\nStatus: {s}' for j,(n,s) in enumerate(recs))
            source='Target plot: Clover\n\n'+body;p=parse(source)
            for kind in ('selected_visible','none_available','other_visible','none_unavailable'):
                visible=p['crop'] if kind=='selected_visible' else p['other_crop'] if kind=='other_visible' else None
                cases.append({'id':f'c_{len(cases):03d}','target':'Clover','source':source,'state':state,
                    'kind':kind,'visible_display':visible,'archive_available':kind!='none_unavailable'})
    queries=[];links=[];seen={}
    for c in cases:
        for kind,n in [('none',1),('rule',3),('examples',6)]:
            for rotation in range(n):
                text=render(c,kind,rotation)
                if text not in seen:
                    qid=f'q_{len(queries):03d}';seen[text]=qid
                    queries.append({'id':qid,'prompt':text,'guidance':kind,'rotation':rotation})
                links.append({'case_id':c['id'],'query_id':seen[text],'guidance':kind,'rotation':rotation})
    assert len(cases)==24 and len(queries)==80 and len(links)==240
    dump_new(ROOT/'DATA.json',cases);dump_new(ROOT/'QUERIES.json',queries);dump_new(ROOT/'LINKS.json',links)
    dump_new(ROOT/'DECODER_FIXTURES.json',fixtures())
    assert sha(ROOT/'generate.py')==sha(PRIOR/'generate.py')
    deps=[ACQ/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    deps += [PRIOR/'run/ROUTER_RAW.jsonl',PRIOR/'run/LOGIT_HEAD_CHECK.json']
    names=['DATA.json','QUERIES.json','LINKS.json','DECODER_FIXTURES.json','PROTOCOL.md','study.py',
        'decoder.py','domain.py','test_study.py','io_utils.py','generate.py','task_reference.py',
        'routing_reference.py','evidence.py','runtime_reference.py','lora_cpu.py']
    dump_new(ROOT/'FREEZE.json',{'sha256':{n:sha(ROOT/n) for n in names},
        'dependencies':{str(p):sha(p) for p in deps},'timing':'before tokenizer/model load and all80new forwards'})
    print('Frozen24scenarios,80actual router queries;43declared decoder fixtures')

def replay():
    f=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in f['sha256'].items())
    fixtures_data=json.loads((ROOT/'DECODER_FIXTURES.json').read_text())
    assert all(decode_v2(x['text'])['action']==x['expected'] for x in fixtures_data)
    old=[json.loads(s) for s in (PRIOR/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    rows=[{'run_id':p['run_id'],'strict_v1':decode_v1(p['text']),'declared_v2':decode_v2(p['text']),
           'raw_text':p['text']} for p in old]
    dump_new(ROOT/'HISTORICAL_DECODER_REPLAY.json',{'scope':'development/regression replay,not fresh model evidence or revised old scores',
        'new_model_calls':0,'rows':rows,'strict_recognized':sum(r['strict_v1'] is not None for r in rows),
        'v2_recognized':sum(r['declared_v2']['action'] is not None for r in rows),'fixture_expectations':len(fixtures_data)})
    print('Declared decoder fixtures and historical replay complete')

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
    queries=json.loads((ROOT/'QUERIES.json').read_text());links=json.loads((ROOT/'LINKS.json').read_text())
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    assert json.loads((ROOT/'HISTORICAL_DECODER_REPLAY.json').read_text())['fixture_expectations']==43
    out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl')
    base=Path('/workspace/cache_backend_models/smollm2-135m');manifest=json.loads((ACQ/'MANIFEST.json').read_text())
    assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    torch.set_num_threads(2);torch.manual_seed(73103)
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in queries}
    assert max(lengths.values())<=768
    dump_new(out/'TOKENIZATION.json',{'prompt_lengths':lengths,'max_prompt_tokens':max(lengths.values()),'no_truncation':True})
    guard.read('before_model_load')
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=manifest['base_pin'])
    assert parameter_digest(model,True)==manifest['final_digest']
    probes={}
    for i,q in enumerate(queries,1):
        p=generate(model,tok,q['prompt'],24,guard,q['id'])
        p.update({'guidance':q['guidance'],'rotation':q['rotation'],
            'strict_v1':decode_v1(p['text']),'declared_v2':decode_v2(p['text'])})
        append(out/'ROUTER_RAW.jsonl',p);probes[q['id']]=p
        if i%16==0:print(json.dumps({'router_probes':i,'planned':80}),flush=True)
    workers={};routes=[]
    def execute(c,action,meta):
        tool=None;state=None;wid=None;hit=False
        if action in ('FULL','TARGET'):
            tool=retrieve(c,action)
            if tool['available']:
                text='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+tool['source']
                if tool['kind']=='full':text='Read only the record for the target plot.\n'+text
                key=hashlib.sha256(text.encode()).hexdigest();hit=key in workers
                if not hit:
                    w=generate(model,tok,text,8,guard,f'worker_{len(workers):03d}')
                    w.update({'prompt_sha256':key,'state':{'YES':'positive','NO':'zero','WITHHOLD':'missing'}.get(w['text'].strip())})
                    append(out/'WORKER_RAW.jsonl',w);workers[key]=w
                w=workers[key];state=w['state'];wid=w['run_id']
        row={'route_id':f'route_{len(routes):04d}','case_id':c['id'],'kind':c['kind'],**meta,
            **finish_route(c,action,state,tool),'tool':tool,'worker_id':wid,'worker_cache_hit':hit}
        append(out/'ROUTES.jsonl',row);routes.append(row)
    for link in links:
        p=probes[link['query_id']]
        for decoder in ('strict_v1','declared_v2'):
            action=p['strict_v1'] if decoder=='strict_v1' else p['declared_v2']['action']
            execute(cases[link['case_id']],action,{'query_id':link['query_id'],'guidance':link['guidance'],
                'rotation':link['rotation'],'decoder':decoder,'policy':link['guidance']+'__'+str(link['rotation'])+'__'+decoder})
    for policy in ('always_target','always_full','always_unknown','observed_rule'):
        for c in cases.values():
            action={'always_target':'TARGET','always_full':'FULL','always_unknown':'UNKNOWN'}.get(policy)
            if policy=='observed_rule':action=observed_rule(c)
            execute(c,action,{'query_id':None,'guidance':'mechanical','rotation':None,'decoder':None,'policy':policy})
    assert len(routes)==576 and len(workers)==9
    assert parameter_digest(model,True)==manifest['final_digest']
    assert parameter_digest(model,False)==manifest['base_digest_after']
    assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
    assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_router_generations':80,'actual_worker_generations':9,
        'logical_policy_routes':576,'training_updates':0,'no_forced_action_projection':True,
        'old_data_scores_and_saved_weights_unchanged':True})
    print(json.dumps({'complete':True,'routers':80,'workers':9,'routes':576}),flush=True)

def metrics(rows):
    return {'n':len(rows),'actions':dict(Counter(r['action'] or 'INVALID' for r in rows)),
        'grounded_answers':sum(r['grounded_answer'] for r in rows),'justified_unknown':sum(r['justified_unknown'] for r in rows),
        'resolved':sum(r['resolved_in_this_toy'] for r in rows),'invalid_actions':sum(r['end']=='INVALID_ACTION' for r in rows),
        'requests':sum(r['requested'] for r in rows),'unavailable_requests':sum(r['unavailable_request'] for r in rows),
        'unknown_policy':sum(r['end']=='UNKNOWN_POLICY' for r in rows),'unknown_tool':sum(r['end']=='UNKNOWN_TOOL' for r in rows),
        'deferred_with_evidence':sum(r['unknown_with_accessible_evidence'] for r in rows),
        'nominal_cost':sum(r['nominal_tool_cost'] for r in rows)}

def summarize(rows,probes):
    policies={}
    for key in sorted({r['policy'] for r in rows}):
        rs=[r for r in rows if r['policy']==key]
        policies[key]={'total':metrics(rs),'by_kind':{k:metrics([r for r in rs if r['kind']==k]) for k in sorted({r['kind'] for r in rs})}}
    return {'policies':policies,'router_groups':{kind:{'n':sum(p['guidance']==kind for p in probes),
        'stops_at_cap':sum(p['guidance']==kind and p['stop']=='token_limit' for p in probes),
        'v1_recognized':sum(p['guidance']==kind and p['strict_v1'] is not None for p in probes),
        'v2_recognized':sum(p['guidance']==kind and p['declared_v2']['action'] is not None for p in probes),
        'generation_seconds':sum(p['seconds'] for p in probes if p['guidance']==kind)} for kind in ('none','rule','examples')}}

def score():
    rows=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
    probes=[json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    assert len(rows)==576 and len(probes)==80
    dump_new(ROOT/'run/SUMMARY.json',summarize(rows,probes))
    print(json.dumps({k:v['total'] for k,v in summarize(rows,probes)['policies'].items()},indent=2))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','replay','run','score']);a=p.parse_args()
    {'prepare':prepare,'replay':replay,'run':run,'score':score}[a.stage]()
