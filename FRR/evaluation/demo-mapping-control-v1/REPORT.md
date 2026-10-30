# DM-C1: demonstration mapping, an affirmative floor, and concealed score sensitivity

29 October2026 America/Chicago. User authorized resumed experiments, scouts and reviewers. One frozen primary experiment, one separately frozen secondary diagnostic and a navigation repair completed. Inference only; no model training or prompt promotion.

## What changed in our understanding

All27generated answers affirm the target passes. This includes unmeasured and below-threshold targets. Correct/permuted demonstration labels produce zero semantic decision changes and three text changes. That result alone cannot establish label insensitivity: a new, separately frozen readout shows changed literal-label scores beneath identical affirmative decisions. Conversely, changed scores cannot establish task competence. Keep representation sensitivity, selected behavior and warranted answer quality separate.

## Primary design and controls

[Design](DESIGN.md), [cases](CASES.json), [examples](EXAMPLES.json), [contract](SCORING_CONTRACT.md), [freeze](FREEZE.json), [runner](run.py). Nine fresh authored threshold questions: ParcelCedar9kg with missing/6/12kg; TankAmber12liters with missing/8/16liters; BeamSilver15cm with missing/10/20cm. Gold is balanced3YES/3NO/3UNKNOWN. UNKNOWN is explicitly requested for missing measurements. The examples use RodIndigo5cm with7/3/missing measurements. The Beam unit matches the example, so these are limited near-transfer tasks, not wholly distinct-domain evidence.

Three arms hold ordinary guidance and target records fixed:

- **None:** no examples; structural reference with fewer tokens/information.
- **Correct:** example answers YES,NO,UNKNOWN.
- **Permuted:** identical facts/questions/order/format but example answers NO,UNKNOWN,YES. This preserves the label multiset while deliberately making the example answers wrong.

Correct/permuted full prompts match token counts per item (280–284); no-example prompts135–139. Equality of lengths does not make token identities/positions equivalent. Target gold is evaluator metadata, not inserted into model messages. Target facts legitimately determine gold; no hidden/held-out-data claim.

Pinned SmolLM2-135M-Instruct revision12fd25f77366fa6b3b4b768ec3050bf629380bac, CPUfloat32/eager attention/two threads, greedy96newtoken cap, fresh calls/caches, rotated arm order. All27stop atEOS; no semantic retry/tuning. They are27branches of one checkpoint over9exposed authored cases sharing3templates, not27independent models or a population efficacy trial. Final response requests and label vocabulary differ from preceding pilots, so do not interpret changed cross-study totals causally.

## Primary results

| Arm | Explicit matches | Evidence-status matches | Fully warranted | Unsupported certainty on missing measurement | New generated tokens |
|---|---:|---:|---:|---:|---:|
|None|3/9|3/9|3/9|3/9|106|
|Correct examples|3/9|3/9|3/9|3/9|24|
|Permuted examples|3/9|3/9|3/9|3/9|29|

Every primary semantic decision isYES. All successes are above-threshold cases. None of the three missing measurements receivesUNKNOWN; none of the three below-threshold cases receivesNO. No substantive example entity/quantity/block or conditional rule appears in these continuations. A bareYES cannot establish copying because it is also a valid answer token. No answer adds a fabricated quantity or extra explanatory rule; this secondary material-error flag being zero does **not** make the wrong/unsupported decisions acceptable.

Between the matched correct/permuted arms,3/9exact texts change and0/9semantic decisions change. Two outputs in the full run say 'The records establish that Tank Amber passes' without a literal leading label: surface labelNONE, explicit task decisionYES. See [summary and all paired texts](SUMMARY.json), [raw generated continuations and exact inputs](RAW_OUTPUTS.jsonl).

Correct/permuted total input tokens2539each; none1234. Measured inference sums excluding load/serialization are9.615seconds for correct examples,10.024for permuted examples and11.301for none. These are workload observations, not controlled speed, energy, monetary-cost or remaining-compute measurements.

## Independent coding

Root read all27texts and deposited [initial scores](ROOT_SCORES.json), then froze them. Another agent received shuffled target-record/question/gold/output packets without arm mapping/prompts/root scores. Initial reviewer deposit was frozen before comparison. [297field comparisons](REVIEW_COMPARISON.json), eleven fields per response, agree with zero differences; no reconciliation needed. [Review](review/MASKED_REVIEW.md), [review freeze](REVIEW_FREEZE.json). Shared-filesystem masking was instructional; style can reveal conditions. Another scoring judgment is not independent model/scientific replication.

## Secondary diagnostic: unchanged answer does not mean unchanged scores

This followup was chosen **after** primary results; it was not preregistered as part of the original experiment. [Prospective review](review/READOUT_PROSPECTIVE.md), [new freeze](READOUT_FREEZE.json), [probe code](readout_probe.py). It replays the18saved matched-arm input token sequences and scores three fixed uppercase candidate prefixes by teacher forcing. It does not generate18newfreeanswers, train weights, load old caches or modify them.

For candidate sequence c with tokens c1...cm and prompt x:

    ell(c|x) = sum_j log p(c_j | x,c_<j)
    restricted_weight(c|x) = exp(ell(c|x)) / sum_{d in {YES,NO,UNKNOWN}} exp(ell(d|x))

The literal tokenizations have2tokens forYES,1forNO,3forUNKNOWN. NoEOS is included. These are candidate-prefix sequence scores, not full answer probabilities. The restricted normalization excludes every other spelling and continuation, including the generated 'Yes' and explanatory sentences; it is **not semantic confidence**. Unequal sequence lengths and capitalization remain visible, not adjusted after measurement.

Across all9paired inputs:

- UppercaseYES remains the highest-scored of the three literal candidates in both arms.
- Permutation lowersYESraw logscore by0.492–0.673nats, increasesNO by0.564–0.631 andUNKNOWN by0.675–0.868.
- YESrestricted weight falls12.80–16.10percentage points (mean15.06); this is a change within the chosen subset, not confidence or answer accuracy.
- Summed raw mass for these three mutually distinct literal candidate prefixes spans only0.04846–0.17010 over18prompts. Most possible continuation mass is outside the measurement.

[Raw readout scores](READOUT_SCORES.json) and [paired calculations](READOUT_SUMMARY.json) expose all values and token IDs. A separate [saved-data readout review](review/READOUT_REVIEW.md) recomputed108comparisons; [final report review](review/FINAL_REVIEW.md) found no blocking correction. The repeated direction across targets is compatible with general label/serialization sensitivity; it does not identify target-dependent abstract mapping, positional copying or a neural mechanism. No significance or population claim. This rescues a measurement distinction, not the model's task performance. Readout forward-compute sum71.203seconds excludes model load and is additional to primary inference; no new generated-token count is claimed.

## Source weave and lateral finding

[Bounded scout](review/SCOUT.md): three primary selected-section readings. Yoo etal2022 distinguishes distribution-preserving label shuffles and competence limits. From Copying to Composition2610.19113v1 motivates separating copied completion from composed mapping, including larger SmolLM2 experiments. Readout Shortcut2605.22870v1 cautions that a final output can differ from an intermediate representation, in a different teacher-forced arithmetic setup. These sources motivate discriminators; none diagnoses this135Mcheckpoint or establishes an FRR improvement. No paper/code/training replication.

A separate [navigation review](review/NAVIGATION_REVIEW.md) found accumulated 'Latest' paragraphs alongside older active-sounding pause instructions. Five navigation originals are byte-preserved under navigation_before with [original-path/hash receipt](NAVIGATION_ARCHIVE.json). Current handoff/orientation now clearly separate completed work from unexecuted proposals. Historical relative links retain their old base; use original paths at parent76ef0080ad20a3de29ee171117a696ecf2ba4862. Archive hashes establish byte identity, not source truth. No observed navigation-induced agent error or measured behavioral benefit is claimed.

## Preservation and next useful move

2362previous files verified unchanged after generation before intentional navigation updates, including prior cache branches and weights.27new terminal caches are saved locally under/workspace/smollm_demo_mapping_states_v1 with hashes, token sequences and cache lengths. The last generated token may not be forwarded; manifests say so explicitly. Binary model/cache files are not uploaded; text pins and manifests preserve reconstruction information, not guaranteed workspace durability. Final checks account separately for the five archived navigation replacements. Old scientific reports/deposits/failures remain unchanged; core0.2/schema0.1/queue statuses unchanged. No paid modelAPI/rental/purchase initiated.

**Strongest next:** a separately frozen competence/representation probe: extract actual measured value and criterion, compare them, then test uncertainty and answer-polarity/format separately. Balance the direction and labels so indiscriminateYES cannot appear useful. Only then ask whether an optional reasoning instruction helps this model apply information it can access. A stronger model may be informative if it fits included/free compute, but no paid service is implied.

**Lateral:** an independently sourced revision task remains legitimate now, under matched access and inspectable original/changed evidence. Source-binding or quoted-versus-applied examples can follow with counterbalanced mappings/order. No requirement that a toy 'succeed' before external contact. These proposals have not run. No automatic next cycle or background experiment is left running at delivery.

[Final scoped integrity/link/package checks](FINAL_CHECKS.json) distinguish preservation from scientific validity.
