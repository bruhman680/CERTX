# Scoring construction correction

The first blinded scoring packet compressed the C4 receipt to verification of one run, omitting its explicit input/output files and checked-result wording. The original actor packets actually provided those details. Consequently the first scorer flagged them as unsupported on the incomplete scoring record. This is a judge-input construction error, not evidence that the actors fabricated receipt details.

Original packet and review remain unchanged. SCORER_PACKET_REPAIRED.json supplies the full actor-visible receipt to a new fresh scorer blinded to arm mapping and prior judgments. Compare the two reviews without retroactively relabeling the original as correct. This repair is exploratory, not a predeclared final evaluation. Parent review remains unblinded; no independent human adjudication.
