# Cache replay, tool gaps, and a lateral visual-context scout

Client 28 October 2026 America/Chicago; host 29 October UTC. User authorized confident experiments, tool-gap scouting and a parallel heart-image scout. This contact delivers an optional executable planning helper, an actual NumPy KV-cache experiment and primary-source setup notes. It does not reproduce SwaT or test a pretrained model's reasoning.

## What we can use now

New [cache_replay_plan.py](../../tools/cache_replay_plan.py) takes old/new integer-token histories, a cached prefix count/digest and caller-declared execution identities. It returns how much unchanged prefix may be retained and which suffix must be replayed. Model/tokenizer revision, position configuration, attention policy, KV layout, precision, adapter/multimodal identity and namespace are explicit. Unknown identity, incompatible identity, unsupported mask policy or a bad prefix digest forces a full rebuild; invalid token/count structure is rejected.

It plans reuse for causal full-attention caches; it does not own or inspect a real backend's tensors. It is an optional standalone tool, not a modification to the chat service, runtime prompt or default reasoning behavior. [CLI input](CLI_EXAMPLE.json), [usage](USAGE.md).

## Executed numerical contact

[Prospective protocol](PROTOCOL.md) and its hash were saved before execution. Five fixed seeds, ten fixtures per seed, two causal residual-attention layers, width 16, vocabulary 64, NumPy float64, random untrained weights. A vectorized full forward pass is compared with a separately written token-by-token KV implementation after applying the replay plan. This is two paths in the same authored model, not independent external replication.

| Case | Reuse prefix | Replay tokens | Interpretation |
|---|---:|---:|---|
| Append two tokens and query sentinel | 24 | 3 | Old prefix remains numerically reusable |
| Replace early token | 3 | 22 | Rebuild from first changed token |
| Delete three middle tokens | 10 | 12 | Later positions/state need recomputation |
| Replace late token | 20 | 5 | Retain only the unchanged prefix |
| Change actual model weights | 0 | 25 | Rebuild with new model |
| Change actual position offset | 0 | 25 | Rebuild with new positions |
| Change declared adapter or image identity | 0 | 25 each | Metadata routing checks; no actual adapter/image modeled |
| Tamper prefix digest | 0 | 25 | Rebuild despite unchanged mathematical weights/history |
| Only nine tokens cached | 9 | 17 | Reuse is limited by actual declared cached length |

All **50 cases** matched full-rebuild replay-position logits within the prespecified absolute 1e-10 tolerance. Maximum observed discrepancy was **1.5543122344752192e-15**. Final cache arrays and replay/full row counts are recorded; no timing advantage was measured. There are ten fixtures repeated across five seeds, not fifty independent semantic tasks. Token numbers do not encode natural-language corrections or quantifiers.

An intentionally naive control continues from the old cache with only a query sentinel. For early replacement, its maximum-logit discrepancies range approximately 0.0396–0.1234; for middle deletion, 0.3516–0.5229. This control represents ignoring the changed/missing history, not a competing optimized replay algorithm. Metadata-only identity changes leave the toy mathematics unchanged, so the naive control can still match numerically in those cases; conservative invalidation is not proof that every declared change alters the answer. [Original results](RESULTS.json), [post-development expected-prefix checks](PLAN_CHECKS.json).

Append-only additional context can be processed while retaining the old prefix. Editing an earlier token requires rebuilding its affected suffix in this architecture. Neither observation establishes that a pretrained model recognizes a correction, prioritizes the newer evidence or remembers an unqueried fact. That remains the semantic next step.

## A real defect and a limit we did not repair away

Boundary review found that the first helper accepted a matching literal `unknown` model revision and reused two tokens. That violates the intended unknown-identity policy. The [failed result](UNKNOWN_IDENTITY_FAILURE.json) and [original helper](before_unknown_identity_fix/cache_replay_plan.py) are retained. The small repair rejects blank/whitespace and case-insensitive unknown, unspecified and unavailable markers. [Fourteen supplemental checks](SUPPLEMENT_RESULTS.json) cover markers, all nine identity-field changes and the CLI path; all pass. The eight original malformed/missing-input checks also pass. A necessary post-fix rerun of all fifty numeric fixtures produces the identical saved results, not new scientific replication. [Regression results](RESULTS_AFTER_IDENTITY_FIX.json).

A second diagnostic keeps valid token metadata but alters an actual value tensor. The planner still permits the unchanged prefix, while final logits differ by about **0.479**. This is the advertised limit of metadata consistency: it cannot authenticate that a cache artifact came from those tokens and weights. A backend must bind actual tensors, execution configuration and artifact provenance. A hash over declared token IDs is not a proof of tensor origin or factual correctness.

## Scout findings and useful reengineering

[Tool scout](SCOUT.md) connects observed environment capabilities to pinned SwaT configurations and official Transformers/vLLM cache documentation. NumPy is present; PyTorch/Transformers are absent and no nvidia-smi command is visible. No large framework, model weights or datasets were installed. We built the small numerical backend and replay planner within the available tools instead of relabeling it as SwaT. Real cross-family translation still needs compatible models/mappers, tokenizer alignment, dependencies and a controlled evaluation.

A parallel [heart-image scout](HEART_SCOUT.md) found a strong plausible match, [A Heart Means Recursion](https://arxiv.org/abs/2610.36449), by Google DeepMind-affiliated researchers. The user subsequently recalled a Google VLM paper, consistent with this match; the original X post remains unidentified. Here recursion refers to generated recursive code rather than iterative code, not endless looping or a measured internal recursive state. No model calls or effect reproduction were performed.

Our lateral inference: surrounding inputs can affect what information or strategy is used, so verification should distinguish an intended task change from an unintended contextual influence. Numerical cache validity and semantic decision stability are separate measurements. The visual paper suggests possible context-sensitivity probes; it does not establish how a heart would affect this session, all models, or all tasks. Source access limits and proposed controls remain in the scout rather than being promoted to a universal harness rule.

## Next and record boundaries

Strongest next: a pinned pretrained single-model cache backend with artifact binding, followed by corrected-history answer tests. Lateral: exact-material heart/no-image/blank-image screening, only after recovering prompt/assets/model settings. Both proposed; no API execution or new credentials requested. The semantic experiment announced at the outset was narrowed to numerical replay after the runtime probe; no actual semantic-reader effect is claimed.

One scout agent handled the heart lead. Root authored, implemented and reviewed the numerical tool; no independent code/model audit is claimed. Protocol, raw outputs, original helper failure, fix, regression, source pins and current navigation snapshots are retained. Runtime/core/schema/queue status and historical verdicts are unchanged. No background process or automatic continuation is scheduled.
