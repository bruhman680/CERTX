"""Analytic Cauchy-Schwarz envelope, not a repaired optimizer."""
b1,b2=.9,.999
for t in [1,10,100,10000]:
    factor=((1-b1)/(1-b1**t))**2/((1-b2)/(1-b2**t))
    bound=factor*(1-(b1*b1/b2)**t)/(1-b1*b1/b2)
    print(t,bound)
print('asymptotic envelope',(1-b1)**2/(1-b2)/(1-b1*b1/b2))
