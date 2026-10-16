# Forecast instrument: scope and input

`tools/forecast_scores.py` accepts JSONL rows with `case_id`, `condition`, `predicted_probability` and integer binary `outcome`. Give all rows a declared event definition and retain its source-grounded label provenance and original actor response outside this table. The tool validates probabilities and labels, groups by condition and reports descriptive Brier loss, event frequency, and reliability/resolution/uncertainty using **exactly equal forecast probabilities** as groups.

Run `python FRR/tools/forecast_scores.py your-forecasts.jsonl`. There is no real actor dataset in this intake. Do not fabricate one from the old pilot, which did not collect these forecasts.

The exact-group decomposition avoids silently treating arbitrary rounded bins as an exact identity. With many unique forecasts, singleton groups make its reliability component a poor guide to population calibration. This tool does not supply confidence intervals, independence, matched costs, correct labels, or a model of subjective confidence. Brier loss alone is not calibration alone.

`python FRR/tools/check_forecast_scores.py` runs software fixtures. One fixture has constant .5 forecasts and another perfect 0/1 forecasts on balanced outcomes: both have zero empirical group reliability error while Brier loss differs (.25 versus 0) through resolution. That is an arithmetic/software check, not observed HPGM or FRR performance. Other checks cover wrong confident forecasts, the decomposition identity and invalid inputs.
