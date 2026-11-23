# Three cycles on symbol position and equality

22 November 2026, America/Chicago. Twelve fresh calls used the same native system message, symbol exploration seed, fixed SmolLM2-135M-Instruct weights, greedy decoder and 256-token cap. Each four-call comparison was pinned before it ran. Each later cycle was chosen after reading the preceding replies. The model had no access to those replies or scores.

| Cycle | Question and display | Correct content | Correct in requested format | Stop causes |
|---|---|---:|---:|---|
| 1 | Name the last symbol, plain row | 0/4 | 0/4 | 4 EOS |
| 2 | Name the last symbol, labeled positions | 4/4 | 0/4 | 4 EOS |
| 3 | Do the endpoints match, labeled positions | 1/4 | 1/4 | 2 EOS, 2 caps |
| Preserved reference | Do the endpoints match, plain row | 2/4 | 2/4 | 4 EOS |

Cycle 1 gave the same full sentence naming “K” on both familiar rows, and the same sentence with asterisks on both other rows. Cycle 2 named the final symbols correctly in all four cases, in the order ka, su, zo, ve. Every answer used a full sentence despite the symbol-only request. The display explicitly supplied a Last field, so the content gain demonstrates readout with that support.

Cycle 3 restored the original yes-or-no question byte-for-byte. The first two replies both called ka and mi the endpoints, substituting the middle symbol for the final one in their opening claims. Both continued to the cap without an explicit yes or no. The remaining two returned Yes, including on the near miss ve tu zo. The earlier unlabeled comparison answered Yes to all four. Each layout failed to distinguish at least one matched row from its near miss. The difference in exact scores describes these four reused rows and one response per condition.

The position labels, line breaks and input length changed together. Labeled readout shows that a direct question can retrieve the exposed value in this setup. It does not establish how the model represented the unlabeled row, and the equality question elicited a different output. No feedback, weight updates or held-out rows entered these comparisons.

If continuing this diagnostic, the next comparison could present only the two endpoint values on matching and nonmatching examples and use the same equality question. This would remove the need to locate the endpoints among three positions. Keep the existing garden's open expression separate from this test.

The stage RESULTS.json files contain the strict scores. CONTENT_REVIEW.json contains the judgments on longer replies. Each case preserves its prompt and token IDs, full response, stop reason and parameter verification.
