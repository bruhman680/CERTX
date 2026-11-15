# Matched initial-only versus live directory sensing

Prepared R&D source,15 November2026 America/Chicago, using the updated client-date context relayed by root. This file records the design and commands; actual execution status is in `run/STATE` files and `run/RESULTS.json` when present. **Builder preparation and tests perform zero model calls and do not activate a main phase.** Main remains1630.

## Fixed comparison

Two no-FRR arms, `initial_only` and `live`, start from identical copies of the actual main1630 supported filesystem. Each has an empty system message and the same M0 mechanical user text followed by the **same new-instrument initial packet**. No historical assistant examples, curiosity invitation, task, target answer, hint, reward, required action or arm identity is added to model input.

The only common parent-relative filesystem edit replaces WORLD_RULES.txt with the shared mechanical text plus a description of the directory-observation channel. Exact old rule bytes are retained externally. All other inherited writing and material remain intact; a fresh conversation is not a pristine world. Model edits to ordinary files remain lawful and are recorded rather than restored.

Four continuous replies per arm are planned, in round-robin order, for at most **eight actual calls**. Same cached pinned135M model, CPU float32/eager/two threads, original unmodified greedy256 generation function, fresh KV. No weights or adapters are trained. All actual branch pairs persist in input; no pruning or summaries. The complete input must fit7936 tokens.

## Feedback and sensing

Both arms receive a common typed JSON wrapper with `runtime_feedback`: the exact parsed existing runtime-feedback object, or null when no model-facing receipt exists. This includes actual notebook-storage errors as well as cell stdout/stderr/exit/boundary information. Raw runtime feedback is also saved separately. Successful notebook storage suppresses its returned model-facing receipt; its raw guest receipt still exists in the action ledger.

`live` additionally receives `world_observation`, containing the frozen instrument's captured names/types/logical byte sizes and truthful timing/counters. `initial_only` receives no later directory packet. Both arms nevertheless retain **full after-effect captured bundles externally**. No state packet is disguised as a program receipt. No source bundle ID or observer provenance is inserted into the packet.

Snapshots follow the complete known reply effects, including the automatic notebook append and any complete cells. `world_step` is the committed operation count; `reply_index` is the branch reply number. Neither is an autonomous environmental tick. Initial snapshots are not relabeled as fresh later observations. The model sees only partial metadata, **not file contents, complete Markov state, native-OS completeness or a view of its own reasoning**. Automatic notebook growth is not model-initiated tool creation or evidence of learning.

The new packet schema, counters, wrapper and initial rule-description update define a **new matched baseline**. Historical M1 is not a latency-only control. Changing feedback length, JSON structure, numerical counters and timing are part of the observation-channel bundle; this experiment does not identify a unique semantic mechanism.

## Known limits and honest pauses

Observation JSON has a fixed8192-byte bound; the frozen instrument emits all currently supported entries or no packet. It does not hardcode five names, choose interesting files or truncate. This is separate from tokenizing the **whole** input against7936.

After known action effects, the controller saves the full snapshot, raw runtime feedback, observation/error record, hash-linked reply record and branch state before clearing its outer pending marker. If a selected live observation cannot fit, that branch pauses with the known action committed and no partial next packet. An undelivered auxiliary render overflow does **not** pause `initial_only`; its actual runtime feedback can continue if its own input fits. This difference is an operational consequence of the selected channel and may change opportunities; it is not a matched-FLOP comparison.

If the complete next input exceeds7936, the branch pauses without pruning and without losing the already committed action. If effects or checkpointing are unknown, the pending marker remains and the study stops without automatic replay. Wrong, repetitive, prose-only or action-free replies are data, not semantic stop conditions. A fixed4-reply budget, requested pause, declared capacity or dependency drift are distinct stopping bases.

After reply4, a snapshot is still captured and any feedback is selected for a possible next input, but **no fifth generation is scheduled**. Only actual later plan/raw records establish that a post-reply observation was consumed: at most three such exposures per live arm within four calls. Initial perception is separate.

## Commands and checks

Use `/workspace/cache_backend_venv/bin/python study.py prepare`, `preflight`, `run`, or `audit`. Default store is `run/`; `--store PATH` permits a separately named fixture directory. `run` is deliberately single-attempt: existing RUN_STARTED, pending or lock evidence must be inspected, not cleared to force a replay. `PAUSE_REQUEST` stops before the next generation. Existing lock ownership is preserved.

`prepare` clones worlds and initializes common rules but does not load/generate a model. `preflight` checks source inventories, pins, initial token IDs, identical world/input conditions and committed stores. `run` is the only model-loading command and is restricted to real model-study stores. Raw tokens/text precede execution; actual effects, receipt/state separation and hash chains are retained. `audit` recomputes contexts and packets and binds each result to actual committed world batches/events/bundles.

Final-source targeted tests are under `tests-v2/RESULTS.json`: new file perception, persistence across close/reopen, truthful after-effect timing, actual error/observation separation, ordinary-error continuation, full-snapshot/action preservation at live observation overflow, control continuation despite auxiliary overflow, and post-action whole-input capacity handling. Fixture limit overrides are allowed only in explicitly labeled zero-inference fixtures. Their synthetic replies and labels are never model progress.

The first test version passed before root's persistence/audit hardening. It remains under `tests/` with `TEST_RESULTS.json`; exact earlier source/rules/test script are in `source-before-hardening/`. Those historical fixture pins refer to that earlier source and must not be resumed under current code. No old model pilot or main result is overwritten.
