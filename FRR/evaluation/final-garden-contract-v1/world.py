"""Linux world with hard tmpfs quota, external content-addressed checkpoints."""
from pathlib import Path
import base64, hashlib, json, os, resource, selectors, signal, subprocess, time
import ctypes
# Reap sandbox descendants after namespace shutdown instead of leaving zombies.
assert ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)==0
def reap():
 while True:
  try:
   pid,_=os.waitpid(-1,os.WNOHANG)
   if pid==0:break
  except ChildProcessError:break
H=Path(__file__).resolve().parent
WORLD_BYTES=8*1024*1024
PROCESS_AS=32*1024*1024
PROCESS_COUNT=128
OUTPUT_BYTES=8192
NOTICE='''Files in /world persist. Shell and Python 3 are available. Ordinary replies are saved as notebook writing, not executed. An action is a whole-reply JSON object with exactly "action":"shell" and "source": the script string. Actions return stdout, stderr and exit status. Host research files and network are unavailable. Limits: 8 MiB world storage, 8 MiB temporary storage, 32 MiB address space per process, 128 processes for the shared user, 3 seconds per action, 256 KiB per file and 8192 output bytes. Processes, shell variables and /tmp contents end after each action; /world files persist. Each reply allows up to 96 generated tokens. Earlier replies are in prior_replies.jsonl. transitions.json and LAWS.txt are material in this world.'''

def sha(b):return hashlib.sha256(b).hexdigest()
def stable(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def immutable(path,value):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:json.dump(value,f,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
def limits():
 for kind,value in [(resource.RLIMIT_AS,PROCESS_AS),(resource.RLIMIT_NPROC,PROCESS_COUNT),
                    (resource.RLIMIT_CPU,2),(resource.RLIMIT_FSIZE,262144),
                    (resource.RLIMIT_NOFILE,64),(resource.RLIMIT_CORE,0)]:
  resource.setrlimit(kind,(value,value))
def base_args():
 return ['bwrap','--unshare-all','--unshare-user','--disable-userns','--die-with-parent','--new-session','--cap-drop','ALL',
 '--clearenv','--setenv','PATH','/usr/bin:/bin','--setenv','HOME','/world',
 '--setenv','LANG','C.UTF-8','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin',
 '--symlink','usr/lib','/lib','--symlink','usr/lib64','/lib64','--dev','/dev',
 '--size','8388608','--tmpfs','/tmp']

class World:
 def __init__(self):
  self.p=subprocess.Popen(base_args()+['--as-pid-1','--ro-bind',str(H/'server.py'),'/runtime/server.py','--size',str(WORLD_BYTES),'--tmpfs','/world','--chdir','/world','--remount-ro','/dev','--remount-ro','/','/bin/python3','-I','-S','/runtime/server.py'],
      stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,text=True)
  ready=self.p.stdout.readline()
  if not ready or json.loads(ready)!={'ready':True}:
   error=self.p.stderr.read();self.close();raise RuntimeError('Sandbox startup failed: '+error)
  self.home=None
  for _ in range(100):
   for d in Path('/proc').iterdir():
    if not d.name.isdigit():continue
    try:
     status=(d/'status').read_text()
     if f'PPid:\t{self.p.pid}\n' in status and (d/'root/world').is_dir():self.home=d/'root/world';break
    except (FileNotFoundError,PermissionError,ProcessLookupError):pass
   if self.home is not None:break
   if self.p.poll() is not None:raise RuntimeError(self.p.stderr.read())
   time.sleep(.01)
  if self.home is None:self.close();raise RuntimeError('No world mount found')
 def close(self):
  if self.p.poll() is None:
   try:os.killpg(self.p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
  self.p.communicate(timeout=3);reap()
 def capture(self,objects):
  objects=Path(objects);objects.mkdir(parents=True,exist_ok=True);rows=[]
  def walk_error(e):raise e
  inode_paths={}
  for root,dirs,files in os.walk(self.home,followlinks=False,onerror=walk_error):
   dirs.sort()
   for name in sorted(dirs+files):
    p=Path(root)/name;rel=str(p.relative_to(self.home));s=p.lstat()
    if p.is_symlink():rows.append([rel,'symlink',os.readlink(p)])
    elif p.is_dir():rows.append([rel,'directory',s.st_mode & 0o777])
    elif p.is_file():
     key=(s.st_dev,s.st_ino)
     if key in inode_paths:
      rows.append([rel,'hardlink',inode_paths[key]]);continue
     inode_paths[key]=rel
     b=p.read_bytes();digest=sha(b);target=objects/(digest+'.json')
     value={'sha256':digest,'bytes':len(b),'base64':base64.b64encode(b).decode()}
     if not target.exists():immutable(target,value)
     elif json.loads(target.read_text())!=value:raise RuntimeError('Object mismatch')
     rows.append([rel,'file',s.st_mode & 0o777,digest,len(b)])
    else:
     import stat
     if stat.S_ISFIFO(s.st_mode):rows.append([rel,'fifo',s.st_mode & 0o777])
     else:raise RuntimeError('Checkpoint cannot retain this special file; pause without a completeness claim')
  rows.sort();return {'id':sha(stable({'entries':rows,'root_mode':self.home.stat().st_mode & 0o777})),'entries':rows,'root_mode':self.home.stat().st_mode & 0o777}
 def restore(self,bundle,objects):
  assert not any(self.home.iterdir()),'Restore only into a new empty mount'
  rows=bundle['entries'];assert bundle['id']==sha(stable({'entries':rows,'root_mode':bundle['root_mode']}))
  # Reject traversal and symlink ancestors before any host-side reconstruction.
  kinds={r[0]:r[1] for r in rows}
  for r in rows:
   rel=Path(r[0]);assert not rel.is_absolute() and '..' not in rel.parts
   for parent in rel.parents:
    if str(parent)!='.':assert kinds.get(str(parent))=='directory'
  for r in sorted(rows,key=lambda r:(len(Path(r[0]).parts),r[0])):
   p=self.home/r[0]
   if r[1]=='directory':p.mkdir()
   elif r[1]=='symlink':p.symlink_to(r[2])
   elif r[1]=='file':
    obj=json.loads((Path(objects)/(r[3]+'.json')).read_text());b=base64.b64decode(obj['base64'],validate=True)
    assert sha(b)==r[3] and len(b)==r[4];p.write_bytes(b);p.chmod(r[2])
   elif r[1]=='fifo':os.mkfifo(p,r[2]);p.chmod(r[2])
   elif r[1]=='hardlink':pass
   else:raise RuntimeError('Special file requires explicit recovery')
  for r in rows:
   if r[1]=='hardlink':
    assert kinds.get(r[2])=='file';os.link(self.home/r[2],self.home/r[0])
  for r in sorted(rows,key=lambda r:len(Path(r[0]).parts),reverse=True):
   if r[1]=='directory':(self.home/r[0]).chmod(r[2])
  self.home.chmod(bundle['root_mode'])
 def execute(self,source):
  import secrets
  nonce=secrets.token_hex(16)
  self.p.stdin.write(json.dumps({'nonce':nonce,'source':source})+'\n');self.p.stdin.flush()
  ready,_,_=__import__('select').select([self.p.stdout],[],[],6)
  if not ready:raise RuntimeError('Unknown execution outcome: sandbox runtime did not respond; never retry automatically')
  line=self.p.stdout.readline()
  if not line:raise RuntimeError('Unknown execution outcome: sandbox runtime ended; never retry automatically')
  answer=json.loads(line)
  if answer.get('nonce')!=nonce:raise RuntimeError('Runtime protocol mismatch; uncertain action outcome')
  return answer['result']

def action(text):
 try:q=json.loads(text)
 except ValueError:return None
 return q['source'] if isinstance(q,dict) and set(q)=={'action','source'} and q['action']=='shell' and isinstance(q['source'],str) else None

def receive(w,text):
 source=action(text)
 if source is not None:return {'kind':'shell','feedback':w.execute(source)}
 # Notebook can contain shell-looking text; this only appends its literal bytes.
 import shlex
 code="with open('notebook.txt','a',encoding='utf-8') as f: f.write("+repr(text+'\n')+")"
 effect=w.execute('python3 -I -S -c '+shlex.quote(code))
 visible=None if effect['exit_code']==0 and effect['boundary'] is None else effect
 return {'kind':'notebook','feedback':visible,'storage_receipt':effect}
