"""Read-only stimulus audit; creates a new receipt, no model calls or changes to freeze."""
from pathlib import Path
import os,json
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
from design import cases
R=Path(__file__).resolve().parent
def main():
 tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
 qs=json.loads((R/'QUERIES.json').read_text());saved=json.loads((R/'TOKENIZATION.json').read_text());by={c['id']:c for c in cases()};rows=[]
 for q in qs:
  if q['condition']=='legacy_anchor':continue
  c=by[q['case_id']];text=tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=False,add_generation_prompt=True);encoded=tok(text,add_special_tokens=False,return_offsets_mapping=True)
  assert encoded['input_ids']==saved['input_token_ids'][q['run_id']]
  begin=text.index(c['prompt']);end=begin+len(c['prompt']);rb=begin+c['prompt'].index(c['record']);re=rb+len(c['record'])
  def span(a,b):
   hit=[i for i,(x,y) in enumerate(encoded['offset_mapping']) if y>x and y>a and x<b];assert hit;return [min(hit),max(hit)+1]
  rows.append({'run_id':q['run_id'],'case_id':q['case_id'],'condition':q['condition'],'split':q['split'],'content':q['content'],'authority':q['authority'],'placement':q['placement'],'input_tokens':len(encoded['input_ids']),'original_span':span(begin,end),'original_record_span':span(rb,re),'padding_units':q['padding_units']})
 ix={(q['case_id'],q['content'],q['authority'],q['placement']):q for q in rows if q['content'] in ('duplicate','filler')}
 deltas=[]
 for key,row in ix.items():
  c,k,a,p=key
  if not a:
   other=ix[c,k,True,p];deltas.append({'case_id':c,'content':k,'placement':p,'original_record_start_shift_authority_minus_none':other['original_record_span'][0]-row['original_record_span'][0]})
 result={'scope':'Observed token positions in frozen stimuli, no model mechanism inference','rows':rows,'authority_position_deltas':deltas}
 with (R/'SPAN_AUDIT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps({'status':'pass','fresh_prompts':len(rows),'original_record_start_shifts':{p:sorted({d['original_record_start_shift_authority_minus_none'] for d in deltas if d['placement']==p}) for p in ('before','after')}}))
if __name__=='__main__':main()
