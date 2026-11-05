"""Update current navigation only after the completed400boundary is verified."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;ENV=ROOT/'evaluation/source-access-three-cycle-v1/cycle3/environment'
def main():
 x=json.loads((R/'CHECKS.json').read_text());a=x['combined_320_to_400'];state=json.loads((ENV/'STATE.json').read_text());assert state['next_step']==400 and x['status']=='pass' and (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists()
 handoff=f'''# Current handoff: same garden paused at400

5 November2026. [Combined report](evaluation/discovery-continuity-to-400-v1/REPORT.md), [checks](evaluation/discovery-continuity-to-400-v1/CHECKS.json), [resume](evaluation/discovery-continuity-to-400-v1/RESUME.md).

## Active primary

`evaluation/source-access-three-cycle-v1/cycle3/environment`. Active runner: `world_routine.py` in that study. Version: `discovery-play-patch-v1`. Active manifest: `ENVIRONMENT_DISCOVERY_PATCH_V1.json`. Cursor **400**, PAUSE present, RUN.lock and block lock absent, no model job. CURRENT_VERIFY **{x['verification']}** passes352saved generations plus48origin entries. Exact notebook prefixes at320and370are preserved. All{x['old_immutable_files_checked']}pre-existing primary files outside STATE,NOTEBOOK and CURRENT_VERIFY remained unchanged during the extension; the50-entryblock also verified its entire earlier inventory. Old source, manifests, events and plans were not overwritten.

## Latest two blocks

User first authorized50entries320→370, then conditionally another30to400if the review found ordinary observations and passing checks. The first block completed all ten windows; review of every distinct full output confirmed familiar repetition/imitation and no new executed behavior or integrity/resource issue. The second block completed all six windows. Both reports/plans/checkpoints remain separate. [Review](evaluation/discovery-continuity-50-v1/REVIEW_370.json), [50-entryreport](evaluation/discovery-continuity-50-v1/REPORT.md).

Combined80entries: host kinds `{a['host_kinds']}`; world requests{a['world_requests']}, world state changes{a['world_state_changes']}, legacy executions{a['legacy_executions']}; final number{x['world_number']}. Stops `{a['stop_kinds']}`, generated tokens{a['generated_tokens']}. All95entries since world introduction are preserved. Familiar numeric/currency fragments and record-shaped prose are not authoritative actions, rewards or metadata. [Targeted cases](evaluation/discovery-continuity-50-v1/WORLD_TEXT_CASES.json) include a false world description and copied stop label; structured receipts remained correct. No general reasoning, learning or emergent-phase claim.

Same fixed135Mmodel and adapter, sampling.8/.9, input8096/output96/native8192, seed shelf0002, curiosity sentence, charter, tools, history policy and neutral feedback. No condition changes, reset, training, model download, new provisioning or paid inference API. Every session checked unchanged weights. The live world state derives from actual primary receipts after305; no second journal or host-demo history was merged.

## Continue

On later authorization, inspect STATE,active manifest,PAUSE/RUN.lock,current pointer and linked checks. Use the installed active runner; continue in checkedfive-entrywindows with broader reporting as authorized. Do not rerun the finished block drivers, old305installer or older policy runners. Do not silently retry an outstanding plan. Keep terrain stable unless a separately recorded condition change is deliberately chosen. No continuation beyond400is running or authorized by this completed contact.

The present record establishes availability of controls and observed output/action behavior. It does not establish that the model can or cannot use those controls under every other prompt, or that copied state text reflects an internal rule model. External notebook continuity is distinct from online neural learning. Current model/cache/path restoration limits are unchanged.

[Research map](evaluation/CURRENT_RESEARCH_MAP.md), [design synthesis](evaluation/discovery-play-patch-v1/OVERVIEW.md). Earlier navigation snapshots and reports remain historical; this handoff and the passing current verifier describe the active boundary.
'''
 for p,q in [('at400','at 400'),('November2026','November 2026'),('passes352saved','passes 352 saved'),('plus48origin','plus 48 origin'),('at320and370are','at 320 and 370 are'),('All'+str(x['old_immutable_files_checked'])+'pre-existing','All '+str(x['old_immutable_files_checked'])+' pre-existing'),('the50-entryblock','the 50-entry block'),('authorized50entries320→370','authorized 50 entries 320→370'),('another30to400if','another 30 to 400 if'),('50-entryreport','50-entry report'),('Combined80entries','Combined 80 entries'),('All95entries','All 95 entries'),('fixed135Mmodel','fixed 135M model'),('sampling.8/.9','sampling .8/.9'),('after305','after 305'),('checkedfive-entrywindows','checked five-entry windows'),('old305installer','old installer for 305'),('beyond400is','beyond 400 is')]:handoff=handoff.replace(p,q)
 (ROOT/'CURRENT_HANDOFF.md').write_text(handoff)
 orientation=f'''# Orientation: continuous garden paused at400

5 November2026. [Handoff](../CURRENT_HANDOFF.md), [report](../evaluation/discovery-continuity-to-400-v1/REPORT.md), [checks](../evaluation/discovery-continuity-to-400-v1/CHECKS.json), [resume](../evaluation/discovery-continuity-to-400-v1/RESUME.md).

Active `world_routine.py` / `discovery-play-patch-v1` / `ENVIRONMENT_DISCOVERY_PATCH_V1.json`. Same primary at400, paused, no model job/lock. Verifier{x['verification']}passes352generations+48origin. All16five-entrywindows passed across320→370and the conditionally authorized370→400extension. Old320/370notebook prefixes and immutable source records preserved. No reset or condition change.

Combined80entries: {a['world_requests']}world requests, {a['legacy_executions']}legacy executions, number{x['world_number']}; stops{a['stop_kinds']}, tokens{a['generated_tokens']}. Text repetition and copied/incorrect world or status descriptions remain unverified model text, not actual state changes or learned rules. Same weights/settings, zero training or paid inference API. Latest report separates facts, cases and limits.

Next authorized block can retainfive-entrychecks with broader summaries. Do not rerun finished drivers, the old305installer, reset the number, merge a host demo, or silently retry a plan. No run beyond400remains active.
'''
 for p,q in [('at400','at 400'),('November2026','November 2026'),('Verifier'+x['verification']+'passes352generations+48origin','Verifier '+x['verification']+' passes 352 generations plus 48 origin entries'),('All16five-entrywindows','All 16 five-entry windows'),('across320→370and','across 320→370 and'),('authorized370→400extension','authorized 370→400 extension'),('Old320/370notebook','Old 320/370 notebook'),('Combined80entries','Combined 80 entries'),('retainfive-entrychecks','retain five-entry checks'),('old305installer','old installer for 305'),('beyond400remains','beyond 400 remains')]:orientation=orientation.replace(p,q)
 (ROOT/'sync/CURRENT_ORIENTATION.md').write_text(orientation)
 index='''# Current research index

5 November2026. [Handoff](../CURRENT_HANDOFF.md), [design synthesis](discovery-play-patch-v1/OVERVIEW.md).

| Shelf | Entry | Interpretation |
|---|---|---|
| Latest continuation to400 | [Report](discovery-continuity-to-400-v1/REPORT.md), [checks](discovery-continuity-to-400-v1/CHECKS.json), [resume](discovery-continuity-to-400-v1/RESUME.md) | Active primary400paused; latest verifier in handoff; six checked windows after review at370 |
| Original50-entryblock | [Report](discovery-continuity-50-v1/REPORT.md), [review](discovery-continuity-50-v1/REVIEW_370.json), [cases](discovery-continuity-50-v1/CASE_NOTES.md) |320→370, ten checks; ordinary copying/repetition, false world/status descriptions checked against actual host records |
| Discovery introduction | [Report](discovery-introduction-15-v1/REPORT.md) | Historical305→320; same primary; earlier active status superseded |
| Discovery patch build | [Report](discovery-play-patch-v1/REPORT.md), [overview](discovery-play-patch-v1/OVERVIEW.md) | Historical prepared-only host tests at305; installed afterward; engine/demo retained unchanged |
| Stop visibility installation | [Report](generation-boundary-visibility-v1/REPORT.md) | First experienced jointly with world at305; not a separate causal study |
| Overlap review | [Report](pre-resume-overlap-review-v1/REPORT.md) | Historical305review; reuse measures are not reasoning metrics |
| Fundamental-shelf season | [Report](fundamental-seeds-100-v1/REPORT.md) |205→305; one executed calculator action; old renderer retained for replay |
| Previous continuity | [Report](continuity-155-to-205-v1/REPORT.md) |155→205; repeated simple tool example, preserved history |
| Descriptive zoom | [Report](fifty-entry-descriptive-zoom-v1/REPORT.md) | Historical155observations, not a new phase claim |
| Carrier/intervention lessons | [Soil robustness](soil-reset-robustness-v1/REPORT.md) | Constructed-system attribution limits, not proof of this model's memory mechanism |
| Training/binding caution | [Decision comparison](decision-loss-comparison-v1/REPORT.md) | Format success does not establish semantic binding |
| Prior queues/history | [Previous map](discovery-continuity-50-v1/before/CURRENT_RESEARCH_MAP.md), [earlier catalog](fundamental-seeds-100-v1/before/evaluation/CURRENT_RESEARCH_MAP.md) | Historical proposals retained; not all queues completed |

Same continuous external environment. No reset, new seed/rules, training or root review injected into these80entries. All raw prompts, outputs and actions retained. Interpret copied world/metadata text through actual host receipts; do not promote it to state or success. A future explicit control diagnostic remains a proposal, not a result or a condition silently added here. Latest handoff and current verifier supersede old status descriptions. Archived navigation keeps original bytes; its relative links belong to original file locations.
'''
 for p,q in [('November2026','November 2026'),('to400','to 400'),('primary400paused','primary paused at 400'),('at370','at 370'),('Original50-entryblock','Original 50-entry block'),('Historical305','Historical 305'),('at305','at 305'),('Historical155observations','Historical observations at 155'),('these80entries','these 80 entries')]:index=index.replace(p,q)
 (ROOT/'evaluation/CURRENT_RESEARCH_MAP.md').write_text(index)
 print('Current navigation synced to400; old snapshots preserved.')
if __name__=='__main__':main()
