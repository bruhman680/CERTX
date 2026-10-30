# Post-result objective/readout observation

This note was written after scoring. It is a candidate mechanism and next experimental direction, not a preregistered explanation or a change to the frozen results. No new model forward pass or training update was performed for this note.

The pinned tokenizer represents YES with2tokens, NO with1, and WITHHOLD with4. Including EOS, supervised target lengths are3,2,5 respectively; see LABEL_TOKENIZATION.json. All fit the8token generation cap, so the cap does not mechanically exclude WITHHOLD.

The implemented balanced-update objective is:

    L = (1/3) * sum_over_classes [ (1/T_class) * sum_over_target_tokens CE(token) ]

Each completed update has one example perclass and equal total per-sequence weight. However, the coefficient of the *first decision-token* CE term differs: YES1/9, NO1/6, WITHHOLD1/15. Thus equal example counts and per-example normalization do not give equal weight to the first output decision. Later missing-label suffixes and EOS can be predicted under teacher forcing even if the first generated token remains wrong. A low average token loss therefore need not mean the three-class decision is learned.

This algebra is exact for the declared loss, but it does not prove the zero missing-class recall was caused by token length. Source parsing, representation, learning rate, dataset structure, insufficient optimization and vocabulary priors remain alternatives. It also does not establish that summing rather than averaging losses would fix the task; that changes other weights.

Strong next controlled contact: compare an explicitly declared single-token class interface with the current multi-token labels under a new protocol, counterbalancing label mappings so a preferred token is not confused with a semantic class. Freeze new primary cases; the current48 are now regressions. Preserve ordinary text-generation scoring separately from any forced-choice or likelihood diagnostic. No silent relabeling/rescoring/default promotion is made here.
