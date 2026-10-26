# Prospective key correction

The scorer wrote KEY.json and SCORING.md before any reader launched or any participant outcome was accessed. The independent reviewer then found a packet-relative explanation error in AS03. The scorer corrected KEY.json in place before freeze and launch. Current KEY.json is the final approved prospective key; action, retained-claim reuse, numerical warrant, and all other case keys were unchanged by this correction.

Exact original KEY.json bytes were **not retained**. The temporary generator was deleted before this correction request, and no KEY_INITIAL.json was saved. No reconstructed file is represented as an original byte artifact. The original statements and correction are documented from the saved scorer/reviewer messages and tool inputs:

* Original AS03 `remaining_issue` for every pair was: `Calibration uncertainty remains; L-R has no acquisition and supplies no comparison.` This disclosed L-R's failure even in L-A + L-D, where L-R was not requested. For L-A + L-R it could imply knowledge of primary calibration details absent from that packet.
* Original AS03 `next_check` for every pair was: `Acquire a valid full-series reference or establish a certified correction/error envelope for L0.` In L-A + L-R, the internal measurement name L0 had not been delivered.
* Corrected `remaining_issue` is conditional on requested records: with D, identify L0's lack of a present-session offset/error bound; without D, state that no delivered record establishes a valid error contract and briefing acquisition/calibration details remain unknown. With R, state its reported recorder failure; without R, explicitly leave the reference's contents and availability unknown.
* Corrected `next_check` requests a valid full-series bounded reference or certified correction/error envelope, naming L0 only when D was delivered and otherwise referring to the underlying briefing measurement(s).

The correction removes leaked facts from packet-relative expected explanations. All three AS03 actions remain UNRESOLVED; the actual displayed nominal maximum and external truth were unchanged. The scorer inspected the other pair explanations for the same access error and found none. Reviewer approved the remainder of KEY.json and SCORING.md. This correction was prospective and was not prompted by reader behavior.
