# Sampling support on the repeated input

Planned13 November2026; completed/reviewed14 November2026, America/Chicago. One exact2231-token input, temperature0.8, paired seeds27401–27403, top-p0.9 versus1.0. Greedy reference is the previously retained identical input/output. Six actual replies, no model training or main adoption.

At top-p0.9, all three outputs exactly match the old256-token unfinished text. At top-p1.0, there are three distinct texts: one old repeat and two variants. One variant ends naturally at251 tokens; the others hit256. No output has a complete executable cell, so all six only append writing in their separate copied worlds. Variation is observed; improved action or correctness is not.

The additional teacher-forced analysis recomputes probabilities along the saved greedy256-token path. All argmax tokens match the reference. At temperature0.8/top-p0.9,255 positions retain only one choice and one position retains two. This explains why seed changes have little opportunity to alter this particular path. It does not make that sampler wholly deterministic: the two-choice position can vary, and other sampled paths may have different support.

This is a parallel-prefill diagnostic, not an exact trace of every incremental sampling distribution. Numerical ordering differs slightly from the sampler, and cutoff decisions can be sensitive near boundaries. No conclusion about every prefix or full distribution entropy follows. The profile, all raw outputs and settings are retained.

Three paired seeds on one chosen context are descriptive evidence, not a population ranking of decoders. Increasing top-p introduced text variation here without producing a working cell. No repetition penalty, forced fence closure, minimum length or novelty instruction was added, and no setting was adopted in the main garden.
