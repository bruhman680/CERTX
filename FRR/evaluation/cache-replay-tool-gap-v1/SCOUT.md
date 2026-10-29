# Tool scout: what can be used, rebuilt, or still needs another runtime

Client 28 October 2026 America/Chicago; host 29 October UTC. The cloud runtime skill was read; environment_status reported current connected/running observations and an enforced unrestricted HTTP policy, with no configured secrets or outbound identities. Executor policy has vpn_configured=false. These observations describe readiness, not universal endpoint authorization.

A non-secret package probe found NumPy present; torch, transformers, safetensors and huggingface_hub absent. nvidia-smi was not on PATH. This is not a comprehensive GPU or model-weight inventory. No packages, weights, data or containers were installed/launched. Public browsing/GitHub reads worked. No service API keys were requested because no paid/model API execution was needed.

## Primary-source contacts

Pinned [SwaT requirements](https://github.com/Ar-Kareem/SwaT/blob/ae2de2285caf82f4d500526bf6e6992747b98eea/requirements.txt), [experiment 1 config](https://github.com/Ar-Kareem/SwaT/blob/ae2de2285caf82f4d500526bf6e6992747b98eea/scripts/exp1/config.json) and [experiment 2 config](https://github.com/Ar-Kareem/SwaT/blob/ae2de2285caf82f4d500526bf6e6992747b98eea/scripts/exp2/config.json). Requirements name PyTorch 2.6.0 and Transformers 5.2.0. Default training config places sender and receiver on separate CUDA devices; the communication config requires a trained renderer and query-transfer stages. Its summary/receiver backend selects vLLM, but the inspected top-level requirements do not list vLLM. This is an unresolved setup-dependency question, not a demonstrated import failure: runner installation logic was not read. The default pair and uniform head budget do not automatically reproduce the headline comparison. Full config files read; runner/backend code and original result logs not audited. See [manifest](SCOUT_MANIFEST.json).

[Transformers v5.3.0 cache documentation](https://huggingface.co/docs/transformers/v5.3.0/en/cache_explanation) explains that reuse must preserve past/current attention-mask dimensions and correct absolute cache positions. Cache-layer types have different update/storage behavior. This source is conceptual guidance; the inspected SwaT dependency is a different version, so compatibility has not been established.

[vLLM v0.21.0 prefix-caching design](https://docs.vllm.ai/en/v0.21.0/design/prefix_caching/) keys reuse on prefix history and tokens, with additional adapter, multimodal and isolation identity. Its full-block policy and hash serialization also matter. This is an existing engineering lineage, not a newly discovered optimization. We have not installed or tested vLLM.

## Gap-to-action map

| Gap | Useful action now | Remaining boundary |
|---|---|---|
| No session KV read/write interface in the present chat tools | Keep host-chat limitations explicit; save external experiment artifacts | Cannot retrofit this chat thread with a latent channel |
| No torch/transformers installed | NumPy full-attention reference backend for cache arithmetic | No pretrained language behavior, kernel or library integration |
| Reuse decisions need explicit origin/configuration | New optional metadata replay planner plus CLI example | Caller assertions do not authenticate tensor contents |
| Source correction can change the cached suffix | Compare prefix-truncate-and-replay with full recomputation | Numeric equality is not semantic understanding |
| Real SwaT needs pair-specific weights, dependencies and evaluation conditions | Save pinned manifest and staged reproduction plan | No translation model, cross-family test or benchmark result here |
| Unknown visual-context effects | Parallel [heart-image scout](HEART_SCOUT.md) | Source report only; exact materials and model execution still needed |

## Staged path, proposed only

First integrate the planner with one pinned pretrained causal model in an isolated CPU-capable environment. Implement actual cache cropping/position handling and compare cached/rebuilt logits before testing answers. Bind the artifact to its manifest rather than trusting names. Include same-prefix/new-model and same-token/new-image cases. Select a small openly accessible model; model quality and access conditions must be checked at that time.

Then run corrections/negation/median-versus-maximum/unknown tasks with fixed gold labels. Full-history, summary, retrieval and cached-continuation conditions must disclose their different information budgets. Do not equate returning the same logits with retaining every historical fact.

Only then attempt cross-family transfer, with actual compatible mapper weights or training resources, tokenizer alignment and total cost accounting. Confirm vLLM/compaction setup and exact paper-pair/budget correspondence rather than assuming the default config matches a published table. This scaffold reduces preparation uncertainty; it does not close the resource or validation gaps.
