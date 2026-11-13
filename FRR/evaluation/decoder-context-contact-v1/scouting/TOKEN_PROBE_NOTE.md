# Rejected token-equivalence assumption

The first token-only script version asserted that `continue_final_message` would reproduce raw IDs for both selected retained replies. Its first run raised `AssertionError` for turn 1. No model weights or canonical state were touched.

Inspection showed a boundary tokenization difference: original generation ends `[198,198]`, whereas the decoded/retemplated text ends `[1116]`. Turn 12 does match. The script was corrected to report the boolean comparison, first differing offset and both tails rather than treating an unsupported equivalence as a required invariant. This is a diagnostic correction, not a model or world repair. The successful corrected run is saved in `TEMPLATE_RESULTS.json`.
