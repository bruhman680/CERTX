"""Bounded cyclic menu-position x evidence-block-order test; fixed adapted reader."""
from pathlib import Path
from collections import Counter
import importlib.util
import json
import re

ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent/'reader-action-choice-v1'
ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'
from routing import ACTIONS,observation
from runtime_reference import sha,dump_new,append_json,Guard,parameter_digest

HEADER=('Determine the target status. Choose your next action. Start your reply with one action word from the menu. '
        'You may add brief text afterward. At most one request is allowed. '
        'WITHHOLD is a recorded missing status; UNKNOWN means insufficient evidence.')
DESCRIPTIONS={'YES':'answer positive','NO':'answer zero','WITHHOLD':'answer explicitly missing',
              'FULL':'request full source, cost2','TARGET':'request target record, cost1',
              'UNKNOWN':'report insufficient evidence'}

def command(text):
    m=re.match(r'^\s*(YES|NO|WITHHOLD|FULL|TARGET|UNKNOWN)\b',text,re.I)
    return m[1].upper() if m else None

def render(case,rotation,block_order):
    seq=ACTIONS[rotation:]+ACTIONS[:rotation]
    menu='\n'.join(a+': '+DESCRIPTIONS[a] for a in seq)
    blocks=[observation(case),menu] if block_order=='evidence_first' else [menu,observation(case)]
    return HEADER+'\n\n'+'\n\n'.join(blocks)+'\n\nAction:'

def prepare():
    source=json.loads((PRIOR/'DATA.json').read_text());cases=[]
    for state in ('positive','zero','missing'):
        c=next(c for c in source if c['kind']=='selected_visible' and c['state']==state)
        cases.append({**c,'obs_id':state,'desired_action':{'positive':'YES','zero':'NO','missing':'WITHHOLD'}[state]})
    c=next(c for c in source if c['kind']=='none_unavailable')
    cases.append({**c,'obs_id':'unavailable','desired_action':'UNKNOWN'})
    queries=[]
    for c in cases:
        for order in ('evidence_first','menu_first'):
            for rotation in range(6):
                queries.append({'id':f'q_{len(queries):03d}','obs_id':c['obs_id'],
                    'block_order':order,'rotation':rotation,'prompt':render(c,rotation,order)})
    assert len(queries)==len({q['prompt'] for q in queries})==48
    # Exact old forward prompts, not a changed wording presented as a replication.
    spec=importlib.util.spec_from_file_location('old_plain',PRIOR/'plain-actions/plain.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    assert all(render(c,0,'evidence_first')==old.plain_prompt(c,'forward') for c in cases)
    dump_new(ROOT/'OBSERVATIONS.json',cases);dump_new(ROOT/'QUERIES.json',queries)
    deps=[ACQ/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    deps += [PRIOR/n for n in ('DATA.json','plain-actions/plain.py','plain-actions/run/RAW.jsonl')]
    names=['OBSERVATIONS.json','QUERIES.json','PROTOCOL.md','study.py','test_order.py',
           'probe.py','routing.py','evidence.py','runtime_reference.py','lora_cpu.py']
    dump_new(ROOT/'FREEZE.json',{'sha256':{n:sha(ROOT/n) for n in names},
        'dependencies':{str(p):sha(p) for p in deps},'timing':'before tokenizer/model load and all48new forwards',
        'selection':'fixed adapted reader because prior order effect; exposed four observations, not fresh primary'})
    print('Frozen4observations x6rotations x2blockorders=48probes')

def run():
    import os
    os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM
    from lora_cpu import inject_lora,load_adapter
    from probe import probe
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    queries=json.loads((ROOT/'QUERIES.json').read_text());out=ROOT/'run';out.mkdir()
    manifest=json.loads((ACQ/'MANIFEST.json').read_text())
    base=Path('/workspace/cache_backend_models/smollm2-135m')
    assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    torch.set_num_threads(2);torch.manual_seed(73103)
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    guard=Guard(5153960755,out/'RESOURCE.jsonl');guard.read('before_load')
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=manifest['base_pin'])
    assert parameter_digest(model,True)==manifest['final_digest']
    for i,q in enumerate(queries,1):
        row=probe(model,tok,q['prompt'],dict(zip(ACTIONS,ACTIONS)),guard,q['id'])
        row.update({'obs_id':q['obs_id'],'block_order':q['block_order'],'rotation':q['rotation'],
                    'parsed_action':command(row['text'])})
        append_json(out/'RAW.jsonl',row)
        if i%12==0:print(json.dumps({'complete':i,'planned':48}),flush=True)
    assert parameter_digest(model,True)==manifest['final_digest']
    assert parameter_digest(model,False)==manifest['base_digest_after']
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
    dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':48,'candidate_sequences':288,
        'optimizer_updates':0,'tool_requests_executed':0,'base_adapter_old_records_unchanged':True})

def finish():
    from transformers import AutoTokenizer
    from evidence import parse
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    cases={c['obs_id']:c for c in json.loads((ROOT/'OBSERVATIONS.json').read_text())}
    queries={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())}
    rows=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()]
    assert len(rows)==len({r['probe_id'] for r in rows})==48
    for r in rows:
        q=queries[r['probe_id']];c=cases[r['obs_id']]
        assert r['messages']==[{'role':'user','content':render(c,r['rotation'],r['block_order'])}]
        assert r['messages'][0]['content']==q['prompt']
        assert r['input_token_ids']==tok.apply_chat_template(r['messages'],tokenize=True,add_generation_prompt=True)
        assert r['text']==tok.decode(r['generated_token_ids'],skip_special_tokens=True)
        assert r['parsed_action']==command(r['text'])
        assert r['free_key']==(r['text'].strip() if r['text'].strip() in ACTIONS else None)
        for a in ACTIONS:
            s=r['scores'][a];assert s['label']==a and s['ids']==tok.encode(a,add_special_tokens=False)+[tok.eos_token_id]
            assert s['sum']==sum(s['token_logprobs']) and s['mean']==s['sum']/len(s['token_logprobs'])
        assert r['forced_key']==max(ACTIONS,key=lambda a:r['scores'][a]['sum'])
    def metrics(rs):
        visible=[r for r in rs if r['obs_id']!='unavailable'];absent=[r for r in rs if r['obs_id']=='unavailable']
        positions=Counter()
        for r in rs:
            if r['parsed_action'] is not None:
                seq=ACTIONS[r['rotation']:]+ACTIONS[:r['rotation']]
                positions[str(seq.index(r['parsed_action'])+1)]+=1
        return {'n':len(rs),'recognized':sum(r['parsed_action'] is not None for r in rs),
            'exact_words':sum(r['free_key'] is not None for r in rs),
            'actions':dict(Counter(r['parsed_action'] or 'INVALID' for r in rs)),
            'selected_menu_positions':dict(positions),
            'visible_cases':len(visible),'visible_correct_action':sum(r['parsed_action']==cases[r['obs_id']]['desired_action'] for r in visible),
            'unavailable_cases':len(absent),'unavailable_UNKNOWN':sum(r['parsed_action']=='UNKNOWN' for r in absent),
            'forced_expected_action':sum(r['forced_key']==cases[r['obs_id']]['desired_action'] for r in rs)}
    summary={'by_block_order':{},'by_rotation':{},'by_observation':{}}
    for order in ('evidence_first','menu_first'):
        summary['by_block_order'][order]=metrics([r for r in rows if r['block_order']==order])
        for k in range(6):summary['by_rotation'][order+'__'+str(k)]=metrics([r for r in rows if (r['block_order'],r['rotation'])==(order,k)])
        for obs in cases:summary['by_observation'][order+'__'+obs]=metrics([r for r in rows if (r['block_order'],r['obs_id'])==(order,obs)])
    bykey={(r['obs_id'],r['rotation'],r['block_order']):r for r in rows};pairs=[]
    for obs in cases:
        for k in range(6):
            a,b=bykey[obs,k,'evidence_first'],bykey[obs,k,'menu_first']
            valid=a['parsed_action'] is not None and b['parsed_action'] is not None
            pairs.append({'obs_id':obs,'rotation':k,'before':a['parsed_action'],'after':b['parsed_action'],
                'both_valid':valid,'changed_valid_action':valid and a['parsed_action']!=b['parsed_action']})
    summary['block_order_pairs']={'n':24,'both_valid':sum(p['both_valid'] for p in pairs),
        'changed_valid_action':sum(p['changed_valid_action'] for p in pairs),'pairs':pairs}
    old=[json.loads(s) for s in (PRIOR/'plain-actions/run/RAW.jsonl').read_text().splitlines()]
    matches=[]
    for r in rows:
        if r['rotation']!=0 or r['block_order']!='evidence_first':continue
        same=[p for p in old if p['router']=='adapted' and p['input_token_ids']==r['input_token_ids']]
        assert len(same)==1
        matches.append(same[0]['generated_token_ids']==r['generated_token_ids'])
    assert len(matches)==4
    previous=json.loads(Path('/workspace/exposure-order-before.json').read_text())
    assert all(sha(Path('/workspace/frr')/n)==h for n,h in previous.items())
    resources=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
    checks={'status':'pass','rows_audited':48,'frozen_inputs_and_dependencies_match':True,
        'old_local_files_unchanged_before_sync':len(previous),'replication_baseline_matches':sum(matches),'replication_baselines':4,
        'prompt_token_decode_score_checks':True,'input_tokens':sum(len(r['input_token_ids']) for r in rows),
        'output_tokens':sum(len(r['generated_token_ids']) for r in rows),'probe_seconds':sum(r['seconds'] for r in rows),
        'max_sampled_working_bytes':max(p['working_estimate'] for p in resources),
        'max_sampled_rss_bytes':max(p['process_rss'] for p in resources),
        'no_training_or_linear_internal_reasoning_claim':True}
    dump_new(ROOT/'run/SUMMARY.json',summary);dump_new(ROOT/'CHECKS.json',checks)
    print(json.dumps({'by_block_order':summary['by_block_order'],'changed_block_pairs':summary['block_order_pairs']['changed_valid_action'],'checks':checks},indent=2))

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','run','finish']);a=p.parse_args()
    {'prepare':prepare,'run':run,'finish':finish}[a.stage]()
