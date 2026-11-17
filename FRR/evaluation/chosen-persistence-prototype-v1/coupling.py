"""Persistent computational world; raw expressions are recorded externally only."""
from pathlib import Path
import sys,re,os,copy
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'minimal-garden-candidate-v1/world'))
import garden_world as base

def pins():
    return {str(p):base.digest(p) for p in (Path(__file__).resolve(),E/'minimal-garden-candidate-v1/world/garden_world.py')}

def unlink_durable(path):
    path=Path(path);path.unlink()
    fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def check_contract(store):
    contract=base.read(Path(store)/'COUPLING.json')
    if contract['implementation_pins']!=pins():raise base.WorldFault('Coupling implementation drift')
    return contract

def verify(store):
    store=Path(store);check_contract(store)
    if (store/'CREATE_PENDING.json').exists():raise base.PendingOutcome('Initialization incomplete; inspect, do not recreate')
    return base.verify_store(store/'engine')

class ChosenWorld:
    @classmethod
    def create(cls,store,bundle,objects,parent_entry=0):
        store=Path(store);store.mkdir(parents=True,exist_ok=False)
        base.immutable(store/'CREATE_PENDING.json',{'stage':'engine initialization unresolved'})
        base.immutable(store/'COUPLING.json',{'version':'chosen-persistence-prototype-v1','implementation_pins':pins(),
            'expression':'complete exact Python/shell fences execute; all other text has no filesystem effect',
            'automatic_notebook_append':False,'max_complete_cells':8,
            'records':'external engine/batches contains every raw expression; never mounted in /world',
            'physics':'same pinned interpreter/resource/capture laws; no autonomous ticks or evaluator reward'})
        w=base.GardenWorld.create(store/'engine',bundle,objects,parent_entry=parent_entry)
        w.close();unlink_durable(store/'CREATE_PENDING.json')
        return cls.open(store)

    @classmethod
    def open(cls,store):
        store=Path(store);verify(store)
        self=cls.__new__(cls);self.store=store;self.engine=base.GardenWorld.open(store/'engine')
        return self

    @property
    def step(self):return self.engine.step
    def checkpoint(self):return self.engine.checkpoint()
    def close(self):self.engine.close()

    def receive_expression(self,text,reply_id):
        if not isinstance(text,str):raise TypeError('Expression must be text')
        if not isinstance(reply_id,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',reply_id):raise ValueError('Invalid external reply identifier')
        check_contract(self.store);w=self.engine;w._assert_ready()
        target=w.store/'batches'/(reply_id+'.json')
        if target.exists():raise base.PendingOutcome('Reply already recorded; never replay automatically')
        parsed=base.parse_notebook(text);before=w.checkpoint()
        batch={'batch_id':reply_id,'raw_text':text,'parsed':parsed,'operations':[],'status':'planned','boundary':None,
               'before_id':before['id'],'start_step':w.step,'automatic_note_append':False}
        if parsed['complete_executable_cells']>8:
            batch.update(status='boundary',boundary='cell_count_limit',after_id=before['id'],end_step=w.step)
            base.immutable(target,batch);return batch
        base.immutable(w.store/'BATCH_PENDING.json',batch);w._in_batch=True
        try:
            for index,cell in enumerate(parsed['cells']):
                if not cell['executable']:continue
                event=w.apply('python' if cell['language']=='python' else 'shell',cell['source'])
                batch['operations'].append(dict(event,cell_index=index,source_start=cell['source_start'],source_end=cell['source_end']))
                base.atomic(w.store/'BATCH_PENDING.json',batch)
            batch.update(status='completed',after_id=w.checkpoint()['id'],end_step=w.step)
            base.immutable(target,batch);unlink_durable(w.store/'BATCH_PENDING.json')
            return batch
        finally:w._in_batch=False

def recover_known_prefix(store,reason):
    """Explicitly seal a verified committed prefix; never execute the remainder."""
    store=Path(store);verify(store);engine=store/'engine'
    if not isinstance(reason,str) or not reason.strip():raise ValueError('Explicit recovery reason required')
    if (engine/'LOCK.json').exists() or (engine/'PENDING.json').exists():
        raise base.PendingOutcome('Active owner or unresolved individual operation; recovery cannot infer its outcome')
    state=base.read(engine/'STATE.json')
    if not state['paused'] or state['faulted']:raise base.PendingOutcome('Requires a clean paused, verified operation ledger')
    pending=base.read(engine/'BATCH_PENDING.json');reply_id=pending['batch_id']
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',reply_id):raise base.WorldFault('Invalid pending reply identifier')
    if base.read(engine/'bundles'/f"{pending['start_step']:06d}.json")['id']!=pending['before_id']:
        raise base.WorldFault('Pending start snapshot differs')
    parsed=base.parse_notebook(pending['raw_text'])
    if parsed!=pending['parsed']:raise base.WorldFault('Pending parser record differs')
    cells=[(i,c) for i,c in enumerate(parsed['cells']) if c['executable']]
    count=state['step']-pending['start_step']
    if not 0<=count<=len(cells):raise base.WorldFault('Unexpected committed operation count')
    events=[]
    for n in range(count):
        index,cell=cells[n];ev=base.read(engine/'events'/f"{pending['start_step']+n+1:06d}.json")
        if ev['source']!=cell['source'] or ev['channel']!=('python' if cell['language']=='python' else 'shell'):
            raise base.WorldFault('Committed prefix does not match planned cells')
        events.append(dict(ev,cell_index=index,source_start=cell['source_start'],source_end=cell['source_end']))
    sealed={k:copy.deepcopy(pending[k]) for k in ('batch_id','raw_text','parsed','before_id','start_step','automatic_note_append')}
    sealed.update(operations=events,status='interrupted',boundary=None,after_id=base.read(engine/'bundles'/state['bundle'])['id'],
                  end_step=state['step'],unexecuted_cells=len(cells)-count,recovery_reason=reason)
    target=engine/'batches'/(reply_id+'.json')
    # If all cells were committed and the final record was already written, finish only its unlink.
    if target.exists():
        old=base.read(target)
        if old.get('status')=='completed' and count==len(cells) and old['operations']==events:
            if old['raw_text']!=pending['raw_text'] or old['before_id']!=pending['before_id'] or old['after_id']!=sealed['after_id']:
                raise base.WorldFault('Completed record differs from pending')
            sealed=old
        elif old!=sealed:raise base.WorldFault('Existing batch conflicts with recovery')
    else:base.immutable(target,sealed)
    evidence=store/'recovery'/(reply_id+'.json')
    value={'pending_record':pending,'sealed_record':sealed,'operator_reason':reason,'actions_replayed':0}
    if evidence.exists():
        if base.read(evidence)!=value:raise base.WorldFault('Recovery evidence differs')
    else:base.immutable(evidence,value)
    unlink_durable(engine/'BATCH_PENDING.json')
    return sealed
