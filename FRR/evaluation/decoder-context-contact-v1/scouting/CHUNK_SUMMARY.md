# Parent-executed continuation check

The scout prepared the implementation; the parent executed it after the sampling batch on 13 November 2026. This is additional local inference, separate from the earlier token-only scout phase.

After the exact first-turn prompt and 256 saved generated tokens, all 64 subsequent greedy tokens matched the retained uninterrupted run, in-memory cached continuation and fresh raw-token prefill. Cached versus fresh logits differed by at most 0.00005340576171875 and passed the declared atol/rtol 0.0001 comparison. The pending selected final prefix token was fed exactly once; cache length before it was 350 (95 prompt + 255 generated tokens). Active run inventory and model digest stayed unchanged.

This single-context result establishes the tested token-loop equivalence on the current CPU/runtime. No cache was serialized, no process restart resumed a cache, no sampling RNG state was restored, and no naturally emitted EOS was overridden. Retained plan/results/source/logs document these limits. The complete active garden still uses fresh KV per reply.
