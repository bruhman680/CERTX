# Continuation and recovery

The active logical garden is identified by FRR/ACTIVE_GARDEN_PHASE.json. This phase follows the preserved original 750 entries; it is not an independent season whose observations were secretly imported. The older primary storage remains an immutable lineage parent. Its historical STATE.json correctly remains at 750, while this phase's run/STATE.json records the current total.

Do not rerun `run.py run` after completion: it is deliberately single-use and refuses a non-750 starting counter. A new bounded continuation should use a versioned runner, read the latest checkpoint, restore into a new empty World, and verify every blob and chain before any generation. A new phase must preserve this phase and retain the explicit parent link.

On a normal pause, restore the last bundle from run/bundles using run/objects. /world contents, supported types, permissions and links survive; no live model KV cache, process, shell variable or /tmp content survives. Weights do not learn during this run. Re-loading the same cached base checkpoint is not replacing the persistent external world.

On an interrupted generation/action, preserve PENDING.json, raw outputs and any results. Do not automatically repeat generation or execution. A raw reply without a terminal action result may have an unknown effect. Reconstruct only the last committed checkpoint and report the uncertain intervening attempt; don't claim missing world changes were observed. STOP requests are respected between entries. Integrity failures stop and set pause bookkeeping; ordinary notebook writing and ordinary action errors do not gate continuation.

Records outside the guest include prompts, token IDs, exact raw text, action results, before/after checkpoints, content-addressed bytes, hashes and checks. The model can edit its own notebook or prior-replies file without altering those observer records. Guest outputs are observations, not instructions to the external observer.

The base model download identity is HuggingFaceTB/SmolLM2-135M-Instruct, revision 12fd25f77366fa6b3b4b768ec3050bf629380bac; model.safetensors SHA-256 5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c. Weights and the Python environment are not embedded in these research records. Recreate dependencies from the existing cloud/runtime documentation, download the pinned checkpoint if needed, verify its digest, and retain old canonical adapters as historical configurations rather than silently attaching them.
