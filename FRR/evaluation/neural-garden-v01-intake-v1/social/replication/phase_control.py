"""Exploratory per-cell lag recurrence, not a new trained agent or causal proof."""
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(H/'sources'))
import numpy as np
import SOC_MACRO_TRANSFER_probe as transfer

test,_=transfer.observe(transfer.TEST,'fixed_50')
metrics=[]
for lag in [1,2,3,4,5,6]:
    matches=test[:,lag:,:]==test[:,:-lag,:]
    late=test[:,220+lag:,:]==test[:,220:-lag,:]
    metrics.append({'lag':lag,'all_time_category_match':float(matches.mean()),
                    'late_category_match':float(late.mean())})
payload={'source_commit':'3204c81ebc6922d66b0ae2623ee83d629f11f3b8',
    'test_seeds':transfer.TEST,'policy':'fixed_50','metrics':metrics,
    'scope':'Post-read exploratory recurrence diagnostic on the same eight heldout worlds, not independent confirmation or a proof of exact asymptotic periodicity. Separate global-clock control in RESULT.json does not infer per-cell phase.'}
with (H/'replication/PHASE_CONTROL.json').open('x') as f:json.dump(payload,f,indent=2);f.write('\n')
print(json.dumps(payload))
