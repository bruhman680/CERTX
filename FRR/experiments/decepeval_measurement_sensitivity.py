"""Arithmetic reconstruction and hypothetical judge-error sensitivity, no model rerun."""
import json, math
from pathlib import Path

def observed(true_rate,sensitivity,false_positive):
    return sensitivity*true_rate+false_positive*(1-true_rate)

def run():
    # Manually transcribed displayed Table3 neutral/induced pairs, rounded by source.
    cells=[[19.10,78.40,7.20,43.50,50.50,98.50],[23.75,80.63,4.27,21.86,21.72,99.45],
    [4.50,45.50,11.06,27.34,5.50,84.70],[2.20,36.80,1.60,31.70,1.50,47.81],
    [7.09,66.55,13.20,28.00,54.70,97.10],[11.09,36.21,22.20,68.10,53.12,78.59],
    [9.27,36.04,20.37,64.35,58.29,83.33],[6,54.80,4.86,40.05,3.09,99.64],
    [4.91,27.09,2.18,10.65,33.10,94]]
    changes=[r[j+1]-r[j] for r in cells for j in (0,2,4)]
    means=[sum(r[j] for r in cells)/9 for j in (1,3,5)]
    assert abs(sum(changes)/27-41.64)<.01
    # Intentionally hypothetical, not fitted to paper/human judgments.
    neutral=observed(.1,.95,.01); induced=observed(.1,.95,.25)
    assert abs(induced-neutral-.216)<1e-12
    # Conditional calculation: 97/100 independent agreement observations, not accuracy.
    n=100;p=.97;z=1.959963984540054;den=1+z*z/n
    center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return {'scope':'No provider calls, task execution, judge recreation, human rating validation, or raw replication. Table manually transcribed. Error scenario hypothetical; not a claim actual bias explains findings. Agreement interval conditional on 100 independent Bernoulli observations, not correction for seed/clustering or guarantee of construct validity.',
    'table3':{'mean_change_percentage_points':sum(changes)/27,'cells_exceeding25points':sum(x>25 for x in changes),'cells':27,'mean_induced_tool_coding_long_percent':means},
    'hypothetical_equal_true_rate':{'true_rate_both':.1,'judge_sensitivity_both':.95,'false_positive_neutral':.01,'false_positive_induced':.25,'observed_neutral':neutral,'observed_induced':induced,'observed_change':induced-neutral},
    'conditional_97_of_100_agreement_wilson95':[center-half,center+half]}
if __name__=='__main__':
    d=run();p=Path(__file__).resolve().parents[1]/'evaluation/results/decepeval-measurement-sensitivity.json';p.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
