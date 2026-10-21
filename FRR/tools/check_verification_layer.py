"""Prepare and check authored verification instruments; not an agent efficacy trial."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
from verification_layer import evaluate,append_receipt,validate_ledger,digest,canonical

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/verification-layer-v1'


def prepare():
    if (OUT/'FIXTURES.json').exists():raise ValueError('Refusing to overwrite fixture preparation')
    fixtures=[];keys={};art=OUT/'artifacts';art.mkdir(parents=True,exist_ok=True)
    def add(name,payload,verdict,adapter='arithmetic_equal',modify=None,scope='literal-case-A'):
        path=art/(name+'.json');path.write_text(json.dumps(payload,sort_keys=True)+'\n')
        c=dict(claim_id=name,contract_id=name+'-contract-1',scope=scope,adapter=adapter,
               criterion_id='rational-equality-v1' if adapter=='arithmetic_equal' else 'true-state-band-v1',
               artifact=dict(path=str(path.relative_to(OUT)),sha256=digest(path.read_bytes())))
        if adapter=='arithmetic_equal':c['expected_value']='20'
        else:c.update(target='1',tolerance='1/20')
        if modify:modify(c)
        fixtures.append(c);keys[name]={'0.2':verdict,'0.1':('unresolved' if adapter=='bounded_sensor' else verdict)}
    good={'scope':'literal-case-A','expression':'(2+3)*4'}
    add('literal_correct',good,'supported')
    add('literal_incorrect',good,'contradicted',modify=lambda c:c.update(expected_value='19'))
    add('exact_fraction',{'scope':'literal-case-A','expression':'1/10+2/10'},'supported',modify=lambda c:c.update(expected_value='3/10'))
    add('missing_evidence',good,'unresolved',modify=lambda c:c['artifact'].update(path='absent.json'))
    add('changed_bytes',good,'unresolved',modify=lambda c:c['artifact'].update(sha256='0'*64))
    add('scope_expansion',good,'unresolved',modify=lambda c:c.update(scope='all-cases'))
    add('unsupported_semantic_claim',good,'unresolved',modify=lambda c:c.update(adapter='empirical_truth'))
    add('criterion_changed',good,'unresolved',modify=lambda c:c.update(criterion_id='close-enough-v2'))
    add('undefined_arithmetic',{'scope':'literal-case-A','expression':'1/0'},'unresolved')
    add('forbidden_expression',{'scope':'literal-case-A','expression':'__import__("os")'},'unresolved')
    add('missing_expression',{'scope':'literal-case-A'},'unresolved')
    add('invalid_expected_value',good,'unresolved',modify=lambda c:c.update(expected_value=True))
    add('unimplemented_float_semantics',{'scope':'literal-case-A','expression':'0.1+0.2'},'unresolved')
    add('path_escape',good,'unresolved',modify=lambda c:c['artifact'].update(path='../outside.json'))
    def sensor(name,payload,verdict):add(name,{'scope':'sensor-bench-A',**payload},verdict,adapter='bounded_sensor',scope='sensor-bench-A')
    sensor('bounded_sensor_good',{'measured':'1','bias_bounds':['0','0']},'supported')
    sensor('bounded_sensor_bad',{'measured':'1','bias_bounds':['2/5','2/5']},'contradicted')
    sensor('sensor_unknown_bias',{'measured':'1'},'unresolved')
    sensor('sensor_ambiguous_band',{'measured':'1','bias_bounds':['0','1/10']},'unresolved')
    sensor('sensor_boundary_inclusive',{'measured':'1','bias_bounds':['-1/20','1/20']},'supported')
    sensor('sensor_inconsistent_bounds',{'measured':'1','bias_bounds':['1','0']},'unresolved')
    sensor('sensor_outside_above',{'measured':'6/5','bias_bounds':['0','0']},'contradicted')
    sensor('sensor_invalid_number',{'measured':'not-a-number','bias_bounds':['0','0']},'unresolved')
    (OUT/'FIXTURES.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    (OUT/'KEYS.json').write_text(json.dumps(keys,indent=2)+'\n')
    paths=[ROOT/'tools/verification_layer.py',ROOT/'tools/check_verification_layer.py',OUT/'PROTOCOL.md',OUT/'FIXTURES.json',OUT/'KEYS.json',*sorted(art.glob('*.json'))]
    (OUT/'LAUNCH_MANIFEST.json').write_text(json.dumps({'status':'Prepared before instrument execution; authored development fixtures, not held-out evidence','hashes':{str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in paths}},indent=2)+'\n')
    print(json.dumps({'fixtures':len(fixtures),'rulesets':2,'new_model_calls':0}))


def run():
    manifest=json.loads((OUT/'LAUNCH_MANIFEST.json').read_text())
    unchanged=all(digest((ROOT/p).read_bytes())==v for p,v in manifest['hashes'].items())
    if not unchanged:raise ValueError('Prepared artifact changed')
    fixtures=json.loads((OUT/'FIXTURES.json').read_text());keys=json.loads((OUT/'KEYS.json').read_text());records=[]
    for version in ['0.1','0.2']:
        for c in fixtures:
            receipt=evaluate(c,OUT,version);expected=keys[c['claim_id']][version]
            records.append({'claim_id':c['claim_id'],'expected':expected,'receipt':receipt,'matched':receipt['verdict']==expected})
    (OUT/'RECEIPTS.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in records))
    old=[x for x in records if x['receipt']['ruleset']=='0.1' and next(c['adapter'] for c in fixtures if c['claim_id']==x['claim_id'])!='bounded_sensor']
    regression=all(x['receipt']['verdict']==next(y['receipt']['verdict'] for y in records if y['receipt']['ruleset']=='0.2' and y['claim_id']==x['claim_id']) for x in old)
    summaries={}
    for name in ['unresolved_only','integrity_only','0.1','0.2']:
        outputs=[]
        for c in fixtures:
            target=keys[c['claim_id']]['0.2'];receipt=next(x['receipt'] for x in records if x['claim_id']==c['claim_id'] and x['receipt']['ruleset']=='0.2')
            predicted='unresolved' if name=='unresolved_only' else ('supported' if receipt['checks'].get('integrity')=='pass' else 'unresolved') if name=='integrity_only' else next(x['receipt']['verdict'] for x in records if x['claim_id']==c['claim_id'] and x['receipt']['ruleset']==name)
            outputs.append((predicted,target))
        summaries[name]={'matches_final_contract_key':sum(a==b for a,b in outputs),'unwarranted_support':sum(a=='supported' and b!='supported' for a,b in outputs),'withheld_supported':sum(a=='unresolved' and b=='supported' for a,b in outputs),'contradictions_identified':sum(a=='contradicted' and b=='contradicted' for a,b in outputs),'total':len(outputs)}
    ledger=OUT/'DEVELOPMENT_LEDGER.jsonl'
    if ledger.exists():raise ValueError('Refusing to overwrite existing ledger')
    name='bounded_sensor_good'
    r1=next(x['receipt'] for x in records if x['claim_id']==name and x['receipt']['ruleset']=='0.1')
    r2=next(x['receipt'] for x in records if x['claim_id']==name and x['receipt']['ruleset']=='0.2')
    e1=append_receipt(ledger,r1);prefix=ledger.read_bytes()
    append_receipt(ledger,r2,supersedes=e1['event_sha256'],revision_note='Adapter extension assesses supplied bias bounds; previous unresolved assessment retained.')
    prefix_preserved=ledger.read_bytes().startswith(prefix)
    events=[json.loads(x) for x in ledger.read_text().splitlines()];validate_ledger(events)
    changed=deepcopy(events);changed[0]['receipt']['verdict']='supported'
    try:validate_ledger(changed)
    except ValueError:tamper_detected=True
    else:tamper_detected=False
    # Both the chain and its hashes can be rewritten by a sufficiently privileged writer.
    rewritten=deepcopy(changed);previous=None
    for e in rewritten:
        e['previous_event_sha256']=previous
        body={k:v for k,v in e.items() if k!='event_sha256'};e['event_sha256']=digest(canonical(body));previous=e['event_sha256']
    whole_chain_rewrite_passes=bool(validate_ledger(rewritten))
    with tempfile.TemporaryDirectory() as tmp:
        try:append_receipt(Path(tmp)/'bad.jsonl',r2,supersedes='absent',revision_note='invalid revision')
        except ValueError:invalid_revision_rejected=True
        else:invalid_revision_rejected=False
    result=dict(scope='Authored instrument/contract checks and ruleset extension replay; not agent efficacy, independently held-out confirmation or empirical sensor calibration',fixture_count=len(fixtures),evaluations=len(records),new_model_calls=0,all_expected_verdicts_matched=all(x['matched'] for x in records),prior_adapter_verdict_regression_free=regression,prior_adapter_cases=len(old),summary=summaries,ledger_checks=dict(prefix_preserved=prefix_preserved,modified_event_detected=tamper_detected,invalid_revision_rejected=invalid_revision_rejected,whole_chain_rewrite_still_passes_local_hash_check=whole_chain_rewrite_passes),launch_hashes_unchanged=unchanged)
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert result['all_expected_verdicts_matched'] and regression and prefix_preserved and tamper_detected and invalid_revision_rejected and whole_chain_rewrite_passes


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['prepare','run']);args=p.parse_args();prepare() if args.mode=='prepare' else run()
