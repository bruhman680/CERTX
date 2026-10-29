"""Untrained causal attention cache arithmetic. Not SwaT or language reasoning."""
from pathlib import Path
import sys,json,hashlib,copy
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from cache_replay_plan import plan, token_digest, IDENTITY_FIELDS

D=16;V=64;L=2

def weights(seed):
    rng=np.random.default_rng(seed)
    return {'embed':rng.normal(0,.3,(V,D)), 'layers':[
        [rng.normal(0,.25,(D,D)) for _ in range(4)] for _ in range(L)],
        'out':rng.normal(0,.25,(D,V))}

def position(n,offset):
    return .2*np.sin((np.arange(n)[:,None]+offset)/np.power(100,np.arange(D)[None,:]/D))

def full(ids,w,offset=0):
    x=w['embed'][ids]+position(len(ids),offset)
    for q,k,v,o in w['layers']:
        Q,K,Val=x@q,x@k,x@v
        scores=Q@K.T/np.sqrt(D)
        scores[np.triu_indices(len(ids),1)]=-np.inf
        a=np.exp(scores-np.max(scores,axis=1,keepdims=True));a/=a.sum(axis=1,keepdims=True)
        x=x+np.tanh((a@Val)@o)
    return x@w['out']

def incremental(ids,w,cache=None,offset=0):
    cache=[(np.empty((0,D)),np.empty((0,D))) for _ in range(L)] if cache is None else [(k.copy(),v.copy()) for k,v in cache]
    rows=[]
    for token in ids:
        t=len(cache[0][0]);x=w['embed'][token]+position(t+1,offset)[-1]
        for i,(q,k,v,o) in enumerate(w['layers']):
            K=np.concatenate((cache[i][0],(x@k)[None,:]),axis=0)
            Val=np.concatenate((cache[i][1],(x@v)[None,:]),axis=0)
            score=(K@(x@q))/np.sqrt(D);a=np.exp(score-score.max());a/=a.sum()
            x=x+np.tanh((a@Val)@o);cache[i]=(K,Val)
        rows.append(x@w['out'])
    return np.array(rows),cache

def ident(seed,offset=0):
    return {'model_revision':f'random-seed-{seed}','tokenizer_revision':'fixed-integer-v1',
            'position_config':f'absolute-sinusoid-offset-{offset}','attention_policy':'causal_full',
            'kv_layout':'layers-tokens-d16','dtype':'float64','adapter_identity':'none',
            'multimodal_identity':'none','namespace':'authored-cpu-experiment'}

def run():
    rows=[];validation=[]
    base=list(range(1,25));sentinel=[62]
    for seed in [3,11,29,47,83]:
        w=weights(seed);_,oldcache=incremental(base,w)
        cached={'token_ids':base,'cache_token_count':len(base),'prefix_sha256':token_digest(base),'execution_identity':ident(seed)}
        early=base.copy();early[3]=40
        late=base.copy();late[20]=41
        specs=[('append',base+[43,44]+sentinel,seed,0,None),
               ('early_replace',early+sentinel,seed,0,None),
               ('middle_delete',base[:10]+base[13:]+sentinel,seed,0,None),
               ('late_replace',late+sentinel,seed,0,None),
               ('model_change',base+sentinel,seed+1000,0,None),
               ('position_change',base+sentinel,seed,5,None),
               ('adapter_change',base+sentinel,seed,0,'adapter'),
               ('multimodal_change',base+sentinel,seed,0,'multimodal'),
               ('tampered_digest',base+sentinel,seed,0,'digest'),
               ('partial_cache',base+[43]+sentinel,seed,0,'partial')]
        for name,new,newseed,offset,special in specs:
            c=copy.deepcopy(cached);req={'token_ids':new,'execution_identity':ident(newseed,offset)}
            if special=='adapter':req['execution_identity']['adapter_identity']='adapter-B'
            if special=='multimodal':req['execution_identity']['multimodal_identity']='image-B'
            if special=='digest':c['prefix_sha256']='0'*64
            if special=='partial':
                c['cache_token_count']=9;c['prefix_sha256']=token_digest(base[:9])
            decision=plan(c,req);keep=decision['reuse_prefix_tokens'];ww=weights(newseed)
            truncated=[(k[:keep].copy(),v[:keep].copy()) for k,v in oldcache]
            actual,rebuilt=incremental(new[keep:],ww,truncated,offset)
            expected=full(new,ww,offset)
            err=float(np.max(np.abs(actual-expected[keep:])))
            stale,stale_cache=incremental(sentinel,ww,oldcache,offset)
            stale_err=float(np.max(np.abs(stale[-1]-expected[-1])))
            rows.append({'seed':seed,'case':name,'plan':decision,'max_logit_error_vs_full':err,
                         'naive_old_cache_plus_sentinel_error':stale_err,
                         'replayed_numerical_rows':len(actual),'full_numerical_rows':len(new),
                         'final_cache_bytes':sum(k.nbytes+v.nbytes for k,v in rebuilt),
                         'same_model_numeric_agreement':err<=1e-10,
                         'identity_only_caveat':special in ['adapter','multimodal']})
    exemplar={'token_ids':base,'cache_token_count':24,'prefix_sha256':token_digest(base),'execution_identity':ident(3)}
    request={'token_ids':base+[62],'execution_identity':ident(3)}
    for name,edit in [('negative_token',lambda c,r:r.update(token_ids=[-1])),('boolean_token',lambda c,r:r.update(token_ids=[True])),('count_too_large',lambda c,r:c.update(cache_token_count=25)),('boolean_count',lambda c,r:c.update(cache_token_count=True)),('missing_tokens',lambda c,r:r.pop('token_ids'))]:
        c,r=copy.deepcopy(exemplar),copy.deepcopy(request);edit(c,r)
        try:plan(c,r);rejected=False
        except ValueError:rejected=True
        validation.append({'case':name,'rejected':rejected})
    for name,edit in [('missing_identity',lambda c,r:r.pop('execution_identity')),('blank_revision',lambda c,r:r['execution_identity'].update(model_revision='')),('unsupported_mask',lambda c,r:(c['execution_identity'].update(attention_policy='sliding'),r['execution_identity'].update(attention_policy='sliding')))]:
        c,r=copy.deepcopy(exemplar),copy.deepcopy(request);edit(c,r);d=plan(c,r)
        validation.append({'case':name,'forced_full_rebuild':d['reuse_prefix_tokens']==0,'reasons':d['reasons']})
    output={'scope':'Untrained random numeric cache development; no language/semantic efficacy or SwaT reproduction.',
            'numpy':np.__version__,'rows':rows,'validation':validation,
            'all_numeric_rows_match':all(x['same_model_numeric_agreement'] for x in rows),
            'all_invalid_inputs_handled':all(x.get('rejected',x.get('forced_full_rebuild',False)) for x in validation)}
    print(json.dumps(output,indent=2))
    return output

if __name__=='__main__':
    r=run()
    sys.exit(0 if r['all_numeric_rows_match'] and r['all_invalid_inputs_handled'] else 1)
