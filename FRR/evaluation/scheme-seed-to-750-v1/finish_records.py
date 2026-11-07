"""Completed seeded-block report and current navigation; no model calls."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent;F=H.parent.parent
A=json.loads((H/'ANALYSIS.json').read_text());assert A['status']=='pass' and A['next_step']==750 and A['calls']==100
assert not (H/'REPORT.md').exists()
completion=json.loads((H/'COMPLETED.json').read_text());seed=A['user_seed'];windows=A['windows'];reviews=sorted(H.glob('ATTENTION_*_REVIEW.json'))
prior=json.loads((H.parent/'scheme-continuation-to-650-v1/ANALYSIS.json').read_text())
lines=['| Entries | Calls | Host kinds | Scheme submissions | Output caps | Verified |','|---|---:|---|---:|---:|---:|']
for w in windows:
 kinds=', '.join(sorted(set(w['host_kinds'])))
 lines.append(f"| {w['start_step']+1}–{w['next_step']} | {w['calls']} | {kinds} | {w['scheme_submissions']} | {w['stops'].count('token_limit')} | {w['verification']} |")
result=f"Host kinds: `{json.dumps(A['host_kinds'],sort_keys=True)}`. Scheme statuses: `{json.dumps(A['scheme_statuses'],sort_keys=True)}`. Successful Scheme statuses: `{json.dumps(A['successful_scheme_statuses'],sort_keys=True)}`."
report=f'''# Same garden, user seed from entry 651, paused at 750

6 November 2026 America/Chicago. Completed the requested **100-entry continuation**, entries **651–750**, in **{len(windows)} checked windows**, each at most ten replies. The original world and its history continue. No diagnostic/test garden was imported or substituted.

## Exact user seed

> {seed}

The seed was introduced at saved step 650 / human entry 651. Every new prompt includes that exact text, including the final emoji, in a separately identified user-seed section. It broadens the invitation within the existing environment. It does not grant new host/network/file authority or bypass the Scheme profile, command syntax or resource limits.

## Recorded condition changes

The user also authorized ten-entry checked windows, with closer inspection for curious events. A new versioned runner adds the seed and widens the maximum checked window from five to ten; a non-note host result pauses for observer review. The old runners, manifests, seed shelves and 650-entry history are preserved. The current pointer selects **seeded_routine.py** and **ENVIRONMENT_SCHEME_USER_SEED_V1.json**.

The model, canonical adapter, sampler, absolute-step seed rule, fresh KV per call, 96-token output cap, 8,096-token input cap, runtime profile, notebook/archive access and old number patch remain unchanged. No display-framing repair, grammar-constrained decoding, output normalization, training, download or paid inference was introduced. Sampling and context remain finite; this is a continuing trajectory, not an unbounded reasoning system.

## Results

{result}

There were {A['stops'].get('eos',0)} model-EOS endings and {A['stops'].get('token_limit',0)} 96-token cap stops. Maximum input was {A['max_input_tokens']} / 8,096 tokens; {A['generated_tokens']} tokens were generated. There were {A['exact_unique_texts']} exactly distinct reply strings; the longest adjacent exact repeat was {A['longest_exact_adjacent_repeat']}. The complete user seed appeared verbatim in {A['seed_verbatim_replies']} replies. These are literal descriptive counts, not measures of understanding or internal state.

The host alias table contains {len(A['scheme_snapshot']['aliases'])} aliases. Artifact tables unchanged from the start: **{A['artifact_tables_unchanged']}**; alias tables unchanged: **{A['alias_tables_unchanged']}**; complete portable bundle unchanged: **{A['final_bundle_matches_start']}**. A changed audit log is distinct from changed artifacts; model-produced metadata is not host state.

{len(reviews)} observer review records were retained. A validation rejection is not successful guest evaluation. The `executed` flag still means a terminal host event exists; interpret it together with status, error and actual state. [Earlier label note](../scheme-continuation-to-550-v1/RECEIPT_LABEL_NOTE.md).

## Window record

{chr(10).join(lines)}

## Verification and preservation

A disposable-copy connection check used **zero model calls**. Four selected old renders matched byte for byte, all 150 integrated historical entries replayed, the exact emoji-bearing seed was checked, the ten/eleven-entry bounds were exercised, and one clearly labelled synthetic note tested new record transport and replay. The copy and its fixture were discarded. All 2,571 original primary files were unchanged during that test. [Checks](CONNECTION_CHECKS.json).

Activation then retained the old world bundle, created a new immutable seed card/manifest and updated the active pointer. Final verifier **{A['final_verification']['verification']}**, cursor **750**, reconstructs old and seeded prompt versions, token IDs, outputs, stop records, RNG seeds, environment pins, dispatch receipts and independently replayed portable worlds. It checks live-store equality, notebook continuity, all protected historical hashes, sessions and sampled resource limits. All new sessions checked unchanged weights and zero training updates.

The full notebook now has 48 origin entries and 702 saved generations. The original prefix through 650 is preserved byte for byte. Current STATE, NOTEBOOK, CURRENT_VERIFY and ACTIVE_RUNNER are authorized projections/pointers; their exact old bytes are archived under before/. Earlier manifests, raw outputs, plans, sources and sessions were not rewritten. The old missing interrupted attempt at step 492 remains unknown.

## Interpretation

The previous 100-entry block had host kinds `{json.dumps(prior['host_kinds'],sort_keys=True)}`. This block has `{json.dumps(A['host_kinds'],sort_keys=True)}`. This is a descriptive sequential comparison: the optional seed, operational cadence and continuing history differ. It cannot isolate the seed's causal effect or establish emergence, learning, intention or a new stable reasoning phase.

Reply text may quote invitations, host-looking labels or claimed platform details. Such claims remain unverified unless a real host receipt supports them. Persistence here is external state and record continuity, not weight updates or retained hidden activations. Presentation issues identified in the prior block remain hypotheses; they were not repaired during this run.

## Resume point

The garden is paused at **750**, with no further model calls scheduled. Use [RESUME.md](RESUME.md) and **seeded_routine.py**, not an older runner. Verify before arming. Inspect any new non-note receipt and state change before resuming a zoomed window. Preserve every earlier form; future seed or framing changes require a recorded new version.

[Analysis](ANALYSIS.json) · [Completion](COMPLETED.json) · [Observation rules](OBSERVATION_RULES.md) · [Current verifier](../source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json)
'''
report=report.replace('## Interpretation\n',f'''## Interpretation

The routed reply at human entry 688 began `(675-686)`, matching the then-visible history range. Leading-parenthesis routing sent it to Scheme; validation rejected the unsupported token. Its intended role is unknown. The pause, independent replay, artifact/alias comparison and observer review are retained in [ZOOM_NOTES.md](ZOOM_NOTES.md) and [ATTENTION_004_REVIEW.json](ATTENTION_004_REVIEW.json). No repair, hint, seed change or model retry was introduced.

| Descriptive measure | Prior block 551–650 | Seeded block 651–750 |
|---|---:|---:|
| EOS endings | {prior['stops'].get('eos',0)} | {A['stops'].get('eos',0)} |
| Output-cap stops | {prior['stops'].get('token_limit',0)} | {A['stops'].get('token_limit',0)} |
| Exactly distinct replies | {prior['exact_unique_texts']} | {A['exact_unique_texts']} |
| Longest adjacent exact repeat | {prior['longest_exact_adjacent_repeat']} | {A['longest_exact_adjacent_repeat']} |
| Routed Scheme submissions | {prior['scheme_submissions']} | {A['scheme_submissions']} |

''',1)
(H/'REPORT.md').write_text(report)
nav=f'''# Current: original garden with exact user seed, paused at 750

6 November 2026 America/Chicago. [Seeded 100-entry report](evaluation/scheme-seed-to-750-v1/REPORT.md), [analysis](evaluation/scheme-seed-to-750-v1/ANALYSIS.json). Same garden and history; entries 651–750 are saved. Final verifier {A['final_verification']['verification']} passed; PAUSE present, no run/block lock, no further inference scheduled.

The user seed, including the final 😁, is preserved in [USER_SEED.json](evaluation/scheme-seed-to-750-v1/USER_SEED.json), visible in every new prompt from step 650. The user also authorized at most ten entries per checked window. Non-note host events pause for observer review. Actual checked windows: {len(windows)}; review records: {len(reviews)}. No host permissions, runtime capabilities, model/adapter, sampler or token caps were expanded. Zero training updates, unchanged weights in all new sessions.

{result}

Use **evaluation/scheme-seed-to-750-v1/seeded_routine.py** and its [resume guide](evaluation/scheme-seed-to-750-v1/RESUME.md). The active manifest is ENVIRONMENT_SCHEME_USER_SEED_V1.json. Older prompts/manifests replay under their original versions. Exact old pointer/projection bytes are in before/. Never replace a missing SQLite store with a fresh world; verify or reconstruct its last settled portable bundle.

The seed and operational cadence are recorded condition changes, not a randomized seed-effect test. Interpret model text, terminal receipts, successful statuses and artifact changes separately. The old missing attempt at step 492 remains unknown. Earlier navigation below is historical context, not the active resume instructions.

---

'''
for rel in ['CURRENT_HANDOFF.md','sync/CURRENT_ORIENTATION.md','evaluation/CURRENT_RESEARCH_MAP.md']:
 p=F/rel;assert p.read_bytes()==(H/'before'/p.name).read_bytes(),'Unexpected navigation edit'
 prefix=nav
 if rel.startswith('sync/'):prefix=prefix.replace('](evaluation/','](../evaluation/')
 if rel.startswith('evaluation/'):prefix=prefix.replace('](evaluation/','](')
 p.write_text(prefix+p.read_text())
print('Seeded block report and navigation synced at 750.')
