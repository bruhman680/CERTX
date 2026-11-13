"""External report for the actual unchanged five-reply continuation."""
from pathlib import Path
import json,hashlib,collections
H=Path(__file__).resolve().parent;C=H.parent/'minimal-garden-candidate-v1';R=C/'run'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    before=json.loads((H/'BEFORE_INVENTORY.json').read_text());state=json.loads((R/'STATE.json').read_text())
    assert state['human_entry']==1567 and state['paused']
    changed=[p for p,v in before.items() if not (C/p).is_file() or sha(C/p)!=v]
    assert set(changed)=={'run/STATE.json','run/world/STATE.json'}
    assert not any((R/p).exists() for p in ['RUN.lock','PENDING.json'])
    assert not any((R/'world'/p).exists() for p in ['LOCK.json','PENDING.json','BATCH_PENDING.json'])
    prior_texts={json.loads(p.read_text())['text'] for p in sorted((R/'raw').glob('*.json')) if int(p.stem)<=12}
    rows=[];table=[]
    for n in range(13,18):
        raw=json.loads((R/'raw'/f'{n:06d}.json').read_text());event=json.loads((R/'events'/f'{n:06d}.json').read_text())
        batch=json.loads((R/'batches'/f'{n:06d}.json').read_text())
        code=[o for o in batch['operations'] if o['channel']!='note']
        row={'entry':1550+n,'turn':n,'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),
           'stop':raw['stop'],'complete_cells':event['cell_count'],
           'incomplete_fences':sum(not c['complete'] for c in batch['parsed']['cells']),
           'code_operations':len(code),'note_stored':batch['note_stored'],
           'matches_prior_reply_exactly':raw['text'] in prior_texts,
           'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),
           'feedback':event['feedback'],'boundary':event['boundary'],'text':raw['text']}
        rows.append(row)
        table.append(f"| {row['entry']} | {row['input_tokens']} | {row['output_tokens']} | {row['stop']} | {row['complete_cells']} | {row['note_stored']} | {row['matches_prior_reply_exactly']} |")
    sessions=[json.loads(p.read_text()) for p in (R/'sessions').glob('*_RESULT.json')]
    session=[x for x in sessions if x['start_turn']==12 and x['end_turn']==17]
    assert len(session)==1 and session[0]['model_calls']==5 and session[0]['reason']=='completed'
    summary={'start_entry':1562,'end_entry':1567,'actual_main_model_replies':5,'settings_changed':False,'diagnostic_import':False,
       'code_operations':sum(x['code_operations'] for x in rows),'complete_cells':sum(x['complete_cells'] for x in rows),
       'notebook_appends':sum(x['note_stored'] for x in rows),'distinct_new_reply_texts':len({x['text_sha256'] for x in rows}),
       'new_replies_matching_prior_text':sum(x['matches_prior_reply_exactly'] for x in rows),
       'changed_preexisting_paths':changed,'all_other_prior_candidate_files_unchanged':True,
       'paused':True,'pending_or_owned_lock':False,'session_result':session[0]}
    (H/'AFTER_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
    (H/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (H/'REPLIES.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    (H/'REPORT.md').write_text('''# Main garden resumed: 1562 → 1567

13 November 2026, America/Chicago. Five actual main-garden replies, not detached diagnostic loops. The same selected computational-notebook version resumed through its existing runner. Original reference 1550 remains preserved.

## What changed and what stayed fixed

The main run advanced from turn 12 to 17, corresponding to entries 1563–1567, and paused cleanly. The broad invitation, world laws, supported persistence, parser, resource bounds, greedy decoder, 256-token output cap, exact accumulating conversation and fresh KV per reply are unchanged. No sampled diagnostic output, world, random state, helper tool, hint, feedback rewrite or new instruction was imported. No training or paid model endpoint was used.

## All five replies

| Main entry | Input tokens | Output tokens | Stop | Complete cells | Notebook append | Exact match to a prior reply |
|---|---:|---:|---|---:|---|---|
'''+ '\n'.join(table)+'''

The table reports observable output and dispatch, not an accuracy score. The full new texts are retained in `REPLIES.json` and the canonical raw/event records. Repetitive or unfinished writing remains permitted and preserved. No conclusion about maturation, internal reasoning changes, consciousness or an inability to change follows from a five-reply block.

## Integrity and state

The runner checked model parameter digests, source pins and the old reference during the block, then reconstructed and verified the full actual run before pausing. `SUMMARY.json` retains its actual session result, next-input size and original input limit. `AUDIT.json`/`REVIEW.md` supply the independent read-only record audit once complete.

Every pre-existing candidate file remains byte-identical except the two expected current-state pointers, `run/STATE.json` and `run/world/STATE.json`. New raw replies, plans, event records, notebook objects, world checkpoints and session records were appended. The historical activation/build records and every prior reply remain unchanged. No unknown pending marker or owned run/world lock remains. The root phase pointer still selects the same version and contract.

The original reference at 1550, the detached sampled branches and their separate numbering remain intact. Current navigation points to this continuation; prior navigation snapshots are archived rather than rewritten as though this result had already happened.

## Next

Continue from **1567**, not from an older paused snapshot or a detached branch. A further bounded block can use the existing source and same settings, subject to the exact-context capacity check. No new competence claim or repair is required to keep observing. If a real code action, ordinary error or storage/capacity boundary appears, inspect its actual receipts; unknown effects retain their pending evidence and stop without replay.
''')
if __name__=='__main__':main()
