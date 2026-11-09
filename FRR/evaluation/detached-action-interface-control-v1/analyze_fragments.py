"""Retrospective text analysis only. Never dispatches an extracted fragment."""
from pathlib import Path
import json
H = Path(__file__).resolve().parent
done = json.loads((H / 'COMPLETED.json').read_text())
target = {'action':'shell','source':'pwd'}
decoder = json.JSONDecoder()
findings = []
for row in done['results']:
    hits = []
    for offset, char in enumerate(row['text']):
        if char!='{':
            continue
        try:
            value,end = decoder.raw_decode(row['text'][offset:])
        except ValueError:
            continue
        if value==target:
            hits.append({'start':offset,'end':offset+end,'literal':row['text'][offset:offset+end]})
    if hits:
        findings.append({'seed':row['seed'],'arm':row['arm'],'whole_reply_action':row['valid_action_envelope'],'target_fragments':hits})
assert all(not r['whole_reply_action'] for r in findings)
observation = {'status':'observed','retrospective':True,'model_calls':0,'fragments_executed':0,
    'trials_with_embedded_target':len(findings),'findings':findings,
    'scope':'Descriptive recognition of complete target JSON as an interior substring. Does not change the parser, main outcomes or model feedback, infer intention, or promote writing to an action.'}
with (H / 'EMBEDDED_JSON_OBSERVATION.json').open('x') as f:
    json.dump(observation,f,indent=2,ensure_ascii=False)
    f.write('\n')
print(json.dumps({'trials_with_embedded_target':len(findings),'fragments_executed':0}))
