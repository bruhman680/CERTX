"""Refresh external documentation/manifests after a completed, audited window."""
from pathlib import Path
import json,hashlib
R=Path('/workspace/frr');H=Path(__file__).resolve().parent;P=R/'evaluation/chosen-persistence-prototype-v1';D=P/'candidate'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

if __name__=='__main__':
    r=read(H/'RESULTS.json');assert r['status']=='pass';start=r['start_turn'];end=r['end_turn'];count=r['actual_model_calls_this_window']
    assert not (D/'PENDING.json').exists() and not (D/'RUN.lock').exists()
    rows=r['rows'];first=rows[0];last=rows[-1]
    first_raw=read(D/f'raw/{start+1:06d}.json');last_raw=read(D/f'raw/{end:06d}.json')
    copied=r['literal_last_user_message_copies'];ops=r['actual_model_cell_operations_this_window'];next_tokens=r['exact_next_input_tokens']
    summary=f"{count} actual replies{start+1}–{end}; {copied} exact latest-user-message copies; {ops} executed cells; {r['end_world_entries']} supported world entries; operation step{r['end_world_step']}."
    handoff=f'''# Resume the same chosen-persistence FRR candidate at{end}

Read REPORT.md, RESULTS.json and ../chosen-persistence-prototype-v1/candidate/STATE.json and CONTRACT.json. Primary target remains the new pretrained-model + FRR world; old retrieval/label/repair queues are parked. Main1630 is separate and unchanged.

{summary} Contract, prior records, FRR, body, laws, sensing and full-history policy unchanged. All audits pass, weights unchanged. Candidate is paused at{end}; stop_reason={r['stop_reason']!r}; no live pending/lock/background generation. Exact next input{next_tokens}/7936tokens. These dependent observations are not independent replications or evidence of a permanent plateau/learning.

Proposed next bounded window up to25 under the same contract, not queued. Input and observation capacity can pause earlier; do not hide truncation or silently clear a stop. Full history stays external and all actual pairs stay in immediate input until the existing bound.

```sh
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/chosen-persistence-prototype-v1/session.py audit
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/chosen-persistence-prototype-v1/session.py run --budget 25
```

Never rerun prepare, clear pending to replay, use legacy receive_notebook, change prompts after quiet output or import fixture solutions. Model-chosen code is the only world-write route; observer retention is external. Errors and non-action are data, not quality gates. Synthetic blocked test fixtures remain outside candidate. Candidate count is not a main counter.
'''
    report=f'''# Same candidate continued from{start} to{end}

17 November2026, America/Chicago. {summary} The user authorized up to25 replies toward38. Actual outcome and any boundary are recorded without resetting the world. Main1630 remains preserved.

## Contract and observations

No new seed, task, correction, reward, source/body/FRR/law/sensing change or context pruning. The new candidate's original contract remains fixed: compact FRR plus mechanical laws, code-only chosen filesystem writes, complete external records, truthful directory observations and real cell receipts. All actual native-role pairs remain in context within7936inputtokens. No automatic world notebook append occurs.

This window has{copied}/{count} exact copies of the latest supplied user packet. Output token counts range{min(x['output_tokens'] for x in rows)}–{max(x['output_tokens'] for x in rows)}; all stop values are{sorted(set(x['stop'] for x in rows))}. Inputs grow{first['input_tokens']}→{last['input_tokens']}; the exact next input is{next_tokens}tokens. Full rows/raw data are external, not pasted into operator context after every reply. Stored post-final-reply feedback is prepared for the next call, not already consumed.

Actual cell operations{ops}, supported world entries at end{r['end_world_entries']}, world step{r['end_world_step']}. No automatic world notes. Where no operation occurs, there is no action-error/repair or artifact-reuse opportunity to score. Quiet copying is not proof of internal reasoning state, permanent plateau, inability or growth. No FRR efficacy estimate follows from this single continuous condition.

## Computation and continuity

Recorded generation time is{first_raw['seconds']:.2f}seconds at the first window input and{last_raw['seconds']:.2f}seconds at the last. These are observations of this CPU/eager run with growing full context, not a universal benchmark or a reason to prune it secretly. The retained source/model/runtime limits remain the declared ones.

PLAN.json captured the before-state, contract hash and all previous raw/plan/record/observation/snapshot hashes. All remain unchanged. The source/main/pointer/tensor guards and completed invocation audit pass; supplemental readout revalidates messages/IDs/decoding, parser/effect records, authentic observations/receipts, state/hash ancestry and next input. Cleanly paused at{end}, stop_reason={r['stop_reason']!r}, no live pending marker or lock. The synthetic blocked mechanics-test fixture is separate, not an unresolved candidate action.

Current README/status/handoff/manifest are refreshed; their previous bytes are retained under before/. Original initial-pilot and first-continuation records remain historical. The current candidate continues that same trajectory rather than replacing a branch or counting repeated prompts as independent samples.

## Next window

A further bounded window up to25 is proposed under the unchanged contract, not scheduled. Exact input/observation caps still apply and may end a future budget early. Preserve quiet behavior and zoom into any actual transition without turning observer judgments into model instructions. New seeds, dynamics, context policies or promotion are separate explicitly recorded choices. Older retrieval/alias/repair queues stay parked.
'''
    (H/'REPORT.md').write_text(report);(H/'NEXT_SESSION.md').write_text(handoff)
    (P/'NEXT_SESSION.md').write_text(handoff.replace('Read REPORT.md, RESULTS.json','Read ../chosen-persistence-continuation-v2/REPORT.md, ../chosen-persistence-continuation-v2/RESULTS.json',1))
    (P/'README.md').write_text(f'''# Chosen-persistence FRR garden: current candidate{end}

17 November2026, America/Chicago. {summary} [Latest report](../chosen-persistence-continuation-v2/REPORT.md), [handoff](NEXT_SESSION.md), [original build evidence](REPORT.md). Main remains1630 and unchanged; the candidate is a distinct fresh world with its own turn count.

Ordinary writing is archived externally. Only complete exact Python/shell cells change /world. Files persist across replies; transient processes/variables/cache do not. Compact FRR and mechanical laws, body, observation and finite full-context policy are frozen in candidate/CONTRACT.json. No task, reward, score, solution or autonomous clock is added. Ten operator mechanics checks and the original split1+2 pilot are retained.

Candidate is paused at{end}, stop_reason={r['stop_reason']!r}, next exact input{next_tokens}/7936tokens. No live pending/lock/background model run. A further window up to25 is proposed, not queued:

```sh
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/chosen-persistence-prototype-v1/session.py audit
/workspace/cache_backend_venv/bin/python /workspace/frr/evaluation/chosen-persistence-prototype-v1/session.py run --budget 25
```

Do not rerun prepare or clear pending to force replay. No hidden history pruning; capacity stops honestly. Unknown session outcomes require explicit forensic reconciliation. World-prefix recovery alone does not reconcile model-session history. The intentionally blocked unknown-marker mechanics fixture is outside the candidate, and its synthetic marker represents no actual attempted action. Original build/report/protocol, pilot summary and all raw histories remain preserved. Earlier current documentation is archived in continuation/before/ records and Git history.
''')
    status=read(H/'before/prototype_STATUS.json');status.update(status='continuous_candidate_window_complete',date='2026-11-17 America/Chicago',candidate_turn=end,actual_model_calls=end,last_continuation_calls=count,world_step=r['end_world_step'],world_entries=r['end_world_entries'],candidate_paused=True,candidate_pending=False)
    (P/'STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
    scope=read(H/'before/ACTIVE_RESEARCH_SCOPE.json');scope.update(date='2026-11-17 America/Chicago',status=f'same chosen-persistence candidate paused at{end} after bounded continuation',handoff='evaluation/chosen-persistence-continuation-v2/NEXT_SESSION.md',latest_report='evaluation/chosen-persistence-continuation-v2/REPORT.md',candidate_turn=end,next_direction='continue same candidate with frozen contract for proposed up to25 replies; no run queued',model_calls_queued=False)
    (R/'sync/ACTIVE_RESEARCH_SCOPE.json').write_text(json.dumps(scope,indent=2)+'\n')
    for path,link in [(R/'sync/CURRENT_ORIENTATION.md','../evaluation/chosen-persistence-continuation-v2/'),(R/'evaluation/CURRENT_RESEARCH_MAP.md','chosen-persistence-continuation-v2/')]:
        old=(H/'before'/path.name).read_text();assert path.read_text()==old
        intro=f'''# Current checkpoint — same chosen-persistence FRR candidate{end}

17 November2026, America/Chicago. [Report]({link}REPORT.md), [results]({link}RESULTS.json), [handoff]({link}NEXT_SESSION.md). Newer pretrained-model + FRR world stays primary; old retrieval/label/repair studies stay parked.

{summary} No automatic world notes. Input{first['input_tokens']}→{last['input_tokens']}; next exact input{next_tokens}/7936. Contract, previous records, body/weights/FRR/laws/sensing and full-context policy unchanged; no reset/new task/seed/hint/reward. Recorded replies are dependent trajectory data, not independent replications or a learning/plateau claim. External archive retains everything without making it a world file.

Run/supplemental audits and before hashes pass. Main1630/source/ACTIVE_GARDEN_PHASE unchanged. Candidate cleanly paused at{end}, stop_reason={r['stop_reason']!r}, no live pending/lock/background inference. Earlier current documentation/manifests/nav/scope retained under this window's before/. Synthetic blocked mechanics fixture is not a live candidate action. Proposed next up to25 under same contract, not queued; declared input/observation limits may stop earlier, never silent pruning.

Previous navigation follows unchanged.

---

'''
        path.write_text(intro+old)
    pm={str(x.relative_to(P)):sha(x) for x in sorted(P.rglob('*')) if x.is_file() and '__pycache__' not in x.parts and x!=P/'MANIFEST.json'}
    (P/'MANIFEST.json').write_text(json.dumps({'status':'prototype-current-checkpoint-artifact-manifest','candidate_turn':end,'previous_manifest_preserved':'../chosen-persistence-continuation-v2/before/prototype_MANIFEST.json','sha256':pm},indent=2,sort_keys=True)+'\n')
    hm={str(x.relative_to(H)):sha(x) for x in sorted(H.rglob('*')) if x.is_file() and '__pycache__' not in x.parts and x!=H/'MANIFEST.json'}
    (H/'MANIFEST.json').write_text(json.dumps({'status':'completed-window-artifact-manifest','prototype_checkpoint_manifest_sha256':sha(P/'MANIFEST.json'),'sha256':hm},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'finalized','candidate_turn':end,'actual_model_calls_this_window':count}))
