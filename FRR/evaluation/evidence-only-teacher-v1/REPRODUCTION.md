# Reproduction and scope

This study uses existing local model and adapter binaries, not a new download or paid inference service. Their identities are pinned by FREEZE.json, the acquisition MANIFEST.json dependency, and the run manifest. This text/code publication does not contain those binaries. Merely cloning GitHub does not reproduce model availability.

`study.py run` consumes the saved frozen QUERIES.json, TOKENIZATION.json and code dependencies. It creates a new run directory exclusively; do not rerun over saved outputs. `study.py verify` reconstructs results and also writes new summary/check files exclusively. Use a separate copy for replay, preserving source outputs.

Preparation in this actual run included the independent review recorded in scouts/DESIGN_REVIEW.md: the initial helper generated lengths only; before model load, exact chat-template token IDs were added to TOKENIZATION.json and code/protocol/tokenization hashes were re-frozen. before_prepare retains the initial files. For a newly generated preparation, add these exact token IDs after `study.py prepare`, recompute affected FREEZE.json hashes, and declare the preparation date/timing before any new outputs. Do not present a regenerated freeze as the historical one.

Every model call receives only one user prompt and begins with a fresh KV cache. Supplementary faithful notes restate supplied facts; no retrieval tool, gold answer, previous model answer, training step or persistent memory update enters a prompt. Gold labels exist in scoring metadata and candidate scoring after free generation. The seven legacy anchors are checks of historical behavior, not new fresh-case accuracy evidence.
