"""Summarize all retained outcomes without rerunning inference/actions."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
def main():
 r=json.loads((H/'RESULTS.json').read_text());rows=r['rows'];groups={}
 for p in [.9,1.0]:
  rr=[x for x in rows if x['case_id'].startswith(f'decode_p{int(p*100)}_')]
  groups[str(p)]={'replies':len(rr),'distinct_output_texts':len({x['text_sha256'] for x in rr}),
    'complete_cells':sum(x['complete_cells'] for x in rr),'eos':sum(x['stop']=='eos' for x in rr),
    'model_code_operations':sum(o['channel']!='note' for x in rr for o in x['operations'])}
 profile=json.loads((H/'decoder/NUCLEUS_PROFILE.json').read_text())
 (H/'decoder/READOUT.json').write_text(json.dumps({'sampling':groups,'profile':{k:v for k,v in profile.items() if k!='rows'}},indent=2)+'\n')
 retrieval_rows=[x for x in rows if x['case_id'].startswith('retrieval_')]
 retrieval_seen=[]
 for x in retrieval_rows:
  target=x['metadata']['expected_value']
  raw=json.loads((H/'results'/x['case_id']/f"raw{x['turn']}.json").read_text())
  outputs=[o['feedback']['stdout'] for o in x['operations'] if o['channel']!='note' and o['feedback'] is not None]
  retrieval_seen.append(target in raw['text'] or any(target in s for s in outputs))
 total={'actual_model_generations':len(rows),'extra_teacher_forced_forward_passes':r['teacher_forced_profile_passes'],
  'model_code_operations':sum(o['channel']!='note' for x in rows for o in x['operations']),
  'canonical_unchanged':r['canonical_unchanged'],'weights_unchanged':r['weights_unchanged'],'main_entry':1580,
  'observations':{'cases':3,'distinct_input_hashes':len({x['input_sha256'] for x in rows if x['case_id'].startswith('obs_')}),
    'distinct_output_hashes':len({x['text_sha256'] for x in rows if x['case_id'].startswith('obs_')})},
  'decoder':groups,'retrieval':{'branches':len({x['case_id'] for x in retrieval_rows}),'replies':len(retrieval_rows),
    'target_seen_in_text_or_stdout':any(retrieval_seen),'replies_with_target_in_text_or_stdout':sum(retrieval_seen)},
  'activation':False,'background_work':False}
 (H/'SUMMARY.json').write_text(json.dumps(total,indent=2)+'\n')
if __name__=='__main__':main()
