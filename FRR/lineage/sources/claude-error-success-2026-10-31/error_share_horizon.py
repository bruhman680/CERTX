"""
FOLLOW-UP (added AFTER seeing that P1 failed in error_vs_success_info.py; predictions written before running this file):
Error-step share of cumulative KL as a function of window length n (1..22), for each ordered pair.
 F1 For truth EC (EC->SH, EC->WK) the error share starts above .5 and crosses below .5 somewhere in n=7..12 (successes accumulate evidence that no cluster-persistence exists).
 F2 For truth SH or WK against EC, error share stays above .75 at every n>=4 (the difference is cluster-after-error, which is error-centered).
 F3 For SH->WK the error share exceeds 1 (success part negative) from some n<=14 and for WK->SH the error share is negative or small by n=12.
Interpretation guard: share is a decomposition of an expected log-likelihood ratio by outcome type under the TRUE world; it says where evidence arrives, not that an error-driven learner would do better.
"""
import sys; sys.argv=['x']
import io, contextlib
SD='/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad/err_relay/'
src=open(SD+'error_vs_success_info.py').read().split('print("A) chain-rule')[0]
ns={}
with contextlib.redirect_stdout(io.StringIO()): exec(src,ns)
split_kl=ns['split_kl']; import itertools
print("n:      "+" ".join(f"{n:5d}" for n in range(2,23,2)))
sh={}
for P,Q in itertools.permutations(('SH','EC','WK'),2):
    row=[]
    for n in range(2,23,2):
        t,o,_=split_kl(P,Q,n); kl=t[0]+t[1]; row.append(t[1]/kl if abs(kl)>1e-9 else float('nan'))
    sh[(P,Q)]=row; print(f"{P}->{Q}: "+" ".join(f"{x:5.2f}" for x in row))
def cross(row):
    for n,x in zip(range(2,23,2),row):
        if x<.5: return n
    return None
print("F1 crossings below .5:", {k:cross(sh[k]) for k in (('EC','SH'),('EC','WK'))})
print("F2 min share n>=4:", {k:round(min(x for n,x in zip(range(2,23,2),sh[k]) if n>=4),2) for k in (('SH','EC'),('WK','EC'))})
print("F3 SH->WK first n with share>1:", next((n for n,x in zip(range(2,23,2),sh[('SH','WK')]) if x>1),None)," WK->SH share at n=12:",round(sh[('WK','SH')][5],2))
