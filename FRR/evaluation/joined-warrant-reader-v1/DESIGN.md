# Cycle 1 prospective joined-warrant reader contact

Status: DRAFT_NOT_FROZEN. No readers dispatched. Root approval follows prospective scorer and reviewer inspection; any correction must preserve the original authored files first. Only `modules/verification-layer.md` and `evaluation/quality-preview-reader-v1/NEXT_CONTACT.md` informed this preparation. Numerical fixtures here were newly authored; prior numerical examples were not consulted.

The narrow question is whether optional joined-warrant guidance changes fresh readers' fidelity about supplied, absent, conflicting, or inapplicable premises and the full acceptance target, relative to ordinary task diligence. This is an authored development contact, not a whole-framework FRR test, held-out confirmation, or durable habit/efficacy claim. All evidence is delivered. No acquisition choice, query planning, real sensor trust, or empirical calibration validation is tested.

## Cases and decisions

`cases.json` contains eight concise fictional prose packets in four mirrored pairs. Within each pair, numerical evidence and numerical thresholds remain identical. Only the relevant assignment premise, calibration key, assignment consistency, or acceptance quantity changes. Pair metadata and filenames are never shown to participants. Units, dates, complete populations, authority rules, bias sign, and applicability are stipulated where needed.

1. A piece assignment supplied in acquisition versus genuinely absent from the whole packet.
2. An exact lot/date/unit calibration join versus a date-mismatched certificate with no transfer relation.
3. Consistent equally authoritative assignment records versus conflicting equally authoritative records without priority; at least one record is correct.
4. The same complete-population mean certificate used for mean acceptance versus maximum acceptance.

The common response contract defines RELEASE as compliance in every compatible state, HOLD as violation in every compatible state, and UNRESOLVED as both possibilities remaining. Thus HOLD is a justified negative task result rather than a procedural synonym for uncertainty. The set has two warranted RELEASE cases, two warranted HOLD cases, and four unresolved cases. Unresolved cases are designed to retain actual compliant and violating witnesses; the independent key must check these before freeze. No case embeds a verdict or worked explanatory conclusion.

## Instruction arms

Ordinary task diligence (exact text):

> Read the task and evidence carefully. Identify the requested decision, perform relevant calculations, and distinguish established facts from uncertainty. Check that your answer addresses the stated scope and acceptance rule. Clearly explain your decision using the supplied records, state any consequential limitations, and give a useful next check when needed.

Optional joined-warrant check (exact text):

> Read the task and evidence carefully. Optionally check joined warrants: identify required premises, combine applicable records using exact keys, and separate supplied premises from absent or conflicting ones. Check whether evidence covers the full acceptance target. Explain your decision, state consequential limitations, and give a useful next check when needed.

Both texts contain exactly 50 whitespace-separated words, verified by `str.split()`. They are not matched for model tokens, reasoning effort, or compute. The joined arm is optional and scoped; neither arm names FRR. All remaining instructions and case evidence are identical for the two readers assigned the same case. Numerical evidence is identical between mirrored cases, but their relevant premise/task change necessarily changes prose length.

## Sixteen fresh one-turn contexts

Each case is delivered once per arm to a separate fresh context: 8 cases × 2 arms = 16 one-turn readers. Readers receive no conversation history, tools for analysis, peers, key, scorer, arm names, pair labels, or other cases. The delivery exception is exactly one read-only exec call to read only the assigned neutral `prompts/Rxx.txt`. After that read, the reader returns JSON directly with no further tools, peer contact, or file writes. Reader access restrictions are instructional in the shared workspace, not technical isolation. Both arms use the same delivery mechanism and tool availability; actual compliance and tool/reader costs must be recorded.

Root will render only after prospective case/key review and approval. `render.py --output <new-directory> --seed 20261027 --root-approved` deterministically shuffles all case/arm combinations and writes sixteen neutral prompt files plus a private assignment manifest with hashes. It refuses an existing output directory. Rendering does not dispatch readers. The seed and algorithm are fixed prospectively; root should not search seeds or replace readers on the basis of their answers. The assignment manifest, prompts, and arm associations remain unavailable to scorers/reviewers until masked scoring deposits are complete. Case/key review itself is allowed prospectively without rendered assignments.

The common preamble fixes action semantics and asks for one JSON object containing `action`, `bound_or_value`, `satisfied_premises`, `missing_or_conflicting_premises`, `evidence_ids`, `next_check`, and `rationale` (at most 180 whitespace-separated words). Numeric answers must identify their quantity and unit; no compulsory speculative next measurement is imposed when the packet resolves the task.

## Prospective review and limits

The independent scorer owns the key and scoring specification, including numerical acceptance sets, supplied/missing premise attribution, decision correctness, and useful next-check scope. Review must distinguish a correct action with a false missing-premise explanation from a fully supported response. Scoring should also distinguish false release from needless withholding and avoid requiring the optional arm's wording. Root controls freeze, masked dispatch, scoring deposits, and later unmasking.

Save the initial `DESIGN.md`, `cases.json`, and `render.py` bytes under `originals/` before any prospective correction; disclose the reason and exact changes. Do not silently relabel cases after contact. The author has not rendered assignments, dispatched readers, or inspected reader outputs. With only one fresh reader per case/arm, any differences are descriptive and confounded with reader variation. Word matching does not establish token/compute matching. Fictional accepted premises establish conditional task reasoning only; they do not authenticate real records or demonstrate broader reasoning improvement.

Prospective correction before reader contact: root requested decisive-action balance. Initial bytes of all three author-owned files are preserved in `originals/`. Case05 now consistently assigns T to violet and U to ivory; case06 uses that as E3 and the opposite as E4. No numerical summaries changed. This changes case05 from RELEASE to HOLD and leaves case06 unresolved. The initial explicit absent-assignment and alternative-record consequence language created strong cues. A second root-requested prospective refinement removed those inline consequences: case02 E2 now contains only readings; pair3 E1 retains equal authority, at least one correct, no priority, and no independent truth guarantee. Before-refinement bytes are preserved in `originals/before-cue-refinement/`. The task remains authored premise discrimination with possible ceiling effects, not a naturalistic or held-out join-discovery test.
