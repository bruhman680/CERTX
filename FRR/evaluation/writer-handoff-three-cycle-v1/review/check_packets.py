from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parents[1]
p=json.loads((D/'cycle2/READER_PACKETS.json').read_text());w={x['id']:x['text'] for x in json.loads((D/'cycle1/WRITER_OUTPUTS.json').read_text())};q=json.loads((D/'QUERIES.json').read_text());expected=[('WH01','W90',False),('WH02','W180',True),('WH03','W90',True),('WH04','W180',False)]
checkrows=[]
for rid,writer,access in expected:
 r=p[rid];prompt=r['prompt'];handoff=prompt.split('\n\nHANDOFF\n',1)[1].split('\n\nQUESTIONS\n',1)[0];qs=prompt.split('\n\nQUESTIONS\n',1)[1].split('\n\nFirst reply:',1)[0]
 checkrows.append({'id':rid,'actual_writer_text_preserved':handoff==w[writer],'queries_match':json.loads(qs)==q,'access_policy_matches':r['original_access']==access and ('available for one lookup' in prompt if access else 'not available in this condition' in prompt),'writer_matches':r['writer']==writer,'prompt_words':len(prompt.split()),'characters':len(prompt)})
ph=json.loads((D/'cycle2/PACKET_HASHES.json').read_text());paths={'READER_PACKETS.json':D/'cycle2/READER_PACKETS.json','WRITER_OUTPUTS.json':D/'cycle1/WRITER_OUTPUTS.json','QUERIES.json':D/'QUERIES.json'}
checks={'all_packet_bindings':all(hashlib.sha256(paths[k].read_bytes()).hexdigest()==v for k,v in ph.items()),'all_rendered_fact_checks':all(all(r[k] for k in ['actual_writer_text_preserved','queries_match','access_policy_matches','writer_matches']) for r in checkrows),'same_guidance':len({r['prompt'].split('\nACCESS\n',1)[0] for r in p.values()})==1}
out={'scope':'Reader-packet preservation and source binding, not independent prompt-delivery attestation','checks':checks,'rows':checkrows,'followup_condition':'Original source only if access permitted AND actual first reply requests it; otherwise no new evidence.'}
(D/'review/PACKET_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
