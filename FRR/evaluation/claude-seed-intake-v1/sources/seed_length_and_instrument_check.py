"""
SEED LENGTH AND INSTRUMENT CHECK (Claude, 2026-11-05). Two small computations for the numeric-seed redesign. No model involved.
PART A (Occam count): how long must a seed of numbers be before 'a rule fits it' is meaningful? For a hypothesis family F over an alphabet of A values, a uniformly random length-n sequence is 'explained' by some rule with probability |F_n| / A^n, where F_n is the set of distinct length-n sequences the family generates. Exact enumeration.
  Families (alphabet A=100): AFF(M) = x_{k+1}=(a x_k + b) mod m for all 2<=m<=M, 0<=a,b,x0<m.   Also digits (A=10) with M=10.
  PREDICTIONS (before running): A1 AFF(30), A=100: false-rule prob at n=3 between .05 and .25, at n=4 <=.005, n=5 <=1e-4. A2 AFF(60), A=100: n=3 >= .40. A3 digits, AFF(10), A=10: n=4 between .15 and .40 and n=6 < .01. A4 the smallest n with false-rule prob < .05 grows with family size (AFF(60) needs n>=4, AFF(30) n=4 or less).
PART B (instrument check with synthetic agents, to see whether the planned measures can discriminate, i.e. whether the test could fail): seeds of n numbers (values 0..99) from generators SQUARES (k^2 mod 100), FIB (mod 100), PARITY (0,1,0,1..), CONST (7), SHUFFLE (iid uniform). Agents continue the sequence by 8 numbers: COPY (repeats the seed), FLUENT (bigram Markov fit to the seed, ignores rules), RULE (simplest consistent rule from H = {period<=3 with >=2 repeats, constant first difference, constant second difference, Fibonacci-like} mod 100, else falls back to FLUENT), RANDOM (iid).
  Observer measures: copy flag (>=6 of 8 continuation values equal the seed's values in order), rule-consistency = fraction of the 8 matching the TRUE generator's next values (undefined for SHUFFLE), and false-rule rate = fraction of SHUFFLE seeds for which the RULE agent claims a rule.
  PREDICTIONS: B1 COPY copy flag >=.95 on all seeds and rule-consistency near 0 on SQUARES/FIB (<=.1), 1.0 on CONST only by coincidence. B2 FLUENT rule-consistency <.5 on SQUARES and FIB and >=.9 on CONST and PARITY (local patterns). B3 RULE rule-consistency 1.0 on all structured seeds at n=8; its false-rule rate on SHUFFLE is <=.03 at n=4 and <=.001 at n>=6. B4 RANDOM rule-consistency <.05 on all seeds.
Scope: toy agents I wrote and their hypothesis family is my own; this shows what the measures can and cannot separate, not what any model does.
"""
import itertools, numpy as np
rng=np.random.default_rng(20261106)
# ---------- PART A ----------
def aff_seqs(M,n,A):
    S=set()
    for m in range(2,M+1):
        for a in range(m):
            for b in range(m):
                for x0 in range(m):
                    s=[x0]; x=x0
                    for _ in range(n-1): x=(a*x+b)%m; s.append(x)
                    S.add(tuple(s))
    return len(S)
print("PART A: false-rule probability of a uniformly random length-n sequence (exact)")
tab={}
for label,A,M in (("AFF(30) A=100",100,30),("AFF(60) A=100",100,60),("AFF(10) digits A=10",10,10)):
    row=[]
    for n in range(2,9):
        c=aff_seqs(M,n,A); p=c/(A**n); row.append(p); tab[(label,n)]=p
    print(f"  {label:20s} n=2..8: "+" ".join(f"{p:.2e}" for p in row))
for label in ("AFF(30) A=100","AFF(60) A=100","AFF(10) digits A=10"):
    nmin=next((n for n in range(2,9) if tab[(label,n)]<.05),None); print(f"  smallest n with false-rule prob <.05 for {label}: {nmin}")
print(" A1 AFF(30): n=3 %.3f n=4 %.2e n=5 %.2e"%(tab[('AFF(30) A=100',3)],tab[('AFF(30) A=100',4)],tab[('AFF(30) A=100',5)]))
print(" A2 AFF(60) n=3: %.3f"%tab[('AFF(60) A=100',3)])
print(" A3 digits AFF(10): n=4 %.3f n=6 %.4f"%(tab[('AFF(10) digits A=10',4)],tab[('AFF(10) digits A=10',6)]))
# ---------- PART B ----------
def gen(kind,n,rng):
    if kind=='SQUARES': return [(k*k)%100 for k in range(n)]
    if kind=='FIB': 
        s=[0,1]; 
        while len(s)<n: s.append((s[-1]+s[-2])%100)
        return s[:n]
    if kind=='PARITY': return [k%2 for k in range(n)]
    if kind=='CONST': return [7]*n
    return list(rng.integers(0,100,n))
def next_true(kind,n,L):
    return gen(kind,n+L,None)[n:] if kind!='SHUFFLE' else None
def fit_rule(s):
    n=len(s)
    for p in (1,2,3):
        if n>=2*p and all(s[i]==s[i-p] for i in range(p,n)): return ('per',p)
    d=[(s[i]-s[i-1])%100 for i in range(1,n)]
    if len(d)>=3 and len(set(d))==1: return ('d1',d[0])
    if len(d)>=3:
        dd=[(d[i]-d[i-1])%100 for i in range(1,len(d))]
        if len(dd)>=2 and len(set(dd))==1: return ('d2',dd[0])
    if n>=4 and all((s[i]-s[i-1]-s[i-2])%100==0 for i in range(2,n)): return ('fib',0)
    return None
def extend(rule,s,L):
    s=list(s)
    for _ in range(L):
        t,v=rule
        if t=='per': s.append(s[-v])
        elif t=='d1': s.append((s[-1]+v)%100)
        elif t=='d2': d=(s[-1]-s[-2])%100; s.append((s[-1]+d+v)%100)
        else: s.append((s[-1]+s[-2])%100)
    return s[-L:]
def fluent(s,L,rng):
    nxt={}
    for a,b in zip(s,s[1:]): nxt.setdefault(a,[]).append(b)
    out=[]; cur=s[-1]
    for _ in range(L):
        cur=int(rng.choice(nxt[cur])) if cur in nxt else int(rng.integers(0,100)); out.append(cur)
    return out
def agent(name,s,L,rng):
    if name=='COPY': return (list(s)*3)[:L]
    if name=='FLUENT': return fluent(s,L,rng)
    if name=='RANDOM': return [int(x) for x in rng.integers(0,100,L)]
    r=fit_rule(s); return extend(r,s,L) if r else fluent(s,L,rng)
L=8; T=400
print("\nPART B: per agent and seed kind (n=8): copy flag / rule-consistency")
res={}
for name in ('COPY','FLUENT','RULE','RANDOM'):
    row=[]
    for kind in ('SQUARES','FIB','PARITY','CONST','SHUFFLE'):
        cf=[];rc=[]
        for _ in range(T):
            s=gen(kind,8,rng); c=agent(name,s,L,rng)
            cf.append(sum(1 for i in range(L) if c[i]==s[i%len(s)])>=6)
            if kind!='SHUFFLE': rc.append(np.mean([a==b for a,b in zip(c,next_true(kind,8,L))]))
        res[(name,kind)]=(float(np.mean(cf)),float(np.mean(rc)) if rc else None)
        row.append(f"{kind}:{res[(name,kind)][0]:.2f}/"+("-" if not rc else f"{res[(name,kind)][1]:.2f}"))
    print(f"  {name:7s} "+"  ".join(row))
print("\nRULE agent false-rule rate on SHUFFLE seeds by seed length n (20000 seeds each)")
fr={}
for n in (4,5,6,8,12):
    k=sum(fit_rule(list(rng.integers(0,100,n))) is not None for _ in range(20000)); fr[n]=k/20000
    print(f"  n={n:2d}: {fr[n]:.4f}")
print("\nCHECKS")
print(" B1 COPY copy flag min:",round(min(res[('COPY',k)][0] for k in ('SQUARES','FIB','PARITY','CONST','SHUFFLE')),2),"| rule-consistency SQUARES/FIB:",round(res[('COPY','SQUARES')][1],2),round(res[('COPY','FIB')][1],2))
print(" B2 FLUENT rule-consistency SQUARES/FIB:",round(res[('FLUENT','SQUARES')][1],2),round(res[('FLUENT','FIB')][1],2),"| CONST/PARITY:",round(res[('FLUENT','CONST')][1],2),round(res[('FLUENT','PARITY')][1],2))
print(" B3 RULE rule-consistency:",{k:round(res[('RULE',k)][1],2) for k in ('SQUARES','FIB','PARITY','CONST')},"| false-rule n=4 / n>=6:",fr[4],[fr[n] for n in (6,8,12)])
print(" B4 RANDOM rule-consistency:",{k:round(res[('RANDOM',k)][1],3) for k in ('SQUARES','FIB','PARITY','CONST')})
