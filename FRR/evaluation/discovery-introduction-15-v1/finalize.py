"""Assemble descriptive evidence and continuation records after cursor320verification."""
from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment'
def main():
 x=json.loads((R/'CHECKPOINT_320.json').read_text());assert x['status']=='pass' and x['next_step']==320
 rows=[json.loads((ENV/'events'/f'{i:06d}.json').read_text()) for i in range(305,320)]
 sessions=[json.loads(f.read_text()) for f in (ENV/'sessions').glob('*.json')];sessions=[s for s in sessions if s['start_step']>=305];assert len(sessions)==3 and sum(s['calls'] for s in sessions)==15 and all(s['weights_unchanged'] and s['training_updates']==0 for s in sessions)
 resources=[json.loads(line) for s in sessions for line in (ENV/'sessions'/f"{s['session']}_RESOURCE.jsonl").read_text().splitlines()]
 assert all(t['working_estimate']<t['working_limit'] for t in resources)
 assert all(z['environment_version']=='discovery-play-patch-v1' and 'OPTIONAL PLAY PATCH (actual host world)' in z['prompt'] for z in rows)
 evidence={k:v for k,v in x.items() if k!='events'};evidence.update(total_history_entries=320,total_saved_generations=272,origin_entries=48,checkpoints=[dict(cursor=t,verification=json.loads((R/f'CHECKPOINT_{t}.json').read_text())['verification']) for t in (310,315,320)],all_new_inputs_contain_world_view=True,unique_reply_texts=len(set(r['text'] for r in rows)),max_input_tokens=max(len(r['input_token_ids']) for r in rows),max_working_bytes=max(t['working_estimate'] for t in resources),working_limit=resources[0]['working_limit'],new_generation_seconds=sum(r['seconds'] for r in rows),model_weights_unchanged=True,provider_api_calls=0)
 (R/'CHECKS.json').write_text(json.dumps(evidence,indent=2)+'\n');(R/'SESSIONS.json').write_text(json.dumps(sessions,indent=2)+'\n')
 table='\n'.join(f"| {r['step']} | {r['step']+1} | {r['host_result']['kind']} | {r['stop']} | {len(r['generated_token_ids'])} |" for r in rows)
 report=f'''# Discovery introduction: same garden, 305 → 320

5 November 2026. **Completed 15 new model entries; paused at320.** Active version `discovery-play-patch-v1`, runner `../source-access-three-cycle-v1/world_routine.py`. This is the original continuous primary, with a versioned environmental addition at305, not a restarted/fork-substituted garden.

## What changed

The [prepared numeric patch](../discovery-play-patch-v1/REPORT.md) was introduced through its explicit installer. It added a persistent bounded number and A/B objects with LOOK/TOUCH controls. Transformation rules remain in observer code; input exposes controls and current state. No goal, reward, worked transformation or extra root guidance was added. Existing seeds, curiosity sentence, legacy tools, neutral feedback, sampling, model, adapter and generation limits were retained.

The model also experienced the previously installed stop-status visibility for the first time. This is therefore a combined experienced change, not a single-factor causal comparison. [Pre-run plan](PLAN.json), [activation log](ACTIVATION_LOG.txt), [design synthesis](../discovery-play-patch-v1/OVERVIEW.md).

## What happened

* {x['new_model_calls']} actual generations completed; all {x['host_kinds'].get('record_receipt',0)} resulted in ordinary-text record receipts.
* {x['world_commands']} recognized world commands executed. No LOOK/TOUCH transition or malformed-world-command response was observed. No legacy tool execution occurred.
* The world number remained **{x['world_number']}**. Its initial value staying unchanged is not evidence of a discovered rule.
* {x['stop_kinds'].get('token_limit',0)} replies reached the96-token cap; {x['stop_kinds'].get('eos',0)} ended with the model's end token. Total generated tokens: {x['generated_tokens']}. Neither stop kind is a correctness/completeness judgment.
* Every new input included the actual world view. Availability is established; meaningful use or an internal understanding is not established.

Outputs included numbers and number lists, seed-shelf-like language, narrative/OS-version fragments and notebook-shaped text. At zero-based step310, the model wrote a host-generation-status-style heading inside its own reply. At311, it wrote a monetary-reward claim. These are generated text, not actual host metadata, compensation, a changed reward function or evidence that a tool ran. The canonical event's host_result remains the authority. The first reply's standalone0 could match the visible world number or other numeric context; this contact cannot attribute it to world understanding.

No task score was assigned and no failed/non-use trial was replaced. Repetition, fiction and non-use remain part of the record. The model had permission to ignore the patch; non-use does not establish inability to operate it under every other condition. It also supplies no positive action-based evidence of discovery in this window. No emotion, awareness, phase transition or training improvement is inferred.

## Integrity and continuity

Activation passed full old-history replay at305 (0056). The three five-entry windows passed at310 (0057),315 (0058) and320 ({x['verification']}). Final replay covers **272 saved generations plus48 origin entries** under their original policy versions. The original305-entry notebook is an exact byte prefix of the current notebook. All905pre-existing primary files other than the three deliberately updated projections/pointers remain unchanged. Old event/prompt/manifest/source files were not edited.

The patch's state derives from actual committed primary receipts after305. The separate host-demo journal was not imported. Model weights and adapter digests stayed unchanged in all three sessions; no training, paid provider API, download or provisioning was performed. The maximum recorded working-memory estimate was {evidence['max_working_bytes']} bytes, below the {evidence['working_limit']}-byte guard. New inputs stayed within8096tokens (maximum {evidence['max_input_tokens']}). Generation time totaled {evidence['new_generation_seconds']:.2f}seconds; it is a local runtime observation, not a billing claim or benchmark.

[Final checks](CHECKS.json), [sessions](SESSIONS.json), checkpoint [310](CHECKPOINT_310.json), [315](CHECKPOINT_315.json), [320](CHECKPOINT_320.json). All raw prompts, token IDs, outputs, action receipts and resource samples remain under the primary's environment directory. The15newzero-based event files are000305through000319; the resulting entry count is320.

## Per-entry index

| Zero-based event | Resulting count | Host result | Stop | Output tokens |
|---|---|---|---|---|
{table}

This index is descriptive. Full reply text is retained in checkpoint320 and the canonical raw events; none is silently promoted to a factual account of the world.

## Next direction

Keep the same environment stable for an authorized larger continuation. Compose the existing cadence from at mostfiveentries per integrity check, with broad summaries around20entries and closer inspection if actual changes warrant it. There is no need to force object use or change rules in response to this short window. Longer observation can test whether use emerges; more entries alone would not prove understanding. If a later controlled grammar/affordance probe becomes useful, record it as a separate explicit condition rather than rewriting this run.

At320PAUSEis present, RUN.lock is absent, and no model job is left running. No continuation beyond320occurred in this contact. [Resume guide](RESUME.md). The prepared installer targets the historical305boundary and must not be rerun now; continue with the installed active runner. Existing earlier reports remain historical records, not current-status documents.

In garden terms: a new bed is open beside the old paths. Across these15entries, the small garden mostly continued scattering words and numbers along familiar-looking paths. We observed no step into the new bed yet. The fence, journal and old roots held; the next longer season can remain open without pretending the new plants have already grown.
'''
 (R/'REPORT.md').write_text(report)
 (R/'STATUS.md').write_text(f'# Completed and paused at320\n\n15newentries complete. Activeworld_routine.py/discovery-play-patch-v1, verifier{x["verification"]}passes. Sameprimary, worldnumber{x["world_number"]}, {x["world_commands"]}worldcommands. No job left running. See REPORT.md,CHECKS.json and RESUME.md. Prior in-progress state is preserved in the logs and publication history.\n')
 print(json.dumps(evidence,indent=2))
if __name__=='__main__':main()
