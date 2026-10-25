"""Separate algebraic control and scoped-mixture witnesses; no Claude code imported."""
import cmath
import json
import math
import random
from pathlib import Path

P=Path(__file__).resolve().parent

def compare(z,w):
    x,y=[v.real for v in z],[v.imag for v in z]
    a,b=[v.real for v in w],[v.imag for v in w]
    re=math.fsum(u*v for u,v in zip(x,a))+math.fsum(u*v for u,v in zip(y,b))
    im=math.fsum(u*v for u,v in zip(x,b))-math.fsum(u*v for u,v in zip(y,a))
    direct=sum(u.conjugate()*v for u,v in zip(z,w))
    den=math.sqrt(math.fsum(abs(v)**2 for v in z)*math.fsum(abs(v)**2 for v in w))
    mod=math.hypot(re,im)/den
    angle=math.atan2(im,re) if math.hypot(re,im)>1e-12 else None
    return direct,complex(re,im),mod,angle,den

rng=random.Random(91387)
errors={'inner_product':0.,'modulus':0.,'angle_wrapped':0.}
n=0
for d in (1,3,11,29):
    for _ in range(32):
        z=[complex(rng.gauss(0,1),rng.gauss(0,1)) for i in range(d)]
        w=[complex(rng.gauss(0,1),rng.gauss(0,1)) for i in range(d)]
        h,real_h,m,ang,den=compare(z,w)
        errors['inner_product']=max(errors['inner_product'],abs(h-real_h))
        errors['modulus']=max(errors['modulus'],abs(abs(h)/den-m))
        if ang is not None:
            diff=math.atan2(math.sin(cmath.phase(h)-ang),math.cos(cmath.phase(h)-ang))
            errors['angle_wrapped']=max(errors['angle_wrapped'],abs(diff))
        n+=1

def unit(v):
    norm=math.sqrt(math.fsum(abs(x)**2 for x in v))
    return [x/norm for x in v]

global_rows=[]
for status,phi in [('A',0.),('N',math.pi),('U',math.pi/3)]:
    h,_,m,ang,_=compare([1+0j],[cmath.exp(1j*phi)])
    global_rows.append({'status_codebook_supplied':status,'real_cosine':h.real,'modulus':m,'angle':ang})

scoped=[]
for context,binding in [(.5,1.),(1.,1.),(2.,1.)]:
    q=unit([complex(context),complex(binding)])
    row={'context_amplitude':context,'binding_amplitude':binding,'statuses':{}}
    for status,phi in [('A',0.),('N',math.pi),('U',math.pi/3)]:
        # Use an exact sign for N so a mathematically zero product stays visibly zero.
        ph=-1+0j if status=='N' else cmath.exp(1j*phi)
        w=unit([complex(context),binding*ph])
        h,_,m,ang,_=compare(q,w)
        row['statuses'][status]={'real_cosine':h.real,'imaginary_channel':h.imag,'modulus':m,'angle':ang}
    scoped.append(row)

checks={
 'two_real_bilinear_channels_recover_complex_product':errors['inner_product']<1e-12,
 'real_channels_recover_normalized_modulus':errors['modulus']<1e-12,
 'real_channels_recover_nonzero_angle':errors['angle_wrapped']<1e-12,
 'global_phase_retains_relevance_modulus':all(abs(r['modulus']-1)<1e-12 for r in global_rows),
 'equal_scoped_context_binding_opposition_modulus_zero':scoped[1]['statuses']['N']['modulus']<1e-12,
 'zero_product_angle_not_assigned':scoped[1]['statuses']['N']['angle'] is None,
 'context_dominant_A_N_angle_collision':abs(scoped[2]['statuses']['A']['angle']-scoped[2]['statuses']['N']['angle'])<1e-12,
 'binding_dominant_N_opposes_reference':abs(abs(scoped[0]['statuses']['N']['angle'])-math.pi)<1e-12,
}
out={'scope':'exact algebra plus moderate random formula checks and oracle orthogonal context/binding examples, not end-to-end language retrieval',
     'seed':91387,'random_pairs':n,'max_absolute_errors':errors,'unknown_codebook_phase':'pi/3, supplied not learned',
     'global_rows':global_rows,'scoped_rows':scoped,'checks':checks}
(P/'REAL_CHANNEL_RESULTS.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(out,indent=2,allow_nan=False))
assert all(checks.values())
