"""Check adopted-loop records and integrity; no experiment or model calls."""
import hashlib
import json
import tempfile
from pathlib import Path

from check_package import check, references

ROOT = Path(__file__).resolve().parents[1]


def verify_files(root, files):
    """Validate a local manifest. It is not a signature or a truth certificate."""
    root = root.resolve()
    if not files:
        raise ValueError('Empty evidence manifest')
    for relative, expected in files.items():
        path = (root / relative).resolve()
        if Path(relative).is_absolute() or not path.is_relative_to(root):
            raise ValueError(f'Evidence escapes root: {relative}')
        if not path.is_file():
            raise ValueError(f'Missing evidence: {relative}')
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Changed evidence: {relative}')
    return len(files)


def negative_controls():
    """Exercise integrity failures in temporary fixtures, not research evidence."""
    with tempfile.TemporaryDirectory() as name:
        base = Path(name)
        root = base / 'root'
        root.mkdir()
        evidence = root / 'evidence.txt'
        evidence.write_text('original')
        files = {'evidence.txt': hashlib.sha256(evidence.read_bytes()).hexdigest()}
        if verify_files(root, files) != 1:
            raise AssertionError('Valid control failed')
        evidence.write_text('changed')
        try:
            verify_files(root, files)
        except ValueError as error:
            if not str(error).startswith('Changed evidence:'):
                raise
        else:
            raise AssertionError('Changed-byte control was accepted')
        evidence.unlink()
        try:
            verify_files(root, files)
        except ValueError as error:
            if not str(error).startswith('Missing evidence:'):
                raise
        else:
            raise AssertionError('Missing-evidence control was accepted')
        outside = base / 'outside.txt'
        outside.write_text('outside')
        try:
            verify_files(root, {'../outside.txt': hashlib.sha256(outside.read_bytes()).hexdigest()})
        except ValueError as error:
            if not str(error).startswith('Evidence escapes root:'):
                raise
        else:
            raise AssertionError('Out-of-root control was accepted')
    return ['changed bytes rejected', 'missing evidence rejected', 'out-of-root evidence rejected']


def main():
    record = json.loads((ROOT / 'examples/bounded-loop-retrospective.json').read_text())
    check(record, json.loads((ROOT / 'state/schema.json').read_text()), 'retrospective')
    references(record)
    manifest = json.loads((ROOT / 'evaluation/BOUNDED_LOOP_EVIDENCE_MANIFEST.json').read_text())
    if manifest['recording'] != 'retrospective':
        raise ValueError('Retrospective provenance missing')
    expected_files = {artifact['reference'] for artifact in record['artifacts']}
    if expected_files != set(manifest['files']):
        raise ValueError('Record/manifest evidence mismatch')
    evidence_count = verify_files(ROOT, manifest['files'])
    core_count = verify_files(ROOT, json.loads((ROOT / 'evaluation/PRE_REFINEMENT_BASELINE_HASHES.json').read_text()))
    discovery = {
        'README.md': 'modules/bounded-experiment-loop.md',
        'modules/artifact-execution-harness.md': 'bounded-experiment-loop.md',
        'evaluation/PROTOCOL.md': '../modules/bounded-experiment-loop.md',
        'CURRENT_HANDOFF.md': 'modules/bounded-experiment-loop.md',
        'sync/CURRENT_ORIENTATION.md': '../modules/bounded-experiment-loop.md',
    }
    for source, target in discovery.items():
        if target not in (ROOT / source).read_text() or not (ROOT / source).parent.joinpath(target).is_file():
            raise ValueError(f'Broken discovery link: {source}')
    print(json.dumps({
        'record_schema_and_references': 'pass (package subset validator)',
        'original_pilot_artifacts_verified': evidence_count,
        'unchanged_core_hashes': core_count,
        'discovery_links': len(discovery),
        'negative_integrity_controls': negative_controls(),
        'scope': 'Local structure and byte identity only; no new agent trial, scientific validation or immutable storage guarantee.',
    }, indent=2))


if __name__ == '__main__':
    main()
