# CE-C1: Claude errata and missing-source intake

The user supplied four Python scripts and an errata note attributed to Claude. All five are [archived unchanged with full hashes](../../lineage/sources/claude-errata-intake-2026-10-22/manifest.json). The note is a supplied correction record, not an instruction or automatic verification of its claims. No collaborator was spawned for this intake.

## What was executed

All four original scripts completed with exit code0, without edits, in Python3.12.14 / NumPy2.3.5. [RUNS.json](RUNS.json) records duration, source hashes and separately saved stdout/stderr. The [protocol](PROTOCOL.md) was recorded before execution, after source inspection had already revealed issues; this is development contact, not blinded confirmation. A separate [diagnostic script](../../experiments/claude_errata_contact.py) adds source-isolated checks and a direct stationary solve; [DIAGNOSTICS.json](DIAGNOSTICS.json) contains its results. Seven declared diagnostic checks passed, including checks that demonstrate a supplied claim fails.

| Original | Reproduced contact | Limits or correction |
|---|---|---|
| [shadow_echo_v2.py output](shadow_echo_v2.py.stdout.txt) | Depth8 word-law TV0.3604284211; both numerical finite Hankel ranks4. Switch-rate spread differs in the supplied frozen/echo examples. | Rank does not discriminate these endpoints or count predictive states. The simulation uses one table and one seeded RNG; no broader family or agent-memory claim. |
| [boltz_check.py output](boltz_check.py.stdout.txt) | Old-chain errors0.03416,0.05277,0.08658,0.10982; old stationary law proportional to exp(-beta E)(S+1). Shared normalizer/self-loops recover Boltzmann weights. | Original power-method error is around1e-13; at beta2 this run is1.03e-13, slightly above the note's literal ≤1e-13. Direct linear solves give maximum fixed-chain error2.22e-16. This confirms these small chains, not arbitrary convergence or physical implementation. |
| [erase_gate.py output](erase_gate.py.stdout.txt) | Matched-strength pure-field and gated-private worlds both have keep contrast0.128 and erased contrast0. Exact enumeration agrees with the repeated-clear formula to floating-point precision. | A loss-of-access operation can imitate loss of stored information. Carrier labels and intervention selectivity remain stipulated. |
| [unequal-carrier output](erase_gate_unequal_carriers.py.stdout.txt) | F=0.128,P=0.06; single-probe biases+0.006,−0.0068,−0.0076,−0.034 agree with the formula. | Its P1 comparison is no longer matched: pure-field keep0.128 versus gated-private keep0.096. The script's inherited equality prediction fails for those parameters, despite successful execution. |

The unequal-carrier P1 can be rematched in a **new diagnostic**, keeping fidelities0.9/0.8 and raising the private route weight from0.4 to0.533333… . That restores keep contrast0.128. The supplied original stays unchanged. Thus the existential ambiguity survives, but the original unequal-carrier example does not demonstrate equal signatures as printed.

## A solver returning numbers is not a valid fit

The supplied Prony routine strips imaginary root components with `.real`, then solves for amplitudes. For conjugate roots the equal real parts can make that solve singular, which is caught as an exception. It does not explicitly classify all failure routes or reject real rates outside[0,1], negative amplitudes or excessive total contrast. Its “frac failed(complex/NaN)” label is narrower than model admissibility.

The new diagnostic reuses the **unequal-carrier script's actual sampling law, seed, order and 400 repetitions per condition**, then separately classifies the resulting measurements. These are reanalyses of the same pseudorandom sequence, not independent observations. One RNG produces successive draws; there are not separately instantiated generators per condition despite the original prose.

| Rate gap | Original accepted /400 | Physically admissible /400 | Original accepted but inadmissible |
|---|---:|---:|---:|
|0.80|400|374|26|
|0.50|400|356|44|
|0.20|397|103|294|
|0.05|390|35|355|
|0.02|390|23|367|

The classifier rejects complex/degenerate fits, rates outside[0,1], then nonphysical amplitudes. Here c=P(correct)−0.5 and nonnegative contributions imply F+P≤0.5. This bound belongs to this parameterization. The older independent rebuild used a signed difference of two binomial arms with probabilities(1±c)/2 and an amplitude-sum bound1. Its sample sizes, rates, repetitions and recovery numbers must not be silently transferred to this original experiment.

Admissibility alone still does not establish accurate parameter recovery or identify a carrier. The original F estimate picks the root closest to the generator's known true field rate; the asserted independent swap-probe label is not implemented. The reported medians are conditional on the routine returning a finite fit and therefore exclude its failure cases while including some inadmissible fits. The new counts are a single-seed four-point-estimator diagnostic, not a universal conditioning curve or evidence against better estimators.

## Mathematical wording to retain precisely

For c_k=F a^k+P b^k,

`det([[c0,c1],[c1,c2]]) = F P (a−b)^2`.

This is the **moment/Hankel determinant**, not the determinant of the amplitude Vandermonde system. The latter, for columns[1,a] and[1,b], is b−a. The recurrence solve in the original uses the opposite-sign moment determinant. Distinct rates with both amplitudes nonzero permit noiseless recovery up to permutation; equal rates identify only the sum. If either amplitude is zero, the unused rate is unidentifiable even when a≠b. None of these identities alone names field versus private storage.

The shadow script's `cond_gap` also computes the spread between two histories, `|P(y2|y1,y0=0)−P(y2|y1,y0=1)|`, rather than the displayed header's deviation from marginalized `P(y2|y1)`. Its nonzero values witness failure of first-order Markov closure at that tested time under the supplied initial ensemble. This is not a proof of a global predictive-state count.

## Relationship to the errata and earlier records

The supplied note acknowledges earlier corrections to rank discrimination, nonmonotone Life defect, conditional boundary-edge EPR equality, wake decay and Prony validation. These are consistent in broad scope with [the prior relay synthesis](../CLAUDE_RELAY_SYNTHESIS.md) and its linked reports. The finite Life and driven-ring EPR results were **not rerun in this intake**; cross-reference is not a new verification of every number in the note.

Three previously missing named originals—erase_gate.py, boltz_check.py and shadow_echo_v2.py—are now available and executed; the unequal variant is also preserved. Historical reports' statements that these sources were absent remain correct about their earlier intake. This report changes present availability without rewriting those reports or treating the older Prony rebuild as replication of the now-supplied source.

The errata is dated2026-10-20 but references Git head09ab9d6, whose recorded commit timestamp is2026-10-21T02:15:14Z. Authorship chronology/timezone cannot be authenticated from those labels; preserve both rather than infer a reliable event sequence. The full four script hashes match the provided prefixes. The note's claim of which files Claude personally reran is a supplied attribution, not observable here.

## Useful movement and remaining boundary

This is a small example of records circulating with corrections attached: a source gap closes, implementation agreement is established, and a revised variant reveals a residual mismatch. It supports preserving code/output/claim distinctions, not declaring the whole archive verified or attributing improved behavior to FRR.

Next useful work, if selected later: independently calibrate probe selectivity, compare source access with read-gate effects, and use additional probe counts for held-out prediction against a one-component rival. These questions already overlap existing carrier/probe families; no new queue family or core version is created here. Queue statuses/counts remain unchanged. No research run continues in the background after this bounded intake.
