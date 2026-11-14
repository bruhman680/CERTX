# Pass 1: the model body, its interface, and decoding support

Read 14 November 2026, America/Chicago. Three primary-source contacts, selected for the completed observation/decoder/retrieval probes. This is a targeted scout, not an exhaustive review. No model calls, downloads, installations, external code execution, or main-garden changes were made.

## 1. Check the exact body before borrowing a family capability

The [official SmolLM2-135M-Instruct card at the cached revision](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct/blob/12fd25f77366fa6b3b4b768ec3050bf629380bac/README.md) describes 2T-token pretraining, supervised instruction tuning and DPO. Crucially, its function-calling claim is explicitly qualified to the 1.7B family member. Its 135M evaluation table covers instruction/general reasoning benchmarks, not our persistent Python-file environment. The card also cautions that outputs can be inaccurate or inconsistent. Read depth: model summary, usage, evaluation, limitations and training sections; exact revision confirmed in page.

**Local inference:** the 135M body has substantial prior training, but neither its size label nor the family card establishes success at this particular file-reading task. Conversely, four filename-as-JSON mistakes in one repeated history do not establish an intrinsic inability to read files. Capability, elicitation, context and environment remain separate variables. Do not substitute a larger family member's advertised tool results for measurement of this body.

## 2. Small tool agents are often deliberately specialized

[TinyAgent v3](https://arxiv.org/html/2409.00608v3), dated 25 October 2024, studies 1.1B/7B models trained for a fixed 16-tool Mac assistant. Sections 3.1–3.4 describe initially poor plan generation, task-specific finetuning, tool/example retrieval and dependency-graph evaluation. This is explicit training and application design, not merely supplying an open sandbox. Its [official README pinned at cc45c0e](https://github.com/SqueezeAILab/TinyAgent/blob/cc45c0e842f5d163c3df1c8f41d60e90e005867d/README.md) warns that its open models/ToolRAG were trained on the original toolset; custom-tool support is qualified to GPT models. The README says 40K use cases while paper v3 says 80K training examples: preserve that version discrepancy rather than silently reconciling it. Read depth: abstract/introduction and sections 3.1–3.4 plus README capabilities, ToolRAG, trained models and customization; no code audit or reproduction.

**Transfer boundary:** its benchmark wins do not establish open-ended emergence, arbitrary new-tool transfer, or 135M competence. Tool selection and supplied examples are additional mechanisms with their own failure modes. A call graph being correct is also a narrower criterion than checking that a real user-world effect occurred.

## 3. A seed only matters where the decoder permits alternatives

[Transformers generation documentation v4.57.1](https://huggingface.co/docs/transformers/v4.57.1/en/main_classes/text_generation) distinguishes greedy decoding from sampling and defines temperature, nucleus filtering, output limits, cache and score-return settings. This version matches the installed package version read locally. Read depth: GenerationConfig strategy, cache, logits and output sections. The previously opened v4.56.0 page is superseded for this contact; neither page is a reproduction of our custom incremental sampler.

**Local inference:** our measured 255 singleton positions on one greedy path explain why reseeding top-p .9 had little room to change those replies. The one two-choice position prevents a claim of complete determinism. Full-support sampling changed text in two branches but produced no complete executable cell. A decoder change is an experimental condition, not demonstrated learning or a task repair. Library defaults must not be silently mixed with the worker's declared custom implementation.

## Strongest next diagnostic, before another world alteration

The existing prompted retrieval experiment placed its task after eight old repeated output/receipt pairs. It did not include a fresh-history control. The clean next detached comparison is the **same pinned body, world, file-reading request, decoder and token cap**, with (a) original repeated history and (b) neutral fresh context. This measures a history-condition effect; shorter input and different positions remain part of that bundled intervention. A later length/position-matched irrelevant-history control would be needed to separate history content from those confounds.

Within each context condition, retain two hidden nonce worlds with identical model input and one authentic operator-read control. Rotate new nonces/paths in any replication and keep answers out of task text. Distinguish: target available on disk; valid cell emitted; open/read actually attempted; target returned by the environment; target used in the reply. Merely inserting a correct receipt cannot count as model retrieval, and process exit 0 cannot count as task success.

This design is our inference from the local failure and source limitations, not a protocol reproduced from TinyAgent. Do not insert demonstrations, auto-repair parsing, train weights, add tool APIs, or adopt sampling changes in main as part of this scout. Any such comparison should be declared separately so increased assistance remains visible.

## Adaptive handoff to the next pass

Scout upstream/laterally for **demonstration/history effects and position dependence**, and for **active acquisition versus passive availability**. These are more diagnostic of this result than collecting additional large-agent success headlines. Counter-scout whether fresh prompting changes apparent capability and whether generic tool evaluation conflates syntax, plan correctness and realized state. No source here warrants attributing the old repeated output to maturation, panic, attention failure or absent internal representation.

All opened primary contacts succeeded. Search-only alternatives and third-party copies were not promoted to evidence. The GitHub repository metadata and pinned README were read through the GitHub connector; arXiv/HF pages through web access. Search results included later small-model tool benchmarks, but these were not opened or relied on. See SOURCES.json for access/version scope.
