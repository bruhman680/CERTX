"""Packet-relative and source-grounded scoring for authored MS-L1 contact."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evaluation/memory-task-shift-v1'
c=json.loads((OUT/'CONFIG.json').read_text());keys=json.loads((OUT/'KEYS.json').read_text());m=json.loads((OUT/'MANIFEST.json').read_text())
unchanged=all(hashlib.sha256((OUT/p).read_bytes()).hexdigest()==h for p,h in m['hashes'].items());assert unchanged
rows=[json.loads(x) for x in (OUT/'RESPONSES.jsonl').read_text().splitlines()];assert len(rows)==16
records=[];groups=defaultdict(list);replies=[]
for a in c['assignment_order']:
 one=next(x for x in rows if x['id']==a['id'] and x['turn']==1);two=next(x for x in rows if x['id']==a['id'] and x['turn']==2);cond=a['condition'];policy=keys['conditions'][cond];truth=keys[a['world']]['truth'];request=one['response']['request']
 has_source=cond=='record_supplied' or(cond=='lookup_current' and request=='RUN')
 initial=truth if cond=='record_supplied' else 'UNRESOLVED';final=truth if has_source else 'UNRESOLVED'
 if request=='RUN' and cond.startswith('lookup'):
  record=c['records'][a['world']]['stale' if cond=='lookup_stale' else 'current']
 else:record='No additional evidence is supplied; no record was requested.' if request is None else 'Record lookup is unavailable.'
 replies.append({'id':a['id'],'agent':'/root/'+a['id'].lower(),'turn':2,'message':record+'\n'+c['turn2']})
 r={**a,'truth':truth,'initial_decision':one['response']['decision'],'request':request,'final_decision':two['response']['decision'],'initial_packet_warrant':one['response']['decision']==initial,'request_matches_policy':request==policy['request'],'final_packet_warrant':two['response']['decision']==final,'grounded_completion':has_source and two['response']['decision']==truth,'appropriate_unresolved':not has_source and two['response']['decision']=='UNRESOLVED','false_certainty':not has_source and two['response']['decision']!='UNRESOLVED','returned_words':[len(x['raw_response'].split()) for x in [one,two]]}
 records.append(r);groups[cond].append(r)
summary={name:{'readers':len(rs),'participant_turns':2*len(rs),'initial_packet_warrant':sum(x['initial_packet_warrant'] for x in rs),'final_packet_warrant':sum(x['final_packet_warrant'] for x in rs),'grounded_completions':sum(x['grounded_completion'] for x in rs),'appropriate_unresolved':sum(x['appropriate_unresolved'] for x in rs),'false_certainty':sum(x['false_certainty'] for x in rs),'requests':sum(x['request'] is not None for x in rs),'returned_words':sum(sum(x['returned_words']) for x in rs)} for name,rs in groups.items()}
result={'study':'MS-L1','scope':'Two constructed worlds with stipulated source accuracy; access-policy contact, not prompt efficacy or internal/long-window memory decay','fresh_contexts':8,'participant_turns':16,'all_planned_responses_retained':True,'launch_hashes_unchanged':unchanged,'summary':summary,'records':records,'all_200_word_caps_respected':all(max(r['returned_words'])<=200 for r in records),'actual_token_dollar_compute_cost':'unavailable','response_capture':'Collaboration final-message payload text plus parsed JSON; no private reasoning/backend metadata','isolation':'fork_turns none plus no-tool/no-file instruction; shared filesystem/tools and model ancestry remain'}
(OUT/'SECOND_MESSAGES.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in replies));(OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'summary':summary,'hashes_unchanged':unchanged},indent=2))
