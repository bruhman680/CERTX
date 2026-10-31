"""Frozen full-cohort exact-label scoring; primary/challenge/regression/dev separate."""
from pathlib import Path
import json,hashlib,sys
from collections import Counter
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(R/'tools'))
from stored_run_audit import evaluate
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):
 with p.open('x') as f:f.write(json.dumps(x,indent=2)+'\n')
for freeze in ('FREEZE.json','RAW_FREEZE.json'):
 for name,value in json.loads((P/freeze).read_text())['sha256'].items():assert h(P/name)==value,name
run=P/'run';manifest=json.loads((run/'RUN_MANIFEST.json').read_text());assert manifest['status']=='complete' and manifest['calls']==360
old=R/'evaluation/lora-state-pilot-v1';prep=R/'evaluation/decision-token-preparation-v1'
oldcases=json.loads((old/'EVAL_CASES.json').read_text());oldkeys={k['id']:k for k in json.loads((old/'KEYS.json').read_text())}
sets={'dev':[c for c in oldcases if c['split']=='dev'],'primary':json.loads((prep/'NEW_PRIMARY_CASES.json').read_text()),'challenge':json.loads((P/'CHALLENGE_CASES.json').read_text()),'regression':[c for c in oldcases if c['split']=='test']}
keys={**oldkeys,**{k['id']:k for k in json.loads((prep/'NEW_PRIMARY_KEYS.json').read_text())},**{k['id']:k for k in json.loads((P/'CHALLENGE_KEYS.json').read_text())}}
arms=('original','sequence_mean','decision_balanced');lines=(run/'RAW_OUTPUTS.jsonl').read_text().splitlines(keepends=True);rows=[json.loads(l) for l in lines]
expected=[c['id']+'__'+arm+'__'+subset for arm in arms for subset,cases in sets.items() for c in cases]
assert [r['run_id'] for r in rows]==expected and len(set(expected))==len(expected)==360
out={'scope':'one authored matched lossallocation comparison,notindependentsampling/puretokenlengthcausality','arms':{},'paired_by_subset':{}}
for arm in arms:
 out['arms'][arm]={}
 for subset,cases in sets.items():
  folder=P/'scores'/arm/subset;folder.mkdir(parents=True,exist_ok=False);ids=[c['id']+'__'+arm+'__'+subset for c in cases];chosen=[r for r in rows if r['run_id'] in ids]
  (folder/'RAW_SUBSET.jsonl').write_text(''.join(line for line,row in zip(lines,rows) if row['run_id'] in ids));dump(folder/'KEY_SUBSET.json',[{'id':c['id']+'__'+arm+'__'+subset,'expected':keys[c['id']]['expected']} for c in cases])
  contract={'claim_id':'DLC1-'+arm+'-'+subset,'identity':{'family':'decision_loss_compare','facet':'state_label','cycle':'DLC1','arm':arm},'expected_run_ids':ids,'parser':'strip_upper_exact_label_v1','raw':{'path':'RAW_SUBSET.jsonl','sha256':h(folder/'RAW_SUBSET.jsonl')},'keys':{'path':'KEY_SUBSET.json','sha256':h(folder/'KEY_SUBSET.json')}}
  dump(folder/'contract.json',contract);receipt=evaluate(contract,folder);assert receipt['status']=='computed',receipt;dump(folder/'RECEIPT.json',receipt)
  s=receipt['summary'];label=lambda r:r['text'].strip().upper() if r['text'].strip().upper() in ('YES','NO','WITHHOLD') else 'UNRESOLVED'
  s['perclass']={l:{'n':sum(keys[r['record_id']]['expected']==l for r in chosen),'matches':sum(label(r)==l for r in chosen if keys[r['record_id']]['expected']==l)} for l in ('YES','NO','WITHHOLD')}
  s['confusion']={l:dict(Counter(label(r) for r in chosen if keys[r['record_id']]['expected']==l)) for l in ('YES','NO','WITHHOLD')}
  s['by_family']={f:{'n':sum(r['structure_family']==f for r in chosen),'matches':sum(label(r)==keys[r['record_id']]['expected'] for r in chosen if r['structure_family']==f)} for f in sorted({r['structure_family'] for r in chosen})}
  s['inference_seconds']=sum(r['inference_seconds_excluding_serialization'] for r in chosen);s['cache_bytes']=sum(r['cache_artifact']['bytes'] for r in chosen)
  if subset=='challenge':
   state=lambda v:'WITHHOLD' if v is None else ('NO' if v==0 else 'YES')
   disagree=[r for r in chosen if keys[r['record_id']]['expected']!=state(keys[r['record_id']]['other_value'])]
   s['discordant_target_other']={'n':len(disagree),'matches':sum(label(r)==keys[r['record_id']]['expected'] for r in disagree),'first_or_last_reference_matches':12,'wrong_other_reference_matches':0}
   s['by_target_position']={str(first):{'n':sum(keys[r['record_id']]['target_first']==first for r in chosen),'matches':sum(label(r)==keys[r['record_id']]['expected'] for r in chosen if keys[r['record_id']]['target_first']==first)} for first in (True,False)}
   firstscore=sum((keys[r['record_id']]['expected'] if keys[r['record_id']]['target_first'] else state(keys[r['record_id']]['other_value']))==keys[r['record_id']]['expected'] for r in chosen)
   lastscore=sum((state(keys[r['record_id']]['other_value']) if keys[r['record_id']]['target_first'] else keys[r['record_id']]['expected'])==keys[r['record_id']]['expected'] for r in chosen)
   assert firstscore==lastscore==24 and len(disagree)==24;s['construction_reference_baselines']={'first_sampled_field':firstscore,'last_sampled_field':lastscore,'any_constant_class':12,'always_other':12}
  out['arms'][arm][subset]=s
  dump(folder/'DERIVATION.json',{'parent_raw_sha256':h(run/'RAW_OUTPUTS.jsonl'),'ids':ids,'selection':'predeclaredarm/subset,exactlines,nocorrectnessfiltering','key_labels':'pre-frozenindependentofoutputs'})
for subset,cases in sets.items():
 paired=[]
 for c in cases:
  rr={arm:next(r for r in rows if r['run_id']==c['id']+'__'+arm+'__'+subset) for arm in arms};gold=keys[c['id']]['expected'];a=rr['sequence_mean']['text'].strip().upper()==gold;b=rr['decision_balanced']['text'].strip().upper()==gold
  paired.append({'id':c['id'],'expected':gold,'sequence_mean':rr['sequence_mean']['text'],'decision_balanced':rr['decision_balanced']['text'],'mean_match':a,'balanced_match':b})
 out['paired_by_subset'][subset]={'rows':paired,'counts':dict(Counter('both_match' if x['mean_match'] and x['balanced_match'] else 'balanced_only' if x['balanced_match'] else 'mean_only' if x['mean_match'] else 'neither_matches' for x in paired))}
dump(P/'SUMMARY.json',out);print(json.dumps({'arms':out['arms'],'paired':{s:x['counts'] for s,x in out['paired_by_subset'].items()}},indent=2))
