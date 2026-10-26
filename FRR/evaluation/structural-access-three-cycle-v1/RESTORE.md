# Restore complete original run

`run.tar.xz` contains all16original run files,31,028,502 uncompressed bytes. Archive bytes and every original file hash are in ARCHIVE_MANIFEST.json. The archive preserves exact bytes, not rewritten CSVs or selected successful rows. Unpacked run/ is not duplicated in Git.

From this directory:

```bash
tar -xJf run.tar.xz
python - <<'PY'
from pathlib import Path
import hashlib,json
m=json.loads(Path('ARCHIVE_MANIFEST.json').read_text())
assert hashlib.sha256(Path(m['archive']).read_bytes()).hexdigest()==m['sha256']
for name,entry in m['files'].items():
    content=Path(name).read_bytes()
    assert len(content)==entry['bytes']
    assert hashlib.sha256(content).hexdigest()==entry['sha256'],name
print('All original run bytes verified:',len(m['files']))
PY
```

Optional saved-data replay (NumPy plus standard library):

```bash
python review/audit_ledger.py run
python review/replay.py run
python summarize.py
```

Inspect script arguments/output locations before use; replay writes its current receipt beside the script. Saved published receipts remain available in Git. These audit scripts do not invoke the main experiment. Main code refuses an existing run/ATTEMPT.json; restoring is not a request to rerun it. Fixed audit sample, source-inspection limitation and preserved initial replay are documented in review/REPLAY_REPORT.md.
