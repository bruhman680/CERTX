"""Exploratory, paired train-vs-untrained-vs-fixed policy probe.

No hyperparameter search is performed here. Learned thresholds are evaluated on
fresh matched seeds, not on the training world's own resource trajectories.
"""
import json,sys,platform,hashlib
from pathlib import Path
import numpy as np
from ADAPTIVE_threshold import AdaptiveThresholdGarden
from threshold_policy import ThresholdGarden


def evaluate(size=12, train_steps=900, test_steps=1000, seeds=range(900,910),
             output_name='ADAPTIVE_probe_results.json', trace_decay=.97, lr=.001):
    rows=[]
    for seed in seeds:
        learner=AdaptiveThresholdGarden(seed=seed,size=size,learning=True,
                                        trace_decay=trace_decay,lr=lr)
        thresholds_before=learner.thresholds.copy()
        for _ in range(train_steps): learner.step()
        learned_energy,learned_resource=learner.deterministic_fresh_test(seed+5000,test_steps)
        original=AdaptiveThresholdGarden(seed=seed+5000,size=size,learning=False,deterministic=True)
        original.thresholds=thresholds_before
        fixed=ThresholdGarden(seed=seed+5000,size=size,threshold=.55)
        for _ in range(test_steps): original.step();fixed.step()
        rows.append({"train_seed":seed,"test_seed":seed+5000,
                     "learned_energy":learned_energy,"learned_resource":learned_resource,
                     "untrained_energy":float(original.energy.mean()),
                     "fixed_energy":float(fixed.energy.mean()),
                     "learned_threshold":float(learner.thresholds.mean()),
                     "initial_threshold":float(thresholds_before.mean()),
                     "mean_abs_shift":float(np.mean(np.abs(learner.thresholds-thresholds_before))),
                     "trained_energy":float(learner.energy.mean()),
                     "trained_resource":float(learner.resource.mean())})
    p=Path(__file__).resolve().parent
    sources={f:hashlib.sha256((p/f).read_bytes()).hexdigest()
             for f in ['garden.py','ADAPTIVE_threshold.py','ADAPTIVE_probe.py','threshold_policy.py']}
    summary={k:float(np.mean([r[k] for r in rows])) for k in rows[0] if k not in ('train_seed','test_seed')}
    result={"design":"exploratory, frozen learning settings chosen by agent; no test-based tuning",
            "size":size,"training_ticks":train_steps,"fresh_test_ticks":test_steps,
            "trace_decay":trace_decay,
            "lr":lr,
            "seeds":list(seeds),"python":platform.python_version(),"numpy":np.__version__,
            "source_sha256":sources,"summary":summary,"rows":rows}
    (p/output_name).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return result


if __name__=='__main__':evaluate()
