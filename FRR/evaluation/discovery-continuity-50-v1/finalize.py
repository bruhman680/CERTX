"""Summarize a completed50-entry continuation without editing model history."""
from pathlib import Path
from collections import Counter
import json,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment'
def main():
 x=json.loads((R/'CHECKPOINT_370.json').read_text());assert x['status']=='pass' and x['calls']==50 and x['next_step']==370
 rows=[json.loads((ENV/'events'/f'{i:06d}.json').read_text()) for i in range(320,370)];sessions=[json.loads(p.read_text()) for p in (ENV/'sessions').glob('*.json')];sessions=[s for s in sessions if s['start_step']>=320];assert len(sessions)==10 and sum(s['calls'] for s in sessions)==50 and all(s['weights_unchanged'] and s['training_updates']==0 for s in sessions)
 resources=[json.loads(line) for s in sessions for line in (ENV/'sessions'/f"{s['session']}_RESOURCE.jsonl").read_text().splitlines()];assert all(r['working_estimate']<r['working_limit'] for r in resources)
 assert all(r['environment_version']=='discovery-play-patch-v1' and 'OPTIONAL PLAY PATCH (actual host world)' in r['prompt'] for r in rows)
 checkpoints=[json.loads((R/f'CHECKPOINT_{t}.json').read_text()) for t in range(325,371,5)];assert all(c['status']=='pass' for c in checkpoints)
 world=[r for r in rows if r['host_result']['kind']=='play_patch_receipt'];text_counts=Counter(r['text'] for r in rows);windows=[]
 for lo,hi in ((320,340),(340,360),(360,370)):
  subset=[r for r in rows if lo<=r['step']<hi];windows.append(dict(start=lo,end=hi,calls=len(subset),host_kinds=dict(Counter(r['host_result']['kind'] for r in subset)),stop_kinds=dict(Counter(r['stop'] for r in subset)),generated_tokens=sum(len(r['generated_token_ids']) for r in subset),unique_reply_texts=len(set(r['text'] for r in subset))))
 evidence={k:v for k,v in x.items() if k!='events'};evidence.update(total_history_entries=370,total_saved_generations=322,origin_entries=48,checkpoints=[dict(cursor=c['next_step'],verification=c['verification']) for c in checkpoints],all_inputs_contain_world_view=True,condition_changes=[],executed_world_requests=sum(bool(r['host_result']['executed']) for r in world),world_actions=dict(Counter(r['host_result']['action'] for r in world)),world_state_changes=sum(r['host_result']['before']!=r['host_result']['after'] for r in world),executed_legacy_requests=sum(bool(r['host_result'].get('executed')) for r in rows if r['host_result']['kind']!='play_patch_receipt'),unique_reply_texts=len(text_counts),most_frequent_reply_counts=[dict(text=t,count=c) for t,c in text_counts.most_common(5)],max_input_tokens=max(len(r['input_token_ids']) for r in rows),max_working_bytes=max(r['working_estimate'] for r in resources),working_limit=resources[0]['working_limit'],generation_seconds=sum(r['seconds'] for r in rows),model_weights_unchanged=True,training_updates=0,provider_api_calls=0,reporting_windows=windows)
 (R/'CHECKS.json').write_text(json.dumps(evidence,indent=2)+'\n');(R/'SESSIONS.json').write_text(json.dumps(sessions,indent=2)+'\n')
 table='\n'.join(f"| {w['start']}→{w['end']} | {w['calls']} | {w['host_kinds']} | {w['stop_kinds']} | {w['unique_reply_texts']} |" for w in windows)
 check_table='\n'.join(f"| {c['next_step']} | {c['verification']} | pass | {c['world_commands']} | {c['world_number']} |" for c in checkpoints)
 report=f'''# Unchanged discovery world: 320 → 370

5 November 2026. **Completed the authorized50-entry block; same primary paused at370.** Active runner `world_routine.py`, environment version `discovery-play-patch-v1`. No reset, new seeds, forced object actions or condition changes.

## Observations

There were50actual model generations, totaling{x['generated_tokens']}generated tokens. Host results: `{x['host_kinds']}`. Recognized world requests:{len(world)}; accepted/executed world requests:{evidence['executed_world_requests']}; actual number changes:{evidence['world_state_changes']}; final world number:{x['world_number']}. Executed legacy requests:{evidence['executed_legacy_requests']}. World actions/statuses are counted separately in [checks](CHECKS.json); malformed, blocked and accepted-unchanged actions must not be called discoveries.

Stops: `{x['stop_kinds']}`. A cap is a96-token generation boundary; an end token is not evidence of a complete/correct thought. Every new input included the real world view and controls. Availability does not establish meaningful use or a learned internal representation.

There were{evidence['unique_reply_texts']}distinct exact reply strings across50entries. Exact repeats, numeric answers, invented narratives, command mentions and imitation metadata are not by themselves evidence of success, failure, consciousness, emotion or rule learning. Conversely, reuse of a literal command could still execute a real action. Interpret actual receipts and consequences, rather than novelty of wording alone.

## Broad windows

| Window | Entries | Host kinds | Stop kinds | Exact distinct replies |
|---|---|---|---|---|
{table}

Full generated reply text is retained in [checkpoint370](CHECKPOINT_370.json) and the canonical raw events. These counts are descriptive, not a predeclared phase detector or an independent experimental replication. The same history feeds subsequent inputs; outputs are not independent samples. Host-authored examples and the separate demo were not inserted into this run.

## Integrity and persistence

| Resulting count | Verification | Status | Cumulative world requests in this block | Number |
|---|---|---|---|---|
{check_table}

All ten five-entry windows passed complete version-aware prompt/token/action replay before continuation. Final verification{x['verification']}covers322saved generations plus48origin entries. The pre-block320-entry notebook remains an exact byte prefix. All{x['old_immutable_files_checked']}pre-existing primary files other than the three intended projections/pointers remain unchanged. No old event, prompt plan, policy manifest or source version was overwritten.

All ten inference sessions confirmed unchanged base/adapter weights and zero training updates. Model and cached adapter, sampling.8/.9, input8096/output96/native8192, neutral feedback, user invitation, seed shelf, tools, world rules and history access stayed fixed. The world number derives from actual primary receipts after305; external continuity does not imply persistent neural state or online learning.

Maximum input:{evidence['max_input_tokens']}tokens. Maximum recorded working estimate:{evidence['max_working_bytes']}bytes, below the{evidence['working_limit']}-byte guard. Generation time:{evidence['generation_seconds']:.2f}seconds, a local runtime observation, not a billing claim or performance benchmark. No paid provider API, model download, training or provisioning occurred.

## Continue

The requested block ends here, at370with PAUSE present and no model job or lock left behind. No continuation beyond370was started. Continue the same installed runner on a later authorization; do not run the historical305installer or substitute a reset plot. Keep five-entry integrity checks even if discussion uses broader blocks. Preserve ordinary and failed outputs alike. If a later probe or environmental adjustment is chosen, introduce it as a new recorded condition rather than revising these observations.

[Plan](PLAN.json), [checks](CHECKS.json), [sessions](SESSIONS.json), [previous introduction](../discovery-introduction-15-v1/REPORT.md), [world design](../discovery-play-patch-v1/OVERVIEW.md). Prior navigation is archived under before/. Current navigation should describe370; older reports remain unchanged records of their own boundaries.
'''
 # Readability of numeric placeholders does not affect source records.
 for a,b in {'authorized50-entry':'authorized 50-entry','at370':'at 370','were50actual':'were 50 actual','totaling'+str(x['generated_tokens']):'totaling '+str(x['generated_tokens']),'generated tokens':' generated tokens','requests:':'requests: ','changes:':'changes: ','number:':'number: ','were'+str(evidence['unique_reply_texts'])+'distinct':'were '+str(evidence['unique_reply_texts'])+' distinct','across50entries':'across 50 entries','checkpoint370':'checkpoint370','verification'+x['verification']+'covers322saved':'verification '+x['verification']+' covers 322 saved','plus48origin':'plus 48 origin','pre-block320-entry':'pre-block 320-entry','All'+str(x['old_immutable_files_checked'])+'pre-existing':'All '+str(x['old_immutable_files_checked'])+' pre-existing','sampling.8/.9':'sampling .8/.9','after305':'after 305','at370with':'at 370 with','beyond370was':'beyond 370 was','historical305installer':'historical installer for 305','describe370':'describe 370'}.items():report=report.replace(a,b)
 (R/'REPORT.md').write_text(report);print(json.dumps({k:v for k,v in evidence.items() if k!='most_frequent_reply_counts'},indent=2))
if __name__=='__main__':main()
