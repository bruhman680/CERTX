# Separate-agent review of decision-token preparation data

Reviewed 31 October 2026, before seeing any new-study output. This is an independent agent consistency review of the coordinator-authored source/key pair and proposed comparison. It is not independent ground-truth collection, blinded annotation, an independent training run, or replication. No model calls, training, or network access were used. No FRR file was changed. The only created artifact is this report.

## Finding

No blocking source/key error was found. All 24 primary sources unambiguously specify the named target record or section, and every supplied positive/zero/missing key agrees with that record. The proposed matched two-arm comparison can estimate the effect of the declared loss reallocation on this fixed authored evaluation set. It cannot by itself identify a general token-length cause, robust source binding, or population-level generalization.

## Scope and preservation

Read decision-token-preparation-v1/PROTOCOL.md, NEW_PRIMARY_CASES.json, NEW_PRIMARY_KEYS.json, SOURCE_BINDINGS.json, and FREEZE.json; lora-state-pilot-v1/TRAIN.json, GUIDANCE.json, and EVAL_CASES.json. Checked file bytes against all six hashes in the preparation FREEZE and all four reuse hashes in SOURCE_BINDINGS; all ten match. Hashing the referenced control artifacts and old KEYS file did not inspect study outputs or execute their code. The proposed new training runner is explicitly recorded as not implemented in the preparation freeze; that historical status does not certify a later runner.

## Primary semantic audit: 24 of 24 keys agree

Separately extracted the target batch from each source header, selected its XML record or bullet section, extracted that record's sampled-soil field, and derived YES for positive, NO for zero, WITHHOLD for missing. All IDs are unique, all key IDs match source IDs, and both expected label and target_value agree in every case. This extraction is independent of the key lookup; the semantic rule still comes from the authored guidance.

Each row below identifies three individually checked IDs, with suffixes `_positive`, `_zero`, `_missing`. Positive counts, zero, and the explicit marker `not recorded` produce the shown labels in each format.

| ID prefix | Target | Positive → YES | Zero → NO | Missing → WITHHOLD | Other count / target observations per soil |
|---|---|---:|---:|---|---|
| DT_xml_records_0 | Spruce | 5 | 0 | not recorded | 0 / 0 |
| DT_xml_records_1 | Larch | 8 | 0 | not recorded | 9 / 9 |
| DT_xml_records_2 | Hazel | 14 | 0 | not recorded | unavailable / unavailable |
| DT_xml_records_3 | Alder | 21 | 0 | not recorded | 16 / 16 |
| DT_bullet_sections_0 | Spruce | 5 | 0 | not recorded | 0 / 0 |
| DT_bullet_sections_1 | Larch | 8 | 0 | not recorded | 9 / 9 |
| DT_bullet_sections_2 | Hazel | 14 | 0 | not recorded | unavailable / unavailable |
| DT_bullet_sections_3 | Alder | 21 | 0 | not recorded | 16 / 16 |

The batch names do not collide with Other. XML has exactly one record per named target and explicit batch attributes. Bullets have distinct named section headers and exactly one sampled-soil entry in the target section. Neither representation has a semantic target-versus-Other ambiguity under GUIDANCE. Zero is explicitly recorded and differs from missing; unavailable inspections or observations cannot replace the target field.

The primary set has eight examples per label, twelve per format, and four per label within each format. Any fixed valid-label constant gets 8/24 overall and 4/12 in either format. Each format repeats the same four semantic settings, so there are 24 paired authored cases, eight setting-by-format triplets, and only four distinct semantic settings shared across formats. These are dependent contrasts rather than 24 independent samples.

## What the controls identify and leave unresolved

Within each three-case triplet, only the target sampled-soil value changes. This rules out solving the triplet from its batch name, Other count, target observations count, constant damaged-plots zero, or unavailable inspections alone. Conflicting Other values in the zero/missing cases provide useful distractors.

However, every new source places Other first and the target second, and the target sampled-soil value is the final sampled-soil occurrence and final value. A rule that classifies the last sampled-soil value—or simply the final value—can score perfectly without using the target batch name. Therefore success is evidence for transfer on these representations, not a diagnostic demonstration of named-batch binding. The new formats resemble an XML/bullet rendering of the older records rather than independent task domains.

Other count always equals target observations-per-soil count. Their error predictions are identical here, so errors cannot distinguish wrong-batch reading from wrong-field reading. Positive/zero/missing triplets can reveal insensitivity to the target field, but cannot identify which of those two distractor routes caused it. Missing target values always use `not recorded` in the new set; new-format generalization to explicit null, unavailable, absent fields, malformed records, negatives, conflicting duplicate records, reordered target/Other positions, and target selection among multiple candidate batches is untested. These are limitations to report, not grounds to change the frozen primary set after results.

## Train, dev, overlap

TRAIN has exactly 72 train records: 24 YES, 24 NO, 24 WITHHOLD. Its four families (fields, prose, json, table) each have 18 records, six per label. Six semantic settings are rendered in all four families. Every triplet has correct target/state/label correspondence on reading: positive counts 1, 2, 4, 9, 17, 23; zeros 0; missing `not recorded` or JSON null. Thus the 72 are balanced records, not 72 independent semantic settings. Dataset balance alone does not establish balance of every optimizer update; the actual later sampler/runner must preserve the declared balanced update policy.

EVAL_CASES contains 12 dev plus 48 old test records. Dev has four familiar format families, one Maple setting (positive 11, distractor 13), three states in each family, and four examples per label. It is a known source reused from the previous pilot. It is a narrow familiar-format check, not fresh primary evidence, and should not drive unreported choice between the new arms. The old 48 test records have four previously exposed structural families (scoped_table, nested_list, register, interleaved) and belong in a separately reported regression table.

There is no exact source-text overlap between TRAIN and EVAL_CASES, or between the 24 new primary sources and TRAIN plus EVAL_CASES. New primary family names and target batch names are distinct from those in train/dev/old-test sources. This establishes literal novelty within these files, not an exhaustive search for prior exposure. Format and name novelty do not eliminate shared templates, repeated semantics, or the positional shortcut described above. Freshness before first model forward is an execution/provenance claim that cannot be independently established by reading source files alone.

## Loss math and causal interpretation

Let m be the number of supervised tokens in a label including EOS, and let e_i be the CE of token i after correct causal alignment. The old per-sequence mean is sum(e_i)/m. The proposed sequence loss is 0.5 e_1 + 0.5 sum(e_i for i=2..m)/(m-1). Averaging three equally represented classes implements the declared one-third class average. EOS must be supervised so m is at least two; prompts and padding must be masked consistently.

Old token weights are 1/m; new first-token weight is 1/2 and each remaining token weight is 1/[2(m-1)]. Their total is one per sequence in both objectives. They are identical for m=2. If a label is split into more than one token, its first-token weight increases and all its suffix/EOS weights decrease. This changes the optimization allocation even though total coefficient mass per sequence is fixed; it does not guarantee equal gradient norms, equal semantic difficulty, or improved decisions. The exact changed class weights require checking the actual label tokenization in the final prompt boundary. Strings alone do not establish those token counts.

A matched fresh initialization, unchanged semantic labels/prompts/data/order, identical 48 updates, optimizer/decode policy, and identical evaluation supports a paired comparison of these two complete loss allocations for one seed. It does not separate increased first-token emphasis from reduced suffix/EOS emphasis, their interaction with optimization, or any resulting optimization difficulty. A loss difference is not an inference-time label-length manipulation. With one-token aliases plus EOS, these two objectives coincide, as the protocol correctly states; no alias experiment is required for this phase and none is inferred here.

A gain on 24 whole-label generated answers would support the narrow claim that this reallocation improved this run on this authored split. It would not prove token length caused the prior failure, establish model-internal missingness reasoning, or provide independent-seed robustness. A tie does not establish equivalence. Compare whole-label accuracy using the full denominator, per-label and per-family recall, paired case changes, malformed/capped/non-completed outputs, and the 8/24 constant baseline; keep dev and old regressions separate. Preserve the first-forward exposure boundary and do not tune on the new primary results. Any later changes should be recorded as a follow-up with the original scores retained.
