"""Disposable adapter: literal chosen-world cells, then one physical tick.

External markers/records are never mounted into /world. No model session here.
"""
from pathlib import Path
import hashlib,json,re,sys
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'chosen-persistence-prototype-v1'))
import coupling as c
base=c.base


def tick_source(mode):
    if mode not in ('static','changing'):raise ValueError('unknown law')
    return '''import os,stat,json,hashlib
p='field.bin'
try:
    s=os.lstat(p)
except FileNotFoundError:
    print(json.dumps({'material':'absent'}))
else:
    if not stat.S_ISREG(s.st_mode):
        print(json.dumps({'material':'nonregular','changed':False}))
    else:
        fd=os.open(p,os.O_RDWR|os.O_NOFOLLOW)
        try:
            raw=b''
            while True:
                chunk=os.read(fd,65536)
                if not chunk:break
                raw+=chunk
            out=bytearray(raw)
            n=len(raw)//2
            if MODE=='changing':
                for i in range(n):
                    out[2*i]=raw[2*i+1]
                    out[2*i+1]=raw[2*i]^raw[2*((i-1)%n)+1]^raw[2*((i+1)%n)+1]
                os.lseek(fd,0,0)
                view=memoryview(out)
                while view:
                    count=os.write(fd,view)
                    if not count:raise OSError('zero-length write')
                    view=view[count:]
                os.fsync(fd)
            print(json.dumps({'material':'regular','bytes':len(raw),'before_sha256':hashlib.sha256(raw).hexdigest(),'after_sha256':hashlib.sha256(out).hexdigest()}))
        finally:
            os.close(fd)
'''.replace('MODE',repr(mode))


def fingerprint(text):return hashlib.sha256(text.encode()).hexdigest()

def pins():
    return {'adapter':base.digest(__file__),'coupling':c.pins(),'runtime':base.dependencies()}

class MediumWorld:
    @classmethod
    def create(cls,path,bundle,objects,mode):
        tick_source(mode)
        path=Path(path);path.mkdir(parents=True,exist_ok=False)
        base.immutable(path/'CONTRACT.json',dict(mode=mode,pins=pins(),material='field.bin',tick='after each completed reply; no wall-clock advance',parent_scope='detached mechanics fixture'))
        w=c.ChosenWorld.create(path/'world',bundle,objects,parent_entry=0);w.close()
        base.atomic(path/'STATE.json',dict(replies=0,ticks=0,actor_operations=0))
        (path/'replies').mkdir()
        return cls.open(path)

    @classmethod
    def open(cls,path):
        path=Path(path)
        if base.read(path/'CONTRACT.json')['pins']!=pins():raise base.WorldFault('adapter/runtime drift')
        if (path/'PENDING.json').exists():raise base.PendingOutcome('external reply/tick unresolved; explicit inspection required')
        self=cls.__new__(cls);self.path=path;self.mode=base.read(path/'CONTRACT.json')['mode']
        self.world=c.ChosenWorld.open(path/'world');return self

    def close(self):self.world.close()

    def complete(self,text,reply_id,fail_at=None):
        if not re.fullmatch('[A-Za-z0-9_-]{1,80}',reply_id):raise ValueError('invalid identity')
        if (self.path/'PENDING.json').exists():raise base.PendingOutcome('unresolved outer reply')
        target=self.path/'replies'/(reply_id+'.json')
        if target.exists():
            old=base.read(target)
            if old['text_sha256']!=fingerprint(text):raise ValueError('conflicting reply identity')
            return old
        plan=dict(reply_id=reply_id,text=text,text_sha256=fingerprint(text),before_state=base.read(self.path/'STATE.json'),start_step=self.world.step)
        base.immutable(self.path/'PENDING.json',plan)
        batch=self.world.receive_expression(text,reply_id)
        if fail_at=='after_actions':raise InterruptedError('injected after actor batch')
        event=self.world.engine.apply('python',tick_source(self.mode))
        if fail_at=='after_tick':raise InterruptedError('injected after committed physical tick')
        return seal(self.path,plan,batch,event)


def seal(path,plan,batch,event):
    # A tick is recorded only after a completed (possibly boundary-limited) reply.
    if batch['status'] not in ('completed','boundary'):raise base.PendingOutcome('actor reply incomplete; tick not inferred')
    if event['step']!=batch['end_step']+1 or event['source']!=tick_source(base.read(path/'CONTRACT.json')['mode']) or event['before_id']!=batch['after_id']:
        raise base.WorldFault('physical tick does not match completed actor prefix')
    old=plan['before_state']
    new=dict(replies=old['replies']+1,ticks=old['ticks']+1,actor_operations=old['actor_operations']+len(batch['operations']))
    record=dict(reply_id=plan['reply_id'],text_sha256=plan['text_sha256'],raw_text=plan['text'],before_state=old,after_state=new,
                actor_batch=batch,physical_tick=event,interpretation='execution/environment facts; no evaluator score')
    target=path/'replies'/(plan['reply_id']+'.json')
    if target.exists():
        if base.read(target)!=record:raise base.WorldFault('conflicting final record')
    else:base.immutable(target,record)
    current=base.read(path/'STATE.json')
    if current not in (old,new):raise base.WorldFault('counter state conflicts with reply')
    base.atomic(path/'STATE.json',new)
    c.unlink_durable(path/'PENDING.json')
    return record


def recover(path,reason):
    """Explicitly finish known completed actor batch; never replay an actor cell.

    If tick wasn't attempted, perform its one declared execution. If an individual
    operation has unknown outcome, underlying open refuses; no inference/replay.
    """
    if not isinstance(reason,str) or not reason.strip():raise ValueError('operator reason required')
    path=Path(path);contract=base.read(path/'CONTRACT.json')
    if contract['pins']!=pins():raise base.WorldFault('adapter/runtime drift')
    plan=base.read(path/'PENDING.json');engine=path/'world/engine'
    batchfile=engine/'batches'/(plan['reply_id']+'.json')
    if not batchfile.exists():raise base.PendingOutcome('actor batch not complete; preserve evidence, no automatic replay')
    batch=base.read(batchfile)
    if batch['status'] not in ('completed','boundary'):raise base.PendingOutcome('actor batch incomplete; no tick inferred')
    if batch['raw_text']!=plan['text'] or batch['start_step']!=plan['start_step']:raise base.WorldFault('actor batch differs from outer plan')
    w=c.ChosenWorld.open(path/'world')
    try:
        if w.step==batch['end_step']:
            event=w.engine.apply('python',tick_source(contract['mode']))
            executed=1
        elif w.step==batch['end_step']+1:
            event=base.read(engine/'events'/f'{w.step:06d}.json');executed=0
        else:raise base.WorldFault('unexpected committed operation count')
        record=seal(path,plan,batch,event)
        base.immutable(path/('RECOVERY_'+plan['reply_id']+'.json'),dict(reason=reason,actor_cells_replayed=0,physical_ticks_executed=executed))
        return record
    finally:w.close()
