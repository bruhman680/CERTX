"""External observations only; never used as garden feedback."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
def main():
    result=json.loads((H/'RESULTS.json').read_text())
    rows=[];summary={};notes=[]
    for context in result['plan']['contexts']:
        group=[r for r in result['rows'] if r['context']==context]
        greedy=json.loads((H/'references'/f'{context}.json').read_text())
        summary[context]={'sampling_replies':len(group),
          'replies_with_complete_executable_cells':sum(r['assessment']['complete_executable_cells']>0 for r in group),
          'replies_with_incomplete_fences':sum(r['assessment']['incomplete_fences']>0 for r in group),
          'eos_replies':sum(r['stop']=='eos' for r in group),
          'greedy_complete_executable_cells':greedy['assessment']['complete_executable_cells']}
        rows.append(f"| {context} | greedy reference | {len(greedy['generated_token_ids'])} | retained | {greedy['assessment']['complete_executable_cells']} | {greedy['assessment']['incomplete_fences']} |")
        for r in group:
            a=r['assessment']
            rows.append(f"| {context} | sample {r['seed']} | {r['output_tokens']} | {r['stop']} | {a['complete_executable_cells']} | {a['incomplete_fences']} |")
            raw=json.loads((H/'raw'/f"{context}_{r['seed']}.json").read_text())
            notes.append({'context':context,'seed':r['seed'],'first_500_characters':raw['text'][:500],
              'last_300_characters':raw['text'][-300:],'assessment':a})
    (H/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    (H/'TEXT_EXCERPTS.json').write_text(json.dumps(notes,indent=2,ensure_ascii=False)+'\n')
    table='\n'.join(rows)
    (H/'REPORT.md').write_text('''# Detached decoder and context contact

13 November 2026, America/Chicago. The continuing notebook garden remains paused at entry 1562 and its original reference remains at 1550. No live law, decoder, seed, memory policy, notebook or stored world was changed by this contact.

## Question and planned comparison

After longer greedy replies remained unfinished, we asked whether one declared sampling setting changes output form on the same inputs. The exact first-turn input and prospective turn-13 input were fixed before sampling. Each received four independently initialized CPU random generators with seeds 27101–27104, temperature 0.8 and top-p 0.9, capped at 512 output tokens. Nucleus selection keeps the token that first crosses the probability threshold. The same local 135M parameter model used float32 eager attention, evaluation mode and two CPU threads; parameter digests match before and after. No endpoint or training was used.

The greedy references come from the previous exact-input cap study, taking at most the first 512 generated tokens. They are retained evidence, not new repetitions. Sampling runs are fresh prefills using exactly those input token IDs and no hint, task or instruction change. The same seed set is reused across contexts, so treat contexts as paired conditions rather than eight independent environmental replications. Contexts themselves differ in both length and conversation content; this is not an isolation of length alone.

## All outcomes

| Context | Decoder / seed | Output tokens | Stop | Complete executable cells | Incomplete fences |
|---|---|---:|---|---:|---:|
'''+table+'''

The primary observation is exact parser eligibility. Ordinary writing is allowed and is retained regardless of whether it contains code. No generated code ran in this diagnostic. Static Python syntax checks, where applicable, do not establish correct execution, useful action, reasoning improvement or emergence. Shell syntax was not separately checked. Frequencies from four seeds per input are descriptive; this single sampling setting was not optimized or selected from a parameter search.

`PLAN.json` precedes inference. `RESULTS.json`, `SUMMARY.json`, raw token IDs/text, exact-input references, source scripts and external excerpts retain every outcome. The active run-file inventory stayed identical and no weights changed. No sampled reply was inserted into the continuing garden's history.

## Continuation and operator scouts

[Continuation scout](scouting/SCOUT.md) separates raw-token continuation, KV continuation and new chat turns. Decoding and re-encoding visible text can alter token boundaries, and closing an assistant turn adds model-facing structure. An in-memory exact-token/cache equivalence test is distinct from durable crash-safe cache persistence; read its retained results and limitations before using it as an engineering foundation.

[Operator-lock design](../operator-lock-recovery-design-v1/DESIGN.md) proposes a persistent local flock inode for live ownership, keeping pending transaction and owner history separately. Disposable tests demonstrate release after abrupt death, descriptor lifetime, and the danger of unlinking/recreating a locked pathname. Existing exclusive-create writers do not cooperate with flock: this is not a drop-in migration or deployed repair.

## Next direction

Read the per-context results before interpreting variation as progress. If sampling only changes surface text, it is not a demonstrated action repair. If complete cells appear, their existence still needs separate consequence testing on copies. There is no automatic promotion of a winning sample or alteration of the live decoder. Exact-token chunking may permit mechanically faithful pauses, but must preserve the selected final token, cache position and EOS semantics; it cannot make a model that already ended naturally keep thinking without declaring a changed condition.
''')
if __name__=='__main__': main()
