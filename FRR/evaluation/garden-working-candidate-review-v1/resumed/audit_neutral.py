"""Read-only neutral-diagnostic audit; no model or guest operation."""
from pathlib import Path
import hashlib, json
from audit_retained import audit_store, read

H = Path(__file__).resolve().parent
C = H.parents[1] / 'minimal-garden-candidate-v1'
N = C / 'diagnostics/neutral'
result = read(N/'RESULT.json')
assert result['status']=='completed' and result['model_calls']==6
check = audit_store(N/'run')
assert result['first_memory_file'] is None and result['final_memory_file'] is None
assert all(r['memory_file_after'] is None and r['new_files_since_initial']=={} for r in result['results'])
assert all(r['receipt']['exit_code']==1 and r['receipt']['boundary'] is None for r in result['actual_error_receipts'])
assert all(r['feedback_nonempty'] and r['delivered'] for r in result['feedback_delivery'])
out = {'date':'2026-11-09 America/Chicago','status':'pass','review_model_calls':0,
    'retained_world_chain':check,'model_target_file_write_read_demonstrated':False,
    'native_error_receipts':len(result['actual_error_receipts']),
    'actual_feedback_transitions':len(result['feedback_delivery']),
    'all_new_files_absent':True,
    'scope':'Independent retained-byte/event/source check. This pass verifies faithful execution/evidence, not task success, emergence or a universal incapacity.'}
with (H/'NEUTRAL_RETAINED_AUDIT.json').open('x') as f:
    json.dump(out,f,indent=2)
    f.write('\n')
print(json.dumps(out))
