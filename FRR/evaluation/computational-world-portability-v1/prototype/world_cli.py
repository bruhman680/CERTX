"""Process-bounded entry point for the isolated computational-world prototype.

POSIX host limits supplement, rather than replace, interpreter accounting.
The parent reconciles interrupted requests only after the worker has exited.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid


def run_isolated(db, profile, request_id, expected, source, timeout=None):
    try:
        source_size = len(source.encode('utf-8')) if isinstance(source, str) else None
    except UnicodeError:
        return {'status': 'NOT_ADMITTED', 'error': {'code': 'SYNTAX'},
                'value': None, 'world_snapshot': expected}
    if source_size is None or source_size > profile['max_source_bytes']:
        return {'status': 'NOT_ADMITTED', 'error': {'code': 'SUBMISSION_BYTES'},
                'value': None, 'world_snapshot': expected}
    with tempfile.TemporaryDirectory(prefix='cw-worker-') as directory:
        base = Path(directory)
        request = {'db': str(Path(db).resolve()), 'profile': profile,
                   'request_id': request_id, 'expected': expected, 'source': source}
        (base / 'request.json').write_text(json.dumps(request), encoding='utf-8')
        worker = subprocess.Popen([sys.executable, str(Path(__file__).resolve()),
                                   '--worker', str(base)], stdin=subprocess.DEVNULL,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        watchdog = False
        try:
            worker.wait(timeout=profile['host_timeout_seconds'] if timeout is None else timeout)
        except subprocess.TimeoutExpired:
            watchdog = True
            worker.kill()
            worker.wait()
        output = base / 'result.json'
        if worker.returncode == 0 and output.exists() and output.stat().st_size <= 2 * profile['max_receipt_bytes']:
            try:
                return json.loads(output.read_text())
            except (ValueError, UnicodeError):
                pass  # Invalid host output requires the same commit reconciliation.

        # Never automatically rerun a request whose commit result is uncertain.
        # World recovery terminates abandoned admitted work; an already committed
        # request retains its original receipt.
        from world_store import World
        try:
            world = World(db, profile)
            try:
                row = world.db.execute('SELECT receipt,envelope FROM requests WHERE id=?',
                                       (request_id,)).fetchone()
                if row:
                    retained = json.loads(row['envelope'])
                    if retained['command'] != source or retained['expected_world_snapshot'] != expected:
                        return {'status': 'REQUEST_ID_CONFLICT', 'request_id': request_id,
                                'error': {'code': 'REQUEST_ID_CONFLICT'}, 'value': None,
                                'world_snapshot': world.snapshot()['id'],
                                'controller': {'worker_exit': worker.returncode,
                                               'watchdog': watchdog,
                                               'commit_certainty': 'existing_request_only'}}
                if row and row['receipt']:
                    result = json.loads(row['receipt'])
                    result['controller'] = {'worker_exit': worker.returncode,
                                            'watchdog': watchdog,
                                            'reconciled_after_exit': True}
                    return result
                return {'status': 'HOST_ABORT', 'request_id': request_id,
                        'error': {'code': 'WORKER_ABORT_BEFORE_ADMISSION'}, 'value': None,
                        'world_snapshot': world.snapshot()['id'],
                        'controller': {'worker_exit': worker.returncode,
                                       'watchdog': watchdog, 'commit_certainty': 'not_admitted'}}
            finally:
                world.close()
        except Exception:
            return {'status': 'HOST_STORAGE_UNKNOWN', 'request_id': request_id,
                    'error': {'code': 'RECONCILIATION_FAILED'}, 'value': None,
                    'controller': {'worker_exit': worker.returncode,
                                   'watchdog': watchdog, 'commit_certainty': 'unknown'}}


def compact_observation(receipt, profile):
    """Bound the model-facing view; retain the full receipt in the host ledger."""
    view = {key: receipt.get(key) for key in
            ('status', 'value', 'error', 'world_snapshot', 'request_id')}
    view['truncated'] = False
    event = receipt.get('event', {})
    projection = event.get('result', {}).get('projection')
    if projection is not None:
        view['value'] = None  # Avoid duplicating the same observation twice.
        view['projection'] = projection
    view['request_id'] = receipt.get('request_id') or event.get('request_id')
    limit = profile['max_observation_bytes']
    size = lambda value: len(json.dumps(value, ensure_ascii=False).encode('utf-8'))
    if size(view) > limit:
        view['value'] = None
        view.pop('projection', None)
        view['truncated'] = True
        view['detail'] = 'Full result retained in host receipt; inspect a published artifact when available.'
    if size(view) > limit:
        view['error'] = {'code': (receipt.get('error') or {}).get('code', 'VIEW_LIMIT')}
        view.pop('detail', None)
    if size(view) > limit:
        return {'status': 'VIEW_LIMIT', 'truncated': True}
    return view


def worker_main(directory):
    import resource
    base = Path(directory)
    request = json.loads((base / 'request.json').read_text())
    profile = request['profile']
    resource.setrlimit(resource.RLIMIT_AS, (profile['host_memory_bytes'],) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (profile['host_cpu_seconds'],) * 2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (profile['host_file_bytes'],) * 2)
    from world_store import World
    world = World(request['db'], profile)
    try:
        result = world.submit(request['request_id'], request['expected'], request['source'])
    finally:
        world.close()
    encoded = json.dumps(result, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    if len(encoded) > 2 * profile['max_receipt_bytes']:
        raise RuntimeError('worker transport size limit')
    with (base / 'result.json').open('wb') as output:
        output.write(encoded)
        output.flush()
        os.fsync(output.fileno())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker')
    parser.add_argument('--db')
    parser.add_argument('--source')
    parser.add_argument('--request-id')
    parser.add_argument('--expected')
    args = parser.parse_args()
    if args.worker:
        worker_main(args.worker)
        return
    if not args.db or args.source is None:
        parser.error('--db and --source required')
    profile = json.loads((Path(__file__).resolve().parents[1] / 'constants.json').read_text())
    from world_store import World
    world = World(args.db, profile)
    try:
        expected = args.expected or world.snapshot()['id']
    finally:
        world.close()
    result = run_isolated(args.db, profile, args.request_id or uuid.uuid4().hex,
                          expected, args.source)
    print(json.dumps(compact_observation(result, profile), ensure_ascii=False))


if __name__ == '__main__':
    main()
