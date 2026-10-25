"""Independent check of the post's identity S = R/2 + R^2*c/2, using numpy + exact Fractions (not the post's code).
Predictions (before running): (1) identity holds to ~1e-15 on random complex vectors incl. unequal norms;
(2) post's worked examples: .72, .08, 1210/10201, ranking reversal at unequal norms;
(3) with R constant across candidates, rankings equal cosine rankings; with varying R they can differ;
(4) bounds R(1-R)/2 <= S <= R(1+R)/2; (5) single-coordinate closed form in t, delta."""
import numpy as np
from fractions import Fraction as Fr
rng = np.random.default_rng(777)
def S(z, w):
    ez, ew = np.sum(abs(z)**2), np.sum(abs(w)**2); R = 2*np.sqrt(ez*ew)/(ez+ew)
    return 0.5*np.sum(abs(z+w)**2)/(ez+ew)*R
def parts(z, w):
    u = np.r_[z.real, z.imag]; v = np.r_[w.real, w.imag]
    c = u@v/np.sqrt((u@u)*(v@v)); R = 2*np.sqrt((u@u)*(v@v))/((u@u)+(v@v)); return c, R
mx = 0; bmx = 0
for d in (1, 3, 8, 50):
    for _ in range(2000):
        z = rng.normal(size=d)+1j*rng.normal(size=d); w = np.exp(rng.normal())*(rng.normal(size=d)+1j*rng.normal(size=d))
        c, R = parts(z, w); s = S(z, w); mx = max(mx, abs(s-(R/2+R*R*c/2)))
        lo, hi = R*(1-R)/2, R*(1+R)/2; bmx = max(bmx, lo-s, s-hi)
print(f"(1) max |S - (R/2 + R^2 c/2)| over 8000 random pairs (norm ratios e^N(0,1)): {mx:.2e}")
print(f"(4) max bound violation (<=0 means none): {bmx:.2e}")
# (2) exact examples with Fractions: scalar real case u=1, v=a
def Sx(a):
    a = Fr(a); R = 2*abs(a)/(1+a*a)          # scalar real case: u=1, v=a
    return Fr(1, 2)*(1+a)**2/(1+a*a)*R
print("(2) exact: S(1,2)=", Sx(2), " S(1,-2)=", Sx(-2), " S(1,10)=", Sx(10), "=", float(Sx(10)),
      "| orthogonal equal-norm S=1/2 -> ranks B above A:", Sx(10) < Fr(1, 2))
# (3) ranking: equal-norm candidates -> same order as cosine; varying norms -> can differ
q = rng.normal(size=6)+1j*rng.normal(size=6)
def order(cands, f): return list(np.argsort([-f(q, x) for x in cands]))
cos = lambda z, w: parts(z, w)[0]
eq = []
for _ in range(50):
    x = rng.normal(size=6)+1j*rng.normal(size=6); eq.append(x/np.sqrt(np.sum(abs(x)**2))*3.0)
vr = [x*np.exp(rng.normal()) for x in eq]
print("(3) equal-norm candidates: same ranking as cosine:", order(eq, S) == order(eq, cos),
      "| varying norms: same ranking as cosine:", order(vr, S) == order(vr, cos))
# (5) single coordinate closed form
t, dl = 1.7, 0.9; z = np.array([1+0j]); w = np.array([t*np.exp(1j*dl)])
print("(5) closed form check:", abs(S(z, w) - t*(1+t*t+2*t*np.cos(dl))/(1+t*t)**2))
# the unknown-vs-zero and cancellation witnesses
print("cancellation: sum(z, -z) =", (z + (-z)).sum(), "equals sum of empty set =", 0, "(same aggregate, different history)")
