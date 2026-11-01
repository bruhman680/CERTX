# Revision, authority and preserved history — bounded settling contact

1 November 2026 UTC. Completed final bounded run before the user's requested usage-reset pause. [Protocol](PROTOCOL.md) · [ledger resolver](ledger.py) · [all source ledgers](DATA.json) · [raw model outputs](run/RAW.jsonl) · [materialized receipts](run/RECEIPTS.jsonl) · [summary](run/SUMMARY.json) · [audit](CHECKS.json).

## The contract we tested

A history is not automatically a current state. This contact declares how a small single-status ledger is interpreted, preserving the source events while distinguishing patch, replacement, deletion and conflicting branches. It is an engineered event-ledger test, not a claim of a novel general algorithm, an independently validated source of truth or autonomous small-model reasoning.

Each event names id/source/plot/revision/parents/operation/payload. Parent links define succession. Revisions must advance their parents but do not impose a total order between sibling branches. Roots require replacement. A replacement constructs a snapshot without inheriting omitted fields; a single-parent patch preserves omitted fields. Patch status=null removes the field; delete removes the record. The literal value missing remains a recorded known status mapped WITHHOLD. A patch cannot implicitly resurrect a tombstone; an explicit replacement can.

Different concurrent snapshots remain CONCURRENT_CONFLICT, even when one branch has a larger revision. Equal-valued heads retain both witnesses without treating them as independent confirmations. An explicit replacement merge naming both parents can resolve them; a multi-parent patch is held because no base-selection semantics were declared. Identical event replay does not double-vote; conflicting authorized contents under one ID are held rather than silently overwritten.

The owner allowlist is an out-of-band authority assumption. This test does not authenticate source strings, verify signatures, or establish that an owner is truthful. Missing provenance is held; guest and foreign-plot claims are retained as ignored inputs. A missing/foreign/unauthorized parent breaks the declared target lineage. All raw events remain available even when trustworthy materialized history cannot be produced.

## Fixed design and completed results

25 authored situations × three study target names Cress/Verbena/Sorrel × forward/reverse source display give150logical cases. These names are not globally novel tokens. Four test groups check all cases, every display permutation of the small <=4event fixtures, missing-versus-delete distinctions and input immutability. The resolver matching these authored categories is functional contract coverage, not independent empirical validation.

The raw model receives a new richer ledger instruction including the owner/parent/patch rules and a label-only response request. The selected worker receives a canonical line-format target/status snippet only when code materializes a KNOWN value. The resolver already reads the status, so a pure mapping could answer those cases without any model call. Success is credited separately to code materialization and model readout; no hidden answer enters prompting/resolution.

Actual generations: 144 (135unique raw ledger prompts plus9unique selected-record prompts), not150independent model trials. Logical KNOWN cases: 54/150. Raw model correct on KNOWN cases: 34/54; selected worker consistent: 54/54. The9worker responses are reused across cases and are not independent repeated successes. Raw class labels on held cases: 96; these remain proposals, not endorsed answers.

| Situation | Cases | Receipt categories | Raw KNOWN correct | Selected KNOWN correct | Last-display correct on KNOWN | Max-revision correct on KNOWN |
|---|---:|---|---:|---:|---:|---:|
| base | 6 | {'KNOWN': 6} | 6 | 6 | 6 | 6 |
| cycle | 6 | {'LINEAGE_ERROR': 6} | 0 | 0 | 0 | 0 |
| delete_record | 6 | {'DELETED': 6} | 0 | 0 | 0 | 0 |
| duplicate_conflict | 6 | {'ID_CONFLICT': 6} | 0 | 0 | 0 | 0 |
| duplicate_identical | 6 | {'KNOWN': 6} | 4 | 6 | 6 | 6 |
| empty | 6 | {'SOURCE_ABSENT': 6} | 0 | 0 | 0 | 0 |
| explicit_merge | 6 | {'KNOWN': 6} | 0 | 6 | 3 | 6 |
| foreign_parent | 6 | {'LINEAGE_ERROR': 6} | 0 | 0 | 0 | 0 |
| fork_different | 6 | {'CONCURRENT_CONFLICT': 6} | 0 | 0 | 0 | 0 |
| fork_high_revision | 6 | {'CONCURRENT_CONFLICT': 6} | 0 | 0 | 0 | 0 |
| fork_same | 6 | {'KNOWN': 6} | 6 | 6 | 3 | 6 |
| invalid_revision | 6 | {'LINEAGE_ERROR': 6} | 0 | 0 | 0 | 0 |
| merge_patch | 6 | {'LINEAGE_ERROR': 6} | 0 | 0 | 0 | 0 |
| missing_parent | 6 | {'LINEAGE_ERROR': 6} | 0 | 0 | 0 | 0 |
| missing_provenance | 6 | {'PROVENANCE_MISSING': 6} | 0 | 0 | 0 | 0 |
| only_untrusted | 6 | {'NO_AUTHORIZED_EVIDENCE': 6} | 0 | 0 | 0 | 0 |
| patch_after_delete | 6 | {'LINEAGE_ERROR': 6} | 0 | 0 | 0 | 0 |
| patch_omitted | 6 | {'KNOWN': 6} | 6 | 6 | 3 | 0 |
| recorded_missing | 6 | {'KNOWN': 6} | 0 | 6 | 3 | 6 |
| remove_field | 6 | {'PARTIAL': 6} | 0 | 0 | 0 | 0 |
| replace | 6 | {'KNOWN': 6} | 6 | 6 | 3 | 6 |
| replace_after_delete | 6 | {'KNOWN': 6} | 6 | 6 | 3 | 6 |
| replace_omitted | 6 | {'PARTIAL': 6} | 0 | 0 | 0 | 0 |
| unknown_operation | 6 | {'FORMAT_ERROR': 6} | 0 | 0 | 0 | 0 |
| untrusted_high_revision | 6 | {'KNOWN': 6} | 0 | 6 | 6 | 6 |

No class label is invented for PARTIAL, DELETED, conflicting or invalid lineage cases. A raw UNKNOWN might recognize that a class answer is unavailable, but does not show recognition of the particular graph/provenance reason. Held receipt categories remain distinct. Reversing displayed events leaves every code-based verdict, resolved value, head set and status-origin set unchanged; that property belongs to the resolver, not automatically to the model.

Across75forward/reverse pairs, the resolver has0verdict/state/head/origin changes; raw answers change on4pairs, last-display shortcuts on48, and max-revision shortcuts on9. This is a descriptive pair audit, not additional model calls or a claim about all display permutations for the model. [Pair audit](ORDER_PAIR_AUDIT.json).

Error receipts do not materialize a trusted history; the complete received events, including ignored or invalid claims, remain in DATA.json. This single-field model does not authenticate source labels.

## Comparators and limits

The last-authorized-display and maximum-authorized-revision comparators inspect only one event's literal payload. They deliberately omit inheritance/graph semantics; they are sanity controls under this declared contract, not proof that last-write rules are universally wrong in systems whose contract explicitly uses them.

| Comparator | Correct on KNOWN cases | Class-label endorsements on held cases |
|---|---:|---:|
| arrival_last | 36/54 | 60 |
| max_revision | 48/54 | 51 |

Explicit parent links preserve information that arrival order and a scalar revision do not supply. Patch omission and replacement omission can lead to different snapshots even when the latest payload looks equally empty. No real-world chronology, source trust or broader schema semantics have been inferred here.

The case set is small, authored and single-field. It does not cover cryptographic identity, source spoofing, access revocation, complex patches, multiple-field merges, real clocks, arbitrary formats or every unknown metadata failure. A raw rich-task failure is not an isolated neural mechanism or universal incapacity. No unadapted-model comparison or independent model replication was run.

## Restart point — paused, not running

The strongest next bridge is a read-only, bounded history of one real repository artifact: inspect actual revision links and preserved snapshots, declare which source/version is authoritative for the question, then compare materialized state with the stored artifact. Do not automatically turn newest timestamp, largest number, branch name or a fluent explanation into authority. Keep the small ledger as a reference contract rather than a mandatory gate on every exploration.

Further authority-authentication and multi-field patch questions remain open. Wider model feedback/exploration loop stays parked at the user's request; broader memory/handoff/planning branches remain open. Prior UNKNOWN-notepad failures and evidence-boundary cases remain intact. No additional automatic experiment follows this contact; restart awaits user input after limits reset.

## Runtime and preservation

Input/output tokens 30,256/346; generation time 78.036 seconds excludes model loading/audit/documentation. Cap stops 0. Sampled working estimate max 1,962,172,416 bytes, RSS max 907,268,096 bytes, under5,153,960,755-byte guard. Raw allowance16output tokens, selected8, allinputs<=768without truncation. Every stop and raw output is preserved.

Same existing HuggingFaceTB/SmolLM2-135M-Instruct base revision12fd25f77366fa6b3b4b768ec3050bf629380bac and canonical adapter. Base SHA2565af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c; adapter SHA2564d83525c501f2c68fdfaf127f5f6ffe7d1c30c0bba14ae7168b0cee3aba524e9. CPU float32/eager, two threads, seed73103, greedy fresh caches. Frozen dependencies, saved weights and in-memory digests remain unchanged.

All tests/audits pass: 144 actual input/token/decode/stop records,150logical receipts, expected outcomes, status-origin witnesses and reversal invariance. 3,937 older local files unchanged before navigation sync; current navigation/method-note originals archived. Raw ledgers are not erased on held outcomes.

No training, new model binaries, defaults/core/schema/general-tool/queue changes, downloads/installs, paid APIs/rental, tool actions or background jobs. No new capsule, independent current-binary backup, clean-environment restore or optimizer-resume claim. Existing local12.8MBadapter capsule differs from older desktop6.3MBcopy; dense model/runtime remain local. Account usage/billing is not visible.

Reproduce in a new study directory: tests, venv `study.py prepare`, venv `study.py run`, stdlib `study.py score`, venv `verify_run.py`. Outputs are created exclusively. Preparation tokenizes and checks authored contracts before freezing but does not load the model. Do not overwrite this record or silently replace its dependencies.
