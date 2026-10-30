"""Exact finite-distribution toy calculations; see frozen PROTOCOL.md."""
from pathlib import Path
from itertools import product
from math import comb, sqrt, lgamma, exp
import json, hashlib
import numpy as np

ROOT=Path(__file__).resolve().parent
R=.2; V=.032; LEVELS=(R-sqrt(V),R+sqrt(V)); TOL=1e-11
CHECKS=[]
def check(name, value):
    CHECKS.append({'name':name,'pass':bool(value)})
    if not value: raise AssertionError(name)
def beta(a,b): return exp(lgamma(a)+lgamma(b)-lgamma(a+b))
def word_prob(n,s,kind):
    if kind=='two_point': return sum(p**s*(1-p)**(n-s) for p in LEVELS)/2
    return beta(.8+s,3.2+n-s)/beta(.8,3.2)
def counts(n,kind):
    a=np.array([comb(n,s)*word_prob(n,s,kind) for s in range(n+1)])
    check(f'law_{kind}_{n}',abs(a.sum()-1)<TOL and a.min()>=0)
    return a

def cycle1():
    rows=[]
    for n in (1,2,4,8,16,32,64):
        k=64//n; law=np.array([1.])
        for _ in range(k): law=np.convolve(law,counts(n,'two_point'))
        x=np.arange(65)/64; mean=float(law@x)
        var=float(law@((x-R)**2)); analytic=V/k+(R*(1-R)-V)/64
        naive=R*(1-R)/64
        coverage=float(law[np.abs(x-R)<=1.96*sqrt(naive)].sum())
        check(f'cluster_variance_n{n}',abs(var-analytic)<TOL and abs(mean-R)<TOL)
        check(f'cluster_normalization_n{n}',abs(law.sum()-1)<TOL)
        rows.append(dict(observations_per_soil=n,independent_soils=k,variance=var,analytic_variance=analytic,naive_variance=naive,variance_inflation=var/naive,effective_iid_sample_size=R*(1-R)/var,fixed_iid_interval_coverage=coverage))
    return rows

def cycle2():
    rows=[]
    for n in (1,2,3,4,8,16,32,64):
        a=counts(n,'two_point'); b=counts(n,'beta'); tv=float(abs(a-b).sum()/2)
        check(f'moment_prediction_n{n}',tv<TOL if n<=2 else tv>TOL)
        if n<=8:
            wordtv=sum(abs(word_prob(n,sum(w),'two_point')-word_prob(n,sum(w),'beta')) for w in product((0,1),repeat=n))/2
            check(f'word_vs_count_tv_n{n}',abs(tv-wordtv)<TOL)
        rows.append(dict(length=n,TV=tv,equal_prior_Bayes_error=(1-tv)/2))
    a=counts(16,'two_point'); b=counts(16,'beta')
    pa=pb=np.array([1.])
    for _ in range(4): pa=np.outer(pa,a).ravel(); pb=np.outer(pb,b).ravel()
    tv=float(abs(pa-pb).sum()/2)
    check('four_soils_normalization',abs(pa.sum()-1)<TOL and abs(pb.sum()-1)<TOL)
    return dict(one_soil=rows,four_independent_soils_16_each=dict(count_vectors=len(pa),TV=tv,equal_prior_Bayes_error=(1-tv)/2))

def joint(pi,qa,qs,action):
    out=np.zeros((2,2))
    for internal in (False,True):
        carrier_weight=pi if internal else 1-pi
        efficacy=(qa if internal and action=='agent' else qs if not internal and action=='soil' else 0)
        for old,fresh in product((0,1),repeat=2):
            p1=LEVELS[old]
            for redraw in (False,True):
                weight=carrier_weight*.5*.5*(efficacy if redraw else 1-efficacy)
                p2=LEVELS[fresh if redraw else old]
                out+=weight*np.outer([1-p1,p1],[1-p2,p2])
    return out

def cycle3():
    rows=[]
    for pi,qa,qs in ((.4,.5,.75),(.25,.8,.6),(.5,.4,.9),(.4,1,1),(.4,0,0)):
        ds={}; matrices={}
        for action,expected in [('none',.16),('agent',.16*(1-pi*qa)),('soil',.16*(1-(1-pi)*qs))]:
            law=joint(pi,qa,qs,action); d=law[1,1]/law[1].sum()-R
            check(f'reset_law_{pi}_{qa}_{qs}_{action}',abs(law.sum()-1)<TOL and law.min()>=0 and abs(d-expected)<TOL)
            ds[action]=float(d); matrices[action]=law.tolist()
        a=1-ds['agent']/ds['none']; s=1-ds['soil']/ds['none']
        interval=[float(max(0,a)),float(min(1,1-s))]
        check(f'feasible_pi_{pi}_{qa}_{qs}',interval[0]-TOL<=pi<=interval[1]+TOL)
        recovered=None if qa==0 or qs==0 else [a/qa,1-s/qs]
        if recovered: check(f'known_calibration_{pi}_{qa}_{qs}',max(abs(x-pi) for x in recovered)<TOL)
        rows.append(dict(pi=pi,q_agent=qa,q_soil=qs,excess=ds,unknown_calibration_pi_interval=interval,known_calibration_pi_reconstructions=recovered,joint=matrices))
    for row in rows[1:3]:
        check(f'rival_same_readouts_{row["pi"]}',max(abs(row['excess'][a]-rows[0]['excess'][a]) for a in rows[0]['excess'])<TOL)
    check('passive_internal_external_equivalent',np.max(abs(joint(1,1,1,'none')-joint(0,1,1,'none')))<TOL)
    return rows

def main():
    freeze=json.loads((ROOT/'FREEZE.json').read_text())
    for name,h in freeze.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h: raise RuntimeError('Changed frozen input: '+name)
    result={'scope':'authored finite-distribution toys; no actual agent evidence','cycle1':cycle1(),'cycle2':cycle2(),'cycle3':cycle3(),'checks':CHECKS,'numpy':np.__version__}
    with (ROOT/'RESULTS.json').open('x') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps({'checks':len(CHECKS),'all_pass':all(c['pass'] for c in CHECKS),'cycle1':result['cycle1'],'cycle2':result['cycle2'],'cycle3_summary':[{k:v for k,v in r.items() if k!='joint'} for r in result['cycle3']]},indent=2))
if __name__=='__main__': main()
