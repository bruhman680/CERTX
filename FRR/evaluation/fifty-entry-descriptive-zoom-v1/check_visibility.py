"""Read-only check of the captured stop-status visibility gap."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;E=R.parent/'source-access-three-cycle-v1/cycle3/environment'
es=[json.loads(x) for x in (E/'NOTEBOOK.jsonl').read_text().splitlines()];raw=json.loads((E/'events/000122.json').read_text());nxt=json.loads((E/'events/000123.json').read_text());record=json.loads((R/'VISIBILITY_BOUNDARY.json').read_text())
assert raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96
assert 'stop' not in es[122] and 'token_limit' not in nxt['prompt'] and 122 in nxt['history_steps']
assert record['notebook_projection_fields']==list(es[122].keys()) and record['actual_feedback']==es[122]['feedback'] and record['host_result']==es[122]['host_result']
print('Captured122→123stop-status visibility verified; primary unchanged.')
