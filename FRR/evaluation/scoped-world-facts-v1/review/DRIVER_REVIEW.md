# Prelaunch driver compatibility review

15 November 2026, America/Chicago. Static, read-only review before model execution. No driver import, inference, world opening or main/source mutation was performed. Python AST parsing passed; all eight files listed in DESIGN_FREEZE.json match their recorded hashes at review time.

## Finding

**No blocking compatibility issue found.** This is a code/protocol review, not a substitute for the driver's actual preparation, preflight or artifact audit.

The imported kernel's globals ARMS and TURNS are correctly set to prose/json and three. Kernel functions resolve those module globals at invocation. M, common helpers, body generator, instrument and world implementation continue to point to the preserved source locations. Changing H does not reroute execution physics; the custom prepare supplies its own prefixes/rules/pins.

Preparation preserves source inventories, ACTIVE identity, parent state/world/rules; clones the same parent into each branch; changes only WORLD_RULES; checks that changed path and resulting bytes; verifies stores; renders each actual prepared initial snapshot; asserts snapshot and world equality; then records per-arm actual messages and token IDs. It intentionally permits different input IDs. Neither historical model conversation nor FRR is inserted into this fresh initial conversation. Kernel preflight is compatible with these arm-named paths and turn-zero states.

The shared kernel's only live-selection condition is arm == 'live'. Neither new arm matches, so commit_reply creates identical typed runtime_feedback-only receipts, while preserving after-effect snapshots externally. Auxiliary observation overflow does not block these non-live arms. Known effects are captured before input-capacity pause; unknown effects retain PENDING and prevent automatic replay. The same parser and generation function are used. Raw output is not repaired or promoted into an action by this adapter.

The run loop is prospectively round-robin three turns, with six calls maximum and honest earlier user/capacity/unknown-effect stopping. Single-attempt RUN_STARTED/RESULTS and immutable plan/raw/record paths protect against ordinary automatic replay. Immutable RUN.lock prevents concurrent standard attempts. Guards cover main/source/pointer and listed pins before/after replies. Tensor digest checks surround actual inference, with no parameter updates. Model load is local/offline through the unchanged body dependencies.

Audit remains compatible: it iterates the configured arms; validates full actual message/token history, raw text, parsed cells, receipt payload, actual batch/event/bundle linkage, world verification and state counts. The inherited result alone hardcodes planned_model_calls=8; the adapter explicitly documents and replaces that display field with the declared six while leaving independently computed actual counts unchanged. Zero consumed post-reply observations is asserted. A partial run can legitimately audit with fewer than six actual calls, so final reporting must state actual versus planned rather than infer completion from status pass.

## Nonblocking improvements and limits

The manifest directly pins all operative text files plus DESIGN_FREEZE, but not PROTOCOL.md, FACT_CROSSWALK.md or DESIGN_CHECKS.json, whose hashes are recorded inside that freeze. These match now. Pinning or validating those three through the actual preflight would also guard drift in the external prospective protocol artifacts. This does not currently change model-facing bytes or invalidate the configured comparison.

The adapter omits the upstream run_model's explicit purpose == model_study assertion; its own preparation always writes that purpose, and the actual run is prepared by this adapter. Adding the assertion would harden misuse against foreign hand-written stores, without being necessary for this declared store. The resource monitor begins after model loading; this matches the supplied implementation's operational limit only after creation, not a proof that load-time memory was monitored. Neither issue changes the arm match.

A passed audit cannot establish semantic equivalence as perceived by the model, permission understanding, learning or efficacy. No act remains non-elicitation; error repair requires an actual error and later reply opportunity. Final claims should follow the earlier independent protocol review.

## Exact sources inspected

- experiment.py SHA256: `977869486731f871fa117ade795f134b296980eb2f768c20a8a9e36447b3786a`
- imported study.py SHA256: `cf84dab04d5b890740ba3e03d1743ac71444937b484073b88a28b53321e9f1c0`
