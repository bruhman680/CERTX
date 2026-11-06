"""Write the completed block's current navigation and report; old bytes are in before/."""
from pathlib import Path
import json
D=Path(__file__).resolve().parent;F=D.parent.parent
A=json.loads((D/'ANALYSIS.json').read_text());assert A['status']=='pass' and A['next_step']==550
assert not (D/'REPORT.md').exists(),'Do not overwrite a completed report'
windows=A['windows'];kinds=A['host_kinds'];statuses=A['scheme_statuses'];alias_count=len(A['scheme_snapshot']['aliases'])
lines=['| Entries | Scheme submissions | Output-cap stops | Max input tokens | Verified cursor |','|---|---:|---:|---:|---:|']
for w in windows:lines.append(f"| {w['start_step']+1}–{w['next_step']} | {w['scheme_actions']} | {w['stops'].count('token_limit')} / 5 | {w['max_input_tokens']} | {w['next_step']} |")
entries='\n'.join(lines)
actions='\n'.join(f"- Entry {e['human_entry']} (saved step {e['step']}): `{e['status']}`, error `{(e['error'] or {}).get('code')}`. Raw submission and full receipt retained in the primary archive." for e in A['scheme_events']) or '- No Scheme-looking submission reached the interpreter.'
report=f'''# Same garden, paused at 550

6 November 2026. Completed the user-requested **45-entry block**, from cursor 505 through 550, with nine checked five-entry windows. The environment, model, canonical adapter, prompt renderer, seed shelf, sampling and runtime limits remained unchanged. No new season, diagnostic import, output repair or training was introduced.

## Observed

Host-result kinds: `{json.dumps(kinds,sort_keys=True)}`. Scheme submission statuses: `{json.dumps(statuses,sort_keys=True)}`. Successful Scheme terminal statuses: `{json.dumps(A['successful_scheme_statuses'],sort_keys=True)}`. The final host alias table contains **{alias_count}** aliases. See the retained world bundles for authoritative artifact/request/audit state; unchanged snapshot or aliases does not imply an unchanged audit log.

{actions}

Across the 45 replies, {A['stops'].get('token_limit',0)} reached the 96-token host cap and {A['stops'].get('eos',0)} ended with model EOS. There were {A['exact_unique_texts']} exactly distinct strings; the longest adjacent run of identical strings was {A['longest_exact_adjacent_repeat']}. Literal feature counts: {json.dumps(A['text_features'],sort_keys=True)}. These are reproducible string counts, not semantic or internal-state measurements. Maximum input was {A['max_input_tokens']} / 8,096 tokens; total generated tokens were {A['generated_tokens']}.

The primary prefix through 505 is retained byte for byte in the notebook. Earlier source, event, prompt, manifest and session files remain unchanged; only the current STATE, NOTEBOOK projection and CURRENT_VERIFY pointer advance. Each new raw generation is saved before dispatch, followed by the action receipt and before/after portable world bundles.

## Window record

{entries}

Each checkpoint replayed the connected world from portable bundles and reconstructed saved prompts, token IDs, RNG seeds, decoded outputs and stop metadata. Final verifier **{A['final_verification']['verification']}** reports cursor **550**. It validates the 50 integrated entries since activation at 500, in addition to preserved/hash-checked historical evidence. The full notebook consists of 48 origin entries and 502 saved generations. All nine new sessions report unchanged weights and zero training updates. PAUSE is present; RUN.lock and the block lock are absent.

The earlier missing interrupted attempt at old step 492 remains unknown. A completed later window does not supply that missing evidence.

## Interpretation and boundaries

This is a single correlated continuation, not 45 independent experiments. Repeating a snapshot identifier or host-result-shaped JSON does not create an alias, execute an action, establish understanding or prove self-correction. Model-generated claims about success or capacity remain text unless a host record independently supports them. Conversely, a rejected attempt is preserved evidence of what was submitted and returned, rather than discarded noise.

The live model sees the recent twelve-entry view, current workspace state and archive affordance. Published world state persists between calls, but hidden activations are not carried over and weights do not learn from the notebook. This block does not establish an emergence phase or a general failure of the approach.

[Receipt label note](RECEIPT_LABEL_NOTE.md): the runtime's `executed` flag currently means a terminal host event exists, including validation rejection. The analysis separates terminal receipts from successful statuses. No frozen runtime or historical receipt was changed during this block. A future version can split those fields explicitly.

## Wind-down and next contact

Stopped exactly at 550 as requested. No further model call is scheduled. Continue with the same [active V2 runner and resume guide](../scheme-primary-integration-v1/RESUME.md), verifying the saved cursor and world before arming another window. First inspect the rejected submissions and their following replies if a closer contact is desired. Any command-format or label refinement should be a recorded new version, not silently mixed into this unchanged block.

[Analysis](ANALYSIS.json) · [Completion](COMPLETED.json) · [Observation rules](OBSERVATION_RULES.md) · [Primary verifier](../source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json)
'''
(D/'REPORT.md').write_text(report)
summary=f'''# Current: same continuous garden paused at 550

6 November 2026. [45-entry continuation report](evaluation/scheme-continuation-to-550-v1/REPORT.md), [analysis](evaluation/scheme-continuation-to-550-v1/ANALYSIS.json). Completed entries 506–550 in nine checked windows with unchanged environment, prompts, model, canonical adapter and sampling. Final verifier {A['final_verification']['verification']}; PAUSE present, no RUN.lock or scheduled further inference. Old records retained.

Host kinds: {json.dumps(kinds,sort_keys=True)}. Scheme statuses: {json.dumps(statuses,sort_keys=True)}. Successful Scheme statuses: {json.dumps(A['successful_scheme_statuses'],sort_keys=True)}. Final alias count {alias_count}. Most interpretation must remain at the level of recorded replies/actions; text-shaped snapshots and success claims are not host state. The executed flag records a terminal event, including rejected validation; see [label note](evaluation/scheme-continuation-to-550-v1/RECEIPT_LABEL_NOTE.md). No learning or emergence claim; zero training updates, unchanged weights in all nine sessions.

Use evaluation/scheme-primary-integration-v1/connected_routine_v2.py and its [resume guide](evaluation/scheme-primary-integration-v1/RESUME.md). Verify before arming. Same garden/history, Scheme added at 500; never replace a missing SQLite store with a new empty world. Portable bundles and raw receipts are retained. The old interrupted attempt at step 492 remains unknown.

Next contact after wind-down: inspect the recorded command-validation failures and their following replies, then choose another unchanged continuation or an explicitly versioned refinement. Do not silently repair replies, count rejected forms as successful execution, import host fixtures, or switch adapters. Earlier navigation below is preserved historical context.

---

'''
for rel in ['CURRENT_HANDOFF.md','sync/CURRENT_ORIENTATION.md','evaluation/CURRENT_RESEARCH_MAP.md']:
 p=F/rel;assert p.read_bytes()==(D/'before'/p.name).read_bytes(),'Navigation changed unexpectedly'
 prefix=summary
 if rel.startswith('sync/'):prefix=prefix.replace('](evaluation/','](../evaluation/')
 if rel.startswith('evaluation/'):prefix=prefix.replace('](evaluation/','](')
 p.write_text(prefix+p.read_text())
print('Report and current navigation synced at 550; earlier bytes preserved in before/.')
