# Prospective protocol review, before execution

The fixed oracle generator, condition budget, calibration/evaluation split and actual-retrieved-record metrics are coherent. U/ABSTAIN separation and conservative missing-centre policy are explicit. Projection receives the supplied layout, not learned semantic structure. Shared/noiseless query repetitions and cross-condition reuse must remain visible.

Two implementation-facing clarifications requested before code approval:

1. State the full direct published S equation, including its energy-balance R factor. Exact unit normalization makes R=1 mathematically but should not silently redefine the target formula in an implementation check.
2. Define agreement@1 as the top-ranked true key matching query entity/time/A, independent of decoded stance. A metric based on whether the decoder says A is different and should be separately named. Define encoded-U recall per query as retrieval plus correct decoding of the one relevant U item.

These are prospective specification clarifications, not observed outcome failures. Implementation is being written and has not run; full preflight approval awaits code inspection.

Source scouts support interpretation boundaries: complex relational methods require their learned operator/triple contracts; identifiability results do not establish recovery of our intentionally supplied block partition; probability calibration benchmarks do not calibrate angular-centre confidence. No change to the fixed empirical grid is requested from those readings.
