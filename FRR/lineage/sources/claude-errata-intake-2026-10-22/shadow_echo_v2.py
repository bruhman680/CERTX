import itertools, numpy as np
rng = np.random.default_rng(0)
# K[e][y] -> distribution over next y (same table as original experiment)
K = np.array([[[.85,.15],[.10,.90]],
              [[.55,.45],[.40,.60]]])

def word_law(n, wiring, e_mode):
    """Exact law over visible words of length n.
    wiring: 'frozen' (shadow, e const) | 'echo' (e_t = y_{t-1})
    e_mode: None (natural) | 'iid' (do: e resampled Bernoulli(.5) each step)
            | 'echo' (do: e_t := y_{t-1}) | ('const',c)
    Initial: y0 uniform; e0 uniform."""
    law = {}
    for w in itertools.product([0,1], repeat=n):
        tot = 0.0
        for e0 in (0,1):
            p = 0.25 if False else 0.5*0.5  # y0 uniform, e0 uniform
            e = e0
            for t in range(1,n):
                y_prev = w[t-1]
                if e_mode is None:
                    e_use = e
                elif e_mode == 'iid':
                    e_use = None
                elif e_mode == 'echo':
                    e_use = w[t-2] if t>=2 else e0
                else:
                    e_use = e_mode[1]
                if e_use is None:
                    pt = 0.5*K[0][y_prev][w[t]] + 0.5*K[1][y_prev][w[t]]
                else:
                    pt = K[e_use][y_prev][w[t]]
                p *= pt
                if wiring == 'echo' and e_mode is None:
                    e = y_prev
            tot += p
        law[w] = tot
    return law

def tv(a,b): return 0.5*sum(abs(a[k]-b[k]) for k in a)

print("== 1. passive visible-word law, y0 and e0 uniform ==")
for n in (2,3,4,6,8,10):
    S = word_law(n,'frozen',None); E = word_law(n,'echo',None)
    print(f" n={n:2d}  TV(shadow,echo)={tv(S,E):.4f}")

print("\n== 2. is each visible process Markov-1? max|P(y2|y1,y0)-P(y2|y1)| ==")
def cond_gap(law3):
    gap=0
    for y1 in (0,1):
        for y2 in (0,1):
            c=[law3[(y0,y1,y2)]/sum(law3[(y0,y1,z)] for z in (0,1)) for y0 in (0,1)]
            gap=max(gap,abs(c[0]-c[1]))
    return gap
S3=word_law(3,'frozen',None); E3=word_law(3,'echo',None)
print(f" shadow order-2 gap={cond_gap(S3):.4f}   echo order-2 gap={cond_gap(E3):.4f}")
print(" -> shadow also looks history-dependent passively (Bayesian inference of e)")

print("\n== 3. Hankel rank of word laws (prefix/suffix len<=3) ==")
def hankel(wiring):
    L=7
    law=word_law(L,wiring,None)
    words=[w for k in range(0,4) for w in itertools.product([0,1],repeat=k)]
    def prob(u):  # marginal of word u at positions 0..len-1 (start-aligned)
        k=len(u)
        return sum(v for w,v in law.items() if w[:k]==u)
    def prob_uv(u,v):
        k=len(u)+len(v)
        return sum(p for w,p in law.items() if w[:k]==tuple(u)+tuple(v))
    H=np.array([[prob_uv(u,v) for v in words] for u in words])
    return np.linalg.matrix_rank(H,tol=1e-9)
print(f" rank shadow={hankel('frozen')}  rank echo={hankel('echo')}")

print("\n== 4. long-run switch-rate bimodality (per-trajectory, T=4000, 400 runs) ==")
def sim(wiring,T=4000):
    e0=rng.integers(2); y=rng.integers(2); e=e0; sw=0
    for t in range(T):
        y2=rng.choice(2,p=K[e][y]); sw+= (y2!=y)
        if wiring=='echo': e=y
        y=y2
    return sw/T
for w in ('frozen','echo'):
    r=np.array([sim(w) for _ in range(400)])
    h=np.histogram(r,bins=np.linspace(0.1,0.5,9))[0]
    print(f" {w:6s} mean={r.mean():.3f} sd={r.std():.3f} hist(0.1..0.5)={h.tolist()}")

print("\n== 5. rewiring interventions (TV of law vs own passive law, n=8) ==")
for name,wiring in (('shadow','frozen'),('echo','echo')):
    base=word_law(8,wiring,None)
    for lab,mode in (('do(e~iid fair)','iid'),('do(e_t:=y_{t-1})','echo'),('do(e:=0)',('const',0)),('do(e:=1)',('const',1))):
        print(f" {name:6s} {lab:18s} TV={tv(base,word_law(8,wiring,mode)):.4f}")
print("\n do(e iid) laws equal across models? TV =",
      round(tv(word_law(8,'frozen','iid'),word_law(8,'echo','iid')),6))
