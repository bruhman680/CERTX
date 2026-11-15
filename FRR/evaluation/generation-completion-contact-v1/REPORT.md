# Extra allowance produced EOS, not a completed fence

15 November2026 UTC. **One actual detached model call**, with a512-token allowance. Main remains1630, paused; this reply is not entry1631 and no main body setting is changed.

## Why this contact

The main50 repeatedly reached its256-token cap inside an unfinished Python fence. That alone could tempt us to explain non-execution as insufficient output room. We tested that explanation with the exact next selected input and a larger declared allowance.

`PLAN.json` was saved before inference. The copied generator is AST-identical to the main generator after removing the docstring and budget constants. Maximum output changes256→512, reserved input7936→7680 within8192 total positions. The actual input remains2231 tokens, with no trimming or task/hint added. Same cached135M weights, float32 CPU/eager/two threads, greedy argmax and fresh KV.

The actual supported main1630 world is copied into a detached store. Its only initialization edit appends an explicit diagnostic generation-budget declaration to WORLD_RULES.txt. Physical limits and the original parser remain unchanged. This world-note difference is declared; generation inputs themselves are byte/token-identical to the reference.

## Actual result

- Exact input token IDs equal the main reference: **true**.
- First256 generated token IDs equal the main reference: **true**.
- Total generated tokens: **257**.
- Token257 is **EOS**, and generation stops there despite the larger allowance.
- Decoded text is **exactly the same unfinished program** as the main reply.
- Complete executable cells: **0**; incomplete Python fences: **1**.
- Actual operation: one literal notebook append, no executable cell, no nonempty feedback.

The parser did not reject a complete program. The model terminated without closing its existing fence. For this exact input/body/greedy condition, the hard256-token limit alone therefore does not explain the unfinished text: removing that immediate boundary yields termination, not closure. Increasing the allowance further would not extend this already terminated deterministic sequence under the same stopping rule; changing that rule would be another explicit experiment.

This is not proof that all prompts, larger budgets, samplers or smaller models behave this way. No alternative stopping rule, source repair, sampling intervention, training or generalized competence was tested. It is a narrow discriminating result that prevents a premature capacity-only explanation.

## Integrity

The raw reply and all token IDs are retained before notebook execution. Actual receipts and before/after world IDs are saved. Original source823-file inventory, selected main phase inventory during this contact, ACTIVE pointer, tensor digest and source pins match before/after. The detached world verifies, no pending marker remains, and no action or generation was replayed. Later observer report additions are outside the main model/world and are not a claim of perpetual phase-file immutability.

Independent read-only review confirmed exact input/prefix identity, EOS tokenID2 at257, decoded-text equality and absence of executable cells. The copied generator's algorithm difference was independently checked. The main50 and this contact are separate evidence.

Records: PLAN.json, INPUT_VIEW.json, RAW.json, BATCH.json, RESULTS.json, INITIALIZATION.json, INITIAL_WORLD.json, world/, and before-inventory manifests. No paid model endpoint or weight update was used.
