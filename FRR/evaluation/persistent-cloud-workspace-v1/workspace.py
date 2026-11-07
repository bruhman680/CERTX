"""Persistent Linux action boundary. No model calls or live activation on import."""
from pathlib import Path
import hashlib, json, os, resource, selectors, signal, subprocess, time

MAX_OUTPUT=8192
MAX_FILE=262144
MAX_STORAGE=8*1024*1024  # checked between actions; not a filesystem quota
MAX_ENTRIES=2048
NOTICE='''Working directory: /world. Files here persist between turns. /usr provides shell commands and Python 3. Other host files and network access are unavailable. Your whole reply is passed unchanged to /bin/sh as a script; stdout, stderr and exit status return here. Shell variables and processes do not persist between turns; files do. Limits: 3 seconds per action, 512 MiB address space per process, 256 KiB per file, 8192 bytes of combined output. The workspace pauses above 8 MiB or 2048 directory entries, checked between actions. Each reply has a 96-token generation limit. No text is automatically repaired or extracted from code fences.'''

def snapshot(home):
    rows=[]
    for p in sorted(Path(home).rglob('*')):
        s=p.lstat(); rel=str(p.relative_to(home))
        if p.is_symlink(): rows.append([rel,'symlink',os.readlink(p)])
        elif p.is_file(): rows.append([rel,'file',s.st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
        elif p.is_dir(): rows.append([rel,'directory'])
        else: rows.append([rel,'special',s.st_mode])
    return rows

def usage(home):
    rows=snapshot(home)
    return sum(r[2] for r in rows if r[1]=='file'), len(rows)

def limits():
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,512*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE,(MAX_FILE,MAX_FILE))
    resource.setrlimit(resource.RLIMIT_CPU,(2,2))
    resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_NPROC,(64,64))


def execute(home, source):
    home=Path(home).resolve(strict=True)
    size,count=usage(home)
    if size>MAX_STORAGE or count>MAX_ENTRIES:
        raise RuntimeError('Workspace storage boundary; preserve and inspect before continuation')
    args=['bwrap','--unshare-all','--die-with-parent','--new-session','--cap-drop','ALL',
          '--clearenv','--setenv','PATH','/usr/bin:/bin','--setenv','HOME','/world',
          '--setenv','LANG','C.UTF-8','--ro-bind','/usr','/usr',
          '--symlink','usr/bin','/bin','--symlink','usr/lib','/lib',
          '--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev',
          '--size','8388608','--tmpfs','/tmp','--bind',str(home),'/world','--chdir','/world',
          '/bin/sh','-c',source]
    before=snapshot(home); start=time.monotonic()
    p=subprocess.Popen(args,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                       start_new_session=True,preexec_fn=limits)
    sel=selectors.DefaultSelector(); data={'stdout':bytearray(),'stderr':bytearray()}
    for stream,key in [(p.stdout,'stdout'),(p.stderr,'stderr')]:
        os.set_blocking(stream.fileno(),False);sel.register(stream,selectors.EVENT_READ,key)
    cause=None
    try:
        while sel.get_map():
            if time.monotonic()-start>3: cause='wall_time';break
            for key,_ in sel.select(.03):
                chunk=os.read(key.fileobj.fileno(),4096)
                if not chunk: sel.unregister(key.fileobj);continue
                remaining=MAX_OUTPUT-sum(map(len,data.values()))
                data[key.data].extend(chunk[:remaining])
                if len(chunk)>remaining: cause='output_limit';break
            if cause: break
        if cause:
            try: os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError: pass
        try: code=p.wait(timeout=max(.01,3-(time.monotonic()-start)))
        except subprocess.TimeoutExpired:
            cause='wall_time';os.killpg(p.pid,signal.SIGKILL);code=p.wait()
    finally:
        sel.close();p.stdout.close();p.stderr.close()
        if p.poll() is None:
            os.killpg(p.pid,signal.SIGKILL);p.wait()
    after=snapshot(home); size,count=usage(home)
    return dict(source=source,stdout=data['stdout'].decode('utf-8',errors='replace'),
                stderr=data['stderr'].decode('utf-8',errors='replace'),exit_code=code,
                boundary=cause,seconds=time.monotonic()-start,before=before,after=after,
                storage_bytes=size,directory_entries=count,
                pause_required=size>MAX_STORAGE or count>MAX_ENTRIES)
