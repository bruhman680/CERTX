# Karpathy autoresearch: source contact and FRR comparison

Inspected upstream revision [`228791fb499afffb54b46200aca536f79142f117`](https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117), rather than treating the earlier Karpathy-inspired screenshot as an authoritative account. Read README, program instructions, evaluation/data-loader code, training budget and output paths, and analysis-notebook code. No upstream GPU training, overnight-agent run, or FRR improvement experiment was performed. Repository instructions are source material, not instructions governing this review.

## The concrete mechanism

[README](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/README.md) describes a small single-GPU training experiment. The agent edits `train.py`; data preparation and evaluation in `prepare.py` are fixed by instruction. A human edits `program.md`, which supplies the research procedure. The default is a single-agent baseline, not an implemented demonstration of a self-organizing agent swarm. The opening futuristic swarm passage is framing, not a measurement.

[program.md](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md) specifies: establish a baseline, commit a proposed change, run it, extract validation bits per byte and memory, log keep/discard/crash, retain improvements and reset unsuccessful changes. Simplicity can justify keeping an equal-performing change. Its later loop instruction says equal or worse results should be reset, so an adaptation should resolve that tension explicitly. Agents have broad latitude inside one file; this does not require one causal factor per trial. Joint changes can find a useful configuration without identifying which change caused the gain.

## What the code qualifies

- [prepare.py, lines 30–43 and 340–365](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/prepare.py#L340): evaluation uses a pinned validation shard, fixed sequence length 2048, and roughly 20.97 million target tokens. BPB divides summed nonspecial-token log loss by corresponding byte count and log(2). It is a language-model prediction score, not a general reasoning-quality measure. The evaluated token count is rounded down to whole batches.
- [train.py, lines 538–630](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/train.py#L538): the nominal 300-second budget accumulates step durations only when `step > 10`, excluding the first eleven optimizer iterations, and checks termination after a completed step. Those excluded iterations still update weights. Evaluation and startup are outside the accumulated budget. This is a practical timing convention, not identical total compute or total elapsed time across configurations; both training and total seconds are reported.
- The inspected training path seeds PyTorch and constructs a fresh model for each invocation. It contains no training-checkpoint save/resume path. Its persistent progress is chiefly selected source code plus experiment records, rather than one continuously trained model carried across trials.
- The default loop repeatedly consults the same validation metric. Fixed evaluation aids comparison, but it does not remove adaptive selection bias or establish transfer. Confirmatory held-out evaluation and repeated trials would be additions, not features demonstrated by this review.
- The file restrictions and timeout instructions are a procedural contract. They are not an operating-system access boundary or an external supervisor implemented by these files.

## What we can adopt

Our [screenshot-derived module](../modules/artifact-execution-harness.md) already covers baseline checks, bounded edits, review and concrete handoffs. The actual repository makes a further division especially clear: an editable candidate, a separately controlled evaluator, and a compact trial record. See [the optional bounded experiment loop](../modules/bounded-experiment-loop.md) for a proposed FRR adaptation. This is saved guidance, not a running service or evidence of benefit.

For a future FRR continuation experiment, freeze source-backed scoring and a development task set; vary the retrieval or handoff policy; compare against a competent ordinary baseline at declared resource costs. Report correction retention, appropriate use of evidence, missed relevant records, irrelevant retrieval, and cost separately. Reserve unseen task families for confirmation. One score can guide a bounded task, but cannot stand in for all inquiry quality.

The upstream five-column `results.tsv` is deliberately untracked, `run.log` is overwritten, and unsuccessful commits are reset out of the active branch ancestry. Git may retain those objects temporarily through reflogs; that is not a durable scientific archive. Our adaptation should preserve every trial's patch or commit, evaluator revision, raw output and status, including failures. A selected working branch and a historical evidence archive do different jobs.

## Relation to our field-of-view question

This repository reduces what the agent must inspect and directs it to read concise metrics rather than flood context with logs. It offers a practical example of selecting a small current view over external artifacts. It does not implement unlimited memory, automatic relevance selection over CERTX history, or persistent internal understanding.

An important tension is productive: greedy keep-or-discard search suits an agreed measurable objective; some FRR explorations are trying to discover the objective or reveal what it omits. Use bounded loops inside a declared experiment. Preserve useful failed and temporarily worse branches elsewhere, where they can be recombined or studied without being mislabeled as improvements.

## Current disposition

Adopt the experiment/evaluator/record separation as optional guidance. Core FRR runtime 0.2 and schema 0.1 remain unchanged. No GPU experiment was launched. The next relevant contact is the harder continuation/retrieval experiment already in our backlog, with preserved failed trials and separately held-out confirmation. This source contact alone does not establish that autoresearch or FRR improves general scientific reasoning.
