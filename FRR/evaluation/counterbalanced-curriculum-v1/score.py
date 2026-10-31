"""Frozen full-denominator cohort and header-pair scoring; no model invocation."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib,sys
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(R/'tools'))
from stored_run_audit import evaluate
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def dump(p,x):
 with p.open('x') as f:f.write(json.dumps(x,indent=2)+'\n')
for fr in ('FREEZE.json','RAW_FREEZE.json'):
 for n,v in json.loads((P/fr).read_text())['sha256'].items():assert h(P/n)==v,n
run=P/'run';m=json.loads((run/'RUN_MANIFEST.json').read_text());assert m['status']=='complete' and m['calls']==252
D=P/'fixtures/DATA';sets={'dev':json.loads((D/'DEV_CASES.json').read_text()),'primary':json.loads((D/'PRIMARY_CASES.json').read_text())};keys={x['id']:x for n in ('DEV_KEYS.json','PRIMARY_KEYS.json') for x in json.loads((D/n).read_text())}
arms=('original','control','candidate');lines=(run/'RAW_OUTPUTS.jsonl').read_text().splitlines(keepends=True);rows=[json.loads(l) for l in lines]
expected=[c['id']+'__'+a+'__'+s for a in arms for s,cs in sets.items() for c in cs];assert [r['run_id'] for r in rows]==expected and len(set(expected))==252
norm=lambda r:r['text'].strip().upper() if r['text'].strip().upper() in ('YES','NO','WITHHOLD') else 'UNRESOLVED'
out={'scope':'singleauthoredcurriculum-packagecomparison,fixedpriorcontrolreused,nopurepositioncausalclaim','arms':{},'control_candidate_pairs':{}}
for a in arms:
 out['arms'][a]={}
 for s,cs in sets.items():
  folder=P/'scores'/a/s;folder.mkdir(parents=True,exist_ok=False);ids=[c['id']+'__'+a+'__'+s for c in cs];chosen=[r for r in rows if r['run_id'] in ids]
  (folder/'RAW_SUBSET.jsonl').write_text(''.join(line for line,r in zip(lines,rows) if r['run_id'] in ids));dump(folder/'KEY_SUBSET.json',[{'id':c['id']+'__'+a+'__'+s,'expected':keys[c['id']]['expected']} for c in cs])
  contract={'claim_id':'CS1-'+a+'-'+s,'identity':{'family':'curriculum_state','facet':'state_label','cycle':'CS1','arm':a},'expected_run_ids':ids,'parser':'strip_upper_exact_label_v1','raw':{'path':'RAW_SUBSET.jsonl','sha256':h(folder/'RAW_SUBSET.jsonl')},'keys':{'path':'KEY_SUBSET.json','sha256':h(folder/'KEY_SUBSET.json')}}
  dump(folder/'contract.json',contract);receipt=evaluate(contract,folder);assert receipt['status']=='computed',receipt;dump(folder/'RECEIPT.json',receipt);v=receipt['summary']
  v['perclass']={l:{'n':sum(keys[r['record_id']]['expected']==l for r in chosen),'matches':sum(norm(r)==l for r in chosen if keys[r['record_id']]['expected']==l)} for l in ('YES','NO','WITHHOLD')}
  v['confusion']={l:dict(Counter(norm(r) for r in chosen if keys[r['record_id']]['expected']==l)) for l in ('YES','NO','WITHHOLD')}
  v['by_family']={f:{'n':sum(r['structure_family']==f for r in chosen),'matches':sum(norm(r)==keys[r['record_id']]['expected'] for r in chosen if r['structure_family']==f)} for f in sorted({r['structure_family'] for r in chosen})}
  v['inference_seconds']=sum(r['inference_seconds_excluding_serialization'] for r in chosen);v['cache_bytes']=sum(r['cache_artifact']['bytes'] for r in chosen)
  if s=='primary':
   pairs=defaultdict(list)
   for r in chosen:pairs[keys[r['record_id']]['pair_id']].append(r)
   assert len(pairs)==36 and all(len(g)==2 for g in pairs.values())
   perpair=[]
   for pid,rs in pairs.items():
    gold=[keys[r['record_id']]['expected'] for r in rs];kind='discordant' if len(set(gold))==2 else 'same_state'
    labels=[norm(r) for r in rs];perpair.append({'pair_id':pid,'kind':kind,'record_ids':[r['record_id'] for r in rs],'expected':gold,'outputs':labels,'both_correct':all(label==key for label,key in zip(labels,gold)),'valid_label_switch':all(x!='UNRESOLVED' for x in labels) and labels[0]!=labels[1]})
   v['header_pairs']={kind:{'n':sum(x['kind']==kind for x in perpair),'both_correct':sum(x['both_correct'] for x in perpair if x['kind']==kind),'valid_label_switches':sum(x['valid_label_switch'] for x in perpair if x['kind']==kind)} for kind in ('discordant','same_state')}
   assert v['header_pairs']['discordant']['n']==24 and v['header_pairs']['same_state']['n']==12
   disc=[r for r in chosen if keys[r['record_id']]['pair_type']=='discordant_state'];assert len(disc)==48
   v['discordant_cases']={'n':len(disc),'matches':sum(norm(r)==keys[r['record_id']]['expected'] for r in disc)}
   v['by_position']={pos:{'n':sum(keys[r['record_id']]['position']==pos for r in chosen),'matches':sum(norm(r)==keys[r['record_id']]['expected'] for r in chosen if keys[r['record_id']]['position']==pos)} for pos in ('first','last')}
   v['by_role']={str(role):{'n':sum(keys[r['record_id']]['target_role']==role for r in chosen),'matches':sum(norm(r)==keys[r['record_id']]['expected'] for r in chosen if keys[r['record_id']]['target_role']==role)} for role in (0,1)}
   v['reference_policies']={'constant_class':24,'first_or_last_field':48,'fixed_named_record':48,'header_blind_fully_correct_discordant_pairs':0,'discordant_first_or_last_field':24}
   dump(folder/'HEADER_PAIRS.json',perpair)
  out['arms'][a][s]=v;dump(folder/'DERIVATION.json',{'raw_parent_sha256':h(run/'RAW_OUTPUTS.jsonl'),'selected_ids':ids,'selection':'predeclaredarm/subsetexactlines;no correctnessfiltering','key_source_sha256':h(D/('DEV_KEYS.json' if s=='dev' else 'PRIMARY_KEYS.json'))})
for s,cs in sets.items():
 paired=[]
 for c in cs:
  rr={a:next(r for r in rows if r['run_id']==c['id']+'__'+a+'__'+s) for a in ('control','candidate')};gold=keys[c['id']]['expected'];paired.append({'id':c['id'],'expected':gold,'control':norm(rr['control']),'candidate':norm(rr['candidate']),'control_match':norm(rr['control'])==gold,'candidate_match':norm(rr['candidate'])==gold})
 out['control_candidate_pairs'][s]={'rows':paired,'counts':dict(Counter('both_match' if x['control_match'] and x['candidate_match'] else 'candidate_only' if x['candidate_match'] else 'control_only' if x['control_match'] else 'neither_matches' for x in paired))}
dump(P/'SUMMARY.json',out);print(json.dumps({'arms':out['arms'],'paired':{s:x['counts'] for s,x in out['control_candidate_pairs'].items()}},indent=2))
