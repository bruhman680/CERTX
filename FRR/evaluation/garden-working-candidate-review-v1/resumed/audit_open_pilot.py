"""Data-only audit of the clean paused pilot. Never opens a guest world."""
from pathlib import Path
import hashlib, json
from audit_retained import audit_store, read

H = Path(__file__).resolve().parent
C = H.parents[1] / 'minimal-garden-candidate-v1'
P = H.parents[1] / 'final-garden-contract-v1'
store = C/'run'
plan = read(C/'OPEN_PILOT_PLAN.json')
state = read(store/'STATE.json')
assert state['paused'] and state['turn']==12 and state['human_entry']==1562
assert read(store/'CONTROL_TASKS.json')=={}
assert plan['control_tasks']=={} and plan['maximum_model_replies']==12 and plan['blocks']==[4,8]
audit = audit_store(store)
messages = read(store/'INITIAL_MESSAGES.json')
initial = json.loads(json.dumps(messages))
assert initial[0]=={'role':'system','content':''}
events=[]
for turn in range(1,13):
    row = read(store/'events'/f'{turn:06d}.json')
    raw = read(store/'raw'/f'{turn:06d}.json')
    saved_plan = read(store/'plans'/f'{turn:06d}.json')
    assert raw['messages']==messages==saved_plan['messages']
    assert raw['input_token_ids']==saved_plan['input_token_ids']
    assert raw['decoder']=='greedy_argmax'
    assert len(raw['input_token_ids'])<=7936 and len(raw['generated_token_ids'])<=256
    assert row['stop']==raw['stop']
    messages.extend([{'role':'assistant','content':row['text']},{'role':'user','content':row['feedback']}])
    events.append(row)
original=read(store/'REFERENCE_INVENTORY.json')
current={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest()
         for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
assert original==current
assert read(P/'run/STATE.json')['paused'] and read(P/'run/STATE.json')['next_entry']==1550
first=read(store/'INITIAL_WORLD.json')
final=read(store/'world/bundles'/read(store/'world/STATE.json')['bundle'])
b,a={x[0]:x for x in first['entries']},{x[0]:x for x in final['entries']}
changed=[name for name in sorted(set(a)|set(b)) if a.get(name)!=b.get(name)]
result={'status':'pass','date':'2026-11-09 America/Chicago','review_model_calls':0,'guest_actions':0,
    'closed_pilot_audit':audit,'pilot_turns':12,'candidate_label':1562,'parent_reference':1550,
    'canonical_files_unchanged':len(current),'no_control_tasks':True,
    'full_actual_messages_reconstructed':True,'repeated_directory_injection':False,
    'complete_cell_counts':[e['cell_count'] for e in events],
    'token_cap_replies':sum(e['stop']=='token_limit' for e in events),
    'eos_replies':sum(e['stop']=='eos' for e in events),
    'distinct_texts':len({e['text'] for e in events}),'changed_world_paths':changed,
    'scope':'Open observation with no productivity gate. Foundation I/O competence comes from separately labeled prompted diagnostics, not these open outputs. No emergence, general reasoning or autonomous-learning claim.'}
with (H/'OPEN_PILOT_RETAINED_AUDIT.json').open('x') as f:
    json.dump(result,f,indent=2)
    f.write('\n')
report=f'''# Independent open-pilot review

9 November 2026, America/Chicago. Read-only retained-evidence review after the planned 4+8 pilot. This reviewer made zero model calls, ran no guest operation, and changed no candidate or reference state. Data-only audit source and JSON results are retained alongside this note.

The candidate is cleanly paused at its turn12 (lineage label1562), parent1550. The reference remains paused at1550 and all {len(current)} reference phase files are unchanged. All committed event/receipt/bundle/object chains pass; exact raw replies are linked to authoritative batches, model input messages and saved plans. The initial source pins remain unchanged.

CONTROL_TASKS is empty. The pilot initial mechanics and broad invitation are followed only by actual assistant replies and their factual consequence messages, including declared blank successful-note feedback. No new directory observation, question, investigator grade, summary or hand-selected memory was inserted. This verifies the promised contact policy for these twelve turns, not absence of causal influence from the initial framing or full-history replay.

Observed complete-cell counts: {result['complete_cell_counts']}. Stops: {result['token_cap_replies']} token caps and {result['eos_replies']} EOS. Distinct raw texts: {result['distinct_texts']}. Changed world paths: {changed}. No useful action or novelty was required to permit continuation. Incomplete cells remained writing under the predeclared law; nothing was completed, dedented, repaired or promoted to an action by the observer.

The operational I/O foundation is supported by the separately labeled framing-pair diagnostics: new model cells wrote real37and later retrieved it after fresh process/world restoration in the minimal-framing condition. That result must not be attributed to this open pilot or generalized into dependable task performance under the standard initial framing. The standard diagnostic also demonstrated real partial effects and native errors, including later truncation of an earlier successful write.

Taken together with the runtime tests and source review, the implementation is a usable bounded computational-notebook foundation: writing, declared actions, real consequences, persistent supported state, truthful failures, clean pause/resume and external evidence are available. This pilot does not show spontaneous file work, emergence, general competence, autonomous repair, weight learning, or an inevitable next developmental phase.

Activation may identify this explicitly as a new version inheriting the1550filesystem with a declared context reset, cell grammar, body and memory policy. Preserve the old active pointer and all reference evidence in the lineage. Do not call it an unchanged frozen continuation, an infinite-memory world, or a Conway-sized specification of all inherited Python/Linux behavior.
'''
with (H/'OPEN_PILOT_REVIEW.md').open('x') as f:
    f.write(report)
print(json.dumps(result))
