# Three clause-reader cycles: useful selection, fragile wording

CR-C1/2/3, 30 October 2026 UTC. Parent `0845908f7df455ea38cdb49484d4ed3e48e98984`; follow-up to the [soil-design reader](../soil-design-reader-v1/REPORT.md).

**Supplying a relevant source clause helped on the exposed tasks, but did not establish a reliable reader.** A predeclared question rewording improved soil-count reading while degrading reset-status reading. Their identical aggregate totals concealed opposite movements. Newly authored short passages still produced wrong-number-role answers and a partial-calibration error.

## Frozen design and actual execution

[Protocol](PROTOCOL.md), [32 cases](CASES.json), separate [keys](KEYS.json), [parent sources](PARENT_RECORDS.json), [verbatim selection manifest](SELECTION.json), [guidance](GUIDANCE.json), [runner](run.py), model pin and preservation receipt were frozen in [FREEZE.json](FREEZE.json) before any new inference. Three prespecified phases ran sequentially in one invocation; these are not three adaptive searches or independent replications. [Author checks](AUTHOR_CHECKS.json) verify case count and eight exact selected spans.

The pinned model remains `HuggingFaceTB/SmolLM2-135M-Instruct` at `12fd25f77366fa6b3b4b768ec3050bf629380bac`: text only, CPU float32/eager, two threads, eval/inference mode, greedy generation, 64-new-token cap and EOS stopping. Each call starts a fresh context. There are no examples, retries, training, weight edits, paid services or broad FRR-base intervention. The main assistant is not this local model.

- **C1, 16 calls:** the eight earlier reading questions each receive either the full source or a coordinator-selected, verbatim sufficient span. The question/instruction/model/cap remain the same within each pair. The full arm intentionally repeats exposed SR-C1 inputs.
- **C2, 8 calls:** use the same selected spans and instruction, with one frozen rewording of the question. No wording was selected after seeing outcomes.
- **C3, 8 calls:** new short sources with counts32/8/2/unrecorded and reset-status cases both supplied, only qA supplied, both zero supplied, neither supplied. Use the **original C1 questions**, not the C2 rewording. This distinction limits any transfer claim.

The chosen spans contain the necessary source fact for the reading task. They are not sufficient inputs to the earlier variance or causal-identification tasks. Selection was supplied by the coordinator; the model did not find the spans. The manifest binds exact text and character offsets to each parent source's SHA256. This authenticates the selected bytes against the saved source, not the source's truth or general semantic sufficiency.

All raw responses, stdout/stderr and runtime metadata were frozen in [RAW_FREEZE.json](RAW_FREEZE.json) after completion and before systematic scoring. Partial outputs were inspected for progress updates; semantic review was coordinator-only, neither independent nor masked. No inference was repeated after weak answers. A dtype deprecation warning is preserved in stderr; it did not interrupt execution.

## Results with the scoring qualification visible

The expected answer keys did not change. Whole-response review identified two outputs that explicitly retained the missing soil count but added ambiguous wording about no observations/documentation of shared soil. The conservative tally withholds these; a target-answer sensitivity counts them. [SCORING_NOTE.md](SCORING_NOTE.md) explains this post-result interpretation judgment and preserves the exact raw wording for readers who disagree.

| Condition | Calls / distinct prompts | Unambiguous whole-response matches | Target-answer sensitivity | Token-cap stops |
|---|---:|---:|---:|---:|
| C1 full source | 8 / 8 | 2/8 | 2/8 | 3 |
| C1 selected clause | 8 / 7 | 5/8 | 6/8 | 0 |
| C2 clause, reworded question | 8 / 7 | 5/8 | 6/8 | 0 |
| C3 new clauses, original question | 8 / 8 | 4/8 | 4/8 | 0 |

R2/R4 have identical selected absence statements and questions in each clause condition. Their nominal two slots are not independent evidence; hence the distinct-prompt counts. Across all32calls there are16unambiguous matches,11wrong responses,2qualified target matches and3unresolved source echoes. These totals span intentionally dependent/exposed conditions and are not a population accuracy estimate.

### C1: selection helps, completion is a separate result

All eight full-arm input and generated token sequences exactly reproduce the earlier SR-C1 reading calls. This is a same-procedure repeatability check, not independent evidence. The same three grouping calls copy a source prefix to the cap without answering k. The full-source missing-grouping record again invents k=64; the reset-reading calls again all claim both values were supplied.

With the relevant span supplied, three unambiguous failures improve: the one-soil count G3 and the missing-efficacy records R2/R4. The two previously correct supplied-efficacy records remain correct. The missing-count record also gives the correct missing-count target, but its added shared-observation wording remains qualified.

Selection does not fix all counts. On the64-soil clause, the reader says the record lacks the number of soil draws while acknowledging64independentsoils. On the4-soil clause, it denies independent soil draws altogether. These are completed wrong answers, not truncated answers. Removing the source echo did not itself establish correct source reading.

### C2: equal totals hide opposite family changes

| Family | C1 clause, unambiguous | C2 reworded, unambiguous |
|---|---:|---:|
| Soil grouping | 1/4 | 3/4 |
| Reset-value availability | 4/4 | 2/4 |

For grouping, asking how many independently sampled soils the passage documents produces the correct64,4,1 counts. The missing-count response retains the explicit unknown target with qualified extra wording. For reset availability, asking whether the passage supplies a number for each q value makes the model deny supplied values even when both are present, including zeros. The two absence cases remain correct; they are duplicate selected inputs.

Thus both aggregate scores stay5/8 (6/8 target sensitivity), while the task families move in opposite directions. This is observable wording sensitivity, not evidence for a particular neural mechanism or a universal advantage of one phrase. It does not justify automatically routing all tasks to the new wording. No full-source/reworded-question arm was included, so interaction between question wording and full source is also unmeasured.

### C3: new short sources still lose number roles

New grouping answers include:

- A source says32independentlysampledsoils,2observations each. The response copies those facts, then explicitly answers **2**.
- A source explicitly states8independentsoildraws,8observations each. The response answers **UNKNOWN**.
- A source states2independentlysampledsoils,32observations each. The response answers **32 independent soil draws**.
- The unrecorded-count source is correctly recognized as missing.

The reset reader correctly recognizes both provided nonzero values, both provided zeros, and the absence of both. It incorrectly calls **both** values supplied when only qA is supplied and qS is explicitly unrecorded. This negative case prevents treating any visible q value as sufficient calibration coverage.

The resulting4/8 is a bounded new-source contact under the original question. **It does not test transfer of the C2 reworded question to these new sources.** The missing crossed cell is a strong next experiment. Numeric and wording changes also occur together in C3, so neither is isolated as the cause of its failures.

## Cost, format and preservation

| Condition | Input tokens | Emitted tokens | Measured inference seconds |
|---|---:|---:|---:|
| C1 full | 1,928 | 277 | 23.9991 |
| C1 clause | 836 | 168 | 13.4114 |
| C2 reworded | 892 | 176 | 14.1275 |
| C3 new clause | 829 | 164 | 13.0015 |

Total4,485inputtokens,785emittedtokens,64.5396seconds inference excluding serialization/model load, and .3460seconds cache serialization. The C1 clause input is56.64%smaller than full-source input. Selection effort was manual and uninstrumented, so these are **not end-to-end retrieval cost or speedup claims**. Fewer generated tokens and different outputs also affect runtime. No neutral-length/position-matched control isolates compression, relevance, position or distractor removal. No paid API/resource was invoked.

All32responses used sentences rather than the exact requested bare output format, so strict format adherence is0/32. Semantic scoring does not reject a correct sentence merely for verbosity/case. Twenty-nine calls reached EOS and three capped; all capped calls belong to the full-source arm. Full raw text and judgment rationale are retained in [SCORES.json](SCORES.json), with machine-readable totals in [SUMMARY.json](SUMMARY.json).

Thirty-two new terminal cache files totaling241,523,688bytes remain in `/workspace/smollm_clause_reader_states_v1`. Byte hashes, every saved tensor's sequence dimension, full token IDs, rendered prompt and cached-prefix hashes were checked. The final emitted token may not have been forwarded; recorded prefix lengths preserve that boundary. Caches remain local, with reconstruction IDs/pin published; workspace survival is not guaranteed and none of this exposes or compresses the main assistant's state.

[Preservation after generation](PRESERVATION_AFTER_GENERATION.json) checks2,611priorFRRfiles and240recordedmodel/oldcachefiles unchanged before documentation integration. A reused check harness initially retained a24-case uniqueness assertion; it was corrected to the frozen32-case count, with no scientific artifact or model rerun. The receipt records that bookkeeping correction. Seven previous current documents are separately byte-archived under [ARCHIVE_RECEIPT.json](ARCHIVE_RECEIPT.json). Moved archive links retain their original bases; use original paths at the parent commit for historical navigation. [Final checks](FINAL_CHECKS.json) record final preservation scope.

## Refinement adopted

The optional [verification guidance](../../modules/verification-layer.md) and [soil-design example](../../examples/soil-design-and-reset-calibration.md) now emphasize:

1. Preserve question identity, original source binding, selection method and task scope when handing off an excerpt. A good clause for source reading need not support arithmetic or causal inference.
2. Count completed outputs separately from source-supported outputs; a fluent contradiction is not a repaired readout.
3. Inspect families and paired transitions before trusting an unchanged aggregate score. Predeclare diagnostic partitions where feasible; here the grouping/reset families were fixed before inference.
4. Treat selected text and reworded questions as conditional aids that need their own transfer test, not a default reasoning repair.

No executable guard, threshold comparator, prompt default, core/runtime/schema or queue status changed. The earlier numerical model remains valid in its scope; SR-C1 remains a failed24-call diagnostic. This study supplies no demonstrated improvement in downstream arithmetic, causal identification, a complete multi-step report, autonomous source selection, or broad FRR reasoning.

## Strongest next

Fill the missing crossed cell: apply the **already specified C2 questions** to the eight C3 passages, using frozen existing keys and the original C3 calls as paired controls. No new wording search is needed. This would measure whether the observed family-specific question effect persists on the new records; it would still be a small exposed-fixture sensitivity test, not independent final validation. Only after source-role reading works on genuinely new facts should we reconnect explicit arithmetic with validated inputs. No background run remains active.
