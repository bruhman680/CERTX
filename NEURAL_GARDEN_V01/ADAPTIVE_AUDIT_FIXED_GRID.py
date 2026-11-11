"""Posthoc fixed-threshold horizon control prompted by adaptive shuffle audit.

Threshold candidates were selected after inspecting exploratory results.
Report only as candidate screening, never independent selection/validation.
"""
import json
from pathlib import Path
import numpy as np
from threshold_policy import ThresholdGarden


def main():
    seeds=list(range(10800,10820))
    thresholds=[.45,.475,.49,.5,.51,.525,.55]
    rows=[]
    for seed in seeds:
        row={'seed':seed}
        for threshold in thresholds:
            g=ThresholdGarden(seed=seed,size=16,threshold=threshold)
            for _ in range(2000):g.step()
            row[str(threshold)]=float(g.energy.mean())
        rows.append(row)
    summary={str(t):float(np.mean([r[str(t)] for r in rows])) for t in thresholds}
    out={'design':'posthoc fixed threshold screening at 2000 ticks',
         'seeds':seeds,'grid_size':16,'ticks':2000,'thresholds':thresholds,
         'summary':summary,'rows':rows}
    Path(__file__).with_name('ADAPTIVE_AUDIT_FIXED_GRID.json').write_text(
        json.dumps(out,indent=2)+'\n')
    print(summary)


if __name__=='__main__':main()
