"""Post-run audit of action probes, real tool traces, cache reuse and outcomes."""
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parent

def audit_probe(row,tok,choices):
    assert row['input_token_ids']==tok.apply_chat_template(row['messages'],tokenize=True,add_generation_prompt=True)
    assert row['text']==tok.decode(row['generated_token_ids'],skip_special_tokens=True)
    assert row['free_key']=={v:k for k,v in choices.items()}.get(row['text'].strip())
    assert set(row['scores'])==set(choices)
    for key,label in choices.items():
        score=row['scores'][key]
        assert score['label']==label
        assert score['ids']==tok.encode(label,add_special_tokens=False)+[tok.eos_token_id]
        assert score['sum']==sum(score['token_logprobs'])
        assert score['mean']==score['sum']/len(score['token_logprobs'])
        assert all(v<=0 for v in score['token_logprobs'])
    chosen=max(choices,key=lambda k:row['scores'][k]['sum'])
    assert row['forced_key']==chosen
    assert row['forced_tied']==(sum(s['sum']==row['scores'][chosen]['sum'] for s in row['scores'].values())>1)

def main():
    from transformers import AutoTokenizer
    from routing import router_prompt,observation,CODES,retrieve,simple_rule,terminal
    from evidence import parse
    from runtime_reference import sha,dump_new
    from score import summarize
    freeze=json.loads((ROOT/'FREEZE.json').read_text());plan=json.loads((ROOT/'PLAN.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    menus={m['id']:m for m in json.loads((ROOT/'MENUS.json').read_text())}
    queries={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())}
    links=json.loads((ROOT/'LINKS.json').read_text())
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    assert len(cases)==24 and len(queries)==32 and len(links)==96
    assert len({observation(c) for c in cases.values()})==8
    assert Counter(c['state'] for c in cases.values())==Counter(dict.fromkeys(('positive','zero','missing'),8))
    for c in cases.values():
        assert parse(c['source'])['state']==c['state']
    for link in links:
        assert queries[link['query_id']]['prompt']==router_prompt(cases[link['case_id']],menus[link['menu_id']])
    probes=[json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    workers=[json.loads(s) for s in (ROOT/'run/WORKER_RAW.jsonl').read_text().splitlines()]
    routes=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
    assert len(probes)==64 and len(workers)==9 and len(routes)==480
    assert {(p['router'],p['query_id']) for p in probes}=={(r,q) for r in plan['routers'] for q in queries}
    byprobe={p['probe_id']:p for p in probes};byworker={p['probe_id']:p for p in workers}
    for p in probes:
        assert p['messages']==[{'role':'user','content':queries[p['query_id']]['prompt']}]
        audit_probe(p,tok,dict(zip(CODES,CODES)))
    for w in workers:audit_probe(w,tok,plan['worker_mapping'])
    seen_worker=set()
    for route in routes:
        c=cases[route['case_id']]
        assert route['kind']==c['kind']
        if route['router'] is not None:
            p=byprobe[route['router_probe_id']];menu=menus[route['menu_id']]
            assert p['router']==route['router'] and p['menu_id']==route['menu_id']
            code=p['free_key'] if route['mode']=='free' else p['forced_key']
            assert route['chosen_code']==code
            action=menu['mapping'].get(code)
        else:
            action={'always_target':'TARGET','always_full':'FULL','always_unknown':'UNKNOWN'}.get(route['policy'])
            if route['policy']=='observed_rule':action=simple_rule(c)
        assert action==route['action']
        tool=retrieve(c,action) if action in ('FULL','TARGET') else None
        assert tool==route['tool']
        worker_state=None
        if tool is not None and tool['available']:
            w=byworker[route['worker_probe_id']]
            mapping='; '.join(f'{s}={v}' for s,v in plan['worker_mapping'].items())
            text=plan['worker_template'].format(mapping=mapping,source=tool['source'])
            if tool['kind']=='full':text=plan['worker_full_prefix']+text
            assert w['messages']==[{'role':'user','content':text}]
            key=hashlib.sha256(text.encode()).hexdigest()
            assert w['worker_prompt_sha256']==key
            assert route['worker_cache_hit']==(key in seen_worker)
            seen_worker.add(key);worker_state=w['free_key']
        else:
            assert route['worker_probe_id'] is None and not route['worker_cache_hit']
        expected=terminal(c,action,worker_state,tool)
        assert all(route[k]==v for k,v in expected.items())
        if route['end'] in ('UNKNOWN_POLICY','UNKNOWN_TOOL'):
            assert route['receipt']['label_consistency']=='NOT_AN_ANSWER'
    assert len(seen_worker)==9
    assert summarize(routes,probes)==json.loads((ROOT/'run/SUMMARY.json').read_text())
    earlier=json.loads(Path('/workspace/reader-choice-before.json').read_text())
    assert all(sha(Path('/workspace/frr')/n)==h for n,h in earlier.items())
    resources=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
    receipt={'status':'pass','router_probes_audited':64,'worker_probes_audited':9,'logical_routes_audited':480,
        'old_local_files_unchanged_before_sync':len(earlier),'hidden_source_keys_not_in_router_prompts':True,
        'frozen_inputs_and_checkpoint_dependencies_match':True,'action_tool_cache_receipt_checks':True,
        'unique_visible_observations':8,'free_invalid_actions_not_coerced':True,
        'router_input_tokens':sum(len(p['input_token_ids']) for p in probes),
        'router_output_tokens':sum(len(p['generated_token_ids']) for p in probes),
        'worker_input_tokens':sum(len(p['input_token_ids']) for p in workers),
        'worker_output_tokens':sum(len(p['generated_token_ids']) for p in workers),
        'actual_probe_seconds':sum(p['seconds'] for p in probes+workers),
        'max_input_tokens':max(len(p['input_token_ids']) for p in probes+workers),
        'max_sampled_working_bytes':max(p['working_estimate'] for p in resources),
        'max_sampled_rss_bytes':max(p['process_rss'] for p in resources),
        'no_independent_replication_or_general_policy_claim':True}
    dump_new(ROOT/'CHECKS.json',receipt);print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
