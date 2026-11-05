"""Standalone host journal for fixtures/demos; not the primary notebook authority."""
from pathlib import Path
from dataclasses import asdict
from contextlib import contextmanager
import json,os
from world import Rules,transition,digest

def immutable(path,value):
 path=Path(path);tmp=path.with_name(path.name+'.staging-'+str(os.getpid()));data=(json.dumps(value,sort_keys=True,ensure_ascii=False)+'\n').encode()
 with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 try:os.link(tmp,path)
 finally:tmp.unlink(missing_ok=True)
def project(path,value):
 path=Path(path);tmp=path.with_name(path.name+'.projection-'+str(os.getpid()))
 with tmp.open('x') as f:json.dump(value,f,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)
@contextmanager
def lock(path):
 p=Path(path)/'WRITE.lock';fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:yield
 finally:p.unlink()
class Journal:
 def __init__(self,path):self.path=Path(path)
 @classmethod
 def create(cls,path,rules=Rules()):
  rules.validate();p=Path(path)
  if p.exists() and any(p.iterdir()):raise FileExistsError('Nonempty world directory; no reset/overwrite')
  p.mkdir(parents=True,exist_ok=True);(p/'events').mkdir();immutable(p/'CONFIG.json',dict(kind='host_demo_or_fixture_world',rules=asdict(rules),rules_sha256=rules.fingerprint()));j=cls(p);j.recover();return j
 def rules(self):
  cfg=json.loads((self.path/'CONFIG.json').read_text());r=Rules(**cfg['rules']);r.validate()
  if cfg['rules_sha256']!=r.fingerprint():raise ValueError('Rules fingerprint mismatch')
  return r
 def replay(self):
  r=self.rules();value=r.initial;parent=r.fingerprint();rows=[]
  for i,p in enumerate(sorted((self.path/'events').glob('*.json'))):
   x=json.loads(p.read_text());expected_value,expected=transition(value,x['reply'],r)
   if p.stem!=f'{i:06d}' or x['sequence']!=i or x['parent_sha256']!=parent or x['receipt']!=expected or x['rules_sha256']!=r.fingerprint():raise ValueError('Invalid world journal transition/hash chain')
   content={k:v for k,v in x.items() if k!='event_sha256'}
   if x['event_sha256']!=digest(content):raise ValueError('Event hash mismatch')
   parent=x['event_sha256'];value=expected_value;rows.append(x)
  return dict(number=value,events=len(rows),head_sha256=parent,rules_sha256=r.fingerprint()),rows
 def recover(self):
  with lock(self.path):state,_=self.replay();project(self.path/'STATE.json',state)
  return state
 def apply(self,reply,*,simulate_projection_failure=False):
  with lock(self.path):
   state,rows=self.replay();r=self.rules();_,receipt=transition(state['number'],reply,r);x=dict(sequence=len(rows),reply=reply,receipt=receipt,parent_sha256=state['head_sha256'],rules_sha256=r.fingerprint());x['event_sha256']=digest(x);immutable(self.path/'events'/f'{len(rows):06d}.json',x)
   if simulate_projection_failure:raise RuntimeError('Injected failure after durable event, before projection')
   after,_=self.replay();project(self.path/'STATE.json',after)
  return receipt
