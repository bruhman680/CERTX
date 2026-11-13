"""Describe the retained neutral control, with no model calls or world mutation."""
from pathlib import Path
import collections, json
H=Path(__file__).resolve().parent
r=json.loads((H/'RESULT.json').read_text())
assert r['status']=='completed' and r['model_calls']==6
rows=r['results']
assert all(x['memory_file_after'] is None and not x['new_files_since_initial'] for x in rows)
ops=[op for x in rows for op in x['actual_cell_operations']]
assert len(ops)==6 and all(op['receipt']['exit_code']==1 for op in ops)
summary={'status':'completed','model_calls':6,'canonical_entry':1550,
    'diagnostic_turns':6,'complete_executed_model_cells':len(ops),
    'successful_cell_exits':0,'nonzero_cell_exits':6,
    'memory_file_created':False,'other_new_files':[],
    'actual_NameError_turns':[x['turn'] for x in rows if any('NameError' in op['receipt']['stderr'] for op in x['actual_cell_operations'])],
    'usage_exit_turns':[x['turn'] for x in rows if any('Usage:' in op['receipt']['stdout'] for op in x['actual_cell_operations'])],
    'actual_ZeroDivisionError_turns':[x['turn'] for x in rows if any('ZeroDivisionError' in op['receipt']['stderr'] for op in x['actual_cell_operations'])],
    'stops':dict(collections.Counter(x['stop'] for x in rows)),
    'all_feedback_transitions_delivered':all(x['delivered'] is True for x in r['feedback_delivery']),
    'source_pins_unchanged':r['source_pins_unchanged'],
    'all_six_calls_fresh_subprocess':r['all_six_calls_fresh_subprocess'],
    'all_six_pauses_verified':r['all_six_pauses_verified'],
    'model_driven_persistent_write_read_demonstrated':False,
    'scope':'A new neutral-filename/concise-wording sequential condition. It changes both wording and filename; no isolated lexical-causation claim.'}
with (H/'SUMMARY.json').open('x') as f:
    json.dump(summary,f,indent=2);f.write('\n')
table='\n'.join(f"| {x['turn']} | {x['cells']} | {','.join(str(op['receipt']['exit_code']) for op in x['actual_cell_operations'])} | {'NameError' if x['turn'] in summary['actual_NameError_turns'] else 'Usage exit'} | {x['stop']} |" for x in rows)
text=f'''# Neutral wording six-turn operational diagnostic

9 November 2026, America/Chicago. Six new local CPU model calls; no canonical continuation. The original garden remains at entry **1550**. This separate diagnostic world ends at its own turn6 (lineage label1556), paused and verified.

## Prospective condition

PLAN.json was saved before preparation or inference. Its six fixed prompts ask one-line Python programs to write37to memory.txt, read it, read/add5, divide1by0, print1/2, and read the file again. No program source was supplied. Task wording and filename both differ from the earlier seed.txt control, so this is not an isolated test of a lexical seed association.

All other candidate laws, source pins and model body settings remain unchanged: empty system, short mechanics and original broad invitation, complete explicitly labeled executable cells, greedy256-token outputs, full actual conversation, finite bounds and fresh KV. Each reply ran in a fresh candidate.py subprocess restoring the committed world and exact transcript. Ordinary task failures did not trigger rewriting, source repair, hidden feedback or retries.

## Observations

| Turn | Complete executed cells | Exit status | Actual result | Stop |
| --- | --- | --- | --- | --- |
{table}

Every model reply contained one complete Python cell and that cell really executed. However, **memory.txt never existed**, and no other new file was created. Only the automatic notebook changed. The source on turns1–3and6 placed the requested operation in a function behind a `sys.argv` guard requiring three arguments. The cells had no such arguments, so the programs printed Usage and exited before reaching their file code. A function mentioning open/read is not evidence that a read occurred.

Turns4and5 omitted `import sys` but referenced `sys.argv`, giving genuine NameError receipts. The requested ZeroDivisionError did not occur. The actual turn4 NameError receipt was delivered into the next raw model input; turn5 still emitted a missing-import program and failed similarly. Turn6 included an import again but retained the Usage guard. This sequence does not establish deliberate error recognition or repair.

All five between-turn feedback transitions were present in the following exact model input. Every pause restored and verified successfully. Literal checkpoint-object bytes, model cell sources, stdout/stderr/status, raw inputs/tokens, and newly created-file observations are retained. No receipts or operations were invented.

## What this establishes

The new interface lets prospectively generated complete model cells operate in the world, and factual consequences enter later calls. It does not require a whole-response JSON envelope. These six calls nevertheless **do not demonstrate model-driven persistent write/read**. They do not fulfill that working-foundation criterion merely because their code contains plausible file-operation functions.

The neutral filename and concise request did not remove the CLI-template pattern in this sequential condition. This does not establish the cause of that pattern, nor that all prompts or the model's entire ability would fail. Source-level presentation and accumulated transcript remain possible influences. We did not change the world to auto-call functions, supply arguments, repair source, or reinterpret failures as successful actions.

## Integrity and next boundary

Source pins remain unchanged. The exact original phase inventory was checked by the candidate before/after each call and at every fresh-process verification. All six candidate pauses passed with no training, paid endpoint, downloads, adapters, canonical edits, or adaptive extra calls. The driver made exactly six new model calls and has completed.

Root should retain these negative outcomes and keep the candidate's operational status qualified. The runtime and action/consequence bridge work; genuine model-written persistent data remains an unfilled evidence requirement. No further test, activation or source change was performed by this diagnostic.
'''
with (H/'REPORT.md').open('x') as f:f.write(text)
print(json.dumps(summary))
