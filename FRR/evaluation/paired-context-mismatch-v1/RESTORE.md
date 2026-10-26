# Restore the complete original run

Git stores the25,950,288-byte run archive as26ordered binary volumes in archive/. Assemble before extraction. This preserves all25original files (67,822,575bytes), including full candidate-level outputs, exact NPZ bytes, source copies and diagnostics. No successful rows or seeds were selected. ARCHIVE_MANIFEST.json binds every volume, assembled archive and original file.

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
        assert hashlib.sha256(b).hexdigest()==part['sha256'],part['path']
        out.write(b)
b=Path(m['archive']).read_bytes()
assert len(b)==m['bytes']
assert hashlib.sha256(b).hexdigest()==m['sha256']
print('Archive verified')
PY
tar -xJf run.tar.xz
python - <<'PY'
from pathlib import Path
import hashlib,json
m=json.loads(Path('ARCHIVE_MANIFEST.json').read_text())
for name,entry in m['files'].items():
    b=Path(name).read_bytes()
    assert len(b)==entry['bytes']
    assert hashlib.sha256(b).hexdigest()==entry['sha256'],name
print('All original files verified:',len(m['files']))
PY
```

Optional saved-data audits, NumPy/standard library:

```bash
python review/audit_ledger.py run
python review/replay.py run
python summarize.py
```

The ledger audit checks source comparison claims against the predecessor run; restore its archive too if absent. Both audit scripts write current receipts in review/; published historical receipts remain in Git. Neither invokes the main experiment. Main code refuses a nonempty run/ and is not requested by restoration. Prospective plans, initial audit failures and actual source-inspection scopes are in the review records. Predecessor inputs are already copied inside this archive; no training/model API or downloaded package is needed for array replay.
