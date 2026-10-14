"""Isolate the shared-random-number bug conditional on a fixed joint state."""
import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(41); N=1000000
u=rng.random(N);v=rng.random(N);w=rng.random(N)
y2=u<.15
orig=np.where(v>=.2,False,u<.5);fixed=np.where(v>=.2,False,w<.5)
res={'conditional_initial_state':{'e':0,'y':0,'delta':.2},'samples':N,'target_joint_y2_1_eprime_1':.015,'original_joint':float(np.mean(y2&orig)),'corrected_joint':float(np.mean(y2&fixed)),'original_analytic_joint':.03}
assert abs(res['corrected_joint']-.015)<.0005
assert abs(res['original_joint']-.03)<.0005
out=Path(__file__).resolve().parents[1]/'evaluation/results/sweep-audit-rng-joint.json'
out.write_text(json.dumps(res,indent=2)+'\n');print(res)
