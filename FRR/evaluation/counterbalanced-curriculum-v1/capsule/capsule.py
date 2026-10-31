"""Small, deterministic adapter preservation capsules. Standard library only."""
import argparse
import gzip
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import struct
import tarfile

MAX_FILE = 32 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024
EXCLUDED = ['dense base weights', 'old full-weight checkpoints', 'terminal KV caches',
            'other experiment history, code, data and logs']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def strict_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()

def read_small(path):
    path = Path(path)
    if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_FILE:
        raise ValueError(f'not a bounded regular file: {path}')
    with path.open('rb') as handle:
        data = handle.read(MAX_FILE + 1)
    if len(data) > MAX_FILE:
        raise ValueError('file grew beyond limit')
    return data

def checked(data, declared):
    if not isinstance(declared, str) or sha(data) != declared:
        raise ValueError('declared SHA256 mismatch')

def validate_adapter(data, manifest):
    """Validate F32 safetensors completely without torch/pickle/model loading."""
    if len(data) < 8:
        raise ValueError('short safetensors')
    length, = struct.unpack('<Q', data[:8])
    if not 2 <= length <= 1024 * 1024 or 8 + length > len(data):
        raise ValueError('invalid header size')
    header = strict_json(data[8:8 + length])
    tensors = manifest.get('tensors')
    if not isinstance(header, dict) or not isinstance(tensors, dict) or not tensors:
        raise ValueError('missing tensor map')
    names = set(header) - {'__metadata__'}
    if names != set(tensors):
        raise ValueError('tensor names differ')
    payload = data[8 + length:]
    regions = []
    for name in sorted(names):
        entry = header[name]
        declared = tensors[name]
        if not isinstance(entry, dict) or set(entry) != {'dtype', 'shape', 'data_offsets'}:
            raise ValueError('unsupported tensor header')
        shape = entry['shape']
        if (entry['dtype'] != 'F32' or declared.get('dtype') != 'torch.float32'
                or not isinstance(shape, list) or any(type(x) is not int or x < 0 for x in shape)
                or shape != declared.get('shape')):
            raise ValueError('unsupported dtype or mismatched shape')
        offsets = entry['data_offsets']
        if (not isinstance(offsets, list) or len(offsets) != 2
                or any(type(x) is not int for x in offsets)):
            raise ValueError('invalid offsets')
        start, end = offsets
        if start < 0 or end < start or end > len(payload) or end - start != math.prod(shape) * 4:
            raise ValueError('tensor byte size mismatch')
        regions.append((start, end))
        if any(not math.isfinite(x[0]) for x in struct.iter_unpack('<f', payload[start:end])):
            raise ValueError('nonfinite adapter')
    cursor = 0
    for start, end in sorted(regions):
        if start != cursor:
            raise ValueError('overlapping or unaccounted tensor data')
        cursor = end
    if cursor != len(payload):
        raise ValueError('unaccounted tensor data')
    checked(data, manifest['sha256'])
    return len(names)

def collect(manifest_path, role):
    path = Path(manifest_path).absolute()
    raw = read_small(path)
    m = strict_json(raw)
    base = m['base_pin']
    if not isinstance(base, dict) or not all(isinstance(base.get(x), str) and base[x]
                                           for x in ('model_id', 'revision', 'weights_sha256')):
        raise ValueError('missing base pin')
    result = {f'{role}/TRAINING_MANIFEST.json': raw}
    paths = {'initial': path.parent / 'initial_adapter', 'final': Path(m['checkpoint'])}
    for phase, folder in paths.items():
        if not folder.is_absolute():
            folder = path.parent / folder
        hashes = m['initial_files_sha256' if phase == 'initial' else 'checkpoint_files_sha256']
        if set(hashes) != {'adapter.safetensors', 'manifest.json'}:
            raise ValueError('unexpected checkpoint files')
        for name in sorted(hashes):
            data = read_small(folder / name)
            checked(data, hashes[name])
            result[f'{role}/{phase}/{name}'] = data
        am = strict_json(result[f'{role}/{phase}/manifest.json'])
        if am['base_pin'] != base:
            raise ValueError('adapter base pin differs')
        validate_adapter(result[f'{role}/{phase}/adapter.safetensors'], am)
    optimizer = Path(m['optimizer'])
    if not optimizer.is_absolute():
        optimizer = path.parent / optimizer
    data = read_small(optimizer)
    checked(data, m['optimizer_sha256'])
    result[f'{role}/optimizer_state.pt'] = data
    return result, base

def safe_name(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and str(p) == name and '\\' not in name

def verify_payload(files):
    index = strict_json(files['CAPSULE.json'])
    if set(index) != {'format_version', 'members', 'base_pin', 'excluded', 'limitations'} or index['format_version'] != 1:
        raise ValueError('unsupported capsule index')
    if set(files) != set(index['members']) | {'CAPSULE.json'}:
        raise ValueError('archive inventory mismatch')
    expected = {f'{role}/{phase}/{name}' for role in ('control', 'candidate')
                for phase in ('initial', 'final') for name in ('manifest.json', 'adapter.safetensors')}
    expected |= {f'{role}/{name}' for role in ('control', 'candidate')
                 for name in ('TRAINING_MANIFEST.json', 'optimizer_state.pt')}
    if set(index['members']) != expected:
        raise ValueError('unexpected capsule members')
    for name, record in index['members'].items():
        if not safe_name(name) or set(record) != {'sha256', 'size'} or len(files[name]) != record['size']:
            raise ValueError('invalid member record')
        checked(files[name], record['sha256'])
    for role in ('control', 'candidate'):
        training = strict_json(files[f'{role}/TRAINING_MANIFEST.json'])
        if training['base_pin'] != index['base_pin']:
            raise ValueError('base pin mismatch')
        checked(files[f'{role}/optimizer_state.pt'], training['optimizer_sha256'])
        for phase in ('initial', 'final'):
            hashes = training['initial_files_sha256' if phase == 'initial' else 'checkpoint_files_sha256']
            for name in ('adapter.safetensors', 'manifest.json'):
                checked(files[f'{role}/{phase}/{name}'], hashes[name])
            adapter_manifest = strict_json(files[f'{role}/{phase}/manifest.json'])
            if adapter_manifest['base_pin'] != index['base_pin']:
                raise ValueError('adapter base pin mismatch')
            validate_adapter(files[f'{role}/{phase}/adapter.safetensors'], adapter_manifest)
    return {'status': 'verified', 'members': len(files), 'base_pin': index['base_pin'],
            'excluded': index['excluded']}

def verify_adapter_capsule(archive):
    files = {}
    total = 0
    with tarfile.open(name=None if hasattr(archive, 'read') else archive,
                      fileobj=archive if hasattr(archive, 'read') else None, mode='r:gz') as tf:
        for item in tf:
            if not item.isfile() or not safe_name(item.name) or item.name in files or item.size > MAX_FILE:
                raise ValueError('unsafe, duplicate or oversized member')
            total += item.size
            if total > MAX_TOTAL or len(files) >= 13:
                raise ValueError('archive exceeds bounds')
            files[item.name] = tf.extractfile(item).read()
    return verify_payload(files)

def build_adapter_capsule(control_manifest, candidate_manifest, outputtar):
    """Read/validate both completed branches, then create output exclusively."""
    output = Path(outputtar)
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    control, base = collect(control_manifest, 'control')
    candidate, candidate_base = collect(candidate_manifest, 'candidate')
    if base != candidate_base:
        raise ValueError('control and candidate require the same base pin')
    files = {**control, **candidate}
    if sum(map(len, files.values())) > MAX_TOTAL:
        raise ValueError('capsule too large')
    files['CAPSULE.json'] = encoded({'format_version': 1, 'base_pin': base,
        'members': {name: {'sha256': sha(data), 'size': len(data)} for name, data in sorted(files.items())},
        'excluded': EXCLUDED,
        'limitations': 'Local capsule is not an independent backup until copied off workspace. Requires pinned original base and compatible runtime; excludes other history. Optimizer bytes are hash-checked, never unpickled.'})
    verify_payload(files)
    # Construct and verify before exclusive output creation. Fixed metadata makes bytes deterministic.
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode='wb', filename='', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w', format=tarfile.USTAR_FORMAT) as tf:
            for name, data in sorted(files.items()):
                info = tarfile.TarInfo(name)
                info.size = len(data)
                info.mode = 0o600
                info.mtime = 0
                tf.addfile(info, io.BytesIO(data))
    result = buffer.getvalue()
    receipt = verify_adapter_capsule(io.BytesIO(result))
    # No overwrite, delete, rename or source mutation, even on errors.
    with output.open('xb') as handle:
        handle.write(result)
        handle.flush()
        os.fsync(handle.fileno())
    verify_adapter_capsule(output)
    receipt.update({'archive_sha256': sha(result), 'archive_bytes': len(result), 'output': str(output)})
    return receipt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build')
    build.add_argument('control_manifest')
    build.add_argument('candidate_manifest')
    build.add_argument('outputtar')
    verify = sub.add_parser('verify')
    verify.add_argument('archive')
    args = parser.parse_args()
    if args.command == 'build':
        result = build_adapter_capsule(args.control_manifest, args.candidate_manifest, args.outputtar)
    else:
        result = verify_adapter_capsule(args.archive)
    print(json.dumps(result, sort_keys=True, indent=2))
