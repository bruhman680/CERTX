# Missing counts, known zero and opposite questions: three adaptive cycles

30 October2026, America/Chicago. Parent `f701a7da6bd7116a7d3277ee3e20a755df149ca7`.

**The source-frame benefit survives on the new positive counts, but fails on explicit missing counts.** A predeclared readiness gate stopped the arithmetic follow-up. Removing the extra observation quantity did not eliminate fabrication. Paired presence questions then revealed logically inconsistent answers on five of eight passages. These are useful boundaries for the verification workflow, not evidence of repaired model reasoning.

Thirty-nine new local small-model generations were run across three sequential adaptive contacts: FG-C1(14),MF-C1(9),CP-C1(16). Each protocol/cases/keys/runner/preservation manifest was frozen before its own inference. MF followed the failed FGgate; CP followed MF. They are not one prespecified confirmatory experiment or independent population replications. No training, paid services, retry or old-state deletion occurred.

## Cycle 1: fresh values and the missing/zero boundary

[FG-C1](../frame-generalization-missing-v1/REPORT.md) uses seven authored base records, each in passive-event and there-are frames, with the existing C2 count question and ordinary instruction. Four new value pairs `(independent soils,observations per soil)` are `(5,9),(9,5),(6,18),(18,6)`. Two records leave the soil count unrecorded while supplying9or18observations per soil. One records0soils and says9observations/soil were planned but none collected.

| Source state | Passive-event frame | There-are frame |
|---|---:|---:|
| Positive count | 2/4 | 4/4 |
| Soil count unrecorded | 0/2 | 0/2 |
| Known zero soils, no collected data | 0/1 | 1/1 |
| Total | 2/7 | 5/7 |

The positive there-are count answers retain5,9,6,18in the proper role. In both frames the missing-count answers fabricate a soil count from the observations-per-soil quantity. Passive wording also turns the planned nine observations into nine soils in the explicit-zero record. The there-are zero answer is correctly0.

These results qualify the prior0/4passiveversus4/4there-are contrast: passive answers are not universally wrong, and the better frame is not a general missingness repair. Frame packages change syntax, tense/adverb position and capitalization together. Their intended count key is preserved for this task, not every possible proposition or temporal claim.

### The gate actually remained closed

Before inference, [GATE.json](../frame-generalization-missing-v1/GATE.json) required **all seven there-are records** to have unambiguous source-supported answers before considering a separately frozen arithmetic contact. That includes missing counts and knownzero, not just positive examples. [GATE_RESULT.json](../frame-generalization-missing-v1/GATE_RESULT.json) records5/7andfailuresF5/F6. The branch decision was to withhold arithmetic and investigate source reading.

This is a concrete application of the experimental gate using coordinator judgments, not an autonomous model verifier, statistical competence certificate or general policy. We did not lower the threshold, discard the missing cases, retroactively reopen the gate, or use the correct positive subset to claim an end-to-end arithmetic success. A gate passing on small fixtures would also have remained a scoped condition, not broad validation.

A count of0is a recorded source value. Separately, a sample-mean variance formula involving division by k or by the number of observations is outside its domain when k=0and no data exist. Missing k is an unresolved source fact;0is a known input with a downstream domain boundary. These can both prevent calculation for different reasons. No arithmetic was run in these contacts.

[FGprotocol](../frame-generalization-missing-v1/PROTOCOL.md), [design](../frame-generalization-missing-v1/DESIGN.json), [keys](../frame-generalization-missing-v1/KEYS.json), [freeze](../frame-generalization-missing-v1/FREEZE.json), [raw](../frame-generalization-missing-v1/RAW_OUTPUTS.jsonl), [scores](../frame-generalization-missing-v1/SCORES.json) and [summary](../frame-generalization-missing-v1/SUMMARY.json) preserve every outcome.

## Cycle 2: an unrelated quantity beside an explicit missing count

[MF-C1](../missing-count-foil-v1/REPORT.md) holds this clause fixed:

`There are independently sampled soils, but their number was not recorded.`

Eight sources append an observation-per-soil quantity9,18,7or11, independently rendered as digits or English words. One shared control omits that second sentence. The key is UNKNOWN in all9calls. Word/digit pairs preserve the additional quantity; the no-foil source omits an additional fact but preserves the missing-count target. This is task-specific source reduction, not a universal semantics-preserving rewrite.

| Condition | Correct UNKNOWN answers | What was generated |
|---|---:|---|
| Digit observation quantity | 0/4 | That quantity as a soil count |
| Word observation quantity | 0/4 | That quantity as a soil count |
| No observation sentence | 0/1 | Invented12soils plus a claim that count is absent |

The no-foil response is exactly:

`The given record documents 12 soils, but the count is absent.`

The second clause does not rescue the unsupported first clause. Extra quantities influence which wrong number is produced in the eight foil variants, but the no-foil case shows they are not necessary for an invented count. It would be too broad to conclude that removing numbers, dropping context or simply saying “unrecorded” fixes this reader.

The9/18digitprompts exactly repeat exposed FGthere-are failures; input/generated token IDs match. They are repeatability checks, not fresh independent evidence. The shared no-foil control was run once, not duplicated as four apparent independent controls. All raw text is retained; no unknown key changed.

[MFprotocol](../missing-count-foil-v1/PROTOCOL.md), [basis](../missing-count-foil-v1/BASIS.json), [cases](../missing-count-foil-v1/CASES.json), [keys](../missing-count-foil-v1/KEYS.json), [freeze](../missing-count-foil-v1/FREEZE.json), [raw](../missing-count-foil-v1/RAW_OUTPUTS.jsonl), [scores](../missing-count-foil-v1/SCORES.json), [summary](../missing-count-foil-v1/SUMMARY.json).

## Cycle 3: opposite presence questions

CP-C1 reuses eight exposed source passages: four with recorded counts5,9,18,0and four whose soil count is unrecorded but observation quantity is9,18,7,11. Ask each source in separate fresh contexts:

- `Is the number of independently sampled soils explicitly recorded in this passage? Answer only YES or NO.`
- `Is the number of independently sampled soils unrecorded in this passage? Answer only YES or NO.`

Under these authored two-state source keys, the answers are logical complements. Each question polarity has fourYES/fourNOkeys. Zero counts as recorded, even if no observations were collected. This does not make every arbitrary pair of natural-language questions complementary; the task/source relation is declared here.

| Query | Correct labels |
|---|---:|
| Recorded? | 4/8 |
| Unrecorded? | 7/8 |
| Total | 11/16 |

The model answersYESto every recorded? question. For unrecorded? it answersNOon the three positive-count passages andYESon the zero-count and all four missing-count passages.

| Source record | Recorded? answer | Unrecorded? answer | Both correct? |
|---|---|---|---|
| Count5 | YES | NO | Yes |
| Count9 | YES | NO | Yes |
| Count18 | YES | NO | Yes |
| Recorded0, no collected observations | YES | YES | No |
| Unrecorded count,9observations/soil | YES | YES | No |
| Unrecorded count,18observations/soil | YES | YES | No |
| Unrecorded count,7observations/soil | YES | YES | No |
| Unrecorded count,11observations/soil | YES | YES | No |

Only3/8pairs are both correct and complementary. Five pairs assert both recorded and unrecorded. All four missing sources get the correct unrecorded? answer, while the recorded? answers contradict it. The zero case shows the danger of treating no collected observations as no recorded count.

A complementary pair is not a truth certificate: on a missing-count source, the hypothetical pair recordedYES/unrecordedNOwould be complementary and wrong twice. That is a logical counterexample, not another observed generation. Here inconsistency flags five pairs, but passing consistency alone cannot verify the other three. Truth of those three still comes from the frozen source/key comparison.

These are separate model calls, not one shared internal chain or evidence of a stable contradictory belief. The result shows answer dependence on the question and a failure to preserve this source-state relation across elicitation. A bare correct label does not establish the intended reasoning path. We did not combine the separately generated outputs into a new gated pipeline or use CPto promote the failed FGgate.

[CPprotocol](PROTOCOL.md), [records](RECORDS.json), [cases](CASES.json), [keys](KEYS.json), [freeze](FREEZE.json), [raw](RAW_OUTPUTS.jsonl), [scores](SCORES.json) and [summary](SUMMARY.json) preserve the full paired results. All16outputs are bare `Yes`/`No`; exact uppercase formatting is0/16, case-insensitive formatting16/16. Semantic judgments accept capitalization. Formatting therefore does not explain the five wrong labels.

## What was refined

An optional [worked example](../../examples/missing-zero-and-complement-questions.md) and [verification guidance](../../modules/verification-layer.md) now emphasize:

1. Evaluate the source-state boundary that matters before passing an extraction into a calculator. Positive-value examples alone did not establish missingness handling here.
2. Preserve missing, knownzero, and outside-domain calculation as different states. Withholding for the wrong reason does not verify the source or formula.
3. On declared complementary questions, same-label answers flag an inconsistency, while complementary answers still require source grounding. Do not ask a model to certify its own source reading and treat the result as independent evidence.
4. Keep a failed predeclared gate failed. A later question's correct labels do not silently repair a prior extraction or establish an end-to-end workflow.

The existing source-role guard/threshold comparator, executable policies, core/runtime/schema, weights and research-queue statuses are unchanged. They do not parse these soil sources or validate arbitrary linguistic complements. These are workflow/reporting refinements grounded in the observed failures, not a demonstrated behavioral fix, arithmetic improvement, new general source parser, confidence score or broad FRR advantage.

## Runtime, review and preservation

All39newcalls use pinned local `HuggingFaceTB/SmolLM2-135M-Instruct` revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, CPUfloat32/eager,2threads,eval/inference,argmax,64-new-tokencap,EOS,freshcontexts. Python3.12.14,torch2.6.0+cpu,transformers4.57.1. No examples, retries, continuations, paid APIs, training or state deletion. The main assistant remains separate from this model.

| Contact | Calls | Input tokens | Emitted tokens | Inference seconds excluding load/serialization |
|---|---:|---:|---:|---:|
| FGfresh values/missing/zero | 14 | 1,524 | 170 | 15.9869 |
| MFfoil control | 9 | 999 | 120 | 9.9619 |
| CPpresence polarity | 16 | 1,672 | 32 | 6.7678 |
| Total | 39 | 4,195 | 322 | 32.7167 |

All39reachEOS. Cache serialization totals .2354seconds. Model loading and preservation/hash work are excluded from inference timings; observed local times are not a service-speed/billing guarantee. No paid resource was invoked. Every stderr/runtime manifest is saved; dtype warnings were nonfatal.

Thirty-nine new terminal caches totaling206,536,696bytes are preserved under `/workspace/smollm_frame_generalization_states_v1`, `/workspace/smollm_missing_count_foil_states_v1`, `/workspace/smollm_count_presence_states_v1`. Bytes, saved tensor sequence dimensions, input/rendered prompt IDs, decoded output and cached-prefix hashes were checked. The final emitted token may not have been forwarded into cache; recorded lengths/token sequences retain that boundary. Binaries stay local, manifests retain reconstruction IDs/model pin; workspace persistence is not guaranteed. No main-assistant cache access/storage improvement is claimed.

Each protocol/input manifest predates its own inference. Raw freezes precede structured scoring; progress output viewing is disclosed, with all MF/CPcompletion outputs viewed before scoring. Coordinator semantic/source-equivalence review and saved-data checks were not independent or masked. Gold keys were separately frozen and hashed, not parsed into inference prompts. Later protocols followed earlier results; this is adaptive research rather than a single confirmatory study.

The final pre-integration snapshot records2,757priorFRRfiles and327recordedmodel/oldcachefiles. Separate [FGpreservation](../frame-generalization-missing-v1/PRESERVATION_AFTER_GENERATION.json), [MFpreservation](../missing-count-foil-v1/PRESERVATION_AFTER_GENERATION.json) and [CPpreservation](PRESERVATION_AFTER_GENERATION.json) receipts verify each snapshot and all new caches. Seven old current documents are byte-archived in [ARCHIVE_RECEIPT.json](ARCHIVE_RECEIPT.json) before authorized updates. Moved links keep original bases; use the original paths at the parent for historical navigation. All historical source/code/raw results/model weights/caches remain unchanged. [Final checks](FINAL_CHECKS.json) record the final allowlist/link scope.

## Strongest next

A prospective source-bound state witness is more promising than another ungrounded self-check: explicitly bind the count's role and whether its value is missing or zero before allowing computation. Begin with a declared tiny grammar or trusted structured source, preserve quote/byte identity and unsupported-input abstention, and test false proposed counts against missing andzero sources. The existing field-role guard offers a design pattern but does not implement this domain. Measure whether a model can produce accepted faithful witnesses and useful coverage separately from rejection rate. No such parser/policy is installed in this contact, no arithmetic follow-up ran, and no background job remains active.
