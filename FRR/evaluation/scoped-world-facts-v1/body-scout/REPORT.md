# Body and proficiency scout: training is prior soil, not an agency baseline

Status: bounded primary-source scout, 2026-11-15. No model calls, downloads, installs, external-code execution, or main-garden changes. Main remains preserved at entry 1630.

## Exact contacts and source findings

**SmolLM2, arXiv:2502.02737v1 (4 February 2025).** Read abstract, background, evaluation setup, post-training context, and all of §6; inspected adjacent tables to determine their model scope. The paper specifies 135M training on 2T tokens. Smaller variants used single-stage curated mixtures including filtered DCLM, Stack-Edu, InfiMM-WebMath, FineMath and Cosmopedia. Their SFT used filtered SmolTalk, excluding complex instructions such as function calling and difficult MagPie-Ultra examples, followed by UltraFeedback DPO. Main base/instruct tables are for 1.7B. The authors refer readers to smaller-model cards for further detail; their paper does not give a 135M ambient-world agency evaluation. General base evaluation uses lighteval, zero-shot unless specified, but this does not turn the 1.7B results into measurements of our body. [Primary paper, §6 and §§4.7–5.4](https://arxiv.org/html/2502.02737v1).

**TinyStories, arXiv:2305.07759v2 (24 May 2023).** Read abstract/introduction, dataset and instruction variant, GPT-Eval methods, and §4.2 with nearby examples. Models below 10M parameters trained on a deliberately narrow story distribution produced coherent stories. GPT-Eval used around 50 manually constructed beginnings, ten temperature-1 completions each, and GPT-4 grading for grammar, creativity and consistency. Additional prompts elicited factual, reasoning and context-tracking continuations. These are text-generation evaluations of separately trained bodies; they do not measure environmental action selection. Instruction-conditioned story generation also had its own training-data variant. [Primary paper, §§2–4.2](https://arxiv.org/html/2305.07759v2).

Neither source was reproduced; selected-section reading is not a full-paper audit. No new model card was counted as a third contact. Existing pinned local MODEL_PROFILE.json remains the source of our card-value record.

## What follows for this experiment (our interpretation)

The inherited model is not a blank seed. Its words, conventions and responses reflect prior training. However, these distinctions must remain separate:

| Layer | What would count as local evidence | What is insufficient |
|---|---|---|
| Text competence | Accurate response under a specified text test | Parameter count, training-token count, or fluent prose alone |
| Elicitation | A protocol actually creates an occasion for the capability | Merely declaring the world available |
| Action selection | Model emits an executable action through the actual parser | Describing an action or echoing the world description |
| Environmental consequence | Executor receipt and resulting state change | A claim that the action happened |
| Adaptation | Behavior changes with identified feedback/context/state exposure | Passage of entries alone |
| Weight learning | Documented optimizer updates and changed weights | Persistent files or a growing transcript |

TinyStories is a useful counterweight to a fixed intelligence ladder: distribution and evaluation matter. It supplies no warrant to label our model a child, assign it an IQ or use its parameter count as a capability ceiling. Likewise, exclusion of function-calling examples is a training-recipe fact, not a proof that executable action is impossible.

## Concrete baseline implication

Keep the proposed prose-versus-JSON contact narrow: same explicit scoped facts, same initial world metadata, body, roles, decoder, action grammar and inherited files. Classify spontaneous executable actions and actual consequences separately from accurate prose and repetition. If both conditions remain note-only, the conclusion is **no action elicited in these short task-free conditions**. It cannot distinguish missing understanding, missing motivation, formatting difficulty, inherited conversational habits, or decoder effects.

Do not repair this uncertainty by slipping in a quiz, action example, reward or action instruction. Those would be separately declared contacts. The present scout recommends no body replacement, retraining or solution teaching. A later optional proficiency probe could establish a local capability under an explicit request, but its positive result would not retroactively establish spontaneous agency in this task-free world.

Garden rendering: the seed arrived with years of weather in its grain. That tells us it has roots; it does not tell us which doorway it will choose when no one names a destination.
