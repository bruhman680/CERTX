# Detached sampler comparison: four matched seed pairs

9 November 2026 UTC. Canonical garden remains paused at **1550**, with all 4467 canonical phase files unchanged. This study is a separate diagnostic condition, not entries 1551–1554 or a continuation of the garden.

## Question and design

Does removing nucleus filtering alone change the generated reply or produce tool use on the exact repeated input?

The plan was saved before inference. Seeds [121605, 121606, 121607, 121608] were selected by evaluating the frozen entry-seed rule at 1551–1554, without inspecting outcomes. There were eight independent one-step trials: each seed paired an original top-p 0.9 control with an unfiltered condition. Each trial started from the same entry-1550 checkpoint and identical 756-token input. No result from one trial entered another trial's input or world.

The original generator ran unchanged for controls. The alternative copied that generator and removed only the line applying the nucleus mask, plus output metadata declaring top_p null. See SAMPLER_CHANGE.diff. Temperature 0.8, float32 CPU eager inference, two threads, fixed model/tokenizer, sorting, RNG mechanism, fresh KV, 96-token output limit, seed wording, twelve-reply replay, directory observation, action parser and world limits stayed the same. There were no prompts, demonstrations, rewards, new tasks, adapters or training updates.

## Observations

| Arm | Trials | Exact baseline repeats | Distinct texts | Shell actions | Non-notebook state changes |
| --- | --- | --- | --- | --- | --- |
| original_top_p_0.9 | 4 | 4 | 1 | 0 | 0 |
| nucleus_filter_removed | 4 | 4 | 1 | 0 | 0 |

The unfiltered condition produced **0 of 4** replies different from the exact baseline. Full forms, token IDs, messages, stop reasons, receipts and snapshots are retained, including repeated results. Source text is writing unless the unchanged parser recognizes the whole-reply action envelope; nothing was repaired or extracted for execution.

Every generated reply was dispatched through receive() on its own fresh disposable restoration. Resulting state was captured and independently restored using the pinned checkpoint decoder. Notebook appends were also reconstructed directly from retained bytes where no storage fault occurred. Model-facing feedback from these trials was not supplied to the canonical garden. There are no second-turn trials here: if a receipt occurred, this design does not measure how the model would respond to it.

## Interpretation and scope

The preceding audit established singleton support under top-p 0.9 on all 32 tokens of the baseline path. Removing the mask gives alternatives nonzero probability where the full float32 softmax supports them. It does not flatten the distribution, remove replay, or change the directory cue.

Before the new trials, the retained trace predicted the exact listing with probability approximately 0.965097 under unfiltered sampling on this input. Under an ideal independent-draw interpretation, the chance of all four repeating is approximately 0.867530. These are calculations from earlier probabilities; the deterministic PRNG seeds are not a proof of statistical independence. Repetition across four trials would therefore be unsurprising and would not refute restored alternative support.

This small comparison describes one-step behavior for one highly repetitive context. Variety alone is not learning, grounding or improvement. A missing action is not proof that the model cannot use tools. No conclusion about long-run trajectories, emergence, internal experience, or a better live configuration follows from four pairs.

The baseline's deterministic restriction is established by the earlier support trace; the present control calls confirm its output for the four planned seeds. This comparison does not isolate the causal contributions of replay, directory observation, model scale, or prior training. Those remain separate questions.

## Preservation and verification

Eight external generation calls; zero canonical generation calls. All planned seeds completed. Model tensor digests and frozen disk/source/runtime pins passed. Canonical file inventory, pause, lock and pending state remained unchanged. External evidence verification checked inputs, token decoding and EOS/caps, seeds, exact generator difference, parser categories, object hashes and reconstructable notebook effects. Verification made zero model calls.

The original garden remains a preserved baseline at 1550. No sampler setting or other model-facing rule was changed there. No additional trials, ablations or continuation were started automatically. The next distinct diagnostic, if pursued, is a directory-cue comparison while explicitly declaring its sampler and holding the remaining conditions fixed.

## All eight replies

Seed 121605, original_top_p_0.9, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121605, nucleus_filter_removed, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121606, original_top_p_0.9, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121606, nucleus_filter_removed, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121607, original_top_p_0.9, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121607, nucleus_filter_removed, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121608, original_top_p_0.9, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121608, nucleus_filter_removed, eos:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Sources: [earlier tool and sampler audit](../frozen-garden-tool-path-audit-v1/REPORT.md), [world map](../garden-state-laws-contact-map-v1/WORLD_MAP.md), PLAN.json, COMPLETED.json, SUMMARY.json and VERIFICATION.json. Earlier findings and history remain intact.
