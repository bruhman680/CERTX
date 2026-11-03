"""External attention allocation only. Never changes model inputs or raw files."""
import re,hashlib,statistics,json
from pathlib import Path
MARKERS=('<<<','>>>','Feedback:','CURRENT patch:','Next response:','Notebook:','Observation:')
def norm(text):return re.sub(r'\d+','<N>',' '.join(text.lower().split()))
def form(text):
 if text.strip() in ('YES','NO','WITHHOLD','UNKNOWN'):return 'label'
 if any(m in text for m in MARKERS):return 'record'
 return 'prose' if len(text.split())>=8 else 'short_other'
def index(parent,new,stops):
 out=[]
 for r in new:
  same=[x for x in parent if (x['episode'],x['seed'],x['arm'])==(r['episode'],r['seed'],r['arm'])];tail=same[-5:];knownforms={form(x['text']) for x in tail};questions={norm(x['text']) for x in same if '?' in x['text']};f=[]
  if form(r['text']) not in knownforms:f.append('new_coarse_form')
  if '?' in r['text'] and norm(r['text']) not in questions:f.append('new_question_string')
  median=statistics.median([len(x['generated_token_ids']) for x in tail]) if tail else 0
  if len(r['generated_token_ids'])>=max(32,2*median):f.append('length_surge')
  if len(r['input_token_ids'])>=.9*3072 and not any(len(x['input_token_ids'])>=.9*3072 for x in tail):f.append('input_pressure_crossing')
  if r['stop']=='token_limit' and not any(x['stop']=='token_limit' for x in tail):f.append('new_output_cap')
  peers=[x for x in new if (x['episode'],x['seed'],x['arm'])==(r['episode'],r['seed'],r['arm'])]
  pnew=sum(form(x['text'])==form(r['text']) for x in peers)/len(peers);pold=sum(form(x['text'])==form(r['text']) for x in tail)/len(tail) if tail else 0
  if abs(pnew-pold)>=.4:f.append('window_form_shift')
  out.append(dict(run_id=r['run_id'],episode=r['episode'],seed=r['seed'],step=r['step'],arm=r['arm'],form=form(r['text']),input_tokens=len(r['input_token_ids']),output_tokens=len(r['generated_token_ids']),stop=r['stop'],flags=f))
 rank={'input_pressure_crossing':0,'new_question_string':1,'new_coarse_form':2,'window_form_shift':3,'length_surge':4,'new_output_cap':5}
 flagged=[x for x in out if x['flags']];flagged.sort(key=lambda x:(min(rank[k] for k in x['flags']),hashlib.sha256(('observer-v1:'+x['run_id']).encode()).hexdigest()))
 selected=flagged[:6];quiet=[x for x in out if not x['flags']];sample=min(quiet,key=lambda x:hashlib.sha256(('quiet-v1:'+x['run_id']).encode()).hexdigest()) if quiet else None
 return dict(policy='observer-v1-budget3072; uncalibrated attention heuristics, no phase/truth claim',rows=out,selected_flagged_ids=[x['run_id'] for x in selected],quiet_sample_id=sample['run_id'] if sample else None,flagged_total=len(flagged),flagged_not_selected=max(0,len(flagged)-6),boundary_events=stops)
def main():
 r=Path(__file__).resolve().parent;p=r.parent/'open-garden-return-v1';load=lambda f:[json.loads(s) for s in f.read_text().splitlines()]
 parent=load(p/'run/RAW.jsonl');new=load(r/'run/RAW.jsonl');m=json.loads((r/'run/RUN_MANIFEST.json').read_text());result=index(parent,new,m['stops']);assert len(result['rows'])==len(new)
 with (r/'EVENT_INDEX.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 ids=set(result['selected_flagged_ids']);ids.add(result['quiet_sample_id']);selected=[x for x in new if x['run_id'] in ids]
 with (r/'REVIEW_SAMPLE.json').open('x') as f:json.dump(selected,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
