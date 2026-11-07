"""Corruption probes on a disposable frozen checkpoint copy; no live writes."""
from pathlib import Path
import json,shutil,tempfile,sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parent/'source-access-three-cycle-v1')]
import run as engine
from world import World,immutable

def main():
 from transformers import AutoTokenizer
 source=H/'run';through=780
 assert (source/f'CHECK_{through:06d}.json').exists()
 tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
 with tempfile.TemporaryDirectory() as t:
  target=Path(t)/'run';target.mkdir()
  for name in ['MANIFEST.json','PRIMARY_INVENTORY.json','MODEL_CONDITION.json']:shutil.copyfile(source/name,target/name)
  for name in ['events','raw','results','plans','bundles']:
   (target/name).mkdir()
   for p in sorted((source/name).glob('*.json')):
    if int(p.stem)<=through:shutil.copyfile(p,target/name/p.name)
  shutil.copytree(source/'objects',target/'objects')
  last=target/'events'/f'{through:06d}.json'
  (target/'STATE.json').write_text(json.dumps(dict(next_entry=through,paused=True,latest_bundle=f'{through:06d}.json',last_event_sha256=engine.disksha(last))))
  engine.R=target;w=World()
  try:
   w.restore(engine.read(target/'bundles'/f'{through:06d}.json'),target/'objects')
   baseline=engine.validate(w,tok);assert baseline['status']=='pass'
   probes=[]
   cases=[('raw_content','raw/000751.json','text','tampered'),
     ('plan_manifest','plans/000751.json','manifest_sha256','wrong'),
     ('state_bundle_pointer','STATE.json','latest_bundle','000750.json'),
     ('event_parent','events/000752.json','parent_event_sha256','wrong'),
     ('result_kind','results/000751.json','kind','shell')]
   for name,relative,key,value in cases:
    p=target/relative;before=p.read_bytes();obj=json.loads(before);obj[key]=value;p.write_text(json.dumps(obj))
    caught=False
    try:engine.validate(w,tok)
    except (AssertionError,KeyError):caught=True
    finally:p.write_bytes(before)
    assert caught,name;probes.append({'corruption':name,'detected':True})
   assert engine.validate(w,tok)['status']=='pass'
  finally:w.close()
 immutable(H/'JOURNAL_CORRUPTION_PROBES.json',dict(status='pass',checkpoint=through,disposable_copy_only=True,model_calls=0,corruptions=probes))
 print('Five journal corruption probes detected; live records untouched')
if __name__=='__main__':main()
