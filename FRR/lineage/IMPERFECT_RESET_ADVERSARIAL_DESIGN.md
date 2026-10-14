# Imperfect reset: adversarial carrier identification

Date: 2026-10-13 (user-facing date). Status: design and independent code review; no empirical experiment in this note.

## What the clean toy establishes

`wake_reset_transfer.py` executes a specified finite-state law. Actor y is independently initialized and environmental e is transferred by construction. Its normalized word laws, no-write condition, and analytic first-read contrast are useful verification. Its writer-kept/field-cleared branch equals clearing in code, because no writer-to-reader channel exists. The same-history field copy proves deterministic sufficiency of this state representation, not unique provenance or physical transplantation. These limits are already acknowledged by its scope string.

Calling an independently owned variable environment provides an operational partition, not a new ontology. A full Markov state can be enlarged to include agent and environment. The focal trajectory alone may be non-Markovian after that enlargement is projected away. Field-caused changes in effective focal transition probabilities need not change the full coupled transition operator. A genuinely changing operator requires separate parameters or structural state whose change is measured; a state-dependent read law already accounts for its field dependence.

## An experiment allowed to defeat the desired explanation

Prepare writer payload B in {-1,+1}; hold the reader start fixed. Let the environmental carrier E and leaked actor carrier A be independently manipulable, with E and A taking values in {-1,+1}. Use a declared reader:

P(Y=1 | E,A,Z) = 0.5 + c_E E + c_A A + c_Z Z,

where |c_E|+|c_A|+|c_Z| <= 0.5 and Z is an erasure-induced nuisance. Choose bounded values without clipping; clipping would introduce another nonlinear mechanism. For example c_E=.15, c_A=.10, c_Z=.05.

Cross environment retain/clear with actor leak retain/clear. Cleared carriers are independently fair, not set to a treatment-correlated default. Add sham and real erasure, blinded treatment IDs, and opposite-payload transplants. Evaluate the contrast between payload preparations as well as overall reader rate. In the clean additive construction, payload contrasts identify sums of active coefficients, and the crossed interventions resolve the two candidate carriers. That is an identification result conditional on the additive response and correct interventions.

Independently vary c_E and c_A across held-out worlds including c_E=0. A method that always announces environmental memory must fail in actor-only worlds. Include c_E*c_A interaction worlds, where clearing one carrier changes use of the other: simple subtraction no longer isolates contributions. Report such failures instead of forcing an additive diagnosis.

## Four adversarial rivals

1. **Reset leakage.** Let an apparently reset actor keep a cached payload, initialization seed, or trajectory summary. Clear E while preserving A, then clear A while preserving E. Require a code path that really carries A; a placeholder variable disconnected from the reader cannot test leakage. Reset verification should include object reconstruction and serialized state audit, not only an empty visible history.
2. **Erasure side effects.** Clearing E can change Z, reader sensitivity c_E, or the read operator itself. Real erase with collateral damage can suppress a retained payload effect without proving the payload was removed. A payload-preserving sham that reproduces collateral change, plus restore-after-erase, separates these mechanisms. The sham is informative only if its side effects actually match the relevant erase effects. No universal matching can be assumed.
3. **Shared RNG.** Common random numbers across alternative read branches are legitimate coupling of potential outcomes, preserving marginals. Reusing a draw for emission and a supposedly independent field update changes the joint kernel. Keep separate event streams keyed by mechanism and time, audit conditional transition frequencies, and randomize payload allocation independently. Also reset RNG state separately from actor state: a retained RNG can itself convey information or create paired replay artifacts.
4. **Unknown starting field.** Let E0 already correlate with B. A donor-conditioned final field can then discriminate B even with writing disabled. Include no-write preparations from the same randomized E0 distribution, measure E0 when noninvasive access is available, and compare action-induced change conditional on E0. Opposite transplantation identifies the present carrier response; it does not uniquely reconstruct the history that created it. If E0 is unavailable and allocation is confounded, the wake-origin claim remains unresolved.

## Persistence and rule change

Measure first-read contrast after delay d, and finite future-block TV with an explicit observation budget. Under the flip kernel, contrast decays geometrically and can fall below tolerance without exact erasure. Long mixing time is not an invariant barrier. Positive transition probabilities do not imply quick escape on the observation window. A field becoming inaccessible to the reader is different from disappearing from the full state.

Test effective rule change by holding the focal starting state and read noise fixed while exchanging E. Test full-operator change by holding the full coupled state fixed while exchanging an explicit rule parameter, such as read sensitivity or graph adjacency. Those are different interventions. Structural rule parameters can themselves be modeled as dynamical state at a larger scale; declare that scale rather than inferring universal law from the vocabulary.

## Source relation and limits

Primary source access and genealogy are recorded in `WAKE_RESET_SCOUT_NEW.md`. Reid et al. 2012 provides a manipulated external slime trace with blank-versus-coated agar and avoidance tests; it does not provide all four factorial controls above. Beckers–Halpern 2019 motivates declared intervention maps and distinguishes distribution-specific agreement from stronger abstractions. These supply experimental and formal relatives, not independent confirmations of this engineered additive model.

Next contact: run carrier-identification procedures blindly on clean, leakage-only, erase-side-effect, and initial-field-confounded worlds. The success criterion is correct refusal or attribution across those worlds, not merely reproducing the retained-field contrast in the world designed to have one.

## Independent review of new scripts

Reviewed `experiments/imperfect-reset-carriers.py` directly after its creation. The analytic expectation .5+.256*wrote*[fieldshare*retainfield+(1-fieldshare)*effectiveprivate_retention] correctly combines 80% write success, retention flip probability .1, and measurement flip probability .1. The matched-field contrast with zero private leakage and .5 field share is .128. Distinct arrays separate causal roles; sharing those arrays across intervention arms is legitimate paired variance reduction. The paired standard error is calculated from per-trial differences. No implementation error found on inspection. This is one seeded, constructed world with 72 correlated arms, not 72 independent replications. Initial-carrier independence, fair erasure, and reader mixture are stipulated; no-write null will not diagnose unknown initial correlation absent from the model.

Reviewed `experiments/erase_artifact_counterexample.py` directly. Its environment model and erase-gate-artifact model have exactly equal conditional response laws under keep/clear. Thus unlimited observations from those two interventions cannot discriminate them. Clear-private, opposite field, fresh-private, and gate-restore interventions separate them only because those operators are stipulated selective. The numerical code correctly implements the intended counterexample. Zero signed carrier denotes an average over a fair mixture in this linear response, not a third physical bit value. The artifact is reader-gate change rather than evidence that the environmental payload was erased. This is a mathematical non-identification example, not a frequency estimate of how often such artifacts arise in real agents.

No new primary-source empirical claims were added during this review. The earlier source-access limitations remain unchanged.

## Population-law attribution review

Independently inspected `experiments/attribution-population-laws.py`: no logical implementation flaw found. The environmental reader gate affects only the environmental path, as declared. Its `erase_gate_artifact` family encodes erasure-dependent private response retention, whereas the earlier counterexample explicitly changed a reader gate; the two are observational relatives with distinct implementations. A more descriptive family name would prevent conflation.

The classifier receives only seven response probabilities, but also embeds a known chance baseline .5, opposite-payload symmetry, a fixed tolerance, and assumed intervention semantics. It therefore does not infer independence or selectivity from unconstrained data. Passing all four checks is a conservative sufficient rule in these six designed families, not a generic guarantee. Abstention means the sufficient pattern was not established: it is not a negative diagnosis that the field is absent. In particular off-target damage has a true environmental pathway and deliberately causes abstention. Pure-private worlds also abstain, even when their observations offer stronger negative information than the output label reports. Mixed worlds pass after the stipulated perfect private clearing. These distinctions should be preserved in the results summary.
