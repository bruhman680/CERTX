"""Score labeled binary forecasts. Descriptive software, not a calibration test.

CLI: python forecast_scores.py forecasts.jsonl
Each row: case_id, condition, predicted_probability, outcome (integer 0 or 1).
Keep raw actor responses and label provenance separately; this tool cannot judge them.
"""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


def score_forecasts(probabilities, outcomes):
    if len(probabilities) != len(outcomes) or not probabilities:
        raise ValueError('Need nonempty, equally sized forecasts and labels')
    grouped = defaultdict(list)
    pairs = []
    for p, outcome in zip(probabilities, outcomes):
        if type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1:
            raise ValueError('Forecast probability must be finite and within [0,1]')
        if type(outcome) is not int or outcome not in (0, 1):
            raise ValueError('Observed outcome must be integer 0 or 1')
        p = float(p)
        grouped[p].append(outcome)
        pairs.append((p, outcome))
    n = len(pairs)
    mean_outcome = sum(outcomes) / n
    brier = sum((p-y)**2 for p, y in pairs) / n
    uncertainty = mean_outcome * (1 - mean_outcome)
    reliability = resolution = 0.
    groups = []
    for p, values in sorted(grouped.items()):
        rate = sum(values) / len(values)
        weight = len(values) / n
        reliability += weight * (p-rate)**2
        resolution += weight * (rate-mean_outcome)**2
        groups.append(dict(probability=p, count=len(values), observed_rate=rate))
    return dict(n=n, observed_event_rate=mean_outcome, brier_loss=brier,
                empirical_reliability_exact_groups=reliability,
                empirical_resolution_exact_groups=resolution,
                empirical_uncertainty=uncertainty,
                decomposition_error=brier-(reliability-resolution+uncertainty),
                exact_probability_groups=groups,
                scope='In-sample descriptive decomposition, not population calibration or confidence intervals. Singleton groups are especially uninformative about calibration. No rounding or binning of forecasts applied.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    if not rows:
        raise ValueError('No forecast records')
    conditions = defaultdict(list)
    for row in rows:
        if not isinstance(row.get('case_id'), str) or not row['case_id']:
            raise ValueError('Missing case_id')
        if not isinstance(row.get('condition'), str) or not row['condition']:
            raise ValueError('Missing condition')
        conditions[row['condition']].append(row)
    output = {name: score_forecasts([r['predicted_probability'] for r in subset],
                                    [r['outcome'] for r in subset])
              for name, subset in conditions.items()}
    print(json.dumps(dict(scorer_version='0.1', input=str(args.input), by_condition=output), indent=2))


if __name__ == '__main__':
    main()
