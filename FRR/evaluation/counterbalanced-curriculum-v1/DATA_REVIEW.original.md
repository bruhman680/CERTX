# Separate-agent review of counterbalanced curriculum fixtures

31 October 2026. Reviewed /workspace/curriculum_data/generator.py, README.md, DATA_CHECKS.json, and all six DATA JSON files. This was a separate agent consistency review before inspecting candidate study results. No model calls, training, network access, generator execution, or fixture edits were performed. The only written file is this report. This is not independent ground-truth collection or replication.

No blocking issue was found. Independent parsing of every real source body—not merely the generator's metadata—confirmed all 144 training, 72 primary, and 12 development source/label pairs. All 228 sources are distinct, all six declared data hashes match, all factorial cells are present once, and all 36 primary body pairs have identical bytes with only the target header changed.

## Source-derived semantic checks

Parsed XML with an XML parser, flatJSON as two separate JSON records, bullets by their named sections, tables by their rows, and fields/prose by their explicit batch/count phrases. For each source, independently selected the header-named record, extracted its sampled-soil count, derived positive/zero/missing and YES/NO/WITHHOLD, and compared every supplied semantic and record field. Verified target_value, other_value, target/other state, expected label, identity, role, first/last position, family, all ordered records, record_position, and is_target. Training label, target, and distractor fields also agree. IDs and source/key alignment are unique and consistent.

Both records are complete and explicitly named. Source bodies contain no target/other role words. Every record has observations per soil 5, damaged plots 0, and unavailable inspections. Target and non-target positive sampled-soil values are equal within each split: training 11, primary 13, dev 17. Zero is explicitly 0. Missing is JSON null, XML `unavailable`, or `not recorded` in the remaining formats, all covered by guidance. The identical irrelevant fields remove the previous observation-value cue to target identity. No XML or bullet scope ambiguity was found.

The guidance file matches the old task's declared guidance hash, a3ae0344da886994707e581d3fe56a0b61cc2bf3a11ccfaca8a4dbcdd382bdd5.

## Coverage and header-only primary contrasts

| Split | Cases | Formats | Labels | Identities | Positive sampled-soil value |
|---|---:|---|---|---|---:|
| Train | 144 | fields, prose, flatJSON, table | 48 each | Birch, Cedar | 11 |
| Primary | 72 | XML, bulletsections | 24 each | Hazel, Larch | 13 |
| Dev | 12 | four training formats | 4 each | Birch, Cedar | 17 |

Training is the full 4 formats × 3 target states × 3 non-target states × 2 target identities × 2 target positions. Each of its 48 consecutive triples has labels YES, NO, WITHHOLD while format, non-target state, target identity, and position stay fixed. This supports 48 balanced three-record updates if the runner consumes that order as declared. The data alone cannot establish what the actual loader does.

Primary is the full 2 formats × 3 target states × 3 non-target states × 2 target identities × 2 target positions. XML and bullet forms are absent from candidate training; Hazel/Larch are absent from candidate training and dev. These are training-unseen identities within this fixture set. They appeared in earlier task fixtures, so they must not be described as globally unexposed names.

Primary has 36 exact ordered-body pairs, with opposite target headers Hazel and Larch. Every pair is byte-identical below the first newline. There are 24 discordant-state pairs (48 cases) whose correct label changes when the header changes, and 12 same-state pairs (24 cases) whose correct label stays fixed. Both names occur as target and non-target, in both body positions, with every state combination. Equal positive values permit a true header-only comparison without changing either body's counts.

The dev set is a small familiar-format check: each format has one target identity/position and positive non-target count 17, with three target states. Thus it is balanced by label but not a complete dev factorial. Identity and position are coupled with format in dev. Both records using positive 17 where applicable keeps even target-zero/missing sources textually distinct from training. Dev should not be presented as a broad generalization test.

## Leakage and useful baselines

Primary and dev case objects contain exactly id, split, structure_family, and source; key metadata is separate. Their IDs encode semantic states, and training records contain explicit answer metadata. Consequently the model input must be constructed only from GUIDANCE and source. Passing a whole case dictionary, ID, label, expected, records, or key fields into the prompt would invalidate the comparison. This is a runner condition, not a defect in the source-only fixtures.

No exact source text overlaps among train, primary, and dev. There is intended template/state reuse within split and across renderings, so unique text does not mean independent draws. No exhaustive external contamination search was attempted.

For the 72 primary cases, always reading the first or last sampled-soil value scores 48/72 (66.7%): it reads the target in 36 cases and the same-state non-target in another 12. A fixed named-record policy also gets 48/72. A constant label gets 24/72. Reading only the non-target gets 24/72. On the 48 discordant cases, first/last and fixed-name shortcuts get 24/48; a constant label gets 16/48.

More generally, any deterministic header-blind predictor that sees the same body twice has at most 48/72 overall: at most one correct answer per discordant pair plus both correct answers per same-state pair. It cannot get both labels correct for any discordant pair. Report both-correct discordant-pair accuracy, individual accuracy on discordant cases, both-correct same-state-pair accuracy, and class/format/position breakdowns. A label flip alone is insufficient: both answers should match their respective keys. The 24 same-state cases are useful controls but cannot establish target selection by themselves. These are authored dependent pairs, not 72 independent observations.

## Comparison interpretation and remaining limits

The declared comparison reuses the old mean-objective checkpoint trained for 48 updates on 72 sources over two passes and trains the candidate for 48 updates on 144 sources over one pass. With three examples per update, both expose 144 examples, but candidate unique support doubles while repeated exposure changes. The package also changes record symmetry/completeness, both-identity selection, ordering, positive-number support, and training format details (including two flat JSON records and a different table form). Any measured gain estimates the effect of this complete curriculum package under the fixed update budget. It cannot isolate record position, header pairing, unique-data quantity, or any one of these changes causally. Old-checkpoint provenance and actual execution were outside this fixture audit.

The primary pairs make header dependence directly testable and close the prior universal final-value shortcut. They remain a narrow two-record, two-name, one-positive-magnitude control with fixed within-record field order. Format and identity novelty occur together in primary, so a result does not separate their individual effects. Primary and training also differ in positive magnitude; XML introduces a different explicit missing marker. Generalization to additional names, more records, field reordering, absent fields, duplicate/conflicting records, negative values, or other data domains is untested. Balanced coverage removes the listed simple correlations; it does not prove an internal reasoning mechanism or universal scope binding.

The generator's built-in validate function checks extensive metadata invariants and body-pair equality, but does not independently parse rendered bodies back to typed records. The independent source parsing performed for this review closes that consistency gap for these reviewed bytes. Freeze the generator and final fixtures before any primary forward pass; preserve prior prepared sets and report any later revisions separately.
