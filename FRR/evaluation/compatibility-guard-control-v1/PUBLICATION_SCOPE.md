# Storage and publication scope

The GitHub intake publishes source, protocols, hashes, parameters, all27,000 compact evaluation records, summaries and validations. The original report also points to local full `evaluations.npz` and verbose `evaluations.jsonl`; those two files remain in the current workspace and are excluded from this compact GitHub publication. Their exact byte sizes and SHA-256 hashes are recorded in ARTIFACT_MANIFEST.json. A hash is not a backup of its input.

The compact artifact preserves labels, candidate masks and minimum distances, not the complete A/B arrays, full feature matrix or all three distances. Full-input reinspection and the post hoc nearest-selector script use the local NPZ. Regeneration uses the pinned generator, saved seeds and NumPy version, with input hashes to check equality; cross-version equality is not assumed. The runner and export must be run before a fresh nearest-selector replay if the NPZ is absent.

Parent artifacts, including the original report and artifact manifest, are retained unchanged. The nearest-selector contact is explicitly post hoc. ROOT_AUDIT.stdout records an additional independent reconstruction of all27,000 set labels and rates from the published compact masks.
