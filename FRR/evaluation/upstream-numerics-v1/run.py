from pathlib import Path
import json,hashlib,platform
import numpy as np
import mpmath as mp
D=Path(__file__).resolve().parent;mp.mp.dps=100

def native(o):
    if isinstance(o,np.generic):return o.item()
    if isinstance(o,np.ndarray):return o.tolist()
    raise TypeError(type(o).__name__)
def reference(z,t=None,teacher=None):
    a=[mp.mpf(float(x)) for x in z];mx=max(a);e=[mp.exp(x-mx) for x in a];p=[v/sum(e) for v in e]
    if t is not None:return {'loss':float(-mp.log(p[t])),'gradient':np.array([float(v-int(i==t)) for i,v in enumerate(p)])}
    b=[mp.mpf(float(x)) for x in teacher];me=max(b);eb=[mp.exp(x-me) for x in b];pt=[v/sum(eb) for v in eb]
    return np.array([float(x-y) for x,y in zip(p,pt)])
def probabilities(z):
    a=z-z.max();e=np.exp(a);return e/e.sum()
def logprob(z):
    a=z-z.max();return a-np.log(np.exp(a).sum())
def hard(z,t=0):
    dt=z.dtype;d=z-z[t];mask=np.arange(z.size)!=t
    others=np.exp(d[mask]);tail=others.sum();den=np.array(1,dtype=dt)+tail
    p=np.exp(d)/den;std=p.copy();std[t]-=np.array(1,dtype=dt)
    stable=np.zeros_like(z);stable[mask]=others/den;stable[t]=-stable[mask].sum()
    return -logprob(z)[t],std,np.log1p(tail),stable

def soft(z,teacher):
    p=probabilities(teacher);q=np.exp(logprob(z));standard=q-p
    delta=z-teacher;centered=delta-(p*delta).sum()
    ratio=centered-np.log1p((p*np.expm1(centered)).sum())
    u=p*np.expm1(ratio);stable=u-q*u.sum()
    return standard,stable

def main():
    hardrows=[];softrows=[]
    for dt in (np.float32,np.float64):
        for margin in (10,18,40):
            z=np.array([margin,0,0],dtype=dt);loss,g,sloss,sg=hard(z);ref=reference(z,t=0)
            hardrows.append({'dtype':np.dtype(dt).name,'logit_gap':margin,'stored_logits':z,'standard_loss':loss,'stable_loss':sloss,'reference_loss':ref['loss'],'standard_gradient':g,'stable_gradient':sg,'reference_gradient':ref['gradient'],'standard_gradient_sum':g.sum(),'stable_gradient_sum':sg.sum(),'standard_target_relative_error':abs((g[0]-ref['gradient'][0])/ref['gradient'][0]),'stable_target_relative_error':abs((sg[0]-ref['gradient'][0])/ref['gradient'][0]),'stable_loss_relative_error':abs((sloss-ref['loss'])/ref['loss'])})
        for delta in (0,1e-7,1e-5):
            t=np.array([2,1,0],dtype=dt);z=t+np.array([-delta,delta,0],dtype=dt);g,sg=soft(z,t);ref=reference(z,teacher=t)
            softrows.append({'dtype':np.dtype(dt).name,'requested_delta':delta,'stored_student':z,'teacher':t,'standard_gradient':g,'stable_gradient':sg,'reference_gradient':ref,'standard_sum':g.sum(),'stable_sum':sg.sum(),'standard_max_absolute_error':np.max(abs(g-ref)),'stable_max_absolute_error':np.max(abs(sg-ref))})
    intended_t=np.array([2,1,0],dtype=np.float64);intended_s=intended_t+np.array([-1e-7,1e-7,0]);shift=1e5
    stored_t=(intended_t+shift).astype(np.float32);stored_s=(intended_s+shift).astype(np.float32)
    ig=reference(intended_s,teacher=intended_t);rg=reference(stored_s,teacher=stored_t);_,actual=soft(stored_s,stored_t)
    quant={'common_shift':shift,'intended_student':intended_s,'intended_teacher':intended_t,'stored_student':stored_s,'stored_teacher':stored_t,'intended_reference_gradient':ig,'stored_input_reference_gradient':rg,'stable_stored_gradient':actual,'stored_student_teacher_equal':bool(np.array_equal(stored_s,stored_t))}
    checks={'standard_target_cancellation_witness':any(r['standard_gradient'][0]==0 and r['reference_gradient'][0]!=0 for r in hardrows),'stable_hard_float32_relative':all(r['stable_target_relative_error']<2e-6 and r['stable_loss_relative_error']<2e-6 for r in hardrows if r['dtype']=='float32'),'stable_hard_float64_relative':all(r['stable_target_relative_error']<1e-12 and r['stable_loss_relative_error']<1e-12 for r in hardrows if r['dtype']=='float64'),'stable_equal_logits_exact_zero':all(np.all(r['stable_gradient']==0) for r in softrows if r['requested_delta']==0),'stable_near_equal_error':all(r['stable_max_absolute_error']<1e-12 for r in softrows),'input_quantization_cannot_be_recovered':np.max(abs(ig))>1e-9 and np.all(rg==0) and np.all(actual==0)}
    out={'scope':'Explicit finite-precision algebra, not autodiff or training reproduction','python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__,'reference_decimal_digits':mp.mp.dps,'protocol_sha256':hashlib.sha256((D/'PROTOCOL.md').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'hard':hardrows,'soft':softrows,'representation':quant,'checks':checks}
    (D/'RESULTS.json').write_text(json.dumps(out,indent=2,default=native,allow_nan=False)+'\n');print(json.dumps({'checks':checks,'hard':[{k:r[k] for k in ['dtype','logit_gap','standard_gradient','stable_gradient','stable_target_relative_error']} for r in hardrows],'soft_max_errors':[{'dtype':r['dtype'],'delta':r['requested_delta'],'standard':r['standard_max_absolute_error'],'stable':r['stable_max_absolute_error']} for r in softrows],'representation':quant},default=native,indent=2,allow_nan=False));assert all(checks.values())
if __name__=='__main__':main()
