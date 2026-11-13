"""Report requested versus actual unchanged continuation; never assumes 50."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;C=H.parent/'minimal-garden-candidate-v1';R=C/'run'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    before=json.loads((H/'BEFORE_INVENTORY.json').read_text());initial=json.loads((H/'BEFORE_STATE.json').read_text())
    state=json.loads((R/'STATE.json').read_text());assert state['paused']
    start=initial['turn'];end=state['turn'];actual=end-start
    sessions=[json.loads(p.read_text()) for p in (R/'sessions').glob('*_RESULT.json')]
    matches=[s for s in sessions if s['start_turn']==start and s['end_turn']==end]
    assert len(matches)==1;session=matches[0];assert session['model_calls']==actual
    assert session['reason'] in ('completed','context_capacity','user_pause')
    changed=[p for p,v in before.items() if not (C/p).is_file() or sha(C/p)!=v]
    assert set(changed)<= {'run/STATE.json','run/world/STATE.json'}
    for p in ['RUN.lock','PENDING.json']:assert not (R/p).exists()
    for p in ['LOCK.json','PENDING.json','BATCH_PENDING.json']:assert not (R/'world'/p).exists()
    earlier={json.loads(p.read_text())['text'] for p in (R/'raw').glob('*.json') if int(p.stem)<=start}
    rows=[];table=[]
    for n in range(start+1,end+1):
        raw=json.loads((R/'raw'/f'{n:06d}.json').read_text());ev=json.loads((R/'events'/f'{n:06d}.json').read_text());b=json.loads((R/'batches'/f'{n:06d}.json').read_text())
        code=[o for o in b['operations'] if o['channel']!='note']
        row={'entry':1550+n,'turn':n,'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),
           'seconds':raw['seconds'],'stop':raw['stop'],'complete_cells':ev['cell_count'],'code_operations':len(code),
           'incomplete_fences':sum(not c['complete'] for c in b['parsed']['cells']),
           'note_stored':b['note_stored'],'matches_prior_text_exactly':raw['text'] in earlier,
           'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),'text':raw['text'],'feedback':ev['feedback'],'boundary':ev['boundary'],
           'code_receipts':[o['feedback'] for o in code]}
        assert row['input_tokens']<=7936
        rows.append(row)
        table.append(f"| {row['entry']} | {row['input_tokens']} | {row['output_tokens']} | {row['stop']} | {row['complete_cells']} | {row['note_stored']} | {row['matches_prior_text_exactly']} |")
    v=session['verification'];next_tokens=v['next_input_tokens']
    if session['reason']=='context_capacity':assert next_tokens>7936 and not v['next_input_within_capacity']
    ws=json.loads((R/'world/STATE.json').read_text());wb=json.loads((R/'world/bundles'/ws['bundle']).read_text())
    notebook=next(x for x in wb['entries'] if x[0]=='notebook.txt')
    summary={'requested_replies':50,'completed_replies':actual,'uncompleted_requested_replies':50-actual,
      'start_entry':initial['human_entry'],'end_entry':state['human_entry'],'reason':session['reason'],
      'paused':True,'next_input_tokens':next_tokens,'input_limit':7936,'within_capacity':v['next_input_within_capacity'],
      'context_tokens_not_removed':True,'source_or_model_settings_changed':False,'diagnostic_import':False,
      'complete_cells':sum(x['complete_cells'] for x in rows),'code_operations':sum(x['code_operations'] for x in rows),
      'notebook_appends':sum(x['note_stored'] for x in rows),'distinct_reply_texts':len({x['text_sha256'] for x in rows}),
      'replies_matching_prior_text':sum(x['matches_prior_text_exactly'] for x in rows),
      'generation_seconds_total':sum(x['seconds'] for x in rows),'changed_preexisting_paths':changed,
      'notebook_bytes':notebook[4],'supported_world_file_bytes':sum(x[4] for x in wb['entries'] if x[1]=='file'),
      'all_other_prior_files_unchanged':True,'pending_or_owned_lock':False,'session_result':session}
    (H/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (H/'AFTER_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
    (H/'REPLIES.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    status=f"Requested **50** replies; completed **{actual}**, advancing **{initial['human_entry']} → {state['human_entry']}**. Stop reason: `{session['reason']}`. Next input: **{next_tokens}/7936** tokens."
    (H/'REPORT.md').write_text('''# Requested fifty-reply main-garden block

13 November 2026, America/Chicago.

'''+status+'''

These are actual main-garden entries under the unchanged computational-notebook contract. The run was requested with `candidate.py resume --steps 50`; its declared boundary can stop it before fifty replies. The world, original broad invitation, exact accumulating conversation, greedy256 decoder, source pins, resource bounds and fresh-KV convention stayed fixed. No sampled branch, diagnostic hint, success grade or new instruction was imported. There was no training or paid endpoint.

## All actual replies

| Entry | Input tokens | Output tokens | Stop | Complete cells | Notebook stored | Exact prior-text match |
|---|---:|---:|---|---:|---|---|
'''+ '\n'.join(table)+'''

`REPLIES.json` contains all visible texts, token counts, timings and actual code receipts. `SUMMARY.json` distinguishes requested from actual counts. Writing is permitted and preserved; no output is discarded for being repetitive, unfinished or unproductive. Surface wording does not establish maturation or an internal reasoning mechanism.

## A context pause is different from lost history

The runner includes the entire actual conversation of this selected version in every new input, without summarizing or selecting a replay window. Its limit is 7,936 input tokens, reserving 256 output positions within an 8,192-position model. When the next input exceeds that limit, it pauses before generating; it does not trim history, enlarge the model, switch a memory policy or fabricate the remaining replies.

The conversation, notebook, world files, checkpoint chain and older reference remain stored. The bounded viewing window is full if stop reason is context_capacity; the data store has not disappeared. Context-token count and disk capacity are different constraints. KV reuse can avoid some repeated computation but does not by itself extend the declared positional/context limit.

When capacity is exceeded, an unchanged resume will stop again before another reply. Further continuity then needs a separately declared context/view policy, while preserving this original run and filesystem. That policy is not silently installed during this wind-down. The uncompleted portion is recorded as uncompleted, not scheduled in the background.

## Integrity and wind-down

The runner's final verification checks every actual input, decoded reply, event/raw/batch hash link, world effect and reconstructed current world, along with source pins, model digest and old reference preservation. A pass verifies retained history even when the next input is too large; it does not imply that the next generation fits. `AUDIT.json`/`REVIEW.md` provide the separate read-only audit when complete.

All prior candidate files are preserved byte-for-byte except the two mutable current-state pointers. New records and objects append history; historical activation/build files and original reference1550 are untouched. No unknown pending operation or owned lock remains at a clean pause. Current navigation is updated, with its previous versions archived exactly.

The run is settled and paused for the usage reset. There is no unattended continuation. Read this report, `SUMMARY.json`, the final state and the current phase pointer before any next session. Assess capacity/view options separately from the model's behavior; neither a successful action nor a preferred developmental stage is required to retain or observe its writing.
''')
if __name__=='__main__':main()
