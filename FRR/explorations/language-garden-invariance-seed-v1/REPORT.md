# Endpoint comparison and a seed for invariance

The small model failed to distinguish matching from nonmatching cases in both probes. Removing the middle field left every endpoint answer unchanged. The broader seed made story answers shorter and more compliant on this panel. It did not change whether the model called a relationship the same.

On 22 November 2026, America/Chicago, we began 64 detached calls with a cached SmolLM2-135M-Instruct checkpoint, the pinned native chat template, fixed weights, and greedy generation. There were 16 endpoint calls and 48 repetition-pattern calls. All stopped at EOS. Every fresh opening had one response and no feedback. The persistent garden was outside the study.

## Direct endpoint comparison

The same eight new items appeared with and without a labeled middle field. Both layouts generated the exact word “Yes” on every item. Each got all four true matches and missed all four nonmatches. All eight paired replies were byte-identical across layouts. For example, with just two fields the model said Yes to both `First: lu / Last: lu` and `First: lu / Last: ne`. Removing the middle field also shortened each prompt by four tokens. In these items, that change was insufficient to overcome the all-Yes behavior.

## Broad seed comparison

The model read pairs with the same positional pattern, such as `zi po zi` and `fa re fa`, and near misses, such as changing the second sequence to `fa re re`. A story rendering asked the parallel question about who waved in a three-event round. Each rendering had eight balanced items and three conditions. The attention sentence “When you read a question, take time to think.” matched the placement and tokenizer length of the invariance sentence “When something changes, look for what stays the same.” Both added 13 tokens per item compared with the existing garden seed alone.

| Presentation | Existing seed | Attention control | Invariance seed |
|---|---:|---:|---:|
| Code sequences, exact and correct | 0/8 | 0/8 | 0/8 |
| Short stories, exact and correct | 3/8 | 3/8 | 4/8 |
| Changed patterns correctly called different, both presentations | 0/8 | 0/8 | 0/8 |
| Correctly answered both cases in a matched pair, both presentations | 0/8 | 0/8 | 0/8 |

All 24 code replies broke the requested one-word format. Reading the replies for meaning, every one of the 48 judgments affirmed sameness, for 8/16 correct in each condition. The single strict-score gain over each control came from the invariance sentence turning an affirmative story explanation into a one-word answer on a different true match in each comparison. The new seed also turned a wrong affirmative explanation into a one-word Yes on one near miss per control. The exact-format gains make no casewise gains in the underlying binary judgments.

Some replies used concrete vocabulary from the prompt while giving reasoning unsupported by it. The baseline produced the same Fibonacci explanation after echoing two versions of one item, even though the first preserved the relationship and the second changed it. The invariance condition gave an identical explanation for three code cases after echoing their distinct rows, including both a true match and a near miss.

## Limits and next useful distinction

This was a controlled prompting experiment with one checkpoint, one greedy decoding setup and two small renderings. The gold answer compares which positions are equal. The phrase “same repetition pattern” leaves room to focus on the number of repeats, which was constant here. That ambiguity is a limit of the repetition questions. The simpler endpoint question independently showed the affirmative bias. The measurements describe observable replies. They do not establish what information was encoded internally or whether a differently phrased or learned seed could work.

The next diagnostic would ask the model to name which positions repeat in one sequence, with both positional patterns and counterbalanced options, before asking it to compare patterns across sequences. That would supply a label that has to change with the data and would avoid the Yes/No format in this batch.

[Protocol](PROTOCOL.md) · [Endpoint scores](ENDPOINT_RESULTS.json) · [Seed scores](SEED_RESULTS.json) · [Content review](CONTENT_REVIEW.json)

The opening contract pins the cases, scheduling, scoring and source references. Each archived trace contains the exact prompt, tokens, response and parameter receipt. From a workspace with the pinned pilot runtime and weights, run `python audit_archive.py` to check the archive and recompute the scores without making inference calls.
