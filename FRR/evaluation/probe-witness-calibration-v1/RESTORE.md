# Restore exact witness-calibration study

ARCHIVE_MANIFEST.json binds every ordered binary volume, assembled study-state.tar.xz and original file. Archive contains raw inputs, complete main outputs, source/draft/freeze history, failed/corrected auditor code/logs and reports. Storage volumes are not separate experiments. NumPy plus standard library suffices for saved-data checks; no API/training/install required.

From this directory:

```bash
python - <<'PY'
from pathlib import Path
import hashlib,json
m=json.loads(Path('ARCHIVE_MANIFEST.json').read_text())
with Path(m['archive']).open('wb') as out:
    for part in m['parts']:
        b=Path(part['path']).read_bytes()
        assert len(b)==part['bytes']
        assert hashlib.sha256(b).hexdigest()==part['sha256']
        out.write(b)
assert hashlib.sha256(Path(m['archive']).read_bytes()).hexdigest()==m['sha256']
PY
tar -xJf study-state.tar.xz
python - <<'PY'
from pathlib import Path
import hashlib,json
m=json.loads(Path('ARCHIVE_MANIFEST.json').read_text())
for name,e in m['files'].items():
    b=Path(name).read_bytes()
    assert len(b)==e['bytes']
    assert hashlib.sha256(b).hexdigest()==e['sha256'],name
print('Original study files verified:',len(m['files']))
PY
```

Read REPORT.md and review/REPLAY_REPORT.md before running audits. Independent ledger/replay scripts live in review/; inspect their input/output paths first, as they write new receipts. The source study may need its documented restoration for historical-control comparison. Original published receipts remain in Git. Do not rerun experiment.py merely to restore data: its nonempty-output guard protects history. Current replay PASS does not replace historical CRstrictFAIL. Source read limitations and the initial omitted-Q audit failure remain preserved.
