# Restore exact numerical outputs

Full original run outputs are in run-exact.tar.xz. Verify its SHA256 and byte count against ARCHIVE_MANIFEST.json before extraction. From this planning directory run `tar -xJf run-exact.tar.xz`; it restores run/results.json and run/root_outcomes.tsv. Verify each extracted file against the manifest. Do not overwrite an existing divergent run without preserving it first. ROOT_OUTCOMES.tsv is a byte-identical readable copy of the twenty root rows, not a replacement for full output.

No new experiment execution is needed to inspect the saved evidence. Independent replay used the complete original run before archival; code and audit records are saved alongside. A deliberate new reproduction should use a separate output directory and record its own provenance.
