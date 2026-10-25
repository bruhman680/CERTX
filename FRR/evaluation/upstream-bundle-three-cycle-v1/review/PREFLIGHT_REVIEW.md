# Prospective code and protocol review

Verdict: approved for the one fixed main run, after prospective clarifications and reporting fixes. No study outcomes were generated or consulted for this approval. Reviewer read implementation, protocol, schema, and implementation note; syntax compilation is not a study execution.

The final implementation matches the declared generator, disjoint calibration/evaluation entities, reused noise streams, normalization, full published S factor, real A/B product convention, known-block projection and actual top3 decode paths. Gold scope/status are used only for scoring and calibration labels/oracle diagnostic, not for inference on retrieved records. The 10368-row grid and 41472 method records follow the specified loops.

The exact-query/array hash freeze precedes fitting and scoring. Runtime bound must additionally be enforced by the launch wrapper: the script reports elapsed time after completion rather than internally terminating at180seconds. Publication should exclude generated __pycache__/pyc files; they are not scientific artifacts.

U and ABSTAIN remain distinct. Missing any centre deliberately makes the whole three-way decoder unavailable; this is a conservative policy, not proof that every A/U item lost information. Zero products and tied centre distances are explicit. Added reason-specific abstention counts and decoder availability retain that distinction in aggregates.

Preserved prospective changes: initial protocol named S without full formula; initial code is saved; complete R factor and retrieval-only agreement@1 were clarified; raw/normalized channel controls and pre-scoring query hashes were added; experiment_PREFLIGHT_01.py preserves the code before reason-count reporting. None used outcome feedback.

Scope caveats: block partition and source status phases are supplied; centres are fitted geometric labels, not calibrated probabilities; codebook U anglepi/3 is arbitrary; repeated queries/conditions are dependent; no learned encoder, real language, agent reasoning, or product efficacy is tested. Potential last-bit top3 mismatch near ties must be reported separately from numeric algebra equality. Source scouts inform these assumptions without changing the fixed empirical grid.
