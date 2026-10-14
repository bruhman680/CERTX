"""Exact rival models: keep/clear contrasts alone do not locate persistence."""
import json
from pathlib import Path

def probability(model, bit, condition):
    # Signed field F and private P each in {-1,0,1}; zero = fair mixture.
    f=p=2*bit-1
    gate=1
    if condition=='clear_field':
        f=0
        if model=='erase_gate_artifact':gate=0
    elif condition=='clear_private':p=0
    elif condition=='clear_field_restore_gate':f=0
    elif condition=='swap_field':f=-f
    elif condition=='fresh_private_retained_field':p=0
    elif condition!='keep':raise ValueError(condition)
    if model=='environment':signal=f
    elif model in ('private_leakage','erase_gate_artifact'):signal=p
    else:raise ValueError(model)
    return .3+.15*gate*signal

def run():
    modes=['environment','private_leakage','erase_gate_artifact']
    conditions=['keep','clear_field','clear_private','clear_field_restore_gate','swap_field','fresh_private_retained_field']
    records=[dict(model=m,condition=c,p_one_given_write0=probability(m,0,c),p_one_given_write1=probability(m,1,c),signed_contrast=probability(m,1,c)-probability(m,0,c)) for m in modes for c in conditions]
    for c in ('keep','clear_field'):
        for b in (0,1):assert probability('environment',b,c)==probability('erase_gate_artifact',b,c)
    assert probability('environment',1,'swap_field')!=probability('erase_gate_artifact',1,'swap_field')
    return {'scope':'Constructed exact Bernoulli response laws; no fitting, no data-derived mechanism, no uncertainty. Clear intervention disables response gate only in artifact model. Equal laws on keep/clear yield exactly zero discriminating information even with infinite samples. Other interventions discriminate only if their selective effects are known.', 'records':records}
if __name__=='__main__':
    out=Path(__file__).resolve().parents[1]/'evaluation/results/erase-artifact-counterexample.json'
    out.write_text(json.dumps(run(),indent=2)+'\n')
    print('18 exact model/intervention cells; keep/clear rival equivalence verified; selective intervention separates.')
