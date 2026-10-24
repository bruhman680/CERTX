from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[3];D=R/'evaluation/record-access-bridge-v1'
responses=json.loads((D/'RESPONSES.json').read_text());packets=json.loads((D/'PACKETS.json').read_text());second=json.loads((D/'SECOND_MESSAGES.json').read_text());hashes=json.loads((D/'PACKET_HASHES.json').read_text());errors=[];totals={'contexts':len(responses),'participant_turns':2*len(responses),'record_requests':0,'final_decisions':0,'grounded_rejections':0,'appropriate_unresolved':0};rows=[]
for r in responses:
 rid=r['id'];request=r['first']['requests'];totals['record_requests']+=len(request)
 expected_message='Requested records:\n'+'\n\n'.join(packets[rid]['lookup_payloads'][k] for k in request)+'\n\nReturn your final JSON decisions for A, B and C using the available evidence.\n'
 if second[rid]!=expected_message:errors.append(rid+': delivered evidence mismatch')
 if json.loads(r['first_text'])!=r['first'] or json.loads(r['final_text'])!=r['final']:errors.append(rid+': text/parsed mismatch')
 if len(request)!=len(set(request)) or set(request)!=set('ABC'):errors.append(rid+': actual requests differ')
 cases={x['task']:x for x in r['final']['decisions']}
 if len(r['final']['decisions'])!=3 or set(cases)!=set('ABC'):errors.append(rid+': case schema')
 for k in 'ABC':
  totals['final_decisions']+=1
  z=cases[k]
  if z['decision']!={'A':'reject','B':'unresolved','C':'unresolved'}[k]:errors.append(rid+': verdict '+k)
  if k=='A':totals['grounded_rejections']+=z['decision']=='reject'
  else:totals['appropriate_unresolved']+=z['decision']=='unresolved'
 rows.append({'id':rid,'format':packets[rid]['format'],'first_words':len(r['first_text'].split()),'final_words':len(r['final_text'].split()),'delivered_exact_requested_payloads':second[rid]==expected_message})
for p,h in hashes.items():
 if hashlib.sha256((D/p).read_bytes()).hexdigest()!=h:errors.append('frozen source changed:'+p)
checks={'saved_transcript_and_delivery_consistent':not errors,'expected_counts':totals=={'contexts':4,'participant_turns':8,'record_requests':12,'final_decisions':12,'grounded_rejections':4,'appropriate_unresolved':8}}
out={'scope':'Saved transcript/delivery audit; manual semantic judgments reported separately; no participant recontact','totals':totals,'rows':rows,'checks':checks,'errors':errors,'sha256':{p:hashlib.sha256((D/p).read_bytes()).hexdigest() for p in ['PROTOCOL.md','PACKETS.json','FACTS.json','RESPONSES.json','SECOND_MESSAGES.json','RESULTS.json']}}
Path(__file__).with_name('OUTCOME_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
