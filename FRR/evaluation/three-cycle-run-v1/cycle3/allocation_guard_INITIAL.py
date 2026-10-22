"""Scoped allocation guard; assumes declared design/witness contract is correct."""
import numpy as np

def allocate(X,d,epsilon,*,calibration,population_rank,bounds=(.2,.4)):
    def stop(reason): return {'status':'unresolved','reason':reason}
    if calibration not in ('known','estimated'):
        return stop('calibration_unavailable')
    if population_rank!=2:
        return stop('population_design_insufficient')
    try:
        x=np.asarray(X,dtype=float); y=np.asarray(d,dtype=float)
        b=np.asarray(bounds,dtype=float); e=float(epsilon)
    except (ValueError,TypeError,OverflowError):
        return stop('invalid_input')
    if (x.ndim!=2 or x.shape[1]!=2 or x.shape[0]<2 or y.shape!=(x.shape[0],)
        or b.shape!=(2,) or not np.isfinite(e) or e<0
        or not np.all(np.isfinite(x)) or not np.all(np.isfinite(y))
        or not np.all(np.isfinite(b)) or np.any(b<0)
        or np.any(x<0) or np.any(x>1)):
        return stop('invalid_input')
    if np.linalg.matrix_rank(x,tol=1e-10)<2:
        return stop('estimated_design_singular')
    inverse=np.linalg.pinv(x)
    estimate=inverse@y
    radius=2*e+(float(b.sum())*e if calibration=='estimated' else 0.)
    half=abs(inverse)@np.full(x.shape[0],radius)
    return {'status':'conditional_interval','estimate':estimate.tolist(),
            'half_width':half.tolist(),'condition_number':float(np.linalg.cond(x)),
            'scope':'Conditional on correct design, witness and simultaneous noise-bound assumptions; no physical carrier identification'}
