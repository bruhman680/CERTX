# Optional cache replay planner

Run from the FRR folder:

```bash
python tools/cache_replay_plan.py evaluation/cache-replay-tool-gap-v1/CLI_EXAMPLE.json
```

The JSON result reports reusable prefix length, cached tokens to discard, tokens to replay and invalidation reasons. The example reuses 24 tokens and processes one query token. Only a real backend can perform the truncation/replay. This CLI does not load model weights or tensors. It uses Python standard library only; the numerical experiment additionally uses NumPy.

Construct `cached.prefix_sha256` with `token_digest(cached.token_ids[:cached.cache_token_count])`. This is a consistency digest over canonical JSON integer IDs, not a cache-tensor hash or authentication. All execution identity values are nonempty strings. Explicit absence can be represented by `none`; unknown/unspecified/unavailable or missing values force recomputation. Model revision must name the entire effective forward-pass configuration: callers must not leave hidden adapters, preprocessing, masks or weight changes outside the identity contract. Equality of misleading caller declarations is not verified equality of execution.

Unsupported: cross-family transfer, sliding-window/evicted caches, hidden custom positional behavior, authenticated artifact storage and semantic truth checks. Token IDs must include every causally relevant serialized input for the declared model, with additional image/adapter identities where applicable. Backend batch/mask/position details need an actual integration audit. Changes outside this modeled contract are not certified safe.

If no new tokens need replay, this helper does not supply final logits; the backend must already have stored them or replay the last token after appropriate truncation. Empty-token requests and partially populated real cache objects also need caller handling. Consult [report](REPORT.md) and [scout](SCOUT.md) before treating this development helper as a backend guarantee.

Reproduce the experiment in a directory of your choice to avoid overwriting saved historical results:

```bash
python evaluation/cache-replay-tool-gap-v1/experiment.py > /tmp/cache-replay-results.json
```

`supplement.py` writes its authored CLI input and supplemental results in the study directory; copy the study before rerunning if preserving those exact artifacts. No pretrained model, SwaT translator, API account or GPU is used.
