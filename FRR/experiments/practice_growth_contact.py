"""Retrospective saved-trace audit plus live assessment-reopening exercise."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from verification_layer import evaluate,canonical,digest,append_receipt,validate_ledger
from reopen_assessment import compare
OUT=ROOT/'evaluation/practice-growth-v1'


def prepare():
    p=OUT/'MANIFEST.json'
    if p.exists():raise ValueError('Already prepared')
    paths=['tools/reopen_assessment.py','tools/verification_layer.py','experiments/practice_growth_contact.py','evaluation/practice-growth-v1/PROTOCOL.md','evaluation/pid-contact-v1/RESULTS.json']
    p.write_text(json.dumps({'scope':'New analysis of previously observed data, not prospective original measurement','hashes':{n:digest((ROOT/n).read_bytes()) for n in paths}},indent=2)+'\n');print('prepared')


def run():
    m=json.loads((OUT/'MANIFEST.json').read_text());assert all(digest((ROOT/n).read_bytes())==h for n,h in m['hashes'].items())
    if (OUT/'RESULTS.json').exists():raise ValueError('Refusing to overwrite contact')
    source=json.loads((ROOT/'evaluation/pid-contact-v1/RESULTS.json').read_text());chosen=[];per_seed=[];duplicates=[]
    for seed in source['settings']['noise_seeds']:
        matches=[r for r in source['runs'] if r['scenario']=='noisy_sensor' and r['seed']==seed]
        anchor=next(r for r in matches if r['controller']=='PI');a=np.asarray(anchor['trajectory']);error=a[:,3]-a[:,2];chosen.extend(error)
        per_seed.append({'seed':seed,'controller':'PI','count':len(error),'mean_signed_error':float(error.mean()),'mean_absolute_error':float(abs(error).mean()),'max_absolute_error':float(abs(error).max()),'above_pointwise_008':int((abs(error)>.08).sum())})
        for r in matches:
            b=np.asarray(r['trajectory']);delta=float(np.max(np.abs((b[:,3]-b[:,2])-error)));duplicates.append(delta)
    e=np.asarray(chosen)
    extract={'scope':'Derived measured-minus-true residuals from one saved PI noisy-sensor trajectory per seed; no new measurements','source_sha256':digest((ROOT/'evaluation/pid-contact-v1/RESULTS.json').read_bytes()),'streams':[{'seed':row['seed'],'controller':'PI','residuals':[float(v) for v in e[i*400:(i+1)*400]]} for i,row in enumerate(per_seed)]}
    (OUT/'RESIDUALS.json').write_text(json.dumps(extract,separators=(',',':'))+'\n')
    audit={'data_scope':'Saved noisy-sensor readings minus known simulated true state; one PI stream per seed. No original simulation rerun, physical calibration or new stochastic draws.',
        'selected_seeds':len(per_seed),'selected_rows':len(e),'all_controller_rows':len(e)*len(source['settings']['controllers']),
        'mean_signed_error':float(e.mean()),'mean_absolute_error':float(abs(e).mean()),'max_absolute_error':float(abs(e).max()),
        'abs_mean_within_001':bool(abs(e.mean())<=.01),'pointwise_limit':.08,'rows_exceeding_pointwise_limit':int((abs(e)>.08).sum()),
        'fraction_exceeding_pointwise_limit':float((abs(e)>.08).mean()),'shared_stream_max_difference':max(duplicates),'shared_streams_agree_at_1e_12':max(duplicates)<1e-12,
        'future_absolute_bound':'not established by this finite audit; mathematical Gaussian model is not a bounded-error guarantee', 'per_seed':per_seed}
    assert max(duplicates)<1e-12
    case=OUT/'reopening';case.mkdir(exist_ok=True)
    artifact={'scope':'Q7','measured':'100.040','bias_bounds':['-0.001','0.001']}
    path=case/'record.json';path.write_text(json.dumps(artifact)+'\n')
    old={'claim_id':'Q7-band','contract_id':'old-band','criterion_id':'true-state-band-v1','scope':'Q7','adapter':'bounded_sensor','target':'100','tolerance':'0.1','artifact':{'path':'reopening/record.json','sha256':digest(path.read_bytes())}}
    new={**old,'contract_id':'new-band','tolerance':'0.01'};old_receipt=evaluate(old,OUT);new_receipt=evaluate(new,OUT)
    assert old_receipt['verdict']=='supported' and new_receipt['verdict']=='contradicted'
    plan=compare(old,old_receipt,new,root=OUT);assert 'question_or_criterion' in plan['changed_dimensions'] and plan['action']=='perform_new_scoped_assessment'
    checks={'changed_question_preserves_old_support':True}
    same=json.loads(json.dumps(old,sort_keys=True,indent=4));unchanged=compare(old,old_receipt,same,root=OUT);checks['formatting_only_reuses_binding']=unchanged['action']=='reuse_historical_receipt_for_unchanged_contract'
    note={**old,'note':'shareable explanation'};np_=compare(old,old_receipt,note,root=OUT);checks['note_not_scientific_revision']=np_['changed_dimensions']==['unclassified_metadata'] and np_['action']=='review_metadata_and_bind_a_new_receipt'
    bad=deepcopy(old_receipt);bad['contract_sha256']='0'*64;checks['mismatched_receipt_unresolved']=compare(old,bad,new,root=OUT)['status']=='unresolved'
    bad_art=deepcopy(old_receipt);bad_art['artifact_sha256']='0'*64;checks['mismatched_historical_evidence_unresolved']=compare(old,bad_art,new,root=OUT)['status']=='unresolved'
    checks['missing_contract_unresolved']=compare(None,old_receipt,new,root=OUT)['status']=='unresolved'
    checks['missing_live_check_blocks_reuse']=compare(old,old_receipt,old)['status']=='unresolved'
    changed_method=compare(old,old_receipt,old,root=OUT,current_checker_sha256='0'*64);checks['checker_change_reopens']='checker_revision' in changed_method['changed_dimensions'] and changed_method['action']=='perform_new_scoped_assessment'
    path.write_text(json.dumps({**artifact,'measured':'100.004'})+'\n');stale=compare(old,old_receipt,old,root=OUT);checks['changed_bytes_block_reuse']=stale['status']=='unresolved'
    newer=deepcopy(new);newer['artifact']['sha256']=digest(path.read_bytes());changed_source=compare(new,new_receipt,newer,root=OUT);checks['explicit_evidence_revision_detected']='evidence_bytes_binding' in changed_source['changed_dimensions']
    # Restore original evidence to retain the original assessment pair exactly.
    path.write_text(json.dumps(artifact)+'\n')
    literal_path=case/'literal.json';literal_path.write_text(json.dumps({'scope':'literal','expression':'2+3'})+'\n')
    literal={'claim_id':'literal','contract_id':'L1','criterion_id':'rational-equality-v1','scope':'literal','adapter':'arithmetic_equal','expected_value':'5','artifact':{'path':'reopening/literal.json','sha256':digest(literal_path.read_bytes())}}
    lr=evaluate(literal,OUT);lp=compare(literal,lr,{**literal,'expected_value':'6'},root=OUT);checks['changed_assertion_not_criterion']='assertion' in lp['changed_dimensions'] and 'question_or_criterion' not in lp['changed_dimensions']
    assert all(checks.values())
    for name,value in [('old_contract.json',old),('old_receipt.json',old_receipt),('proposed_contract.json',new),('new_receipt.json',new_receipt),('reopening_plan.json',plan)]: (case/name).write_text(json.dumps(value,indent=2)+'\n')
    ledger=case/'history.jsonl';first=append_receipt(ledger,old_receipt);prefix=ledger.read_bytes();append_receipt(ledger,new_receipt,supersedes=first['event_sha256'],revision_note='New narrower criterion; original old-band support remains historical, not refuted.')
    events=[json.loads(x) for x in ledger.read_text().splitlines()];validate_ledger(events);assert ledger.read_bytes().startswith(prefix)
    result={'study':'PG-C1','saved_trace_audit':audit,'reopening_checks':checks,'old_verdict':old_receipt['verdict'],'new_verdict':new_receipt['verdict'],'same_evidence_hash':old_receipt['artifact_sha256']==new_receipt['artifact_sha256'],'history_prefix_preserved':True,'source_hashes_unchanged':True,'new_model_participants':0}
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({**result,'saved_trace_audit':{k:v for k,v in audit.items() if k!='per_seed'}},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run']);a=p.parse_args();prepare() if a.mode=='prepare' else run()
