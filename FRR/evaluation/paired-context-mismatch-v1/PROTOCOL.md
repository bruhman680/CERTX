# PC-C1/2/3: imperfect paired context, population target and task utility

Prospective three-cycle contact authorized after SA-C1/2/3 on25October2026 (America/Chicago). Cycle1 freezes source inputs, original analytic contrasts, design and preflight. Cycle2 one fixed main execution. Cycle3 independent metric/saved-array audits, report and navigation sync. No new model/provider API, language-model training, package installation, behavioral participant or physical-memory claim. Numerical collaborators communicate; this is not a group-benefit experiment.

## What stays fixed

Reuse exact source `../structural-access-three-cycle-v1/run/inputs.npz`, whose bytes are bound by predecessor ARCHIVE_MANIFEST.json (restore documented archive if absent). Copy unchanged as `run/source_inputs.npz` before scoring; preserve source hash and original source manifest. Never import predecessor experiment functions. Source seeds92501/92507/92509;24complex dimensions, twelve context/twelve binding coordinates; only predecessor denseQ used. Reuse actual evaluation/calibration record/query arrays: eight eval entities x2times x3statuses=48candidate records/seed; four disjoint cal entities; r=.5/2; eval query noise0/1.5, two repetitions/claim. No new eval inputs, phase code, labels, noise, corpus or query selection. A/N/U phase1/-1/exp(i*pi/3), oracle A-reference orientation and known target rank remain supplied. This is a conditional development follow-up, not independent test data or a natural-language encoder.

## New paired training model, frozen grid

For corresponding source seeds use new training master seeds94101/94111/94121. Spawn three separate RNG streams for common context c, binding b and mismatch a. Each bank has1024independent real unit vectors in12dimensions from normalized iid Gaussian draws; save raw and unit arrays. First768are fitting bank; last256are validation contrasts. Banks share no evaluation/calibration examples; common random banks reused across arms and nested prefixes. Validation is for reporting only, never rank/arm selection.

Training pairs are linear, unnormalized after perturbation:

    w_A=((c+delta*a), b)/sqrt(2)
    w_N=((c-delta*a),-b)/sqrt(2)
    D=(w_A-w_N)/2=(delta*a,b)/sqrt(2).

This deliberately varies exactly matched context while holding binding contrast fixed. Five arms: CLEAN delta0; INDEPENDENT delta.5; INDEPENDENT delta1.5 (a independent of b); ALIGNED delta.5; ALIGNED delta1.5 (a=b). Do not normalize perturbed members: that would change the cancellation model. The linear fixture is not a claim that real embedding pairs have these norms or nuisance laws. No extra training noise. Apply SAME saved denseQ to both training members, calibration/query/candidate arrays and analytic projectors. Fit top12 left singular vectors of the uncentered difference matrix for nested m12/48/192/768. Supplied rank/pair status/matching remain privileges. Save all singular values, numeric rank at1e-10, retained rank12 and cutoff gap/tie flag; no empirical rank/threshold selection.

## Analytic population controls

In base coordinates P_B=diag(0,I) is intended binding. CLEAN population second moment diag(0,I)/(2d). INDEPENDENT population second moment diag(delta²I,I)/(2d). Unique top-d target is P_B for delta<1 and context P_C for delta>1; gap=abs(1-delta²)/(2d). ALIGNED population moment [[delta²I,delta I],[delta I,I]]/(2d), target P_G=[[delta²I,delta I],[delta I,I]]/(1+delta²), gap=(1+delta²)/(2d). For spanning aligned training (m>=d), estimated projector equals P_G up to numerical error; distance from P_B is delta/sqrt(1+delta²), not a sampling artifact. No delta1degenerate population condition in grid. Transform Sigma/P by Q * matrix * Q^T. Analytic target is a supervised diagnostic, not a fourth task arm or label truth.

For every arm/m/seed save empirical second moment, operator-norm deviation from analytic moment, distance to population target, distance to intended P_B (each projector distance normalized bysqrt(2d)), principal cosines, eigengap diagnostics and projector residuals. More samples need not yield monotonic finite-prefix improvement. Analytic limits are not established by extrapolating four sample counts.

Also save training and separate256contrast-validation relative residual sum||D-P_hat D||² / sum||D||². These measure preservation of OBSERVED contrast, not correctness of semantic interpretation. For each aligned arm validation residual should be numerically zero with full-rank training despite nonzero intended-target distance. For independent arms finite residual is not an agent error rate. Keep target correctness, contrast fit and task outcome separate.

## Three actual retrieval/status methods

FULL=I, ORACLE=Q P_B Q^T, ESTIMATED=P_hat. All use same full noisy query, clean48candidate records and exact separate calibration arrays. Project actual arrays, normalize, rank by complex-inner-product modulus, decode actual returned top3 using circular centres fitted only on clean calibration entities. Column projector on row arrays is x@P.T, including complex matrices. Centres are circular means of valid normalized products for each status at relevant calibration entity/time.

Fixed policy: projected norm/product<=1e-10 undefined; missing any centre (no valid angles or resultant<=1e-10) => global calibration_unavailable ABSTAIN. Otherwise nearest circular angle; nearest-distance gap<=1e-10 => ambiguous_centre ABSTAIN. Valid single-item zero=>zero_product ABSTAIN. U is encoded source uncertainty; ABSTAIN is decoder availability/ambiguity. Concentration is not a truth probability. Stable canonical tie sort only for exact score ties; log boundary/within-set numeric differences instead of forcing equalization.

Actual returned-record metrics: evidence_recall/count-complete, joint_label_recall/complete, wrong_scope_count, encoded_U_recall, ABSTAIN count and each reason. Relevance requires both entity AND time, all3statuses relevant; wrong-scope label gets no credit. Separate oracle-relevant stance accuracy diagnostic and stored predictions. Gold entity/time/status only in metrics/diagnostic, never supplied as inference features. Save all-candidate products or scores/angles and decoded labels/reasons to enable independent raw-array replay (compact NPZ allowed), plus returned IDs/indices/predictions/reasons and per-query metrics in ledger.

Counts fixed:3seeds x5arms x4m x2r x2eval-eta x32queries=7680paired rows;3methods=23040method records;720method-condition aggregates. Underlying48eval entity/time claims and384base queryIDs with288base unique arrays as predecessor, not independent replications. FULL/ORACLE duplicated across20training settings and must match after pooling; reuse/control checks explicit. Training prefixes/arms likewise paired. No significance, confidence interval or benchmark claim.

## Prospective controls and execution

Check source archive/file/used-array hashes; copied inputs identical; latent/train/eval provenance; clean pair cancellation; arm-defined difference identities before Q; population-target symmetry/idempotence/rank/gap; normalized distance formula; Hermitian/idempotent estimates; actual projected raw product vs independent realA+iB; fixed exact count. Check FULL/ORACLE against unchanged predecessor controls (same raw inputs), allowing reported last-bit within-top3 ties; all metric differences retained. This is reproducibility/control evidence, not an independent dataset. Compare all rows rather than selecting successful seeds.

Root verifies reviewer-approved source/protocol hashes and freezes all existing design/source/review artifacts before run. Executable saves exact inputs and hashes BEFORE fitting/scoring; save fitted/projector/calibration controls before task scoring. Sole main run singleBLASthread timeout180s. Preserve initial source/logs. On failure preserve complete attempt before any diagnosed repair, and distinguish rerun; never tune grid to outcomes. No experiment prior to prospective approval; syntax/independent nonexperimental-seed fixtures allowed and documented.

Fresh independent saved-array auditor fixes sample before outcomes: first/last query of every condition (1440method records); all projectors/diagnostics/centres may be reconstructed. Separate reviewer audits all ledger metrics/aggregates and repetition/availability counts. No implementation imports. Disclose actual source inspection rather than claiming blindness. Original analytic critic checks population identities before outcomes and may review implications later. Report caveats/failures, preserve complete outputs, update mutable navigation/checkpoint only. Core/runtime/schema/queue-status unchanged unless separately justified. End at three completed cycles for user review; no automatic fourth cycle.
