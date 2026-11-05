"""Refresh current navigation only after the final450check. Archive bytes are untouched."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;ENV=ROOT/'evaluation/source-access-three-cycle-v1/cycle3/environment'
def main():
 x=json.loads((R/'CHECKS.json').read_text());assert x['status']=='pass' and x['next_step']==450 and json.loads((ENV/'STATE.json').read_text())['next_step']==450 and (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists()
 (ROOT/'CURRENT_HANDOFF.md').write_text(f'''# Current handoff: same garden paused at 450

5 November 2026. [Run report](evaluation/discovery-400-to-450-v1/REPORT.md), [checks](evaluation/discovery-400-to-450-v1/CHECKS.json), [resume](evaluation/discovery-400-to-450-v1/RESUME.md). [Separate diagnostic](evaluation/world-control-diagnostic-v1/REPORT.md), [diagnostic layers](evaluation/world-control-diagnostic-v1/LAYERS.md).

## Active primary

`evaluation/source-access-three-cycle-v1/cycle3/environment`. Active runner `world_routine.py`, version `discovery-play-patch-v1`, manifest `ENVIRONMENT_DISCOVERY_PATCH_V1.json`. Cursor **450**, PAUSE present, no RUN.lock/block lock/model job. Verifier **{x['verification']}** passes 402 saved generations plus 48 origin entries. Ten five-entry windows passed from 400 to 450. Old 400-entry notebook prefix and all {x['old_immutable_files_checked']} pre-existing primary files outside STATE, NOTEBOOK and CURRENT_VERIFY remain unchanged. Earlier events, plans, manifests and renderers are retained.

## Latest observations

The primary's 50 new entries produced host kinds `{x['host_kinds']}`; world requests {x['world_commands']}, accepted world requests {x['executed_world_requests']}, actual number changes {x['world_state_changes']}, legacy executions {x['executed_legacy_requests']}. Final number {x['world_number']}. Stops `{x['stop_kinds']}`; generated tokens {x['generated_tokens']}. No condition changes, reset, training or diagnostic hints were added. Same fixed 135M base+adapter, sampling .8/.9, input 8096/output 96/native context 8192, shelf0002, curiosity sentence, charter, tools, history policy and feedback. Every session confirmed unchanged weights. No paid inference API, download or new provisioning.

Before continuation, ten isolated diagnostic calls used the saved 400-entry history through its normal recent-12/archive-access view, not all 400 entries directly. Initial eight trials and two adaptive follow-ups are recorded separately. Short world-only LOOK worked 2/2; short use-A worked 2/2, each isolated copy 0→1. Full-context requested trials produced no accepted controls. Short/full changes bundle history, seeds, charter, archive text and length; these trials do not isolate a single cause or establish rule understanding. No probe output/effect/instruction entered the primary; all 1,199 non-bytecode primary files were unchanged during the probes. Recorded diagnostic prompts/tokens/stops/receipts reconstructed without another model call. The first resumed primary entry matched the eligible pre-probe baseline under the same context/seed; that is reproducibility, not independent confirmation.

## Next direction

A useful separately recorded diagnostic could isolate which part of the prompt package affects control expression, or test consequence prediction. Neither was silently added to this primary run. The current evidence distinguishes expression, execution and untested rule understanding; do not call a copied command a general reasoning result. Keep primary terrain stable unless a new condition is deliberately recorded.

On later authorization inspect STATE, active manifest, PAUSE/RUN.lock, pointer and linked checks; use the installed runner in at most five-entry checked windows under broader reporting blocks. Do not rerun finished block drivers, the old installer for 305, older policy runners, reset the world, merge diagnostic/demo outputs, or silently retry an outstanding plan. No continuation beyond 450 remains active. Model/cache/path restoration limits are unchanged.

[Research index](evaluation/CURRENT_RESEARCH_MAP.md). Previous navigation bytes are archived in before/ under both new contacts. Earlier reports remain historical; this handoff and the passing current verifier describe the active boundary.
''')
 (ROOT/'sync/CURRENT_ORIENTATION.md').write_text(f'''# Orientation: paused at 450; diagnostic kept separate

5 November 2026. [Handoff](../CURRENT_HANDOFF.md), [run](../evaluation/discovery-400-to-450-v1/REPORT.md), [checks](../evaluation/discovery-400-to-450-v1/CHECKS.json), [diagnostic](../evaluation/world-control-diagnostic-v1/REPORT.md).

Same active world_routine.py / discovery-play-patch-v1. Primary paused at 450, verifier {x['verification']} passes 402 saved generations plus 48 origin. Ten new five-entry windows passed. Old notebook prefix/source records preserved; no job/lock remains. Fifty new entries: {x['world_commands']} world requests, {x['executed_legacy_requests']} legacy executions, number {x['world_number']}; stops {x['stop_kinds']}. No setup change, reset, training or paid inference API.

Ten diagnostic generations at snapshot400 never entered primary history. Short LOOK/use-A prompts each worked 2/2; full-context requested trials did not execute a control. Short/full differ in a prompt bundle, not solely history length. Command expression/execution is observed in copies; rule inference/transfer is untested. Model/adapter weights stayed unchanged. Follow-up probes were adaptive and separately declared.

Next proposals: isolate prompt components or test prediction explicitly, recorded as a separate condition. Continue the unchanged primary only on later authorization, with five-entry checks and broad summaries. Never rerun the old installer/finished driver or merge probe/demo data. Latest handoff supersedes old status descriptions.
''')
 prior=(R/'before/CURRENT_RESEARCH_MAP.md').read_text();start=prior.index('| Shelf |');end=prior.index('\n\nSame continuous',start);old_table=prior[start:end]
 # Preserve earlier catalog rows as historical links, while replacing the active header/current row.
 old_table=old_table.replace('| Latest continuation to 400 |','| Previous continuation to 400 |').replace('Active primary paused at 400','Historical boundary at 400')
 rows='| Latest primary 400→450 | [Report](discovery-400-to-450-v1/REPORT.md), [checks](discovery-400-to-450-v1/CHECKS.json), [resume](discovery-400-to-450-v1/RESUME.md) | Same primary paused450; ten checks passed; latest verifier in handoff |\n| Separate command diagnostic | [Report](world-control-diagnostic-v1/REPORT.md), [checks](world-control-diagnostic-v1/COMBINED_CHECKS.json), [layers](world-control-diagnostic-v1/LAYERS.md) | Ten isolated calls; short LOOK/A2/2 each, full requested controls0/4; bundle contrast, not rule learning |\n'
 lines=old_table.splitlines();table='\n'.join(lines[:2])+'\n'+rows+'\n'.join(lines[2:])
 (ROOT/'evaluation/CURRENT_RESEARCH_MAP.md').write_text('# Current research index\n\n5 November 2026. [Handoff](../CURRENT_HANDOFF.md). Earlier rows are historical contacts, not active-runner instructions.\n\n'+table+'\n\nPrimary remains one continuous environment, now at450. No diagnostic outputs, hints or effects entered it. All raw model data retained; old sources/manifest versions remain necessary for replay. Future prompt-component or prediction tests are proposals, not results. Current handoff/verifier supersede earlier status descriptions; archived navigation preserves its original bytes.\n')
 print('Current navigation synced to450.')
if __name__=='__main__':main()
