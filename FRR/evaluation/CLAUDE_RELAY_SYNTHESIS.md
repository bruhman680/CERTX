# Claude relay: reproduced contacts and revised boundaries

User supplied a relay dated 2026-10-13 and four Python scripts. All five originals are preserved byte-for-byte with [hashes and missing-source inventory](../lineage/sources/claude-relay-2026-10-15/manifest.json). All four scripts ran unchanged. Three parallel audits examined thermodynamics, finite Life partitions, and source genealogy; a separate wake extension examined reset preparation. Shared code and conceptual ancestry remain explicit. Parallel review is not independent experimental replication.

## What this adds to the earlier exploration

| Contact | What survived execution | Boundary or correction |
|---|---|---|
| Thermodynamics | The ring construction has the declared Boltzmann stationary distribution at zero affinity; driven chains have measurable stationary path irreversibility | Aggregated macro flux can cancel opposing microscopic channels. In general `sigma_lumped <= sigma_boundary <= sigma_full`; equality needs additional conditions |
| Finite Life | All 65,536 successors agree with independent enumeration; forward observable classes and recurrent structure reproduce | The reported mean macro-model defect decreases over the first three tested horizons. Backward class counts can stay fixed while membership changes |
| Wake | Different retained environments affect visible trajectories after the same visible reset | The proposed decay formula is not general; Hankel rank four occurs at both endpoints. Conditioning on a state and intervening to set it require different priors |
| Imperfect probes | A new two-exponential toy verifies exact separation and collision identities | This is not reproduction of missing `erase_gate.py`. Close rates can be identifiable but poorly conditioned; admissible noisy fits are often rare |

Detailed reports: [thermodynamics](RELAY_THERMO_AUDIT.md), [Life](RELAY_LIFE_AUDIT.md), [wake](RELAY_WAKE_AUDIT.md), [Prony](RELAY_PRONY_AUDIT.md). Relevant primary-source relatives and their limits are in [the source weave](../lineage/CLAUDE_RELAY_SOURCE_WEAVE.md).

## Consequential findings

The thermodynamic rebuild advances a genuinely parked task. For the driven six-ring at A=2, full entropy production is .03558049 per uniformized step. The alternating binary observation retains all edges as boundary edges but has zero one-step lumped entropy production: summing channels loses their direction information. The ternary 2-2-2 observation gives a finite KL increment d3 about 1.09958 times the full rate. This reproduces the relay's correction: individual increments need not be bounded by that rate, although cumulative stationary path KL obeys `D_n <= (n-1) sigma`. Physical-time rates require the uniformization conversion. No physical device cost follows from these toy results.

The Life extension supplies a new warning for purported stabilization. Left-window observable-past support has 91 classes at depths 9 through 12, but its membership changes at each depth. States 4791 and 13878 share a class at depth 9 and separate at 10. These backward support partitions are not nested future-prefix partitions, so equal counts do not certify stabilization. Support sets also lack a probability law; they are not automatically reverse predictive states. A node or class remains relative to its observable and temporal question.

The wake extension distinguishes information survival from present readability. Visible distinguishability can return while joint distinguishability never vanished. It also distinguishes naturally finding a system at zero from forcing it to zero: those events generally imply different beliefs about its retained environment. A reader's claimed optimality must be tied to the actual preparation ensemble.

The new Prony contact separates exact identifiability, finite-noise conditioning, and carrier naming. For `c_k=F a^k+P b^k`, the determinant is `F P(a-b)^2`. Distinct nonzero components can be recovered noiselessly up to permutation; at equal rates only their sum is identifiable. Under the declared binomial sampling toy, valid fits fall from 42/50 at gap .8 to 1/50 at gap .05. Conditional error medians alone obscure failure. Algebraic component recovery does not name an environmental or private carrier without a validated intervention.

## Independent noticing

The recurring issue is preservation of a distinction through a chosen read: route identity through flux aggregation, membership through a class count, preparation through a present value, and component identity through a noisy mixture. These are related questions about compression and observation. They are not evidence that the substrates share one physical mechanism or one critical threshold.

This supports keeping FRR's forward predictions and backward checks attached to a specific observable, preparation, and evidence lineage. It does not establish that FRR outperforms ordinary careful reasoning. Runtime 0.2, compact guidance and schema 0.1 remain unchanged; no version promotion is warranted by these tests alone.

## Open, rather than silently closed

- `erase_gate.py`, `boltz_check.py`, and `shadow_echo_v2.py` were referenced but not supplied. Their original numerical claims remain unverified; the new Prony toy cannot substitute for them.
- Finite Life results do not establish infinite-lattice results, stationary reverse-state structure, or semantic memory.
- Broader held-out kernels, independently implemented reset operators, physical mechanisms, and real reasoning-agent transfer remain open.
- The earlier continuation pilot remains an authored small pilot with no general FRR efficacy conclusion.

The next bounded experiment should compare natural conditioning and several explicit reset preparations with calibrated readers, tracking both joint and visible information. A second useful extension would compare past support partitions with probability-weighted reverse states. Neither requires discarding the original exploration or declaring every gap closed.

## Reproduction

With Python and NumPy, run the four audit scripts from any directory: `python FRR/experiments/relay-thermo-audit.py`, `python FRR/experiments/relay-life-audit.py`, `python FRR/experiments/relay_wake_audit.py`, and `python FRR/experiments/relay-prony-audit.py`. They locate their archived sources relative to their own paths and write the linked JSON results. Original scripts are separately retained unchanged. Life exhaustively checks its finite domain; stochastic Prony results use one fixed seed. See [record scope](CLAUDE_RELAY_RECORD_SCOPE.md).
