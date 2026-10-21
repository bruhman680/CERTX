"""Exact illustrative counterexamples; no fitted model or behavioral efficacy test."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def witnesses():
    # Same current observation and target, opposite actuator dynamics.
    worlds=[{'gain':g,'observation':0,'target':1,'successful_action':g} for g in [-1,1]]
    for w in worlds:
        assert w['gain']*w['successful_action']==w['target']
    # For any random policy choosing +1 with p, successes are p and 1-p.
    grid=[F(i,100) for i in range(101)]
    worst=[min(p,1-p) for p in grid]
    assert max(worst)==F(1,2)

    # A correct probability forecast can assign nonzero probability to failure.
    q=F(4,5)
    expected=lambda p:q*(1-p)**2+(1-q)*p**2
    # Exact identity on all rational p: loss(p)-loss(q)=(p-q)^2.
    assert all(expected(p)-expected(q)==(p-q)**2 for p in grid)

    # Valid modus ponens places no guarantee on a conclusion in a world
    # where a premise is false. Enumerate propositional interpretations.
    rows=[]
    for p in [False,True]:
        for qv in [False,True]:
            implication=(not p) or qv
            premises=p and implication
            assert not premises or qv
            rows.append({'P':p,'Q':qv,'P_implies_Q':implication,'premises_hold':premises})

    # Two favorable metrics, conflicting objective orderings.
    options={'A':{'quality':9,'cost':9},'B':{'quality':6,'cost':1}}
    choices={}
    for penalty in [F(1,10),F(1,1)]:
        choices[str(penalty)]=max(options,key=lambda a:options[a]['quality']-penalty*options[a]['cost'])
    assert choices=={'1/10':'A','1':'B'}

    # Same measured target error can coexist with a hidden state error.
    true=F(3,5);bias=F(2,5);target=F(1)
    assert target-(true+bias)==0 and target-true==F(2,5)

    # A compressed record merges contexts needing opposite future actions.
    histories=[{'gain':-1,'latest_y':0},{'gain':1,'latest_y':0}]
    summary=lambda h:h['latest_y']
    assert summary(histories[0])==summary(histories[1])
    assert histories[0]['gain']!=histories[1]['gain']

    return {
      'study':'ES-C1','kind':'Authored exact counterexamples, not prospective empirical evidence',
      'same_feedback_opposite_actions':{'worlds':worlds,'random_policy_success':'p and 1-p; min(p,1-p)<=1/2 for every p in [0,1]','scope':'One-shot decision, no distinguishing history, probe or extra observation. A later informative probe can change this bound.'},
      'forecast_vs_outcome':{'true_event_probability':str(q),'optimal_Brier_forecast':str(q),'expected_Brier_loss':str(expected(q)),'realized_loss_if_event_absent':str(q*q),'event_absent_probability':str(1-q),'identity':'E_loss(p)-E_loss(q)=(p-q)^2; rational grid is a consistency check, identity is algebraic'},
      'valid_inference_false_premise':{'truth_table':rows,'example':{'P':True,'Q':False,'P_implies_Q':False,'conclusion_false':True},'scope':'Validity preserves truth conditional on true premises; this example is not a counterexample to modus ponens.'},
      'objective_tradeoff':{'options':options,'quality_minus_cost_penalty_choices':choices,'scope':'Preference weights differ; outcome facts do not change.'},
      'measurement_vs_state':{'target':str(target),'true_state':str(true),'sensor_bias':str(bias),'measured_error':'0','true_error':str(target-true)},
      'compression_vs_future_control':{'histories':histories,'common_summary':0,'required_actions':[-1,1],'scope':'This chosen summary loses a task-relevant distinction; other summaries can retain it.'},
      'checks':{'all_assertions_passed':True,'new_model_calls':0,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    }


if __name__=='__main__':
    out=Path(__file__).resolve().parents[1]/'evaluation/error-success-contact/WITNESSES.json'
    result=witnesses();out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
