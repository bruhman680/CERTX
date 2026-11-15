"""Read-only joins of actual study records; never executes saved model source."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def join(a,aa,b,bb):
    return [{'turn':n,'input_ids_equal':read(a/'raw'/f'{aa}_t{n}.json')['input_token_ids']==read(b/'raw'/f'{bb}_t{n}.json')['input_token_ids'],
             'output_ids_equal':read(a/'raw'/f'{aa}_t{n}.json')['generated_token_ids']==read(b/'raw'/f'{bb}_t{n}.json')['generated_token_ids']} for n in range(1,4)]

if __name__=='__main__':
    results=[read(ROOT/f'cycle{n}/run/RESULTS.json') for n in range(1,4)]
    audits=[read(ROOT/f'cycle{n}/run/AUDIT.json') for n in range(1,4)]
    assert all(r['status']=='pass' and r['actual_model_calls']==6 and r['main_unchanged'] and r['weights_unchanged'] for r in results)
    assert all(a['status']=='pass' and a['actual_model_calls']==6 for a in audits)
    assert all(not (ROOT/f'cycle{n}/run'/p).exists() for n in range(1,4) for p in ('PENDING.json','PREPARATION_PENDING.json','RUN.lock'))
    links={
        'archived_scoped_prose_to_cycle1_user_all':join(ROOT.parent/'scoped-world-facts-v1/run','prose',ROOT/'cycle1/run','user_all'),
        'cycle1_system_all_to_cycle2_system_all':join(ROOT/'cycle1/run','system_all',ROOT/'cycle2/run','system_all'),
        'cycle2_split_to_cycle3_control':join(ROOT/'cycle2/run','split',ROOT/'cycle3/run','control'),
    }
    frozen={}
    for n in range(1,4):
        d=ROOT/f'cycle{n}/design';f=read(d/'DESIGN_FREEZE.json')
        frozen[str(n)]={p:hashlib.sha256((d/p).read_bytes()).hexdigest()==sha for p,sha in f['sha256'].items()}
        assert all(frozen[str(n)].values())
        if n>1:assert read(d/'CONDITION.json')['prior_readout_sha256']==hashlib.sha256((ROOT/f'cycle{n-1}/READOUT.json').read_bytes()).hexdigest()
    out={'status':'pass','actual_model_calls':sum(r['actual_model_calls'] for r in results),'main_entry':1630,'main_unchanged':True,'weights_unchanged':True,'training_updates':0,'pending':False,'all_design_freezes_match':frozen,'exact_control_joins':links,
         'interpretation':'equal repeated conditions are reproducibility witnesses, not independent samples; any unequal joins would be observations, not silently replaced outputs'}
    with (ROOT/'CROSS_CYCLE_CHECKS.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({k:v for k,v in out.items() if k!='all_design_freezes_match'}))
