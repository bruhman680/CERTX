"""External observer verifier; never imported by the frozen model controller."""
from pathlib import Path
import base64,json,sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H)]
import runner as controller
from world import World,immutable

def main():
 from transformers import AutoTokenizer
 r=controller.R;s=controller.state();assert s['next_entry']==950 and s['paused']
 assert (r/'PAUSE').exists() and not (r/'RUN.lock').exists() and not (r/'PENDING.json').exists()
 rows=controller.rows();assert [x['entry'] for x in rows]==list(range(851,951))
 checks={int(p.stem):controller.read(p) for p in (r/'checks').glob('*.json')}
 assert all(n in checks and checks[n]['status']=='pass' for n in range(860,951,10))
 reports=[controller.read(p) for p in sorted((r/'reports').glob('*.json'))]
 assert [p['through_entry'] for p in reports]==[900,950]
 assert all(p['entries']==50 for p in reports)
 resultfiles=list((r/'sessions').glob('*_RESULT.json'));assert len(resultfiles)==1
 result=controller.read(resultfiles[0]);assert result['calls']==100 and result['actual_end']==950 and result['reason']=='completed'
 tok=AutoTokenizer.from_pretrained(controller.BASE,local_files_only=True,trust_remote_code=False)
 w=World()
 try:
  final=controller.read(r/'bundles/000950.json');w.restore(final,r/'objects');check=controller.validate(w,tok)
 finally:w.close()
 # Direct notebook-byte reconstruction when writing was ordinary, successful,
 # and the model made no explicit shell changes to its notebook.
 notebook_bytes=None
 if all(x['result']['kind']=='notebook' and x['visible_feedback'] is None for x in rows):
  def notebook(bundle):
   entry=next(x for x in bundle['entries'] if x[0]=='notebook.txt' and x[1]=='file')
   q=controller.read(r/'objects'/(entry[3]+'.json'));return base64.b64decode(q['base64'],validate=True)
  value=notebook(controller.read(r/'bundles/000850.json'))
  for x in rows:
   value+=(x['text']+'\n').encode();assert notebook(controller.read(r/'bundles'/f"{x['entry']:06d}.json"))==value
  notebook_bytes=len(value)
 first=controller.read(r/'raw/000851.json');expected=controller.parent_rows()[-12:]
 assert [x['content'] for x in first['messages'] if x['role']=='assistant']==[x['text'] for x in expected]
 assert first['messages'][0]=={'role':'system','content':''}
 decoded=tok.decode(first['input_token_ids']);assert decoded.startswith('<|im_start|>system\n<|im_end|>\n')
 immutable(H/'OBSERVER_FINAL_VERIFICATION.json',{'status':'pass','from_entry':851,'through_entry':950,'model_calls_by_verifier':0,'block_model_calls':100,'regular_integrity_checks':10,'all_integrity_checks_including_zooms':len(checks),'reports':2,'world_restored_in_fresh_namespace':True,'complete_notebook_bytes_reconstructed':notebook_bytes,'first_reply_inherits_entries':[839,850],'factory_instruction_not_inserted':True,'operator_design_pins_unchanged':True,'parent_stages_preserved':True,'controller_verification':check,'independence_scope':'Separate observer pass and direct notebook-byte reconstruction; shared pinned checkpoint decoder is not an independent filesystem implementation.'})
 print('External final verification passed')
if __name__=='__main__':main()
