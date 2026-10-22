"""Two constructed development contacts; no physical/semantic carrier attribution."""
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
from scipy.optimize import least_squares

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/probe-followups-v1'
FILES=['experiments/probe_followups.py','evaluation/probe-followups-v1/PROTOCOL.md']

def hashes():return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in FILES}

def calibration():
    # Readout follows retained correlations; witness bypasses readout gate by construction.
    rows=[]
    for world in ['field','gated_private']:
        for action in ['keep','sham','erase_field_close_gate','erase_field_restore_gate']:
            erased=action.startswith('erase');gate=not(action=='erase_field_close_gate')
            cf=0. if erased else .8;cp=.8
            signal=cf if world=='field' else cp*gate
            rows.append({'world':world,'action':action,'main_contrast':.4*.8*signal/2,
                         'direct_field_success':(.5+.5*cf),'direct_private_success':(.5+.5*cp),
                         'private_gate_open':gate,
                         'contaminated_private_witness_success':.5+.5*cp*gate})
    d,s=.1,.9
    witnessF=1-d/2;witnessP=1-s/2
    ks=np.arange(8);F,P=.128,.06;a,b=1-d,1-s
    permutation=float(np.max(abs((F*a**ks+P*b**ks)-(P*b**ks+F*a**ks))))
    def cell(world,action):return next(r for r in rows if r['world']==world and r['action']==action)
    checks={'keep_erase_main_laws_match':all(cell('field',c)['main_contrast']==cell('gated_private',c)['main_contrast'] for c in ['keep','erase_field_close_gate']),
            'restore_gate_discriminates':cell('field','erase_field_restore_gate')['main_contrast']!=cell('gated_private','erase_field_restore_gate')['main_contrast'],
            'direct_private_witness_survives_gate':cell('gated_private','erase_field_close_gate')['direct_private_success']==.9,
            'contaminated_witness_loses_access':cell('gated_private','erase_field_close_gate')['contaminated_private_witness_success']==.5,
            'sham_preserves':all(cell(w,'keep')['main_contrast']==cell(w,'sham')['main_contrast'] for w in ['field','gated_private']),
            'rates_recovered_by_assumed_direct_witness':bool(np.isclose(2*(1-witnessF),d) and np.isclose(2*(1-witnessP),s)),
            'component_permutation_invariant':permutation==0}
    return {'scope':'Gate-independent direct witness and its accuracy are stipulated; calibration is not independently observed in hardware or agents',
            'rows':rows,'imperfect_clearP':{'direct_success_field':witnessF,'direct_success_private':witnessP,'estimated_d':2*(1-witnessF),'estimated_s':2*(1-witnessP)},'checks':checks}

def curve(name,k):
    if name=='separated':return .128*.9**k+.06*.1**k
    if name=='close':return .128*.45**k+.06*.4**k
    if name=='collision':return .188*.7**k
    if name=='single':return .188*.9**k
    if name=='misspecified':return .188*.8**k*(1+.35*np.sin(np.pi*k/2))
    raise ValueError(name)

def predict(pars,k,two):
    if two:
        A,q,a,b=pars;return A*(q*a**k+(1-q)*b**k)
    A,r=pars;return A*r**k

def fit(k,y,two,one=None):
    A=float(np.clip(y[0],.001,.499));attempts=[];candidates=[]
    starts=[[A,.68,.9,.1],[A,.5,.7,.4],[A,.5,.6,.55]] if two else [[A,r] for r in [.2,.6,.95]]
    for start in starts:
        res=least_squares(lambda p:predict(p,k,two)-y,start,
                          bounds=([0]*len(start),[.5]+[1]*(len(start)-1)),
                          max_nfev=500,ftol=1e-10,xtol=1e-10,gtol=1e-10)
        loss=float(np.sum(res.fun**2));ok=bool(res.success and np.all(np.isfinite(res.x)))
        attempts.append({'start':start,'success':ok,'status':int(res.status),'nfev':int(res.nfev),'train_SSE':loss})
        if ok:candidates.append((loss,res.x.tolist(),'optimized'))
    if two:
        pars=[one['parameters'][0],1.,one['parameters'][1],one['parameters'][1]]
        candidates.append((float(np.sum((predict(pars,k,True)-y)**2)),pars,'embedded_one_component'))
    if not candidates:raise RuntimeError('No successful one-component fit')
    loss,pars,origin=min(candidates,key=lambda x:x[0])
    return {'parameters':pars,'train_SSE':loss,'origin':origin,'attempts':attempts}

def main():
    if sys.argv[1:]==['prepare']:
        p=OUT/'MANIFEST.json'
        if p.exists():raise SystemExit('Refusing overwrite')
        p.write_text(json.dumps({'hashes':hashes(),'scope':'Before first local execution; authored design, not independent confirmation','seed':20261022,'replicates_per_generator':12},indent=2)+'\n')
        print('Prepared source and protocol hashes');return
    if hashes()!=json.loads((OUT/'MANIFEST.json').read_text())['hashes']:raise SystemExit('Frozen inputs changed')
    if (OUT/'RESULTS.json').exists():raise SystemExit('Refusing overwrite')
    start=time.monotonic();rng=np.random.default_rng(20261022);rows=[];testk=np.array([4,6,8,10]);testN=200000
    for name in ['separated','close','collision','single','misspecified']:
        for rep in range(12):
            testtrue=.5+curve(name,testk);testcounts=rng.binomial(testN,testtrue);testobs=testcounts/testN
            row={'generator':name,'replicate':rep,'heldout_counts':testcounts.tolist(),'heldout_N_per_k':testN,'fits':{}}
            for arm,k,N in [('sparse',np.array([0,1,2,3]),300000),('dense',np.array([0,1,2,3,5,7]),200000)]:
                truth=.5+curve(name,k);counts=rng.binomial(N,truth);y=counts/N-.5
                row[arm+'_measurements']={'k':k.tolist(),'N_per_k':N,'counts':counts.tolist()}
                one=fit(k,y,False);two=fit(k,y,True,one)
                for order,fitted in [('one',one),('two',two)]:
                    pred=.5+predict(fitted['parameters'],testk,order=='two')
                    fitted['heldout_predictions']=pred.tolist()
                    fitted['heldout_expected_brier_regret']=float(np.mean((pred-testtrue)**2))
                    fitted['heldout_empirical_brier']=float(np.mean(pred**2+(1-2*pred)*testobs))
                    if order=='two' and name in ['separated','close']:
                        A,q,a,b=fitted['parameters'];slow=A*q if a>=b else A*(1-q)
                        fitted['slow_amplitude_error']=abs(slow-.128)
                    row['fits'][arm+'_'+order]=fitted
            rows.append(row)
        print('Completed '+name,flush=True)
    summary={}
    for name in ['separated','close','collision','single','misspecified']:
        subset=[r for r in rows if r['generator']==name];stats={}
        for key in ['sparse_one','sparse_two','dense_one','dense_two']:
            fits=[r['fits'][key] for r in subset]
            stats[key]={'mean_heldout_expected_brier_regret':float(np.mean([f['heldout_expected_brier_regret'] for f in fits])),
                        'mean_heldout_empirical_brier':float(np.mean([f['heldout_empirical_brier'] for f in fits])),
                        'unsuccessful_optimizer_starts':sum(not a['success'] for f in fits for a in f['attempts'])}
            if 'slow_amplitude_error' in fits[0]:stats[key]['median_slow_amplitude_error']=float(np.median([f['slow_amplitude_error'] for f in fits]))
        stats['dense_two_better_than_dense_one_replicates']=sum(r['fits']['dense_two']['heldout_expected_brier_regret']<r['fits']['dense_one']['heldout_expected_brier_regret'] for r in subset)
        stats['dense_two_better_than_sparse_two_replicates']=sum(r['fits']['dense_two']['heldout_expected_brier_regret']<r['fits']['sparse_two']['heldout_expected_brier_regret'] for r in subset)
        summary[name]=stats
    cal=calibration()
    checks={'calibration_witnesses':all(cal['checks'].values()),'training_budget_equal':4*300000==6*200000,
            'train_test_k_disjoint':not(set([0,1,2,3,5,7])&set(testk)),
            'two_nested_train_loss_not_worse':all(r['fits'][a+'_two']['train_SSE']<=r['fits'][a+'_one']['train_SSE']+1e-15 for r in rows for a in ['sparse','dense']),
            'predictions_valid':all(0.5-1e-12<=x<=1+1e-12 for r in rows for f in r['fits'].values() for x in f['heldout_predictions']),
            'source_protocol_unchanged':hashes()==json.loads((OUT/'MANIFEST.json').read_text())['hashes']}
    result={'scope':'Two constructed contacts; finite seeded fits, held-out measurements and known-generator scoring; no carrier proof or general efficacy',
            'elapsed_seconds':time.monotonic()-start,'calibration':cal,'summary':summary,'rows':rows,'checks':checks}
    (OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':checks,'summary':summary,'elapsed_seconds':result['elapsed_seconds']},indent=2))
    if not all(checks.values()):raise SystemExit('Check failed; preserve output')

if __name__=='__main__':main()
