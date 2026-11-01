"""Audit matched response budgets, examples, source normalization and executed routes."""
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parent

def main():
    from transformers import AutoTokenizer
    from runtime_reference import sha,dump_new
    from task import render,decode_action,normalized_visible,observed_rule,finish_route,example_text
    from routing_reference import retrieve
    from evidence import parse
    from score import summarize
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in freeze['sha256'].items())
    assert all(sha(Path(n))==h for n,h in freeze['dependencies'].items())
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    queries={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())}
    links=json.loads((ROOT/'LINKS.json').read_text())
    assert len(cases)==48 and len(queries)==96 and len(links)==288
    assert all(name not in example_text() for name in ('Juniper','Hemlock'))
    assert Counter(c['state'] for c in cases.values())==Counter(dict.fromkeys(('positive','zero','missing'),16))
    for c in cases.values():
        p=parse(c['source']);assert p['state']==c['state'] and p['target']==c['target']
        visible=normalized_visible(c)
        if visible is not None:assert visible in (p['crop'],p['other_crop'])
    for link in links:
        c=cases[link['case_id']];q=queries[link['query_id']]
        assert q['prompt']==render(c,link['examples'],link['response'])
        assert q['cap']==(8 if link['response']=='direct8' else 64)
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    probes=[json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    workers=[json.loads(s) for s in (ROOT/'run/WORKER_RAW.jsonl').read_text().splitlines()]
    routes=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
    assert len(probes)==96 and len(workers)==18 and len(routes)==480
    byprobe={p['run_id']:p for p in probes};byworker={w['run_id']:w for w in workers}
    assert len(byprobe)==96 and len(byworker)==18
    for p in probes+workers:
        assert p['input_token_ids']==tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)
        assert p['text']==tok.decode(p['generated_token_ids'],skip_special_tokens=True)
        assert 1<=len(p['generated_token_ids'])<=p['cap']
        if p['stop']=='eos':assert p['generated_token_ids'][-1]==tok.eos_token_id
    for p in probes:
        q=queries[p['run_id']]
        assert p['messages']==[{'role':'user','content':q['prompt']}]
        assert (p['examples'],p['response'],p['cap'])==(q['examples'],q['response'],q['cap'])
        assert p['decision']==decode_action(p['text'])
    prefix_pairs=[]
    for q in queries.values():
        if q['response']!='direct8':continue
        long=next(x for x in queries.values() if x['response']=='direct64' and x['prompt']==q['prompt'])
        a,b=byprobe[q['id']],byprobe[long['id']]
        prefix_pairs.append(a['generated_token_ids']==b['generated_token_ids'][:len(a['generated_token_ids'])])
    assert len(prefix_pairs)==32 and all(prefix_pairs)
    seen_worker=set()
    for route in routes:
        c=cases[route['case_id']]
        if route['query_id'] is not None:
            p=byprobe[route['query_id']];action=p['decision']['action']
            assert (route['examples'],route['response'])==(p['examples'],p['response'])
        else:
            action={'always_target':'TARGET','always_full':'FULL','always_unknown':'UNKNOWN'}.get(route['policy'])
            if route['policy']=='observed_rule':action=observed_rule(c)
        assert route['action']==action
        tool=retrieve(c,action) if action in ('FULL','TARGET') else None
        assert tool==route['tool']
        state=None
        if tool is not None and tool['available']:
            text='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+tool['source']
            if tool['kind']=='full':text='Read only the record for the target plot.\n'+text
            key=hashlib.sha256(text.encode()).hexdigest();w=byworker[route['worker_id']]
            assert w['messages']==[{'role':'user','content':text}] and w['prompt_sha256']==key
            assert route['worker_cache_hit']==(key in seen_worker);seen_worker.add(key)
            assert w['state']=={'YES':'positive','NO':'zero','WITHHOLD':'missing'}.get(w['text'].strip())
            state=w['state']
        else:assert route['worker_id'] is None and not route['worker_cache_hit']
        assert all(route[k]==v for k,v in finish_route(c,action,state,tool).items())
    assert len(seen_worker)==18
    summary=summarize(routes,probes)
    assert summary==json.loads((ROOT/'run/SUMMARY.json').read_text())
    head=json.loads((ROOT/'run/LOGIT_HEAD_CHECK.json').read_text())
    assert len(head['calibration'])==6 and all(c['same_argmax'] and c['max_abs_delta']<=1e-4 for c in head['calibration'])
    old=json.loads(Path('/workspace/planning-examples-before.json').read_text())
    assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
    resources=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
    # Explicit-tag suffix lengths expose format costs; they are not added to prompts.
    tag_lengths={a:len(tok.encode('ACTION: '+a,add_special_tokens=False))+1 for a in ('YES','NO','WITHHOLD','FULL','TARGET','UNKNOWN')}
    checks={'status':'pass','router_generations_audited':96,'worker_generations_audited':18,'logical_routes_audited':480,
        'old_files_unchanged_before_sync':len(old),'all_input_and_checkpoint_hashes_match':True,
        'prompt_token_decode_action_tool_cache_receipt_checks':True,'hidden_keys_not_in_router_prompts':True,
        'same_prompt_short_long_prefix_pairs':32,'same_prefix_matches':sum(prefix_pairs),
        'logit_head_calibration_contexts':6,'calibration_prefill_forwards':12,
        'tag_token_lengths_including_eos':tag_lengths,
        'router_input_tokens':sum(len(p['input_token_ids']) for p in probes),
        'router_output_tokens':sum(len(p['generated_token_ids']) for p in probes),
        'worker_input_tokens':sum(len(p['input_token_ids']) for p in workers),
        'worker_output_tokens':sum(len(p['generated_token_ids']) for p in workers),
        'generation_seconds_excluding_load_and_other_work':sum(p['seconds'] for p in probes+workers),
        'unique_prompt_strings':len({p['messages'][0]['content'] for p in probes+workers}),
        'max_sampled_working_bytes':max(p['working_estimate'] for p in resources),
        'max_sampled_rss_bytes':max(p['process_rss'] for p in resources),
        'no_training_or_independent_empirical_replication':True}
    dump_new(ROOT/'CHECKS.json',checks)
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
