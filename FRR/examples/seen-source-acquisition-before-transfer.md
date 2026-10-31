# Seen-source acquisition before interpreting transfer

Optional guidance for small local supervised pilots, informed by the [counterbalanced curriculum contact](../evaluation/counterbalanced-curriculum-v1/REPORT.md).

A low teacher-forced token loss and valid answer formatting do not establish the requested class decision. After a held-out failure, a separately declared small balanced seen-source diagnostic can help distinguish failure to acquire those checked lessons from a claim of pure transfer failure. Evaluate exact generation and each class, retain invalid/unresolved responses, state which seen cases were selected, and keep their result separate from held-out evidence.

A constant-answer baseline on that slice means acquisition is not demonstrated there. It is not a statement about every training example, all models, general FRR, or universal capacity. Do not tune repeatedly on a reserved primary set; once exposed, keep it as regression material and create fresh primary cases. Header response changes and both-correct header pairs are different metrics; compare plausible header-only/field-position policies too.

Before increasing task complexity or spending a larger transfer budget, establish a useful simple acquisition/readout interface under a frozen protocol. No universal accuracy threshold or mandatory new approval gate is defined here. Model-generated labels remain proposals; source-bound deterministic checks retain their own scopes and authority.


## A demonstrated small rung, and the next boundary

The [simple readout contact](../evaluation/simple-readout-acquisition-v1/REPORT.md) learns an explicitly supplied positive/zero/missing status under all four tested interfaces. Both canonical words and cyclic single-token codes work. This is neither detecting real missing evidence nor generalizing to harder record selection. The [bridge](../evaluation/readout-selection-bridge-v1/REPORT.md) fails full two-record inputs despite a successful source-parsed crop; the [single-record full-frame control](../evaluation/readout-selection-bridge-v1/frame-control/REPORT.md) succeeds.

When useful, distinguish a basic learned readout, its free-output formatting, its allowed-choice ranking, and selection of the correct evidence. Test a selection/cropping tool against the actual source grammar rather than author answer keys. A successful crop supplies the right evidence externally; it does not prove the model learned to retrieve it. Frame, length, competing content and target binding can interact. Keep unresolved responses and all classes visible. These are optional diagnostic patterns with a narrow local example, not a universal parsing algorithm, mandatory pass threshold or default model-authority change.
