# Carrier attribution with an explicit probe menu

This extension evaluates six prescribed population-probability worlds. No trajectories are sampled: these are exact observation laws, not six independent empirical discoveries. Attribution function receives only probe probabilities; world labels and mechanism coefficients remain in the generator/scorer. Rules use tolerance .01, declared before evaluation without threshold fitting.

Naive attribution calls a field pathway whenever ordinary retain-minus-clear accuracy exceeds .01. Conservative attribution requires all four: effect survives private clearing; cleared/private-cleared reader is at chance; an opposite-payload field transplant reverses the retained effect around chance; disabling the environmental read route removes the effect without leaving a retain-clear discrepancy. Failure means abstain, not proof no field exists.

| Prescribed family | True field route | Naive says field | Conservative says field | Conservative abstains |
|---|---|---|---|---|
| Pure field | yes | yes | yes | no |
| Private only | no | no | no | yes |
| Erase changes private-reader gate | no | yes | no | yes |
| Mixed field/private | yes | yes | yes | no |
| Imperfect private reset plus erase affecting private retention | no | yes | no | yes |
| True field plus off-target erasure damage | yes | yes | no | yes |

Thus the naive rule falsely attributes field mediation in two specified families. The conservative rule makes zero false field attributions within this family, while abstaining even in one world with real field mediation because erasure damage invalidates its clean-probe assumptions. This is a tradeoff visible by family, not a generic robust score.

Pure field private-cleared accuracies are .75 retained, .50 cleared, .25 opposite transplant, and .50 with environmental reader gated. Mixed world ordinary retained accuracy .95 falls to .70 upon clearing field, but private-clear exposes the same .75/.50/.25 environmental signature. Erase-gate artifact ordinary retained is .70 versus .50 cleared; private clearing removes that signature. Reset-leak ordinary .70 vs .55 looks environmental; private-clear retained .58 vs .52 still differs, but chance/signed-transplant checks reject it. Off-target damage gives genuine retained .75 but cleared .40, and environmental gate .50 vs .40, triggering abstention.

## What the probes assume

The designer knows what each gate/reset/transplant acts on. Hidden architecture from the attribution function does not make probe semantics unknown or independently discovered. If transplant also rewrites private state, or read gating jointly gates another carrier, a nonfield mechanism could duplicate the accepted signature. These finite observable laws cannot rule out all alternative causal realizations. Real-world interventions need source and implementation audits, unknown-initial-field controls, uncertainty intervals, sham resets and independently varied substrates.

No same-benchmark calibration occurred, but the family and rules were authored together; this is not a heldout generalization benchmark. Source weights/constants are invented transparent toy parameters. A separate stochastic two-carrier experiment supplies execution agreement for related clean pathways; it does not validate these constructed world classes independently.

Reproduce: `python experiments/attribution-population-laws.py`. Full observable laws, each rule check and family-specific false-attribution/abstention flags are saved in evaluation/results/attribution-population-laws.json. No GitHub write performed by this agent.
