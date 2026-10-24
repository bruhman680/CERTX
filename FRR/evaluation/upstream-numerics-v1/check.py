from pathlib import Path
import json,hashlib
import numpy as np
import mpmath as mp
D=Path(__file__).resolve().parent;mp.mp.dps=100
j=json.loads((D/'RESULTS.json').read_text());maxerr=0.;shift_residual=mp.mpf(0)
for row in j['hard']:
 z=[mp.mpf(float(v)) for v in row['stored_logits']]
 def ce(*xs):return mp.log(sum(mp.exp(x-xs[0]) for x in xs))
 derivative=np.array([float(mp.diff(ce,tuple(z),tuple(int(i==k) for i in range(3)))) for k in range(3)])
 maxerr=max(maxerr,float(np.max(abs(derivative-row['reference_gradient']))))
 shifted=[v+mp.mpf(100000) for v in z]
 shift_residual=max(shift_residual,abs(ce(*z)-ce(*shifted)))
checks={'highprecision_differentiation_matches_reference':maxerr<1e-30,'real_arithmetic_common_shift_invariance':shift_residual<mp.mpf('1e-90'),'all_declared_checks_pass':all(j['checks'].values()),'source_binding':hashlib.sha256((D/'run.py').read_bytes()).hexdigest()==j['source_sha256'],'protocol_binding':hashlib.sha256((D/'PROTOCOL.md').read_bytes()).hexdigest()==j['protocol_sha256'],'empty_stderr':not (D/'RUN.stderr.txt').read_text()}
out={'scope':'Separate highprecision numerical differentiation and artifact checks; not framework or training replication','max_derivative_reference_error':maxerr,'real_arithmetic_shift_residual':str(shift_residual),'checks':checks}
(D/'CHECKS.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
