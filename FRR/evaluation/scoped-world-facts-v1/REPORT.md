# Scoped world facts: the wording changed, action was not elicited

15 November 2026. Six actual cached SmolLM2-135M-Instruct calls completed in two detached three-reply trajectories. Main remains bounded-main-continuation-v1 at entry **1630, paused**, with its supported files, records and ACTIVE pointer unchanged. Neither experimental branch was promoted. No parameter updates, paid inference endpoint, new goals, rewards, demonstrations or correction messages were used.

## Question and frozen comparison

The earlier compact-FRR contact included a claim that a read-only supplied runtime made the notebook unwritable. That raised a local scope question: could the same explicit writable-storage/read-only-runtime facts be expressed differently without adding behavioral guidance? This is a new matched comparison, not a retrospective proof of the cause of that earlier claim.

Both branches started from the actual main1630 supported checkpoint. The sole common initialization change replaced WORLD_RULES.txt with identical accurate mechanics; all other source files were retained. Both received an empty system message, their respective mechanical user prefix, and the same complete initial directory-metadata packet. This packet contains names, types and sizes, not file contents. Legacy notebooks remain physically present but were not automatically inserted into these fresh conversations.

The differing opening spans were:

Prose: `/world is writable storage. The supplied Python 3 and /bin/sh runtime is read-only.`

JSON: `{"world":{"path":"/world","storage":"writable"},"supplied_runtime":{"programs":["Python 3","/bin/sh"],"access":"read-only"}}`

The remaining mechanical suffix, initial snapshot, action parser, resource limits, cached body, greedy256 decoder and full branch-history policy were matched. Later user messages contained only actual runtime feedback in the common wrapper. Successful automatic notebook storage is silent, so all six actual messages were `{"runtime_feedback":null}`. Post-reply directory packets were preserved externally and never selected for model input.

The intervention changes syntax, labels, wording, length and token positions together. JSON begins18 tokens longer. It is not a pure manipulation of semantic scope, and neither encoding is a neutral or universally superior control. No FRR was supplied in either arm; this study cannot estimate FRR benefit.

## Actual results

| Observation | Prose | JSON |
|---|---:|---:|
| Actual model calls | 3 | 3 |
| Input tokens by reply | 314, 588, 862 | 332, 606, 880 |
| Output tokens by reply | 256, 256, 256 | 256, 256, 256 |
| Unique input-token sequences | 3 | 3 |
| Unique output-token sequences | 1 | 1 |
| Complete executable cells | 0 | 0 |
| Incomplete executable fences | 0 | 0 |
| Model-originated executed programs | 0 | 0 |
| Successful automatic note appends | 3 | 3 |
| Literal note-byte growth | 2778 | 3390 |

Every reply hit the declared generation cap. Each arm's output token sequence was exactly repeated across its three distinct inputs, while the two arms' outputs differed from each other. This is output repetition under growing histories, not an identical-input experiment and not a proof of a permanent attractor. File states continued to change through automatic note storage. Three path-dependent replies are not three independent replications.

The prose reply begins, “The provided Python 3 and /bin/sh runtime is read-only,” then substantially repeats the persistence and cell mechanics and part of the initial snapshot. It omits the opening writable-storage assertion. Omission alone is not a contradictory permission claim. Its copied initial metadata is not evidence that it acquired current file contents or noticed later note growth.

The JSON reply begins, “The provided code snippet demonstrates how to create a notebook file in Python,” names `os.path.getsize()`, and repeatedly describes opening/closing a file. No such program was supplied as an executable snippet or emitted as a complete cell. These are unsupported descriptions, not operation receipts. No actual program, file read, Python API invocation or attempted tool action occurred.

Neither trace clearly repeats the earlier notebook-is-unwritable claim. That does **not** establish repaired scope understanding: the conditions, context and trajectories differ, and no permission-dependent action tests the distinction. Correct recitation would also be insufficient. No action error or subsequent repair/reuse opportunity was elicited; these are not measured zero abilities.

## Verification and provenance

The driver reuses the previously checked live-sensing kernel with explicitly recorded configuration: arms `prose/json`, three replies each, neither selecting the kernel's `live` observation path. The inherited audit's planned-call display is normalized from8 to the declared6 in the wrapper; actual counts are computed from immutable raw/effect records and are not altered. Exact preparation, inputs, tokens, source pins, model digest, snapshots, effects and receipt chains are retained under run/.

Preflight verified identical prepared world IDs and initial packets and tokenized each actual input. Static driver review found no blocking compatibility issue. After launch, an additional frozen-document hash check passed; its timing is explicitly recorded and it is not presented as a pre-inference gate. Operative source files and the design-freeze document were already pinned before generation. Resource monitoring begins after model loading, so it does not measure a whole-process loading peak. These limitations remain in review/DRIVER_REVIEW.md.

The completed run audit and an additional artifact audit passed: all six inputs/outputs tokenize and decode as saved, exact parser results match outputs, effects match the world ledger, receipts match feedback, supported stores verify, weights remain unchanged, and the main/source inventories and ACTIVE pointer match their saved before-state. No PENDING or owned RUN.lock remains. The single-attempt runner must not be reset to replay this study.

## Source weave and what it changes in our understanding

Targeted scout: [ScoNe](https://aclanthology.org/2023.acl-short.154.pdf) motivates checking semantic scope rather than global fluency; [IHEval](https://aclanthology.org/2025.naacl-long.425.pdf) motivates matching roles and wording force; [An Incomplete Loop, v4](https://arxiv.org/html/2404.03028v4) separates plausible rule description from successful use. These are methodological contacts in other settings, not reproduced evidence about this135M world. Read depth and version boundaries are in scout/SOURCES.json.

Body scout: [SmolLM2, §6](https://arxiv.org/html/2502.02737v1) says smaller-model instruction-tuning data excluded complex examples such as function calling. This narrows the assumption that a pretrained text model has been trained for this particular action interface. It does not prove inability: our earlier prompted file-read success remains a counterexample. [TinyStories](https://arxiv.org/html/2305.07759v2) shows why small-model competence is distribution- and evaluation-dependent; it provides no ambient-agency score, age or IQ for this body. Neither source was reproduced. See body-scout/.

FRR use in the research process: preserve the user's open-world intent; separate inherited capability, actual exposure, emitted artifact, operational consequence and interpretation; weave historical positive witnesses against current quiet outcomes; leave multiple mechanisms alive. The current observation is compatible with documentation-continuation habits, absent task pressure, format familiarity, action-channel friction or limited capability. This contact does not choose among those internal explanations.

## Strongest next direction

Keep the main intact. The next clean experimental question is the originally requested FRR exposure under one fixed, explicit interface: a new matched no-FRR/compact-FRR pair using the same scoped-prose initial-only world. Choose this interface for continuity and explicitness, not because prose won. Preserve the full FRR reference and label the compact adaptation accurately. Continue distinguishing text change from action and consequence; quiet results remain publishable observations, not grounds for coaching the inhabitant.

In parallel, an observer-only coupling map can inventory the routes from model output to world effect and from effect to later input, using existing positive and negative witnesses. Alternative actuators or autonomous world ticks remain separate designs, not silent fixes. Longer blocks, body changes and training require their own declared conditions. No next calls are scheduled by this report.

Garden view: changing the sign on the gate changed the story written beside it. Neither seed walked through the gate in these six moments. The useful discovery is the distinction between the sign, the telling, the doorway and an actual footprint. We have sharper labels for those layers; we have not yet grown evidence that one label produces better exploration.
