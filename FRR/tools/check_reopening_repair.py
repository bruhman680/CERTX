"""Disclosed exact-contract reuse repair and read-only regression replay."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from verification_layer import evaluate,digest
from reopen_assessment import compare
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evaluation/practice-growth-v1'


def prepare():
    p=OUT/'REPAIR_MANIFEST.json'
    if p.exists():raise ValueError('Repair already prepared')
    names=['tools/reopen_assessment.py','tools/check_reopening_repair.py','tools/verification_layer.py','evaluation/practice-growth-v1/AMENDMENT_01.md','evaluation/practice-growth-v1/INITIAL_OUTPUT_HASHES.json']
    p.write_text(json.dumps({'hashes':{n:digest((ROOT/n).read_bytes()) for n in names}},indent=2)+'\n');print('prepared repair')


def run():
    m=json.loads((OUT/'REPAIR_MANIFEST.json').read_text());assert all(digest((ROOT/n).read_bytes())==h for n,h in m['hashes'].items())
    old=json.loads((OUT/'reopening/old_contract.json').read_text());receipt=json.loads((OUT/'reopening/old_receipt.json').read_text());new=json.loads((OUT/'reopening/proposed_contract.json').read_text());checks={}
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);shutil.copytree(OUT/'reopening',root/'reopening');path=root/'reopening/record.json';original=path.read_bytes()
        plan=compare(old,receipt,new,root=root);checks['changed_question_preserves_old_support']=plan['historical_verdict']=='supported' and 'question_or_criterion' in plan['changed_dimensions'] and plan['action']=='perform_new_scoped_assessment'
        checks['formatting_only_reuses_binding']=compare(old,receipt,json.loads(json.dumps(old,sort_keys=True,indent=4)),root=root)['action']=='reuse_historical_receipt_for_unchanged_contract'
        p=compare(old,receipt,{**old,'note':'shareable explanation'},root=root);checks['note_not_scientific_revision']=p['changed_dimensions']==['unclassified_metadata'] and p['action']=='review_metadata_and_bind_a_new_receipt'
        bad=deepcopy(receipt);bad['contract_sha256']='0'*64;checks['mismatched_receipt_unresolved']=compare(old,bad,new,root=root)['status']=='unresolved'
        bad=deepcopy(receipt);bad['artifact_sha256']='0'*64;checks['mismatched_historical_evidence_unresolved']=compare(old,bad,new,root=root)['status']=='unresolved'
        checks['missing_contract_unresolved']=compare(None,receipt,new,root=root)['status']=='unresolved'
        checks['missing_live_check_blocks_reuse']=compare(old,receipt,old)['status']=='unresolved'
        p=compare(old,receipt,old,root=root,current_checker_sha256='0'*64);checks['checker_change_reopens']='checker_revision' in p['changed_dimensions'] and p['action']=='perform_new_scoped_assessment'
        art=json.loads(path.read_text());art['measured']='100.004';path.write_text(json.dumps(art)+'\n');checks['changed_bytes_block_reuse']=compare(old,receipt,old,root=root)['status']=='unresolved'
        newer=deepcopy(new);newer['artifact']['sha256']=digest(path.read_bytes());p=compare(new,json.loads((OUT/'reopening/new_receipt.json').read_text()),newer,root=root);checks['explicit_evidence_revision_detected']='evidence_bytes_binding' in p['changed_dimensions'];path.write_bytes(original)
        literal={'claim_id':'literal','contract_id':'L1','criterion_id':'rational-equality-v1','scope':'literal','adapter':'arithmetic_equal','expected_value':'5','artifact':{'path':'reopening/literal.json','sha256':digest((root/'reopening/literal.json').read_bytes())}}
        p=compare(literal,evaluate(literal,root),{**literal,'expected_value':'6'},root=root);checks['changed_assertion_not_criterion']='assertion' in p['changed_dimensions'] and 'question_or_criterion' not in p['changed_dimensions']
        null_plan=compare(old,receipt,{**old,'expected_value':None},root=root);checks['absent_null_never_reuses']=null_plan['action']=='review_metadata_and_bind_a_new_receipt' and null_plan['old_contract_sha256']!=null_plan['proposed_contract_sha256']
        numeric={**old,'note':1};nr=evaluate(numeric,root);boolean_plan=compare(numeric,nr,{**numeric,'note':True},root=root);checks['integer_boolean_never_reuses']=boolean_plan['action']=='review_metadata_and_bind_a_new_receipt' and boolean_plan['old_contract_sha256']!=boolean_plan['proposed_contract_sha256']
    command=[sys.executable,str(ROOT/'tools/reopen_assessment.py'),str(OUT/'reopening/old_contract.json'),str(OUT/'reopening/old_receipt.json'),str(OUT/'reopening/proposed_contract.json'),'--root',str(OUT)]
    cli=subprocess.run(command,capture_output=True,text=True,timeout=10);cli_plan=json.loads(cli.stdout);assert cli.returncode==0 and cli_plan['action']=='perform_new_scoped_assessment'
    hashes=json.loads((OUT/'INITIAL_OUTPUT_HASHES.json').read_text());preserved={n:digest((OUT/n).read_bytes())==h for n,h in hashes.items()};assert all(preserved.values()) and all(checks.values())
    result={'scope':'Disclosed local helper repair; authored regression and CLI checks, not semantic/source reliability validation','checks':checks,'all_checks_passed':True,'initial_output_hashes_preserved':preserved,'cli':{'returncode':cli.returncode,'receipt':cli_plan,'stderr':cli.stderr},'repaired_helper_sha256':digest((ROOT/'tools/reopen_assessment.py').read_bytes()),'repair_source_hashes_unchanged':True}
    (OUT/'REPAIR_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run']);a=p.parse_args();prepare() if a.mode=='prepare' else run()
