# PG-C1 Amendment 01: exact-contract reuse after peer review

Initial helper/protocol were frozen at6f4401c4 before execution. The saved-data audit and eleven initial helper checks completed successfully. All original outputs, including extracted residuals, were committed atbb6b3345 before repair. No participant study or new sensor experiment was run.

Read-only peer review found an uncovered reuse case: compare() used Python .get() equality for field differences. Adding expected_value:null to a sensor contract could leave changed_dimensions empty even though canonical contract hashes differ. It then suggested reuse of a receipt not bound to the exact proposed contract. The field is irrelevant to the sensor adapter, so this does not demonstrate a false scientific verdict, but it violates the helper's exact-contract reuse promise. Numeric metadata1 versus boolean true is a related equality edge case.

Repair: direct receipt reuse now requires equal canonical contract hashes. If recorded-field comparison finds no difference but hashes differ, classify an unclassified contract difference and require review/new binding. Keep the original receipt/assessment intact; semantic equivalence is not inferred.

Freeze repaired helper, new repair driver and this note before expanded checks. Replay the original eleven behavior cases in a temporary copy so preserved evidence is untouched; add absent/null and1/true controls; exercise the CLI; verify every initial output hash. The original launch manifest now intentionally differs only at helper source. Old unchanged-at-run results remain historical, not a claim that old source hashes match the repair. No retuning or rerun of the sensor audit.
