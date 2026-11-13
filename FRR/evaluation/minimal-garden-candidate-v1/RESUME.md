# Resume the computational garden version

Read REPORT.md and ACTIVATION.json for current status before running. The original reference remains at entry 1550; the current new-version count is in run/STATE.json. Diagnostic stores are not the active open run.

The new world accepts complete explicit Python/sh notebook cells and ordinary writing. No rule demands useful behavior. Do not add tasks, demonstrations, scores, seed changes or automatic code repairs during an ordinary open continuation. Do not alter the pinned source, model, decoder, laws or memory policy without recording a new condition.

Use the existing local CPU environment; no paid model endpoint is required:

```sh
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/minimal-garden-candidate-v1/candidate.py status
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/minimal-garden-candidate-v1/candidate.py verify
```

A newly requested bounded block uses:

```sh
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/minimal-garden-candidate-v1/candidate.py resume --steps 12
```

This example does not schedule a block. The current runner supports 1–50 replies per invocation. Exact transcript growth is bounded: if the next input exceeds 7,936 tokens, it pauses before generation rather than dropping history. Longer-term memory redesign remains a separate question.

To request a pause during a running block, create run/PAUSE_REQUEST. The runner checks it between replies; do not kill a process in the middle of a cell when a clean pause is possible. Remove a consumed pause request only after recording why and checking the current state; a request is not an unknown-outcome marker.

Never delete run/PENDING.json, world/PENDING.json, world/BATCH_PENDING.json or an owned lock merely to force continuation. A pending or uncertain operation requires inspection of the retained plan, raw output, receipts and effects. Known ordinary code errors do not require a reset, repair or semantic rejection.

Files and supported modes/links persist across reconstruction. Processes, /tmp, interpreter variables, KV state, timestamps and inode identities do not. The model can create programs and data in files within its laws. External observer interpretations remain outside model inputs; only actual receipts enter the growing conversation.

All source and dependency pins are checked before use. Restoring elsewhere requires the pinned model/tokenizer and compatible sandbox runtime; the archive is not a complete OS image. Preserve lineage and record platform differences rather than assuming identical behavior.
