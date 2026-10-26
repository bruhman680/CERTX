# Restore exact paused state

`STATE_ARCHIVE_MANIFEST.json` lists ordered binary volumes, assembled archive hash and every original file. From this directory:

```bash
python - <<'PY'
from pathlib import Path
import hashlib,json
m=json.loads(Path('STATE_ARCHIVE_MANIFEST.json').read_text())
with Path(m['archive']).open('wb') as out:
    for part in m['parts']:
        b=Path(part['path']).read_bytes()
        assert len(b)==part['bytes']
        assert hashlib.sha256(b).hexdigest()==part['sha256']
        out.write(b)
assert hashlib.sha256(Path(m['archive']).read_bytes()).hexdigest()==m['sha256']
PY
tar -xJf stopped-state.tar.xz
python - <<'PY'
from pathlib import Path
import hashlib,json
m=json.loads(Path('STATE_ARCHIVE_MANIFEST.json').read_text())
for name,entry in m['files'].items():
    b=Path(name).read_bytes()
    assert len(b)==entry['bytes']
    assert hashlib.sha256(b).hexdigest()==entry['sha256'],name
print('Paused files verified:',len(m['files']))
PY
```

The archive includes the completed run, failed pre-fit attempt, both original/repaired source snapshots and freezes, prospective plans, current incomplete replay and its logs. It is an interrupted work record, not a passing result. Read REPORT.md and STOP_STATUS.json before acting. Restore does not request any experiment/audit rerun; diagnose the saved1,170replay comparison errors first when the user resumes. Old source archives remain in their pinned study directories and may need restoration for predecessor-specific checks. No new provider, training or installation needed.
