"""Read-only compact observation; raw generations remain in the primary archive."""
from pathlib import Path
from collections import Counter
import json
D=Path(__file__).resolve().parent;E=D.parent/'source-access-three-cycle-v1/cycle3/environment'
rows=[]
for p in sorted((E/'events').glob('*.json')):
 if 550<=int(p.stem)<650:rows.append(json.loads(p.read_text()))
windows=[json.loads(p.read_text()) for p in sorted(D.glob('WINDOW_*_SUMMARY.json'))]
print(json.dumps(dict(committed_next_step=550+len(rows),new_entries=len(rows),checked_windows=len(windows),
 host_kinds=dict(Counter(r['host_result']['kind'] for r in rows)),stops=dict(Counter(r['stop'] for r in rows)),
 dollar_containing=sum('$' in r['text'] for r in rows),exact_unique_texts=len({r['text'] for r in rows}),
 latest_excerpt=rows[-1]['text'][:100] if rows else None,
 last_verified=windows[-1]['next_step'] if windows else 550,
 error_log_bytes=(D/'BLOCK.stderr').stat().st_size,paused=(E/'PAUSE').exists())))
