"""Counterfactual check of an unchanged generated artifact; no new model calls."""
import run as r
import copy
ROOT=r.H
r.H=ROOT/'program-transfer'
assert not (r.H/'PLAN.json').exists()
before=r.c.inventory()
raw=r.c.read(ROOT/'results/provided_value_t1_raw.json')
sources=r.c.read(r.OLD/'retrieval/jobs.json')[:2]
r.save(r.Path('PLAN.json'),{'trigger':'parsed-value receipt produced a complete file-reading program with correct nonce in labeled stdout','artifact':'../results/provided_value_t1_raw.json','intervention':'execute the exact saved notebook text on two fresh pre-model fixtures whose only data difference is the nonce file; same mechanical declaration','model_calls':0,'claim_scope':'generated program file dependence, not fresh model competence or independent sampling','no_repairs':True,'no_unknown_action_replay':True})
results=[]
for s in sources:
    name='transfer_'+s['case_id'][-1]
    j=r.job(name,s,copy.deepcopy(s['messages']))
    w=r.c.GardenWorld.open(r.Path(j['world_store']))
    try:
        prior=w.checkpoint();batch=w.receive_notebook(raw['text']);after=w.checkpoint()
    finally:w.close()
    r.save(r.Path('results')/(name+'_batch.json'),batch)
    out=[x['feedback']['stdout'] for x in batch['operations'] if x['feedback'] is not None]
    expected=s['metadata']['expected_value']
    row={'case':name,'expected_value':expected,'stdout':out,'expected_labeled_stdout':out==['Value: '+expected+'\n'],'before_id':prior['id'],'after_id':after['id'],'verification':r.c.verify_store(r.Path(j['world_store']))}
    results.append(row)
assert all(x['expected_labeled_stdout'] for x in results)
assert r.c.inventory()==before
r.save(r.Path('RESULTS.json'),{'rows':results,'model_calls':0,'artifact_executions':2,'same_generated_text':True,'main_unchanged':True})
print(results)
