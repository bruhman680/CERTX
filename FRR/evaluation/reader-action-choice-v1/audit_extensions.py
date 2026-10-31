"""Audit outcome-informed interfaces; derive clearly separate policy diagnostics."""
from pathlib import Path
from collections import Counter
import hashlib
import importlib.util
import json

ROOT=Path(__file__).resolve().parent

def main():
    from transformers import AutoTokenizer
    from runtime_reference import sha,dump_new
    from routing import ACTIONS,terminal,retrieve,router_prompt
    from verify import audit_probe
    from score import metrics
    spec=importlib.util.spec_from_file_location('plain_control',ROOT/'plain-actions/plain.py')
    plain=importlib.util.module_from_spec(spec);spec.loader.exec_module(plain)
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    plan=json.loads((ROOT/'PLAN.json').read_text());cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    for sub in ('plain-actions','action-emission'):
        directory=ROOT/sub;freeze=json.loads((directory/'FREEZE.json').read_text())
        assert all(sha(directory/n)==h for n,h in freeze['sha256'].items())
        assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
        assert json.loads((directory/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
    queries={q['id']:q for q in json.loads((ROOT/'plain-actions/QUERIES.json').read_text())}
    links=json.loads((ROOT/'plain-actions/LINKS.json').read_text())
    for link in links:assert queries[link['query_id']]['prompt']==plain.plain_prompt(cases[link['case_id']],link['order'])
    probes=[json.loads(s) for s in (ROOT/'plain-actions/run/RAW.jsonl').read_text().splitlines()]
    byprobe={p['probe_id']:p for p in probes}
    assert len(probes)==len(byprobe)==32
    for p in probes:
        audit_probe(p,tok,dict(zip(ACTIONS,ACTIONS)))
        assert p['messages']==[{'role':'user','content':queries[p['query_id']]['prompt']}]
        assert p['parsed_action']==plain.first_action(p['text'])
    workers={w['probe_id']:w for w in (json.loads(s) for s in (ROOT/'run/WORKER_RAW.jsonl').read_text().splitlines())}
    routes=[json.loads(s) for s in (ROOT/'plain-actions/run/ROUTES.jsonl').read_text().splitlines()]
    assert len(routes)==192
    assert {(r['case_id'],r['order'],r['router'],r['mode']) for r in routes}=={(c,o,m,d) for c in cases for o in ('forward','reverse') for m in plan['routers'] for d in ('free','forced')}
    for r in routes:
        c=cases[r['case_id']];p=byprobe[r['probe_id']]
        action=p['parsed_action'] if r['mode']=='free' else p['forced_key']
        assert r['action']==action and r['order']==p['order'] and r['router']==p['router']
        tool=retrieve(c,action) if action in ('FULL','TARGET') else None
        assert r['tool']==tool
        state=None
        if tool is not None and tool['available']:
            w=workers[r['worker_probe_id']]
            mapping='; '.join(f'{s}={v}' for s,v in plan['worker_mapping'].items())
            text=plan['worker_template'].format(mapping=mapping,source=tool['source'])
            if tool['kind']=='full':text=plan['worker_full_prefix']+text
            assert w['messages']==[{'role':'user','content':text}]
            assert hashlib.sha256(text.encode()).hexdigest()==w['worker_prompt_sha256']
            assert r['worker_reused_from_coded_contact'];state=w['free_key']
        else:assert r['worker_probe_id'] is None and not r['worker_reused_from_coded_contact']
        assert all(r[k]==v for k,v in terminal(c,action,state,tool).items())
    summary=json.loads((ROOT/'plain-actions/run/SUMMARY.json').read_text())
    for policy,data in summary['policies'].items():
        rs=[r for r in routes if r['policy']==policy]
        assert metrics(rs)==data['total']
        for order in ('forward','reverse'):assert metrics([r for r in rs if r['order']==order])==data['by_order'][order]
    echo_cases={c['id']:c for c in json.loads((ROOT/'action-emission/DATA.json').read_text())}
    echoes=[json.loads(s) for s in (ROOT/'action-emission/run/RAW.jsonl').read_text().splitlines()]
    assert len(echoes)==24 and {(p['router'],p['case_id']) for p in echoes}=={(r,c) for r in plan['routers'] for c in echo_cases}
    for p in echoes:
        c=echo_cases[p['case_id']];audit_probe(p,tok,dict(zip(ACTIONS,ACTIONS)))
        assert p['messages']==[{'role':'user','content':c['prompt']}]
        assert p['expected']==c['expected'] and p['parsed_action']==plain.first_action(p['text'])
        assert p['exact_correct']==(p['text'].strip()==p['expected'])
        assert p['prefix_correct']==(p['parsed_action']==p['expected'])
        assert p['forced_correct']==(p['forced_key']==p['expected'])
    es=json.loads((ROOT/'action-emission/run/SUMMARY.json').read_text())
    for model,data in es.items():
        rs=[p for p in echoes if p['router']==model]
        assert data['n']==12
        for key in ('exact_correct','prefix_correct','forced_correct'):assert data[key]==sum(p[key] for p in rs)
        for action,counts in data['by_action'].items():
            group=[p for p in rs if p['expected']==action];assert len(group)==counts['n']==2
            assert counts['exact_correct']==sum(p['exact_correct'] for p in group)
            assert counts['prefix_correct']==sum(p['prefix_correct'] for p in group)
    # Exploratory post-run conditional check: four coded/two plain menu packages,
    # not independent observations of six hidden states sharing the same prompt.
    coded_links=json.loads((ROOT/'LINKS.json').read_text())
    coded_probes={(p['router'],p['query_id']):p for p in (json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines())}
    menus={m['id']:m for m in json.loads((ROOT/'MENUS.json').read_text())}
    plainprobes={(p['router'],p['query_id']):p for p in probes}
    one_yes=next(c for c in cases.values() if c['kind']=='none_available')
    one_no=next(c for c in cases.values() if c['kind']=='none_unavailable')
    diagnostics=[]
    for model in plan['routers']:
        for mode in ('free','forced'):
            for menu_id,menu in menus.items():
                pair=[]
                for c in (one_yes,one_no):
                    link=next(x for x in coded_links if x['case_id']==c['id'] and x['menu_id']==menu_id)
                    p=coded_probes[model,link['query_id']]
                    code=p['free_key'] if mode=='free' else p['forced_key'];pair.append(menu['mapping'].get(code))
                diagnostics.append({'interface':'coded','router':model,'mode':mode,'layout':menu_id,
                    'available_action':pair[0],'unavailable_action':pair[1],
                    'request_then_unknown':pair[0] in ('FULL','TARGET') and pair[1]=='UNKNOWN'})
            for order in ('forward','reverse'):
                pair=[]
                for c in (one_yes,one_no):
                    link=next(x for x in links if x['case_id']==c['id'] and x['order']==order)
                    p=plainprobes[model,link['query_id']]
                    pair.append(p['parsed_action'] if mode=='free' else p['forced_key'])
                diagnostics.append({'interface':'plain','router':model,'mode':mode,'layout':order,
                    'available_action':pair[0],'unavailable_action':pair[1],
                    'request_then_unknown':pair[0] in ('FULL','TARGET') and pair[1]=='UNKNOWN'})
    dump_new(ROOT/'AVAILABILITY_DIAGNOSTIC.json',{'timing':'post-run exploratory diagnostic','unit':'one visible prompt pair per menu/model/mode; repeated hidden worlds not independent','pairs':diagnostics})
    old=json.loads(Path('/workspace/reader-choice-before.json').read_text())
    assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
    for sub,rs in [('plain-actions',probes),('action-emission',echoes)]:
        resource=[json.loads(s) for s in (ROOT/sub/'run/RESOURCE.jsonl').read_text().splitlines()]
        checks={'status':'pass','actual_generations_audited':len(rs),'prior_checkpoint_source_dependencies_unchanged':True,
            'prompt_token_decode_choice_metric_checks':True,'old_files_unchanged_before_sync':len(old),
            'input_tokens':sum(len(p['input_token_ids']) for p in rs),'output_tokens':sum(len(p['generated_token_ids']) for p in rs),
            'probe_seconds':sum(p['seconds'] for p in rs),
            'max_sampled_working_bytes':max(p['working_estimate'] for p in resource),
            'max_sampled_rss_bytes':max(p['process_rss'] for p in resource),
            'no_independent_replication':True}
        dump_new(ROOT/sub/'CHECKS.json',checks)
    dump_new(ROOT/'FINAL_CHECKS.json',{'status':'pass','coded_actual_probes':73,'plain_actual_probes':32,'emission_actual_probes':24,
        'total_actual_generations':129,'logical_routes':672,'teacher_forced_candidate_sequences':747,
        'old_files_unchanged_before_sync':len(old),'no_new_model_binary_or_training':True,
        'counterfactual_worker_reuse_explicit':True,'all_three_freezes_and_metrics_match':True})
    print(json.dumps({'status':'pass','actual_generations':129,'logical_routes':672,
        'availability_request_then_unknown':{i+'__'+m+'__'+mode:sum(d['request_then_unknown'] for d in diagnostics if (d['interface'],d['router'],d['mode'])==(i,m,mode)) for i in ('coded','plain') for m in plan['routers'] for mode in ('free','forced')}},indent=2))

if __name__=='__main__':main()
