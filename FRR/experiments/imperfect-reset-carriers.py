"""Two explicit bit carriers; matched stochastic interventions, no semantic claim.
Reader observes a selected carrier through a binary symmetric measurement channel.
Retention/erasure is controlled; imperfect actor reset can leak private state.
"""
import json
from pathlib import Path
import numpy as np

def writer(payload, baseline, write_draw, enabled, strength=.8):
    """Only writer receives the target payload."""
    return np.where(enabled & (write_draw<strength),payload,baseline)

def reset_controller(field,private,field_retained,private_retained,leakage,leak_draw,erase_field,erase_private):
    """Carrier reset; neither target nor scorer is available."""
    return (field if field_retained else erase_field,
            private if private_retained else np.where(leak_draw<leakage,private,erase_private))

def reader(field,private,field_share,choose,field_flip,private_flip,measurement):
    """Fresh observer: no writer target, initial states, or scoring access."""
    f=np.bitwise_xor(field,field_flip<.1)
    p=np.bitwise_xor(private,private_flip<.1)
    return np.bitwise_xor(np.where(choose<field_share,f,p),measurement<.1)

def score(response,target):
    return (response==target).astype(float)

def run(seed=714,R=200000):
    rng=np.random.default_rng(seed)
    # Shared across intervention arms for paired variance reduction; independent by causal role.
    bit=rng.integers(0,2,R); private_baseline=rng.integers(0,2,R); field_baseline=rng.integers(0,2,R)
    write_private=rng.random(R);write_field=rng.random(R)
    field_flip=rng.random(R); private_flip=rng.random(R)
    leak_draw=rng.random(R); erase_field=rng.integers(0,2,R);erase_private=rng.integers(0,2,R)
    choose=rng.random(R);measure=rng.random(R);blind=rng.integers(0,2,R)
    rows=[]
    for wrote in (False,True):
      # Each deposit acts on its own carrier with independent 80% success.
      field=writer(bit,field_baseline,write_field,wrote)
      private=writer(bit,private_baseline,write_private,wrote)
      for field_retained in (False,True):
       for private_retained in (False,True):
        for leak in (0,.05,.5):
         f,p=reset_controller(field,private,field_retained,private_retained,leak,leak_draw,erase_field,erase_private)
         for field_share in (0,.5,1):
          read=reader(f,p,field_share,choose,field_flip,private_flip,measure)
          correctness=score(read,bit)
          expected=.5+.5*.8*.8*.8*int(wrote)*(field_share*int(field_retained)+(1-field_share)*(1 if private_retained else leak))
          accuracy=float(correctness.mean())
          se=float(correctness.std()/np.sqrt(R))
          assert abs(accuracy-expected)<6*se+.0001
          rows.append(dict(wrote=wrote,field_retained=field_retained,private_retained=private_retained,reset_leakage=leak,field_reader_share=field_share,accuracy=accuracy,expected=expected,se=se))
    # Primary matched contrast: fresh private reset zero leakage, same private controls, field retain vs clear.
    lookup=lambda retained: next(r for r in rows if r['wrote'] and r['field_retained']==retained and not r['private_retained'] and r['reset_leakage']==0 and r['field_reader_share']==.5)
    field=writer(bit,field_baseline,write_field,True)
    private=writer(bit,private_baseline,write_private,True)
    f_keep,p_clear=reset_controller(field,private,True,False,0,leak_draw,erase_field,erase_private)
    f_clear,_=reset_controller(field,private,False,False,0,leak_draw,erase_field,erase_private)
    r_keep=reader(f_keep,p_clear,.5,choose,field_flip,private_flip,measure)
    r_clear=reader(f_clear,p_clear,.5,choose,field_flip,private_flip,measure)
    delta=score(r_keep,bit)-score(r_clear,bit)
    # q=0 reader has no environmental route; q=1 has no private route.
    assert np.array_equal(reader(field,private,0,choose,field_flip,private_flip,measure),reader(1-field,private,0,choose,field_flip,private_flip,measure))
    assert np.array_equal(reader(field,private,1,choose,field_flip,private_flip,measure),reader(field,1-private,1,choose,field_flip,private_flip,measure))
    contrasts={'zero_leakage_field_effect':lookup(True)['accuracy']-lookup(False)['accuracy'], 'expected_effect':.128,'paired_se':float(delta.std()/np.sqrt(R)),'blind_accuracy':float(np.mean(blind==bit))}
    assert abs(float(delta.mean())-contrasts['zero_leakage_field_effect'])<1e-12
    assert all(abs(r['accuracy']-.5)<6*r['se'] for r in rows if not r['wrote'])
    return {'seed':seed,'trials_per_condition':R,'scope':'Designed two independent binary storage channels, known interventions and observer mixture; not learned mediation or real AI memory. Same random arrays across arms for paired comparison; distinct arrays by stochastic causal role.','checks':['72 matched arms','analytic expectation within six Monte Carlo SE','no-write null','independent measurement draws','q0 environment-blind','q1 private-blind','pure reader API excludes target'],'contrasts':contrasts,'records':rows}
if __name__=='__main__':
    result=run();out=Path(__file__).resolve().parents[1]/'evaluation/results/imperfect-reset-carriers.json';out.write_text(json.dumps(result,indent=2)+'\n');print(result['contrasts']);print(len(result['records']))
