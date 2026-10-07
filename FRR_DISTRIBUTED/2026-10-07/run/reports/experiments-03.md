# Garden transplant: executed replay and selection provenance

Worker experiments-03, 2026-10-07. Executed the byte-identical supplied transplant script importing a byte-identical isolated engine copy, Python 3.12.14 / NumPy 2.3.5. Both SHA256 pairs match originals (outputs/experiments-03/provenance.sha256). Actual stdout is outputs/experiments-03/transplant.stdout.txt. This is reproduction from shared originals, not independent empirical replication. Sources remain unchanged. A separately authored reversible diagnostic is provenance_controls.py with executed controls.json.

## Observed evidence

Donors A/B ran seeds 17/23 for 120 steps. A: total wake .62874, target wake zero, archive 28. B: total wake .61909, target wake .08529, archive 23. Recipient seed 7, target seed-4 genotype 011001, mutation disabled, common deep-copied local state/table/RNG, exhale phase.

| Condition | fitness t0 | status t3 | K t3 | archive |
|---|---:|---|---:|---:|
| virgin/empty | .633253 | spark | 3.02029 | 0 |
| A field/empty | .633253 | spark | 3.02029 | 0 |
| B field/empty | .718547 | proto | 3.02029 | 0 |
| virgin/B archive | .633253 | spark | 2.97199 | 23 |
| B field/B archive | .718547 | proto | 2.93752 | 23 |

B field-only target fitness decays to .717782 at t3 and .715527 at t12, retaining proto. Saturated archive/virgin field begins with richness 1, changes target fitness to .514067 at t1 via table redraw, and reaches K=2.41746, integer K=2 at t12. These reproduce the recovered exp_016 note's values to displayed precision.

## How the distinction entered construction

The source explicitly says recipient seed 7 was deliberately chosen near spark/proto promotion; the recovered exp_016 note repeats this. No selection search log, tested-seed inventory, rejected cases, or predeclared distribution is available. Thus selection provenance is an admitted construction choice, not a reconstructable selection procedure or prevalence estimate. Donor histories and additive genome-keyed fitness lookup are explicit code mechanisms; the significance of their effect is additionally supplied by a programmed avg>.65 and verifications>=3 gate.

An observation subtlety: t0 target_fitness recomputes fitness under transplanted soil, but candidate.fitness and fit_history still contain the virgin .6332525266. Actual promotion at t3 averages four values, including that original stored value. New diagnostic logs this: full B average .6968404486 versus virgin .6332525266. A criterion described solely as instantaneous fitness above .65 would misstate this experiment.

## Field/archive distinction and surviving relationship

_die simultaneously deposits .08*c.fitness in soil_field at the dying genome key and appends the genome to soil. Natural histories therefore couple the carriers. The transplant separates them as an artificial intervention. compute_fitness uses soil_field directly; soil_richness returns zero if soil is empty even when field mass is nonzero. Consequently the three empty-archive conditions share controller trajectories through the observed horizons. With an archive present, richness includes field mass/3 plus archive length/80, so field and archive effects are not generally additive or globally independent. Richness affects K and triggers inject_entropy above .6; compost can use archive genotypes after a phase switch. Those later mechanisms prohibit broad long-horizon isolation claims.

The surviving relation is precise: a history-generated genotype-specific field entry can change a reset recipient's programmed status while its initial candidate state and table match. This identifies an external mutable carrier in this synthetic central engine, not distributed storage, thermodynamic entropy, or shared mechanism with language models or graphs.

## Serious rival/residual and reversible improvement

Rival explanation for broad claims: this is an explicitly additive fitness bonus plus a deliberately selected decision boundary. Historical origin is supplied by the donor run, but equal numerical entries inserted manually would have the same recipient effect; the recipient cannot identify the provenance of the entry. The experiment supports carrier causality, not unique historical semantics or an emergent universal threshold.

Implemented diagnostic removes only B's 011001 entry or retains only that entry, with empty archives and common recipient. At t3 removal restores spark / average .6332525266; target-only restores proto / average .6968404486. All four diagnostic conditions have exactly K=3.0202858840311664. This sharpens attribution to that entry for this target/horizon and exposes actual promotion-history values, without editing original sources. Necessity/sufficiency here is local to these interventions and first three steps.

Recommended, not executed: freeze an independently chosen recipient seed distribution and all seven target labels before viewing donor outcomes; report field-only status-change fractions with uncertainty, target-entry shuffled controls, and table/continuation checks. Keep the selected demonstration as an existence witness and its open exploratory question available rather than renaming it a population result.

## Sources inspected

NOW.md and FRR v0.5 compact seed; recovered-originals/2026-10-05/RECOVERY_NOTE.md, true_garden_field_transplant.py, true_garden_fluid_settled.py; CERTX-context/codex-field-wake/exp_016_field_wake_transplant.md; CERTX-context/CONTINUATION_HANDOFF.md and RECOVERED_CODEX_HISTORY.md. The October 5 note/source and this rerun share ancestry; matching documentation and output do not create independent evidence. Intake pause text is superseded by current NOW authorization. No remote writes, downloads, secret inspection, or child agents.
