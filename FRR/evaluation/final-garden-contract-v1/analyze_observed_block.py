"""Descriptive external analysis, not model-visible judgments."""
from pathlib import Path
import json,collections
H=Path(__file__).resolve().parent;R=H/'run'
def main():
 rows=[json.loads(p.read_text()) for p in sorted((R/'events').glob('*.json'))];assert len(rows)==100 and rows[-1]['entry']==950
 texts=[x['text'] for x in rows];longest=0;previous=None;streak=0
 for t in texts:streak=streak+1 if t==previous else 1;longest=max(longest,streak);previous=t
 info={'range':[851,950],'entries':100,'kinds':dict(collections.Counter(x['result']['kind'] for x in rows)),'stops':dict(collections.Counter(x['stop'] for x in rows)),'unique_texts':len(set(texts)),'longest_adjacent_exact_repeat':longest,'empty_replies':sum(not t for t in texts),'directory_phrase_replies':sum('directory entries:' in t.lower() for t in texts),'notebook_storage_faults':sum(x['result']['kind']=='notebook' and x['visible_feedback'] is not None for x in rows),'reports':[json.loads(p.read_text()) for p in sorted((R/'reports').glob('*.json'))],'examples':[{'entry':x['entry'],'text':x['text'],'kind':x['result']['kind']} for x in rows[::20]],'interpretation':'Surface observations under fixed final setup. Different output patterns are not evidence of maturation, emotion, learning or a specific internal mechanism. Final framing differs from previousphase and was held fixed throughout thisblock.'}
 with (H/'OBSERVED_BLOCK_ANALYSIS.json').open('x') as f:json.dump(info,f,indent=2,ensure_ascii=False);f.write('\n')
 print(json.dumps({k:v for k,v in info.items() if k not in ['reports','examples','interpretation']}))
if __name__=='__main__':main()
