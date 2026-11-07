"""Trusted action runtime inside the guest namespace; no research evaluation."""
import shutil,stat
import json,os,resource,selectors,signal,subprocess,sys,time

def limits():
 for kind,value in [(resource.RLIMIT_AS,33554432),(resource.RLIMIT_NPROC,128),(resource.RLIMIT_CPU,2),(resource.RLIMIT_FSIZE,262144),(resource.RLIMIT_NOFILE,64),(resource.RLIMIT_CORE,0)]:resource.setrlimit(kind,(value,value))
def execute(source):
 start=time.monotonic()
 try:p=subprocess.Popen(['/bin/sh','-c',source],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=limits,start_new_session=True,close_fds=True)
 except (OSError,subprocess.SubprocessError) as error:
  return {'stdout':'','stderr':str(error),'exit_code':126,'boundary':'spawn_error','seconds':time.monotonic()-start}
 sel=selectors.DefaultSelector();data={'stdout':bytearray(),'stderr':bytearray()};boundary=None
 for stream,name in [(p.stdout,'stdout'),(p.stderr,'stderr')]:os.set_blocking(stream.fileno(),False);sel.register(stream,selectors.EVENT_READ,name)
 try:
  while sel.get_map():
   if time.monotonic()-start>=3:boundary='wall_time';break
   for key,_ in sel.select(.02):
    b=os.read(key.fileobj.fileno(),4096)
    if not b:sel.unregister(key.fileobj);continue
    remain=8192-sum(map(len,data.values()));data[key.data].extend(b[:remain])
    if len(b)>remain:boundary='output_limit';break
   if boundary:break
  if boundary:
   # PID namespace: kills guest action descendants, excluding this server/PID1.
   try:os.kill(-1,signal.SIGKILL)
   except ProcessLookupError:pass
  try:code=p.wait(timeout=max(.01,3-(time.monotonic()-start)))
  except subprocess.TimeoutExpired:
   boundary='wall_time';os.kill(-1,signal.SIGKILL);code=p.wait()
 finally:
  try:os.kill(-1,signal.SIGKILL)
  except ProcessLookupError:pass
  sel.close();p.stdout.close();p.stderr.close()
  if p.poll() is None:p.wait()
  while True:
   try:
    pid,_=os.waitpid(-1,os.WNOHANG)
    if pid==0:break
   except ChildProcessError:break
 for item in os.scandir('/tmp'):
  if item.is_dir(follow_symlinks=False):
   def repair(function,path,exc):
    os.chmod(path,0o700);function(path)
   shutil.rmtree(item.path,onerror=repair)
  else:os.unlink(item.path)
 return {'stdout':data['stdout'].decode(errors='replace'),'stderr':data['stderr'].decode(errors='replace'),'exit_code':code,'boundary':boundary,'seconds':time.monotonic()-start}
print(json.dumps({'ready':True}),flush=True)
for line in sys.stdin:
 q=json.loads(line);r=execute(q['source']);print(json.dumps({'nonce':q['nonce'],'result':r}),flush=True)
