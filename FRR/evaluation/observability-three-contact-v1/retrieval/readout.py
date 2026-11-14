"""Read-only interpretation of all six prompted retrieval outcomes."""
from pathlib import Path
import sys,json,hashlib,ast,base64
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H))
import common
R=H/'retrieval'
def call_name(node):
    if isinstance(node,ast.Name):return node.id
    if isinstance(node,ast.Attribute):return call_name(node.value)+'.'+node.attr
    return type(node).__name__
def main():
    jobs=common.read(R/'jobs.json');rows=[];raws={};sources=[]
    for j in jobs:
        expected=j['metadata']['expected_value'];case=j['case_id']
        for turn in (1,2):
            d=H/'results'/case
            raw=common.read(d/f'raw{turn}.json');res=common.read(d/f'result{turn}.json');batch=common.read(d/f'batch{turn}.json')
            raws[(case,turn)]=raw
            code=[o for o in batch['operations'] if o['channel']!='note']
            calls=[]
            for cell in batch['parsed']['cells']:
                if cell['executable'] and cell['language']=='python':
                    try:tree=ast.parse(cell['source'])
                    except SyntaxError:continue
                    calls.extend(call_name(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call))
                    sources.append({'case_id':case,'turn':turn,'source':cell['source']})
            stdout=''.join(o['feedback']['stdout'] for o in code if o['feedback'])
            stderr=''.join(o['feedback']['stderr'] for o in code if o['feedback'])
            row={'case_id':case,'turn':turn,'expected_value':expected,'complete_cells':res['complete_cells'],
              'input_tokens':res['input_tokens'],'output_tokens':res['output_tokens'],'stop':res['stop'],
              'target_in_model_text':expected in raw['text'],'target_in_executed_stdout':expected in stdout,
              'exit_codes':[o['feedback']['exit_code'] for o in code if o['feedback']],
              'stdout':stdout,'stderr':stderr,'static_calls':sorted(set(calls)),
              'static_file_read_calls':[x for x in sorted(set(calls)) if x=='open' or x.endswith(('.read_text','.read_bytes','.read'))],
              'json_loads_present':'json.loads' in calls,
              'code_changed_paths':sorted({p for o in code for p in o['changed_paths']}),
              'raw_sha256':common.sha(d/f'raw{turn}.json'),'result_sha256':common.sha(d/f'result{turn}.json')}
            rows.append(row)
    pairchecks=[]
    for turn in (1,2):
        a,b=raws[('retrieval_hidden_a',turn)],raws[('retrieval_hidden_b',turn)]
        pairchecks.append({'turn':turn,'input_ids_identical':a['input_token_ids']==b['input_token_ids'],
             'output_ids_identical':a['generated_token_ids']==b['generated_token_ids'],
             'texts_identical':a['text']==b['text']})
    finalfiles=[]
    for j in jobs:
        store=Path(j['world_store']);state=common.read(store/'STATE.json');assert state['paused']
        bundle=common.read(store/'bundles'/state['bundle']);entry=next((x for x in bundle['entries'] if x[0]=='probe_value.json'),None)
        decoded=None
        if entry is not None and entry[1]=='file':
            obj=common.read(store/'objects'/(entry[3]+'.json'))
            try:decoded=json.loads(base64.b64decode(obj['base64']))
            except (ValueError,TypeError):pass
        finalfiles.append({'case_id':j['case_id'],'final_probe_contents':decoded,
            'matches_initial_target':decoded=={'value':j['metadata']['expected_value']}})
    result={'scope':'prompted two-turn diagnostic, no free-emergence or general competence claim',
      'rows':rows,'hidden_pair_checks':pairchecks,'final_fixture_files':finalfiles,
      'metadata_is_not_model_input':'worker generates from job messages only; hidden targets absent from preparation messages',
      'model_calls_by_readout':0,'world_writes_by_readout':False}
    common.save(R/'RESULTS_INTERPRETATION.json',result)
    common.save(R/'EXECUTED_SOURCES.json',sources)
    table='\n'.join('| '+ ' | '.join([r['case_id'],str(r['turn']),str(r['complete_cells']),str(r['exit_codes']),str(r['target_in_model_text']),str(r['target_in_executed_stdout'])])+' |' for r in rows)
    (R/'REPORT.md').write_text('''# Prompted retrieval controls

13 November 2026, America/Chicago. This is an explicit task diagnostic on copied worlds, not the main garden's open exploration. No model inference, execution, or world write was performed by this readout.

## Fixture and input controls

Two ordinary readable files contain different values, K7M4Q9 and R2V8T6, at the same path `probe_value.json`. Their supported filesystem snapshots differ only in that file. Their first model inputs are exactly identical and neither target appears in those messages. The task asks for the value field to be read and printed. A third world has the same supported filesystem as A; it supplies the same task plus an authentic operator-originated Python read receipt showing A's value. The operator attribution is explicit. This extra receipt changes input length/content and makes the target directly available; it is not evidence of model-chosen retrieval.

Each branch receives at most two replies. The second input appends only the first actual assistant reply and factual consequences, without repeating the task or adding a solution. All complete cells run unchanged. `PREPARATION_CHECKS.json`, `FIXTURE_PAIR_AUDIT.json`, source commands and receipts ground the controls.

| Case | Turn | Complete cells | Code exit codes | Target appears in text | Target appears in code stdout |
|---|---:|---:|---|---|---|
'''+table+'''

## Interpretation

Read the executed sources and actual stdout separately from process exit. The hidden-pair code calls `json.loads` on the literal filename string `probe_value.json`, instead of opening the valid file and parsing its contents. It catches the resulting JSONDecodeError and prints an invalid-JSON message plus None, exiting normally with code0. That is a handled error in the generated procedure; it does not show that the fixture file is invalid or that sandbox access was denied. The real operator read and decoded fixture bytes establish readability and valid JSON.

The hidden first replies are identical, and their second replies should be interpreted with the exact comparisons in `hidden_pair_checks`. In the observed hidden followup, the described target changes from value to boundary without performing the intended file access. Receipt-schema vocabulary appearing in code or prose is not itself retrieval or error resolution.

For the supplied-read case, target text or stdout, if present, can use information already delivered in the prompt. That outcome cannot by itself establish an actual file read. The per-case static call inventory is an aid to source inspection rather than a universal dynamic tracing system; actual receipts and complete source remain authoritative.

`RESULTS_INTERPRETATION.json` records every row, exact pair comparisons, stdout/stderr, source calls and final fixture state. A zero exit code, a complete fence, mention of the filename, an answer in prose, and a successful read are distinct observations. This small selected-context diagnostic does not establish general inability to retrieve or success on future retrieval tasks.
''')
    print(json.dumps({'rows':len(rows),'hidden_pair_checks':pairchecks,
       'target_stdout_count':sum(x['target_in_executed_stdout'] for x in rows)}))
if __name__=='__main__':main()
