# Interface, observation and evaluation contract

Client date: 5 November 2026, America/Chicago. Prospective requirements and manually reasoned examples, not passed tests or model results. LANGUAGE.md and STATE_EXECUTION.md define language/persistence semantics.

## 1. Discoverable action surface

Commands: `put`, `define`, `run`, `run-save`, `inspect`, `list`, `drop`, `help`. The host supplies `request_id` and `expected_world_snapshot` on every request; mutations use whole-snapshot CAS. The agent emits one bounded command, without mandatory rationale. Embedded source uses the documented R7RS-small Scheme subset; world publication/inspection APIs are distinguished from Scheme procedures.

Initial observations provide a compact deterministic card: reference revision, snapshot, command forms, current quota profile/remaining allowances, storage use, and first index page. State that `run` does not save, `run-save` publishes atomically only on success, exhaustion saves no VM, and dropping names need not reclaim retained bytes. Public capability instructions, language rules and limits are discoverable through `help`/`inspect`. Procedures lack ambient file/network/clock access.

Normal responses contain status, request ID, before/after snapshots, bounded result/error with location, charged/remaining resources, committed IDs/aliases and audit ID. Distinguish `COMPUTED`, `PUBLISHED`, guest failure and uncertain host commit. Mark truncated values explicitly with canonical byte length; no invisible result-publication handle is implied.

`list` supplies deterministic snapshot-bound pagination. Rows expose kind, name, revision, size, and procedure signature/direct dependencies. `inspect` supplies bounded data/source/dependency/receipt pages with revision/hash, offsets, byte counts and explicit truncation. Bound both items and bytes; one large artifact remains retrievable. Cursors bind snapshot/query/offset; reject malformed, expired or mismatched cursors rather than restarting silently. Concurrent alias changes cannot alter an existing traversal. Inspection consumes observation allowance without mutating guest state.

## 2. Quiet observations, audit and recovery

Guest world, compact response and host audit are separate. `run`, `inspect`, `list`, `help`, and failed actions can consume resources/add bounded audit events without changing the guest snapshot. Only successful publication/drop changes guest state. Audit growth or observer summaries are not constructions.

Default observations show outcomes/effects/resources. Bounded traces are inspectable on demand with explicit truncation. Retain exact commands/envelopes, resolved inputs/dependencies, snapshots, semantic/cost/reference versions, limits, charged work, outcome/commit certainty and response identity. Reserve audit capacity independently before admission, including request/capture/snapshot metadata and bounded terminal result/error. No silent pruning or guest eviction pays for receipts.

Pause between committed actions: stop admission, reconcile in-flight IDs, persist world/ledger/allowances, then reset context. Restoration preserves IDs, dependency pins, history and total budgets. Unknown commit requires retry/reconciliation of the original ID before new mutation. A stored successful checkpoint can continue; exhausted evaluator state cannot.

## 3. Onboarding and seeds

Common onboarding supplies only the neutral interface/reference/limits and persistence/error explanation. Assigned competence checks are labeled and end before open choice. No continuing goal curriculum, seed completion, project category or explanation gates world use.

No-seed snapshots exclude seed prompts/artifacts/aliases while sharing kernel, onboarding and budgets. Optional seeds record wording/data, provenance, timing, whether requested and added artifacts. Ignoring, revisiting, editing or leaving a seed is valid. Continuing seeds are a separate declared condition, not hidden rescue. Describe observable seed adoption and project continuation; do not infer curiosity from topic counts, fluent reports or silence.

## 4. Host acceptance matrix

Future executable requirements, not results. Freeze fixtures/versions/limits; compare tiny bounded expressions against an independently simple reference evaluator. Enumerate small ASTs/action sequences where practical. Preserve expected/actual records; acceptance failure blocks model testing and is not a model failure. Finite checks are not a proof.

| ID | Fixture/counterexample | Required result |
| --- | --- | --- |
| H01 | Valid command versus trailing expression, unknown command, malformed Unicode, oversized/deep bytes | Bounded parsing rejection before expensive work; no partial publication. |
| H02 | Wrong type/arity, unbound variable, duplicate parameters; malformed text draft versus executable definition | Source-local errors; ordinary draft allowed, invalid definition rejected. |
| H03 | Safe `if` branch versus error/loop in unselected branch; arguments with competing failures | Only selected branch runs; specified left-to-right error/cost. |
| H04 | Integer boundaries, division signs, Unicode supplementary/combining slice boundaries | Exact specified result/error; no wrap/coercion/platform indexing drift. |
| H05 | Rebind helper after publishing caller; self-recursion; unresolved/cyclic links | Pinned caller unchanged; correct own-revision recursion; invalid links atomic rejection. |
| H06 | Exactly enough versus one-short fuel, frame/allocation/integer/output limits; costly primitive with tiny fuel | Independent bounds enforced; primitives cannot bypass work accounting; no failed result artifact. |
| H07 | Tiny reference versus implementation; pinned deterministic replay | Same canonical values, errors, costs/effects; distinguish replay from ID-cache lookup. |
| H08 | Successful run/run-save; evaluation failure; stale snapshot/CAS conflict | COMPUTED versus PUBLISHED correct; failure changes no guest state. |
| H09 | Lost response/retry; ID reused with changed payload; faults around commit | One outcome/publication; conflict rejected; known abort versus unknown commit reconcilable. |
| H10 | Independently fill guest/audit/action/work/observation quotas; oversized receipt | Responsible quota explicit; no partial write, hidden reset, eviction or unlimited ledger. |
| H11 | Many entries, long source, duplicate-looking names, concurrent update, tampered cursor | Stable complete pages; canonical source reconstructs; invalid cursor rejected. |
| H12 | Inspect/list/help/error/pure run versus publication | Audit/observation changes never count as guest changes; allowances accurate. |
| H13 | Drop pinned revision's name, then recreate name | Old pins usable/charged; no false byte reclamation or historical retargeting. |
| H14 | Save/reload completed checkpoint versus exhaust before next checkpoint | Same pinned continuation as uninterrupted run; exhaustion saves nothing. |
| H15 | Pause during lost-response action, then restore | Original request reconciled; no duplicate commit, invented success or budget reset. |
| H16 | Seed/no-seed worlds; inspect capability rules; attempt ambient authority | Only declared seed delta; rules discoverable; no ambient access through data/names. |

## 5. Isolated model pilot

The latest diagnostic, `../padding-and-prediction-v1/REPORT.md`, retained 76 isolated generations. Commands depended on prompt construction; all 24 transition predictions were 8 despite integer-format compliance. Adaptive checks separated extraction, transformation and field selection; adapter contribution affected style/content. These narrow results neither measure Scheme usability nor establish general inability. Score format, extraction, command effects and correctness separately.

After host acceptance, freeze a disposable world, exact original 135M base/LoRA hashes, tokenizer/template, sampling, seeds, semantic versions and budgets. Keep input cap 8,096/output cap 96; no larger model is assumed. Measure card/response token costs. Favor short definitions/helpers, incremental ordinary text drafts and inspection over expecting long one-turn programs. Optional source blocks preserve exact command bytes; no rationale required. Never crop incomplete commands into validity. Do not alter primary world, weights, adapter or training data.

Assigned checks: discovery, literal storage, expression, named procedure, composition, feedback repair, pinned held-out reuse, checkpoint continuation after context reset, and deliberate exhaustion without inventing progress. Fresh contexts receive discovery plus retained world, not evaluator-written solutions. Then run a separate finite open-choice period with no compulsory construction. Compare optional-seed/no-seed snapshots; compare useful retained library/no library/matched-size irrelevant library under equal retrieval and total budgets, reporting setup costs. Syntax aids/quota changes are declared interventions.

Archive all raw generations, commands, receipts and failures without selective retries. Predeclare repeated matched seeds, scoring and infrastructure rerun rules. Report parse/admission validity, host/guest errors, held-out correctness, publications, discovery, feedback revisions, dependency reuse, checkpoint/reset continuity, idle visits and resource use separately. Explanations cannot substitute for effects, or valid syntax for correctness. Results may establish tested usability/library-assisted performance with fixed weights; they do not establish weight learning, intrinsic curiosity or general intelligence.

## 6. Complete expected transcripts for review

These are manually reasoned acceptance fixtures, not interpreter or model output. `S0`, `T1`, `Rtwice1`, and similar labels below stand for actual immutable snapshot/revision IDs returned by a future host; they are not an accepted identifier grammar or fabricated hash values. Each table row is one request/generation, never a multi-action model reply. Responses elide only the common receipt fields already required above; actual receipts retain them. The host injects a unique `request_id` and the row's expected snapshot. No rationale is submitted.

The host declares the shared fixture quotas in `constants.json`: command/depth/source/reachable-source, integer/frame/allocation, fuel/action/visit, output/page/observation, guest/audit/receipt reserve, action count and independent process deadline. No numerical production recommendation is adopted here. These examples require sufficient declared capacity; host tests must confirm exact costs. Model trials retain output cap 96 and measure every command with its tokenizer; oversized commands require short helpers/drafts, never hidden extra output. The exhaustion fixture explicitly overrides action fuel to zero.

**Construct, compose, and pin.** All aliases begin absent. Each successful publication advances the snapshot; pure computation leaves it unchanged.

| Request / expected snapshot | Exact command | Required result/effect |
| --- | --- | --- |
| c1 / S0 | `(define (twice x) (+ x x))` | `PUBLISHED`, `twice -> Rtwice1`, world S1. |
| c2 / S1 | `(define (four x) (twice (twice x)))` | `PUBLISHED`, `four -> Rfour1`, world S2; both calls pin Rtwice1. |
| c3 / S2 | `(run-save answer (four 3))` | `PUBLISHED`, answer value `12`, world S3; receipt lists Rfour1/Rtwice1. |
| c4 / S3 | `(define (twice x) (+ x 100))` | `PUBLISHED`, `twice -> Rtwice2`, world S4; Rtwice1 retained. |
| c5 / S4 | `(run (four 3))` | `COMPUTED`, value `12`, world S4; no result artifact. |

**Counterexample and guard repair.** This independent fixture begins at T0 with no aliases.

| Request / expected snapshot | Exact command | Required result/effect |
| --- | --- | --- |
| g1 / T0 | `(define (first xs) (car xs))` | `PUBLISHED`, first revision F1, world T1. |
| g2 / T1 | `(run-save found (first '()))` | `FAILED_EVALUATION`, empty-list selector diagnostic at `car`; world T1, `found` absent, audit retained. |
| g3 / T1 | `(define (first xs) (if (null? xs) (list "absent") (list "present" (car xs))))` | `PUBLISHED`, first revision F2, world T2. |
| g4 / T2 | `(run (first '()))` | `COMPUTED`, value `("absent")`; world T2. The unselected `car` does not run. |
| g5 / T2 | `(run (first '(7)))` | `COMPUTED`, value `("present" 7)`; world T2. |

**Explicit checkpoint, pinning, and paused recovery.** The state is `(remaining total)` for a finite countdown sum; this step is called only with positive remaining. The unconditional step deliberately keeps this fixture small. It is not an automatic resumable VM. `advance` pins the step revision when it is published.

| Request / expected snapshot | Exact command | Required result/effect |
| --- | --- | --- |
| p1 / U0 | `(define (step s) (list (- (car s) 1) (+ (car s) (car (cdr s)))))` | `PUBLISHED`, step P1, world U1. |
| p2 / U1 | `(define (advance s) (step s))` | `PUBLISHED`, advance A1 pins P1, world U2. |
| p3 / U2 | `(run-save checkpoint (advance '(2 0)))` | `PUBLISHED`, checkpoint C1 value `(1 2)`, world U3; receipt records A1/P1 and original input. |
| p4 / U3 | `(define (step s) s)` | `PUBLISHED`, step P2, world U4; A1 still pins P1. |
| pause / U4 | Host stops admission, saves world/ledger/allowances, resets only the model context, restores U4. | No guest mutation, no fuel/visit reset. New context receives discovery card. |
| p5 / U4 | `(inspect checkpoint)` | `OBSERVED`, C1 data `(1 2)` and its provenance A1/P1 are retrievable; world U4. |
| p6 / U4 | `(run-save checkpoint (advance checkpoint))` | `PUBLISHED`, C2 value `(0 3)`, world U5; A1 invokes P1, not P2. C1 remains immutable. |

At p6 the host captures checkpoint C1's data from U4 before evaluation; the program has no ambient world reads. The expected sum `3` matches uninterrupted two-step execution under A1/P1.

**Exhaustion is not a checkpoint.** Begin with U5 from the preceding fixture. For this request only, the host declares a fuel limit of zero, visible before submission; other limits remain the declared fixture profile. This tests the boundary without guessing an unimplemented transition count.

| Request / expected snapshot | Exact command | Required result/effect |
| --- | --- | --- |
| e1 / U5 | `(run-save checkpoint (advance '(3 0)))` | `FAILED_LIMIT`, fuel exhaustion before completing evaluation; world U5, alias checkpoint still C2, no C3 or staged result handle. A bounded failure audit record exists. |
| e2 / U5 | `(inspect checkpoint)` | With normal observation allowance: `OBSERVED`, checkpoint remains C2, value `(0 3)`; no saved mid-execution continuation. |

If e1 loses its transport response, retrying the identical request ID/envelope first retrieves or reconciles its outcome; it does not grant a fresh execution. A later run with more fuel is a new declared action from an explicit successful checkpoint or other chosen input, not a continuation of e1's VM. The exhausted computation establishes only incompleteness under that allowance.
