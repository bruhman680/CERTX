"""Environmental rules and durable records; no model or semantic evaluator.

Legacy receive keeps exact whole-reply JSON semantics. receive_notebook is a
separate, prospective computational-notebook law; it never repairs source.
"""
from pathlib import Path
import base64, hashlib, importlib.util, json, os, shlex, shutil, uuid

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parents[1] / 'final-garden-contract-v1'
_spec = importlib.util.spec_from_file_location('candidate_frozen_world_dependency', FROZEN / 'world.py')
_runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_runtime)

class WorldFault(RuntimeError):
    """Uncertain or uncheckpointable effects; no automatic action replay."""

class PendingOutcome(WorldFault):
    pass

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def immutable(path, value):
    _runtime.immutable(path, value)

def atomic(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp.' + uuid.uuid4().hex)
    with temporary.open('x') as stream:
        json.dump(value, stream, sort_keys=True)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)

def dependencies():
    paths = [Path(__file__).resolve(), FROZEN/'world.py', FROZEN/'server.py']
    host = read(FROZEN/'HOST_RUNTIME_IDENTITY.json')['critical_guest_executables_sha256']
    for path, expected in host.items():
        if digest(path) != expected:
            raise WorldFault('Frozen guest executable drift: ' + path)
    return {str(path):digest(path) for path in paths} | host

def _bundle_id(bundle):
    return _runtime.sha(_runtime.stable({'entries':bundle['entries'], 'root_mode':bundle['root_mode']}))

def verify_store(store):
    """Check committed ancestry and bytes without running or replaying actions."""
    import re
    store = Path(store)
    manifest,state = read(store/'MANIFEST.json'),read(store/'STATE.json')
    if dependencies() != manifest['dependencies']:
        raise WorldFault('World dependency drift')
    if type(state['step']) is not int or state['step'] < 0 or state['parent_entry'] != manifest['parent_entry']:
        raise WorldFault('Invalid world counter/lineage')
    if digest(store/'bundles/000000.json') != manifest['parent_bundle_sha256']:
        raise WorldFault('Initial copied bundle bytes changed')
    count = state['step']
    numbers = {int(p.stem) for p in (store/'events').glob('*.json') if re.fullmatch(r'[0-9]+',p.stem)}
    if numbers != set(range(1,count+1)):
        raise WorldFault('Committed event sequence is not contiguous')
    previous = read(store/'bundles/000000.json')
    if previous['id'] != _bundle_id(previous) or previous['id'] != manifest['parent_bundle_id']:
        raise WorldFault('Initial bundle identity changed')
    last = None
    for number in range(1,count+1):
        path = store/'events'/f'{number:06d}.json'
        event = read(path)
        receipt = read(store/'events'/f'{number:06d}_RECEIPT.json')
        after = read(store/'bundles'/f'{number:06d}.json')
        if (event['step'] != number or event['parent_event_sha256'] != last or
            event['before_id'] != previous['id'] or event['after_id'] != after['id'] or
            after['id'] != _bundle_id(after) or receipt['receipt'] != event['receipt']):
            raise WorldFault('World event/bundle/receipt chain mismatch')
        for key in ('step','channel','source','raw_text','before_id','parent_event_sha256'):
            if receipt['operation'][key] != event[key]:
                raise WorldFault('Saved operation and event differ')
        b,a = {x[0]:x for x in previous['entries']},{x[0]:x for x in after['entries']}
        if event['changed_paths'] != [n for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)]:
            raise WorldFault('Saved filesystem delta differs')
        previous,last = after,digest(path)
    if state['bundle'] != f'{count:06d}.json' or state['last_event_sha256'] != last:
        raise WorldFault('World state does not point to committed history')
    for path in (store/'objects').glob('*.json'):
        obj = read(path)
        b = base64.b64decode(obj['base64'],validate=True)
        if _runtime.sha(b) != path.stem or obj['sha256'] != path.stem or obj['bytes'] != len(b):
            raise WorldFault('Stored object hash/length mismatch')
    for path in (store/'bundles').glob('*.json'):
        bundle = read(path)
        if bundle['id'] != _bundle_id(bundle):
            raise WorldFault('Stored bundle identity mismatch')
        for entry in bundle['entries']:
            if entry[1] == 'file':
                obj = read(store/'objects'/(entry[3]+'.json'))
                if obj['bytes'] != entry[4]:
                    raise WorldFault('Bundle/object byte count differs')
    return {'status':'pass','step':count,'parent_entry':manifest['parent_entry'],
            'bundle_id':previous['id'],'objects':len(list((store/'objects').glob('*.json')))}

def parse_notebook(text):
    """Exact column-zero fences. Unknown fences shield contents; no repair.

    All column-zero runs of >=3 backticks open a fence, shielding contents.
    Only exactly three backticks plus exact lower-case python or sh execute.
    A closing line is exactly the opening backtick delimiter, with no info.
    LF and CRLF delimiters are accepted. Offsets are end-exclusive.
    """
    if not isinstance(text, str):
        raise TypeError('Notebook text must be a string')
    import re
    cells, position, opening = [], 0, None
    for line in text.splitlines(keepends=True):
        plain = line[:-2] if line.endswith('\r\n') else line[:-1] if line.endswith('\n') else line
        if opening is None:
            match = re.fullmatch(r'(`{3,})(.*)', plain)
            if match:
                opening = {'delimiter':match[1], 'language':match[2], 'fence_start':position, 'source_start':position+len(line)}
        elif plain == opening['delimiter']:
            cell = dict(opening, source_end=position, fence_end=position+len(line), complete=True)
            cell['source'] = text[cell['source_start']:cell['source_end']]
            cell['executable'] = cell['delimiter']=='```' and cell['language'] in ('python','sh')
            cells.append(cell)
            opening = None
        position += len(line)
    if opening is not None:
        cell = dict(opening, source_end=len(text), fence_end=len(text), complete=False, executable=False)
        cell['source'] = text[cell['source_start']:]
        cells.append(cell)
    for cell in cells:
        cell['offset_unit'] = 'Unicode code points; end exclusive'
        for key in ('fence_start','source_start','source_end','fence_end'):
            cell[key+'_utf8'] = len(text[:cell[key]].encode('utf-8'))
    return {'cells':cells, 'complete_executable_cells':sum(c['executable'] for c in cells),
            'raw_codepoints':len(text), 'raw_utf8_bytes':len(text.encode('utf-8'))}

class GardenWorld:
    """Owned persistent copy of the 1550 world, with one live isolated mount."""
    @classmethod
    def create(cls, store, parent_bundle, parent_objects, parent_entry=1550):
        store, parent_bundle, parent_objects = Path(store), Path(parent_bundle), Path(parent_objects)
        store.mkdir(parents=True, exist_ok=False)
        for name in ('objects','bundles','events','batches','faults'):
            (store/name).mkdir()
        bundle = read(parent_bundle)
        if bundle['id'] != _bundle_id(bundle):
            raise WorldFault('Invalid parent bundle')
        for entry in bundle['entries']:
            if entry[1] != 'file':
                continue
            src = parent_objects/(entry[3]+'.json')
            obj = read(src)
            b = base64.b64decode(obj['base64'], validate=True)
            if _runtime.sha(b) != entry[3] or len(b) != entry[4] or obj['sha256'] != entry[3] or obj['bytes'] != len(b):
                raise WorldFault('Invalid parent object')
            if not (store/'objects'/src.name).exists():
                shutil.copyfile(src, store/'objects'/src.name)
        shutil.copyfile(parent_bundle, store/'bundles/000000.json')
        immutable(store/'MANIFEST.json', {'version':'minimal-garden-world-v1','parent_entry':parent_entry,
            'parent_bundle':str(parent_bundle.resolve()),'parent_bundle_sha256':digest(parent_bundle),
            'parent_bundle_id':bundle['id'],'dependencies':dependencies(),
            'notebook_grammar':'column-zero exact ```python or ```sh; exact ``` close; no repairs',
            'notebook_max_complete_cells':8,'ordinary_cell_errors':'continue later cells',
            'notebook_storage_fault':'retain actual receipt and continue lawful cells when outcome is known','cell_limits':'frozen runtime, separately for each cell',
            'persistence':'supported filesystem state; no process variables, /tmp or KV continuity'})
        atomic(store/'STATE.json', {'step':0,'parent_entry':parent_entry,'bundle':'000000.json',
            'last_event_sha256':None,'paused':True,'faulted':False})
        return cls.open(store)

    @classmethod
    def open(cls, store):
        self = cls.__new__(cls)
        self.store = Path(store)
        self.objects = self.store/'objects'
        self._token = uuid.uuid4().hex
        self._guest = None
        self._closed = False
        self._in_batch = False
        self._owns_lock = False
        immutable(self.store/'LOCK.json', {'token':self._token,'pid':os.getpid()})
        self._owns_lock = True
        try:
            if (self.store/'PENDING.json').exists() or (self.store/'BATCH_PENDING.json').exists():
                raise PendingOutcome('Pending operation/batch requires explicit inspection; never replay automatically')
            verify_store(self.store)
            state = read(self.store/'STATE.json')
            if not state['paused'] or state['faulted']:
                raise PendingOutcome('World is not a clean paused checkpoint')
            self._guest = _runtime.World()
            self._guest.restore(read(self.store/'bundles'/state['bundle']),self.objects)
            if self._guest.capture(self.objects) != self.bundle:
                raise WorldFault('Restored world mismatch')
            state['paused'] = False
            atomic(self.store/'STATE.json',state)
            return self
        except BaseException:
            if self._guest is not None:
                self._guest.close()
            self._release_lock()
            raise

    @property
    def step(self):
        return read(self.store/'STATE.json')['step']

    @property
    def bundle(self):
        return read(self.store/'bundles'/read(self.store/'STATE.json')['bundle'])

    def _release_lock(self):
        lock = self.store/'LOCK.json'
        if self._owns_lock and lock.exists() and read(lock).get('token') == self._token:
            lock.unlink()
        self._owns_lock = False

    def _assert_ready(self):
        if self._closed or self._guest is None:
            raise WorldFault('World is closed')
        if (self.store/'PENDING.json').exists():
            raise PendingOutcome('An operation is pending; no automatic replay')
        if (self.store/'BATCH_PENDING.json').exists() and not self._in_batch:
            raise PendingOutcome('A notebook batch is pending; no automatic replay')
        if read(self.store/'STATE.json')['faulted']:
            raise WorldFault('World is faulted')
        if dependencies() != read(self.store/'MANIFEST.json')['dependencies']:
            raise WorldFault('World dependency drift')

    def checkpoint(self):
        self._assert_ready()
        actual = self._guest.capture(self.objects)
        if actual != self.bundle:
            raise WorldFault('Live world differs from committed checkpoint')
        return actual

    def observe(self):
        """Factual data only; callers choose the model-facing observation policy."""
        bundle = self.checkpoint()
        last = None if self.step == 0 else read(self.store/'events'/f'{self.step:06d}.json')
        return {'step':self.step,'parent_entry':read(self.store/'STATE.json')['parent_entry'],
                'bundle':bundle,'last_receipt':None if last is None else last['receipt']}

    def _fault(self, error, stage):
        attempted = read(self.store/'PENDING.json')['step'] if (self.store/'PENDING.json').exists() else self.step
        fault = {'step_attempted':attempted,'stage':stage,'type':type(error).__name__,
                 'message':str(error),'automatic_replay_allowed':False}
        try:
            snapshot = self._guest.capture(self.objects)
            immutable(self.store/'faults'/(uuid.uuid4().hex+'_WORLD.json'),snapshot)
            fault['uncommitted_bundle_id'] = snapshot['id']
            fault['filesystem_capture_available'] = True
        except BaseException as capture_error:
            fault['filesystem_capture_available'] = False
            fault['capture_error'] = repr(capture_error)
            fault['uncommitted_filesystem_recovery'] = 'not guaranteed; effects after last bundle may be lost on shutdown'
        immutable(self.store/'faults'/(uuid.uuid4().hex+'_FAULT.json'),fault)
        state = read(self.store/'STATE.json')
        state['faulted'] = True
        atomic(self.store/'STATE.json',state)

    def apply(self, channel, source, raw_text=None):
        self._assert_ready()
        if channel not in ('shell','python','note','noop') or not isinstance(source,str):
            raise ValueError('Explicit channel must be shell, python, note or noop with string source')
        before = self.checkpoint()
        state = read(self.store/'STATE.json')
        number = state['step']+1
        pending = {'step':number,'channel':channel,'source':source,'raw_text':raw_text,
                   'before_id':before['id'],'parent_event_sha256':state['last_event_sha256']}
        immutable(self.store/'PENDING.json',pending)
        stage = 'before execution'
        try:
            if channel == 'noop':
                receipt,kind = None,'noop'
            else:
                if channel == 'shell':
                    command,kind = source,'shell'
                elif channel == 'python':
                    command,kind = 'python3 -I -S -c '+shlex.quote(source),'python'
                else:
                    code = "with open('notebook.txt','a',encoding='utf-8') as f: f.write("+repr(source+'\n')+")"
                    command,kind = 'python3 -I -S -c '+shlex.quote(code),'notebook'
                stage = 'execute: receipt may be uncertain'
                receipt = self._guest.execute(command)
                if (not isinstance(receipt,dict) or not isinstance(receipt.get('stdout'),str) or
                    not isinstance(receipt.get('stderr'),str) or type(receipt.get('exit_code')) is not int or
                    not (receipt.get('boundary') is None or isinstance(receipt.get('boundary'),str))):
                    raise WorldFault('Malformed runtime receipt; action outcome uncertain')
            stage = 'known receipt; capture not yet committed'
            immutable(self.store/'events'/f'{number:06d}_RECEIPT.json',{'receipt':receipt,'operation':pending})
            after = self._guest.capture(self.objects)
            immutable(self.store/'bundles'/f'{number:06d}.json',after)
            b,a = {x[0]:x for x in before['entries']},{x[0]:x for x in after['entries']}
            feedback = receipt
            if channel == 'note' and receipt['exit_code'] == 0 and receipt['boundary'] is None:
                feedback = None
            event = dict(pending, kind=kind, receipt=receipt, feedback=feedback,
                         after_id=after['id'], changed_paths=[n for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)])
            immutable(self.store/'events'/f'{number:06d}.json',event)
            state.update(step=number,bundle=f'{number:06d}.json',last_event_sha256=digest(self.store/'events'/f'{number:06d}.json'))
            atomic(self.store/'STATE.json',state)
            (self.store/'PENDING.json').unlink()
            return event
        except BaseException as error:
            self._fault(error,stage)
            raise WorldFault('Operation not cleanly committed; inspect pending/fault evidence, never replay automatically') from error

    def receive(self, text):
        """Legacy exact-JSON action law; ordinary writing remains literal."""
        source = _runtime.action(text)
        return self.apply('shell',source,raw_text=text) if source is not None else self.apply('note',text,raw_text=text)

    def receive_notebook(self, text, max_cells=8):
        self._assert_ready()
        if max_cells != 8:
            raise ValueError('The declared notebook limit is exactly eight complete executable cells')
        parsed = parse_notebook(text)
        batch_id = f'{self.step:06d}_'+uuid.uuid4().hex
        batch = {'batch_id':batch_id,'raw_text':text,'parsed':parsed,'operations':[],
                 'status':'planned','boundary':None,'note_stored':False}
        if parsed['complete_executable_cells'] > max_cells:
            batch.update(status='boundary',boundary='cell_count_limit')
            immutable(self.store/'batches'/(batch_id+'.json'),batch)
            return batch
        immutable(self.store/'BATCH_PENDING.json',batch)
        self._in_batch = True
        try:
            note = self.apply('note',text,raw_text=text)
            batch['operations'].append(note)
            batch['note_stored'] = note['feedback'] is None
            batch['note_storage_fault'] = note['feedback']
            atomic(self.store/'BATCH_PENDING.json',batch)
            for index,cell in enumerate(parsed['cells']):
                if not cell['executable']:
                    continue
                event = self.apply('python' if cell['language']=='python' else 'shell',cell['source'])
                event_reference = dict(event,cell_index=index,
                    source_start=cell['source_start'],source_end=cell['source_end'])
                batch['operations'].append(event_reference)
                atomic(self.store/'BATCH_PENDING.json',batch)
            batch['status'] = 'completed'
            immutable(self.store/'batches'/(batch_id+'.json'),batch)
            (self.store/'BATCH_PENDING.json').unlink()
            return batch
        finally:
            self._in_batch = False

    def close(self):
        if self._closed:
            return
        error = None
        try:
            if self._guest is not None:
                try:
                    state = read(self.store/'STATE.json')
                    if not state['faulted'] and not (self.store/'PENDING.json').exists() and not (self.store/'BATCH_PENDING.json').exists():
                        self.checkpoint()
                except BaseException as checkpoint_error:
                    error = checkpoint_error
                    self._fault(checkpoint_error,'close: live state differs or cannot be checkpointed')
                finally:
                    try:
                        self._guest.close()
                    finally:
                        state = read(self.store/'STATE.json')
                        state['paused'] = True
                        atomic(self.store/'STATE.json',state)
        finally:
            self._release_lock()
            self._closed = True
        if error is not None:
            raise WorldFault('Close checkpoint failed; runtime stopped and fault recorded') from error

    def __enter__(self):
        return self

    def __exit__(self,*exc):
        self.close()
