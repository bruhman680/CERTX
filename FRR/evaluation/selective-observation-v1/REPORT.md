# Selective attention without discarding the evidence

2 November2026 client date. User asks to reduce assistant context burden and focus close review around changes instead of processing every routine run. We introduced an external observer and replaced a large current research map with a short index. The model's notebook, interface, feedback, sampler, checkpoint and history policy remain unchanged.

## What is now read by default

[ATTENTION.md](ATTENTION.md) is the compact working entry point. Routine behavior becomes counts and links; up to6flagged example slots plus1deterministic quiet sample get excerpts. All boundary events are separately mandatory. [EVENT_INDEX.json](EVENT_INDEX.json) retains metadata and flags for every row, including flags outside the excerpt budget. [REVIEW_SAMPLE.json](REVIEW_SAMPLE.json) preserves full selected records for deeper lookup; it is not routinely pasted into the assistant context. Raw records remain separately archived.

The policy flags new coarse forms, new normalized question strings, token-length surges, input-pressure crossings, newly encountered output caps and large changes in coarse-form frequency against each trajectory/arm's preceding5responses. Thresholds are explicit heuristics, not calibrated phase detection or measures of reasoning quality. Question novelty is relative to the parent raw rows supplied to this observer, not exhaustive lifetime or semantic novelty. Quiet means unflagged by this policy, not healthy, unimportant or truly stationary. Sampling some quiet outputs helps inspect blind spots; it does not guarantee that every important event is caught. Marker and numeric-normalization rules can miss semantic changes.

## Continuation and observation result

30newgeneration calls completed out of40maximum. Two trajectories completed their planned5newrounds; two stopped individually at the declared2048input-token boundary, while the others continued. Four histories remain complete at35,32,35,33events (per-trajectory identities in AUDIT.json). No pruning/truncation/reset or input-budget increase occurred. Maximum observed over-limit planned requests were2060and2068tokens; those requests were recorded but never sent to the model. This is a resource-envelope event, not evidence of an emergent mental phase or a loss of the saved history. The model config supports a larger positional range, but this experiment did not silently expand its budget.

All30model rows entered the event index. Seven were flagged; six enter the bounded focus packet, with one additional flag retained in the full index. One unflagged sample was chosen deterministically by SHA ordering. This yields7routine example slots plus2mandatory boundary events instead of importing all30prompts/replies. The close-review excerpts show continuing record/template output, a new question string about the 'next smallest answer', and a coarse-form shift toward short Y/Response fragments. These are candidate observations, not demonstrated improvement. The quiet sample still resembles the earlier record-format baseline.

The new question and apparent score/Feedback text remain generated data. Actual task_score is None and actual feedback is the same neutral message for every new reply. No generated request is executed. The observer neither controls the garden nor changes model inputs, and no score/cap/phase claim is accepted solely from generated text.

## Context and history maintenance

The old research map had accumulated inline snapshots. Its exact bytes are archived at before/evaluation/CURRENT_RESEARCH_MAP.md and in Git history. The current map is now a short shelf index, with direct links to current work, earlier model/measurement/provenance work and that historical catalog. Current handoff and orientation are also archived before replacement. Older reports/raw outputs remain immutable. Navigation compression does not alter the model notebook, erase runs or create an 'absolute memory' claim.

Three contract tests pass, including identical parent/current model-interface rendering and deterministic quiet sampling. CHECKS.json reconstructs every dynamic prompt/token/output/feedback/history/checkpoint. AUDIT.json independently recomputes observer output exactly, verifies it does not mutate its input records, checks every indexed row and selection budget, validates all4parent prefixes, and confirms both boundary requests were not model calls. Model saved-file/in-memory digests stay unchanged. All owned jobs complete; no scheduled/background continuation. No install/download/new model/training/paid API or default controller change.

## What this changes in practice

Our normal read order is current handoff -> attention digest -> indexed exception -> exact raw evidence as needed. Every-row machine integrity checks continue. Full transcripts are not automatically brought into the working conversation, and all data are not treated as equally deserving human attention. A later observer version can reindex the preserved data; thresholds/selection changes should be versioned and their discovery timing recorded.

Next continuation must explicitly address the model's input budget for the two paused trajectories. Selective assistant attention has solved a different issue: review load. It does not free tokens inside the model's unchanged complete-history prompt. A larger declared budget or a separately labeled context-view experiment can be assessed later while preserving the raw notebooks. No context-view/truncation experiment is adopted here. Earlier representation/role/no-history hypotheses and broader research directions remain open.
