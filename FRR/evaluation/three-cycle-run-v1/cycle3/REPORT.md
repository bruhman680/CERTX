# Cycle3: review, guard and preservation

This is an adaptive review/refinement cycle, not a third independent confirmation or a randomized comparison of FRR versus other guidance. It reuses Cycle1 data and the Cycle2 exact counterexample. Root and three delegated agents share platform ancestry and session context; role separation does not make the evidence independent.

## Review changed our interpretation

The [separate Cycle1 audit](../review/CYCLE1_AUDIT.json) reconstructed candidate decisions and continuous estimates from saved measurements. Its biggest clarification is that estimated redundant designs look numerically rank2 in2338/2400 cases even though their stipulated population design is rank1. Pooling two duplicate reset arms does not force equality of their independently noisy coordinate estimates. The structural refusal, not pooling alone, prevents reporting a generic allocation. The original protocol rationale and result data remain preserved; Cycle1's report discloses the correction.

The audit also distinguishes4800 unique synthetic datasets from14400 offline analysis rows; the same measurements support known, estimated and absent-calibration views. Statistical costs must not be tripled. Across both designs and all budgets, the experiment models213120000 scalar Bernoulli trials, sampled efficiently as aggregate binomial counts; these are not213million tool calls, model calls or separately materialized random bits. Hardware/preparation/real-world calibration costs are outside this accounting.

The [Cycle2 report](../cycle2/REPORT.md) identifies model saturation: a three-parameter independence-assumed fit can match three measurements exactly while giving biased contributions and wrong out-of-fit predictions. Joint-witness and Fréchet results are conditional constructions, not empirical calibration success or universal identification.

## Executable refinement

Cycle1's original allocation implementation has no singular-estimate guard. All2400 observed estimated diverse matrices were full rank, so this caused no observed result error. A constructed singular input nevertheless needs an explicit unresolved outcome. [allocation_guard.py](allocation_guard.py) now checks calibration availability, declared population rank, admissible finite inputs and estimated rank before returning conditional estimates and intervals. It does not independently establish witness validity, population design rank, readout correctness or independence.

[Protocol](PROTOCOL.md) precedes the guard execution. [check_guard.py](check_guard.py) exercises full-rank, semantically redundant, numerically singular, absent-calibration and invalid-input cases, then replays all4800 saved full-rank mode-assessments. [CHECKS.json](CHECKS.json) records agreement within4.45e-16 and zero new random draws. This is a tested scoped utility, not deployment into a general agent runtime. Original Cycle1 source/results are unchanged.

## Guidance and stopping

The optional verification guidance can now name a sharper measurement obligation: distinguish numeric invertibility from identifiable design; validate joint effects when the readout depends on relationships; include a consequential out-of-fit check; and retain unresolved status if calibration is missing. No universal numeric gate, core FRR version, scheduler or scientific queue completion follows.

After source/measurement binding checks and GitHub publication, this is the third and final requested cycle. Return for user review rather than launch a fourth. Unknown or biased witnesses, access loss, unknown reset targets, finite-sample interaction inference and real-agent transfer remain open. The deferred readable-code/history idea remains untouched.

## Adversarial guard review and repair

A separate reviewer then challenged inputs beyond the initial fixtures. The initial guard accepted an impossible Bernoulli contrast vector[2,2,2] and emitted infinite interval widths for an extreme finite radius. Initial guard source, checker, receipt and execution streams are preserved with `_INITIAL` names; their passing fixtures did not cover these faults. The repaired guard rejects out-of-range contrasts and nonfinite derived uncertainty. Two additional fixtures pass, with all4800 saved full-rank allocations/widths still unchanged within4.45e-16. This is a new checker revision, not retroactive evidence the initial checker was complete. The review's initial nonstandard Infinity-containing JSON is also preserved separately and rendered strictly in the corrected audit.
