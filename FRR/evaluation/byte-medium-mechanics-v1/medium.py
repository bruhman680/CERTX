"""Detached byte-material fixture. No model execution or sandbox integration.

Transactions contain only pure byte operations; atomic replacement cannot make
external process effects transactional. Single operator writer, not a server.
"""
import base64
import hashlib
import json
import os
from pathlib import Path

LIMIT = 65536

def evolve(data):
    """Periodic second-order XOR medium. Any odd trailing byte remains unchanged."""
    if data is None:
        return None
    out = bytearray(data)
    n = len(data) // 2
    for i in range(n):
        a, b = data[2*i:2*i+2]
        out[2*i] = b
        out[2*i+1] = a ^ data[2*((i-1) % n)+1] ^ data[2*((i+1) % n)+1]
    return bytes(out)

def inverse(data):
    if data is None:
        return None
    out = bytearray(data)
    n = len(data) // 2
    for i in range(n):
        a, b = data[2*i:2*i+2]
        out[2*i] = b ^ data[2*((i-1) % n)] ^ data[2*((i+1) % n)]
        out[2*i+1] = a
    return bytes(out)

def encode(data):
    return None if data is None else base64.b64encode(data).decode('ascii')

def decode(data):
    return None if data is None else base64.b64decode(data, validate=True)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def create(path, mode, initial):
    path = Path(path)
    if mode not in ('static', 'changing'):
        raise ValueError('unknown declared law')
    if not isinstance(initial, bytes) or len(initial) > LIMIT:
        raise ValueError('initial byte material exceeds fixture bound')
    state = dict(version=1, mode=mode, tick=0, operation_count=0,
                 material=encode(initial), events=[])
    # Exclusive initialization; a partial file is evidence, not an invitation to reset.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(canonical(state)); f.flush(); os.fsync(f.fileno())
    fsync_dir(path.parent)
    return state

def fsync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def read(path):
    state = json.loads(Path(path).read_bytes())
    if state['version'] != 1 or state['mode'] not in ('static', 'changing'):
        raise ValueError('fixture contract mismatch')
    return state

def operation(data, op):
    """Synthetic operations stand in for writes, not a proposed model language."""
    kind = op.get('kind')
    if kind == 'delete':
        return None
    if kind == 'write':
        value = decode(op['bytes'])
        if value is None:
            raise ValueError('write requires bytes')
    elif kind == 'append':
        if data is None:
            raise FileNotFoundError('material absent')
        extra = decode(op['bytes'])
        if extra is None:
            raise ValueError('append requires bytes')
        value = data + extra
    else:
        raise ValueError('unknown synthetic operation')
    if len(value) > LIMIT:
        raise ValueError('material byte capacity')
    return value

def complete(path, reply_id, operations, fail_at=None):
    """Commit pure operations followed by one tick in a single atomic state.

    Retrying an identical committed ID returns its stored event with no replay;
    conflicting reuse refuses. Unknown/corrupt outcomes require inspection.
    fail_at is external crash injection only, never part of world observation.
    """
    if not isinstance(reply_id, str) or not reply_id or len(reply_id) > 80:
        raise ValueError('reply identity required')
    request = dict(reply_id=reply_id, operations=operations)
    fingerprint = digest(request)
    state = read(path)
    for event in state['events']:
        if event['reply_id'] == reply_id:
            if event['request_sha256'] != fingerprint:
                raise ValueError('conflicting identity reuse')
            return event
    material = decode(state['material'])
    before = encode(material)
    receipts = []
    for op in operations:
        try:
            material = operation(material, op)
            receipts.append(dict(status='ok', material=encode(material)))
        except (ValueError, KeyError, TypeError, FileNotFoundError) as error:
            receipts.append(dict(status='error', error_type=type(error).__name__, error=str(error)))
    pre_tick = encode(material)
    if state['mode'] == 'changing':
        material = evolve(material)
    event = dict(reply_id=reply_id, request_sha256=fingerprint,
                 prior_event_sha256=digest(state['events'][-1]) if state['events'] else None,
                 before=before, operations=operations, receipts=receipts,
                 pre_tick=pre_tick, after=encode(material), tick=state['tick']+1,
                 operation_count=state['operation_count']+len(operations))
    state.update(tick=event['tick'], operation_count=event['operation_count'], material=event['after'])
    state['events'].append(event)
    path = Path(path)
    pending = path.with_name(path.name+'.pending')
    # A stranded pending file must be resolved explicitly, never overwritten.
    if pending.exists():
        raise RuntimeError('unresolved pending replacement; inspect before retry')
    with pending.open('xb') as f:
        f.write(canonical(state)); f.flush(); os.fsync(f.fileno())
    if fail_at == 'before_replace':
        raise InterruptedError('injected before replacement')
    os.replace(pending, path)
    if fail_at == 'after_replace':
        raise InterruptedError('injected after replacement before directory fsync')
    fsync_dir(path.parent)
    return event

def recover_pending(path):
    """Seal a verified pure-state extension. Does not execute any operation."""
    path = Path(path); pending = path.with_name(path.name+'.pending')
    old, proposed = read(path), read(pending)
    if (proposed['version'], proposed['mode']) != (old['version'], old['mode']):
        raise ValueError('pending law differs')
    if proposed['events'][:-1] != old['events'] or len(proposed['events']) != len(old['events'])+1:
        raise ValueError('pending is not a one-event extension')
    last = proposed['events'][-1]
    # Recompute the entire proposal from the old state, using no process execution.
    expected = json.loads(canonical(old))
    data = decode(expected['material']); receipts=[]
    for op in last['operations']:
        try:
            data=operation(data, op); receipts.append(dict(status='ok', material=encode(data)))
        except (ValueError, KeyError, TypeError, FileNotFoundError) as error:
            receipts.append(dict(status='error', error_type=type(error).__name__, error=str(error)))
    event=dict(reply_id=last['reply_id'], request_sha256=digest(dict(reply_id=last['reply_id'],operations=last['operations'])),
               prior_event_sha256=digest(old['events'][-1]) if old['events'] else None,
               before=old['material'],operations=last['operations'],receipts=receipts,
               pre_tick=encode(data),after=encode(evolve(data) if old['mode']=='changing' else data),
               tick=old['tick']+1,operation_count=old['operation_count']+len(last['operations']))
    expected.update(tick=event['tick'],operation_count=event['operation_count'],material=event['after'])
    expected['events'].append(event)
    if proposed != expected:
        raise ValueError('pending proposal does not recompute exactly')
    os.replace(pending,path); fsync_dir(path.parent)
    return event
