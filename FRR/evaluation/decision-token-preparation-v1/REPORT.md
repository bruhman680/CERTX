# Decision-token controls prepared; garden settled

30 October2026. User requested the strongest next step within near-limit usage, preservation and wind-down. This contact performed tokenizer, mapping and exact-rational objective checks; no model inference, optimizer update or learning-efficacy experiment occurred. No new agents, paid services or installations.

[CONTROL_CHECKS.json](CONTROL_CHECKS.json) confirms A/B/C each encode as one token (IDs49/50/51), roundtrip to the literal label, and three cyclic mappings place each semantic class at each alias exactly once. This controls a fixed alias preference across mappings; it does not eliminate all vocabulary/interface confounds.

The proposed first experiment keeps current semantic labels and source prompts fixed across two fresh adapter branches. Compare the prior mean-over-target-tokens objective with:

    L = mean_over_three_examples [0.5*CE(first decision token)
                                  +0.5*meanCE(remaining label tokens and EOS)]

YES/NO/WITHHOLD have target lengths includingEOS of3/2/5. Old first-token coefficients per balanced update are1/9,1/6,1/15. New coefficients are1/6for each class, with equal total sequence weight. Exact fraction checks verify normalization, both implementations of the proposed formula on21explicit loss-vector examples, and identity of the two objectives for a one-token alias plusEOS. These are algebraic checks, not21model experiments.

The intervention deliberately reallocates suffix/decision loss; it does not isolate every mechanism associated with token length. Any future improvement needs per-class, completion and full-denominator analysis. The earlier missing-class failure remains unexplained. Alias mappings are a subsequent interface control, not a silent rescoring of existing outputs. No forced-choice metric is relabeled as ordinary generation.

[Protocol](PROTOCOL.md), [24new primary cases](NEW_PRIMARY_CASES.json), [keys](NEW_PRIMARY_KEYS.json), [source bindings](SOURCE_BINDINGS.json), checker and results are frozen in [FREEZE.json](FREEZE.json). Cases cover two new formats (XML scoped records and sectioned bullets), with8positive/8zero/8missing keys; target/distractor settings are counterbalanced. They have had no model forward pass. Keys are coordinator-authored typed-oracle data, not independent gold review. Previous72train/12dev sources remain bound and unchanged; old48testcases are exposed regressions. The new loss training runner is not implemented or started in this preparation contact.

[PRESERVATION.json](PRESERVATION.json) verifies628existing model/checkpoint/optimizer/cache files against previously recorded hashes, including the original model, earlier partial full-weight checkpoint, all older states, LoRA probe/initial/final adapters and120latest caches. Everything remains in place. Local binaries remain subject to workspace retention; Git records code/data/token metadata/hashes rather than large model binaries.

Latest actual learning result remains [LoRA pilot](../lora-state-pilot-v1/REPORT.md):48balancedupdates,19/48structuraltest,16/48constantbaseline,missing0/16. Original/frozenbaseunchanged,no defaultpromotion. [Registry](../station-registry-v1/README.md) remains read-only and scope-preserving; no global truth/confidence score.

The next session can implement the frozen phaseA objective comparison after resource preflight. If the protocol/data need changing, preserve this preparation and record the revision before training. No work continues in background. Earlier failures, tools, core/schema, broadqueue and source-reading gate remain unchanged.
