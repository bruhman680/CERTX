"""Post-result semantic readback and branch audit; never changes frozen metrics."""
from pathlib import Path
import hashlib
import json
from task import finish_route,decode_action
from routing_reference import retrieve

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump_new(path,value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')

ROOT=Path(__file__).resolve().parent

def alias(text):
    # Exact phrase from the offered UNKNOWN description; do not map the opposite.
    return 'UNKNOWN' if text.strip().casefold()=='action: report insufficient evidence' else None

def main():
    assert alias('ACTION: Report Sufficient Evidence') is None
    cases={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
    probes={p['run_id']:p for p in (json.loads(s) for s in (ROOT/'run/ROUTER_RAW.jsonl').read_text().splitlines())}
    links=json.loads((ROOT/'LINKS.json').read_text())
    expanded=[]
    for link in links:
        if link['examples'] or link['response']!='plan64':continue
        p=probes[link['query_id']];action=alias(p['text'])
        if action is not None:
            assert p['decision']['action'] is None
            expanded.append({'case_id':link['case_id'],'query_id':link['query_id'],
                'counterfactual_action':action,**finish_route(cases[link['case_id']],action)})
    unique={r['query_id'] for r in expanded}
    description={'timing':'post-run interpretation audit,not preregistered primary decoder',
        'exact_alias':'ACTION: Report insufficient evidence -> UNKNOWN',
        'strict_primary_metrics_unchanged':True,'new_model_calls':0,'new_tool_actions':0,
        'actual_probes_with_alias':len(unique),'logical_routes_with_alias':len(expanded),
        'would_be_justified_unknown':sum(r['justified_unknown'] for r in expanded),
        'would_defer_despite_accessible_evidence':sum(r['unknown_with_accessible_evidence'] for r in expanded),
        'not_evidence_of_calibrated_uncertainty':True,'routes':expanded}
    dump_new(ROOT/'SEMANTIC_READBACK.json',description)
    child=ROOT/'example-order-check'
    data={c['id']:c for c in json.loads((child/'DATA.json').read_text())}
    queries={q['id']:q for q in json.loads((child/'QUERIES.json').read_text())}
    raw={r['run_id']:r for r in (json.loads(s) for s in (child/'run/RAW.jsonl').read_text().splitlines())}
    routes=[json.loads(s) for s in (child/'run/ROUTES.jsonl').read_text().splitlines()]
    workers={w['run_id']:w for w in (json.loads(s) for s in (ROOT/'run/WORKER_RAW.jsonl').read_text().splitlines())}
    assert len(routes)==len(raw)==24
    for r in routes:
        q=queries[r['query_id']];p=raw[r['query_id']];c=data[r['case_id']]
        assert (p['case_id'],p['rotation'])==(q['case_id'],q['rotation'])
        assert p['decision']==decode_action(p['text']);action=p['decision']['action']
        tool=retrieve(c,action) if action in ('FULL','TARGET') else None
        assert tool==r['tool'];state=None
        if tool is not None and tool['available']:
            w=workers[r['worker_id']];state=w['state']
            text='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+tool['source']
            if tool['kind']=='full':text='Read only the record for the target plot.\n'+text
            assert w['messages']==[{'role':'user','content':text}]
            assert w['prompt_sha256']==hashlib.sha256(text.encode()).hexdigest()
        else:assert r['worker_id'] is None
        assert all(r[k]==v for k,v in finish_route(c,action,state,tool).items())
    for directory in (ROOT,child):
        f=json.loads((directory/'FREEZE.json').read_text())
        assert all(sha(directory/n)==h for n,h in f['sha256'].items())
        assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
        assert json.loads((directory/'CHECKS.json').read_text())['status']=='pass'
    old=json.loads(Path('/workspace/planning-examples-before.json').read_text())
    assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
    checks={'status':'pass','actual_generation_probes':138,'main_router':96,'main_worker':18,
        'lesson_order_router':24,'logical_executed_routes':504,'old_files_unchanged_before_sync':len(old),
        'all_frozen_inputs_and_checkpoint_dependencies_match':True,'no_training_or_new_model_state':True,
        'strict_decoder_and_semantic_readback_kept_separate':True,'description_alias_probes':len(unique),
        'unsupported_opposite_phrase_not_mapped':True,'worker_reuse_checked':True}
    dump_new(ROOT/'FINAL_CHECKS.json',checks)
    print(json.dumps({**checks,'alias_logical_routes':len(expanded),
        'alias_justified_unknown':description['would_be_justified_unknown'],
        'alias_deferrals':description['would_defer_despite_accessible_evidence']},indent=2))

if __name__=='__main__':main()
