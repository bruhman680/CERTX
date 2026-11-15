"""External literal-pattern and equality analysis; no inference or world operations."""
from pathlib import Path
import json,re
H=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def raw(c,n):return read(H/f'cycle{c}/raw/{n}.json')
def eq(a,b):return a['generated_token_ids']==b['generated_token_ids']

if __name__=='__main__':
    results=[read(H/f'cycle{c}/RESULTS.json') for c in (1,2,3)]
    audits=[read(H/f'cycle{c}/AUDIT.json') for c in (1,2,3)]
    assert all(x['status']=='pass' for x in results+audits)
    assert sum(x['actual_model_calls'] for x in results)==8
    assert all(x['main_unchanged'] and x['weights_unchanged'] and x['world_actions']==0 and x['automatic_note_appends']==0 for x in results)
    assert not any((H/f'cycle{c}'/p).exists() for c in (1,2,3) for p in ('PENDING.json','RUN.lock'))
    patterns=[];ids=set()
    for c in (1,2,3):
        p=read(H/f'cycle{c}/PLAN.json')
        if c>1:
            import hashlib
            assert p['previous_results_sha256']==hashlib.sha256((H/f'cycle{c-1}/RESULTS.json').read_bytes()).hexdigest()
        for case in p['cases']:
            r=raw(c,case['name']);ids.add(tuple(r['input_token_ids']))
            patterns.append({'cycle':c,'case':case['name'],'literal_named_file_strings':sorted(set(re.findall(r'file is named "([^"]+)"',r['text']))),
                             'first_sentence':r['text'].split('. ')[0],
                             'scope':'literal extraction, not verified object existence or semantic scoring'})
    factorial={
      'receipt_change_under_world_prior_outputs_equal':eq(raw(3,'world_native'),raw(3,'world_renamed')),
      'receipt_change_under_directory_prior_outputs_equal':eq(raw(3,'directory_native'),raw(3,'directory_renamed')),
      'prior_change_under_native_receipt_outputs_equal':eq(raw(3,'world_native'),raw(3,'directory_native')),
      'prior_change_under_renamed_receipt_outputs_equal':eq(raw(3,'world_renamed'),raw(3,'directory_renamed'))}
    repeats={n:eq(raw(1,n),raw(3,'world_'+n)) for n in ('native','renamed')}
    out={'status':'pass','cycles':3,'actual_model_calls':8,'distinct_input_token_sequences':len(ids),'factorial_output_equalities':factorial,
         'cycle1_to_cycle3_exact_output_repeats':repeats,'literal_patterns':patterns,'main_entry':1630,'main_unchanged':True,'weights_unchanged':True,'training_updates':0,'world_actions':0,
         'scope':'pointwise deterministic context effects, not population estimates, internal mechanism identification, world learning or independent replications'}
    with (H/'ANALYSIS.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out))
