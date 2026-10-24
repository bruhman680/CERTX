from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[3]
D=R/'evaluation/record-access-bridge-v1'
facts=json.loads((D/'FACTS.json').read_text());packets=json.loads((D/'PACKETS.json').read_text());hashes=json.loads((D/'PACKET_HASHES.json').read_text());errors=[];counts={}
for rid,p in packets.items():
 s=p['prompt'];body=s.split('TASK RECORDS\n',1)[1].split('\nFirst reply:',1)[0]
 if p['format']=='structured':tasks=json.loads(body)
 else:tasks=[json.loads(line.split(': ',1)[1]) for line in body.splitlines()]
 if tasks!=facts['tasks']:errors.append(rid+': task mismatch')
 for k,raw in p['lookup_payloads'].items():
  if p['format']=='structured':record=json.loads(raw)
  else:record={name:json.loads(value) for name,value in (line.split(' = ',1) for line in raw.splitlines())}
  if record!=facts['records'][k]:errors.append(rid+': lookup mismatch '+k)
 counts[rid]={'format':p['format'],'prompt_words':len(s.split()),'prompt_characters':len(s),'lookup_words':{k:len(v.split()) for k,v in p['lookup_payloads'].items()}}
if len({p['prompt'].split('TASK RECORDS\n',1)[0] for p in packets.values()})!=1:errors.append('guidance mismatch')
for name,h in hashes.items():
 if hashlib.sha256((D/name).read_bytes()).hexdigest()!=h:errors.append('binding mismatch '+name)
checks={'all_format_renderings_preserve_facts':not errors,'four_context_packets':len(packets)==4,'two_each_format':sum(p['format']=='raw' for p in packets.values())==2 and sum(p['format']=='structured' for p in packets.values())==2}
out={'scope':'Prospective packet/source equivalence check, not participant outcome or format efficacy','counts':counts,'checks':checks,'errors':errors,'interpretation_limits':['Fixed allocation order, not randomized format assignment','12 task decisions clustered in4contexts','Visible revision/run/status cues; authored development only','Instructional isolation is not physical tool/access isolation','Different prompt/followup word and character lengths are part of the rendering contrast, not equal compute']}
Path(__file__).with_name('PACKET_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
