"""Explain explicit assessment changes without rewriting a historical verdict.

This is a local difference/binding utility, not semantic equivalence or truth validation.
"""
import argparse
import json
from pathlib import Path
from verification_layer import canonical,digest
import verification_layer as verifier


def compare(old_contract,old_receipt,new_contract,root=None,current_checker_sha256=None):
    result={'status':'unresolved','changed_dimensions':[], 'historical_verdict':old_receipt.get('verdict') if isinstance(old_receipt,dict) else None,
            'action':'recover_original_contract_and_receipt','notes':[], 'binding_checks':{}}
    if not all(isinstance(x,dict) for x in [old_contract,old_receipt,new_contract]):
        result['notes'].append('Original contract, receipt and proposed contract must be supplied as objects.');return result
    try:
        old_hash=digest(canonical(old_contract));new_hash=digest(canonical(new_contract))
    except (TypeError,ValueError):
        result['notes'].append('Contracts must be finite canonical JSON.');return result
    result.update(old_contract_sha256=old_hash,proposed_contract_sha256=new_hash)
    metadata_match=all(old_receipt.get(k)==old_contract.get(k) for k in ['claim_id','contract_id','criterion_id','scope'])
    certified=old_receipt.get('verdict') in ['supported','contradicted']
    old_declared_artifact=old_contract.get('artifact',{})
    artifact_match=(not certified) or (isinstance(old_declared_artifact,dict) and old_receipt.get('artifact_sha256')==old_declared_artifact.get('sha256') and isinstance(old_receipt.get('artifact_sha256'),str))
    bound=old_receipt.get('contract_sha256')==old_hash and metadata_match and artifact_match
    result['binding_checks']['historical_contract']=bound
    if not bound:
        result['action']='recover_or_repair_historical_binding';result['notes'].append('Binding mismatch does not establish that the historical claim was false.');return result
    changed=[]
    def fields(names,dimension):
        if any(old_contract.get(n)!=new_contract.get(n) for n in names):changed.append(dimension)
    fields(['claim_id'],'claim_identity');fields(['scope'],'scope');fields(['adapter'],'method')
    fields(['criterion_id','target','tolerance'],'question_or_criterion');fields(['expected_value'],'assertion')
    old_art=old_contract.get('artifact',{});new_art=new_contract.get('artifact',{})
    if not isinstance(old_art,dict) or not isinstance(new_art,dict):
        result['notes'].append('Artifact binding must be an object.');return result
    if old_art.get('sha256')!=new_art.get('sha256'):changed.append('evidence_bytes_binding')
    if old_art.get('path')!=new_art.get('path'):changed.append('evidence_location')
    known={'claim_id','contract_id','scope','adapter','criterion_id','target','tolerance','expected_value','artifact'}
    if {k:v for k,v in old_contract.items() if k not in known}!={k:v for k,v in new_contract.items() if k not in known}:changed.append('unclassified_metadata')
    if old_contract.get('contract_id')!=new_contract.get('contract_id'):changed.append('contract_identity')
    if {k:v for k,v in old_art.items() if k not in {'sha256','path'}}!={k:v for k,v in new_art.items() if k not in {'sha256','path'}}:changed.append('unclassified_artifact_metadata')
    if current_checker_sha256 is None:
        try:
            actual=digest(Path(verifier.__file__).read_bytes())
            current_checker_sha256=verifier.SOURCE_SHA256_AT_IMPORT if actual==verifier.SOURCE_SHA256_AT_IMPORT else None
        except OSError:current_checker_sha256=None
    method_known=isinstance(current_checker_sha256,str) and len(current_checker_sha256)==64
    result['binding_checks']['current_checker_identity_available']=method_known
    if method_known and old_receipt.get('checker_sha256')!=current_checker_sha256:changed.append('checker_revision')
    result['changed_dimensions']=changed
    live=None
    if root is not None:
        try:
            root=Path(root).resolve();path=(root/new_art['path']).resolve()
            if Path(new_art['path']).is_absolute() or not path.is_relative_to(root) or path.stat().st_size>1_000_000:raise ValueError('Artifact outside local bounds')
            live=digest(path.read_bytes())==new_art['sha256']
        except (OSError,KeyError,TypeError,ValueError):live=False
    result['binding_checks']['proposed_live_artifact']=live
    result['notes'].append('Differences concern recorded fields; source reliability and semantic equivalence are not inferred.')
    if not method_known or live is not True:
        result['action']='resolve_current_method_or_evidence_binding';return result
    result['status']='ready_for_next_action'
    if changed:
        scientific={'claim_identity','scope','method','question_or_criterion','assertion','evidence_bytes_binding','checker_revision'}
        result['action']='perform_new_scoped_assessment' if scientific.intersection(changed) else 'review_metadata_and_bind_a_new_receipt'
    elif old_receipt.get('verdict') in ['supported','contradicted']:
        result['action']='reuse_historical_receipt_for_unchanged_contract'
    else:result['action']='reassess_unresolved_contract'
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('old_contract');p.add_argument('old_receipt');p.add_argument('proposed_contract');p.add_argument('--root');a=p.parse_args()
    values=[json.loads(Path(n).read_text()) for n in [a.old_contract,a.old_receipt,a.proposed_contract]]
    print(json.dumps(compare(*values,root=a.root),indent=2))


if __name__=='__main__':main()
