"""External summary after the fixed three-loop run."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
def main():
    r=json.loads((H/'RESULTS.json').read_text());lines=[];observations=[]
    for row in r['rows']:
        raw=json.loads((H/'raw'/f"{row['loop']:02d}.json").read_text())
        code=[o for o in row['operations'] if o['channel']!='note']
        exits=[o['feedback']['exit_code'] for o in code if o['feedback']]
        paths=sorted(set(p for o in code for p in o['changed_paths']))
        lines.append(f"| {row['loop']} | {row['input_tokens']} | {row['output_tokens']} | {row['stop']} | {row['complete_executable_cells']} | {exits or 'no code dispatched'} | {', '.join(paths) or 'none'} |")
        observations.append({'loop':row['loop'],'text':raw['text'],'code_exit_codes':exits,'code_changed_paths':paths})
    (H/'TEXT_REVIEW.json').write_text(json.dumps(observations,indent=2,ensure_ascii=False)+'\n')
    summary={'completed_loops':r['completed_loops'],'one_persistent_world':True,
      'complete_cells':sum(x['complete_executable_cells'] for x in r['rows']),
      'code_operations':sum(o['channel']!='note' for x in r['rows'] for o in x['operations']),
      'world_store_verification':r['world_verification'],'canonical_entry':1562,
      'canonical_unchanged':r['canonical_run_unchanged'],'weights_unchanged':r['weights_unchanged'],
      'success_required_for_continuation':False,'readiness':'operationally ready for bounded unchanged live continuation, subject to final audit; no demonstrated general self-repair'}
    (H/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (H/'REPORT.md').write_text('''# Three consecutive feedback loops

13 November 2026, America/Chicago. Fixed-budget detached continuation. The live garden remains paused at entry 1562, with reference 1550 preserved. These three loops have their own numbers; they are not live entries 1563–1565.

## What persisted

We selected the first predeclared full-traceback branch (seed 27201) from the previous study, rather than choosing an output that looked successful. Its complete actual chat and post-reply world checkpoint initialize this branch. That parent reply was unfinished writing, so its actual next projected feedback is empty. The original failed action and full actual traceback remain earlier in the complete conversation.

The same branch then receives exactly three further model replies. Every reply is passed unchanged through the original notebook rule; actual code results, if any, are projected into the next user turn. Successful ordinary notebook writing has an empty projected receipt under the existing law. There are no new hints, tasks, demonstrations, corrections, summaries or grading messages. Files and notebook persist in one world store, which is closed and reconstructed between loops. The full conversation accumulates without dropping history. Fresh KV per reply matches the existing session convention.

The earlier diagnostic did not retain its sampling RNG state. We explicitly declared a new seed 27301 once, then carried the same generator continuously through all three loops and retained its before/after states. This is a new sampling session on a continuing world/transcript; it is not uninterrupted continuation of the old random stream. Temperature .8/top-p .9 and cap 512 match the prior detached condition. The live garden's greedy256 contract remains untouched.

## Every loop

| Loop | Input tokens | Output tokens | Stop | Complete cells | Code exit codes | Code-changed paths |
|---|---:|---:|---|---:|---|---|
'''+ '\n'.join(lines)+'''

Read `TEXT_REVIEW.json` and the raw records for the full visible writing. A lack of dispatched code does not erase the notebook or count as an observer rejection. Complete syntax, code dispatch, actual consequences, and useful error correction remain separate observations. Three turns in a selected branch cannot establish a developmental phase, a stable attractor, improved reasoning, or general inability to change.

## Evidence and interruption boundary

`PLAN.json` and `INITIAL_MESSAGES.json` precede inference. Every loop retains exact input IDs, messages, output IDs, text, RNG states, a raw/batch/record hash chain, before/after world state and a store verification. The parent diagnostic and canonical run inventories stayed unchanged; the local model digest stayed unchanged. No training or paid endpoint was used. `REVIEW.md`/`AUDIT.json` provide the independent continuity check when complete.

This detached runner refuses existing artifacts and leaves a pending marker if a generation/application has unknown completion. It is not a durable general-purpose resume service and has no power-loss proof. Its initial-capacity edge case is documented in the review; the actual fixed initial input is within capacity. No unknown action is automatically replayed, and no interrupted marker is deleted to force progress.

## Readiness to continue the garden

Operational readiness is assessed from preserved source/state, exact feedback, transcript and world linkage, resource capacity, clean paused checkpoints and absence of unknown pending effects. It does not require the model to produce useful code or successfully repair the earlier error. Writing-only or repeated replies remain lawful observations.

If the final audit passes, these checks support a small bounded continuation of the **unchanged live garden**, with the original greedy decoder, 256-token cap, complete history and existing mechanics. The detached sampled transcript, files and RNG must not be imported as though they were the live trajectory. A reasonable next live block is five replies with a final integrity check and earlier inspection of any actual boundary or unknown effect. Existing capacity checks pause honestly rather than summarizing or pruning.

The checks do not establish robust self-correction, comprehensive library support, unlimited context or safe durable KV serialization. Any future alteration of feedback format, decoder, chunk semantics or world facilities must be declared as a separate condition. No such alteration was adopted here.
''')
if __name__=='__main__':main()
