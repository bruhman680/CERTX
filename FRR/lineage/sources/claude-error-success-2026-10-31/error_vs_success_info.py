"""
ERROR vs SUCCESS INFORMATION: where does the evidence that separates worlds live -- after/at errors or after/at successes -- and is that valence or rarity?
Motivation (Thomas, 2026-10-31): "a form of reasoning that learns more from errors than successes". I could not find this named form in the repo (ChatGPT-side work may not be pushed).
So this tests a NARROW operational reading only: evidence increments about WORLD IDENTITY, split by outcome type. Not a test of any reasoning form, agent, or FRR.
Worlds SH/EC/WK from soil_toy.py (executed unchanged), rate .2, lag-1 cov .032. Exact enumeration, no sampling.

Measures
 A) Chain-rule split of KL(P||Q) over length-n words (stationary start): sum_t E_P[log P(o_t|past)/Q(o_t|past)] split by o_t = error vs success. 'per-event intensity' = split / P(that outcome type).
 B) Intervention split: Chernoff C of DO_F (force error, then watch 5) vs DO_S (force success, then watch 5), from the soil_budget laws.
 C) Rate sweep, analytic, EC vs IND(r) with p = r(1-c)+c*last, c=.2 fixed: share of KL rate carried by steps right AFTER an error vs after a success, r in {.05,.2,.5,.8,.95}.

PREDICTIONS (written before running):
 P1 (A) For all three ordered pairs, error steps carry > 60% of the cumulative KL at n=12, and per-event intensity of an error step is > 3x that of a success step.
 P2 (A) SH-vs-WK is the exception to 'gains come early': its KL keeps growing with n at a roughly constant per-step rate beyond n=6 (not saturating), unlike EC-involving pairs which saturate by n~6.
 P3 (B) C(DO_F) > C(DO_S) for every pair; for SH-WK the ratio is >= 5.
 P4 (C) share-after-error at r=.2 is about .765 (hand calc), exactly .5 at r=.5, and share(r) + share(1-r) = 1 (valence symmetry). So the asymmetry tracks RARITY of the event, not its being an error.
 P5 (C) share-after-error rises monotonically as r falls, above .9 at r=.05.
 Not tested: real agents, unknown worlds, learners that must discover the worlds, any claim that an error-driven learner generalizes better.
"""
import io, contextlib, itertools, numpy as np
from scipy.optimize import minimize_scalar
SD='/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad/'
src=open(SD+'soil_relay/soil_toy.py').read().split('# passive TV between worlds')[0]
ns={}
with contextlib.redirect_stdout(io.StringIO()): exec(src,ns)
build,stationary,W,idx,NS=ns['build'],ns['stationary'],ns['W'],ns['idx'],ns['NS']
WORLDS=('SH','EC','WK')
def kern(w):
    M,D,pv=build(w,**W[w]); return M,stationary(M[0]+M[1])
K={w:kern(w) for w in WORLDS}
def prefix_probs(w,n):
    M,pi=K[w]; levels=[]; cur=pi[None,:]
    for t in range(n):
        cur=np.concatenate([cur@M[0],cur@M[1]],axis=0)  # index appends newest symbol as LSB
        levels.append(cur.sum(1))
    return levels
def split_kl(P,Q,n):
    lp=prefix_probs(P,n); lq=prefix_probs(Q,n); tot={0:0.0,1:0.0}; occ={0:0.0,1:0.0}; per_t=[]
    prev_p=np.array([1.0]); prev_q=np.array([1.0])
    for t in range(n):
        p=lp[t]; q=lq[t]; pp=np.repeat(prev_p,2); pq=np.repeat(prev_q,2); last=np.arange(len(p))%2
        # symbol index: word index = 2*prefix_index + last
        cp=p/pp; cq=q/pq; contrib=p*np.log(cp/cq)
        for o in (0,1):
            m=last==o; tot[o]+=contrib[m].sum(); occ[o]+=p[m].sum()
        per_t.append((contrib[last==1].sum(),contrib[last==0].sum()))
        prev_p,prev_q=p,q
    return tot,occ,per_t
print("A) chain-rule KL(P||Q) split by outcome at step t (nats), cumulative to n; share from error steps; per-event intensity ratio (error/success)")
print(f"{'P':3s} {'Q':3s} {'n':>3s} {'KL':>9s} {'err':>9s} {'succ':>9s} {'err share':>9s} {'intens ratio':>12s}")
res={}
for P,Q in itertools.permutations(WORLDS,2):
    for n in (6,12):
        tot,occ,per_t=split_kl(P,Q,n); kl=tot[0]+tot[1]
        ir=(tot[1]/occ[1])/(tot[0]/occ[0]) if tot[0]>0 else float('nan')
        res[(P,Q,n)]=(kl,tot[1]/kl,ir)
        print(f"{P:3s} {Q:3s} {n:3d} {kl:9.5f} {tot[1]:9.5f} {tot[0]:9.5f} {tot[1]/kl:9.3f} {ir:12.2f}")
print("   P1: error share >.6 and intensity ratio >3 in every row:", all(v[1]>.6 and v[2]>3 for v in res.values()))
print("   (note: success-step contribution can be NEGATIVE in a row; an error-share above 1 means successes push toward the wrong world on average under P.)")
print("\nA2) per-step KL increments (error part, success part), SH->WK and WK->SH and EC->WK, t=1..16 (cumulative-gain growth check, P2)")
for P,Q in (('SH','WK'),('WK','SH'),('EC','WK'),('SH','EC')):
    _,_,pt=split_kl(P,Q,16); inc=[a+b for a,b in pt]
    print(f"  {P}->{Q}: "+" ".join(f"{x:.4f}" for x in inc))
# B) Chernoff for DO_F vs DO_S
RA=None
def forced(world,kw,o):
    u=kw.get('u',0.0); d=kw.get('d',0.0); T=np.zeros((NS,NS))
    for (s,l),i in idx.items():
        if world=='WK':
            nxt=({1:1.0} if s==1 else {1:u,0:1-u}) if o==1 else ({0:1.0} if s==0 else {0:d,1:1-d})
        else: nxt={s:1.0}
        for s2,ps in nxt.items(): T[i,idx[(s2,o)]]+=ps
    return T
def law(world,o,n=5):
    M,pi=K[world]; v=pi@forced(world,W[world],o); out=[]
    for w in itertools.product((0,1),repeat=n):
        x=v.copy()
        for q in w: x=x@M[q]
        out.append(x.sum())
    return np.array(out)
def chern(p,q):
    r=minimize_scalar(lambda l: np.log(np.sum(np.exp(l*np.log(p)+(1-l)*np.log(q)))),bounds=(0,1),method='bounded',options={'xatol':1e-12}); return -r.fun
print("\nB) Chernoff C per episode: force error (DO_F) vs force success (DO_S), observe 5 after")
okB=True
for a,b in (('SH','EC'),('SH','WK'),('EC','WK')):
    cf=chern(law(a,1),law(b,1)); cs=chern(law(a,0),law(b,0)); okB&=cf>cs
    print(f"  {a}-{b}: C(DO_F)={cf:.5f}  C(DO_S)={cs:.6f}  ratio {cf/cs:.1f}")
print("   P3: DO_F > DO_S for every pair:",okB)
# C) rate sweep EC vs IND
def kl_b(p,q): return p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q))
c=.2; print("\nC) EC vs IND(r), c=.2: share of KL rate from steps right after an error")
sh={}
for r in (.05,.2,.35,.5,.65,.8,.95):
    a=r*kl_b(r*(1-c)+c,r); b=(1-r)*kl_b(r*(1-c),r); sh[r]=a/(a+b)
    print(f"  r={r:.2f}: share after error {sh[r]:.3f}   (after success {1-sh[r]:.3f})")
print("   P4 sym check max|share(r)+share(1-r)-1| =",max(abs(sh[r]+sh[round(1-r,2)]-1) for r in sh),"  share(.2)=",round(sh[.2],3))
print("   P5 monotone falling in r:", all(sh[x]>sh[y] for x,y in zip(sorted(sh),sorted(sh)[1:])), " share(.05)=",round(sh[.05],3))
