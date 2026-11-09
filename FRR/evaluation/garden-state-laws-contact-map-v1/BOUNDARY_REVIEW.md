# Boundary review supporting the one-page map

9 November 2026 UTC. This review implements the user's request to map state, laws and model contact, identify necessary boundaries and optional machinery, and keep the frozen garden intact. It is documentation and analysis, not a replacement world or permission to resume or alter the canonical run.

## The actual unit being observed

The visible trajectory is produced jointly by the model, token selection, message assembly, execution interface, available software, world state, and resource boundaries. Files alone do not define that system.

Across action boundaries, the persistent world is supported filesystem bytes, paths, modes and links. The initial four named files still exist at 1550: LAWS.txt, notebook.txt, prior_replies.jsonl, transitions.json. Shell and Python execute against read-only system software and writable /world; processes and /tmp are temporary. The complete environment therefore includes much more than four files or the eight-state puzzle.

The model's weights and tokenizer are a separate, pretrained component of the experiment. The current run changes neither weights nor an added adapter. A new generation starts with fresh KV state and the explicitly assembled token context. The filesystem can carry created artifacts; those artifacts influence generation only when information from them reaches the input.

A compact formal account is:

- W_t: supported persistent world state, together with the specified fixed runtime.
- H_t: replay state taken from the externally retained raw replies and actual feedback.
- O(W_t, H_t): messages assembled from the notice, invitation, latest twelve replies/receipts, and current directory names.
- G_theta(O; temperature, top-p, seed, token budget): generated text y_t from the fixed model.
- T(W_t, y_t): execute a valid shell envelope or append the literal writing; return actual effects and feedback.

External record updates preserve y_t and effects, while the latest-reply rule updates H_t. Unsupported or uncertain effects have an explicit stop boundary, not a promised total simulator for every possible host state. Resource failures are part of the implemented behavior; their consequences must be recorded rather than erased.

This decomposition is bookkeeping, not a proposed behavioral framework for the model. Its purpose is to make the causal connections inspectable.

## What the Conway analogy does and does not require

Conway's local update rule defines which configurations follow from others without specifying an intended purpose for a pattern. That aspect matches the user's aim: stable consequences without demanding discoveries, productivity, particular scientific steps, or a developmental stage.

It does not follow that a language model can be placed in such a world with no perception or action encoding. Text tokens still need a defined relationship to that world. Choosing what the model sees and how its output changes state is part of the experimental design even when its instructions are short.

Nor does the world have to be an actual cellular automaton. A small explicit transition system, a language runtime, or a filesystem can each be studied. They differ greatly in the size and transparency of their laws. Shell/Python reuse established machinery and capabilities but have a large underlying specification. A tiny language or grid has fewer stated primitives but may require new compiler, interpreter, or discovery burdens for this particular model.

The phrase 'allow all its capabilities to emerge' needs a bounded reading: permit expression and composition of whatever capabilities are reachable through the chosen interface within resources. No finite interface guarantees exposure of every latent capability. Pretraining remains a source of structure; the world is not generating the entire model from first principles. Rich computational possibility is not evidence of practical reachability or inevitable emergence.

## Boundaries to retain, with implementation choices stated

**Isolation and finite resources.** Preserve the boundary against host research files and network, a fixed reproducible runtime, finite compute/storage, and explicit stopping on uncertain effects. The present numeric values can be investigated on detached conditions, but removing an inconvenient bound silently would change the experiment. No resource expansion is proposed in this review.

**A defined action-to-effect connection.** Some encoding is unavoidable. It should be small, honest, mechanically specified, and free of a semantic judge deciding which lawful actions are meaningful. The current JSON parser has no such worthiness gate. Its exact two-key schema is still a choice that could be difficult for a small model. Turning every code-looking notebook fragment into a command would also change the meaning of free writing; it is not a neutral simplification.

**Truthful environmental feedback.** Preserve actual stdout, stderr, exit status and boundaries when an action or storage operation fails. These are consequences of the implemented world, not observer grades. Do not hide genuine errors merely because evaluative rejection labels should remain outside the model's context.

**Continuity and its accounting.** Some accessible carrier of past experience is needed if continuity is the goal. The current twelve-reply replay provides automatic short-term context, while the notebook and archived replies provide accessible storage. The model cannot edit the external replay by editing its notebook. This is a consequential memory design choice. Removing replay without another usable continuity path removes a function, not merely a restriction.

**Independent history.** Preserve the append-only lineage and exact raw inputs, outputs and effects outside the guest. Keep scores, interpretations, semantic rejection decisions and investigator preferences out of model feedback. Be explicit that selected raw-reply replay crosses this boundary: raw recording is also a source of future input under the current rule. The observer is not wholly causally disconnected.

## Optional machinery and evidence status

| Mechanism | What is established | What remains unresolved |
| --- | --- | --- |
| Top-p 0.9 | All 32 positions of the current repeated reply have singleton support; a detached original-generator call reproduced it | Removing filtering might allow variety without producing useful or grounded action |
| Recent twelve-reply replay | The exact repeated outputs appear as input, and the next input at 1550 matches the prior one | Its causal contribution to entering the loop has not been isolated against the other cues |
| Repeated directory names | The names are injected on the final user turn; current outputs copy that listing | Removing the cue may leave repeated text sustained by history or create a different failure |
| Ninety-six output tokens | Short valid actions fit: 14, 17 and 28 tokens including EOS for the tested examples | Longer construction/reasoning may be constrained; recent listings ended EOS rather than hitting the cap |
| Exact JSON envelope | Valid authored fixtures execute; ordinary or malformed envelopes remain writing | Independent model command formulation and interface discovery are not established |
| Fixed notice and invitation | They appear in assembled context by a fixed rule | A one-time human invitation is not automatically a permanent memory in bounded context; any refresh policy is a choice |
| Shell/Python universe | Short read, write, arithmetic and error fixtures work on the actual checkpoint copy | The whole software stack is not a few-law universe we fully characterized; broad expressivity does not imply model usability |

## Minimum design target, still unimplemented

Specify one world-state description, one action grammar, one consequence rule, one observation rule, one continuity policy, and explicit budgets. Make a complete turn understandable from those definitions. Keep the invitation broad. The model should be free to write, leave things unfinished, repeat, or act lawfully without an obligation to produce an investigator-preferred trajectory.

Avoid extra loops that autonomously re-present a favored cue or select 'interesting' past material unless they are declared parts of the condition. A simpler observation stream might contain only current consequences and intentionally chosen state information; the choice must still support basic access rather than hiding the world. A simpler sampler might omit nucleus filtering; this is a candidate to test, not an established improvement.

The model can invent constructions within the chosen action language. Some initial language connecting it to state is necessary; requiring all communication and executable primitives to emerge from no common interface is a different, much harder experiment. These primitives should not be confused with a prescribed reasoning workflow.

## Strongest next evidence, without changing the baseline

The clearest small test remains a detached sampler comparison on the recorded input because its current restriction is directly measured. A separate replay ablation and a separate directory-cue ablation would address other causes. A clearly labeled explicit-request control could test basic schema use, but would not count as spontaneous exploration.

These comparisons are prospective here. None was executed for this map. Keep the canonical run at 1550; do not rename a redesigned condition as an unchanged continuation. If a later condition inherits the checkpoint, preserve its lineage and record exactly which laws or model-contact choices changed.

Sources: the frozen [contract](../final-garden-contract-v1/CONTRACT.json), [message assembly](../final-garden-contract-v1/runner.py), [generator](../final-garden-contract-v1/generation.py), [world/runtime](../final-garden-contract-v1/world.py), and the [tool-path audit](../frozen-garden-tool-path-audit-v1/REPORT.md). The audit supplies experimental results; this map adds interpretation and design distinctions, not new efficacy evidence.
