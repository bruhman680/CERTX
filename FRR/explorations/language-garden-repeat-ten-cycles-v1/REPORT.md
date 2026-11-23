# Ten cycles on whether a repeat answer follows the row

23 November 2026, America/Chicago.

The initial repeat-versus-Last split reproduced on one new row where both questions were answered correctly. The behavior remained unreliable across words, digits and opaque labels. In the reserved panel, the model correctly named the repeat on 5/12 word rows. Choosing any one fixed position would have scored 8/12.

## Cycle results

These scores count recognizable correct content. None of the 64 replies used the requested bare answer form. Seven hit the 256-token cap. There were 57 distinct rendered user inputs because some exploratory fixtures repeated across or within cycles. Each call used a fresh context and the same pinned SmolLM2-135M-Instruct weights with greedy decoding.

| Cycle | Comparison | Correct content |
|---:|---|---:|
| 1 | Ask for Repeat and Last separately on the same four fresh rows where they differ | Repeat 2/4, Last 3/4, both correct on 1/4 |
| 2 | Replace opaque labels with digits in the early-repeat layout | 0/4 |
| 3 | Remove the broad garden preface from the same four digit prompts | 0/4, with all four replies identical to cycle 2 |
| 4 | Move the repeat through all three position pairs using opaque labels | 1/6 |
| 5 | Count each named symbol separately on three selected labeled rows | 1/6, with 0/3 rows having both counts correct |
| 6 | Flatten those same six count prompts to plain rows | 0/6 at the first assertion |
| 7 | Return to the repeat question with everyday words | 4/6 |
| 8 | Name the two equal fields in the question and ask for their shared value | 1/6 |
| 9 | Edit Last where the correct answer should stay fixed or change | 0/6, with 0/3 edit pairs correct on both sides |
| 10 | Test twelve reserved everyday-word rows, four of each shape | 5/12 |

## What moved with the input

In cycle 1, the model correctly answered `kef` for Repeat and `dov` for Last on the row `kef kef dov`. On `taz taz wip` it correctly named `taz` as the repeat and incorrectly gave the same answer for Last. So the two correct Repeat answers yielded one fully correct paired distinction. On `rud rud bem` it returned `bem` to both questions. The split observed in the previous study occurs again, with different failure patterns on nearby rows.

The reserved word panel preserved all three ways a symbol could appear twice. Correct content was 2/4 for AAB, 2/4 for ABA and 1/4 for ABB. Three replies named the other word and four named no word from the row. Each fixed positional rule, including copying Middle, scores 8/12 on these same fixtures. The model can give a fluent naming sentence whose answer stays put when the facts change. For example, it answered “Duck” on all three duck/goat rows, including `duck goat goat`. It likewise answered “Grove” on all three lake/grove rows and was correct on only the one where `grove` appeared twice.

## Boundaries on interpretation

The exploratory comparison of everyday words with opaque labels was 4/6 versus 1/6. Each of those panels had only four distinct prompts because the builder reused two rows within the panel. Cycle 8 inherited those duplicates. The reserved panel had twelve distinct prompts and kept every shape equally represented. The word result in cycle 7 tied each position-copy rule, and the reserved result fell below all three.

Cycle 6 illustrates the need to distinguish a usable answer from an answer found later in a loop. One capped reply echoed the row and then correctly said `rud` appeared twice. The frozen first-assertion measure did not count that reply. Even reading past the row echo, the paired `bem` reply incorrectly said it appeared twice too. That check does not support discriminating the two counts.

The frozen policy used labeled digits in cycle 9 after the field hint performed poorly. All six outputs named “the cross,” the same outside the row answer seen in cycles 2 and 3. That makes cycle 9 a weak test of sensitivity among recognizable symbol answers. It documents a uniform off-row response under these digit prompts. We kept the word “symbol” across the lexical conditions for comparability. Its interpretation may be part of the behavior, so the result does not establish inability to compare digits or words under another task wording.

The study did not meet its prespecified threshold for retrying the invariance cue. The preface-removal replay tests only the original garden preface on four digit fixtures. The model weights received no updates, and the continuing garden did not advance.

The next contact is a matched wording probe on the same everyday-word rows. Compare “Which word appears twice?” with the current “Which symbol appears twice?” Keep all three repetition shapes balanced and record out-of-row answers, both correct sides of minimal pairs, and the three fixed-position baselines. That probes grounding before introducing another abstract seed.

[Frozen decision rules](design.py) · [Protocol](PROTOCOL.md) · [Scores and paired comparisons](SUMMARY.json)

Every numbered directory has the pre-call prompt and predecessor score hashes, exact token traces, replies and results. Run `python run_cycles.py audit` in the pinned pilot environment and `python summarize_cycles.py audit` to reproduce the checks without inference.
