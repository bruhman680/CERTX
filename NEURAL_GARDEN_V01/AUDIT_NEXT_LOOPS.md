# Independent methodology audit: longitudinal Neural Garden

**Scope:** Next evidence-driven loops for `LIVING_GARDEN.py`, the archived matched-policy sweeps, and future intervention studies. This is a simulator methodology audit, not a certification of autonomous evolution or intelligence.

## Priority intervention safety finding — corrected

The initial `intervene` operation preserved only a *visible* pre-intervention snapshot (`resource`, `energy`, `activity`, metrics) before replacing the in-place checkpoint. That snapshot omitted hidden neural state, distinct per-cell weights, and both RNG streams, so it **was not sufficient to undo an intervention exactly**. Calling interventions reversible without a prior full-state fork would have been too strong.

**Fix applied:** `LIVING_GARDEN.py` now writes a separate **full model checkpoint** and SHA-256/fingerprint metadata under `backups/interventions/` *before* applying any intervention. It validates the archived state against the original in-memory fingerprint. New `restore-fork --backup BASENAME --destination DIR` creates a paused exact-state branch from that archival checkpoint without erasing the source's subsequent history.

**Verification:** On an independent seed-37 size-4 temporary world, advanced 10 ticks, paused, applied 0.5 resource intervention, then restored the pre-intervention checkpoint into two new forks. Both forks had identical full-state fingerprints at tick 10, and independently advancing each for another 17 ticks produced identical fingerprints at tick 27. Restoring left the source (post-intervention) world intact. A separate status inspection confirmed the canonical size-16, seed-37 Living Garden remained paused at tick 100 with fingerprint `477bea9e3a7752ee0008910c158444f47a1779d15db300fee128ee4a2f97cfcb`. Python compilation passed.

The new backup metadata supports forensic audit, but it must be copied with the main world checkpoint to persistent private storage. Pickle is *trusted local input only*; loading externally supplied pickle is unsafe. Exact rewind is implemented as **fork creation**, not destructive in-place history rewrite.

## Other methodological distinctions

1. **Persistent object vs. scientifically controlled world:** One long-lived history is the observational subject, not an independent causal comparison. When it exhibits a surprising event, fork exact-state twins at the same tick with a predeclared intervention in one and unchanged control in the other. Retain both histories; compare outcomes and re-run on independently initialized worlds before generalizing.
2. **Stored energy vs. raw energy budget:** Clipping to `[0,1]` can hide both deficit at the floor and surplus at the ceiling. Report raw pre-clipping drift and floor/ceiling occupation alongside mean energy. A flat low-energy tail is not viable equilibrium.
3. **Resource recovery vs. energy recovery:** Prior shocks let resource rebound rapidly while cell energy remained depleted. These have different time constants. Future intervention reports need recovery-to-baseline times for *both* fields and integrated energy loss.
4. **Behavioral learning vs. prediction:** The current v0.1 neural predictor does not observe the **current sampled action** when making resource predictions. Its on-policy MSE is an action-marginal metric that cannot establish action-conditioned causal understanding. A learned policy's ecological score is a separate outcome.
5. **Individual simulation cells vs. replication units:** All cells share a coupled resource field and neighborhood effects. Statistical replication units are independent seeded worlds or independent controlled forks from independently seeded ancestors—not 256 cells or individual time points.
6. **Independent mutations vs. selection:** The evolutionary pilot supplies inheritance but has no demonstrated mutational fitness advantage over clones. Do not infer adaptive evolution from lineage depth or changing diversity alone.
7. **Event-log crash consistency:** `LIVING_GARDEN.advance()` appends per-tick JSONL records before periodically saving its checkpoint; after abrupt `SIGKILL` or machine failure, metrics may contain ticks newer than the last saved state, then repeated tick labels upon resume. The base CLI has a `checkpoint_recovery` marker; the Living CLI presently does **not** automatically reconcile such duplicate histories. Graceful pause/SIGTERM is supported. Interpret metrics as an append-only *observational record* with possible recovery episodes; use checkpoint tick and full-state fingerprint as authoritative state, not the largest logged tick alone.
8. **Archive identity and reproducibility:** Include run source hash, Python/NumPy versions, named interventions, RNG state in full checkpoints, source–fork parent fingerprint, reason and tick. A user-adjusted world law belongs to a *new labeled model* or clearly annotated intervention, not an untraceable edit of `garden.py`.

## Recommended living-world protocol

**Observe:** Progress the canonical Garden in recoverable batches, e.g. 100 ticks with a full checkpoint and summary at the boundary. Track short-term covariance, raw energy drift, energy floor, spatial heterogeneity, population proxies and latent neural changes, not just colors.

**Orient:** If raw budget becomes persistently negative, seek an explanatory residual: Are cells harvesting scarce sites? Is resource abundant but action timing poor? Does prediction MSE improve while energy deteriorates? Refrain from changing laws just to lift energy.

**Fork:** Keep the exact-state control and make the smallest explicit change in a sibling branch, preferably one variable at a time. Separate environmental intervention, reward function change, and genetic/reproductive extension.

**Test:** Run control/treatment for identical future horizons, compare difference trajectories (not single endpoints), then repeat on fresh ancestors to test generalization. Preserve negative and mixed results.

**Integrate:** Promote a mechanism into the canonical world *only when evidence supports it* and the change is explicitly logged; never silently replace the history. Save branch checkpoints privately and publish code, per-run metrics, and provenance on the dedicated GitHub research branch.

This protocol makes a **single persistent world** the primary object of inquiry while keeping causal controls rigorous and recoverable.
