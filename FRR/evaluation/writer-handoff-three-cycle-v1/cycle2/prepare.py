from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parent
w={x['id']:x['text'] for x in json.loads((ROOT/'cycle1/WRITER_OUTPUTS.json').read_text())};queries=json.loads((ROOT/'QUERIES.json').read_text())
guide='Track evidence scope, changes, uncertainty and meaningful relationships. Use only this packet and one supplied reply. Do not use tools, files, web or other agents. This is a fictional read-only task. The handoff was produced by a prior assistant from a source ledger and may be incomplete. Keep each reply within300words.\n'
packets={}
for rid,writer,access in [('WH01','W90',False),('WH02','W180',True),('WH03','W90',True),('WH04','W180',False)]:
 policy='The original source ledger is available for one lookup if you request ORIGINAL.' if access else 'The original source ledger is not available in this condition; no original lookup can be supplied.'
 prompt=guide+'\nACCESS\n'+policy+'\n\nHANDOFF\n'+w[writer]+'\n\nQUESTIONS\n'+json.dumps(queries,ensure_ascii=False,indent=2)+'\n\nFirst reply: JSON with request_original boolean and answers list containing id, answer and basis. One followup will return the requested source if permitted, or no new evidence. Final reply: JSON answers list with id, answer, source and basis.\n'
 packets[rid]={'writer':writer,'original_access':access,'prompt':prompt}
(D/'READER_PACKETS.json').write_text(json.dumps(packets,indent=2,ensure_ascii=False)+'\n');(D/'PACKET_HASHES.json').write_text(json.dumps({'READER_PACKETS.json':hashlib.sha256((D/'READER_PACKETS.json').read_bytes()).hexdigest(),'WRITER_OUTPUTS.json':hashlib.sha256((ROOT/'cycle1/WRITER_OUTPUTS.json').read_bytes()).hexdigest(),'QUERIES.json':hashlib.sha256((ROOT/'QUERIES.json').read_bytes()).hexdigest()},indent=2)+'\n')
for rid,v in packets.items():print(rid+'\n'+v['prompt'])
