# Persistent text world scout: give the garden effective room to act

5 November 2026. Research and design inference only. Three parallel scouts inspected primary papers, official GitHub implementations and actual Hugging Face cards. No simulator installation, new model inference, training, paid API, or primary-world change was performed.

## Result

The user's intended environment is technically coherent: a persistent, bounded world with composable mechanics, effective agent choices, optional seeds and room for projects to outlast a run. Graphics are unnecessary for these properties. The strongest direction is a small local object/state engine borrowing proven patterns, rather than importing a large benchmark or adding more invitation language to the current numeric patch.

“Play, interact, learn, improve and tend your environment” can serve as the broad invitation. The engine must supply actual affordances and feedback. Learning, improvement, causal understanding, motivation and tending remain separate observations to test; those words in a prompt do not establish them.

The present garden remains paused at **entry 500**, original `discovery-play-patch-v1`, verifier **0096**. Its number is 0. This research neither resumes it nor activates a replacement. The previous [diagnostic report](../padding-and-prediction-v1/REPORT.md) remains the latest model evidence: long context can suppress control expression; all 24 tested consequence predictions were 8; format and content success differ. A richer world might provide better opportunities but does not repair these capabilities by itself.

## What the scouts found

| Source | Useful mechanism | Boundary relevant to our garden |
|---|---|---|
| [ScienceWorld](https://arxiv.org/abs/2203.07540) | Object properties/containment, mixing and connections, processes that advance over time | Existing tasks are episodic; durable sandbox continuity needs explicit engineering |
| [TextWorld](https://arxiv.org/abs/1806.11532) | Logical facts, action preconditions/effects, controlled task complexity | Quest completion and game generation are not free construction |
| [TextWorldExpress](https://github.com/cognitiveailab/TextWorldExpress/blob/main/textworld_express/textworld_express.py) | Small grounded action interface; seed/configuration/action-history restoration | Replay restores an episode; it does not itself create an enduring build world |
| [Crafter](https://github.com/danijar/crafter/blob/main/crafter/data.yaml) | Explicit gathering, crafting and placement recipes | Image-first survival engine; text adapter, peaceful rules and durable restore need work |
| [Voyager](https://arxiv.org/html/2305.16291v2) | Verified reusable executable skill library and feedback loop | GPT-4-based task generation/criticism; external skill memory, not weight learning |
| [DiscoveryWorld](https://github.com/allenai/discoveryworld/blob/main/discoveryworld/DiscoveryWorldAPI.py) | Object IDs, instruments, causal actions and structured observations | Current observation API renders/saves images even when the agent uses only text |
| [OMNI](https://arxiv.org/html/2306.01711v2) and [OMNI-EPIC](https://arxiv.org/html/2405.15568v3) | Task selection, failure archives and stepping stones | Separate pretrained selectors/generators and training machinery; the broad EPIC demonstration simulates learning |
| [AgentGym](https://arxiv.org/html/2406.04151v1) | Uniform action/observation interfaces and recorded trajectories | AgentEvol's improvement includes explicit fine-tuning, unlike our fixed-weight runs |

These are architectural precedents, not independent confirmations of FRR or evidence that this 135M+LoRA model will exploit the same mechanisms. Detailed read depth, caveats and implementation links are in [text worlds](TEXT_WORLD_SCOUT.md), [open-ended systems](OPEN_ENDED_SCOUT.md), [practical resources](RESOURCE_SCOUT.md) and [cross-review](PEER_REVIEW.md). Moving GitHub branches were inspected but not pinned or executed; source-derived feasibility is not local compatibility testing.

### Hugging Face: useful data, different from a living world

The inspected [ScienceWorld task-list card](https://huggingface.co/datasets/SeanWang0027/scienceworld-tcod-split) supplies task/variation descriptors, not executable dynamics or trajectories. It needs the simulator, and its declared ScienceWorld 1.2.3 basis must be checked against upstream version changes. The [TextWorld state-tracking card](https://huggingface.co/datasets/keenanpepper/textworld-state-tracking) supplies context/entity/state probes, not action execution. Its long contexts and narrow property inventory limit its immediate fit. Neither dataset was downloaded or used for training. They are optional evaluation resources; they do not provide continuity by themselves.

### Lateral contact: rules can be materials

The root scout checked the abstracts and official documentation/README of two adjacent systems, a shallower pass than the three main scouts. [Alchemy](https://arxiv.org/abs/2102.02926) explores latent causal structure; its [official documentation](https://github.com/google-deepmind/dm_alchemy/blob/master/docs/index.md) describes a symbolic version with discrete stone/potion actions and feature-vector observations alongside the 3D environment. This directly supports the distinction between underlying dynamics and graphical presentation. It is still a task benchmark, not a persistent construction world; no local symbolic runtime was verified.

[Baba Is AI](https://arxiv.org/abs/2407.13729) puts manipulable rule tiles inside a bounded game. The [official repository](https://github.com/nacloos/baba-is-ai) offers a Gym environment. Design inference: later, agent-authored arrangements or small interpreted recipes could alter in-world behavior while the host's interpreter remains fixed. This does not require arbitrary code execution or mutable host rules. It is a peripheral future direction, not a recommended first layer or an assertion that the current model can compose rules.

## Recommended first design: a small persistent workshop

This is a proposal, not built or activated here.

1. **World:** stable IDs; a small set of objects, materials and containers; connections; properties; a few transparent transitions. Start with one or two composable processes rather than hundreds of scientific objects. A circuit and a growing plant are examples, not mandatory first tasks.
2. **Effective choice:** inspect, move/place, connect/disconnect, use, write and wait. Creation draws from a finite catalog with known resource rules. The model may arrange and combine these freely within bounds; prose does not silently create state.
3. **Readable interface:** short local state, a compact action reference, inspectable rules and immediate state deltas. Optional valid-action menus reduce syntax burdens; they must not leak hidden puzzle answers. Host inspection may be comprehensive while the acting model sees a declared local view.
4. **Continuity:** versioned snapshots plus action log, explicit RNG state where applicable, durable IDs, deterministic replay tests and resource invariants. Pausing ends compute activity and freezes world time. A successful project does not automatically reset the environment.
5. **Time and tending:** make time advancement explicit. Free inspection should not quietly consume water or destroy a project. If actions advance processes, expose that rule. Tending means executed upkeep with measurable consequences, not gardening vocabulary in output.
6. **Optional seeds:** materials, notes, questions or puzzles placed in the same world. Record their origin and timing. The model can inspect, ignore, revisit or repurpose them within mechanics. Harness-selected goals must remain attributable to the harness.
7. **Memory:** distinguish persistent world artifacts, external notes/recipes, current prompt and model weights. Saving an arrangement does not mean it has been recalled; writing a recipe does not mean it works. Archive only tested recipes as verified, retain failed attempts separately.

We can fully specify the transition rules without knowing every arrangement or predicting the model's choices. That distinction preserves both host accountability and room for discovery. Bounds on materials, object count, action count and interpreter power need not prescribe one trajectory.

### Suggested broad invitation

> This world persists between visits. You may inspect, arrange, build, experiment, write notes and care for what you create. You may follow a seed or choose another activity. Use the available actions; their effects and limits are shown by the world. You can pause or leave a project unfinished.

Keep the invitation short and store mechanics in inspectable form. “Learn and improve” can be part of the aspiration, but should not become a demand to claim success. Narration can accompany action; it is not a substitute for action receipts.

## Strongest next work and confidence

**High confidence: specify and host-test a small engine before moving the primary.** Freeze action semantics, tick order, persistence and budgets. Use scripted action sequences to test creation/placement, impossible actions, resource conservation, process advancement, restart/replay equality and pause behavior. A finite enumeration is useful where the state space is small. This establishes our observational ground independently of model performance.

**Moderate confidence: a short isolated small-model affordance pilot.** Compare compact direct commands, a tiny valid-action menu and a brief free-choice invitation in matched starting worlds. Separate command validity, executed effects, prediction correctness, revision after feedback and durable reuse. Retain all raw outputs. The goal is to see which interface the existing model can actually use, not to search for attractive prose. Existing context and arithmetic failures make an immediate long rich-world run a weak first test.

**Conditional next: a versioned continuous-world season.** Only after usable action expression and host restoration are demonstrated, introduce optional seeds and longer visits. Preserve old season and history; label any transition explicitly. Do not silently replace the model, disable its adapter or import prototype outputs into the primary.

**Lateral directions:** bounded rule-composition recipes; an optional tested-skill shelf; state-tracking data for independent probes; or a small TextWorldExpress comparative baseline. These are queued possibilities, not prerequisites for the first workshop.

Confidence is high that 3D graphics are unnecessary and that persistence/explicit mechanics are feasible. Confidence is moderate in this minimal architecture's suitability. Confidence remains low-to-unknown that the fixed current model will spontaneously undertake sustained projects, discover reliable rules or improve through interaction. Continuing a world, retaining external memory and updating weights are different mechanisms.

## Observation without crowding

Retain every action receipt and before/after state outside chat. Report calm periods in aggregates; zoom in on actual construction, revisits, prediction errors, repairs, loops, resource depletion or rule conflicts. Keep a small predeclared uniform sample too, so event-triggered attention does not erase ordinary failures. Repetition, novelty, verbosity and self-reported confidence are descriptive signals, not proof of understanding.

Useful questions are: did a choice alter state; did a later choice use that consequence; did feedback change a retry; could a recipe be repeated under its stated conditions; did an artifact persist across process restart; what came from the model versus menus, seeds, retrieved recipes or host assistance? No single score is proposed as universal growth.

## Preservation and limitations

The primary study's 1,504 non-bytecode file hashes were captured before record updates and compared afterward; see [preservation](PRIMARY_PRESERVATION.json). No primary verifier was rerun, so 0096 remains the current pointer. The prior runtime-recovery unknown and unavailable interrupted-session post-digest remain unknown; literature research does not repair that historical gap.

Earlier navigation bytes are retained in `before/`; earlier reports remain intact. This is a focused scout, not an exhaustive literature review or a reproduction of any published score. No package is described as installed, no dataset as loaded, no proposed environment as activated, and no hypothetical model behavior as observed.
