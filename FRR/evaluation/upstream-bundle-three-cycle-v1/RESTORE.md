# Restore the complete saved run

All15original run files are preserved byte-for-byte in [run.tar.xz](run.tar.xz). This includes raw NPZ inputs/queries, compressed per-query ledger, all fitted centres, full aggregates, numerical controls, source/protocol snapshots and original hash manifests. The archive is transport only; it does not rerun or alter the experiment. [ARCHIVE_MANIFEST.json](ARCHIVE_MANIFEST.json) gives every file's SHA256 plus the archive hash.

From this directory after checking out/downloading the progress branch:

```sh
tar -xJf run.tar.xz
```

Verify archived/restored bytes with Python's standard library:

```python
import hashlib, json
from pathlib import Path
m = json.loads(Path('ARCHIVE_MANIFEST.json').read_text())
assert hashlib.sha256(Path(m['archive']).read_bytes()).hexdigest() == m['archive_sha256']
for item in m['files']:
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256']
print('All original run bytes verified')
```

Readable [RUN_SUMMARY.json](RUN_SUMMARY.json) exposes selected slices and controls without extraction; the complete grid remains in the archive. Restore before these optional replays, which write their receipts beside the review scripts:

```sh
python review/audit.py run
python review/audit_ledger.py run
```

These are different checks on the saved data, not fresh empirical trials. The saved main source can reproduce into a new directory with NumPy installed; existing output directories are refused. ZIP timestamps can differ in a newly generated NPZ, so compare actual arrays/hashes and results as well as transport bytes.

Publication omits redundant unpacked run files to limit repository bulk. Local extraction creates `run/`; no remote link to an unpacked file is required for reading the summary/report. Python bytecode caches are not research artifacts.
