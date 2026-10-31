"""Pack this contact and its bridge, then verify bytes without extracting/unpickling.

Fixed local research snapshot; not a generic hostile-archive service or complete
offline environment. Destination is outside the source trees and never overwritten.
"""
from pathlib import Path
import hashlib
import io
import json
import tarfile

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
DEST = Path('/workspace/frr_capsules/simple-readout-and-selection-v1.tar.gz')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    studies = [ROOT, PARENT / 'readout-selection-bridge-v1']
    assert all(json.loads((s / 'run/RUN_MANIFEST.json').read_text())['status'] == 'complete' for s in studies)
    assert all(json.loads((s / 'CHECKS.json').read_text())['status'] == 'pass' for s in studies)
    sources = {}
    for study in studies:
        for p in sorted(study.rglob('*')):
            if '__pycache__' in p.parts or not p.is_file():
                continue
            if p.is_symlink():
                raise ValueError('No symlinks in fixed snapshot')
            sources[str(p.relative_to(PARENT))] = p
    assert sum(p.stat().st_size for p in sources.values()) < 128 * 1024**2
    entries = {name: {'sha256': digest(p.read_bytes()), 'bytes': p.stat().st_size} for name, p in sources.items()}
    manifest = {'format': 'fixed-research-snapshot-v1', 'members': entries,
        'base_model_included': False, 'python_environment_included': False,
        'older_history_included': False, 'optimizer_numeric_resume_tested': False,
        'instructions': 'Use pinned base and compatible runtime; adjust original absolute workspace paths. Preserve snapshot untouched. Code and records also published on CERTX research branch.'}
    payload = (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode()
    DEST.parent.mkdir(exist_ok=True)
    with tarfile.open(DEST, mode='x:gz') as tar:
        for name, p in sources.items():
            tar.add(p, arcname=name, recursive=False)
        info = tarfile.TarInfo('CAPSULE.json'); info.size = len(payload)
        tar.addfile(info, io.BytesIO(payload))
    with tarfile.open(DEST, mode='r:gz') as tar:
        members = tar.getmembers()
        assert len(members) == len(entries)+1
        assert len({m.name for m in members}) == len(members)
        assert all(m.isfile() for m in members)
        for m in members:
            b = tar.extractfile(m).read()
            if m.name == 'CAPSULE.json':
                assert b == payload
            else:
                assert len(b) == entries[m.name]['bytes']
                assert digest(b) == entries[m.name]['sha256']
    receipt = {'path': str(DEST), 'bytes': DEST.stat().st_size, 'sha256': digest(DEST.read_bytes()),
        'regular_members_verified': len(entries)+1, 'member_bytes_read_without_extraction': True,
        'pickle_not_loaded': True, 'snapshot_members': entries,
        'excludes': ['dense base weights', 'Python environment', 'older research outside these two studies'],
        'not_a_fresh_environment_or_optimizer_resume_rehearsal': True,
        'not_an_independent_backup_until_copied_off_workspace': True}
    with (ROOT / 'CAPSULE_RECEIPT.json').open('x') as f:
        json.dump(receipt, f, indent=2, sort_keys=True); f.write('\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'snapshot_members'}, indent=2))

if __name__ == '__main__':
    main()
