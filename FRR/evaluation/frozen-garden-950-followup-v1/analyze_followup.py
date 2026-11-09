"""External descriptive analysis only. Does not modify the frozen controller."""
from pathlib import Path
import argparse,json,collections
H=Path(__file__).resolve().parent;R=H.parent/'final-garden-contract-v1/run'
def main(end):
 allrows=[json.loads(p.read_text()) for p in sorted((R/'events').glob('*.json'))];rows=[x for x in allrows if 950<x['entry']<=end]
 assert len(rows)==end-950 and json.loads((R/'STATE.json').read_text())['paused']
 def describe(batch):
  texts=[x['text'] for x in batch];longest=0;streak=0;previous=None
  for text in texts:streak=streak+1 if text==previous else 1;longest=max(longest,streak);previous=text
  return {'entries':len(batch),'range':[batch[0]['entry'],batch[-1]['entry']],'kinds':dict(collections.Counter(x['result']['kind'] for x in batch)),'stops':dict(collections.Counter(x['stop'] for x in batch)),'distinct_texts':len(set(texts)),'longest_exact_adjacent_repeat':longest,'directory_list_replies':sum(t.startswith('Directory entries:') for t in texts),'storage_faults':sum(x['result']['kind']=='notebook' and x['visible_feedback'] is not None for x in batch),'forms':dict(collections.Counter(texts)) if len(set(texts))<=8 else None}
 intervals=[(950,min(1050,end))]+([(1050,end)] if end>1050 else [])
 info={'status':'descriptive','current_entry':end,'new_entries':end-950,'total_since_final_freeze':end-850,'blocks':[describe([x for x in rows if a<x['entry']<=b]) for a,b in intervals],'overall':describe(rows),'new_operator_design_changes':0,'model_training_updates':0,'reports':[json.loads(p.read_text()) for p in sorted((R/'reports').glob('*.json')) if 950<int(p.stem.split('_')[-1])<=end],'examples':[{'entry':x['entry'],'text':x['text'],'kind':x['result']['kind']} for x in rows[::50]],'interpretation':'Fixed model/world inputrules; counts describe texts and recordedactions, not internal maturity/emotion/learning. External scheduling changed only after a verified100block. No semantic requirement to exitrepetition.'}
 with (H/f'ANALYSIS_THROUGH_{end:06d}.json').open('x') as f:json.dump(info,f,indent=2,ensure_ascii=False);f.write('\n')
 print(json.dumps({k:v for k,v in info.items() if k not in ['reports','examples','interpretation','overall','blocks']}));print(json.dumps(info['overall']))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--end',type=int,required=True);main(p.parse_args().end)
