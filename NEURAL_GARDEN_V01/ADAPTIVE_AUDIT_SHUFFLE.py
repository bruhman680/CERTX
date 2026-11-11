"""Independent test: does training do more than shift threshold distribution?

Evaluate learned per-cell thresholds, spatially shuffled learned thresholds,
constant learned mean threshold, and untrained thresholds on matched fresh worlds.
No source Garden equations are modified. This is an exploratory follow-up,
not a preregistered held-out confirmation.
"""
import json
import numpy as np
from pathlib import Path
from ADAPTIVE_threshold import AdaptiveThresholdGarden


def run():
    rows=[]
    for seed in range(1800,1810):
        learner=AdaptiveThresholdGarden(seed=seed,size=16,learning=True)
        before=learner.thresholds.copy()
        for _ in range(1200): learner.step()
        learned=learner.thresholds.copy()
        shuffled=np.random.default_rng(seed+70000).permutation(learned)
        variants={'learned':learned,'shuffled':shuffled,
                  'uniform_mean':np.full_like(learned,learned.mean()),
                  'untrained':before}
        row={'train_seed':seed,'test_seed':seed+9000}
        for label,weights in variants.items():
            g=AdaptiveThresholdGarden(seed=seed+9000,size=16,learning=False,
                                      deterministic=True)
            g.thresholds=weights.copy()
            for _ in range(2000):g.step()
            row[label]=float(g.energy.mean())
        rows.append(row)
    summary={label:float(np.mean([r[label] for r in rows]))
             for label in ('learned','shuffled','uniform_mean','untrained')}
    out={'design':'exploratory posthoc positional-shuffle/uniform-ablation',
         'seeds':list(range(1800,1810)),'train_ticks':1200,
         'test_ticks':2000,'size':16,'summary':summary,'rows':rows}
    Path(__file__).with_name('ADAPTIVE_AUDIT_SHUFFLE.json').write_text(
        json.dumps(out,indent=2)+'\n')
    print(summary)


if __name__=='__main__':run()
