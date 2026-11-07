"""Independent final checks, run after the main block pauses; no model inference."""
from pathlib import Path
import base64,json,sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parent/'source-access-three-cycle-v1')]
from world import World,sha,stable,action,immutable
from run import R,read,records,validate

def main():
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
 assert read(R/'STATE.json')['paused'] and (R/'PAUSE').exists() and not (R/'RUN.lock').exists() and not (R/'PENDING.json').exists()
 rows=records();assert len(rows)==100 and [r['entry'] for r in rows]==list(range(751,851))
 assert [read(p)['next_entry'] for p in sorted(R.glob('CHECK_*.json'))]==list(range(760,851,10))
 assert [read(p)['through_entry'] for p in sorted(R.glob('REPORT_*.json'))]==list(range(770,851,20))
 # Every externally retained content-addressed byte object validates independently.
 objects=list((R/'objects').glob('*.json'))
 for p in objects:
  obj=read(p);b=base64.b64decode(obj['base64'],validate=True);assert sha(b)==obj['sha256']==p.stem and len(b)==obj['bytes']
 for row in rows:
  raw=read(R/'raw'/f"{row['entry']:06d}.json")
  assert raw['stop']==row['stop']
  assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
 w=World()
 try:
  bundle=read(R/'bundles/000850.json');assert read(R/'PAUSED_WORLD.json')==bundle
  w.restore(bundle,R/'objects');check=validate(w,tok)
 finally:w.close()
 # When all entries are notebook writes, verify exact accumulated bytes, not just receipts.
 notebook_exact=None
 if all(r['result']['kind']=='notebook' and r['visible_feedback'] is None for r in rows):
  def data(bundle):
   row=next(r for r in bundle['entries'] if r[0]=='notebook.txt' and r[1]=='file')
   return base64.b64decode(read(R/'objects'/(row[3]+'.json'))['base64'])
  expected=data(read(R/'bundles/000750.json'))
  for r in rows:
   expected+=(r['text']+'\n').encode();assert data(read(R/'bundles'/f"{r['entry']:06d}.json"))==expected
  notebook_exact=True
 immutable(H/'INDEPENDENT_FINAL_CHECK.json',dict(status='pass',entry=850,entries=100,checkpoints=10,reports=5,
    primary_history_unchanged=True,all_content_objects_validated=len(objects),fresh_mount_restoration=True,
    all_stop_labels_verified=True,notebook_bytes_reconstructed=notebook_exact,
    local_model_calls=0,weights_verified='disk hash; in-memory tensor invariance checked by main runner',runner_check=check))
 print('Independent final checks passed')
if __name__=='__main__':main()
