"""Predeclared exact-law discrimination; probe menu assumes known reset/gate semantics.
Attributor sees probabilities only. World generator has explicit carrier labels.
"""
import json
from pathlib import Path
TOL=.01  # fixed before evaluation; no threshold calibration

def world_law(kind, field_retained=True, private_retained=True, transplant_sign=1, reader_gate=True):
    f=.25 if kind in ('pure_field','mixed','off_target_damage') else 0
    p=.2 if kind in ('private_only','mixed','erase_dependent_private_response') else 0
    retention=int(private_retained)
    if kind=='reset_leak':
        p=.2; retention=1 if private_retained else .4
        # Erasure manipulates private retention too: an explicit off-target pathway.
        retention*=1 if field_retained else .25
    if kind=='erase_dependent_private_response':
        retention*=int(field_retained)
    prob=.5+f*int(field_retained)*transplant_sign*int(reader_gate)+p*retention
    if kind=='off_target_damage' and not field_retained:
        prob-=.1  # erasure damages reader even with environmental gate disabled
    assert 0<=prob<=1
    return prob

def observation(world):
    return {'ordinary_keep':world(field_retained=True),
            'ordinary_clear':world(field_retained=False),
            'private_clear_keep':world(field_retained=True,private_retained=False),
            'private_clear_clear':world(field_retained=False,private_retained=False),
            'private_clear_opposite_transplant':world(field_retained=True,private_retained=False,transplant_sign=-1),
            'reader_gate_keep':world(field_retained=True,private_retained=False,reader_gate=False),
            'reader_gate_clear':world(field_retained=False,private_retained=False,reader_gate=False)}

def attribute(obs):
    """No world labels, mechanism parameters or truth flags are received."""
    naive=obs['ordinary_keep']-obs['ordinary_clear']>TOL
    tests={'survives_private_clear':obs['private_clear_keep']-obs['private_clear_clear']>TOL,
           'clear_is_chance':abs(obs['private_clear_clear']-.5)<=TOL,
           'opposite_payload_reverses':abs(obs['private_clear_keep']+obs['private_clear_opposite_transplant']-1)<=TOL and obs['private_clear_opposite_transplant']<.5-TOL,
           'reader_gate_removes_effect':abs(obs['reader_gate_keep']-obs['reader_gate_clear'])<=TOL and abs(obs['reader_gate_keep']-.5)<=TOL}
    return {'naive_field_attribution':naive,'conservative_field_attribution':all(tests.values()),'checks':tests}

def run():
    truth={'pure_field':True,'private_only':False,'erase_dependent_private_response':False,'mixed':True,'reset_leak':False,'off_target_damage':True}
    rows=[]
    for family,has_field in truth.items():
        obs=observation(lambda **kwargs:world_law(family,**kwargs));pred=attribute(obs)
        rows.append({'family':family,'actual_field_pathway':has_field,'observations':obs,**pred,'naive_false_field_attribution':pred['naive_field_attribution'] and not has_field,'conservative_false_field_attribution':pred['conservative_field_attribution'] and not has_field,'conservative_abstains':not pred['conservative_field_attribution']})
    assert [r['family'] for r in rows if r['naive_false_field_attribution']]==['erase_dependent_private_response','reset_leak']
    assert not any(r['conservative_false_field_attribution'] for r in rows)
    assert next(r for r in rows if r['family']=='off_target_damage')['conservative_abstains']
    return {'rule_tolerance_predeclared':TOL,'scope':'Exact prescribed observation laws, not heldout empirical worlds or generic attribution guarantee. Function receives observations only; probe semantics supplied by designer.','rows':rows}
if __name__=='__main__':
    result=run();out=Path(__file__).resolve().parents[1]/'evaluation/results/attribution-population-laws.json';out.write_text(json.dumps(result,indent=2)+'\n')
    for r in result['rows']:print(r['family'],r['naive_field_attribution'],r['conservative_field_attribution'],r['conservative_abstains'])
