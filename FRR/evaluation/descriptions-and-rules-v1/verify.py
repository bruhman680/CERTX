"""Audit prospective decoder definitions, raw replies, actual routes and reuse."""
from pathlib import Path
from collections import Counter
import hashlib
import json
from io_utils import sha,dump_new

ROOT=Path(__file__).resolve().parent

def main():
    from transformers import AutoTokenizer
    from decoder import decode_v1,decode_v2,fixtures
    from domain import render,finish_route,observed_rule
    from routing_reference import retrieve
    from evidence import parse
    from study import summarize
    f=json.loads((ROOT/'FREEZE.json').read_text())
    assert all(sha(ROOT/n)==h for n,h in f['sha256'].items())
    assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
    fixture_data=json.loads((ROOT/'DECODER_FIXTURES.json').read_text())
    assert fixture_data==fixtures() and len(fixture_data)==43
    assert all(decode_v2(c['text'])['action']==c['expected'] for c in fixture_data)
    old=[json.loads(s) for s in (ROOT.parent/'planning-and-examples-v1/run/ROUTER_RAW.jsonl').read_text().splitlines()]
    assert len(old)==96 and all(decode_v1(p['text'])==p['decision']['action'] for p in old)
    hist=json.loads((ROOT/'HISTORICAL_DECODER_REPLAY.json').read_text())
    assert hist['strict_recognized']==sum(decode_v1(p['text']) is not None for p in old)
    assert hist['v2_recognized']==sum(decode_v2(p['text'])['action'] is not None for p in old)
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    queries={q['id']:q for q in json.loads((ROOT/'QUERIES.json').read_text())}
    links=json.loads((ROOT/'LINKS.json').read_text())
    assert len(cases)==24 and len(queries)==80 and len(links)==240
    assert Counter(c['state'] for c in cases.values())==Counter(dict.fromkeys(('positive','zero','missing'),8))
    for c in cases.values():assert parse(c['source'])['state']==c['state']
    for link in links:assert queries[link['query_id']]['prompt']==render(cases[link['case_id']],link['guidance'],link['rotation'])
    probes=[json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines()]
    workers=[json.loads(s) for s in (ROOT/'run/WORKER_RAW.jsonl').read_text().splitlines()]
    routes=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
    assert len(probes)==80 and len(workers)==9 and len(routes)==576
    byprobe={p['run_id']:p for p in probes};byworker={w['run_id']:w for w in workers}
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    for p in probes+workers:
        assert p['input_token_ids']==tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)
        assert p['text']==tok.decode(p['generated_token_ids'],skip_special_tokens=True)
        assert 1<=len(p['generated_token_ids'])<=p['cap']
        if p['stop']=='eos':assert p['generated_token_ids'][-1]==tok.eos_token_id
    for p in probes:
        q=queries[p['run_id']]
        assert p['messages']==[{'role':'user','content':q['prompt']}]
        assert (p['guidance'],p['rotation'])==(q['guidance'],q['rotation'])
        assert p['strict_v1']==decode_v1(p['text']) and p['declared_v2']==decode_v2(p['text'])
    assert {(r['case_id'],r['query_id'],r['decoder']) for r in routes if r['query_id'] is not None}=={
        (x['case_id'],x['query_id'],d) for x in links for d in ('strict_v1','declared_v2')}
    seen=set()
    for r in routes:
        c=cases[r['case_id']]
        if r['query_id'] is not None:
            p=byprobe[r['query_id']]
            action=p['strict_v1'] if r['decoder']=='strict_v1' else p['declared_v2']['action']
        else:
            action={'always_target':'TARGET','always_full':'FULL','always_unknown':'UNKNOWN'}.get(r['policy'])
            if r['policy']=='observed_rule':action=observed_rule(c)
        assert action==r['action']
        tool=retrieve(c,action) if action in ('FULL','TARGET') else None
        assert tool==r['tool'];state=None
        if tool is not None and tool['available']:
            w=byworker[r['worker_id']]
            text='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+tool['source']
            if tool['kind']=='full':text='Read only the record for the target plot.\n'+text
            key=hashlib.sha256(text.encode()).hexdigest()
            assert w['messages']==[{'role':'user','content':text}] and w['prompt_sha256']==key
            assert r['worker_cache_hit']==(key in seen);seen.add(key)
            state={'YES':'positive','NO':'zero','WITHHOLD':'missing'}.get(w['text'].strip())
            assert w['state']==state
        else:assert r['worker_id'] is None and not r['worker_cache_hit']
        assert all(r[k]==v for k,v in finish_route(c,action,state,tool).items())
    assert len(seen)==9
    assert summarize(routes,probes)==json.loads((ROOT/'run/SUMMARY.json').read_text())
    prior=json.loads(Path('/workspace/descriptions-rules-before.json').read_text())
    assert all(sha(Path('/workspace/frr')/n)==h for n,h in prior.items())
    resources=[json.loads(s) for s in (ROOT/'run/RESOURCE.jsonl').read_text().splitlines()]
    negatives=[x for x in fixture_data if x['expected'] is None]
    checks={'status':'pass','actual_router_probes_audited':80,'actual_worker_probes_audited':9,'logical_routes_audited':576,
        'decoder_fixture_expectations':43,'negative_or_unsupported_fixtures':len(negatives),
        'old_v1_negative_fixture_accepts':sum(decode_v1(x['text']) is not None for x in negatives),
        'v2_negative_fixture_accepts':sum(decode_v2(x['text'])['action'] is not None for x in negatives),
        'old_local_files_unchanged_before_sync':len(prior),'frozen_inputs_checkpoints_transcripts_routes_cache_match':True,
        'historical_strict_decoder_reproduced':True,'fresh_v1_v2_action_differences':sum(p['strict_v1']!=p['declared_v2']['action'] for p in probes),
        'router_input_tokens':sum(len(p['input_token_ids']) for p in probes),'router_output_tokens':sum(len(p['generated_token_ids']) for p in probes),
        'worker_input_tokens':sum(len(p['input_token_ids']) for p in workers),'worker_output_tokens':sum(len(p['generated_token_ids']) for p in workers),
        'generation_seconds':sum(p['seconds'] for p in probes+workers),
        'unique_prompt_strings':len({p['messages'][0]['content'] for p in probes+workers}),
        'max_sampled_working_bytes':max(p['working_estimate'] for p in resources),'max_sampled_rss_bytes':max(p['process_rss'] for p in resources),
        'no_training_or_independent_empirical_replication':True}
    dump_new(ROOT/'CHECKS.json',checks)
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
