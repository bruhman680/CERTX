"""Write the settled block report from audited artifacts, without model actions."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
a=json.loads((H/'BLOCK_AUDIT.json').read_text())
assert a['status']=='pass' and a['end_entry']==1630
assert not (H/'REPORT.md').exists(),'Preserve previous report'
text=f'''# Main continuation1581–1630: capacity repaired, repetition preserved

15 November2026 UTC. **{a['actual_model_replies']} actual new main model calls**, ending paused at **1630**. Checks at1590,1600,1610,1620 and1630 all pass. Original main1580 and all **{a['source_phase_preserved_files']}** of its non-cache files remain unchanged. This is an explicitly activated linked phase, not promotion of the detached prototype.

## What changed, with authorization

The user authorized the requested50 entries and limiting input when the token bound is exceeded. The preceding full-history condition required8104 input tokens, beyond its7936-token limit. Its source/state remains intact.

The new version retains the exact initial framing and latest eight complete assistant/actual-receipt pairs, with oldest-whole-pair fallback to7936 if necessary. It never truncates the latest pair and pauses if initial framing plus that pair cannot fit. Every included/omitted entry and exact input token sequence is saved in each plan. Eight is a declared tested setting, not an established optimal memory span.

The actual supported world at1580 was cloned. Its only initialization change is the exact recorded mechanical continuity appendix in WORLD_RULES.txt. No archive-copy machinery, directory observations, diagnostic task, correction hint, score or behavioral objective was added. Existing writing persists. Complete source1551–1580 exchanges plus new events remain externally authoritative; this is current-phase history, not a claim that all earlier seasons are in the immediate model context.

The selected ACTIVE pointer now identifies bounded-main-continuation-v1. ACTIVATION.json records the user authorization, before/after pointer and preflight. Detached prototype candidate1581–1583 remains separately labeled evidence and does not count toward these main entries.

## Same body and physical laws

The cached SmolLM2-135M-Instruct revision12fd25f77366fa6b3b4b768ec3050bf629380bac is unchanged: CPU float32/eager/two threads, greedy256, fresh KV, no adapter or training. Complete exact Python/shell fences execute unchanged under the original parser; unfinished writing stays writing. The same finite process/file/world/output bounds apply. Actual ordinary errors would return and remain compatible with future cells. Unknown outcomes halt with evidence retained and no automatic replay.

## Observed50-entry block

| Observation | Audited result |
|---|---:|
| Actual new main replies | {a['actual_model_replies']} |
| Exact distinct input-token sequences | {a['distinct_input_token_sequences']} |
| Exact distinct output-token sequences | {a['distinct_output_token_sequences']} |
| Distinct reply texts | {a['distinct_reply_texts']} |
| Input tokens per reply | {a['input_tokens']} |
| Output tokens per reply | {a['output_tokens']} |
| Complete executable cells | {a['complete_executable_cells']} |
| Incomplete Python/shell fences | {a['incomplete_executable_language_fences']} |
| Nonempty actual feedback | {a['nonempty_feedback']} |
| Notebook bytes before/after | {a['initial_notebook_bytes']} / {a['final_notebook_bytes']} |

Every reply equals the preserved parent's last reply. It begins the same network-node program and reaches the256-token cap without closing its fence. We do not close or execute it afterward. There is no observed new model-chosen tool operation, successful repair, developmental transition or generalized learning in this block. Absence of a complete cell does not reveal a deliberate choice not to act; output completion is a separately testable condition.

These are fifty actual forward-generation calls and fifty actual notebook operations, not copied/reconstructed counts or replayed prototype outputs. Identical deterministic inputs are nevertheless not independent statistical samples of reasoning variety. The declared context selector advances entry identities, but repeated text/empty receipts keep the actual token sequence constant.

The capacity repair succeeds in its limited engineering purpose: the requested continuation fits and completes. It does not demonstrate better reasoning or retrieval. The separate three-cycle retrieval repair study found no correct effect under its tested feedback/coaching conditions; its prompts and failures were not imported here.

## Immediate repetition and a changing world

The model's conversational projection repeats, while its persistent notebook grows by **{a['literal_append_bytes']} bytes** and world identities change. This is not a fixed point of the full coupled model/environment state. Full external current-phase history now contains **{a['external_current_phase_exchanges']} exchanges**. Rendering it without selection would take **{a['full_unselected_input_tokens']} tokens**; the declared next selected view remains within capacity.

ACCUMULATION_NOTE.md derives a conditional resource prediction: with unchanged887-byte appends and no other relevant change,155 full appends from1580 fit beneath262144 bytes; entry1736 would request growth beyond that per-process file-size bound. That is arithmetic under explicit premises, not an observed future event or a plan to push to failure. Partial writes, ordinary errors and unknown outcomes cannot be predicted exactly from that arithmetic. The requested block ends1630 below the bound.

## Checks and continued use

Final-source zero-inference tests verified real file persistence across close/reopen, actual receipt inclusion, ordinary error followed by a successful later cell, rejection of unresolved pending outcomes without replay, lock ownership, and mandatory-latest-pair capacity handling. These explicitly synthetic test labels are not main progress. Earlier pre-hardening tests and their source snapshot remain preserved as historical artifacts.

The real run checkpoints/closes/reopens and verifies every10 replies. BLOCK_AUDIT.json additionally recomputes selected views, input/output IDs, decoded text, event ancestry, operation chains, parent-source hashes, pointer/contract identity and literal notebook-byte growth. No resource boundary or unresolved outcome occurred. Total recorded generation time is {a['generation_seconds_total']:.1f} seconds; median reply generation is {a['generation_seconds_median']:.1f} seconds. Timing is a property of this CPU run, not a benchmark guarantee.

Current settled state is entry1630, turn50, paused; no RUN.lock or PENDING remains. The reusable command is cachedvenv Python runner.py resume --steps50 --check-every10, after verify and within a new user request. Resume starts from this actual state, not the parent's1580 or a detached pilot. Existing pending/lock evidence must never be cleared to force progress.

## Next strongest distinctions

The first unresolved question is completion versus procedure selection: can the same input and generator produce a closed lawful cell with a separately declared larger output budget? That belongs in a detached comparison, retaining the unchanged main condition. The prepared generation-completion contact is separate evidence if run; it must not be counted as entry1631 or silently alter this phase's256-token body setting.

The other near-term diagnostic is correction-information placement: same task/correction initially versus after a failed example. The small source scout records relevant primary-paper contrasts without claiming our135M body replicated their methods. Neither avenue justifies claiming emergence from repeated cycles alone.

Garden interpretation: we gave the run enough immediate-context space to continue without losing its full record. It walked the same visible path50 more times. Its written ground changed; its observed procedure did not. That is a usable observation, and the unsuccessful turns remain part of the history.

Records: CONTRACT.json, ACTIVATION.json, PREFLIGHT.json, tests-v2/, run/BASE_ARCHIVE.json, run/plans/, run/raw/, run/batches/, run/events/, run/world/, run/sessions/, BLOCK_AUDIT.json. Previous navigation and pointer are preserved under before/ and BEFORE_ACTIVE_POINTER.json.
'''
(H/'REPORT.md').write_text(text)
with (H/'RESUME.md').open('a') as f:f.write('\n## Settled main block,15 November2026 UTC\n\nThe initial prepared1580 description above is historical. The selected main is now1630,turn50,paused after50actual model replies and five passing ten-entry checks. Original1580 remains intact. Read REPORT.md and BLOCK_AUDIT.json before a new requested continuation. No pending or lock remains.\n')
print({'report_written':True,'entry':a['end_entry']})
