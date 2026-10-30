# Distributed weighing stations — user's open design idea

The user suggested many distributed weighing stations relaying to a main station. This is recorded as a useful architecture question, not a tested result. Our current two optional tools are local task-specific checkers; they do not constitute a deployed distributed verification system.

A relay would need to preserve the station's question, recipe/version, source hashes, input roles, assumptions, cohort, unresolved cases and result. A main station should check compatibility and shared source ancestry before combining reports. Ten reports copied from one observation are not ten independent observations. Contradictions can indicate incompatible questions, scopes or assumptions rather than a fact to resolve by voting.

Possible later experiment: pass several receipts for the same underlying artifact through an aggregator, including duplicate ancestry and different parser/cohort policies. Expected behavior would be to retain distinct scopes and flag incompatibilities, not invent a single confidence score. This remains a later direction; no aggregator or new confidence policy was installed in this run.
