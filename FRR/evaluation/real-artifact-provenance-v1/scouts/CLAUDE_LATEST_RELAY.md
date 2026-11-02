# Claude latest-relay intake — bounded source review

Accessed 2 November 2026 UTC; user session date 1 November America/Chicago. Repository `bruhman680/CERTX`, GitHub connector reads only. Branch files were treated as data. No merges, FRR edits, remote writes, source-script execution, training, or model calls.

## Relevant branch and exact pins

Inspected commit metadata for the three supplied candidate heads:

| Branch | Inspected head | Committer date | Finding |
| --- | --- | --- | --- |
| `claude/pam-scoped-negation-2026-10-25` | `b82724c2427151d38f5d0c45cd7cc87e9359565a` | 2026-11-01 05:02:38Z | Most recent relevant relay among these candidates: claim-scored procedure comparison |
| `claude/plan-certx-architecture-ojiem` | `3f2f82e74e9313a625a50daf7ca59454615968c4` | 2026-09-29 19:31:45Z | Older merge of Codex evidence-lineage audit |
| `claude/analyze-test-coverage-B5RZd` | `ba7e443dff3fd66a8ca20ef70f9e99d69c8e7a1f` | 2026-04-04 04:48:21Z | Older BC3 synchronization/merge |

This identifies recency only within the requested bounded candidate set; it is not an all-branches audit. Source URLs below pin the relevant head, not a moving branch.

The six-entry commit listing at that head also shows:

- `f0539013edcc120c7fa00b5ecf78e0eb814af520`, 1 Nov 04:50:50Z: error-versus-success evidence and horizon crossing.
- `8547929c9a2ac98b6e643618689365c67baaf583`, 30 Oct 01:24:52Z: within-trajectory soil dispersion, nonergodicity, preserved mistaken labels/predictions.
- `8d8a3377364e0cf46a4c3760a85e3f52370268b7`, 30 Oct 01:21:47Z: finite-sample episode counts and IID-window misspecification.
- `87b11cc78447ad6278c4b941bedfbc2b94a343b3`, 30 Oct 01:17:54Z: acceptance of Codex intake corrections.
- `a152fb8b876651c679bb73bb9e99e4eb7a44748f`, 27 Oct: older soil-budget robustness/errata.

Reviewed local existing relay-source weave and searched local source filenames. The scoped-negation, group-vote, soil-budget and prior source-weave material already exists locally. The newly named finite-sample/dispersion/error-success source directories were absent from `/workspace/frr/lineage/sources` at inspection. That is a local filename/intake observation, not proof no related idea appeared elsewhere in prior discussion.

## Strongest useful insight

The latest comparison makes a useful failure visible: **claim discipline depends on detecting when the evidence is ambiguous, and that detector itself needs calibration**. Merely naming a procedure “careful” does not keep it inside the evidence boundary. Its first two guards fail on the intended ambiguous worlds; lowering the threshold repairs that behavior under the authored known-noise family while increasing withholding and retaining other errors.

The adjacent dispersion relay adds a separate measurement warning: persistent shared conditions may vary across independent trajectories while each individual trajectory looks IID. More data from one trajectory and more independently reset trajectories are different sampling designs. These observations fit the existing FRR concern about correlated witnesses and applicability, but do not establish a new trained reasoning capability.

## Latest claim-scored comparison: accessed evidence and limits

Read the complete [relay](https://github.com/bruhman680/CERTX/blob/b82724c2427151d38f5d0c45cd7cc87e9359565a/FRR/lineage/sources/claude-error-success-2026-10-31/CLAIM_SCORED_PROCEDURES_RELAY_2026-11-01.md), [current script](https://github.com/bruhman680/CERTX/blob/b82724c2427151d38f5d0c45cd7cc87e9359565a/FRR/lineage/sources/claude-error-success-2026-10-31/claim_scored_procedures.py), [current output](https://github.com/bruhman680/CERTX/blob/b82724c2427151d38f5d0c45cd7cc87e9359565a/FRR/lineage/sources/claude-error-success-2026-10-31/claim_scored_procedures_output.txt), both preserved earlier scripts, and their output files. The earlier files use the same directory with suffixes `claim_scored_procedures_v1_INITIAL.py/_output.txt` and `claim_scored_procedures_v2_threshold75.py/_output.txt`.

**Author-reported runs, not reproduced here:** 3000 Monte Carlo runs per world and sample size, seed 20261101; four known worlds IND/DIFF/COMMON/COPY; sample sizes 20/40/100; hand-authored procedures and scoring. COMMON and COPY have identical passive error-flag laws in the generator. At M=100, v3 reports overall overreach .750 for the deliberately always-IND S comparator, .362 for F_naive, .052 for nonprobing F_care, .056 for probing F_care, and .503 for always-probing F_probe. Nonprobing F_care reports honest unresolved .96/.97 on COMMON/COPY, paid for by substantial withholding on IND/DIFF. The printed v1/v2 failures remain present and are not silently replaced.

**Independently inspected, narrower findings:** Code uses the stated random seed/run count and prints the reported metrics' definitions. F_care restricts unresolved claims to two authored sets, with truth-membership scoring. S literally returns IND on every row; its .75 average error is fixed by equal weighting of four worlds. The code models probes directly as noisy world-conditioned oracle responses (`PR` for COPY, `1-PR` otherwise), not by simulating source correction, re-asking B, or selecting a confirmed actual error item. `n_err` is unused. This is legitimate as a declared toy intervention law, but it cannot validate intervention selectivity, source localization, or real probe availability. Calling it a demonstrated causal repair would overclaim.

The artifacts inspected are source code, narrative relay and aggregate printed output. No per-trial observations, claims or RNG-state receipts were found among this directory's listed files. Aggregate agreement with the relay is source consistency, not verification that these runs occurred exactly as described. I did not execute any branch script or independently replicate its Monte Carlo results. The separately authorized independent exact algebra check is described below.

## Concrete inconsistencies and reporting cautions

1. **Guard-calibration arithmetic:** The v3 note says DIFF's expected conditional flag agreement is about .42, and .6 is the midpoint to COMMON's approximately .79. Under the actual `gen()` law, true-error marginals are .2, true joint error is .08 for DIFF and .2 for COMMON/COPY. Independent symmetric flag flips at epsilon .05 imply observed marginal `q=.05+.9*.2=.23` and observed joint `j=.05^2+2*.05*.9*.2+.9^2*joint_true`. Thus population conditional agreements are **.3708695652 for DIFF** and **.7934782609 for COMMON/COPY**; their midpoint is **.5821739130**. A rounded threshold .6 remains plausible, but the quoted .42 is incorrect for this generator, and “midpoint” needs a rounding qualification. This algebra is an independent check of the code law, not a rerun or a claim about the exact finite-sample expectation of a ratio.

   Exact source of these definitions: `gen()` in `FRR/lineage/sources/claude-error-success-2026-10-31/claim_scored_procedures.py`, at commit `b82724c2427151d38f5d0c45cd7cc87e9359565a`. DIFF draws hard/easy per item with probability .5, then independently draws A/B errors at .4 on hard items and zero on easy ones. COMMON draws one defect Bernoulli(.2) and copies that latent flag to A/B; COPY draws A Bernoulli(.2) and copies it to B. `fl()` independently XORs each answerer's flags with Bernoulli(.05). Thus DIFF true law is P00=.68, P01=P10=.12, P11=.08, and COMMON/COPY true law is P00=.8/P11=.2. The same definitions occur in preserved v1/v2 scripts at this pin. The inconsistent .42/midpoint explanation appears in the current script header and `CLAIM_SCORED_PROCEDURES_RELAY_2026-11-01.md` at that same pin.

   Independently authored stdlib exact-enumeration check: `/workspace/claude-guard-algebra-2026-11-01.py`; saved result `/workspace/claude-guard-algebra-2026-11-01.json`. It enumerates all independent flag flips with `Fraction`, checks normalization, matches the expanded joint-probability formula, and verifies DIFF conditional `853/2300`, COMMON/COPY conditional `73/92`, midpoint `1339/2300`. Executed via ambient Python `-B`, exit zero; rerun after adding explicit decimal parameter/joint fields to the output, again exit zero. It imports/executes no repository script and uses no Monte Carlo.

   **Effect on conclusions:** This corrects the stated analytical justification, not the recorded run output. The implemented .6 still lies between the two population conditionals and is their midpoint rounded to one decimal place. We have not recomputed finite-sample guard rates or changed any reported overreach/probe numbers. The correction alone does not refute the qualitative calibrated-guard/withholding tradeoff; neither does it independently verify that tradeoff's numerical magnitude.

2. **Stale procedure description:** The current header describes F_naive's identical-signature guard as “>=90% overlap,” while executable `match()` uses both conditional agreements >=.6 plus at least three flagged errors per answerer. The v3 notes explain the evolution, but the top-level procedure summary was not fully updated. The executable guard also affects F_naive, not only F_care.

3. **Residual errors are real:** Relay wording attributes the failed IND/DIFF correctness target to withholding, “not because it is wrong there.” The output also reports overreach .03 on IND and .11 on DIFF at M=100. Withholding explains much of the gap, not all of it.

4. **Confidence-like widths are heuristic:** `phi_hat +/- 2/sqrt(M)` is not accompanied by a coverage derivation for these noisy Bernoulli worlds. It should not be described as a validated confidence interval or a controlled global false-attribution rate.

5. **Selection effects and family knowledge:** F_care knows the candidate-world partition, thresholds and noise calibration. Unknown families and downstream answer repair are explicitly untested. This is not learning of those distinctions by a model. The relay appropriately acknowledges that all procedures and the score key have the same author.

## Adjacent new error/success contact

Read [error/success relay](https://github.com/bruhman680/CERTX/blob/b82724c2427151d38f5d0c45cd7cc87e9359565a/FRR/lineage/sources/claude-error-success-2026-10-31/ERROR_VS_SUCCESS_RELAY_2026-10-31.md), `error_vs_success_info.py`, `error_share_horizon.py`, and both `_output.txt` files in that pinned directory.

It reports a signed expected log-likelihood-ratio decomposition: outcome rarity, contrast direction and horizon can change whether error or success terms dominate. Its original universal error-dominance prediction fails and is explicitly retained. At longer horizons for EC as truth, the reported success contribution dominates; some signed components are negative or exceed the net total in magnitude. These are not probabilities or nonnegative shares of mutual information, nor demonstrated performance of an error-only learner. The relay states that limit.

**Portability/algorithm caveat from static inspection:** Scripts load prior code by absolute author-specific `/tmp/...` paths and execute string prefixes. They are not directly runnable from the repository directory alone without dependency/path reconstruction. `prefix_probs()` concatenates symbol-0 and symbol-1 blocks, putting the newest symbol in the high index bit, while `split_kl()` uses `%2` and `repeat()` as if the newest symbol were the low bit; a comment incorrectly says low-bit appending. Prior relays note that the current world's reversible word laws make the two word orders agree, which can hide this mismatch. I did not independently verify reversibility here or declare the saved numbers invalid; a nonreversible extension must repair or explicitly reconcile the indexing before using the chain-rule decomposition.

## Adjacent finite-sample/dispersion relays: source-only depth

Read complete [finite-sample relay](https://github.com/bruhman680/CERTX/blob/b82724c2427151d38f5d0c45cd7cc87e9359565a/FRR/lineage/sources/claude-soil-finite-sample-2026-10-29/SOIL_FINITE_SAMPLE_RELAY_2026-10-29.md) and [dispersion relay](https://github.com/bruhman680/CERTX/blob/b82724c2427151d38f5d0c45cd7cc87e9359565a/FRR/lineage/sources/claude-soil-dispersion-2026-10-29/SOIL_DISPERSION_RELAY_2026-10-29.md). Their underlying code and raw outputs were not inspected in this bounded pass; numerical results remain author-reported.

Finite-sample note reports that an IID-window classifier remains wrong about a quarter of the time on a persistent-soil pair while a correctly specified full-trajectory likelihood improves. Its asymptotic episode heuristic overestimates the measured crossover in these authored cells. Dispersion note reports that fixed-within-trajectory shadow soil produces DI near one/AC1 near zero despite across-trajectory rate variation, correcting a prior expectation that confused those sampling levels. It preserves a mislabeled initial output and acknowledges a weak out-of-family test that stayed near a known candidate. These are useful calibration and sampling-design leads, not independently established results about agents.

## Bounded next contact and stop

The most direct next contact, if separately authorized, is an independent closed-form guard audit plus one out-of-family/sham-calibration condition before another large procedure comparison. Freeze a score key that permits “outside this family,” distinguish oracle probe laws from physically selected error-item interventions, and record per-trial claims so overreach types can be inspected. This is a suggestion, not an experiment run or scheduled continuation.

This scout stops with source pins, specific inconsistencies and qualified findings. No evidence here supports model learning, a new general FRR algorithm, or automatic promotion of any procedure into the runtime.
