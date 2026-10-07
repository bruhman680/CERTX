# Fixed recipient evaluation: garden transplant

Worker experiments-06, 2026-10-07. Implemented and executed an isolated evaluation under outputs/experiments-06/. No originals modified, agents spawned, downloads, remote writes, or secrets accessed.

## Frozen design and separation from selection

Before running heldout.py, wrote predeclared.json and its SHA256 to provenance.sha256. Fixed all 64 consecutive recipient seeds 1000–1063, all seven original seed labels, donor seeds 17/23 with 120 steps, and horizon 3. No recipient was filtered, replaced, or selected by threshold proximity. Original selected recipient 7 is excluded. Donors remain the original demonstration donors, so donor-selection generalization is untested. This is an operational predeclaration within this local run, not an externally timestamped preregistration. The script and raw per-recipient records are retained.

Within each recipient seed, virgin/A/B/complement-key-B/numeric-copy-B conditions deep-copy the same seeded engine, candidate histories, table, and RNG. All start K=3, mutation=0, exhale phase, empty archive. Assertions check table and RNG matching at intervention time. Complement-key-B maps every six-bit field key to its bitwise complement while retaining every entry value and total mass. Numeric-copy-B reassigns identical values without any additional historical representation. All original seed candidates are evaluated at t3; no label chosen after seeing outcomes.

These are new recipient RNG/table instances of the same engine, conditional on fixed donor histories. They are not independent mechanism replications or independent empirical support from the original sources. “Held out” means excluded from the original selected example and chosen before this evaluation, not proof nobody previously ran these seeds.

## Executed result

| Field | Recipients with any status changed /64 | seed-4 changed /64 | seed-5 changed /64 |
|---|---:|---:|---:|
| A | 0 | 0 | 0 |
| B | 8 | 7 | 1 |
| B complement keys | 0 | 0 | 0 |
| B numeric copy | 8 | 7 | 1 |

All other labels changed in zero recipients. B changes six seed-4 candidates spark→proto, one seed-4 extinct→spark (recipient 1062), and one seed-5 spark→proto (1013). Thus 8/64=12.5% is a status difference rate, not exclusively a promotion rate; promotion differences are 7/64. The original selected target-only result does not capture the prevented-extinction outcome. Descriptive Wilson intervals: B any-status 6.47–22.77%; A and complement-key-B 0–5.66%. These intervals treat seeded instances as sampling proxies; the deterministic consecutive seed interval is not a demonstrated random sample from a natural population. Do not treat 448 correlated candidates as independent recipients.

Donor B's seed-5 entry can also matter: recipient 1013 seed-5 average is .642273868 virgin versus .653180325 B. Every B record equals its numeric-copy record exactly, including RNG and controller outcomes.

## Residual: matched initialization is not matched continuation

Even at t3, seven recipients have unequal K under each transplanted field versus virgin. Six have one death in both arms; subsequent soil_richness includes existing transplanted field mass once the initially empty archive gains a death. Recipient 1062 has one virgin death versus no B deaths. This reveals a short-horizon coupling absent in selected recipient 7: an initially empty archive does not stay empty. B RNG state differs from virgin in one recipient; complement and A RNG remain equal. This does not invalidate the matched intervention but prohibits claiming all status effects hold controller trajectory and RNG consumption fixed throughout. Script retains K, K_int, archive counts, candidate averages, and RNG states to expose the distinction.

The surviving relation: a donor-produced genotype-indexed field changes some reset recipients' programmed outcomes across a fixed unfiltered collection, while identical field numbers give identical futures. The result strengthens sensitivity beyond one chosen near-threshold recipient. It does not establish universality, donor prevalence, unique historical semantics, or an emergent phase transition.

Serious rival: explicit additive genotype fitness bonuses and programmed gates explain outcomes. Recipient cannot distinguish donor history from identical numerical entries; numeric-copy equivalence directly demonstrates that provenance has no separate engine-level causal role. Complement control suggests key alignment matters for these seven labels and this horizon, not that arbitrary shuffles are always ineffective.

## Concrete reversible improvement

Implemented predeclared recipient enumeration, all-label reporting, mass-preserving key reassignment, numeric-copy control, and continuation diagnostics in new heldout.py; discard that folder to reverse changes. Recommended next, not executed: independently predeclare donor seed sets and vary them crossed with these recipients; add a diagnostic wrapper holding richness/controller fixed to separate direct fitness and death-mediated controller effects. Such a wrapper changes the model and must be reported as an intervention rather than its natural continuation. Preserve the selected original as an existence witness.

## Commands and artifacts

Executed copies of both original garden scripts into outputs/experiments-06/, then wrote predeclared.json before writing/running heldout.py. Executed:

```sh
sha256sum /workspace/frr-distributed-2026-10-07/outputs/experiments-06/predeclared.json /workspace/frr-distributed-2026-10-07/outputs/experiments-06/true_garden*.py > /workspace/frr-distributed-2026-10-07/outputs/experiments-06/provenance.sha256
cd /workspace/frr-distributed-2026-10-07/outputs/experiments-06 && python heldout.py > run.stdout.txt
```

Run completed successfully in under one second. results.json contains plan, donor fields, all rows, aggregate changes and descriptive intervals; run.stdout.txt records summary. Follow-up read of results.json identified all transition types and the seven archive/controller discrepancies. No threshold-search phase occurred.

Sources inspected: NOW.md; FRR v0.5 Compact Runtime Seed; original true_garden_field_transplant.py and true_garden_fluid_settled.py in full; reports/experiments-03.md in full; RECOVERY_NOTE.md; opening context/history sections of CONTINUATION_HANDOFF.md and RECOVERED_CODEX_HISTORY.md. Source ancestry is shared with original transplant and worker03; this report's new contribution is independently authored evaluation code and newly executed seeded conditions, not independent scientific provenance.
