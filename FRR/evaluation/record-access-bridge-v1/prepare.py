from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
TASKS=[{'id':'A','question':'Decide whether shipment P31 meets its release temperature rule.','rule':'Approve iff authoritative maximum temperature is at most8C.','index':{'record':'A','location':'sensor/P31/export','current_revision':2},'summary':{'revision':1,'max_C':7.8}}, {'id':'B','question':'Decide whether release R62 meets its zero-failure rule.','rule':'Approve iff the authoritative test artifact for runR62/checksumK62 reports zero failures.','index':{'record':'B','location':'bench/recent.json','required_run':'R62','required_checksum':'K62'},'summary':{'text':'Previous operation: tests passed.'}}, {'id':'C','question':'Decide whether kit N14 meets its net-mass rule.','rule':'Approve iff the signed mass record for N14 reports at least90kg.','index':{'record':'C','location':'vault/N14/signed_mass'},'summary':{'listed_kg':90}}]
RECORDS={'A':{'record_id':'A','entity':'P31','revision':2,'maximum_C':8.4},'B':{'record_id':'B','artifact_run':'R61','checksum':'K61','failed_tests':0},'C':{'record_id':'C','path':'vault/N14/signed_mass','read_status':'locked','reason':'decryption key unavailable','decoded_content':None}}
GUIDE='Track relationships, source scope and assumptions; distinguish what the evidence supports from what remains unresolved. You are a reader in a fictional read-only task. Use only the packet and one supplied lookup reply. Do not use tools, files, web or other agents. Authority rules are stipulated, not authenticated. Keep each reply within300words.\n'
def render(x,fmt):
 if fmt=='structured':return json.dumps(x,indent=2)
 if isinstance(x,list):return '\n'.join('entry '+str(i+1)+': '+json.dumps(v,separators=(',',':')) for i,v in enumerate(x))
 return '\n'.join(k+' = '+json.dumps(v,separators=(',',':')) for k,v in x.items())
packets={}
for i,fmt in enumerate(['raw','structured','structured','raw'],1):
 rid=f'RA{i:02d}';p=GUIDE+'\nTASK RECORDS\n'+render(TASKS,fmt)+'\nFirst reply: JSON with requests (up to3 unique IDs A/B/C) and preliminary decisions/reasons. A followup will provide only those requested records. Final reply: JSON decisions list with task, decision, evidence_state, source and reason.\n'
 packets[rid]={'format':fmt,'prompt':p,'lookup_payloads':{k:render(v,fmt) for k,v in RECORDS.items()}}
(D/'PACKETS.json').write_text(json.dumps(packets,indent=2)+'\n');(D/'FACTS.json').write_text(json.dumps({'tasks':TASKS,'records':RECORDS},indent=2)+'\n')
(D/'PACKET_HASHES.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'PROTOCOL.md',D/'PACKETS.json',D/'FACTS.json']},indent=2)+'\n')
print(json.dumps({k:{'format':v['format'],'prompt_words':len(v['prompt'].split())} for k,v in packets.items()}))
