# Worker context components: preserve the record, vary its surroundings

1 November 2026 UTC. Prospective diagnostic, frozen after tokenizer-only length checks and before model loading or inspection of any new output. [Protocol](PROTOCOL.md), [frozen design](FREEZE.json), [queries](QUERIES.json), [raw results](run/RAW.jsonl), [summary](run/SUMMARY.json), [audit](CHECKS.json).

## Question and scope

Earlier familiar-status prompts read supplied snippets correctly in the canonical worker frame, but richer contextual prompts sometimes deferred on supplied zero-status records. Those earlier comparisons changed instruction, context and names together. This contact holds each literal record fixed and varies field packages under two fixed headers. It asks which controlled prompt changes affect this fixed adapted reader; it does not expose private reasoning, identify a neural cause, or test a wider feedback loop.

Three new study name pairs Maple/Fir, Cedar/Elm, Hazel/Ash are not globally novel words. Nine supplied records use Maple, Cedar and Hazel with positive/zero/missing statuses. Other names appear only as surrounding labels, not competing records. The intended answer always refers to the one supplied record. A mismatching target line can still introduce pragmatic task ambiguity; an output change alone is not proof that the model cannot read the record.

Each record gets one bare canonical-worker anchor and 58 factorial prompts: two headers ×29 field conditions. The bodies always include the same Visible record heading, target/Label plot fields before it, archive/Window fields after the record. The 29 conditions are: no fields; target same/different; four access values; target×access eight combinations; and corresponding unrelated-label controls. Both field labels and values change between yes/no and available/unavailable packages. Fields are not moved to other positions here.

The canonical header is the existing status mapping. The explicit-visible header adds visible-record/other-plot wording and an absent-record UNKNOWN instruction. These are instruction packages of different lengths and meanings, not a one-phrase ablation. No absent-record case exists in this contact; all records contain a status.

Controls retain corresponding values and positions but replace Target with Label and Archive with Window. Token counts were frozen before outputs: 36/252 relevant/unrelated pairs are equal-length (target-only); the other216 relevant prompts have one more token than their controls. We therefore do not call all controls length-matched or infer a uniquely semantic cause. The bare anchor additionally removes the Visible record heading; the factorial comparisons keep that heading fixed.

## Completed outcomes

All 531 planned prompts ran exactly once, with 531 unique prompt strings. Overall correct: 491/531. Canonical header including bare anchors: 269/270; explicit-visible header: 222/261.

On the same 261 factorial record/context cases, canonical is 260/261 versus explicit-visible 222/261; all nine additional bare canonical anchors are correct. Both headers are correct on all nine no-surrounding-field cases, so the richer header does not fail in every context.

The 36 incorrect UNKNOWN replies occur on zero records in every explicit-visible condition containing available/unavailable, across all three names, with or without a target line, for both Archive and Window labels. Three additional explicit-visible zero errors become YES under the unrelated mismatching Label plot plus Window accessible: yes combination. Target-only lines cause no errors in this grid. These results make target mismatch alone an insufficient explanation of the observed failures; they do not isolate the internal computation or the responsible instruction phrase.

The familiar header's one exception is Hazel/positive with Label plot: Hazel and Window accessible: no, where it returns NO. It therefore remains a strong reference within this grid rather than a guaranteed reader under arbitrary surrounding text.

| Condition | Canonical correct /9 | Explicit-visible correct /9 |
|---|---:|---:|
| bare anchor (no heading) | 9/9 | not tested |
| no_fields | 9/9 | 9/9 |
| relevant_target_same | 9/9 | 9/9 |
| relevant_target_different | 9/9 | 9/9 |
| relevant_access_yes | 9/9 | 9/9 |
| relevant_access_no | 9/9 | 9/9 |
| relevant_access_available | 9/9 | 6/9 |
| relevant_access_unavailable | 9/9 | 6/9 |
| relevant_both_same_yes | 9/9 | 9/9 |
| relevant_both_same_no | 9/9 | 9/9 |
| relevant_both_same_available | 9/9 | 6/9 |
| relevant_both_same_unavailable | 9/9 | 6/9 |
| relevant_both_different_yes | 9/9 | 9/9 |
| relevant_both_different_no | 9/9 | 9/9 |
| relevant_both_different_available | 9/9 | 6/9 |
| relevant_both_different_unavailable | 9/9 | 6/9 |
| unrelated_target_same | 9/9 | 9/9 |
| unrelated_target_different | 9/9 | 9/9 |
| unrelated_access_yes | 9/9 | 9/9 |
| unrelated_access_no | 9/9 | 9/9 |
| unrelated_access_available | 9/9 | 6/9 |
| unrelated_access_unavailable | 9/9 | 6/9 |
| unrelated_both_same_yes | 9/9 | 9/9 |
| unrelated_both_same_no | 8/9 | 9/9 |
| unrelated_both_same_available | 9/9 | 6/9 |
| unrelated_both_same_unavailable | 9/9 | 6/9 |
| unrelated_both_different_yes | 9/9 | 6/9 |
| unrelated_both_different_no | 9/9 | 9/9 |
| unrelated_both_different_available | 9/9 | 6/9 |
| unrelated_both_different_unavailable | 9/9 | 6/9 |

Every condition is reported rather than selecting a best arrangement. These are deterministic same-model observations, not independent model replications.

| Header | Positive | Zero | Recorded missing |
|---|---:|---:|---:|
| canonical | 89/90 | 90/90 | 90/90 |
| explicit_visible | 87/87 | 48/87 | 87/87 |

| Header | Maple | Cedar | Hazel |
|---|---:|---:|---:|
| canonical | 90/90 | 90/90 | 89/90 |
| explicit_visible | 74/87 | 74/87 | 74/87 |

Wrong outputs by instruction/status: `{('explicit_visible', 'zero'): 39, ('canonical', 'positive'): 1}`. Wrong output strings: `{'UNKNOWN': 36, 'YES': 3, 'NO': 1}`.

A response UNKNOWN on a supplied zero record is an incorrect deferral, not demonstrated uncertainty calibration. The stored `recognized` flag refers only to exact present-status answer labels YES/NO/WITHHOLD. UNKNOWN lies outside that set but is an offered absent-record response in the richer header; it must not be described as arbitrary malformed language. Exact raw strings, validity and correctness remain distinct. No outputs are projected to a permitted label or reinterpreted after the fact.

## Paired comparisons

Left/right directions are named explicitly. All repeated baseline uses below are paired comparisons, not new model calls.

| Pair family | Pairs | Same output | Left correct | Right correct | Left correct/right wrong | Left wrong/right correct | Both wrong |
|---|---:|---:|---:|---:|---:|---:|---:|
| paired_relevant_left_unrelated_right | 252 | 248 | 234 | 230 | 4 | 0 | 18 |
| paired_canonical_left_explicit_right | 261 | 221 | 260 | 222 | 39 | 1 | 0 |
| paired_no_fields_left_extra_fields_right | 504 | 464 | 504 | 464 | 40 | 0 | 0 |
| paired_bare_left_visible_heading_right | 9 | 9 | 9 | 9 | 0 | 0 | 0 |
| paired_yes_no_left_available_unavailable_right | 216 | 179 | 212 | 180 | 33 | 1 | 3 |

The comparisons support only the exact tested prompt packages. Header order and extra fields are fixed by design; there is no claim about every location, instruction, model, source format, or independently trained adapter. A grid of nearby strings is not a distributional guarantee. The same supplied status and intended response can produce different answers when instructions or surrounding fields change, but the experiment does not identify which internal computation or individual phrase is responsible.

## What to carry forward

Keep the proven canonical worker instruction as the reference for supplied-record reading. Do not promote the richer instruction or alternate access wording as a repair. Their additional specificity does not automatically preserve established behavior. Controller-provided record identity/access checks and source receipts still carry their own credit; this contact does not make the model a controller or show it learning from a mistake.

Strongest next diagnostic: decompose the instruction package prospectively. Cross visible-record/other-plot clarification present/absent with the absent-record UNKNOWN clause present/absent, using a fixed mapping and selected predeclared archive/window/no-field contexts. Include equal-token unrelated controls where feasible and retain all arms before choosing any modification. This can test whether the absence clause, clarification, or their interaction matters; the present two-header comparison cannot decide that.

A later hybrid/source-revision/layout contact remains useful, and broader memory/handoff/planning branches remain open. The larger model exploration/consequence-feedback loop stays parked as requested. No failure here is evidence of internal linear reasoning, universal incapacity, model error awareness, a learning update, or general FRR efficacy.

## Runtime and verification

Same existing canonical LoRA adapter on HuggingFaceTB/SmolLM2-135M-Instruct, revision12fd25f77366fa6b3b4b768ec3050bf629380bac. Base weights SHA2565af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c; adapter SHA2564d83525c501f2c68fdfaf127f5f6ffe7d1c30c0bba14ae7168b0cee3aba524e9. CPU float32/eager, two threads, fixed seed73103, greedy fresh cache, 12output-token cap, <=768input-token ceiling. No training, tools, retrieval, worker-cache reuse, downloads/installs or paid API calls. Dense model/runtime are local and not bundled with GitHub code/data/logs.

Input/output tokens 48,462/1,844; generation time 202.315 seconds excludes load/documentation/audit time. Maximum prompt 107 tokens, no truncation; cap stops 0. Sampled working estimate max 1,939,308,544 bytes, RSS max 896,335,872 bytes, below working guard5,153,960,755bytes. No billing/remaining-account-usage visibility.

Four test groups and the audit pass. All 531 prompts, token IDs, decoded raw text, scores, control pair counts, saved checkpoint dependencies and in-memory parameter digests are checked. 3,811 older local files are unchanged before navigation sync. Four current navigation/method-note originals are archived. Old reports/scores/failures/weights remain history. No default policy, core/schema/general-tool or queue change; no new capsule/restore/independent-backup claim and no background model task remains.

To reproduce without overwriting: copy the study into a new run directory, run four tests, `study.py prepare`, `study.py run`, `study.py score`, then `verify.py` using the existing venv where Transformers/Torch are needed. Preparation tokenizes locally before freezing but never loads the model. Files are created exclusively; existing run paths intentionally stop a repeat. Preserve original local dependency paths or explicitly declare replacements in a new study.
