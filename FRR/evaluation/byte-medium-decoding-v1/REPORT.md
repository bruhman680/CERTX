# Decoder diagnostic: variation without exploration

17 November 2026, America/Chicago. Three predeclared one-shot branches from exactly the same saved changing-world initial messages, token IDs, model body and initial material. These branches preserve the turn38 reference, selected main1630 and both previous turn3 pilots. They do not continue or reset those histories.

## Result

The new greedy reply matched the earlier first changing-world reply **token-for-token**. Both sampled replies differed from it and from each other, but neither produced an executable cell or model-created artifact. All three reached the256-token generation ceiling. Each branch received one successful physical tick; the only resulting world entry remained field.bin.

| Branch | New calls | Decoder | Output pattern | Actor operations |
|---|---:|---|---|---:|
| Greedy replay | 1 | argmax | Same repeated world.bin prose as before | 0 |
| Sample17 | 1 | temperature0.8, top_p0.95, seed17 | Paraphrases laws, with an incorrect executable-cell delimiter | 0 |
| Sample29 | 1 | same sampling policy, seed29 | Partial observation-like JSON followed by a long zero run | 0 |

The greedy text's dominant exact sentence occurred13 times. Sample17 had no repeated complete sentence under the recorded splitter, but included the false claim that a column-zero line exactly `http://example.org` opens an executable cell. That is generated prose, not the actual law. No URL was visited, no parser rule changed and no text was repaired into an action. Its response also introduced a supposed workaround although no such task was supplied.

Sample29 emitted an unfinished JSON-like prefix and a223-character run of zeros. The actual initial material's hex representation has a122-character run of zeros after its leading01. The sampled reply was not an exact packet copy and did not constitute valid complete JSON. It ended at the declared token ceiling. One sentence segment in this output is not evidence of low repetition: the exact-sentence descriptor misses repetition inside a long numeric string. EXTRA_DESCRIPTORS.json records this limitation with character-run counts.

This is useful negative evidence against treating sampling as an automatic route to exploration. It also shows that the particular greedy text sequence is not inevitable under every decoder. It does not establish improved reasoning, learning, reliable action, a population-level repetition rate or a preferred long-term sampling policy. Only two sampled seeds were tested, one draw each, chosen before seeing outputs.

## Prospective setup

PROTOCOL.md, sampling.py and run.py were frozen in CONTRACT.json before generation. The three conditions were greedy, then private CPU generator seeds17 and29. Sampled selection used temperature0.8 and a nucleus containing at least0.95 probability mass, retaining the threshold-crossing token, then renormalized multinomial sampling. There were no repetition penalties, semantic scores, rewards, best-of selection, coaching, prompt changes or output-dependent replacement calls.

The cached pretrained SmolLM2-135M-Instruct body used float32/eager/two CPU threads, fresh attention cache per call and a maximum256 generated tokens. The original pinned greedy generator was used for greedy replay. Sampling changed token selection while retaining its forward-pass loop. Every branch used1129 initial tokens, identical native-role messages and identical world bytes and observations. No post-action feedback was used in another model call in this diagnostic. Each generated reply was then executed literally through the unchanged adapter, followed by its one physical tick.

The model was loaded offline from the existing cache; no paid model endpoint, model download or training procedure was used. Parameter digests were checked before inference, after each branch and at completion. Weights stayed fixed under those checks. The policy comparison therefore concerns output decoding, not weight adaptation.

## Verification

Five preflight sampler checks passed: inclusion/renormalization at the nucleus threshold, retaining only a dominant token when it supplies enough mass, full mass at top_p1, reproducibility with identical private seeds, and refusal of nonfinite logits without repair. These are mechanism checks, not model competence tests.

The external audit verifies exact initial messages and token IDs across all three branches; raw output decoding, stopping boundaries and saved policies; literal parsing; actual actor batches, physical tick sources and committed snapshots; observations and operation counters; inherited bundle/event/receipt chains; implementation pins; clean paused state and absence of live pending actions/locks. The greedy token comparison against the prior saved first reply passes. Sampler execution was not rerun token-by-token with the model during the audit; policy and seed provenance are supported by the pinned implementation and raw records, not an independent stochastic replication.

All1040 protected files stayed unchanged: the original943 reference/main/pointer files plus97 files of the prior model-pilot study. No inference or action occurred in any protected garden. All new branches are cleanly paused at one reply, with full initial context, raw token output and actual effects retained. No background inference remains. RESULTS.json reports pass.

## Confidence and next strongest question

High confidence: exact greedy replay in this environment, decoder-sensitive text variation for the two named seeds, zero executable actions, unchanged protected histories and successful world-only physical ticks.

Unestablished: learning, self-directed exploration, a benefit from a different seed over time, or an inherent inability of this body to use its actuator. The earlier observation of file execution under a different prompt remains evidence of conditional capability; this diagnostic does not erase it or show that this free-world context elicits it.

The strongest next targeted uncertainty is **observation presentation**. The model is reusing either law prose or a repetitive serialized byte representation. That association suggests a hypothesis, not a proven cause. A separate prospective comparison could hold material, physics, body, FRR and decoder fixed while presenting the same bytes as raw hex versus a lossless compact run-length representation. This would test input-format sensitivity without prescribing what to do or changing the material's laws. It must use declared fresh diagnostic branches and preserve these histories. A less repetitive or more varied response would still need to be distinguished from genuine world interaction.

No such presentation change, further model call or long continuous block is queued. Do not alter the existing greedy source, FRR, contracts or byte laws in place.

Garden translation: changing how the gardener chooses words changed its recitation, but it still did not work the soil. Before changing the soil again, we can investigate whether our way of displaying it invites copying.
