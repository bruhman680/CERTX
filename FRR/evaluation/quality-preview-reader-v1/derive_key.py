import json,itertools,hashlib
from pathlib import Path
p=Path(__file__).parent
cases=json.loads((p/'cases.json').read_text())
# Independently transcribed from literal D/C/R/M contracts, not hidden_truth.
data={
'QP01':dict(prefix='N',threshold=28.2,unit='°C',raw=[26.8,27.4,27.1],correction=.3,error=.08,range=[24.8,29.4],channel='NK-6',capture='Nr42',refmax=27.71,referror=.04,root='Na',briefings=['Moss','Flint','Reed']),
'QP02':dict(prefix='O',threshold=8.6,unit='mm/s',raw=[6.9,8.1,7.5],correction=.25,error=.5,range=[4.9,10.1],channel='OK-6',capture='Or42',refmax=8.72,referror=.04,root='Oa',briefings=['Aster','Linen','Slate']),
'QP03':dict(prefix='P',threshold=15.7,unit='bar',raw=[14.4,15.1,14.8],correction=.55,error=.45,range=[12.4,17.1],channel='PK-6',capture='Pr42',refmax=15.6,referror=.35,root='Pa',briefings=['Cedar','Lark','Opal'])}
r=lambda x:round(x,8)
def action(v,t):
 if v is None:return 'UNRESOLVED'
 return 'RELEASE' if v[1]<=t else 'HOLD' if v[0]>t else 'UNRESOLVED'
out={'version':'quality-preview-reader-v1-prospective-key-1','source_sha256':hashlib.sha256((p/'cases.json').read_bytes()).hexdigest(),'derivation':'Authoritative literal initial + delivered record entailment; preview forecast excluded from physical warrant. Hidden truth not used to establish warrant.','decision_rule':'For maximum interval [L,U], RELEASE iff U<=threshold; HOLD iff L>threshold; else UNRESOLVED. Unknown bound is UNRESOLVED.','cases':{},'counts':{}}
for c in cases:
 cid=c['id']; d=data[cid]; ids=list(c['records']); D,C,R,M=[f"{d['prefix']}-{x}" for x in 'DCRM']
 assert ids==[D,C,R,M]
 assert min(d['raw'])>=d['range'][0] and max(d['raw'])<=d['range'][1]
 primary=[r(max(d['raw'])+d['correction']-d['error']),r(max(d['raw'])+d['correction']+d['error'])]
 ref=[r(d['refmax']-d['referror']),r(d['refmax']+d['referror'])]
 joint=[max(primary[0],ref[0]),min(primary[1],ref[1])]
 primary_samples=[[r(x+d['correction']-d['error']),r(x+d['correction']+d['error'])] for x in d['raw']]
 states={}
 for s in [(),*[(x,) for x in ids],*itertools.combinations(ids,2),tuple(ids)]:
  present=set(s); pr={D,C}<=present; rr={R,M}<=present
  bound=joint if pr and rr else primary if pr else ref if rr else None
  a=action(bound,d['threshold']); name='EMPTY' if not s else '+'.join(s)
  missing=[]
  if not pr:missing.append({'route':'primary','missing_ids':[x for x in [D,C] if x not in present]})
  if not rr:missing.append({'route':'reference','missing_ids':[x for x in [R,M] if x not in present]})
  reason=('Both complete routes intersect; maxima-only reference contract permits this tight joint maximum interval.' if pr and rr else 'Complete exact channel/range/coverage primary join.' if pr else 'Complete exact capture/current-task reference join.' if rr else 'No complete authoritative task-to-physical-bound join. Initial summaries and preview supply none.')
  if bound and a=='UNRESOLVED':reason+=' Applicable interval straddles the inclusive threshold.'
  nextcheck=None if a!='UNRESOLVED' else ('Tighten an applicable physical error bound enough to decide the task; unchanged copies cannot do so.' if pr and rr else 'Complete a missing applicable route; a straddling complete route requires tighter physical uncertainty or a decisive other route.')
  states[name]={'delivered_ids':list(s),'action':a,'retained_claim_reuse':a=='RELEASE','claim_status':'warranted' if a=='RELEASE' else 'refuted' if a=='HOLD' else 'unsupported','task_maximum_interval':bound,'complete_routes':(['primary'] if pr else [])+(['reference'] if rr else []),'origin_root':d['root'] if D in present else None,'briefing_edges':([f"{d['root']} -> {d['briefings'][0]}",f"{d['briefings'][0]} -> {d['briefings'][1]}",f"{d['briefings'][1]} -> {d['briefings'][2]}"] if D in present else None),'missing_joins':missing,'reason':reason,'acceptable_next_check':nextcheck}
 paths={}
 for first,second in itertools.permutations(ids,2):
  pair=tuple(x for x in ids if x in {first,second}); gold=states['+'.join(pair)]
  decisive=[]
  for other in ids:
   if other==first:continue
   pair2=tuple(x for x in ids if x in {first,other}); g=states['+'.join(pair2)]
   if g['action']!='UNRESOLVED':decisive.append(other)
  paths[first+' -> '+second]={'ordered_ids':[first,second],'final_state':'+'.join(pair),'final_action':gold['action'],'retained_claim_reuse':gold['retained_claim_reuse'],'reachable_decisive_second_ids':decisive,'selected_decisive_second':second in decisive,'missed_available_decisive_second':bool(decisive) and second not in decisive,'lookup_cost':2,'selection_rationale_rule':'Judge prospective plausibility from inventory and already delivered evidence; never require knowledge of unseen numeric content.'}
 out['cases'][cid]={'threshold':d['threshold'],'unit':d['unit'],'primary_derivation':{'channel':d['channel'],'raw_samples':d['raw'],'raw_range':d['range'],'correction':d['correction'],'residual_bound':d['error'],'sample_intervals':primary_samples,'maximum_interval':primary},'reference_derivation':{'current_capture':d['capture'],'maximum':d['refmax'],'per_sample_error_bound':d['referror'],'maximum_interval':ref},'joint_maximum_interval':joint,'singleton_completion_check':'All four remain UNRESOLVED: D lacks correction/residual, C lacks task/channel assignment, R lacks capture scope, M lacks readings. Preview and unkeyed initial summaries cure none.','states':states,'ordered_paths':paths,'external_truth_diagnostic_only':{'actual_maximum':c['hidden_truth']['generation_truth']['actual_maximum'],'claim_correct':c['hidden_truth']['claim_correct']},'preview_diagnostic_only':{'predicted_route':c['hidden_truth']['preview_predicted_route'],'correct':c['hidden_truth']['preview_prediction_correct']}}
 assert len(states)==12 and len(paths)==12
out['counts']={'cases':len(cases),'states':sum(len(c['states']) for c in out['cases'].values()),'ordered_paths':sum(len(c['ordered_paths']) for c in out['cases'].values())}
text=json.dumps(out,indent=2,ensure_ascii=False)+'\n'
initial=p/'KEY_INITIAL.json'
if initial.exists():raise SystemExit('Refusing to overwrite existing KEY_INITIAL.json')
(p/'KEY.json').write_text(text);initial.write_text(text)
print(json.dumps(out['counts']))
