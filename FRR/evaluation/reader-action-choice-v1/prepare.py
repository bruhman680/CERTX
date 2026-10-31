"""Freeze finite action choice, original/adapted routers and fixed-policy controls."""
from pathlib import Path
import hashlib
import json
from evidence import STATES, parse
from routing import layout, router_prompt

ROOT = Path(__file__).resolve().parent
ACQ = ROOT.parent / 'simple-readout-acquisition-v1'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def put(n, v):
    with (ROOT/n).open('x') as f:
        json.dump(v, f, indent=2, sort_keys=True); f.write('\n')

def main():
    cases = []
    for i, state in enumerate(STATES):
        for order in range(2):
            recs = [('Rowan', state), ('Aspen', STATES[(i+1)%3])]
            if order:
                recs.reverse()
            body = '\n\n'.join(f'Record {j+1}:\nPlot: {n}\nStatus: {s}' for j, (n, s) in enumerate(recs))
            source = 'Target plot: Rowan\n\n'+body
            parsed = parse(source)
            for kind in ('selected_visible', 'none_available', 'other_visible', 'none_unavailable'):
                visible = parsed['crop'] if kind=='selected_visible' else parsed['other_crop'] if kind=='other_visible' else None
                cases.append({'id': f'c_{len(cases):03d}', 'world_id': f'w_{i}_{order}',
                    'target': 'Rowan', 'source': source, 'state': state, 'kind': kind,
                    'visible': visible, 'archive_available': kind!='none_unavailable'})
    menus = [layout(c, d) for c in ('direct','reverse') for d in ('forward','reverse')]
    queries, links, seen = [], [], {}
    for case in cases:
        for menu in menus:
            text = router_prompt(case, menu)
            if text not in seen:
                qid = f'q_{len(queries):03d}';seen[text]=qid
                queries.append({'id': qid, 'prompt': text, 'menu_id': menu['id']})
            links.append({'case_id': case['id'], 'menu_id': menu['id'], 'query_id': seen[text]})
    assert len(cases)==24 and len(queries)==32 and len(links)==96
    prior = json.loads((ACQ/'PLAN.json').read_text())
    put('DATA.json', cases);put('MENUS.json', menus);put('QUERIES.json', queries);put('LINKS.json', links)
    put('PLAN.json', {'seed':73103, 'routers':['original','adapted'], 'modes':['free','forced'],
        'actions':['YES','NO','WITHHOLD','FULL','TARGET','UNKNOWN'], 'max_output_tokens':8,
        'working_limit_bytes':5153960755, 'max_prompt_tokens':256,
        'base_weights_sha256':prior['base_weights_sha256'], 'base_revision':prior['base_revision'],
        'worker_mapping':prior['mappings']['canonical'],
        'worker_template':'Map the status to its answer. {mapping}. Return only the answer.\n\n{source}',
        'worker_full_prefix':'Read only the record for the target plot.\n',
        'fixed_policies':['always_target','always_full','always_unknown','observed_rule'],
        'deduplication':'exact visible router prompts per model; exact worker prompt cache within this run',
        'no_training_or_output_based_retry':True})
    deps=[ACQ/'run/canonical'/n for n in ('MANIFEST.json','final/adapter.safetensors','final/manifest.json')]
    names=['DATA.json','MENUS.json','QUERIES.json','LINKS.json','PLAN.json','PROTOCOL.md','prepare.py',
           'run_choice.py','probe.py','routing.py','score.py','test_choice.py','evidence.py','runtime_reference.py','lora_cpu.py']
    put('FREEZE.json', {'sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps},
                       'timing':'before tokenizer/model load and all new forwards'})
    print('Frozen24scenarios,4menus,32unique visible prompts per router;no training')

if __name__=='__main__':
    main()
