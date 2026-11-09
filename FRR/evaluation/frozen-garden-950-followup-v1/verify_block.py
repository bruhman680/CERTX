"""External bounded-block verification, never imported by frozen controller."""
from pathlib import Path
import argparse,base64,json,sys
H=Path(__file__).resolve().parent;PHASE=H.parent/'final-garden-contract-v1';sys.path.insert(0,str(PHASE))
import runner as control
from world import World,immutable

def main(start,end):
 r=control.R;s=control.state();assert s['paused'] and s['next_entry']==end
 assert (r/'PAUSE').exists() and not (r/'RUN.lock').exists() and not (r/'PENDING.json').exists()
 sessions=[control.read(p) for p in (r/'sessions').glob('*_RESULT.json')]
 session=next(x for x in sessions if x['start']==start and x['target']==end)
 assert session['actual_end']==end and session['calls']==end-start and session['reason']=='completed'
 rows=[x for x in control.rows() if start<x['entry']<=end];assert [x['entry'] for x in rows]==list(range(start+1,end+1))
 reports=[control.read(p) for p in sorted((r/'reports').glob('*.json')) if start<int(p.stem.split('_')[-1])<=end]
 assert sum(x['entries'] for x in reports)==end-start and reports[-1]['through_entry']==end
 for n in range(start+10,end+1,10):assert control.read(r/'checks'/f'{n:06d}.json')['status']=='pass'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(control.BASE,local_files_only=True,trust_remote_code=False)
 w=World()
 try:
  after=control.read(r/'bundles'/f'{end:06d}.json');w.restore(after,r/'objects');checked=control.validate(w,tok)
 finally:w.close()
 exact_notebook=False
 if all(x['result']['kind']=='notebook' and x['visible_feedback'] is None for x in rows):
  def data(n):
   b=control.read(r/'bundles'/f'{n:06d}.json');entry=next(e for e in b['entries'] if e[0]=='notebook.txt' and e[1]=='file')
   return base64.b64decode(control.read(r/'objects'/(entry[3]+'.json'))['base64'],validate=True)
  expected=data(start)
  for row in rows:
   expected+=(row['text']+'\n').encode();assert expected==data(row['entry'])
  exact_notebook=True
 faults=sum(x['result']['kind']=='notebook' and x['visible_feedback'] is not None for x in rows)
 checknames=[p for p in (r/'checks').glob('*.json') if start<int(p.stem)<=end]
 result={'status':'pass','start_entry':start,'end_entry':end,'new_model_calls':len(rows),'observer_model_calls':0,'regular_checks':(end-start)//10,'all_checks':len(checknames),'reports':reports,'frozen_configuration_preserved':True,'known_session_outcome':session['reason'],'pending_or_lock':False,'notebook_storage_faults':faults,'notebook_bytes_reconstructed':exact_notebook,'controller_verification':checked,'eligible_for_wider_observer_cadence':faults==0,'scope':'Fresh restore uses pinned shareddecoder; direct notebookbyte reconstruction is additional. Stability concerns integrity and knownoperationaloutcomes, not a requirement for novelty or useful action.'}
 immutable(H/f'VERIFIED_{start:06d}_{end:06d}.json',result);print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True);a=p.parse_args();main(a.start,a.end)
