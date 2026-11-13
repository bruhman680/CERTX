"""Summarize actual framing-pair effects; does not run or edit the worlds."""
from pathlib import Path
import base64, hashlib, json
H=Path(__file__).resolve().parent
r=json.loads((H/'RESULT.json').read_text())
assert r['status']=='completed' and r['new_model_calls']==6 and r['source_pins_unchanged']

def read(p):return json.loads(Path(p).read_text())
def memory_at(store,step):
    b=read(store/'world/bundles'/f'{step:06d}.json')
    es=[e for e in b['entries'] if e[0]=='memory.txt']
    if not es:return None
    e=es[0]
    assert e[1]=='file'
    obj=read(store/'world/objects'/(e[3]+'.json'))
    data=base64.b64decode(obj['base64'],validate=True)
    assert hashlib.sha256(data).hexdigest()==e[3] and len(data)==e[4]
    return {'bytes':len(data),'sha256':e[3],'utf8':data.decode()}

timelines={}
for arm,a in r['arms'].items():
    store=H/arm/'run'
    items=[]
    for out in a['outcomes']:
        batch=read(store/'batches'/f"{out['turn']:06d}.json")
        for op in batch['operations']:
            if op['channel'] not in ('python','shell'):continue
            items.append({'turn':out['turn'],'world_step':op['step'],'channel':op['channel'],
                'source':op['source'],'receipt':op['receipt'],'memory_after':memory_at(store,op['step'])})
    timelines[arm]=items
with (H/'OPERATION_TIMELINE.json').open('x') as f:
    json.dump({'model_calls':0,'timelines':timelines,'scope':'Observer reads of retained per-operation snapshots; no new effects.'},f,indent=2)
    f.write('\n')
minimal=r['arms']['minimal']
standard=r['arms']['standard']
assert minimal['outcomes'][0]['memory_file_after']['utf8']=='37'
assert all(x['memory_file_after']['utf8']=='37' for x in minimal['outcomes'])
assert all(x['memory_file_after']['utf8']=='' for x in standard['outcomes'])
assert any(x['memory_after'] and x['memory_after']['utf8']=='37' for x in timelines['standard'])
summary={'status':'completed','new_model_calls':6,'source_pins_unchanged':True,'canonical_reference_unchanged':True,
    'minimal':{'turns':3,'model_file_write_demonstrated':True,'retained_final_memory':'37',
        'actual_read_stdout_turn2':'37\n','actual_read_stdout_turn3':'37\n',
        'add_five_task_succeeded':False,'initial_missing_file_error':True},
    'standard':{'turns':3,'model_file_write_demonstrated':True,'intermediate_written_values':['37','5'],
        'retained_final_memory':'','later_cell_truncation_before_TypeError':True,'add_five_task_succeeded':False},
    'both_worlds_restore_verified':True,
    'interpretation':'Prompted file I/O and real consequence/state continuity demonstrated under declared prospective notebook law. Does not establish spontaneous exploration, arithmetic success on this task, conscious intent or general learning. Joint initial-framing difference, not isolated phrase causality.'}
with (H/'SUMMARY.json').open('x') as f:
    json.dump(summary,f,indent=2);f.write('\n')
report='''# Familiar file-question framing pair

9 November 2026, America/Chicago. Six newly approved local CPU model calls in two separate three-turn diagnostic stores. The original garden remains at1550; no candidate activation, source change or canonical continuation occurred in this check.

## Prospective setup

PLAN.json was saved before preparation and inference. Both arms inherit the same1550filesystem and recorded WORLD_RULES.txt addition, model, tokenizer, prospective executable-cell grammar, greedy decoder,256-token output limit and resource bounds. Each reply used a fresh CLI process restoring the actual prior candidate world and complete transcript.

The three identical questions ask how to write string37to memory.txt in Python, how to read/print it, and then to read/addfive/print. No program source was supplied. The minimal arm starts with an explicit empty system and empty user message; its first question is the only substantive initial user input. The standard arm starts with the default short mechanics and broad invitation before the same questions. This compares the joint initial framing, not individual words or invitation and mechanics separately. The six-call count was fixed; no adaptive repair, argument insertion or program stripping occurred.

## Results

| Arm | Turn1 end-file | Turn2 real read | Turn3 requested addfive | Final file |
| --- | --- | --- | --- | --- |
| Minimal |37|Actual file read, stdout37|Read37again; did not addfive|37|
| Standard |Empty after later error|Read actual empty file; no printed contents|Wrote literal5, then later error emptied it|Empty|

In the minimal arm, turn1 generated two complete Python cells. The first tried reading the absent file and returned a real FileNotFoundError. The next cell wrote37successfully. The known error did not suppress the later cell. Turn2's new model-generated code actually opened the saved file, called read(), and printed its contents after fresh process/world restoration. This was not just a constant print. A later write cell re-stored37. Turn3 repeated that read/write behavior and ignored the requested arithmetic. Those ordinary task failures remain recorded.

In the standard arm, turn1 also generated a missing-file read followed by a successful write of37. It then produced an additional malformed multi-context-manager cell. That cell opened memory.txt in write mode, truncating it, before raising TypeError when treating a string as another context manager. The final file was therefore empty. Turns2and3 retained this pattern: the file was read, a value was written, and an additional malformed cell truncated it before error. Turn3 wrote literal5rather than adding five to a retrieved37. There was no correct42result.

OPERATION_TIMELINE.json verifies these intermediate bytes from retained per-operation snapshots, rather than inferring effects from prose. It shows intermediate37writes in the standard arm as well as the later empty state. There was no rollback, code repair, function invocation, or injected argument behind the model's output.

## What is now established

The small model can generate new executable cells that create and read real persistent files under this prospectively declared interface. The minimal arm demonstrated stored37surviving fresh processes and being retrieved by actual file-reading code. Both arms received genuine consequences in subsequent model inputs. All pauses restored and verified; source pins and the original reference remained unchanged.

This is a prompted operational demonstration. It does not establish self-directed exploration, an understanding of every law, general file-task competence, correct arithmetic, or learning. The model's prose contains incorrect explanations, including treating a read-only example as file creation. Under the candidate's declared physical rule every complete labeled cell executes, including code presented as an alternative; the observer does not infer which example the model intended. This rule explains why a later example can destroy an earlier successful result. It is not hidden extraction or a change applied after observing old outputs.

The minimal condition's stronger final-state result should not be generalized into a universal 'shorter is better' claim. There are only two three-turn deterministic trajectories on one file task. The standard condition changes several framing features jointly and also produced actual working file operations before the later failure. The original candidate has not been promoted or changed by this result.

## Evidence and stopping point

PLAN.json, SOURCE_PINS.json, both initial stores, every model token/input/output, raw source/receipts, world events and snapshots, per-turn observations, each arm's RESULT.json and the combined RESULT.json are retained. Every fresh CLI call and separate verification passed. There were exactly six new model calls and no extra calls or activation. Both diagnostic stores are paused at their own turn3, lineage label1553; the canonical original stays1550.
'''
with (H/'REPORT.md').open('x') as f:f.write(report)
print(json.dumps(summary))
