"""Versioned data-only export/import. No SQL, code or file paths from bundles."""
import hashlib
import json
import os
from pathlib import Path
import tempfile

VERSIONS = {'bundle': 'cw-bundle-1', 'language': 'cw-scheme-1',
            'evaluator': 'cw-eval-1', 'cost': 'cw-cost-1',
            'protocol': 'cw-portability-1'}
TABLES = {
    'meta': ('key', 'value'), 'artifacts': ('id', 'kind', 'record', 'size'),
    'aliases': ('name', 'id'), 'snapshots': ('id', 'record'),
    'requests': ('id', 'hash', 'envelope', 'state', 'before_id', 'receipt', 'reserved'),
    'events': ('sequence', 'id', 'record'),
    'captures': ('id', 'request_id', 'record'),
    'capture_links': ('request_id', 'capture_id'),
}


class BundleError(Exception):
    pass


def packed(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(packed(value)).hexdigest()


def _publish_file(temporary, destination):
    destination = Path(destination)
    # Atomic create without overwrite, on the same filesystem.
    os.link(temporary, destination)
    os.unlink(temporary)
    fd = os.open(destination.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def export_world(world, destination):
    destination = Path(destination)
    if destination.exists():
        raise BundleError('destination exists')
    with world.lock:
        world.verify_integrity()
        if world.db.execute("SELECT 1 FROM requests WHERE state!='TERMINAL'").fetchone():
            raise BundleError('unsettled request')
        world.db.execute('BEGIN IMMEDIATE')
        try:
            tables = {}
            for table, columns in TABLES.items():
                rows = [dict(row) for row in world.db.execute('SELECT '+','.join(columns)+' FROM '+table)]
                tables[table] = sorted(rows, key=packed)
            body = {'schema': 'cw-bundle-1', 'versions': VERSIONS,
                    'profile': world.profile, 'tables': tables,
                    'manifest': {t: {'rows': len(v), 'sha256': digest(v)} for t, v in tables.items()}}
            result = {**body, 'sha256': digest(body)}
            raw = packed(result)
            if len(raw) > world.profile['max_bundle_bytes']:
                raise BundleError('bundle size limit')
        finally:
            world.db.rollback()  # Read-only export leaves the live world intact.
    fd, temporary = tempfile.mkstemp(prefix='.cw-export-', dir=destination.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw); handle.flush(); os.fsync(handle.fileno())
        _publish_file(temporary, destination)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return {'sha256': result['sha256'], 'bytes': len(raw), 'snapshot': world.snapshot()['id']}


def _load_bundle(path, profile):
    if Path(path).stat().st_size > profile['max_bundle_bytes']:
        raise BundleError('bundle size limit')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise BundleError('duplicate key')
            result[key] = value
        return result
    def integer(value):
        if len(value.lstrip('-')) > 20:
            raise BundleError('integer size limit')
        return int(value)
    def no_float(value):
        raise BundleError('noninteger JSON number')
    try:
        bundle = json.loads(Path(path).read_bytes(), object_pairs_hook=unique,
                            parse_int=integer, parse_float=no_float, parse_constant=no_float)
        if set(bundle) != {'schema', 'versions', 'profile', 'tables', 'manifest', 'sha256'}:
            raise BundleError('bundle fields')
        if bundle['schema'] != 'cw-bundle-1' or bundle['versions'] != VERSIONS:
            raise BundleError('unsupported version')
        if bundle['profile'] != profile or type(bundle['profile']) is not dict:
            raise BundleError('profile mismatch')
        if bundle['sha256'] != digest({k: v for k, v in bundle.items() if k != 'sha256'}):
            raise BundleError('bundle checksum')
        if set(bundle['tables']) != set(TABLES) or set(bundle['manifest']) != set(TABLES):
            raise BundleError('table set')
        caps = {'meta': 64, 'artifacts': profile['max_artifacts'], 'aliases': profile['max_aliases'],
                'snapshots': profile['max_actions'] + 1, 'requests': profile['max_actions'],
                'events': profile['max_actions'], 'captures': profile['max_actions'],
                'capture_links': profile['max_actions']}
        for table, columns in TABLES.items():
            rows = bundle['tables'][table]
            if type(rows) is not list or len(rows) > caps[table]:
                raise BundleError('row limit')
            if bundle['manifest'][table] != {'rows': len(rows), 'sha256': digest(rows)}:
                raise BundleError('table checksum')
            for row in rows:
                if type(row) is not dict or set(row) != set(columns):
                    raise BundleError('row fields')
                for col, value in row.items():
                    is_number = col in ('size', 'reserved', 'sequence')
                    if is_number:
                        if type(value) is not int or value < 0:
                            raise BundleError('numeric field')
                    elif value is not None and type(value) is not str:
                        raise BundleError('text field')
                    elif value is None and col != 'receipt':
                        raise BundleError('unexpected null')
        if any(row['state'] != 'TERMINAL' or row['receipt'] is None for row in bundle['tables']['requests']):
            raise BundleError('unsettled request')
        return bundle
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError) as exc:
        raise BundleError('malformed bundle') from exc


def validate_world(world):
    import scheme_core as sc
    from world_store import canonical, _safe
    world.verify_integrity()
    profile = world.profile
    if world.db.execute('PRAGMA foreign_key_check').fetchone():
        raise BundleError('foreign key violation')
    if json.loads(world._meta('profile')) != profile:
        raise BundleError('retained profile mismatch')
    actual_size = world.db.execute('SELECT COALESCE(SUM(size),0) FROM artifacts').fetchone()[0]
    if actual_size > profile['max_world_bytes']:
        raise BundleError('artifact capacity')
    for row in world.db.execute('SELECT * FROM artifacts'):
        if row['size'] != len(row['record'].encode()) or row['size'] > profile['max_artifact_bytes']:
            raise BundleError('artifact size mismatch')
        art = world.load_artifact(row['id'])
        if art['kind'] == 'data':
            sc.check_value(art['payload'], profile)
            if sc.value_wire(art['payload']) != json.loads(row['record'])['payload']:
                raise BundleError('noncanonical data')
        elif art['kind'] == 'procedure':
            p = art['payload']
            if p['language_version'] != VERSIONS['language'] or p['evaluator_version'] != VERSIONS['evaluator']:
                raise BundleError('procedure version')
            for ref in p['bindings'].values():
                if world.load_artifact(ref['id'])['kind'] != ref['kind']:
                    raise BundleError('dependency kind')
            compiled = sc.compile_definition(sc.parse_one(p['source'], profile), p['bindings'],
                                             world.load_artifact, profile)
            if any(compiled[k] != p[k] for k in ('name', 'params', 'body', 'bindings')):
                raise BundleError('procedure source/capture mismatch')
        else:
            raise BundleError('artifact kind')
    for row in world.db.execute('SELECT record FROM snapshots'):
        snapshot = json.loads(row['record'])
        if snapshot['world_id'] != world._meta('world_id'):
            raise BundleError('snapshot world identity')
        ids = snapshot['artifacts']
        if ids != sorted(set(ids)):
            raise BundleError('snapshot artifact set')
        for aid in ids:
            world.load_artifact(aid)
        if any(aid not in ids for name, aid in snapshot['aliases']):
            raise BundleError('snapshot dangling alias')
        names = [name for name, aid in snapshot['aliases']]
        if names != sorted(set(names)):
            raise BundleError('snapshot alias set')
    if int(world._meta('actions')) != world.db.execute('SELECT COUNT(*) FROM requests').fetchone()[0]:
        raise BundleError('action count')
    if world._metadata_bytes() > profile['max_metadata_bytes']:
        raise BundleError('metadata capacity')
    audit_bytes = 0
    fuel = allocation = 0
    for row in world.db.execute('SELECT * FROM requests'):
        receipt = json.loads(row['receipt']); event = receipt['event']
        envelope = json.loads(row['envelope'])
        if envelope['world_id'] != world._meta('world_id') or event['world_id'] != world._meta('world_id'):
            raise BundleError('request world identity')
        if envelope['request_id'] != row['id'] or event['request_id'] != row['id']:
            raise BundleError('request identity')
        audit_bytes += len(row['envelope'].encode()) + len(row['receipt'].encode())
        fuel += int(event['usage']['quota_fuel_charged'])
        allocation += int(event['usage']['quota_allocation_charged'])
        retained = world.db.execute('SELECT record FROM events WHERE id=?', (receipt['receipt_id'],)).fetchone()
        if not retained or canonical(event).decode() != retained['record']:
            raise BundleError('receipt event mismatch')
        for key, expected in (('status', event['status']), ('error', event['error']),
                              ('world_snapshot', event['after_world'])):
            if receipt[key] != expected:
                raise BundleError('receipt projection mismatch')
        if receipt['audit_after'] != {'sequence': event['audit_after_sequence'], 'head': receipt['receipt_id']}:
            raise BundleError('receipt audit mismatch')
        value = None
        if event['status'] == 'COMPUTED':
            value = sc.value_from_wire(event['result']['value'])
        elif event['status'] == 'OBSERVED':
            value = event['result']['projection']
        elif event['status'] == 'PUBLISHED':
            envelope = json.loads(row['envelope'])
            if str(sc.parse_one(envelope['command'], profile)[0]) == 'run-save':
                value = world.load_artifact(event['result']['artifact_ids'][0])['payload']
        if _safe(receipt['value']) != _safe(value):
            raise BundleError('receipt value mismatch')
    if audit_bytes != int(world._meta('audit_bytes')) or audit_bytes > profile['max_audit_bytes']:
        raise BundleError('audit byte accounting')
    if fuel != int(world._meta('visit_fuel')) or not 0 <= fuel <= profile['max_visit_fuel']:
        raise BundleError('fuel accounting')
    if allocation != int(world._meta('visit_alloc')) or not 0 <= allocation <= profile['max_visit_allocation']:
        raise BundleError('allocation accounting')
    for link in world.db.execute('SELECT request_id,capture_id FROM capture_links'):
        request = world.db.execute('SELECT envelope FROM requests WHERE id=?', (link['request_id'],)).fetchone()
        record = world.db.execute('SELECT record FROM captures WHERE id=?', (link['capture_id'],)).fetchone()
        if not request or not record:
            raise BundleError('capture link')
        capture = json.loads(record['record']); envelope = json.loads(request['envelope'])
        if capture['snapshot_id'] != envelope['expected_world_snapshot']:
            raise BundleError('capture snapshot')
        saved = world.db.execute('SELECT record FROM snapshots WHERE id=?', (capture['snapshot_id'],)).fetchone()
        if not saved:
            raise BundleError('capture missing snapshot')
        snapshot = json.loads(saved['record'])
        namespace = {name: {'id': aid, 'kind': world.load_artifact(aid)['kind']}
                     for name, aid in snapshot['aliases']}
        action = sc.parse_one(envelope['command'], profile)
        if str(action[0]) not in ('run', 'run-save'):
            raise BundleError('capture command')
        compiled = sc.compile_expression(action[-1], namespace, world.load_artifact, profile)
        if capture['resolved_ast'] != compiled['body']:
            raise BundleError('capture source mismatch')
        if capture['direct_dependencies'] != sorted({x['id'] for x in compiled['bindings'].values()}):
            raise BundleError('capture dependency mismatch')
    return world.verify_integrity()


def import_world(source, destination, profile):
    from world_store import World
    destination = Path(destination)
    if any(Path(str(destination) + suffix).exists() for suffix in ('', '-wal', '-shm', '.owner.lock')):
        raise BundleError('destination exists')
    bundle = _load_bundle(source, profile)
    fd, temporary = tempfile.mkstemp(prefix='.cw-import-', suffix='.sqlite', dir=destination.parent)
    os.close(fd)
    world = None
    try:
        world = World(temporary, profile)
        world.db.execute('BEGIN IMMEDIATE')
        for table in ('aliases', 'capture_links', 'captures', 'requests', 'events', 'snapshots', 'artifacts', 'meta'):
            world.db.execute('DELETE FROM ' + table)
        for table in ('meta', 'artifacts', 'snapshots', 'requests', 'events', 'captures', 'capture_links', 'aliases'):
            columns = TABLES[table]
            for row in bundle['tables'][table]:
                world.db.execute('INSERT INTO '+table+' ('+','.join(columns)+') VALUES ('+
                                 ','.join('?' for _ in columns)+')', tuple(row[k] for k in columns))
        world.db.commit()
        result = validate_world(world)
        world.db.execute('PRAGMA wal_checkpoint(TRUNCATE)')
        world.close(); world = None
        with open(temporary, 'rb') as file:
            os.fsync(file.fileno())
        _publish_file(temporary, destination)
        return result
    except Exception as exc:
        if isinstance(exc, BundleError):
            raise
        raise BundleError('invalid world state') from exc
    finally:
        if world is not None:
            world.close()
        for suffix in ('', '-wal', '-shm', '.owner.lock'):
            Path(temporary + suffix).unlink(missing_ok=True)
