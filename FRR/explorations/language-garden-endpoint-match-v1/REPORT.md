# Direct comparison of first and last symbols

22 November 2026, America/Chicago. Four detached calls asked the same question about one row at a time. Each pair changed only the final symbol. All four prompts had 72 input tokens with the same native framing, seed, pinned model, and greedy decoder.

| Row | Expected | Actual |
|---|---|---|
| `ka mi ka` | Yes | Yes. |
| `ka mi su` | No | Yes |
| `ve tu zo` | No | Yes |
| `ve tu ve` | Yes | Yes |

All responses met the requested answer format and reached EOS after two or three tokens including EOS. Two of four were correct, equal to the always-yes baseline. Neither near miss changed the answer. Fresh labels and reversed ordering of the two cases in the second pair also left the answer label unchanged. The test did not demonstrate endpoint discrimination under this prompt, and its null result occurred within finished replies. The prior open-ended structural probe had a different failure mode and reached its cap while counting.

The balanced set catches an invariant answer in this trial. Four cases do not diagnose why the model says yes. For a bounded follow-up, present the two endpoints directly and ask which symbol appears last, using the same row pairs. This checks position readout with an answer that varies and then makes it possible to compare readout with equality judgments. Keep such a check in a detached record before further transfer claims.

Each exact input, reply, generated token sequence, stop reason, and parameter verification receipt is archived. Each case used its single opportunity and is paused. Scoring follows the frozen protocol. RESULTS.json retains each outcome.
