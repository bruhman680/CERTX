# Pass 2: history content, response form, and position

Read 14 November 2026. Three primary paper contacts, selected after reading both Pass 1 reports. This scout changes no garden state, prompt, decoder, weights, or execution rules. No model, dataset, package, or external code was downloaded or run. The continuing garden remains paused at 1580. Source evidence motivates detached controls; it does not diagnose the local model's mechanism.

## The three contacts

**Min et al., Rethinking the Role of Demonstrations, arXiv v2, 20 October 2022.** Sections 3–5 separate correct input–label mappings from input distribution, label space and example pairing. The paper tests classification/multiple-choice with 774M–175B bodies, not open Python interaction. In §5.1, replacing inputs with out-of-distribution text while preserving labels/format sometimes performs worse than removing demonstrations. Direct and channel formulations also differ in sensitivity to label replacement. Thus a filler retaining turn structure is a useful control, but calling it neutral does not establish that it has no effect. The [official repository README](https://github.com/Alrope123/rethinking-demonstrations) exposes declared variants, seeds and templates; its code was not audited or run. Read depth: [paper](https://arxiv.org/html/2202.12837v2) methods §3, ablations §4–5 and selected discussion; arXiv metadata and conference PDF beginning cross-checked. Contrary evidence matters: examples can help despite incorrect mappings, so repeated history is not automatically harmful.

**Zhao et al., Calibrate Before Use, ICML 2021 / arXiv v2, 10 June 2021.** Sections 2–4 vary examples, order and format separately, measuring answer repetition and majority/recency effects. Section 5 estimates a context-dependent answer preference using content-free inputs. This is an output adjustment, explicitly distinguished from aligning confidence with empirical accuracy. For generation, their correction concerns only the first output token; the tasks and 1.5B–175B bodies differ substantially from our 135M file interaction. The [primary conference PDF](https://proceedings.mlr.press/v139/zhao21c/zhao21c.pdf) was read through methods and §3–5, not its full appendix or implementation. Extraction: measure repetition and response form alongside task success, and vary ordering separately from content. It does not establish that output recalibration repairs our code, or that arbitrary open-world output should have a uniform distribution. More examples can hurt in their experiments; larger context is not necessarily more useful evidence.

**Liu et al., Lost in the Middle, arXiv v3, 20 November 2023.** A focused second reading covered §2.1, §3.1–3.2, §4.2 and token-count appendix F, rather than repeating the abstract. Their synthetic task uses random UUID key–value pairs to reduce semantic confounds, moving the relevant pair while varying distractor count. Section 3.2 reports a response-mode wrinkle: LongChat can produce retrieval code where a value was requested. Section 4.2 places the query both before and after the data, improving synthetic retrieval but slightly worsening most tested QA positions. Token counts differ across model/tokenizer settings. The [paper](https://arxiv.org/html/2307.03172v3) therefore supports recording actual token placement and separating response mode from correct content. Its in-context data retrieval is different from choosing to access a file outside the prompt; its results cannot establish our model's attention pattern or justify inserting repeated task reminders into the continuing garden.

## Strongest proposed detached comparison

The local result remains a filename-versus-content mistake in one inherited context. The strongest next experiment is the same task and file worlds under different histories. This proposal is our inference, not a reproduction of the three papers.

| Condition | Keep fixed | Deliberate difference | What it can address |
| --- | --- | --- | --- |
| Inherited | Body/revision, world, task, mechanics, decoder, output cap | Eight real repeated reply/receipt pairs | Baseline matching the failed contact |
| Fresh | Same fixed elements | Remove those pairs | Bundled effect of history, length and placement |
| Length-matched declared filler | Same fixed elements and task token position as closely as possible | Replace history content, retaining role/message structure | Whether equal-length alternative content behaves differently |

A filler should not contain target nonces, example file-reading solutions, fresh instructions, or the old repeated network program. Preserve exact role boundaries and receipt field names where the comparison requires them. Record total token count, task start/end positions and differences that cannot be matched. Matching character length is insufficient. Prefer more than one independently specified filler if results warrant expansion: unrelated prose and synthetic tokens are different interventions, not interchangeable blank space.

Do not erase the original failed histories. Save each input and its provenance externally, so a later audit can tell what changed. Retain the hidden A/B nonce worlds with identical model-visible input within each condition; counterbalance filenames and values in replication. A supplied authentic read receipt is a separate availability control, not evidence of model-chosen file access. First-turn comparisons are especially interpretable; once replies and genuine receipts diverge, later turns measure complete interaction trajectories rather than identical contexts.

Readouts should distinguish complete executable cell, actual file-access attempt, value returned by execution, value used in answer, incorrect parsing of the filename, and repetition of prior text. Correct answer from supplied text and correct answer after an observed file read are different outcomes. Empty or malformed cells and handled errors remain observations, not obstacles to suppress.

## What outcomes would and would not mean

Fresh success with inherited failure would establish a context-condition dependence for the tested case. It would leave content, length, task position and role structure bundled. If matched fillers also succeed, that strengthens a history-content explanation relative to simple length; it still does not locate an internal mechanism. If all fail, capability, task interpretation, interface and elicitation remain live alternatives. If one filler succeeds and another fails, the control itself is influential and needs characterization.

If valid code appears without reading the file, response-form improvement has occurred without task completion. If access occurs but the answer is wrong, acquisition and subsequent use have separated. These distinctions prevent a small surface improvement from being narrated as general reasoning growth.

No source in this pass warrants changing the main world or declaring a context repair. A rolling window, added demonstrations, a repeated query, calibration and sampling changes would each be separately declared assistance. Current strongest confidence is in the need for the comparison, not its outcome.

## Pass 3 challenge handoff

Challenge the label “neutral history,” the assumption that fresh success proves memory damage, and the assumption that copying old code is equivalent to not perceiving the task. Seek controls that would reverse those interpretations. In particular, distinguish answer-token priors from full-program generation, and prompt-contained retrieval from external acquisition. Preserve contrary results rather than selecting the source condition that sounds most helpful.

Access log and version scope are recorded in SOURCES.json. One speculative HTML URL for Min v4 returned 404; metadata established that v2 is the actual latest listed version, and v2 HTML succeeded. No denied-access source was used as evidence.
