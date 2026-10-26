# Storage and transport note

Full candidate-level outputs make the byte-exact archive25,950,288bytes. Git stores it as26ordered volumes with per-volume hashes; assembly reproduces the original archive exactly. Volumes are storage boundaries, not independent experiments. RESTORE.md gives verification/extraction.

An initial oversized workspace-to-tool read caused a JSON control-character/truncation error during upload preparation. The branch and scientific artifacts were unchanged. Smaller350,000-character reads transferred the same base64 bytes; every created binary blob was checked against its locally computed Git blob SHA. This was a publication transport adjustment, not a new or repaired experiment. Final tree/head verification and preservation of historical blobs are checked separately at deposition.
