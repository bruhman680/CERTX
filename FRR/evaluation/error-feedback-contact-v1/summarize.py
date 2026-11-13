"""External retained-outcome summary; no model-facing judgments."""
from pathlib import Path
import json,collections
H=Path(__file__).resolve().parent
def main():
    result=json.loads((H/'RESULTS.json').read_text());groups={};table=[];texts=[]
    for condition in result['plan']['conditions']:
        rr=[r for r in result['rows'] if r['condition']==condition]
        groups[condition]={'replies':len(rr),'with_complete_cells':sum(r['complete_executable_cells']>0 for r in rr),
          'with_incomplete_fences':sum(r['incomplete_fences']>0 for r in rr),
          'eos':sum(r['stop']=='eos' for r in rr),
          'code_operations':sum(o['channel']!='note' for r in rr for o in r['operations'])}
        for r in rr:
            codes=[o for o in r['operations'] if o['channel']!='note']
            exitcodes=[o['feedback']['exit_code'] for o in codes if o['feedback'] is not None]
            changed=sorted(set(p for o in codes for p in o['changed_paths']))
            table.append(f"| {condition} | {r['seed']} | {r['output_tokens']} | {r['stop']} | {r['complete_executable_cells']} | {exitcodes or 'no code dispatched'} | {', '.join(changed) or 'none'} |")
            raw=json.loads((H/'raw'/f"{condition}_{r['seed']}.json").read_text())
            texts.append({'condition':condition,'seed':r['seed'],'text':raw['text'],'exit_codes':exitcodes,'code_changed_paths':changed})
    (H/'SUMMARY.json').write_text(json.dumps(groups,indent=2)+'\n')
    (H/'TEXT_REVIEW.json').write_text(json.dumps(texts,indent=2,ensure_ascii=False)+'\n')
    (H/'REPORT.md').write_text('''# One-step error-feedback contact

13 November 2026, America/Chicago. Detached diagnostic branches; the continuing notebook garden is unchanged at entry 1562 and its original reference remains at 1550. No weights, live decoder, world laws or live memory changed.

## Question

After one sampled reply produced a complete Python cell that failed during multiprocessing semaphore creation, does showing its detailed actual error change the next reply or its real consequences compared with showing only failure status?

This test uses one selected parent reply from the earlier decoder study. That reply's code fence closed but its surrounding explanatory prose reached the 512-token cap. Both conditions retain the exact original initial chat, full sampled assistant reply, and a user-role receipt produced by the canonical `project_feedback` function. The full condition is that actual receipt unchanged. The status-only control changes only stderr to an empty string, retaining stdout, channel, exit code 1 and boundary fields. It is an explicitly counterfactual information-removal control; the true original error remains preserved in the source record. It adds no hint, solution, grading or request to fix anything.

## Planned comparison and all results

Seeds 27201–27203 are paired across both conditions. Sampling temperature .8/top-p .9 and output cap 512 match the preceding diagnostic. Every generation starts with fresh KV, exact retained role sequence, float32 eager CPU and the same local 135M model. Six followup replies were planned before inference. Each reply is delivered unchanged once through the existing notebook law into its own reconstruction of the same exact post-error physical checkpoint. Any complete cells run within the unchanged sandbox and their actual receipts are retained. No second model reply consumes those new receipts in this one-step protocol.

| Feedback | Seed | Output tokens | Stop | Complete cells | Code exit codes | Code-changed paths |
|---|---:|---:|---|---:|---|---|
'''+ '\n'.join(table)+'''

`SUMMARY.json` reports frequencies by condition. Raw replies, token IDs and parsed fences, batch receipts, per-operation events, object stores and independent world verifications are retained. `PEER_REVIEW.md` and `AUTHENTICITY_REVIEW.json` independently check source text, receipt identity, sole stderr difference and parent checkpoint linkage. The parent diagnostic and active run inventories stayed identical, and parameter digests matched before/after. This uses cached local inference and no paid endpoint.

## What the comparison can and cannot establish

Different observed replies under these two inputs demonstrate sensitivity within this bounded setup. Removing the traceback changes both content and token length, so a difference cannot be uniquely assigned to semantic understanding of that error. Reusing three seeds creates paired random conditions, not six independent garden histories. The parent was selected for having a complete cell, not sampled at random from all possible model behavior.

Prose can refer to errors or propose an alternative without producing an executable action. A complete fence can dispatch and still fail. A zero exit code alone does not demonstrate meaningful repair or a correct explanation. These layers must be read separately from the actual raw text and receipts. Notebook writing is permitted behavior, and all outputs stay in the record. No model reply is rejected for lacking code or for missing an investigator-preferred solution.

This is in-context one-step responsiveness, not weight training, long-term memory acquisition or evidence of a developmental phase. Repeated failed approaches could need more opportunities, but additional cycles have not occurred here. The two-condition experiment is also a new diagnostic chat branch, not exact raw-token continuation of the capped parent and not a replacement for the live greedy trajectory.

## Next direction

Use the observed consequences and read the full text before choosing a follow-up. A multi-step branch would need its own fixed reply budget, exact actual receipts, per-branch persistent world, and no retrospective solution hints. An independent length/content control could better isolate information carried by the detailed traceback. Neither inference nor environmental conditions should be silently changed to force a favorable result.
''')
if __name__=='__main__':main()
