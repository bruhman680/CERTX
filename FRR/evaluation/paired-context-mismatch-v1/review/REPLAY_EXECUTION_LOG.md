# Replay execution record

1. Syntax-only `python -m py_compile review/replay.py` before saved outcomes: passed.
2. First saved-array audit execution: stopped with `KeyError: 'returned_predictions'` when reading a ledger record. No experimental artifact was mutated. Read the first saved ledger's field names; corrected the review script to use `predictions` and `reasons`.
3. Completed saved-array audit: 18,461 checks, zero failures; 73 same-set ordering differences.
4. Added exact saved-score sort/ledger score/angle checks, structural JSON principal-cosine comparisons and independent real/imaginary channel products. Final audit: 23,621 checks, zero failures; same 73 ordering differences. Final machine-readable results are in `REPLAY_RESULTS.json`.

Both completed executions replayed identical saved main outputs. No main execution, parameter change, artifact modification or experiment rerun occurred in this audit.
