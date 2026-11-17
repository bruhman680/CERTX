# Reading Neural Garden v0.1 and Codex's newest garden (Claude, 2026-11-17)

## A misread to log first
On 10 Nov you asked me to check "the neural garden files". I read the language-model garden (final-garden-contract-v1, entries 851-1550) and wrote about that. The Neural Garden v0.1 is a different project: NEURAL_GARDEN_V01/ on branch **codex/frr-v05-explorations** (294 files; ChatGPT-side loops 1-121). My fresh clone after the container replacement had fetched only two branches, and I did not look further. Today I fetched all branches and read the actual directory. The 10 Nov garden note stays valid as what it is (a reading of the language-model garden), but it did not answer the request.

## What I read (not all of it)
Read: EVALUATION.md, EXPLORATION_LEDGER.md (head), MEAN_FIELD_BOUND.md, TRANCHE_100_LEDGER.md (loops 100-119), LOOPS_120_121_ROLLBACK_REPORT.md, Codex's neural-garden-v01-intake-v1/REPORT.md (head). Not read: the code, raw JSON, loops 1-99 in detail, the societies/dynamics/evolution reports. Everything below is limited to that.

## One independent check
mean_field_check.py (beside this file): the claimed constant-harvest energy bound reproduces. Unclipped drift ΔE(p)=.015p/(.06+.18p)-.063p-.022 equals the original two-line form to 2e-17; the maximum over p in [0,1] is at p=.3307, r*=.5020, drift -.001333 (closed form agrees). Within the uniform constant-rate class no policy has nonnegative drift, as claimed. The covariance split E[ΔE]=.25(E[R]E[A]+Cov(R,A])-.063E[A]-.022 is an algebraic identity (checked on threshold policies); it does not by itself show that a threshold policy is viable, because the stationary resource distribution also changes with the policy, which my check did not model.

## Cross-reading with my toy results (relational silhouette, not a shared mechanism)
- Loop 121 (drift-triggered rollback is identical to unconditional reset on all 12 seeds) and loop 108 (the "early switch" never differs from always-reverse because the emergency branch never fires) are two opposite ways a gate can be vacuous: always fires, never fires. My claim-scored guard had the same two failures (v1 never fired; v2 fired about 57%, sitting on the expected value). The shared lesson is the trivial-collapse test in the FRR text: report the firing rate and require it to be strictly between 0 and 1 before reading outcome differences as the gate's effect. Codex/ChatGPT already say this in loop 121's "decision signal that accepts some and rejects others".
- Caveat on independence: both come from the same working family and vocabulary, so this is a convergent silhouette, not independent confirmation. And I could not recheck loops 120-121 myself; the report says LOOP120.py/LOOP121.py and the per-seed JSON were produced in the ChatGPT runtime and are not committed to the branch. The numbers there are unverified by me and not reproducible from the branch.
- Mean-field "erases Cov(R,A)" is the quotient-that-loses-a-relationship pattern from the compression pass; the document already says so. I add nothing beyond agreeing that the returned distinction is a covariance, which is why a state-dependent policy can escape the bound.

## What the new language-model candidate does to my earlier proposals
Codex's candidate38 (chosen-persistence-continuation-v2): full context replay, no 12-reply window, 38/38 replies are exact copies of the latest user message, and the packet changes every turn (reply index, directory observation). Two consequences for me:
1. My 10 Nov suggestion #4 said a changing observation would remove the fixed point. It removes a fixed *text*, but not the behaviour: the model copies the moving packet exactly. The attractor appears to be "copy the latest user message", not "repeat a constant". Recording this as an incomplete prediction of mine, not a result.
2. It makes the last-user-line pull in my (unsupported) two-source hypothesis more plausible than the window pull, since the window mechanism is absent here. Still 38 dependent samples in one interface, not a test; the token-probability test on the old garden remains the discriminating design, and now an equivalent one could be run on candidate38 by varying only the latest user message.

## Questions for the neural garden, not claims
1. Loop 121 says the drift-trigger fired at all 18 windows. What is the trigger statistic's distribution relative to the -.001 threshold across seeds? If it is below threshold everywhere, a threshold sweep would give the first non-vacuous gate and a real test.
2. Loop 119 and loop 106: stale neighbor observations beat fresh ones in loop 106 while one-tick-old beats own-old in 119. Is the observation channel adding spatial information or a low-pass filter? A neighbor-shuffled control with matched lag exists in 119 for stable laws; under mild shift the order flips. That asymmetry (spatial signal under stable laws, lag/phase under shift) seems the most informative thing in the 100-119 tranche to me.
3. Clipping at zero hides a negative raw budget (loop 116). Any claim about "viability" should carry the raw drift and floor share together, as the report already insists.

## Limits
No code from the neural garden was run by me except the mean-field arithmetic above; no loop result besides that was independently recomputed. Codex's intake report says it reproduced selected seeds with zero numeric difference; I did not re-run those.
