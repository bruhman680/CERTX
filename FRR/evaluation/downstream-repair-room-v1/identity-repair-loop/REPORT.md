# One later repair, with the mistake retained

31 October 2026 UTC. Outcome-informed follow-up to the completed downstream study.

All 48 wrong-target model handoffs reached a later identity receipt. The receipt triggered one bounded repair: reopen the original source, select its target, and read that record with the actual mistaken answer still in the prompt. Result: **48/48 final labels and source receipts pass**. It repaired 36 wrong labels and retained 12 labels that had matched despite the earlier identity mistake.

The trigger checks record identity, not answer accuracy. Original outputs, failure receipts and parent IDs remain in the main study; repairs append a new branch. The selector is a small explicit parser, and the same saved model is used without training. This is tool-mediated recovery, not model-initiated search, error awareness or a universal verification layer.

All 48 input prompts already occurred among the main study’s readouts; they contain only 24 distinct prompts. These 48 executions demonstrate the controller operating on the actual earlier handoffs. They do not add an independent capability replication or fresh primary sample. The closed toy grammar is solvable by the parser alone.

[Protocol](PROTOCOL.md), [inputs](INPUTS.json), [freeze](FREEZE.json), [raw](run/RAW.jsonl), [appended receipts](run/RECEIPTS.jsonl), [summary](run/SUMMARY.json), [checks](CHECKS.json), [overall report](../REPORT.md). No new model state, external service, install, download or default promotion. Fresh-environment restoration, unrestricted source truth and independent replication remain outside scope.
