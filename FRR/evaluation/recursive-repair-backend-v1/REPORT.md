# Practicing bounded recursion and reaching a real pretrained cache backend

Client 28 October 2026 America/Chicago; host 29 October UTC. User authorized continued experiments and asked whether recursion can be practiced now. Yes: explicit recursive dependency checks are usable, with grounding and stopping rules. This contact separately tests a typed recursive audit and a public pretrained model's cache replay. Neither establishes autonomous recursive self-improvement, an internal recursive reasoning mechanism or the heart-image effect.

## The practical change

The previous [cache replay/tool-gap contact](../cache-replay-tool-gap-v1/REPORT.md) used an untrained NumPy network because no framework was installed. This run created an isolated CPU environment outside the FRR package, installed PyTorch 2.6.0 CPU, Transformers 4.57.1 and safetensors 0.6.2, and downloaded the public [SmolLM2-135M-Instruct model](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct/tree/12fd25f77366fa6b3b4b768ec3050bf629380bac). Exact revision and file hashes are saved. No paid API, credentials, remote model code, GPU or SwaT mapper was used. The model card describes this as an instruction-tuned small model, not a visual model or the model used in our prior reader trials. It is a suitable small integration probe, not a proxy for all model capability.

The protocol, model pin and six semantic case/key texts were frozen before inference. A separate graph/code freeze preceded graph execution. [Prospective protocol](PROTOCOL.md), [backend cases](BACKEND_CASES.json), [graph cases](GRAPH_CASES.json), [model pin](MODEL_PIN.json), [downloaded file hashes](DOWNLOADED_FILES.json), [environment](ENVIRONMENT_REQUIREMENTS.txt). `public_api_metadata_only` in MODEL_PIN describes the initial pin lookup; it does not mean this later run avoided loading weights.

## Recursive audit: six scoped cases

The [recursive evaluator](recursive_audit.py) descends from a requested decision to its declared child dependencies. It validates child fingerprints before reusing a memoized result, applies stipulated numeric/conjunction rules and returns the resulting change to the parent. Old outcomes are kept separately. Source facts and dependency relationships are supplied typed data, not discovered natural-language reasoning.

| Change or boundary | Historical result | Reassessed result |
|---|---|---|
| Correct retention measurements | Supported | Contradicted |
| Switch criterion from median to mean on 70, 90, 90 | Supported | Contradicted |
| Withdraw permission | Supported | Contradicted |
| Remove measurements | Supported | Unresolved |
| Add a self-dependency | Supported | Unresolved; cycle stop |
| Put evidence beyond declared depth | Supported | Unresolved; depth stop |

All six outcomes match the prespecified literal fixture key. A naive unchecked reuse control keeps the old supported assessment. Some unchanged dependencies are reused; unrelated nodes are not requested. Traversal still checks reachable dependencies before memo reuse, so this is not a demonstrated runtime speedup or constant-time repair. An iterative algorithm could implement the same dependency semantics. No general advantage of recursion over iteration follows. [Complete traces](GRAPH_RESULTS.json).

## Pretrained backend: computation matched; answer contract did not

For six authored correction/scope cases, the old prompt was prefetched into an actual KV cache. The cache was serialized to safetensors, bound to file bytes and declared model/tokenizer/config identities, reloaded, cropped to the unchanged token prefix and continued with the revised suffix using the existing [planner](../../tools/cache_replay_plan.py). An independently computed full revised prompt was the reference. Both then decoded greedily, without sampling, for the frozen maximum of eight new tokens, with eager float32 CPU attention and two threads.

All six last-prompt logit vectors had observed maximum difference **0.0** in this run; all six greedy token sequences matched exactly. This is observed same-model execution equivalence on these six prompts, not a guarantee across versions, batching, masks or models. It does not transfer caches across families. [Backend code](backend.py), [results](BACKEND_RESULTS.json), [raw log](BACKEND_RUN.log).

All six outputs failed the requested PASS/FAIL/UNKNOWN first-label format. Thus strict label-and-gold matching is **0/6**, including two fragments whose ordinary-language direction agrees with PASS. The result field `semantic_gold_matches` implements only this strict first-label match; it is not a six-item general factual-accuracy measurement. Do not recode answers into labels after the fact or call all six semantically wrong. Eight-token outputs are budget-limited fragments; the cap is a substantial interpretive limitation and must stay visible.

For example, B4 begins by asserting improved completion even though the dawn-shift group had no measured results, and B6 begins by saying the rule is met even though one error exceeds its every-item limit. These are observable conflicting fragments, not full reasoning-trace diagnoses. B1 and B2 begin with affirmative responses compatible with their PASS key but still violate format. B3 is too incomplete for a confident whole-answer interpretation. We did not retry, extend generation, change prompts, constrain decoding or tune the key to improve the score.

This is the useful separation: correct numerical replay preserved the same response, including its limitations. It did not make the model a better verifier. The next semantic evaluation needs an explicit format-versus-content rubric and a separately chosen output budget/model; any follow-up must preserve this run.

## Artifact binding: a narrow gap is reduced

Each actual cache artifact is saved locally, with its SHA-256 and byte size in the results; weights and cache tensors are not published to the research repository. Reloading checks its exact file hash before deserialization. One byte-altered cache has a different hash. A [supplemental exercised loader](artifact_check.py) successfully loads the original and raises a binding mismatch before loading the altered file; [diagnostic](ARTIFACT_CHECK.json). The supplementary function is not silently substituted into historical inference code.

This improves on the previous planner-only demonstration, where valid token metadata could accompany altered tensors. It establishes file-byte consistency against a locally recorded expected digest. It does not authenticate the original model execution, defeat a producer who forges both manifest and cache, or certify source truth. Immutable expected manifests and provenance trust remain external responsibilities. Cache state and model files must remain available to rerun; their local paths are environmental and not durable GitHub storage.

## What recursion we can practice

A bounded recursive review can ask: what supports this result; what supports that premise; what changed; what must be reassessed? It stops at sufficient evidence, missing information, repeated dependencies or its declared resource boundary. It then returns the scoped finding upstream. This run practices that distinction by checking numerical success, then checking whether answer behavior actually satisfied the task.

The [practice note](../../examples/bounded-recursive-review.md) is an optional file we can return to. It is not installed as an autonomous loop and has no measured effect on agent behavior. Existing [reopening checks](../../tools/reopen_assessment.py) remain useful for explicit recorded contract changes; no earlier tool/core/runtime/schema/queue status was overwritten.

Remaining gaps: natural-language dependency extraction, independent factual evidence, semantic scoring beyond a strict label, adequate model/output-budget selection, long recursive chains, model/version drift, authenticated provenance and cross-family transfer. Heart-image visual steering remains a separate [source lead](../cache-replay-tool-gap-v1/HEART_SCOUT.md); no visual experiment ran here. Code recursion, recursive review, output repetition and permanent model self-improvement remain distinct.

## Checks, scope and next contact

Root authored and reviewed the code and cases; no independent reviewer or new subagent was used in this contact. One backend inference run, one six-case graph execution and one post-run loader diagnostic are recorded; generated answers were not retried. Structural checks verify hashes, links and package/queue consistency, not broad effectiveness. Setup/model acquisition and logs are part of the work, with exact dependencies saved; no timing or cost advantage is inferred.

Strongest next: prospectively separate response-format compliance from answer content and allow complete responses in a matched cache/full comparison. First use a small number of independent corrected-history cases with a clear scorer; then consider stronger models or recursion-guided review with matched information/call budgets. Those changes are proposed, not secretly added to this run. Lateral visual/cross-family work remains open. No background process or automatic recursion is scheduled.
