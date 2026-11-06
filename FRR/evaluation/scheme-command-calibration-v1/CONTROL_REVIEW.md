# Independent control review: Scheme command calibration

6 November 2026. Design review only; no model calls, model/runtime changes, primary-world access or old-study changes. Sources: `computational-world-portability-v1/REPORT.md` and `pilot/PLAN.json`. This review is a recommendation, not a claim that the following matrix has already been preregistered or run.

The previous result is 0/10 accepted model actions under one broad card, two fixed seeds and fresh contexts; 0/8 requested outcomes, with two free-choice turns unscored. It establishes an observed interface failure in that fixture. Host validation and model action success are separate. The repair prompt summarized a genuine setup failure but did not test iterative learning from the model's own execution feedback.

## Suggested compact fixed matrix

Freeze complete prompts, token IDs, seeds, setup commands, expected outcomes, dispatcher/version pins, raw-output treatment, branch construction, feedback projection and analysis tables before generation. Reuse the deployed canonical adapter for all main cells. Use two new fixed seeds, paired across conditions; do not choose seeds after seeing output. Fresh disposable worlds and contexts unless the row explicitly specifies a second turn. Keep generation settings/output budget identical to the pilot unless a changed setting is itself declared.

| Block | Cells | Calls | Identifiable contrast |
|---|---|---:|---|
| A: literal command emission | 4 literal targets × 2 card conditions × 2 seeds | 16 | Narrow copying prompt versus broad card, with target information held fixed |
| B: small variation | 2 arithmetic targets × the same 2 card conditions × 2 seeds | 8 | Emission for a requested expression without its complete answer supplied |
| C: feedback fork | 2 arithmetic targets × 2 seeds; one shared first reply, then 2 continuation branches | 12 | Actual execution feedback versus another attempt with the same prior reply and equal attempt budget |
| Optional D: adapter reference | 2 targets × 2 card conditions × 2 seeds, adapter scale zero | 8 | Local dependence on adapter presence in the fixed A subset |

A–C total 36 calls, including failed and successful first turns. D adds 8; omit it unless adapter dependence is a specific predeclared question. A smaller budget may use two A targets (8 calls), but then it cannot support conclusions about definition/retrieval interfaces. No unplanned success-dependent expansion or selective reruns. Declare infrastructure-failure handling separately from ordinary invalid output.

**A targets:** `(run (+ 2 3))`, `(run (+ 4 7))`, `(define (double x) (+ x x))`, `(page seed value "" 32)`. Supply the same complete literal target to both card conditions, verbatim, with the same final instruction such as “Copy the command below exactly. Reply with only that command.” The narrow condition contains only the minimal output rule and literal; the broad condition additionally contains the original card. Hold literal position, task text, chat roles/template and output budget fixed. Seed setup for `page` must be identical within pairs and recorded. Different seeds do not create independent task coverage.

The A contrast identifies the effect of the whole added broad-card context under supplied-target copying. Length, distractor commands and instruction content remain bundled; it cannot identify which caused any difference. Do not manufacture arbitrary filler merely to call this a pure syntax-card effect. Comparing a supplied exact answer against broad-card synthesis would instead conflate answer availability, task demands and context.

**B targets:** ask for `2 + 3` and `4 + 7` using a run command, without presenting the requested complete command. Give both conditions the same non-target example, e.g. `(run (+ 1 1))`; only the broad condition adds the broad card. Record the shared example as assistance. This is near variation, not held-out Scheme competence. A versus B is descriptive because task instruction and answer availability change together. Use the existing guarded-list case only as a separately declared harder extension; it is not needed to resolve the smallest expression interface.

**C construction:** use one fixed minimal prompt/task family without a complete answer, with the same non-target example as B. Save each first raw generation, dispatch it once, then fork its transcript and exact post-dispatch world into two isolated continuations. Both branches receive the same previous model reply, same task restatement and same “Reply with one command” instruction. Feedback branch receives a fixed projection of that actual receipt: status, error code/message or actual value, without a suggested repair or correct command. Practice branch receives a neutral “Try the requested command again” message without the receipt. Use equal output budgets and fixed second-turn seeds across branches. Include all first turns, even successes; report repair among initially failed pairs separately and report success retention among initially successful pairs. Never select only convenient error types after generation.

This controls for the extra attempt and exposure to the model's earlier text. Feedback length and diagnostic information still differ by design, so call the effect “receipt feedback versus practice,” not a mechanism-specific learning effect. Save feedback byte/token counts. Padding with meaningless text creates a new intervention and is unnecessary. A third branch is needed only if claiming a distinct effect of feedback format versus information; no such claim is justified here. Host setup errors supplied before a first reply would test informed repair, not this feedback contrast.

## Exact scoring and records

Report separate binary outcomes per model reply, with raw strings and counts by target/seed/condition:

1. **Literal match:** entire decoded reply after the predeclared outer-whitespace strip equals the supplied target. No parenthesis completion, fence removal, extraction or alternate candidate. Report any additional normalization only as a separate descriptive metric.
2. **Accepted execution:** actual dispatcher receipt shows success for the entire stripped reply. Parsing alone is insufficient; record parser/command/evaluation failure separately. A read or pure run need not change the guest snapshot to succeed.
3. **Task success:** actual value equals the requested integer for arithmetic; definition is published and the predeclared host probe `(run (double 3))` returns integer 6; retrieval is the requested first `value` page of the seeded artifact, not merely any successful command. Literal mismatch may still be accepted and task-correct. No task outcome is inferred from prose.
4. **Feedback change:** paired second-turn execution/task success, with first-turn outcome, error category and first-to-second transitions. Report feedback/practice discordant pair counts. Do not pool first and second turns into an apparent independent success rate.

For definitions, host probes must have separate IDs and labels and cannot count as model actions. Record raw generation before dispatch; prompt and input IDs, seed/settings, stop reason/token counts, receipt, before/after guest snapshots and audit changes. Preserve every reply. Request retries for record checks are not additional independent model attempts. Keep model/adapter hashes fixed, check unchanged tensors using the existing safeguards, and do not train.

## Adapter reference and interpretation limits

Scale zero is useful only after verifying the existing runtime supports it without writing weights, and freezing identical prompts/token IDs/settings in the same A subset. It is a reference contrast on this task distribution, not evidence of adapter damage in general. Declare the exact scale mechanism; a disabled-adapter context is not silently interchangeable with a scale-zero forward pass. No comparison to a newly downloaded or differently prompted base model. If unsupported without runtime changes, defer D rather than changing this review's scope.

Copying success would establish a lower bound on command emission with the answer supplied. It would not establish Scheme reasoning, constructive free play, autonomous persistence or broad usability. Failure on every A cell would justify inspecting tokenization/template/stop configuration and command emission before a longer season; it would not identify which component failed or show that the model can never use Scheme. Variation or feedback success remains local to the declared commands, prompts and seeds. Tiny paired counts support a diagnostic description, not a stable population estimate or a broad ranking of models/adapters.
