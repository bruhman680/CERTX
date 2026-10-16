# HG1: operations, phase labels and the next reader

Status: **protocol draft; not launched or preregistered as final**. Queue entries HPGM-01 and HPGM-03 share this proposed run. Required task packets, answer keys and measured-cost execution setup are not yet prepared. The draft is a concrete starting point, not proof that a behavioral experiment is runnable today.

Question: do functional checkpoints help at a declared resource cost, and does expressing the same operations as HPGM phases change that effect? Does their closing record help a fresh reader continue?

## Comparison

All arms share competent task instructions: fulfill the request accurately, use supplied evidence, preserve consequential uncertainty, and avoid invented results. All receive the same case evidence. The responding model must not receive scoring keys or condition-specific desired conclusions. Use the same frozen model/settings/tool access and two actor calls per case/replicate in all arms.

1. **Ordinary:** competent task execution with a neutral finalize prompt on the second call.
2. **Generic continuation:** same opportunity and caps, but explicitly continue working before finalizing; no functional gate checklist.
3. **Functional checkpoints:** first call establishes purpose/evidence, identifies relevant alternatives and makes a candidate artifact. Second call checks its evidence, revises warranted errors and prepares a continuation record.
4. **HPGM labels:** identical functional instructions and access as arm 3, with COUPLE/OBSERVE/ORIENT/PLAY/PRACTICE/DREAM headings attached. Freeze exact arm text before launch. A label effect must not be attributed to extra operations or evidence.

This is a pilot configuration; it does not establish necessity of six stages, an optimal ordering or timing law. Prompt lengths may differ: report actual input/output tokens where available, rather than calling equal output caps equal compute. If measurements cannot be obtained, keep that cost dimension unknown and narrow any claim accordingly.

## Proposed task and call budget

Prepare eight cases in four separately authored dependency families, two variants per family. Reserve two complete families for development and two for later confirmation; freeze allocation and hashes before inspecting actor outputs. Existing six-case recovery-pilot cases may train the scorer or exercise plumbing but must not be relabeled independent confirmation. Public repository visibility and shared workspace access limit blinding; document assigned access and any actual isolation rather than promise it.

For development: four cases x four arms x two replicates = 32 writer trajectories, with two actor calls each and one fresh reader each: **96 model completions maximum**, excluding any separately declared adjudication calls. Proposed output caps: 768 tokens on each actor call and 512 on the reader. These are operational caps, not cognitive constants. Record actual settings and realized consumption. Do not begin if the host cannot track the declared call budget. Confirmation is a separate later stage with its own recorded launch decision and budget; saving this draft does not launch either stage.

Randomize condition order and counterbalance cases. Choose and freeze concrete task families, keys and arm text before launch. Useful case features include obsolete corrections, a missing execution receipt, insufficient evidence, and a justified later update, but the author must not simply rewrite old answer-bearing cases. Record author/model/source genealogy; a fresh context alone does not prove independent authorship.

## Reader contact

Require all arms to leave the same maximum-length final continuation artifact, proposed cap 180 words. A fresh reader receives that artifact and a common continuation request, without the author's other outputs or arm label. Common reader guidance does not mention HPGM. Keep any identifying phase headings out of the reader packet through a frozen content-preserving normalization rule, or report the reader as potentially unblinded. Preserve both original and normalized artifacts.

Measure recoverable corrections, proper status/version use, missing-evidence handling, appropriate authorized action, and unsupported additions. State what the reader could actually access. A written handoff is not successful until its use is tested.

## Scoring and forecasts

Use source-grounded correctness checks wherever possible; retain raw answers and exact evidence available to actors. Blind adjudicators to arm labels where feasible. Preserve evaluator mistakes and version any repair instead of overwriting the original review. Predeclare failure coding and record disagreements.

Primary exploratory outcomes: material factual/status errors and correct task completion, reported separately for writers and readers. Secondary outcomes: source fidelity, warranted revision, unsupported changes, length and available cost. No aggregate score may hide a truthfulness regression. With four development cases and two replicates, this is a small correlated pilot, not a population efficacy estimate.

If collecting confidence, define the event explicitly (for example, correctness of the final binary claim under the task's fixed key), elicit one probability before revealing its outcome, and retain every forecast and label. Use [forecast_scores.py](../../tools/forecast_scores.py) for descriptive Brier loss and exact-forecast-group decomposition. Do not score missing forecasts as .5 or silently omit failures: record them separately with denominators. This sample is too small for a strong population-calibration conclusion or a reconstruction of the post's 22% claim.

## Predictions, promotion and prerequisites

Candidate predictions: functional checkpoints may reduce material errors or improve handoff use relative to generic continuation; phase labels may add nothing when operations match. Equal or worse results are admissible. Final primary comparisons, any practical effect threshold and all prompt text must be frozen before launch. Development findings may inform a later protocol, but used families then remain development rather than untouched confirmation.

Before launch: finish independent task packets and keys; freeze arm and reader templates; verify normalization does not erase meaningful content; declare exact model/settings/cost access and stopping rules; save a launch manifest and commit; only then collect behavioral outputs. Follow the adopted bounded loop and retain failed trials. No actual-agent benefit, phase constant or physical mechanism is assumed.
