from pathlib import Path
import json,hashlib,itertools
import numpy as np
D=Path(__file__).resolve().parent
INTERVALS=[(.2,.8),(.75,.9),(.1,.3),(.55,.7)]

def risks(v):return np.array([1-v,.15+.4*v])
def policy_loss(q,v):return (1-q)*(1-v)+q*(.15+.4*v)
def loss(q,L,U):return max(policy_loss(q,L),policy_loss(q,U))
def regret(q,L,U):return max(policy_loss(q,v)-min(risks(v)) for v in (L,U))
def candidates(L,U,objective):
    slopes=[];intercepts=[]
    for v in (L,U):
        intercept=1-v-(min(risks(v)) if objective=='regret' else 0)
        slopes.append(-.85+1.4*v);intercepts.append(intercept)
    q=[0.,1.]
    if abs(slopes[0]-slopes[1])>1e-14:
        crossing=(intercepts[1]-intercepts[0])/(slopes[0]-slopes[1])
        if 0<=crossing<=1:q.append(float(crossing))
    f=regret if objective=='regret' else loss
    return min(q,key=lambda z:(f(z,L,U),z))

def probe_enum(v,k,d):
    total=0.
    for s,erased in itertools.product((0,1),repeat=2):
        pr=(v if s else 1-v)*(d if erased else 1-d)
        post=s*(1-erased)
        total+=pr*(k+float(s and erased)+min([1-post,.15+.4*post]))
    return total

def main():
    rows=[];grid=np.linspace(0,1,10001);max_grid=0.;max_enum=0.
    for L,U in INTERVALS:
        delta=[risks(v)[0]-risks(v)[1] for v in (L,U)]
        dominant='fallback' if min(delta)>=-1e-12 else 'rely' if max(delta)<=1e-12 else None
        qloss=candidates(L,U,'loss');qregret=candidates(L,U,'regret')
        for obj,q in [('loss',qloss),('regret',qregret)]:
            f=loss if obj=='loss' else regret
            max_grid=max(max_grid,abs(f(q,L,U)-min(f(z,L,U) for z in grid)))
        probes=[]
        for k,d in [(.03,0),(.5,0),(.03,.8)]:
            vals=[]
            for v in (L,U):
                expected=k+.15*(1-(1-d)*v)+d*v
                max_enum=max(max_enum,abs(expected-probe_enum(v,k,d)));vals.append(expected)
            worst=max(vals);naive=max(k+.15*(1-v) for v in (L,U))
            probes.append({'cost':k,'damage_probability':d,'endpoint_losses':vals,'worst_expected_loss':worst,'no_probe_minimax':loss(qloss,L,U),'prefer_probe_by_worst_loss':bool(worst<loss(qloss,L,U)-1e-12),'naive_ignoring_damage_worst_loss':naive,'naive_prefers_probe':bool(naive<loss(qloss,L,U)-1e-12)})
        rows.append({'interval':[L,U],'dominant_pure_action':dominant,'minimax_loss_fallback_probability':qloss,'minimax_loss':loss(qloss,L,U),'pure_minimax_loss':min(loss(0,L,U),loss(1,L,U)),'minimax_regret_fallback_probability':qregret,'minimax_regret':regret(qregret,L,U),'pure_minimax_regret':min(regret(0,L,U),regret(1,L,U)),'probes':probes})
    checks={'analytic_vs_grid':max_grid<2e-4,'probe_formula_vs_state_enumeration':max_enum<1e-10,'all_mix_probabilities_valid':all(0<=x['minimax_loss_fallback_probability']<=1 and 0<=x['minimax_regret_fallback_probability']<=1 for x in rows),'narrow_high_interval_rely':rows[1]['dominant_pure_action']=='rely','narrow_low_interval_fallback':rows[2]['dominant_pure_action']=='fallback','wide_randomization_improves_loss':rows[0]['minimax_loss']<rows[0]['pure_minimax_loss'],'wide_randomization_improves_regret':rows[0]['minimax_regret']<rows[0]['pure_minimax_regret'],'damaging_probe_reverses_naive_choice':rows[0]['probes'][2]['naive_prefers_probe'] and not rows[0]['probes'][2]['prefer_probe_by_worst_loss']}
    out={'scope':'Conditional authored expected-loss decision analysis; not empirical memory benefit','protocol_sha256':hashlib.sha256((D/'PROTOCOL.md').read_bytes()).hexdigest(),'source_cycle1_sha256':hashlib.sha256((D.parent/'cycle1/RESULTS.json').read_bytes()).hexdigest(),'rows':rows,'maximum_grid_gap':max_grid,'maximum_enumeration_error':max_enum,'new_random_draws':0,'checks':checks}
    (D/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
if __name__=='__main__':main()
