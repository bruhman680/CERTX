# Counterbalanced batch-state curriculum

Run `python generator.py` to regenerate fixtures and `DATA_CHECKS.json`. The generator performs no network, model, or training operations.

- `DATA/TRAIN.json`: 144 labeled cases, ordered as 48 contiguous YES/NO/WITHHOLD triples. Each triple fixes format, other-record state, target identity, and target position. Four training formats are fields, prose, flat JSON records, and table.
- `DATA/PRIMARY_CASES.json`: 72 source-only cases with exactly `id`, `split`, `structure_family`, and `source`. XML and bullet sections are wholly held out from training. `DATA/PRIMARY_KEYS.json` holds labels, pair identities, and record metadata separately.
- `DATA/DEV_CASES.json`: 12 familiar-format source-only development cases. `DATA/DEV_KEYS.json` holds their labels and metadata separately.
- `DATA/GUIDANCE.json`: exact guidance from the existing lora-state-pilot-v1 task.

Birch/Cedar training records use positive 11. Hazel/Larch primary records use positive 13. Birch/Cedar development records use positive 17. Every record contains observations per soil 5, damaged plots 0, and unavailable inspections. The body uses batch identities without target/other role words; only the header selects the target.

The 72 primary sources form 36 pairs with byte-identical ordered fact bodies and different target headers: 24 discordant-state pairs (48 cases) and 12 same-state pairs (24 cases). All 228 sources are unique. Primary, train, and development labels are each balanced. The development fixtures use a positive other-record count of 17 to keep every source distinct from training, including target zero and missing cases.

The intended comparison is this training package versus the existing old 72-source-trained mean checkpoint, with the same 48 updates. Format and support also change, so the comparison cannot isolate record-position causality.
