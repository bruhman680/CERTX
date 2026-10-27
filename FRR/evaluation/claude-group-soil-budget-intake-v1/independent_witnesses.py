"""Elementary new rational ensemble and design witnesses; no soil-model imports."""
from fractions import Fraction as F
from itertools import combinations
from math import comb, log, sqrt
from pathlib import Path
import json

def moment(levels,k):
    return sum(w*p**k for w,p in levels)

def majority(n,levels):
    return sum(w*sum(F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(n//2+1,n+1)) for w,p in levels)

def main():
    symmetric=[(F(1,2),F(1,50)),(F(1,2),F(19,50))]
    asymmetric=[(F(81,106),F(1,10)),(F(25,106),F(131,250))]
    a,b=symmetric,asymmetric
    assert moment(a,1)==moment(b,1)==F(1,5)
    va=moment(a,2)-moment(a,1)**2;vb=moment(b,2)-moment(b,1)**2
    assert va==vb==F(81,2500)
    assert moment(a,3)!=moment(b,3)
    table=[]
    for n in (3,9,31,101):
        x,y=majority(n,a),majority(n,b)
        table.append({'n':n,'symmetric_exact':str(x),'asymmetric_exact':str(y),'symmetric_float':float(x),'asymmetric_float':float(y)})
    # Conditional iid law of large numbers gives these limits; not estimated from n=101.
    floors=[sum(w for w,p in v if p>F(1,2)) for v in (a,b)]
    assert floors==[0,F(25,106)]
    # Direct diagnosis of the deposited rounded code's moment equality claim.
    rounded=[(F(1,2),F('0.0211')),(F(1,2),F('0.3789'))]
    original_asym=[(F(16,21),F(1,10)),(F(5,21),F(13,25))]
    rvar=moment(rounded,2)-F(1,5)**2
    assert rvar-F('0.032')==F('0.00000521')
    assert moment(original_asym,2)-F(1,5)**2==F('0.032')
    # Three candidates, two fixed-allocation designs. A and B have different blind pairs.
    designs={'A':{'H1':F(1,10),'H2':F(9,10),'H3':F(1,10)},
             'B':{'H1':F(1,10),'H2':F(1,10),'H3':F(9,10)}}
    # Any differing Bernoulli pair here is .1 vs .9: Chernoff optimum s=.5,
    # coefficient=2 sqrt(.1*.9)=.6 exactly. Identical pairs give C=0.
    c=log(5/3)
    pair_cs={name:{f'{x}-{y}':(0.0 if probs[x]==probs[y] else c) for x,y in combinations(probs,2)} for name,probs in designs.items()}
    fixed_half={p:(pair_cs['A'][p]+pair_cs['B'][p])/2 for p in pair_cs['A']}
    assert min(pair_cs['A'].values())==min(pair_cs['B'].values())==0
    assert min(fixed_half.values())>0
    # A random labeled arm per episode has arithmetic mixing inside log, rather
    # than the geometric product for a fixed number of episodes in each arm.
    random_half_blind_pair=-log((1+.6)/2)
    assert random_half_blind_pair<c/2
    out={'scope':'Independent elementary constructions; exact Fraction moments/vote probabilities; logarithmic design exponents displayed as floats; no real-agent or finite-sample result',
         'matched_moment_example':{'symmetric_levels':[[str(w),str(p)] for w,p in a],'asymmetric_levels':[[str(w),str(p)] for w,p in b],
                                 'shared_mean':str(moment(a,1)),'shared_covariance':str(va),'third_moments':[str(moment(a,3)),str(moment(b,3))],
                                 'majority_rows':table,'conditional_iid_large_n_limits':[str(v) for v in floors]},
         'original_rounded_code':{'symmetric_covariance':str(rvar),'asymmetric_covariance':str(F('0.032')),'difference':str(F('0.00000521'))},
         'mixture_counterexample':{'per_design_pair_exponents':pair_cs,'fixed_half_pair_exponents':fixed_half,
                                  'pure_worst_pair_exponents':[0,0],'fixed_half_worst_pair_exponent':min(fixed_half.values()),
                                  'random_labeled_half_worst_pair_exponent':random_half_blind_pair,
                                  'fixed_half_worst_pair_exact_formula':'(1/2)*ln(5/3)','random_labeled_half_exact_formula':'ln(5/4)',
                                  'interpretation':'Per-pair C_mix<=weighted arm C does not forbid maximin benefit across different bottleneck pairs. Fixed-count and randomized labeled-arm protocols are distinct.'}}
    target=Path(__file__).with_name('INDEPENDENT_WITNESSES.json');target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'shared_mean':str(moment(a,1)),'shared_covariance':str(va),'majority_limits':[str(v) for v in floors],
                      'rounded_covariance_difference':str(F('0.00000521')),'pure_worst_pair_exponents':[0,0],
                      'fixed_half_worst_pair_exponent':min(fixed_half.values()),'random_labeled_half_worst_pair_exponent':random_half_blind_pair},indent=2))

if __name__=='__main__': main()
