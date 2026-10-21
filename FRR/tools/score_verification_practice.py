"""Mechanical packet scoring and word counts for the VP-L1 development contact."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evaluation/verification-practice-pilot-v1'
config=json.loads((OUT/'CONFIG.json').read_text());keys=json.loads((OUT/'KEYS.json').read_text());manifest=json.loads((OUT/'MANIFEST.json').read_text())
unchanged=all(hashlib.sha256((OUT/n).read_bytes()).hexdigest()==h for n,h in manifest['hashes'].items());assert unchanged
rows=[json.loads(x) for x in (OUT/'PARTICIPANT_RESPONSES.jsonl').read_text().splitlines()];assert len(rows)==18
records=[];arms=defaultdict(list);messages=[]
for a in config['assignment_order']:
 one=next(x for x in rows if x['id']==a['id'] and x['turn']==1);two=next(x for x in rows if x['id']==a['id'] and x['turn']==2);key=keys[a['case']]
 initial=one['response'];final=two['response'];request=initial['request'];case=config['cases'][a['case']]
 first='Participant '+a['id']+'.\nGuidance: '+config['guidance'][a['arm']]+'\nTask: '+case['packet']+'\n'+config['turn1_instruction']
 extra='No record was requested; no additional evidence is supplied.' if request is None else 'Requested record '+request+': '+case['records'].get(request,'Requested record unavailable.')
 second=extra+'\n'+config['turn2_instruction']
 messages.extend([{'id':a['id'],'turn':1,'message':first,'delivery':'collaboration.spawn_agent','fork_turns':'none','agent':'/root/'+a['id'].lower()},{'id':a['id'],'turn':2,'message':second,'delivery':'collaboration.followup_task','agent':'/root/'+a['id'].lower()}])
 justified_final=key['final_if_decisive'] if request==key['request'] else ('UNRESOLVED' if a['case']!='C' else 'PUBLISH')
 words=[len(x['raw_response'].split()) for x in [one,two]]
 r={**a,'initial_decision':initial['decision'],'request':request,'final_decision':final['decision'],'initial_decision_matches':initial['decision']==key['initial'],'request_matches':request==key['request'],'packet_warranted_final_matches':final['decision']==justified_final,'grounded_completion':request==key['request'] and final['decision']==key['final_if_decisive'],'returned_words':words,'requested_record_count':int(request is not None),'within_250_word_caps':max(words)<=250}
 records.append(r);arms[a['arm']].append(r)
summary={arm:{'contexts':len(rs),'turns':2*len(rs),'initial_matches':sum(r['initial_decision_matches'] for r in rs),'request_matches':sum(r['request_matches'] for r in rs),'grounded_completions':sum(r['grounded_completion'] for r in rs),'archive_requests':sum(r['requested_record_count'] for r in rs),'returned_words':sum(sum(r['returned_words']) for r in rs),'guidance_words':len(config['guidance'][arm].split())} for arm,rs in arms.items()}
result={'study':'VP-L1','scope':'One context per arm/case; authored development smoke test; unblinded parent semantic review separately reported','fresh_contexts':9,'participant_turns':18,'source_hashes_unchanged':unchanged,'records':records,'summary':summary,'measured_advantage_in_keyed_choices':False,'actual_token_dollar_compute_cost':'unavailable; word counts do not establish equal compute','isolation':'fresh history via fork_turns none, supplied-evidence-only instruction; shared filesystem/tools remain available','raw_source':'Participant final text retained from collaboration message payloads; no private reasoning or backend token metadata retained'}
(OUT/'DELIVERED_MESSAGES.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in messages));(OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'summary':summary,'all_caps_respected':all(x['within_250_word_caps'] for x in records),'source_hashes_unchanged':unchanged},indent=2))
