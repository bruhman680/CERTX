# Serialization repair

The first numerical execution reached output serialization and failed because a NumPy boolean is not accepted by the ordinary JSON encoder. No RESULTS.json was written. The original source and execution streams are retained as INITIAL_FAILED artifacts. A subsequent summary-read command also failed because that result file did not yet exist; that orchestration error is visible in the tool trace.

The serializer was changed to explicitly convert NumPy scalars to native values and reject nonfinite JSON. No losses, intervals, thresholds, actions, probes or numerical method changed. The repaired execution passed all eight checks. Its first scalar-conversion lambda was then tightened to raise TypeError for unsupported types rather than silently use null; a strict replay and independent review will check final output identity. This is an exporter refinement, not a new scientific experiment or selected successful sample.
