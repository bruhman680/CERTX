"""Posthoc exact-line recurrence aid for reviewer attention, not semantic novelty."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parent
STAGES=('carried-garden-exploration-v1','open-notebook-continuation-v1','open-garden-three-batches-v1','selective-observation-v1','open-garden-settling-v1','open-garden-return-v1','open-garden-continuation-v2')
def normalized(line):return re.sub(r'\d+','<N>',' '.join(line.strip().strip('|').lower().split()))
def main():
 registry={};current=[];pins={}
 for stage in STAGES:
  p=R.parent/stage/'run/RAW.jsonl';pins[stage]=hashlib.sha256(p.read_bytes()).hexdigest()
  for row in [json.loads(s) for s in p.read_text().splitlines()]:
   for line in row['text'].splitlines():
    if '?' not in line:continue
    key=normalized(line);prior=registry.get(key);entry=dict(stage=stage,run_id=row['run_id'],line=line)
    if stage==R.name:current.append(dict(**entry,seen_in_earlier_stage=bool(prior and prior['stage']!=stage),first_seen=prior or entry))
    if key not in registry:registry[key]=entry
 with (R/'QUESTION_RECURRENCE.json').open('x') as f:json.dump(dict(scope='Posthoc global exact normalized question-line lookup; not semantic novelty or per-trajectory prior exposure',source_sha256=pins,current=current,registry=registry),f,indent=2);f.write('\n')
 print(json.dumps(current,indent=2))
if __name__=='__main__':main()
