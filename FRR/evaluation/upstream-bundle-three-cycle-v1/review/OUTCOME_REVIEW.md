# UB-C3 outcome and interpretation review

Verdict: the fixed run and saved metrics support the scoped findings below. Prospective code inspection approved SHA256270e4c53103998d7cf9b74c420e2e6c7d4df457db358410816a6134e826128b9 with protocol905480dd73bd53f976f8f4473056fe2a314604a7877b8a8a1dbc2729ba8dc3d0 before outcomes. The reviewer did not execute the main study or import implementation functions into the audit.

## All-ledger check

[audit_ledger.py](audit_ledger.py) independently recomputes every recorded retrieval/decoding metric from actual returned IDs, predictions, reasons and centre availability. All10368query-condition rows and41472method records agree; all1296full-condition aggregates match recomputed sums/denominators/means. No incorrect entity/time gets label credit; relevant U is not confused with ABSTAIN. Conservative missing-centre policy and per-reason abstention counts remain visible. [LEDGER_AUDIT.json](LEDGER_AUDIT.json) saves8passing checks and no discrepancies.

This is metric reconstruction, not independent empirical replication or a complete array replay. The separate replay auditor reconstructs arrays/centres/readouts on a prospectively chosen sample without importing experiment.py. Their sample reports22rows/88readouts/99centre diagnostics agreeing within1e-10; two binding order-only near-tie differences leave top3sets unchanged. Their saved results should not be described as bitwise-identical rank replay.

Numerical controls report zero discrepancies above declared1e-10 tolerance, zero complex/real-modulus top3set mismatches and zero cosine/S top3set mismatches across1728generated query-condition comparisons per control. Exact-source identities supply generality; these finite checks validate the implementation in this input range. Calibration/evaluation entity overlap is0. Runtime was below the declared180seconds.

## Component versus pipeline findings

Under GLOBAL encoding, full cosine's oracle-relevant stance accuracy is1 but complete evidence retrieval and joint complete success are0 across the fixed grid. Its mean evidence recall is about.539. The conditional diagnostic alone would therefore hide total failure of the full three-record goal. Full modulus and its matched real A/B implementation have joint complete success1 in this bounded oracle GLOBAL grid; that does not establish universal robustness or learned language competence.

For SCOPED encoding, across the full deliberately mixed grid, full modulus evidence completeness is about.309 but joint completeness only about.106; oracle stance accuracy is about.477. These descriptive means combine selected calibration/weight/noise conditions and are not population estimates. More interpretable clean matched-calibration witnesses are:

| Context ratio | Full-modulus oracle stance accuracy | Full-modulus complete evidence | Full-modulus joint complete | Mechanism |
|---|---:|---:|---:|---|
|.5|1|.9167|.9167|Some relevant records lose retrieval competition despite correctly readable stance when given them.|
|1|0|0|0|The N calibration product vanishes; the declared conservative three-way decoder abstains globally. Evidence recall still2/3.|
|2|1/3|.1875|0|A/N angle centres collide; angle-only decoding abstains on those classes.|

Each row pools96paired/noiseless query uses across3seeds, not96independent claims. The r1 global abstention is an evaluator policy when one class centre is unavailable; it does not prove that A or U individually lost information. The r2 collision is a limitation of this angle readout under the supplied mixture, not proof the whole vector became identical.

Known binding-block projection yields noiseless joint success1 in those three matched settings. Its average joint completeness over the selected grid is about.951, with degradation under noise. This control uses a supplied semantic partition; it is not a learned separator. Its GLOBAL/SCOPED binding inputs are the same by construction, so identical mode-level outcomes are not independent confirmations. Removing context can also discard useful signal/SNR: GLOBAL full modulus outperforms the projected binding method in this grid. Projection is not universally preferable.

Modulus deliberately ignores stance during relevance ranking, so status variants mathematically tie. Its agreement@1 can be affected by last-bit ordering even when evidence and decoded labels are correct; e.g clean binding results show top1-A rates below1 while joint success is1. Do not interpret that as lost stance. Exact top3set/joint metrics are the primary evidence goal here.

## Interpretation limits and upstream meaning

A/N/U status assignment, query orientation, phase convention and block layout are oracle supplied. U is an encoded source-level label, not a decoder probability; ABSTAIN is a numerical/calibration ambiguity outcome. Fitting a circular centre does not calibrate epistemic confidence. Repeated noise draws and reused arrays/conditions are paired; query hashes show1728IDs but only720distinct evaluation array byte hashes, each ID reused under6calibration conditions. These are48latent evaluation entity/time claims across seeds, not10368independent experiments.

The direct source works concern learned graph triples/operators, not sentence stance. The lateral identifiability theorem concerns unobserved factors under its assumptions, not our intentionally known partition; its calibration benchmark concerns predictive probabilities, not circular means. Their implications are design constraints, not extra evidence that this synthetic result transfers.

The user's broader-bundle intuition is usefully operationalized as a staged map: source/status assignment, representation/layout, phase operator, noise, retrieval, centre fitting and task scoring. A readout can have multiple input preimages while full records remain distinct. Nothing here proves a formal topological fiber bundle, universal shared error source, learned semantics or agent-group advantage.

Next useful upstream boundary is whether the block partition is supplied, transported with coordinate changes, inferred, or lost; a common orthogonal change preserves full inner products while a fixed binding-coordinate mask requires a correspondingly transported projection. This is a proposed later control, not added to the completed grid. An encoder-learning contact would require its own held-out data and measurement design.

All prospective formula/metric/reporting repairs were preserved before execution. No post-outcome code/grid adjustment or extra main run was needed. Three cycles can close with these scoped findings and the explicit next boundary.
