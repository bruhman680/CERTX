"""Detached Linux advisory-lock behavior probes. No garden source is modified."""
from pathlib import Path
import fcntl, json, os, platform, subprocess, sys

H=Path(__file__).resolve().parent

def attempt(path):
    fd=os.open(path,os.O_CREAT|os.O_RDWR|os.O_CLOEXEC,0o600)
    try:
        try:
            fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            return False
    finally:
        os.close(fd)

def holder(path):
    fd=os.open(path,os.O_CREAT|os.O_RDWR|os.O_CLOEXEC,0o600)
    fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    print('ready',flush=True)
    sys.stdin.readline()
    os._exit(93)

def main():
    target=H/'disposable'
    target.mkdir(exist_ok=False)
    lock=target/'OPERATOR_LOCK'
    p=subprocess.Popen([sys.executable,__file__,'holder',str(lock)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    assert p.stdout.readline().strip()=='ready'
    blocked=not attempt(lock)
    inode_before=lock.stat().st_ino
    p.stdin.write('exit\n');p.stdin.flush()
    assert p.wait(timeout=5)==93
    after=attempt(lock)
    assert blocked and after and lock.stat().st_ino==inode_before

    # A duplicate retains the same open file description until the last close.
    fd=os.open(lock,os.O_RDWR|os.O_CLOEXEC)
    fcntl.flock(fd,fcntl.LOCK_EX)
    duplicate=os.dup(fd)
    os.close(fd)
    duplicate_holds=not attempt(lock)
    os.close(duplicate)
    duplicate_release=attempt(lock)
    assert duplicate_holds and duplicate_release

    # Deliberate disposable anti-pattern: unlink splits the synchronization object.
    alias=target/'UNLINK_ANTIPATTERN'
    old=os.open(alias,os.O_CREAT|os.O_RDWR|os.O_CLOEXEC,0o600)
    fcntl.flock(old,fcntl.LOCK_EX)
    old_inode=os.fstat(old).st_ino
    alias.unlink()
    new=os.open(alias,os.O_CREAT|os.O_RDWR|os.O_CLOEXEC,0o600)
    fcntl.flock(new,fcntl.LOCK_EX|fcntl.LOCK_NB)
    split=os.fstat(new).st_ino!=old_inode
    assert split
    os.close(new);os.close(old)
    result={'platform':platform.platform(),'python':platform.python_version(),
        'contender_blocked_while_holder_alive':blocked,
        'acquired_after_actual_os_exit_93':after,
        'persistent_lock_inode_unchanged':lock.stat().st_ino==inode_before,
        'duplicate_descriptor_kept_lock':duplicate_holds,
        'last_descriptor_close_released':duplicate_release,
        'unlink_recreate_allows_two_distinct_locked_inodes':split,
        'canonical_sources_or_worlds_accessed':False,
        'scope':'local filesystem Linux process/descriptor probes; not integration, power-loss, network-filesystem, or migration tests'}
    (H/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='holder': holder(Path(sys.argv[2]))
    else: main()
