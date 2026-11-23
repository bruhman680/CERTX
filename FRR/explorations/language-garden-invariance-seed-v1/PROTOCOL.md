# Endpoint comparison and a seed for invariance

The frozen SmolLM2-135M-Instruct language pilot supplies the native system message, base symbol seed, CPU runtime, greedy decoder and 256-token generation limit. Every call is a fresh opening with the same weights and zero feedback. The continuing garden is outside this batch.

## Endpoint diagnostic

Reuse the published equality question verbatim. Give the same eight fresh rows in two forms: labeled First/Last fields, or labeled First/Middle/Last fields. Each of two symbol pairs produces AA, AB, BA and BB using the same distractor within that pair. This crosses endpoint identity with the answer and balances Yes and No. The deletion changes prompt length and removes the Middle field as well as its value. The comparison therefore estimates the combined effect of the shorter display.

## Invariance seed

Use two small panels that ask whether a repetition relationship survived. The code panel uses label sequences. The story panel names the people performing three successive actions. Neither shares literal labels between the two sequences in a case. Every block crosses first and second patterns ABA and ABB, so the first and second presentations considered alone each leave the answer balanced. Each negative has a nearby positive with the same first sequence and just one changed position in the second. Two lexical blocks per rendering give 16 cases in total. No case supplies an example answer or states the seed's domain application.

Run each case in three conditions. The baseline is the original garden seed. The attention control adds a general invitation to deliberate. The invariance condition adds “When something changes, look for what stays the same.” Both additions have the same placement. Preflight records exact tokenizer lengths. This tests an inference-time prompt difference on these items and encodings. The two renderings use task-specific wording and different vocabulary, so their comparison measures bundled presentation differences. Calls are ordered with a fixed deterministic shuffle within each stage. The panel is written and pinned before either stage.

## Measurement

Primary scoring accepts a complete answer consisting of Yes or No, case-insensitively, after stripping outer whitespace. Count correct answers separately by gold label, and record invalid replies and stop reasons. Also show the number of complete matched pairs for endpoints, and the number of source-held-constant pairs in the seed panel for each condition. A correct pair requires both answers. Report casewise gains and losses when comparing conditions. The always-Yes and always-No baselines each score one half, with zero correct pairs. A seed that increases Yes replies without improving both gold classes may instead change response bias. A score gain limited to one panel or shared by the attention control does not strongly isolate the invariance sentence. Inspect long replies descriptively after scoring. The fixtures, scoring, model source, model assets and both preflight panels are pinned before model generation.
