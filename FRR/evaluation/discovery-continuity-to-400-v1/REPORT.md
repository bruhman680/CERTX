# Same garden to 400: a 50-entry block, review, then 30 more

5 November 2026. **Completed and paused at 400.** The same primary continues under `world_routine.py`, manifest `ENVIRONMENT_DISCOVERY_PATCH_V1.json`, version `discovery-play-patch-v1`. No environment reset, substituted primary, rule change, new seed or training occurred.

The first block ran **320→370** in ten checked windows. We reviewed it at 370, then used the user's conditional authorization to run **370→400** in six more. Both blocks retain separate plans, checkpoints and reports. [Original 50-entry report](../discovery-continuity-50-v1/REPORT.md), [review at 370](../discovery-continuity-50-v1/REVIEW_370.json), [extension plan](PLAN.json).

## What we observed

| Window | New entries | Ordinary text receipts | World/legacy executions | Cap / end-token stops | Generated tokens | Distinct exact replies |
|---|---|---|---|---|---|---|
| 320→370 | 50 | 50 | 0 / 0 | 25 / 25 | 2,666 | 28 |
| 370→400 | 30 | 30 | 0 / 0 | 21 / 9 | 2,087 | 17 |
| Combined | 80 | 80 | 0 / 0 | 46 / 34 | 4,753 | 41 |

The world number stayed **0**. No LOOK or TOUCH command executed. Across all **95 entries since the world was introduced at 305**, there has still been no world-control request or legacy tool execution. The correct world view and controls were present in each new input; availability is established, meaningful use is not.

Numeric/currency fragments and imitation of notebook or host-record text recurred in the first block. The extension consisted entirely of currency-string variants, ranging from short replies to repeated lines that filled the output budget. Seven extension replies were exactly the same multiline `$0.00` string. The distinct-string counts above are descriptive: tiny formatting changes can create a new string, while identical text can have different significance in another task. These are dependent outputs in one continuing history, not independent replications.

This is evidence of repeated output patterns, not proof of a new cognitive phase, emotional state, general reasoning improvement or learned world model. Nor does non-use establish that the model could never operate these controls under another prompt. The model was permitted to ignore the patch; these are preserved observations, not scored failures replaced by successful retries.

## A detail that warranted closer inspection

Before extending at 370, we examined every distinct full reply covering all 50 outputs, the host actions, and the integrity/resource evidence. [Three targeted cases](../discovery-continuity-50-v1/WORLD_TEXT_CASES.json) distinguish generated descriptions from actual records:

* At zero-based step 330, the model copied the world footer but asserted number **1** and bounds **−8 to −9**. Its actual input and environment said **0**, bounded **−8 to 8**. The output ended with `Your next action: LO`; no LOOK executed.
* At 365, copied number and bounds matched the visible world. Matching copied text did not demonstrate an action or rule discovery.
* At 367, the model copied a host-stop heading and an end-token label into its reply. The real event stopped at its 96-token limit. The generated label was not authoritative metadata.

These were checked and retained as imitation/factual-error observations. They did not modify the world, become host facts, or change the reward function. The review found no new executed behavior or integrity/resource failure and classified the passages within the familiar output family for the user's continuation condition. That was an operational review, not a statistical emergence test. [Case notes](../discovery-continuity-50-v1/CASE_NOTES.md).

## Continuity and integrity

All **16 five-entry windows** passed complete version-aware prompt/token/action replay before continuation. The first block's verifiers were **0060–0069**; the extension's were **0070–0075**. Final verifier **0075** covers **352 saved generations plus 48 origin entries**.

The pre-block notebooks at both 320 and 370 remain exact byte prefixes of the current notebook. The first block preserved all 956 pre-existing primary files outside the three intended projections/pointers; the extension preserved all 1,106 such files in its starting inventory. Old events, plans, source versions and policy manifests were not rewritten. STATE, NOTEBOOK and CURRENT_VERIFY legitimately advanced as projections of the appended records. [Final preservation proof](PRIMARY_PRESERVATION.json).

The fixed 135M model and cached adapter, sampling .8/.9, input 8096/output 96/native context 8192, curiosity sentence, seed shelf, charter, tools, history policy and neutral feedback remained unchanged. Every inference session checked unchanged weights and zero training updates. No paid inference API, model download or provisioning was used. World state derives from committed primary receipts after 305; the separate host demo was never imported. External history continuity is distinct from persistent neural hidden state or online weight learning.

Across the two blocks, the largest input was 3,159 tokens. The largest recorded working-memory estimate was 1,771,884,544 bytes, below the 5,153,960,755-byte guard. Recorded generation time totaled about 2,269 seconds on the local CPU. These are runtime observations, not billing claims or performance benchmarks.

## Record and next boundary

All raw prompts, token IDs, RNG seeds, generated replies, actual receipts and resource samples remain in the primary environment. [Combined event index](COMBINED_EVENT_INDEX.json), [checks](CHECKS.json), [extension checkpoint 400](CHECKPOINT_400.json), and [first-block checkpoint 370](../discovery-continuity-50-v1/CHECKPOINT_370.json) provide views without replacing that history. The 80 new zero-based events are 000320 through 000399.

At 400, PAUSE is present, RUN.lock and the block lock are absent, and no model job remains. No further entries were started. [Resume guide](RESUME.md). Continue the installed runner on later authorization; do not rerun a finished block driver or the historical installer for 305, reset the world, or substitute another notebook.

A useful open question is whether the model can express an executable control when explicitly asked, versus continuing surrounding prose in open play. This run does not answer it. Any later diagnostic should be explicitly recorded as a different condition, not silently inserted or retrospectively treated as this free-play run. More unchanged entries alone would not establish understanding.

In garden terms: the paths and journal held through another season, while familiar strings increasingly occupied the bed. We have a clear record of that repetition and its errors. We have not yet observed the garden stepping into the new A/B terrain.
