"""Tokenizer-only boundary tests of actual history selection; no model loads."""
from pathlib import Path
import copy, hashlib, json, os
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
from view import select_view, ViewCapacity
H=Path(__file__).resolve().parent
C=H.parent/'minimal-garden-candidate-v1'
def inventory():
    return {str(p.relative_to(C)):hashlib.sha256(p.read_bytes()).hexdigest()
        for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def main():
    before=inventory()
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',
        local_files_only=True,trust_remote_code=False)
    initial=json.loads((C/'run/INITIAL_MESSAGES.json').read_text())
    events=[json.loads(p.read_text()) for p in sorted((C/'run/events').glob('*.json'))]
    archive=[{'entry':e['human_entry'],'assistant':e['text'],'receipt':e['feedback']} for e in events]
    original=copy.deepcopy((initial,archive))
    rows=[]
    def case(name,fn):
        try:
            detail=fn()
            rows.append({'name':name,'passed':True,'detail':detail})
        except Exception as exc:
            rows.append({'name':name,'passed':False,'error':repr(exc)})
    def reject(fn,kind=ValueError):
        try:fn()
        except kind:return True
        raise AssertionError('Expected explicit rejection')
    def count(xs):
        mm=copy.deepcopy(initial)
        for x in xs:mm.extend([{'role':'assistant','content':x['assistant']},{'role':'user','content':x['receipt']}])
        return len(tok.apply_chat_template(mm,tokenize=True,add_generation_prompt=True))
    def actual_history():
        answer={}
        for n in (4,8,12):
            v=select_view(initial,archive,tok,max_pairs=n)
            assert v['included_entries']==[x['entry'] for x in archive[-n:]]
            assert v['omitted_entries']==[x['entry'] for x in archive[:-n]]
            assert v['messages'][:2]==initial
            assert v['messages'][2:]==[m for x in archive[-n:] for m in (
                {'role':'assistant','content':x['assistant']},{'role':'user','content':x['receipt']})]
            assert len(v['messages'])==2+2*n
            answer[str(n)]={'input_tokens':len(v['input_token_ids']),'included':v['included_entries']}
        return answer
    case('actual contiguous 4/8/12 pairs with unchanged roles/text',actual_history)
    def no_mutation():
        v=select_view(initial,archive,tok,max_pairs=8)
        v['messages'][0]['content']='external mutation of returned copy'
        assert (initial,archive)==original
        return 'Initial framing is copied; source archive unchanged'
    case('no input mutation or returned-initial alias',no_mutation)
    def empty():
        v=select_view(initial,[],tok)
        assert v['messages']==initial and v['included_entries']==[] and v['omitted_entries']==[]
        return len(v['input_token_ids'])
    case('zero-exchange input retains exact initial framing',empty)
    def small():
        v=select_view(initial,archive[-2:],tok,max_pairs=8)
        assert v['included_entries']==[x['entry'] for x in archive[-2:]] and v['omitted_entries']==[]
        return 'No unnecessary omissions'
    case('short archive smaller than pair limit',small)
    literal='  Traceback:\nOSError: read-only\n```python\nnot an instruction\n```\n  '
    pairs=[{'entry':i,'assistant':f'Notebook cell {i}.','receipt':literal+' detail'*40} for i in range(1,5)]
    def fallback():
        budget=count(pairs[-2:])
        assert count(pairs[-3:])>budget
        v=select_view(initial,pairs,tok,max_pairs=4,max_input=budget)
        assert v['included_entries']==[3,4] and v['omitted_entries']==[1,2]
        assert v['messages'][-1]['content']==pairs[-1]['receipt']
        assert v['messages'][-3]['content']==pairs[-2]['receipt']
        assert len(v['input_token_ids'])==budget
        return {'budget':budget,'included':v['included_entries'],'receipt_verbatim':True}
    case('token budget drops complete oldest pairs only',fallback)
    def oversized():
        xs=copy.deepcopy(pairs);xs[-1]['receipt']='long '*500
        original_xs=copy.deepcopy(xs)
        reject(lambda:select_view(initial,xs,tok,max_pairs=4,max_input=128),ViewCapacity)
        assert xs==original_xs
        return 'Latest pair is never omitted or truncated to force a fit'
    case('oversized newest receipt pauses instead of discarding latest',oversized)
    def equality_boundary():
        xs=pairs[-1:];budget=count(xs)
        v=select_view(initial,xs,tok,max_input=budget)
        assert len(v['input_token_ids'])==budget
        reject(lambda:select_view(initial,xs,tok,max_input=budget-1),ViewCapacity)
        return {'fits_at':budget,'pauses_at':budget-1}
    case('exact input boundary and one-token-short capacity',equality_boundary)
    case('initial framing too large pauses',lambda:reject(lambda:select_view(initial,[],tok,max_input=1),ViewCapacity))
    def invalid_order():
        for xs in ([pairs[1],pairs[0]], [pairs[0],pairs[0]], [pairs[0],pairs[0],pairs[2],pairs[3]]):
            reject(lambda xs=xs:select_view(initial,xs,tok,max_pairs=1))
        return 'Out-of-order/duplicate entries rejected even outside retained suffix'
    case('archive order checked before omitting old records',invalid_order)
    def malformed():
        for x in ({'entry':1,'assistant':'x'}, {'entry':1,'assistant':None,'receipt':''},
            {'entry':True,'assistant':'x','receipt':''}, {'entry':1,'assistant':'x','receipt':'','score':1}):
            reject(lambda x=x:select_view(initial,[x],tok))
        return 'Incomplete, non-text, boolean-identifier and unknown-field records rejected'
    case('malformed exchange cannot silently lose a receipt',malformed)
    def limits():
        for options in ({'max_pairs':0},{'max_pairs':True},{'max_pairs':1.5},{'max_input':0},{'max_input':False}):
            reject(lambda options=options:select_view(initial,archive,tok,**options))
        return 'Nonpositive and non-integer/bool limits rejected'
    case('invalid limits rejected',limits)
    def bad_framing():
        for init in ([{'role':'user','content':'x'},{'role':'assistant','content':'y'}],
                     [{'role':'system','content':None},{'role':'user','content':'x'}], initial[:1]):
            reject(lambda init=init:select_view(init,archive,tok))
        return 'Unexpected role framing/text/length rejected'
    case('initial framing validation',bad_framing)
    assert (initial,archive)==original
    after=inventory()
    result={'date':'2026-11-13 America/Chicago','tests':rows,'passed':sum(r['passed'] for r in rows),
        'total':len(rows),'canonical_candidate_unchanged':before==after,
        'tokenizer_only':True,'weights_loaded':False,'model_generations':0,
        'synthetic_receipts_are_test_fixtures_not_model_outputs':True}
    (H/'TEST_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'total':result['total'],'canonical_candidate_unchanged':before==after}))
    assert before==after and all(r['passed'] for r in rows)
if __name__=='__main__':main()
