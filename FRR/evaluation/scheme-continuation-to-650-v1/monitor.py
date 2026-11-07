"""Compact read-only progress; raw data stay outside conversation context."""
from pathlib import Path
from collections import Counter
import json,sys
D=Path(__file__).resolve().parent;E=D.parent/'source-access-three-cycle-v1/cycle3/environment'
rows=[json.loads(p.read_text()) for p in sorted((E/'events').glob('*.json')) if 550<=int(p.stem)<650]
windows=sorted(D.glob('WINDOW_*_SUMMARY.json'))
info=dict(cursor=550+len(rows),checked_windows=len(windows),kinds=dict(Counter(r['host_result']['kind'] for r in rows)),stops=dict(Counter(r['stop'] for r in rows)),unique=len({r['text'] for r in rows}),error_bytes=(D/'BLOCK.stderr').stat().st_size)
other=[dict(step=r['step'],status=r['host_result'].get('status'),kind=r['host_result']['kind']) for r in rows if r['host_result']['kind']!='record_receipt']
if other:info['recent_actions']=other[-3:]
if '--peek' in sys.argv and rows:info['latest_excerpt']=rows[-1]['text'][:160]
print(json.dumps(info))
