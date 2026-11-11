# CERTX Neural Garden branch — completeness and recovery inventory

**Exclusive research branch:** `bruhman680/CERTX`, ref `codex/frr-v05-explorations`. No merge or write to `main` or Claude's branches was requested or performed.

## Verified on 2026-11-11 UTC

Read the GitHub Contents directory listing for `NEURAL_GARDEN_V01` at our branch. For every one of its **56 normal text files that also exists at the local directory root**, compared the remotely reported Git blob SHA against `git hash-object` for the exact local file bytes: **56/56 matched, zero discrepancies**. This includes implementation, independent audits, research reports, summaries, the event/history ledger, and a self-contained HTML demonstration replay. The remote directory contains an additional large compressed text archive described below. This inventory is a point-in-time check; later file changes require a new comparison.

## Complete experimental data and exceptions

1. `THOUSAND_RUN_ROWS.jsonl.gz.b64` is a gzip-compressed, base64-encoded version of the 1,000-run row-level archive. It is stored in **the research GitHub branch**, with the exact machine-readable plain JSONL retained privately. Decode after cloning the branch:

   `base64 -d THOUSAND_RUN_ROWS.jsonl.gz.b64 | gzip -d > THOUSAND_RUN_ROWS.jsonl`

   Then verify `sha256sum THOUSAND_RUN_ROWS.jsonl` equals `e900765d70738d6e8dcaab13ca53710410ac7eb300b6e6edff69664669ff3000`. Avoid treating the compressed blob's Git SHA as if it were the raw JSONL SHA.

2. `LIVING_GARDEN_tick100_checkpoint.tar.gz` is a **private checkpoint**, not committed publicly; its 256 individual neural weights, RNG state, exact step-100 world and operating log are preserved in ChatGPT Library file `libfile_1b6b560baa2c8191b3e925c26d34d703`. Recover it from the same account, unpack to the simulator's expected run directory, and follow `LIVING_GARDEN_GUIDE.md`. Treat included `.pkl` files as trusted local data only.

3. `Neural_Garden_v01_demo_checkpoint.tar.gz` is an older **private demonstration checkpoint**, not committed publicly; ChatGPT Library `libfile_43de54e161bc81919ac01634d26e2d81`. The non-sensitive `demo_replay.html` was committed publicly so the visual history survives without uploading the raw checkpoint.

4. `THOUSAND_RUN_ROWS.jsonl` (uncompressed 1,000-run row data) is additionally saved privately in ChatGPT Library `libfile_ff2bad2ff7908191a9c305153d01b3f1`, besides its reconstructable compressed branch copy.

5. Local transient directories (`__pycache__`, `demo_run/`, `runs/`, `runs/living_world/`) and short-lived binary state files are intentionally **not committed** as repo source. Persistent code and instructions to reproduce them are committed; the important runnable living-world checkpoint is privately backed up as above. This avoids exposing detailed dynamic state through a public source repository.

## Scope and limits

This audit covers the `NEURAL_GARDEN_V01` research workspace only. It does not assert that every file on every historical branch of CERTX has been copied or rebased into this branch. Existing branch ancestry provides ordinary shared history, and cross-branch changes should be selected deliberately so unrelated experiments remain separate.

The user authorized **2,000 research loops in total** (initial 1,000 plus another 1,000), with unrestricted simulator cycles/tests inside each loop. Only **14 substantive loops** are documented as completed through this audit; no claim is made that all 2,000 have run, or that agents execute while this chat is idle.
