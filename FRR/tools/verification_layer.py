"""Scoped verification receipts. Two prototype rulesets, not a general truth judge."""
import argparse
import ast
import fcntl
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path

VERSIONS={'0.1','0.2'}
CRITERIA={'arithmetic_equal':'rational-equality-v1','bounded_sensor':'true-state-band-v1'}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rational(text):
    if not isinstance(text,str) or len(text)>256:
        raise ValueError('Expected a bounded rational string')
    result=Fraction(text)
    if max(result.numerator.bit_length(),result.denominator.bit_length())>4096:
        raise ValueError('Rational magnitude limit')
    return result


def expression_value(text):
    if not isinstance(text,str) or len(text)>256:
        raise ValueError('Expression length limit')
    tree=ast.parse(text,mode='eval')
    if sum(1 for _ in ast.walk(tree))>64:
        raise ValueError('Expression complexity limit')
    def visit(node):
        if isinstance(node,ast.Expression):return visit(node.body)
        if isinstance(node,ast.Constant) and type(node.value) is int and abs(node.value)<=10**9:
            return Fraction(node.value)
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            val=visit(node.operand);return val if isinstance(node.op,ast.UAdd) else -val
        if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
            left,right=visit(node.left),visit(node.right)
            if isinstance(node.op,ast.Add):result=left+right
            elif isinstance(node.op,ast.Sub):result=left-right
            elif isinstance(node.op,ast.Mult):result=left*right
            else:result=left/right
            return rational(str(result))
        raise ValueError('Unsupported expression syntax')
    return visit(tree)


def evaluate(contract,root,version='0.2'):
    if version not in VERSIONS:raise ValueError('Unknown ruleset')
    record=dict(claim_id=contract.get('claim_id'),contract_id=contract.get('contract_id'),
        criterion_id=contract.get('criterion_id'),scope=contract.get('scope'),ruleset=version,
        checker_sha256=digest(Path(__file__).read_bytes()),contract_sha256=digest(canonical(contract)),
        verdict='unresolved',checks={},assumptions=[],reason='')
    def stop(reason):record['reason']=reason;return record
    if not all(isinstance(contract.get(k),str) and contract[k] for k in ['claim_id','contract_id','criterion_id','scope','adapter']):
        return stop('Missing contract identity, criterion or scope')
    try:
        root=Path(root).resolve();spec=contract['artifact'];path=(root/spec['path']).resolve()
        if Path(spec['path']).is_absolute() or not path.is_relative_to(root):raise ValueError('Artifact outside root')
        if path.stat().st_size>1_000_000:raise ValueError('Artifact size limit')
        data=path.read_bytes();actual_hash=digest(data);record['artifact_sha256']=actual_hash
        if actual_hash!=spec['sha256']:
            record['checks']['integrity']='fail';return stop('Evidence bytes differ from bound artifact')
        record['checks']['integrity']='pass';payload=json.loads(data)
        if payload['scope']!=contract['scope']:
            record['checks']['scope']='fail';return stop('Claim scope differs from evidence scope')
        record['checks']['scope']='pass'
        adapter=contract['adapter']
        if adapter not in CRITERIA or (version=='0.1' and adapter=='bounded_sensor'):
            return stop('No available domain adapter in this ruleset')
        if contract['criterion_id']!=CRITERIA[adapter]:
            record['checks']['criterion']='unresolved';return stop('Criterion is not implemented by this adapter')
        record['checks']['criterion']='pass'
        if adapter=='arithmetic_equal':
            actual=expression_value(payload['expression']);claimed=rational(contract['expected_value'])
            record['computed_value']=str(actual)
            record['verdict']='supported' if actual==claimed else 'contradicted'
            record['assumptions']=['Claim concerns the literal expression and exact rational semantics only.']
            record['checks']['domain']='pass' if actual==claimed else 'fail'
            return stop('Exact rational comparison completed')
        measured=rational(payload['measured']);bounds=payload.get('bias_bounds')
        if not isinstance(bounds,list) or len(bounds)!=2:return stop('Sensor bias bounds unavailable')
        low,high=map(rational,bounds)
        if low>high:return stop('Inconsistent bias interval')
        target=rational(contract['target']);tol=rational(contract['tolerance'])
        if tol<0:return stop('Negative tolerance')
        state_low,state_high=measured-high,measured-low
        ok_low,ok_high=target-tol,target+tol
        record['computed_state_interval']=[str(state_low),str(state_high)]
        record['assumptions']=['Supplied reading is faithful and supplied bias interval covers the actual bias.',
                               'Measurement equals true state plus bias; other measurement errors are absent or included in bounds.']
        if state_low>=ok_low and state_high<=ok_high:record['verdict']='supported'
        elif state_high<ok_low or state_low>ok_high:record['verdict']='contradicted'
        record['checks']['domain']={'supported':'pass','contradicted':'fail','unresolved':'unresolved'}[record['verdict']]
        return stop('State-band assessment conditional on supplied measurement assumptions')
    except (KeyError,TypeError,ValueError,OSError,SyntaxError,ZeroDivisionError,RecursionError) as exc:
        return stop('Check unavailable or invalid input: '+type(exc).__name__)


def validate_ledger(events):
    previous=None
    for event in events:
        body={k:v for k,v in event.items() if k!='event_sha256'}
        if body.get('previous_event_sha256')!=previous or digest(canonical(body))!=event.get('event_sha256'):
            raise ValueError('Ledger chain mismatch')
        previous=event['event_sha256']
    return previous


def append_receipt(path,receipt,supersedes=None,revision_note=None):
    """Local hash chain under a writer lock; not authentication or tamper-proof storage."""
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a+',encoding='utf-8') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX)
        handle.seek(0);events=[json.loads(line) for line in handle if line.strip()]
        previous=validate_ledger(events)
        if supersedes:
            old=next((e for e in events if e['event_sha256']==supersedes),None)
            if old is None or old['receipt']['claim_id']!=receipt['claim_id'] or not revision_note:
                raise ValueError('Revision needs a prior event for this claim and a note')
        body=dict(previous_event_sha256=previous,receipt=receipt,supersedes=supersedes,revision_note=revision_note)
        event={**body,'event_sha256':digest(canonical(body))}
        handle.seek(0,2);handle.write(json.dumps(event,sort_keys=True)+'\n');handle.flush();os.fsync(handle.fileno())
        return event


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('contract');parser.add_argument('--root',required=True)
    parser.add_argument('--version',choices=sorted(VERSIONS),default='0.2')
    parser.add_argument('--ledger');parser.add_argument('--supersedes');parser.add_argument('--revision-note')
    args=parser.parse_args();contract=json.loads(Path(args.contract).read_text())
    receipt=evaluate(contract,args.root,args.version)
    if args.ledger:print(json.dumps(append_receipt(args.ledger,receipt,args.supersedes,args.revision_note),indent=2))
    else:print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
