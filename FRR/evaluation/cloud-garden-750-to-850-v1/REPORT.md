# Continuous garden: entries 751–850, notebook and action separated

7 November 2026, America/Chicago. Completed the authorized 100-entry block. Ten integrity checks passed, every ten entries from 760 through 850; five reports cover twenty entries each. The phase is paused at **850**, with no scheduled continuation. An independent final verification passed. The prior 750 entries and all original environment files remain unchanged.

## What changed, and what continued

This is a versioned continuation of the same logical garden, with parent entry 750, not a new season whose diagnostic observations were substituted into its history. FRR/ACTIVE_GARDEN_PHASE.json identifies the active phase and current state. Old storage remains frozen at 750 as the lineage parent; this phase stores entries 751–850. All earlier model replies were carried into an accessible prior_replies.jsonl file; older researcher prompts and charters were not re-promoted as current instructions. Original observer records remain externally retained.

The model's default output is notebook writing. Writing can remain unfinished, code-shaped, uncertain or unorganized; no approval or semantic rejection is applied. Only a whole-reply JSON object with exactly action="shell" and a source string enters the shell. This is an action interface, not evidence that we can infer the model's private intention. Code written in the notebook is not silently promoted into a program. The model may use actions to modify its own notebook and other world files; external raw records cannot be rewritten by those edits.

The world is a persistent /world filesystem with shell and Python. The original three historical eight-state transition matrices and their indexing laws are available as files. No solution, grouping, task score, compulsory objective, FRR behavioral recipe, or reward for tool use was supplied. Our evaluation and checkpoint records remained outside the guest mounts. Actual action or notebook-storage errors would be returned; researcher approval is not a continuation gate.

This phase used cached SmolLM2-135M-Instruct without the added canonical YES/NO/WITHHOLD adapter. The old adapter and its history remain preserved. Removing its attachment changes the effective model condition; it does not erase old records or the base model's inherited knowledge. No training or weight updates occurred. Temperature .8, top-p .9, 96-token output limit, 8096-token input boundary, fresh KV per generation and two CPU threads were used. Recent context comprises up to twelve current-phase replies with actual environmental consequences. The longer record is available through files if the model uses the interface to retrieve it. The short recent-context window is replayed from externally retained raw replies, not reread from the mutable notebook: deleting a notebook passage would not erase that short replay window. This is an explicit memory/presentation condition, not unrestricted control over every future input.

## Preflight and independent review

The initial shell-every-reply prototype did not match the user's notebook intention. Its three diagnostic errors remain historical evidence; they were not counted as garden entries. Notebook/action separation was tested separately and then connected here.

The first attempts to attach actions to a size-limited tmpfs failed. Failed test logs are retained. An independent reviewer also identified a real Python startup-hook hazard and checkpoint/validation edge cases. Those led to the persistent trusted runtime, isolated notebook appending, read-only system/device mounts, disabled nested user namespaces, stronger content-addressed checkpoints, FIFO/hardlink handling and fuller hash/chain checks. See REVIEW_AND_LIMITS.md for the actual review scope and unresolved limits.

Eighteen host tests passed. A strengthened Python-hook regression included a positive control showing that ordinary Python could execute the planted hook, then verified that notebook appending could not. Five deliberate journal corruptions in a disposable checkpoint copy were all detected. These fixtures were not imported into the live world and did not become model achievements.

Four isolated model interface probes compared full and concise descriptions at two paired seeds. All four returned notebook text rather than an executable action envelope; none created the requested probe file. They did not establish that either description gives usable action access to this model. The probes were excluded from the 100-entry history. Their lack of success was not made a behavioral gate for the authorized free-writing continuation.

## Observed block

| Through entry | Notebook replies | Shell actions | Notebook storage faults | EOS | Token cap | Distinct texts |
| --- | --- | --- | --- | --- | --- | --- |
| 770 | 20 | 0 | 0 | 2 | 18 | 20 |
| 790 | 20 | 0 | 0 | 2 | 18 | 20 |
| 810 | 20 | 0 | 0 | 4 | 16 | 20 |
| 830 | 20 | 0 | 0 | 1 | 19 | 20 |
| 850 | 20 | 0 | 0 | 2 | 18 | 20 |

Across the block: host kinds {"notebook": 100}; stops {"token_limit": 89, "eos": 11}; **100 distinct texts**; longest adjacent identical run **1**. There were 26 replies containing Markdown code fences. Those are surface text counts, not measures of insight, useful novelty or internal reasoning.

The model produced writing that includes assistant-like prose, programming fragments and restatements or transformations of supplied context. Notebook writing was retained as writing. No shell-mediated file retrieval or program construction is evidenced unless a shell action is explicitly recorded in the counts above. The Markov material was available as files; availability alone does not demonstrate that the model inspected or understood it. Automatic retention of writing is an infrastructure effect, distinct from model-requested environmental construction.

## Evidence and integrity

The runner retained each plan and exact raw generation before executing an action or appending writing. Records contain rendered user text, complete input token IDs, generated token IDs, sampled seeds, decoded output, environmental results, parent-event hashes and before/after world identities. Content-addressed byte objects retain checkpoint file contents outside the model's reach.

Every tenth entry checked the old primary inventory, pinned code/model files, event chain, manifest/raw hashes, prompt and input reconstruction, token decoding, state pointer, live checkpoint and independent restoration into a fresh mount. In-memory tensor digests were checked on the frozen base model; disk weights were independently hashed. Final verification additionally checked all 104 byte objects, stop labels, the complete 751–850 sequence, ten checkpoints, five reports, pause state and absence of an outstanding action. Fresh-mount restoration uses the same pinned checkpoint decoder, not a wholly independent implementation of filesystem semantics. The separate final verifier additionally reconstructs accumulated notebook bytes directly from raw replies. Exact accumulated notebook-byte reconstruction: **True**.

The previous unknown interrupted attempt around old step 492 remains unknown. This phase neither reconstructs it nor claims to repair missing observations.

## Remaining influences and limits

**Factory system header:** the tokenizer automatically inserts “You are a helpful AI assistant named SmolLM, trained by Hugging Face” when called with a user-only message list. This was identified during the block and kept constant, not silently changed midway. It appears in the recorded input tokens and pinned chat template. This run is not entirely instruction-free. Removing that header in an explicitly versioned next condition is a concrete refinement; inherited pretrained tendencies would still remain afterward.

The recent reply history is serialized into a user message as JSON. That presentation can itself encourage quoting, escaping, role description or repetition. It is a candidate harness influence, not a demonstrated causal mechanism here. Native conversation roles or a less escaped view could be compared on matched disposable contexts without turning our preferences into live rewards.

Persistent files are not persistent weights, a persistent KV cache or proof of learning. Distinct texts do not establish improved reasoning; repetitions do not prove panic, stagnation or a specific internal state. Generated explanations are not verified access to private internal reasoning. No causal efficacy ranking of FRR, adapters, environments or prompts follows from this mixed-condition transition.

/world and /tmp have hard 8 MiB tmpfs data-block limits, but inode metadata is outside that byte quota. Actions have 32 MiB per-process address-space and 128 shared-UID process limits, three seconds of wall time, two CPU seconds per process, bounded output and individual files. These do not constitute an aggregate cgroup memory guarantee. Root/system/device mounts are read-only, and nested user namespaces are disabled. /tmp, shell variables and processes end between actions; /world files persist. Unsupported checkpoint types or unreadable state stop the observer rather than justify a completeness claim. See REVIEW_AND_LIMITS.md and RESUME.md for reconstruction scope and recovery.

## Strongest next contact

Keep the notebook/action distinction. Remove the automatically inserted factory instruction in the next version and test interface/history presentation on matched isolated contexts. The purpose is to determine how much of the observed writing comes from how we expose the world, without requiring the model to act or treating its notebook as unsuccessful code. Preserve the current phase as observed; do not retroactively rewrite its inputs or outcomes.

Garden view: the new plot can retain writing and support real computation. This block shows what the small model wrote under that access arrangement. It does not yet show the garden using those computational affordances to build new functioning tools.
