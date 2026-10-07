# Experiments 05: archive/read/deposition separation

Executed locally 2026-10-07. Isolated executable improvement: `outputs/experiments-05/reset_controls.py`; results `controls.json`; source hashes `provenance.sha256`. Original engine remains byte-identical in an isolated copy. No agents, downloads, remote writes, or secret inspection. First execution completed assertions but failed JSON serialization of NumPy integer; scalar serialization was corrected and full execution passed.

## What the archive can reconstitute

Source tracing finds only `_die` adds entries to `soil_field`. It simultaneously appends a genotype to `soil`. Neither `compost`, `soil_richness`, nor `inject_entropy` reconstructs field values from archive records. Archive entries contain genotypes, not deposition fitness/time, so they do not encode enough to invert decaying wake deposits. Compost reads three archive donors and creates an offspring; a subsequent death can deposit a new value. This is an indirect archive→candidate→death→field path, not archive restoration of the original field.

Executed witness: after clearing field and tripling checkpoint archive to cross the compost richness gate, compost created genotype 100010 with fitness .5239476516 and wake remained exactly zero. Killing that offspring deposited .04191581213 (=.08 times its current fitness). Archive-only feedback can thus start new wake, but through an intervening candidate/death.

## Reset controls actually executed

Common deep-copied seed99 checkpoint at step120, initial K=2.330461, archive27. All four controls initially clear wake. Subclasses preserve original logic except labelled interventions: `NoDeposit._die` keeps extinction/archive append but omits field deposition; `NoDepositNoRichness` additionally returns zero richness. These are diagnostic changes to the isolated copy's runtime class, not proposed replacement engine behavior. No scoring-read override was implemented; with field identically zero, scoring wake is already zero.

| condition | t1 wake | t100 wake | t100 archive | t100 K | t100 richness |
|---|---:|---:|---:|---:|---:|
| one-shot reset | .038846 | 1.172244 | 71 | 0 | 1 |
| no deposition | 0 | 0 | 71 | 0 | .8875 |
| no deposition + no richness | 0 | 0 | 69 | 2.637700 | 0 |
| no deposition + initially empty archive | 0 | 0 | 48 | 1.025998 | .6 |

Every no-deposition endpoint was asserted to have an empty field. Thus field remains absent despite archived genotypes, compost possibility and continued engine dynamics. Archive-mediated control alone can drive K to its lower bound; the shared K=0 endpoint is not evidence of equal field state. Clearing archive once does not prevent new archive deposits. No-deposition/no-richness preserves an archive but disables its richness-driven controller influence, dormant waking, entropy gate and compost gate together; this is a bundled path control, not identification of any single controller mechanism.

## Controller and measurement paths

Richness is zero with empty archive, otherwise min(1, field mass/3+archive length/80). Its reads drive the K controller, compost emergence (.45 with at least three archived entries), dormant waking (.5), and entropy injection (.6). The latter redraws NK tables and mutates some candidates; conditional branches change RNG consumption. Therefore long-horizon differences after reset include controller/table/RNG-mediated effects.

Snapshot is an aggregate observation, not a restart state: it omits genomes/statuses/fitness histories, archive, field keys, NK table, RNG, mutation parameters and phase/age. Executed two copies with equal snapshots but different RNG states (one extra RNG draw). This witnesses lost transition-state information; no claim of measured continuation divergence for that pair is made.

At reset t0 cached snapshot mean fitness=.5426529 while recomputed mean=.5310337. At t100 no-deposition cached=.555358 versus recomputed=.536983 even though field remains zero: entropy table redraw can leave caches stale for candidates not rescored by `inject_entropy`. Snapshot mismatch therefore cannot be attributed uniquely to wake deletion. Logging table entries and freshly recomputed scores is the implemented reversible measurement improvement.

## Scope, rival, surviving relation

This is one deterministic seeded execution of a synthetic engine and controlled source interventions, not independent physical evidence or a prevalence estimate. Archive/field storage are distinct but naturally co-written and functionally coupled. The surviving relation: persistent archive can change future opportunities through programmed richness/control and recombination even when direct field scoring is disabled; surviving numerical field entries can separately affect scoring.

Serious rival to a general environmental-memory interpretation is explicit additive scoring plus hand-coded controller thresholds and conditional RNG draws. The experiment locates carriers and paths in code, not a universal mechanism or uniquely recoverable historical semantics. Repeated independently predeclared checkpoint seeds and single-path controller controls are recommended, not executed. Preserve the open question of which retained carrier keeps a later possibility available; no cube is needed for these path witnesses.

Sources inspected: NOW.md; FRR v0.5 compact seed and relevant wake/reset passages; recovered engine, wake probe, transplant, RECOVERY_NOTE; CERTX continuation handoff and recovered history; experiments03/04 reports. Prior reports orient shared-source comparisons and are not independent replication. Current NOW supersedes historical intake pause.
