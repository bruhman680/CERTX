# One-word replay of the reserved repetition panel

23 November 2026, America/Chicago.

Changing “Which symbol appears twice?” to “Which word appears twice?” changed the replies on the same twelve labeled rows. The frozen scorer went from 5/12 to 6/12. A direct reading of the answers found 5/12 versus 2/12 because the scorer credited some replies that only talked about a word's symbol. The apparent gain depends on how a reply is scored.

The only text edit was in the question. The response instruction still said “Reply with the symbol only.” All twelve pairs had the same token count. The native template, preface, weights, decoding and generation limit matched the original run. All twelve new generations reached EOS. All answers in both arms missed the bare-answer format.

| Measure | “Which symbol” | “Which word” |
|---|---:|---:|
| Frozen scorer, correct named in-row item | 5/12 | 6/12 |
| Review, directly named the correct repeated item | 5/12 | 2/12 |
| Pairs with both sides correct when the gold answer switches | 0/8 | 1/8 |
| Bare correct answers | 0/12 | 0/12 |

The eight switching pairs share cases within lexical families. The one passing pair in the word arm was `cloud rock cloud` and `cloud rock rock`. The model named `cloud` then `rock`. A copy-Last rule also passes that pair. On `cloud cloud rock`, the word arm incorrectly named `rock`, where the symbol arm correctly named `cloud`. Copying any fixed position scores 8/12 over the whole panel.

## Why the scores differ

The frozen scorer extracts a recognizable candidate from a simple first assertion. It credited “The symbol for ‘duck’ is ‘d’” as `duck` in all three duck/goat rows. That reply defines an initial. Across all three lake/grove rows, the model said “The symbol for the word ‘lake’ appears twice in this row.” That claim mentions `lake` but describes the repetition of a symbol it never identifies. It produced two frozen-score gains and one loss without naming a concrete repeated word in any of those three replies. The direct-answer review records these judgments separately from the frozen scores.

The word condition also replaced all four “the cross” answers. Three were now the letter “P” for the thread/paper family. The fourth became the correct explicit `rock` response. A change in what the model talks about can coincide with little change in whether the answer tracks the row.

## Next comparison

Cross the task noun and answer instruction in a small matched panel. Use either “Which word” or “Which symbol,” with either “Reply with the word only” or “Reply with the symbol only.” Freeze a direct-answer scorer before the runs, with a check for initials and references to unnamed symbols. Hold the three repetition patterns and the lexical families constant across the four arms. That can distinguish a question-wording effect from an interaction with the response instruction. This replay used one panel, one decoder, and one checkpoint.

[Protocol](PROTOCOL.md) · [Frozen scores and paired results](RESULTS.json) · [Direct-answer review](CONTENT_REVIEW.json)

The exact new prompts, responses and token IDs are archived beside the original trace pins. Run `python run_word_probe.py audit` from the pinned pilot environment to recompute the frozen comparison without inference.
