from pathlib import Path
import json,collections
H=Path(__file__).resolve().parent;R=H/'run'
def main():
 rows=[json.loads(p.read_text()) for p in sorted((R/'events').glob('*.json'))]
 assert len(rows)==100 and rows[-1]['entry']==850
 texts=[r['text'] for r in rows];longest=0;current=0;prev=None
 for text in texts:
  current=current+1 if text==prev else 1;longest=max(longest,current);prev=text
 result={'entry_range':[751,850],'entries':len(rows),'model':'cached SmolLM2-135M-Instruct, no added adapter',
   'host_kinds':dict(collections.Counter(r['result']['kind'] for r in rows)),
   'stops':dict(collections.Counter(r['stop'] for r in rows)),
   'unique_texts':len(set(texts)),'longest_adjacent_identical_run':longest,
   'notebook_storage_faults':sum(r['result']['kind']=='notebook' and r['visible_feedback'] is not None for r in rows),
   'shell_exit_codes':[r['result']['feedback']['exit_code'] for r in rows if r['result']['kind']=='shell'],
   'texts_containing_code_fences':sum('```' in t for t in texts),
   'twenty_entry_reports':[json.loads(p.read_text()) for p in sorted(R.glob('REPORT_*.json'))],
   'examples':[{'entry':r['entry'],'text':r['text'],'kind':r['result']['kind']} for r in rows[::20]],
   'interpretation_limits':['Notebook writing is not itself failed action','Code-looking notebook text is not evidence of an executed program','Generated explanations are not verified private reasoning','Finite text variation or repetition does not demonstrate learning, agency, emergence or internal stabilization','No training updates; inherited tokenizer system header remains; no causal attribution across simultaneous condition changes']}
 with (H/'ANALYSIS.json').open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['examples','interpretation_limits','twenty_entry_reports']}))
if __name__=='__main__':main()
