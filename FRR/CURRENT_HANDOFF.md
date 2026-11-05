# Current handoff: same garden paused at 450

5 November 2026. [Run report](evaluation/discovery-400-to-450-v1/REPORT.md), [checks](evaluation/discovery-400-to-450-v1/CHECKS.json), [resume](evaluation/discovery-400-to-450-v1/RESUME.md). [Separate diagnostic](evaluation/world-control-diagnostic-v1/REPORT.md), [diagnostic layers](evaluation/world-control-diagnostic-v1/LAYERS.md).

## Active primary

`evaluation/source-access-three-cycle-v1/cycle3/environment`. Active runner `world_routine.py`, version `discovery-play-patch-v1`, manifest `ENVIRONMENT_DISCOVERY_PATCH_V1.json`. Cursor **450**, PAUSE present, no RUN.lock/block lock/model job. Verifier **0085** passes 402 saved generations plus 48 origin entries. Ten five-entry windows passed from 400 to 450. Old 400-entry notebook prefix and all 1196 pre-existing primary files outside STATE, NOTEBOOK and CURRENT_VERIFY remain unchanged. Earlier events, plans, manifests and renderers are retained.

## Latest observations

The primary's 50 new entries produced host kinds `{'record_receipt': 50}`; world requests 0, accepted world requests 0, actual number changes 0, legacy executions 0. Final number 0. Stops `{'token_limit': 39, 'eos': 11}`; generated tokens 3803. No condition changes, reset, training or diagnostic hints were added. Same fixed 135M base+adapter, sampling .8/.9, input 8096/output 96/native context 8192, shelf0002, curiosity sentence, charter, tools, history policy and feedback. Every session confirmed unchanged weights. No paid inference API, download or new provisioning.

Before continuation, ten isolated diagnostic calls used the saved 400-entry history through its normal recent-12/archive-access view, not all 400 entries directly. Initial eight trials and two adaptive follow-ups are recorded separately. Short world-only LOOK worked 2/2; short use-A worked 2/2, each isolated copy 0→1. Full-context requested trials produced no accepted controls. Short/full changes bundle history, seeds, charter, archive text and length; these trials do not isolate a single cause or establish rule understanding. No probe output/effect/instruction entered the primary; all 1,199 non-bytecode primary files were unchanged during the probes. Recorded diagnostic prompts/tokens/stops/receipts reconstructed without another model call. The first resumed primary entry matched the eligible pre-probe baseline under the same context/seed; that is reproducibility, not independent confirmation.

## Next direction

A useful separately recorded diagnostic could isolate which part of the prompt package affects control expression, or test consequence prediction. Neither was silently added to this primary run. The current evidence distinguishes expression, execution and untested rule understanding; do not call a copied command a general reasoning result. Keep primary terrain stable unless a new condition is deliberately recorded.

On later authorization inspect STATE, active manifest, PAUSE/RUN.lock, pointer and linked checks; use the installed runner in at most five-entry checked windows under broader reporting blocks. Do not rerun finished block drivers, the old installer for 305, older policy runners, reset the world, merge diagnostic/demo outputs, or silently retry an outstanding plan. No continuation beyond 450 remains active. Model/cache/path restoration limits are unchanged.

[Research index](evaluation/CURRENT_RESEARCH_MAP.md). Previous navigation bytes are archived in before/ under both new contacts. Earlier reports remain historical; this handoff and the passing current verifier describe the active boundary.
