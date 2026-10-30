"""Post-result exact rational check, not an independent reviewer/replication."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
R=F(1,5); V=F(4,125)
def moment_two(k):
    return sum(F(comb(k,j))*R**(k-j)*V**(j//2) for j in range(0,k+1,2))
def moment_beta(k):
    a=F(1)
    for j in range(k): a*= (F(4,5)+j)/(4+j)
    return a
def count(n,s,moment):
    return comb(n,s)*sum((-1)**j*comb(n-s,j)*moment(s+j) for j in range(n-s+1))
rows=[]
for n in (1,2,3,4,8):
    a=[count(n,s,moment_two) for s in range(n+1)]
    b=[count(n,s,moment_beta) for s in range(n+1)]
    assert sum(a)==sum(b)==1 and min(a+b)>=0
    tv=sum(abs(x-y) for x,y in zip(a,b))/2
    assert (tv==0)==(n<=2)
    rows.append({'n':n,'TV_fraction':str(tv),'TV':float(tv)})
D=V/R
reset=[]
for pi,qa,qs in [(F(2,5),F(1,2),F(3,4)),(F(1,4),F(4,5),F(3,5)),(F(1,2),F(2,5),F(9,10))]:
    ds=[D,D*(1-pi*qa),D*(1-(1-pi)*qs)]
    assert ds==[F(4,25),F(16,125),F(11,125)]
    a=1-ds[1]/ds[0]; s=1-ds[2]/ds[0]
    assert a==F(1,5) and 1-s==F(11,20)
    reset.append({'pi':str(pi),'readouts':list(map(str,ds)),'feasible_pi':['1/5','11/20']})
out={'scope':'post-result coordinator exact-arithmetic audit','rival_counts':rows,'reset_identities':reset}
p=Path(__file__).resolve().parent
with (p/'RATIONAL_AUDIT.json').open('x') as f: json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
