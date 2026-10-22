# Cycle1: readable does not mean representative

[Protocol](PROTOCOL.md) precedes [run.py](run.py). This exact-population observation-model contact follows the previous run's open witness-validity boundary. It is a new authored model, not a physical-memory or actual-agent experiment. No source search, random sampling, provider calls or threshold tuning was needed. The first execution took about.012seconds and passed eight declared checks. Original execution streams are retained; no failed runs or discarded cases occurred.

## Construction

Survival S is binary, with probability v. Readability G depends on survival through a1=P(G1|S1) and a0=P(G1|S0). A zero-coded observation returns S*G, conflating unreadable with readable absent state. The ternary observation returns1,0,or missing. Its probabilities are

`p1=v*a1; p0=(1-v)*a0; pmissing=1-p1-p0`.

A216-cell grid varies v,a1,a0 over0,.2,.4,.6,.8,1. It includes36 MCAR cells(a1=a0), of which30 have positive readability and six are wholly unreadable. No repeated-same-state temporal process is modeled; results concern one-shot population laws, not arbitrary memory trajectories.

## What changes when missingness becomes visible

Two selected worlds have the same zero-coded readout distribution: survival.2 with full access, versus survival1 with access.2. Both return1 with probability.2. Ternary observations distinguish these examples: [.2,.8,0] versus[.2,0,.8]. Explicit missingness therefore recovers an observation distinction that zero coding removes here.

But visible missingness does not guarantee survival identification. The selected state-dependent gates

- v=.2,a1=1,a0=.25;
- v=.8,a1=.25,a0=1

both produce ternary distribution[.2,.2,.6]. Reading only the available outputs gives survival estimate.5, wrong for either latent survival. Conditional-on-readable estimates on the grid differ from true survival by up to.8. This is a selection effect in the authored model, not an observed real-system bias.

Without gate-selection assumptions, the population identified set is

`v in [p1,1-p0]`.

The lower bound follows because readable survivors cannot exceed all survivors; the upper bound because readable nonsurvivors cannot exceed all nonsurvivors. Every point in that interval is attainable by a1=p1/v,a0=p0/(1-v), with valid endpoint conventions. Endpoint/midpoint constructions agree numerically, and the separate checker rejects all tested just-outside points. In the paired example the set is[.2,.8]. It is an identified set from exact population observations, not a finite-sample confidence interval.

Under the explicit MCAR assumption a1=a0>0, the conditional-on-readable value p1/(p1+p0) recovers v. If readability is zero, even MCAR leaves[0,1]. The assumption does work; the observation alone does not authenticate it.

## Restoration needs its own causal contract

Two explicit4x4 operators force G=1. The preserving operator leaves S unchanged and reveals v. The rewriting operator redraws S with survival.6 and therefore reveals.6 regardless of its prior value. Successful reading after restoration cannot by itself establish that content survived the operation. A direct external witness can distinguish survival probabilities only because direct, accurate access is stipulated; this study does not supply such an instrument in real agents or hardware.

[RESULTS.json](RESULTS.json) retains every joint law, interval construction, restored readout and selected example. [CHECKS.json](CHECKS.json) separately checks scalar observation constraints, outside-set infeasibility, protocol binding and execution results. Maximum attainability error is2.23e-16. Eight model checks and five scalar/artifact checks pass. The scalar check uses the same assumptions; it is not independent empirical validation.

## Useful next consequence

Treat absent witness output as missing rather than erased, then ask whether the readable subset is selected in a consequential way. When access-selection semantics are unknown, carry a set of plausible survival values rather than a forced point. A next decision may be stable across that set, even if the latent state is not identified; another may require additional access or evidence. Restoration must be checked for side effects before it is used to infer prior persistence.

No universal preference for ternary formats, novel memory carrier, practical framework advantage or actual-agent benefit is established. Unknown response errors, false missingness flags, restoration costs and state-dependent temporal transitions remain open. No broad queue or core-runtime change follows.
