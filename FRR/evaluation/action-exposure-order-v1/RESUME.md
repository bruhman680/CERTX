# Exposure-order contact resumption

This is the user's final bounded test before winding down. Do not start another experiment automatically.

Frozen study:48prompts, fixed adapted canonical reader, four exposed observations, six cyclic menu rotations, evidence before/after menu. Source labels/meanings remain fixed. No training or tool-action execution.

Run command writes fresh run/ and refuses overwrite. If interrupted, retain all partial files; do not silently retry or treat partial as complete. Once run/RUN_MANIFEST.json says complete, use:

    /workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/action-exposure-order-v1/study.py finish

The audit uses the prior local snapshot /workspace/exposure-order-before.json and must precede current navigation updates. Preserve/byte-archive old CURRENT_HANDOFF.md, sync/CURRENT_ORIENTATION.md and evaluation/CURRENT_RESEARCH_MAP.md before syncing them. Earlier experiments and weights must remain unchanged. Publish only this new contact plus the three current navigation updates, verifying archives and all older Git blobs outside that allowlist. User expects a brief result and a decompression in chat, then no background work until return.

## Completed state

The run and finish audit have now completed; CHECKS.json, REPORT.md and the current handoff record the result. Do not rerun the immutable study or its exclusive-create finish stage. Resume only with new user directions after the usage reset.
