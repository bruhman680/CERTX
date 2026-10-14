# Imperfect reset: carrier versus access

## Question and result

Can a fresh reader recover a written bit from an environment despite imperfect private reset, and can the observed effect be assigned to that environment?

The stochastic experiment introduces two separate carriers, independently written at probability .8, separate .1 channel/measurement noise, and private-reset leakage 0, .05, or .5. Field retention and private retention are independently varied. It runs 72 matched conditions with 200,000 samples per condition, one seeded set of common random draws across arms. These are correlated intervention arms in one constructed world, not 72 independent replications. Distinct causal-role draws avoid the earlier noisy-echo RNG bug.

At equal reader mixture and no private leakage, field retention gives .628565 accuracy versus .500615 after field clearing: paired effect .12795, paired Monte Carlo SE .001078, analytic effect .128. Both nominally cleared with .5 private leakage gives .5642. No-write and blind controls are at chance. All conditions agree with the specified analytic law within six Monte Carlo SE; this is a numerical consistency check, not scientific acceptance of a general memory hypothesis.

See IMPERFECT_RESET_CARRIERS_REPORT.md and experiments/imperfect-reset-carriers.py.

## The rival that defeats a simple erase test

An exact counterexample compares an environmental carrier to a private carrier whose reader gate is disabled by the erase action. Both produce exactly the same conditional response laws under keep and clear. Infinite samples from those two conditions cannot tell the models apart. Selective field swapping, private clearing, and restoring the access gate discriminate them, provided each operation actually has the stipulated selective effect.

See experiments/erase_artifact_counterexample.py and results/erase-artifact-counterexample.json (18 exact model/intervention cells). This is an explicit observational-equivalence counterexample for a restricted intervention family, not a statement that memory location can never be identified.

## What changed in our inquiry

A reset is an intervention with a success rate and possible side effects. A missing response can mean erased storage, blocked access, reader alteration, or noise. A successful response can mean retained field, private leakage, correlated initial conditions, or another unblocked path.

A changed environmental state can alter the focal system's effective transitions while the full coupled transition operator stays fixed. That is already useful persistence, but does not establish emergence of a new law. If claiming rule evolution, specify the rule-bearing variable and a larger coupled model; test it separately from stored payload.

Role-separated review found no implementation error, but shares code/context lineage. Source assumptions and access depth are tracked in ../lineage/IMPERFECT_RESET_SOURCE_SCOUT.md and ../lineage/IMPERFECT_RESET_ADVERSARIAL_DESIGN.md. No real AI reasoning benefit, semantic growth, or permanent substrate claim is tested.

## Next discriminating contact

Use unknown initial fields, calibrated but imperfect reset operators, and a reader whose channel routing can change under erase. Ask whether a proposed diagnostic recovers the correct carrier across held-out worlds, including erase-gate artifacts. Preserve uncertainty where the available interventions cannot distinguish the rivals. These toy tests should precede any claim that a swarm can autonomously infer memory location.

## Attribution challenge executed

A final six-family exact-law test gives an attribution function observation probabilities only, with tolerance .01 declared before evaluation. A naive keep-minus-clear rule falsely attributes environmental persistence in the erase-dependent private-response and reset-leakage families. A conservative conjunction checks survival after private clearing, a chance cleared baseline, reversal after opposite-payload transfer, and removal of contrast when environmental reader access is blocked. It accepts pure field and mixed carriers; it does not endorse private-only, artifact, leakage, or real field plus off-target erase damage.

Not endorsing the last case is deliberate abstention despite a genuine field pathway, not proof that the field is absent. The fixed .5 baseline, selective probe semantics, and symmetric payload response are assumptions of the authored family. No held-out benchmark or mechanism-free diagnostic was demonstrated. A private spoof of the same observation laws could still pass. See ATTRIBUTION_POPULATION_LAWS_REPORT.md and experiments/attribution-population-laws.py. No false attribution in six chosen families is a boundary result, not universal validation.
