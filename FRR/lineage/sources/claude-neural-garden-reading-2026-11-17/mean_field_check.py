# Independent check of NEURAL_GARDEN_V01/MEAN_FIELD_BOUND.md (branch codex/frr-v05-explorations, commit 3204c81e).
import numpy as np, math
from scipy.optimize import minimize_scalar
a,b=.06,.18
r=lambda p:a/(a+b*p)
dE=lambda p:.25*r(p)*p-.03-.055*p+.008*(1-p)
dE2=lambda p:.015*p/(.06+.18*p)-.063*p-.022
ps=np.linspace(0,1,100001)
print("max |dE-dE2| over grid:",np.abs(dE(ps)-dE2(ps)).max())
res=minimize_scalar(lambda p:-dE(p),bounds=(0,1),method='bounded',options={'xatol':1e-10})
print("argmax p=%.4f r*=%.4f maxdrift=%.6f"%(res.x,r(res.x),dE(res.x)))
p_cf=(math.sqrt(.015*.06/.063)-.06)/.18; print("closed-form p*=%.4f drift %.6f"%(p_cf,dE(p_cf)))
rng=np.random.default_rng(0); R=rng.beta(2,2,10**6)
for th in (.3,.55,.7):
    A=(R>th).astype(float); lhs=(.25*R*A-.063*A-.022).mean()
    rhs=.25*(R.mean()*A.mean()+np.cov(R,A)[0,1])-.063*A.mean()-.022
    print("covariance identity, theta",th,"lhs %.6f rhs %.6f"%(lhs,rhs))
