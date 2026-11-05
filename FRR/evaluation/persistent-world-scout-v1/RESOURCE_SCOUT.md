# Persistent text world resource scout

Research date: 2026-11-05. Scope: primary source inspection only. No environment was installed, launched, adopted or activated; no model inference, model download, paid API call, or mutation of the paused `source-access-three-cycle-v1/cycle3/environment` was performed. The fixed local 135M model and prior adapter are outside this scout's scope. GitHub sources were read through the GitHub connector; Hugging Face cards were opened through the web connector. External documentation was treated as evidence, not operating instructions.

## Decision

**Best small text-native starting point: TextWorldExpress. Best existing tending simulator: ScienceWorld. Best construction rules to adapt: Crafter.** None of the inspected packages is already a durable, freely editable, text-only garden/workshop world. Task environments preserve state during an episode; that is different from a world that survives process restarts and continues after a goal is achieved.

For the user's desired long-lived world, the lowest-complexity adoption direction is a small local object graph/state machine borrowing the *design patterns* below: explicit bounded actions, visible preconditions and costs, placement/crafting rules, ticking plant state, and versioned state plus an action log. This is a recommendation for a future build, not an implementation or activation. If adopting an existing runtime is preferred, start with TextWorldExpress for a small comparative baseline, or ScienceWorld if growing/mixing/testing matter more than minimal dependencies.

| Resource | Strong fit | Main gap | CPU/dependencies | Recommendation |
|---|---|---|---|---|
| TextWorldExpress | Text, small room graph, enumerated valid actions, replay persistence API | Episodic tasks; no general build/tend vocabulary | Scala/JVM + Python/Py4J; bundled JAR listed at ~1.69 MB | First executable baseline |
| ScienceWorld | Object graph, plant life stages, chemistry/electrical interaction, valid actions | More complex task simulator; persistent sandbox wrapper needed | Scala/JVM + Python/Py4J | Richer tending alternative |
| Crafter | Material placement, plant placement, explicit resource/crafting graph | Image-first, survival randomness; text and persistence adapters needed | Python, NumPy, Pillow, imageio, opensimplex, ruamel.yaml | Best rules source for construction |
| DiscoveryWorld | Python object graph, scientific interaction, object UUIDs and ticks | Rendering/assets and scenarios add overhead | pygame/pathfinding/NumPy; requirements also include OpenAI-related agent libraries | Defer for this constrained task |
| HF task/state cards | Reproducible seed/task selection and state-tracking probes | Data does not execute world transitions | Small metadata/cards; simulator required for interactive task list | Optional evaluation material only |

CPU suitability is an architectural assessment, not a measured benchmark on this workspace. No inference capability or success rate of the fixed 135M model is established by this research.

## 1. TextWorldExpress — strongest lightweight text-native baseline

Identity: official `cognitiveailab/TextWorldExpress`, Apache-2.0 according to repository metadata. Metadata reports `archived=false`, default branch `main`, last push 2025-08-25. Repository update time is not used as evidence of code maintenance.

Inspected in full: [README](https://github.com/cognitiveailab/TextWorldExpress/blob/main/README.md), [Python API](https://github.com/cognitiveailab/TextWorldExpress/blob/main/textworld_express/textworld_express.py), [FastObject.scala](https://github.com/cognitiveailab/TextWorldExpress/blob/main/simulator/src/main/scala/textworldexpress/objects/FastObject.scala), [setup.py](https://github.com/cognitiveailab/TextWorldExpress/blob/main/setup.py). Also inspected package and Scala directory listings; the package listing gives the bundled JAR size without downloading it. License classification was checked in repository metadata, not a legal audit of all files.

Concrete capabilities:

- `load(gameName, gameParams)`, `reset(seed, gameFold, generateGoldPath=False)`, `step(action)` and `infos['validActions']` expose a finite grounded action interface. Small `twc` clean-up games can be limited to one room/two objects; CookingWorld has bounded room, ingredient and distractor counts.
- `getObjectTree()` exposes internal ground truth. `FastObject` has container backreferences, contents, openability/movability flags and food preparation state. `Room` has explicit north/south/east/west links. This is directly inspectable object graph logic rather than an LLM pretending to simulate a world.
- The actual Python API implements `serialize()`, `deserialize()` and `clone()`. Serialization stores game, parameters, seed/fold and actions; deserialization regenerates the episode and replays actions. This is **replay reconstruction**, not an arbitrary graph snapshot. Pin the code/JAR and record explicit seeds for replay; avoid relying on `seed=None`.
- Optional gold paths are generated from hand-authored agents. The README cautions that these may be wandering paths, not shortest paths. Arithmetic, sorting and map-reading variants offer optional puzzles.

Documented reproduction, for a future separately authorized trial: Java 1.8 and `pip install textworld-express`; instantiate `TextWorldExpressEnv(envStepLimit=...)`, load `twc` with `numLocations=1,numItemsToPutAway=2,includeDoors=0`, then reset with an explicit seed/fold. Source changes require Scala/sbt build work, rather than merely changing Python.

Main limit: `step` marks done on score success, task failure or step cap. Object classes such as garden/workbench in the source do not prove an agent can garden or construct arbitrary objects: the implemented game/action rules define that boundary. Building/tending and continuing beyond goals require explicit new transitions and termination policy. Do not use the precrawled-path mode here: README examples warn of large trees, minutes/hours of preparation, finite horizons and up to ~1 GB per seed.

## 2. ScienceWorld — best existing plant/chemistry world

Identity: official `allenai/ScienceWorld`, Apache-2.0 per repository metadata; `archived=false`, `main`, last push 2026-08-20. An initial `cognitiveailab/ScienceWorld` lookup returned 404; the verified canonical source is the AllenAI repository.

Inspected in full: [README](https://github.com/allenai/ScienceWorld/blob/main/README.md), [Python API](https://github.com/allenai/ScienceWorld/blob/main/scienceworld/scienceworld.py), [Plant.scala](https://github.com/allenai/ScienceWorld/blob/main/simulator/src/main/scala/scienceworld/objects/livingthing/plant/Plant.scala). Inspected object and plant directory listings to locate the actual implementation. Metadata supplies the license classification.

The README lists 30 task families including grow-plant, grow-fruit, chemistry mixing, melting/freezing, circuits and Mendelian genetics. The actual plant implementation advances a lifecycle on `tick`; flowers reject self-pollen/wrong-species pollen and form fruit after enough ticks. This supplies real tending consequences, not narrative-only descriptions. Exact watering/growth preconditions live deeper in lifecycle/property code and were **not** exhaustively audited.

The API supplies `get_valid_action_object_combinations()`, versions with template/object IDs, referent lookups and `getObjectTree()`. It distinguishes possible combinations, which may include invalid actions, from valid combinations. `look()` and `inventory()` are free observations. A compact chooser can use grounded valid strings instead of requiring the small model to invent commands. The full object tree is an oracle inspection channel; decide explicitly which local observations the acting model receives.

Future reproduction: Java 1.8+, Python 3.8+, `pip install scienceworld`; load a named task and variation, then `reset()` and `step()`. Modifying Scala rules requires recompiling the packaged JAR with the documented build script/sbt. No installation was attempted. Keep one world instance alive and add persistence/replay deliberately; run-history export is not itself a restore API.

Critical version caveat: current README warns that 1.3.0 introduces deterministic UUID enumeration across resets/JVM versions, fixing stochastic outcomes but potentially changing physics trajectories, ambiguous command resolution, gold paths and ordering relative to 1.2.x. Pin package/JAR version; do not mix old HF task/trajectory assumptions with new runtime outcomes silently. Also the `easy` preset includes `selfWateringFlowerPots`, which removes part of the tending problem. Leave that simplification off for a meaningful garden. Existing tasks are a richer but still bounded simulator, not unrestricted creation.

An upstream-linked [HF Space card](https://huggingface.co/spaces/MarcCote/ScienceWorld/blob/main/README.md) was actually inspected: Apache-2.0, Streamlit 1.10.0, `app.py`, and page status “Running” at research time. It is a demo, not a checkpoint or durable local persistence system. No interactive session was started.

## 3. Crafter — clearest construction/crafting rules

Identity: official `danijar/crafter`; MIT confirmed by [LICENSE](https://github.com/danijar/crafter/blob/main/LICENSE). Metadata reports `archived=false`, last push 2024-01-23. README labels it “Stable release”; that does not establish active maintenance.

Inspected in full: [README](https://github.com/danijar/crafter/blob/main/README.md), [data.yaml](https://github.com/danijar/crafter/blob/main/crafter/data.yaml), [env.py](https://github.com/danijar/crafter/blob/main/crafter/env.py), [constants.py](https://github.com/danijar/crafter/blob/main/crafter/constants.py), [setup.py](https://github.com/danijar/crafter/blob/main/setup.py), and license. `setup.py` identifies version 1.8.3 and runtime dependencies; an attempted `requirements.txt` lookup was absent.

This is a 2D survival world, not natively text-only. Its YAML is unusually useful for a small transparent world: 17 actions; bounded inventory; gather rules and required tools; placement costs/allowed terrain; crafting costs and nearby-workstation requirements. Examples verified in YAML: a table consumes two wood; a furnace consumes four stone; a plant consumes a sapling on grass; an iron pickaxe needs wood, coal and iron near table and furnace. This is effective construction within known bounds.

`Env.step` returns `info` containing inventory, achievements, semantic map and player position. A text adapter could serialize local symbolic information and map action labels to indices, with visible affordances/preconditions. That adapter does not currently exist in the inspected source. The engine still renders the ordinary image observation every reset/step through `_obs()`; a genuinely text-only fork would bypass that work explicitly.

Future reproduction: `pip install crafter`; direct `crafter.Env(...)` or Gym interface. pygame is optional for GUI; NumPy/imageio/Pillow/opensimplex/ruamel.yaml are runtime requirements. Default world is 64×64, episode limit 10,000; `length=0` disables the time limit in inspected code, but death still ends an episode. The seed is combined with episode counter on reset, so record both or reconstruct the same reset sequence. Random drops/creatures are inspectable stochastic rules, not intrinsically deterministic transitions. No durable save/load API was found in `env.py`; capturing RNG, world objects and player state needs additional work. Peaceful tending would require an intentional rules variant.

## 4. DiscoveryWorld — rich Python object graphs, excessive overhead here

Identity: official `allenai/discoveryworld`, Apache-2.0 code, `archived=false`, last push 2025-03-10. README explicitly excludes commercial CuteRPG art assets from the Apache license and asks derivative projects to support the artist; do not treat the asset pack as Apache-licensed code.

Inspected in full: [README](https://github.com/allenai/discoveryworld/blob/main/README.md), [DiscoveryWorldAPI.py](https://github.com/allenai/discoveryworld/blob/main/discoveryworld/DiscoveryWorldAPI.py), [ActionHistory.py](https://github.com/allenai/discoveryworld/blob/main/discoveryworld/ActionHistory.py), [Object.py](https://github.com/allenai/discoveryworld/blob/main/discoveryworld/objects/Object.py), [requirements.txt](https://github.com/allenai/discoveryworld/blob/main/requirements.txt). Object source inspection included attributes, container/parts links, tick recursion and `to_dict()`; export does not establish a corresponding restore mechanism.

`loadScenario(name,difficulty,randomSeed,...)` builds a seeded scenario. `listKnownActions()` documents actions; commands are JSON such as `USE` with object UUID arguments. Pickup/put/open/activate/read/use and directional movement are explicit. The world advances with a separate `tick()`; `performAgentAction()` prevents an agent from acting twice before ticking. Object attributes include temperature, mixtures, living state and soil nutrients. This is a strong reference for structured object interaction.

However `getAgentObservation()` unconditionally renders both grid/no-grid views, saves PNGs, encodes vision images and also returns UI JSON. Merely ignoring `vision` does not remove rendering, assets or disk writes. Its headless window still uses pygame. Requirements include pygame, pathfinding, NumPy and OpenAI/tiktoken libraries for the broader agent stack; no paid API is needed conceptually for simulator rules, but no minimal dependency split was verified.

Future reproduction should follow the README's clone/install and API examples in an isolated working directory, using a custom local action provider and explicit `tick()`. Text-only extraction and durable restore need engineering first. Also source review found `getActionDescriptions(limited=True)` pops names whose entries are already commented out, a plausible `KeyError`; this was not run. Prefer ordinary enumeration until verified. This is not the first adoption for the small CPU-only world.

## 5. Actual Hugging Face contribution — seeds and probes, not a simulator

### Portable ScienceWorld task seeds

Actually read the [SeanWang0027/scienceworld-tcod-split dataset card](https://huggingface.co/datasets/SeanWang0027/scienceworld-tcod-split), schema and visible rows. The card declares Apache-2.0 and 3,602 task descriptors (2,294 train, 1,308 test), about 473 kB. Each `task_desc` is JSON with `task_name`, `var_num`, and blank `jar_path`; `targe` is intentionally empty. This is a community task list, not trajectories or an executable environment. The installed ScienceWorld package/JVM generates transitions. It offers concrete reproducible starting situations, including plant tasks, without downloading model weights.

Future use: load the dataset, parse a descriptor, and pass its task/variation into ScienceWorld. Pin dataset revision and simulator version. The card reports validation against ScienceWorld 1.2.3; current upstream determinism changes require separate checking. Its whole-task-type split differs from official within-task variation splits and has no dev split. Use seeds for scenario selection, not as proof of persistent sandbox quality. No dataset payload was downloaded.

### State-tracking probe material

Actually read the [keenanpepper/textworld-state-tracking card](https://huggingface.co/datasets/keenanpepper/textworld-state-tracking) and viewer schema/examples. MIT card; 27,145 examples (24,076 train, 3,069 dev), with context, entity, positive_state and negative_state. Useful only as optional object-state consistency probes; it cannot execute actions or persist a world. Card claims only 13 entities and open/closed/eaten properties, with average context about 2,850 words: excessive for the desired compact controller. Viewer counts also differ from some card claims, so audit before evaluation use. Future loading via the HF datasets library should pin a revision and use held-out traces; no training or loading was performed.

## Additional triage and remaining gaps

[AgentGym README](https://github.com/WooooDyy/AgentGym/blob/main/README.md) was read: it supplies HTTP wrappers (`createEnv`, observation, available_actions, step, reset) around existing environments and lists TextCraft/ScienceWorld/BabyAI. This adds orchestration, not durable world semantics; avoid adopting the full training/server stack for one tiny local world. Its TextCraft subdirectory README was inspected, but only documents an install and HTTP launch, insufficient to recommend its rules. [ADaPT](https://github.com/archiki/ADaPT) metadata/root listing confirms a MIT repository containing `TextCraft`; source/action rules were not audited in this pass. This is a follow-up candidate, not a verified adoption choice. Craftax and MiniGrid text adapters were not audited, so no capability claims are made for them.

Before any future adoption, the concrete unresolved requirements are: process-restart persistence; continuing after milestones; an explicit finite create/place/tend action set; regeneration/resource conservation rules; compact observation/delta formatting; separation of world inspection from acting observations; and version-pinned deterministic replay checks. Enumerating grounded actions can reduce command syntax errors but does not establish that the 135M model can plan or choose well. A future smoke trial can use a scripted chooser first and evaluate the fixed model only under separately authorized inference limits.

Only this report was written by this scout. All runtime and compatibility assertions above come from source inspection, not local execution.
