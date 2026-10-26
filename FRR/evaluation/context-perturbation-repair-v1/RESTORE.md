# Restore evidence and current completed review

The original stopped-state archive is immutable and includes the historical failing replay. Restore scientific data separately from current review files so an old snapshot does not replace the resumed audit.

1. Assemble the original data archive with STATE_ARCHIVE_MANIFEST.json:

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
tar -xJf stopped-state.tar.xz --wildcards 'run/*' 'attempt-01/*' 'frozen-attempt-01/*'
```

2. Assemble the current completion archive with COMPLETION_ARCHIVE_MANIFEST.json by the same part/hash loop above, using that manifest filename. Then:

```bash
tar -xJf completion-review.tar.xz
```

It contains current code, final reports, complete error classifications, original failure reports and audit versions; all exact file hashes are listed in its manifest. It does not duplicate scientific data already present in the stopped-state archive. The original STOP_STATUS.json, failing REPLAY_RESULT.json and original paused archive are historical and unchanged. Current status is RESUME_STATUS.json.

3. Read FINAL_REPORT.md and review/REPLAY_REPORT.md before replaying anything. Original strict ordered replay remains FAIL. Its1,170errors are exhaustively classified as ordering-only cascades; fixed-ID/membership checks pass separately. Re-executing review/replay_audit.py intentionally reproduces the strict failure. Classification uses review/replay_classification.py; inspect its arguments/output destinations before execution. Other independent reconstruction scripts/receipts are in review/. They use NumPy/standard library and shared saved data, never the main experiment.

Restoration does not request a main rerun or convert an exact-order failure to PASS. Original source studies may need their own documented restoration for predecessor-specific checks. RESTORE_AT_USER_PAUSE.md retains the original full paused-snapshot instructions; use those only in a separate directory if the entire interrupted state is wanted.
