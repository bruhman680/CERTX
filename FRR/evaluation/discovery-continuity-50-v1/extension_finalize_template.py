"""Final evidence for the separately authorized370→400extension, plus combined80-entrysummary."""
from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment'
def main():
 x=json.loads((R/'CHECKPOINT_400.json').read_text());assert x['status']=='pass' and x['calls']==30 and x['next_step']==400;assert (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists() and not (R/'BLOCK.lock').exists()
 rows=[json.loads((ENV/'events'/f'{i:06d}.json').read_text()) for i in range(370,400)];combined=[json.loads((ENV/'events'/f'{i:06d}.json').read_text()) for i in range(320,400)];lifetime=[json.loads(p.read_text()) for p in sorted((ENV/'events').glob('*.json')) if int(p.stem)>=305]
 sessions=[json.loads(p.read_text()) for p in (ENV/'sessions').glob('*.json')];sessions=[s for s in sessions if s['start_step']>=370];assert len(sessions)==6 and sum(s['calls'] for s in sessions)==30;assert all(s['weights_unchanged'] and s['training_updates']==0 for s in sessions)
 resources=[json.loads(line) for s in sessions for line in (ENV/'sessions'/f"{s['session']}_RESOURCE.jsonl").read_text().splitlines()];assert all(r['working_estimate']<r['working_limit'] for r in resources)
 assert all(r['environment_version']=='discovery-play-patch-v1' and 'OPTIONAL PLAY PATCH (actual host world)' in r['prompt'] for r in rows)
 checkpoints=[json.loads((R/f'CHECKPOINT_{n}.json').read_text()) for n in range(375,401,5)];assert all(c['status']=='pass' for c in checkpoints)
 first=ROOT/'evaluation/discovery-continuity-50-v1';first_checks=json.loads((first/'CHECKS.json').read_text());assert first_checks['calls']==50 and first_checks['status']=='pass'
 before=json.loads((first/'PRIMARY_BEFORE.json').read_text());prefix=b''.join((ENV/'NOTEBOOK.jsonl').read_bytes().splitlines(keepends=True)[:320]);assert hashlib.sha256(prefix).hexdigest()==before['evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl']
 def describe(subset):
  world=[r for r in subset if r['host_result']['kind']=='play_patch_receipt'];return dict(calls=len(subset),host_kinds=dict(Counter(r['host_result']['kind'] for r in subset)),world_requests=len(world),world_executions=sum(bool(r['host_result']['executed']) for r in world),world_state_changes=sum(r['host_result']['before']!=r['host_result']['after'] for r in world),legacy_executions=sum(bool(r['host_result'].get('executed')) for r in subset if r['host_result']['kind']!='play_patch_receipt'),stop_kinds=dict(Counter(r['stop'] for r in subset)),generated_tokens=sum(len(r['generated_token_ids']) for r in subset),unique_reply_texts=len(set(r['text'] for r in subset)))
 evidence={k:v for k,v in x.items() if k!='events'};evidence.update(total_history_entries=400,total_saved_generations=352,origin_entries=48,checkpoints=[dict(cursor=c['next_step'],verification=c['verification']) for c in checkpoints],extension=describe(rows),combined_320_to_400=describe(combined),lifetime_since_305=describe(lifetime),frequent_combined_replies=[dict(text=t,count=c) for t,c in Counter(r['text'] for r in combined).most_common(10)],max_input_tokens=max(len(r['input_token_ids']) for r in rows),max_working_bytes=max(r['working_estimate'] for r in resources),working_limit=resources[0]['working_limit'],generation_seconds=sum(r['seconds'] for r in rows),condition_changes=[],model_weights_unchanged=True,training_updates=0,paid_inference_api_calls=0,old_320_notebook_exact_prefix_also_preserved=True)
 (R/'CHECKS.json').write_text(json.dumps(evidence,indent=2)+'\n');(R/'SESSIONS.json').write_text(json.dumps(sessions,indent=2)+'\n')
 index=[]
 for r in combined:index.append(dict(step=r['step'],resulting_count=r['step']+1,host_kind=r['host_result']['kind'],stop=r['stop'],output_tokens=len(r['generated_token_ids'])))
 (R/'COMBINED_EVENT_INDEX.json').write_text(json.dumps(index,indent=2)+'\n')
 allchecks=first_checks['checkpoints']+evidence['checkpoints'];table='\n'.join(f"| {c['cursor']} | {c['verification']} | pass |" for c in allchecks);allstats=evidence['combined_320_to_400'];ext=evidence['extension']
 report=f'''# Continuing to400: 50entries, review, then30more

5 November2026. **Same continuous primary, paused at400.** Active runner `world_routine.py`, manifest `ENVIRONMENT_DISCOVERY_PATCH_V1.json`, environment version `discovery-play-patch-v1`. No reset, changed rules, new seeds, root commentary injected into the model, or substituted primary.

## Two preserved blocks

The original [50-entryblock](../discovery-continuity-50-v1/REPORT.md) ran320→370in tenfive-entrywindows. At370we completed its report and reviewed actual host actions, output families, resources and integrity. The [recorded review](../discovery-continuity-50-v1/REVIEW_370.json) found the observations ordinary for this run and all checks passing. That satisfied the user's [conditional authorization](../discovery-continuity-50-v1/EXTENSION_AUTHORIZATION.json) for another30entries. This second block ran370→400in sixfive-entrywindows, with the same environment.

The review was an operational continuation decision, not a statistical emergence test. It did not treat passing hashes as proof of good reasoning, or non-use of tools as proof of incapacity. Both blocks and their original boundaries remain separately recorded.

## Observations

Across all80newentries: host kinds `{allstats['host_kinds']}`; world requests{allstats['world_requests']}, executed world requests{allstats['world_executions']}, actual world-number changes{allstats['world_state_changes']}, executed legacy requests{allstats['legacy_executions']}. Final world number:{x['world_number']}.

Stops across80entries: `{allstats['stop_kinds']}`; total generated tokens{allstats['generated_tokens']}; exact distinct reply strings{allstats['unique_reply_texts']}. The30-entryextension alone produced{ext['generated_tokens']}tokens, with host kinds `{ext['host_kinds']}` and stops `{ext['stop_kinds']}`.

The structured host receipts determine what actually happened. Numbers, currency strings, narrative claims, command mentions or host-shaped headings inside generated text do not establish execution or a changed reward function. An end token is not proof of a completed or correct thought; a cap is the unchanged96-token boundary, not a task-failure judgment.

The world view and controls were present in every new input. There have now been95entries since introduction at305; actual world requests over that whole interval:{evidence['lifetime_since_305']['world_requests']}. Availability is established. Whether the model can reliably use the controls under other conditions, form rule predictions, or transfer knowledge is not established by this unchanged observation run. No internal mental state, online neural learning or general reasoning improvement is inferred.

Full raw outputs, prompts, token IDs, RNG seeds, receipts and resource samples are preserved in the primary. Full extension reply text is in [checkpoint400](CHECKPOINT_400.json); the first50are in their own checkpoint370. [Combined event index](COMBINED_EVENT_INDEX.json) and [checks](CHECKS.json) provide a compact view without replacing raw history. Recurrence counts describe dependent outputs in one continuing history, not independent replications or a phase detector.

## Integrity

| Resulting count | Verification | Result |
|---|---|---|
{table}

All16windows passed complete version-aware replay before continuation. Final verifier{x['verification']}covers352saved generations plus48origin entries. Exact pre-block notebook prefixes at320and370are preserved. The extension checked{x['old_immutable_files_checked']}pre-existing primary files outside STATE,NOTEBOOK and CURRENT_VERIFY; all remained unchanged. No old event, plan, source or manifest was rewritten.

The same fixed135Mmodel and cached adapter were used, with sampling.8/.9, input8096/output96/native8192, the same seeds/curiosity invitation, charter, legacy tools and neutral feedback. Every session confirmed unchanged weights and zero training updates. The live world state derives from primary action receipts after305; the separate host demo never entered this history. External notebook continuity is not a claim of persistent neural hidden state.

The extension's maximum input was{evidence['max_input_tokens']}tokens. Its maximum working estimate was{evidence['max_working_bytes']}bytes, below the{evidence['working_limit']}-byte guard. Extension generation time was{evidence['generation_seconds']:.2f}seconds, a local runtime observation, not a billing claim or benchmark. No paid inference API, model download or new provisioning was used.

## Resume

At400,PAUSEis present, RUN.lock and the block lock are absent, and no model job is left running. No continuation beyond400occurred. On later authorization, continue using the installed active runner and passing current verifier; do not rerun the old305installer, reset the number, substitute a fresh notebook or merge a host demo. Keep five-entry integrity checks under broader reporting cadences and inspect actual changes when warranted.

No new scientific claim or condition change is required to end at this round boundary. The next observations should remain tied to actual actions and consequences, with repetition and non-use retained as data. Earlier reports remain historical records; the latest handoff and current pointer describe the active boundary.
'''
 for a,b in [('to400','to 400'),('50entries','50 entries'),('30more','30 more'),('November2026','November 2026'),('at400','at 400'),('50-entryblock','50-entry block'),('ran320→370in tenfive-entrywindows','ran 320→370 in ten five-entry windows'),('At370we','At 370 we'),('another30entries','another 30 entries'),('ran370→400in sixfive-entrywindows','ran 370→400 in six five-entry windows'),('all80newentries','all 80 new entries'),('across80entries','across 80 entries'),('The30-entryextension','The 30-entry extension'),('newtokens','new tokens'),('unchanged96-token','unchanged 96-token'),('been95entries','been 95 entries'),('at305','at 305'),('first50are','first 50 are'),('All16windows','All 16 windows'),('covers352saved','covers 352 saved'),('plus48origin','plus 48 origin'),('at320and370are','at 320 and 370 are'),('fixed135Mmodel','fixed 135M model'),('sampling.8/.9','sampling .8/.9'),('after305','after 305'),('PAUSEis','PAUSE is'),('beyond400occurred','beyond 400 occurred'),('old305installer','old installer for 305')]:report=report.replace(a,b)
 (R/'REPORT.md').write_text(report);print(json.dumps({k:v for k,v in evidence.items() if k not in ('frequent_combined_replies',)},indent=2))
if __name__=='__main__':main()
