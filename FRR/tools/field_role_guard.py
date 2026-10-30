"""Optional literal-source witness guard for one tiny threshold-record grammar.

This validates proposed field roles/quotes and complete note coverage. It does
not authenticate sources, parse arbitrary language, or certify physical truth.
"""
from __future__ import annotations
import argparse
import hashlib
import re
from pathlib import Path
from evidence_threshold import load_json
import json

GUARD_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
RULESET = 'field-role-witness-0.1'
MAX_BYTES = 1_048_576
NUMBER = r'[0-9]{1,64}'
LIMITATIONS = ['Literal declared source grammar only; unsupported prose withholds.',
               'Source hashes establish byte identity, not authenticity or empirical truth.',
               'Binding a proposal is not a task verdict or an LLM competence result.']

def _keys(x, keys):return isinstance(x,dict) and set(x)==set(keys)
def _num(x):return isinstance(x,str) and re.fullmatch(NUMBER,x) is not None

def bind(proposal, source_path, expected_sha256, entity, unit):
    out={'ruleset':RULESET,'guard_sha256':GUARD_SHA256,'status':'unresolved',
         'stage':'invalid_context','reasons':[],'limitations':LIMITATIONS[:]}
    def reject(stage, reason):
        out.update(stage=stage);out['reasons'].append(reason);return out
    if (not isinstance(entity,str) or not entity.strip() or len(entity)>128 or
            not isinstance(unit,str) or unit not in {'cm','kg'} or not isinstance(expected_sha256,str) or
            not re.fullmatch(r'[0-9a-f]{64}',expected_sha256)):
        return reject('invalid_context','Expected literal entity/unit and lowercase source SHA256.')
    try:
        if hashlib.sha256(Path(__file__).read_bytes()).hexdigest()!=GUARD_SHA256:
            return reject('guard_changed','Guard differs from loaded source snapshot.')
        with Path(source_path).open('rb') as stream:data=stream.read(MAX_BYTES+1)
    except (OSError,TypeError,ValueError):
        return reject('source_unavailable','Source or guard could not be read.')
    if len(data)>MAX_BYTES:return reject('unsupported_source','Source exceeds one MiB.')
    actual=hashlib.sha256(data).hexdigest();out['source_sha256']=actual
    if actual!=expected_sha256:return reject('source_hash_mismatch','Source bytes differ from expected hash.')
    try:text=data.decode('utf-8').strip()
    except UnicodeDecodeError:return reject('unsupported_source','Source is not UTF8.')
    e,u=re.escape(entity),re.escape(unit)
    criterion=re.match(e+r' must measure at least (?P<value>'+NUMBER+r') '+u+r' to pass\.',text)
    if criterion is None:return reject('unsupported_source','Criterion does not match the complete declared grammar.')
    note=re.compile(r'Note (?P<id>[A-Z]): (?:(?P<missing>no measurement for '+e+r' is recorded)\.|'+e+r' measures (?P<value>'+NUMBER+r') '+u+r'\.)')
    pos=criterion.end();notes={};ids=set()
    while pos<len(text):
        if text[pos]!=' ':return reject('unsupported_source','Unexpected content between source clauses.')
        found=note.match(text,pos+1)
        if found is None:return reject('unsupported_source','An entire source clause is unsupported; nothing is silently skipped.')
        if found['id'] in ids:return reject('unsupported_source','Repeated note IDs have no declared precedence.')
        ids.add(found['id']);notes[found.group(0)]={'state':'missing'} if found['missing'] else {'state':'measured','value':found['value']}
        pos=found.end()
    if not notes:return reject('unsupported_source','At least one explicit observation note is required.')
    if not _keys(proposal,{'entity','unit','source_sha256','minimum','observations'}):
        return reject('invalid_proposal','A complete typed witnessed proposal is required; copied context is not a field value.')
    if (proposal['entity'],proposal['unit'],proposal['source_sha256'])!=(entity,unit,actual):
        return reject('proposal_identity_mismatch','Proposal entity/unit/source binding differs from caller context.')
    minimum=proposal['minimum']
    if (not _keys(minimum,{'value','quote'}) or not _num(minimum['value']) or
            minimum['quote']!=criterion.group(0) or minimum['value']!=criterion['value']):
        return reject('criterion_binding_mismatch','Minimum value must bind to the criterion quotation, not an observation.')
    if not isinstance(proposal['observations'],list):return reject('invalid_proposal','Observations must be a list.')
    seen=set();bound=[]
    for item in proposal['observations']:
        if not isinstance(item,dict) or not isinstance(item.get('quote'),str):
            return reject('observation_binding_mismatch','Each observation requires an exact source note quotation.')
        quote=item['quote'];expected=notes.get(quote)
        if expected is None or quote in seen:
            return reject('observation_binding_mismatch','Observation quotation is absent, repeated, or belongs to the criterion role.')
        required={'state','quote'} if expected['state']=='missing' else {'state','value','quote'}
        if not _keys(item,required) or item['state']!=expected['state']:
            return reject('observation_binding_mismatch','Observation type or schema differs from quoted source role.')
        if expected['state']=='measured' and (not _num(item['value']) or item['value']!=expected['value']):
            return reject('observation_binding_mismatch','Measured value differs from its quoted source note.')
        seen.add(quote);bound.append(dict(expected))
    if seen!=set(notes):return reject('incomplete_observations','Every source note must be covered, including missing/conflicting notes.')
    out.update(status='bound',stage='bound_fields',entity=entity,unit=unit,
               fields={'minimum':minimum['value'],'observations':bound},source_note_count=len(notes))
    out['reasons'].append('All proposed roles, values, quotations and note coverage match this literal source grammar.')
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('proposal',type=Path)
    p.add_argument('--source',required=True,type=Path);p.add_argument('--sha256',required=True)
    p.add_argument('--entity',required=True);p.add_argument('--unit',required=True);args=p.parse_args()
    try:proposal=load_json(args.proposal.read_bytes())
    except (OSError,ValueError,UnicodeDecodeError):
        print(json.dumps({'status':'unresolved','stage':'invalid_proposal','reasons':['Proposal is not readable strict JSON.']}));return
    print(json.dumps(bind(proposal,args.source,args.sha256,args.entity,args.unit),indent=2))
if __name__=='__main__':main()
