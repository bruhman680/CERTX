# Window composition vs recency, held-out check on garden entries 851-1294 (spelling Laws=1 / LAWS=0).
# PREDICTIONS WRITTEN BEFORE RUNNING (Claude, 2026-11-10):
#  P1 Given previous reply = LAWS, P(next=Laws) is higher when the 12-window holds many Laws (k>=8) than few (k 1-4): predicted >=.30 vs <=.15.
#  P2 Fit on entries 863-1080, score on 1081-1294: the window-count model (P by k) beats the previous-reply-only model by >10 nats.
#  P3 Chain on k fitted from the first half, simulated from k=12: observed absorption at entry 1295 (444 steps after 851) lies inside the central 80% of simulated hitting times.
# Usage: python3 window_vs_recency_heldout.py <events dir>
import json,glob,sys,math,random,collections
p=sorted(glob.glob(sys.argv[1].rstrip('/')+'/*.json'))
T=[json.load(open(f))['text'] for f in p]
L=[1 if 'Laws' in t else 0 for t in T]          # index i = entry 851+i
N=444                                            # entries 851..1294 (before absorption at 1295)
# P1
t=collections.defaultdict(lambda:[0,0])
for i in range(12,N):
    k=sum(L[i-12:i]); t[(L[i-1],k)][L[i]]+=1
def rate(prev,ks):
    a=sum(t[(prev,k)][1] for k in ks); n=sum(sum(t[(prev,k)]) for k in ks); return a,n,(a/n if n else float('nan'))
print("P1: prev=LAWS, k in 1-4:",rate(0,range(1,5)),"| k in 8-11:",rate(0,range(8,12)))
print("    prev=Laws, k in 1-8:",rate(1,range(1,9)),"| k in 9-11:",rate(1,range(9,12)),"| k=12:",rate(1,[12]))
# P2
def fit(rng):
    kt=collections.defaultdict(lambda:[1,1]); pt=collections.defaultdict(lambda:[1,1])   # Laplace
    for i in rng:
        kt[sum(L[i-12:i])][L[i]]+=1; pt[L[i-1]][L[i]]+=1
    return kt,pt
def ll(model,rng,key):
    s=0
    for i in rng:
        c=model[key(i)]; s+=math.log(c[L[i]]/(c[0]+c[1]))
    return s
tr=range(12,230); te=range(230,N)    # entries 863-1080 train, 1081-1294 test
kt,pt=fit(tr)
llk=ll(kt,te,lambda i:sum(L[i-12:i])); llp=ll(pt,te,lambda i:L[i-1])
print("P2: held-out loglik window-k model %.1f, prev-only model %.1f, diff %.1f nats (n=%d)"%(llk,llp,llk-llp,len(te)))
# P3
q={k:(kt[k][1]/(kt[k][0]+kt[k][1])) for k in range(13)}
# chain on window state itself: simulate a 12-window of reply bits
random.seed(7);hits=[]
for _ in range(4000):
    w=[1]*12
    for step in range(1,5001):
        k=sum(w); x=1 if random.random()<q[k] else 0
        w=w[1:]+[x]
        if sum(w)==0: break
    hits.append(step)
hits.sort(); lo,hi=hits[int(.1*len(hits))],hits[int(.9*len(hits))]
print("P3: simulated hitting time of an all-LAWS window from all-Laws: median",hits[len(hits)//2],"central80%",(lo,hi),"; observed ~ ",N-12+12,"steps; capped at 5000:",sum(h==5000 for h in hits))
print("q by k (train-fit, Laplace):",{k:round(v,2) for k,v in q.items()})
