# Cache-to-Cache refresh — 1 November 2026 session

Accessed 2 November 2026 UTC; user session date 1 November America/Chicago. Static primary-source review only. No training, inference, installation, paid API, or FRR modification.

## Result and actual delta

The screenshot identifies the same **Cache-to-Cache: Direct Semantic Communication Between Large Language Models**, Tianyu Fu et al., already contacted locally on 27 October. [arXiv identity/history](https://arxiv.org/abs/2510.03215) still identifies v2, revised 2 March 2026; no newer arXiv revision was listed at access.

The current default-branch head returned by GitHub is [5eac72b90faf7b3dc2638e874fe7cba1e74c8bcf](https://github.com/thu-nics/C2C/commit/5eac72b90faf7b3dc2638e874fe7cba1e74c8bcf), dated 28 October 2026. Its parent is the prior contact's `bdb932aa63637959074a9a6fd59992a4d0d9ad22`. [GitHub comparison](https://github.com/thu-nics/C2C/compare/bdb932aa63637959074a9a6fd59992a4d0d9ad22...5eac72b90faf7b3dc2638e874fe7cba1e74c8bcf) reports one commit ahead, zero behind, and **README.md as the only changed file** (15 additions, 6 deletions).

The substantive new line replaces a future release notice with an announcement linking the separate [thu-nics/AKV](https://github.com/thu-nics/AKV) repository, described by the authors as their cache-engineering-for-agents follow-up. The remaining changes add its related-project card and adjust layout. GitHub metadata confirms that AKV exists as a public repository; a subsequent authorized bounded implementation inspection appears below. This is a new research lead, not a new C2C runtime feature or an established capability to adopt.

## Compact paper verification

[Paper v2](https://arxiv.org/html/2510.03215v2), §§3.3–4.3 and A.3: trained residual KV fusers combine source and receiver caches, with input-dependent weighting and layer gates. Both LLMs stay frozen; the fuser uses receiver next-token supervision. Main training uses 500k OpenHermes examples. Token and terminal-layer alignment support selected cross-family pairs, including Qwen/Llama/Gemma, rather than arbitrary untrained interoperability.

The abstract reports 6.4–14.2% higher average accuracy than individuals, 3.1–5.4% over text communication, and 2.5× average latency speedup. These are author-reported headline aggregates. Table 4's text-baseline improvements are 5.36, 4.15 and 3.06 accuracy points averaged by sharer; reported speedups are 3.46×, 1.51× and 14.41×. Timing uses one A100, batch one. Text communication is analyze-then-respond; cache communication skips intermediate decoding. Table 3 gives 1596ms versus 445ms, including 90ms fusion. I did not recover an explicit aggregation recipe mapping every table to the abstract's ranges/2.5×; no pooled estimate is asserted. A.3.5 says linear temperature annealing; A.4.6 records harmful wrong-answer transfer.

## Code and configuration verification

The [current pinned README](https://github.com/thu-nics/C2C/blob/5eac72b90faf7b3dc2638e874fe7cba1e74c8bcf/README.md) still headlines **8.5–10.5%, 3.0–5.0%, 2.0×**, unlike paper v2. Keep these source/version-specific; they are not an additional replication or an uncertainty range around v2.

Read the [pinned C2CProjector implementation](https://github.com/thu-nics/C2C/blob/5eac72b90faf7b3dc2638e874fe7cba1e74c8bcf/rosetta/model/projector.py#L862): separate key/value paths concatenate source and target, compute projected features and input-dependent weights, then add gated weighted projections to the target tensors. Its temperature update uses exponential interpolation. The previous report's linear-versus-exponential discrepancy therefore remains present in this inspected code; it was not repaired by the new README commit. This is a static formula comparison, not proof of which schedule produced published checkpoints.

The [pinned example training recipe](https://github.com/thu-nics/C2C/blob/5eac72b90faf7b3dc2638e874fe7cba1e74c8bcf/recipe/train_recipe/C2C_0.6%2B0.5.json) names Qwen3-0.6B receiver, Qwen2.5-0.5B-Instruct teacher, three-layer C2CProjector, last-aligned mapping, frozen teacher/base, 500k samples, 2048 sequence length, seed 42, eight CUDA processes. It is a configuration example, not an execution receipt. No wrapper, checkpoint bytes, or training run was authenticated.

## Overlap with existing FRR records

Read these first:

- `/workspace/frr/evaluation/cache-transfer-join-contact-v1/SOURCE_CONTACT.md`
- `/workspace/frr/evaluation/cache-transfer-join-contact-v1/REPORT.md`
- `/workspace/frr/evaluation/cache-replay-tool-gap-v1/REPORT.md`

The earlier source contact already records the same v2 paper, trained cache fusers, alignment/gating, OpenHermes training, enrichment-oracle cost boundary, wrong-answer transfer, preliminary multi-model extensions, and the temperature-schedule difference. The refresh adds current source-version confirmation and the precise documentation-only Git delta. It does not invalidate or upgrade the prior authored 24-packet joined-premise exercise into a C2C reproduction.

The later numerical replay study already distinguishes tensor replay correctness from semantic correction recognition and artifact authenticity. Its random NumPy attention model and token-prefix planner are not cross-model cache translation. No new run here changes those outcomes or proves any semantic-memory benefit.

## Interpretation and useful next contact

**Inference:** Cross-family demonstrations are evidence for the evaluated trained pairs and alignment procedure. They do not establish a universal cache format, zero-training pairing, stable behavior after model/tokenizer revision drift, or reliable source-truth selection. Reported accuracy-point differences should not be silently converted to relative-percent gains. Latency depends on the chosen text baseline's generation behavior and the measured hardware/workload; the headline should not be promised for our workflow.

No new C2C capability can be adopted in this chat from this refresh. The available agent interface does not expose this chat's KV tensors or permit inserting trained fusers into its serving stack. Source files and text handoffs remain different operations from activation sharing. A minimal current-shell runtime probe was subsequently performed for the AKV inspection below; it does not inventory every project virtual environment.

The main agent subsequently authorized the bounded read-only AKV contact below. It establishes a concrete operation and runtime boundary, without recommending installation. A real pretrained corrected-history cache test remains unexecuted.

## AKV follow-up: actual operations, provenance boundary, CPU suitability

Pinned head: [c567a429a058f1abce3b2879e69978b09e0fda4c](https://github.com/thu-nics/AKV/commit/c567a429a058f1abce3b2879e69978b09e0fda4c), dated 21 October 2026, returned by GitHub's default-branch commit endpoint. Read top-level README, system README, agent policy and request helpers, agent/system/root package manifests, and the reposition kernel. Did not read the AKV paper or audit the entire server patch, cache tree, scheduler, eviction logic, tests, or benchmarks.

**Mechanism from docs/source:** The [README](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/README.md) splits agent-side selection policies from a modified SGLang server. Drop removes selected messages' KV entries after a declared trigger message; retained positions stay unchanged. Reposition separately compacts retained positions. The original complete message history and numbering remain in requests. Policies can use turn counts, token budgets, or agent tools. This is within-model cache surgery, not C2C's trained cross-model fuser.

The [actual reposition kernel](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/sglang/kernels/ops/attention/context_reposition.py) uses old/new RoPE tables to undo the old key rotation and apply the new one. It copies V and nonrotary K components, retaining source bits for same-position copies. The wrapper explicitly requires tensors on one CUDA device, page size one, and unquantized float16/bfloat16/float32 KV. Its docstring says the caller supplies disjoint destination slots and validates CPU positions/slots. This verifies a mechanism in the file, not correct integration across all server paths.

**Relevant semantic limit — inference:** Reusing a retained token's V and contextual key content cannot in general make it equal to a newly computed token state from a history in which the dropped message never existed. A retained later token may already encode that message. AKV therefore does not contradict our earlier result that rebuilding after a textual edit is needed to reproduce full fresh-forward computation in the authored causal-attention toy: it defines a different cache operation. Removing a fact's direct KV access is not demonstrated epistemic retraction or complete forgetting. Reposition alone is not recomputation of all causal dependencies.

**Continuity versus provenance:** [CachePolicy.process](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policy.py) preserves cumulative operation history; [request.py](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/policies/utils/request.py) hashes the accepted message prefix/boundaries and selected context settings (`model`, `tools`, chat-template kwargs, reasoning effort, API style). Reusing an operation history with a changed prefix or settings raises an error. It deep-copies the outgoing payload and renders cumulative Drop/Reposition fields without deleting messages. These inspected checks do not bind model weight/tokenizer revisions or authenticate actual tensor bytes, source authority, or factual claims. The full backend may have additional validation; it was not audited here.

**Supported scope from [system README](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/README.md):** Qwen/Qwen1.5–2.5/Qwen3 including MoE and AgenticQwen, GPT-OSS, and MiniMax-M2 architectures. Tensor parallelism is supported. Context operations exclude pipeline/context/decode-context parallelism, speculative decoding, LoRA, HiCache, external/session caches, and beam search. Listed attention backends are FlashInfer, Triton, and FA3 subject to GPU/model support. This is a documented compatibility list, not tested coverage by us; SmolLM2 is not on it.

**CPU/local feasibility:** The [system manifest](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/system/pyproject.toml) requires modified `sglang==0.5.20+akv`, router `0.3.2+akv`, and a CUDA13 Mooncake package; Python is constrained to 3.12. The README additionally requires Rust/Cargo and a C++20 compiler for startup CPU kernels. Those CPU kernels do not make the inspected CUDA reposition path CPU-compatible. The initial shell probe used ambient Python, which lacks Torch/SGLang; it did not inspect the actual FRR runtime. At the main agent's correction, a read-only probe of `/workspace/cache_backend_venv/bin/python` confirms **Torch 2.6.0+cpu, Transformers available, CUDA unavailable (`torch.cuda.is_available() == False`), SGLang unavailable**. The shell also lacks `nvidia-smi`; no wider hardware inventory was run. Thus Torch is present in the working project environment; the missing pieces for this inspected AKV path are its compatible CUDA backend and modified SGLang stack.

The [agent manifest](https://github.com/thu-nics/AKV/blob/c567a429a058f1abce3b2879e69978b09e0fda4c/akv/agent/pyproject.toml) declares no base dependencies, with optional tokenization dependencies. Pure policy/payload logic is plausibly suitable for separate CPU study, subject to Python/import verification. I did not install or run it. The actual cache backend cannot run unchanged on the CPU setup under this inspected CUDA path, and it does not accept the current SmolLM adapter as a documented supported configuration.

**Stop point:** No immediate runtime adoption. The useful conceptual distinction is exact corrected-history replay versus deliberate retained-state cache editing. If compatible GPU/backend access is later authorized, a bounded comparison should preserve those as different conditions and measure factual correction answers plus residual dropped-context influence; that experiment is not run or scheduled here. This authorized scout stops after recording this note.

## Access scope and remaining uncertainty

Used the GitHub connector for current commit metadata, commit diff/comparison, README, projector, example recipe, and the bounded AKV files listed above. Used browser retrieval for arXiv abstract/history and v2 HTML methods, results, relevant appendices. No secondary articles, author contact, remote demo invocation, model/checkpoint download, benchmark reproduction, or activation inspection. Default-branch head is a time-of-access observation. The inspected commits were reported unsigned by GitHub; no provenance stronger than repository retrieval is claimed.

Cloud runtime/network skill had already been read for this scout session; network policy was inspected and HTTP policy reported enforced/unrestricted. No credentials were printed. This note is the only new workspace artifact for this refresh.
