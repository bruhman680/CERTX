"""Exact intervention toy: persistence location is operationally specified, not inferred from labels."""
import json
from pathlib import Path
import numpy as np

K = np.array([[[.85,.15],[.10,.90]],[[.55,.45],[.40,.60]]])

def deposit(bit, strength, passes):
    field = np.array([.5,.5])
    for _ in range(passes):
        field = (1-strength)*field
        field[bit] += strength
    return field

def hold(field, epsilon, delay):
    return field @ np.linalg.matrix_power(np.array([[1-epsilon,epsilon],[epsilon,1-epsilon]]),delay)

def read_law(field, y_reset, horizon, copy_strength, reader_blind=False):
    # Fresh focal reader gets only a fixed visible start, no writer state/history.
    # Emission uses current field; field then retains or copies previous visible y.
    cur = {(y_reset,):field.copy()}
    for _ in range(horizon):
        nxt = {}
        for history, a in cur.items():
            yp = history[-1]
            transition = (1-copy_strength)*np.eye(2)
            transition[:,yp] += copy_strength
            for y in (0,1):
                likelihood = np.full(2, K[:,yp,y].mean()) if reader_blind else K[:,yp,y]
                nxt[history+(y,)] = (a*likelihood) @ transition
        cur = nxt
    return {h:float(a.sum()) for h,a in cur.items()}

def tv(left,right):
    return .5*sum(abs(left[k]-right[k]) for k in left)

def run():
    records=[]
    for strength in (0,.02,.2,1):
        for passes in (1,10):
            for epsilon in (0,.01,.1,.5):
                for delay in (0,1,10,100):
                    pair=[hold(deposit(b,strength,passes),epsilon,delay) for b in (0,1)]
                    for y_reset in (0,1):
                        for horizon in (1,4,8):
                            for mode in ('retained','cleared','transplanted','writer_kept_field_cleared','no_write','opposite_transplant','reader_blind'):
                                if mode in ('cleared','writer_kept_field_cleared','no_write'):
                                    used=[np.array([.5,.5])]*2
                                elif mode=='transplanted':
                                    used=[p.copy() for p in pair]
                                elif mode=='opposite_transplant':
                                    used=[pair[1].copy(),pair[0].copy()]
                                else:
                                    used=pair
                                laws=[read_law(p,y_reset,horizon,.2,reader_blind=(mode=='reader_blind')) for p in used]
                                distance=tv(*laws)
                                assert all(abs(sum(l.values())-1)<1e-11 for l in laws)
                                if mode in ('cleared','writer_kept_field_cleared','no_write','reader_blind'):
                                    assert distance<1e-12
                                if horizon==1 and mode in ('retained','transplanted'):
                                    expected=.3*(1-(1-strength)**passes)*abs(1-2*epsilon)**delay
                                    assert abs(distance-expected)<1e-11
                                records.append(dict(strength=strength,passes=passes,epsilon=epsilon,delay=delay,y_reset=y_reset,horizon=horizon,mode=mode,tv=distance))
    # Same field state from another history produces exactly the same reader law.
    example=hold(deposit(1,.2,10),.01,10)
    assert read_law(example,0,8,.2)==read_law(example.copy(),0,8,.2)
    return {'scope':'Designed finite-state intervention, not emergent memory or a physical substrate. Field is independently transferable by construction. Writer-kept control has no writer-to-reader channel by construction. Transplant equivalence establishes sufficiency in this model, not unique history or independent replication.',
            'checks':['normalized laws','zero clear/no-write effects','analytic one-step formula','identical-state history aliasing'],
            'records':records}

if __name__=='__main__':
    result=run()
    out=Path(__file__).resolve().parents[1]/'evaluation/results/wake-reset-transfer.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(f'{len(result["records"])} exact conditions; all checks passed; {out}')
    for r in result['records']:
        if r['strength']==.2 and r['passes']==10 and r['epsilon']==.01 and r['delay'] in (0,10,100) and r['y_reset']==0 and r['horizon']==1 and r['mode'] in ('retained','cleared','transplanted'):
            print(r)
