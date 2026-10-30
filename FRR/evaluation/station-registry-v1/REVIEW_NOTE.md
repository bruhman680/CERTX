# Coordinator review correction

30 October 2026. Coordinator review found two receipt-shape validation gaps: audit label-count dictionary equality allowed bool/float values numerically equal to integer row counts; source field states could swap known/observed roles. No current demo input uses either invalid form, so existing four scoped outcomes are expected to remain unchanged.

Before edits, thirteen original files were copied byte-for-byte to `before_review/`, including tool, freeze, receipt, checks, tests and output, protocol, manifest, preparation/check scripts, guide and report. `before_review/ARCHIVE.json` inventories original byte hashes. Original source receipts and ancestry artifacts remain unchanged.

The corrected tool requires exact nonnegative integer label-count values and exact role states: `soil_count.state=known`, `per_soil_observations.state=observed`. Regression tests cover bool/float/negative/string label counts against a valid one-row control and either/both swapped source roles. These are structural checks; source truth and assumptions remain external.

Revised protocol/tool/tests/manifest and archive inventory are frozen before fourteen-test rerun and corrected demo. Post-demo checks verify both the revised freeze and every archived file, and require unchanged four scoped results and shared-ancestry warnings. This is coordinator review refinement of subagent-built work, not independent replication or masked review.
