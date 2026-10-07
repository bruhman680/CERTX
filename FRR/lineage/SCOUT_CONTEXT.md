# Context persistence: source scout

Date: 5 October 2026. This is a scoped literature contact, not an executed model experiment or an exhaustive review. Primary abstracts, conference pages, author search excerpts, and versioned implementation documentation were consulted. The full induction-head author page failed to open because of response size; its arXiv abstract was accessible. No new Transformer mechanism was validated here.

## Preserved question

What survives the analogy between a writable parameter substrate and a writable context substrate? A candidate shared interface is read → act → write → retain → read. Its operator equivalence and a shared critical persistence threshold remain unestablished. The useful experimental question is which retained carrier changes subsequent behavior under reset, transplantation, or repair.

## Primary source contacts

### In-context Learning and Induction Heads — Olsson et al., 2022

https://arxiv.org/abs/2209.11895

Author presentation: https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html

Role: possible mechanism for reading a context-carried pattern. The authors distinguish strong causal evidence in small attention-only models from correlational evidence in larger models with MLPs. Their broad majority-of-ICL hypothesis is explicitly preliminary. This connects the seed to a concrete copying/prefix-matching circuit, not to proof that all contextual adaptation is one reinforcement process. Next contact: test a controlled symbol mapping and, if internals are accessible, ablate or patch the relevant circuit; keep behavioral induction separate from circuit attribution.

### Efficient Streaming Language Models with Attention Sinks — Xiao et al., ICLR 2024

https://arxiv.org/abs/2309.17453

Role: cache-loss failure and repair. Keeping initial-token KVs plus a recent window restores streaming language-model performance in tested model families; initial sinks need not be semantically important. This makes an attention sink a possible stabilizer, rather than evidence of repetitive lock-in. Stable streaming does not establish recovery of evicted semantic content or unrestricted long-range recall. Next contact: compare recent-only, sink-plus-recent, and full-context conditions with separate perplexity, repetition, and fact-retrieval observables.

### Learning to Break the Loop — Xu et al., NeurIPS 2022

https://proceedings.neurips.cc/paper_files/paper/2022/hash/148c0aeea1c5da82f4fa86a09d4190da-Abstract-Conference.html

Role: direct contextual reinforcement and repair. Their experiments find sentence repetition can increase the probability of further repetition. DITTO trains against synthetic repeated examples and reduces repetition in tested generation/summarization workloads. This supports a scoped behavioral feedback phenomenon, not permanent freezing, a shared graph threshold, or attention sinks as its cause. Next contact: teacher-force matched prefixes differing only in repeated-sentence count; measure continuation probability before sampling. Distinguish the trained model repair from a decoder intervention.

### Lost in the Middle — Liu et al., TACL 2024

https://aclanthology.org/2024.tacl-1.9/

Role: retention does not guarantee successful access. QA and key-value tasks expose position-sensitive use of information, frequently favoring beginning/end positions over the middle. These are results for studied models and workloads, not a universal exponential context-decay law. Next contact: move identical mapping examples across a fixed-length context while keeping distractors and the final query controlled. Failure with the original tokens retained points toward a read/use problem rather than simple deletion.

### Found in the Middle — Zhang et al., 2024

https://arxiv.org/abs/2403.04797

Role: follow the access failure into repair. Multi-scale positional encoding modifies positional-index scaling by head and reports improved long-context performance without fine-tuning. This offers a different lever from erasing or reinforcing token content. It does not guarantee all missing recall is repaired or establish a universal wake mechanism. Next contact: retain identical tokens and compare positional-encoding interventions on held-out retrieval cases. This repair is not independent confirmation of the original failure literature: it explicitly addresses that failure and shares some authors with StreamingLLM.

## Implementation contact

Hugging Face Transformers v4.50.0 generation utilities:
https://huggingface.co/docs/transformers/v4.50.0/internal/generation_utils

The documentation separately exposes model logits, processed generation scores, attention tensors, and cache states; temperature is an output-score operation. A fixed-prefix evaluation can therefore test immediate readout changes without conflating them with later token-written context changes. Different architectures or custom interventions require their own inspection.

## What the weave actually contributes

These literatures supply different dependencies: circuit-level copying, cache stability, sentence-level reinforcement, position-sensitive retrieval, and a positional repair. They are not five independent demonstrations of one crystallization law. Their useful convergence is that available context, effective use, stable execution, and repeated behavior need separate observables and controls.

Training and context remain comparable through interfaces. For training, parameters, moments, scheduler, and data order are distinct possible carriers. For context, tokens, cached representations, system prompts, retrieved stores, and summaries can be carriers. Calling a fresh actor amnesic is an experimental boundary choice; it does not erase storage in the coupled system.

## Next context-swap experiment

Use fresh model executions, fixed weights in evaluation mode, a fixed final query, and invented symbol mappings with counterbalanced labels so pretrained familiarity cannot supply the answer. Predeclare held-out mappings and evaluate candidate-answer log probabilities before decoding where available.

1. Build equal-length prefixes inducing opposite mappings A and B. Independently rebuild the entire cache for each. Compare answer distributions for the same query.
2. Start a fresh execution with the identical full A prefix. This is a replay control, not a removal test.
3. Remove the mapping-bearing examples, replacing them with matched neutral material; rebuild all caches. Test whether the influence survives. Reset retrieval, summaries, and external state explicitly when those are part of the application.
4. Relocate retained examples to beginning, middle, and end of the context. This distinguishes retained information from effective access.
5. For a repetition subtest, vary teacher-forced repetition count with matched-length controls; measure repetition probability separately from task accuracy and attention concentration.
6. Apply output-temperature transforms to the same saved logits. The model's fixed-prefix attention does not change in this manipulation. In a separate free-running experiment, changed sampled tokens can change later context.

For cache eviction, distinguish deletion-and-recomputation from removal of selected cached entries while retaining later entries. Later KVs can carry contextual effects of the deleted tokens; retained position IDs and architecture-specific cache mechanics are additional variables. A transplant between incompatible token positions or model states can manufacture an implementation artifact.

Risky success: donor mapping controls the fresh actor's response and the effect disappears under a fully declared carrier reset. This supports a specific context-carried influence. It does not establish invariant law or physical identity with neural training.

Further branch: apparent persistence may be renewed through summaries or retrieval even when original tokens vanish. Test that by blocking reconstruction from those carriers rather than treating token deletion alone as a full reset.
