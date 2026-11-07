# Continue the same frozen garden

Current count950, paused. No operator design changes are implied by continuation. Read CONTRACT.json and FREEZE_INTENT.md; the seed/model/world/input rules are fixed.

Run only a newly user-authorized bounded block, using the existing runner:

```
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/final-garden-contract-v1/runner.py resume --steps 100 --integrity-every 10 --report-every 50
```

The example does not authorize100 more entries by itself. Steps may be1–250. External integrity cadence may narrow within1–10; reporting may use50 or100, with the latter chosen only when observational evidence warrants broader summaries. These observer options do not change model-facing messages, physics, sampling or memory rules. Generic resume restores the latest checkpoint and retains current count and recent12 replies.

Before inference, source/contract/model/runtime hashes, prior stages and latest committed state are verified. Root ACTIVE_GARDEN_PHASE.json must identify this phase. A new session has an owned exclusive lock. A contender cannot remove another session's lock or pause it. Never delete a PENDING.json or outstanding plan simply to force a resume: an interrupted model/action attempt requires explicit evidential inspection, and unknown effects are not silently replayed.

Actual code-free verification is available via runner.py verify. Redirect its output to a new observer artifact rather than overwriting the original preflight log. This restores a fresh temporary namespace and checks records; it makes no model inference calls. Reconstruction uses the same pinned checkpoint decoder, not an independent filesystem implementation.

All supported /world bytes, modes and links persist. Processes, shell variables, /tmp, timestamps, inode numbers and model KV cache are not persistent under the declared boundary. Old notebook and prior-replies files remain in-world and can be changed by the model's own permitted actions; external raw records cannot be rewritten by it. The automatic recent12 context comes from raw reply records, so editing the notebook does not retroactively edit that short replay.

The code/manifest/contract, model and kernel-context limits are not silently repaired after the freeze. Capacity overflow, unsupported/unreadable state, hash drift or uncertain execution is an explicit stopping point. A change beyond the frozen rules is a separately recorded experimental condition rather than ordinary continuation.

Cached model provenance: HuggingFaceTB/SmolLM2-135M-Instruct revision12fd25f77366fa6b3b4b768ec3050bf629380bac, weights SHA2565af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c. No additional adapter is attached. The research archive stores reproducible metadata and checkpoint bytes, not the large model download or a complete Linux image. Restoring on a different platform must check the declared dependencies and record infrastructure differences rather than assuming identical conditions.
