# Open-ended exploration scout

Research only; primary sources checked 2026-11-05. Scope: a bounded, potentially text-only world in which a fixed 135M+LoRA model can make and revisit lasting arrangements. Existing evidence of context-sensitive command expression does not establish planning, intrinsic motivation, general reasoning, or online weight learning.

## Five primary sources and what actually persists

### 1. Voyager — strongest external skill-memory pattern

[Wang et al., arXiv:2305.16291v2](https://arxiv.org/html/2305.16291v2), especially §§2.1–2.3, §3.3, Appendix A.1; [author project](https://voyager.minedojo.org/).

GPT-4 proposes tasks under an explicit diversity directive, using state and completed/failed tasks. A separate action-generation loop executes code, receives environment/interpreter feedback, and consults a GPT-4 success critic. Successful programs enter a retrievable, composable skill library. GPT-3.5 and embedding services also support the harness. Model weights remain unchanged: “lifelong learning” here is accumulated executable memory and in-context use of pretrained capability.

Continuity exists within exploration, but transfer evaluation explicitly clears inventory and starts a new world while retaining skills. Outcomes emphasize items, travel, tech milestones, and selected unseen tasks; they do not establish unrestricted construction, tending, or persistent attachment to an arrangement. Critic judgments are another model dependency.

**Text transfer:** store verified command recipes with preconditions and observed effects; retrieve a few relevant recipes. Do not assume the small model can synthesize JavaScript, compose recipes, judge success, or generate suitable goals merely because GPT-4 can.

### 2. DiscoveryWorld — strongest graphics-free causal feedback pattern

[Jansen et al., arXiv:2406.06769v1](https://arxiv.org/html/2406.06769v1), §§3.1–3.4, §§4.1–4.2, Appendix C.2; [official repository](https://github.com/allenai/discoveryworld).

The simulator supports text observations as JSON with object IDs, descriptions, inventory and interaction information; graphics are optional. Objects have measurable properties, and actions support experiments and consequential changes. Tasks are parametrically varied from authored themes and difficulty levels. An automatic scorer records completion and procedure; explanatory knowledge is also evaluated.

Published GPT-4o baseline evaluations are independent zero-shot task runs with no knowledge carryover. They are not continuous habitation or online weight training. Strong agents struggle despite planning and hypothesis-management scaffolds. Completion can be distinguished from having discovered an explanatory rule, a useful evaluation separation.

**Text transfer:** expose stable object identities, observable consequences, repeatable instruments and small causal puzzles. Borrow experimental affordances rather than the full scientific reasoning burden. A retained notebook would be external memory added by our design; it is not evidence that these baseline agents learn across persistent lives.

### 3. OMNI — curriculum selection is an external mechanism

[Zhang et al., arXiv:2306.01711v2](https://arxiv.org/html/2306.01711v2), §§3.1–3.3, §§4–5 and optimization appendices.

OMNI trains task-conditioned RL agents. A curriculum estimates changes in success probability and favors tasks with learning progress, including declining performance. A pretrained LM judges human-style interestingness from environment descriptions and prior mastery; its judgments downweight boring tasks. The LM selector and learned action policy are distinct components. Task rewards and policy optimization are explicit.

Its Crafter/BabyAI experiments support choosing among tasks using learnability and interestingness, not an agent's spontaneous wants. Episodic task training and measured success distributions do not demonstrate a continuously preserved personal world. An interestingness judge inherits pretrained human priors and its prompt's framing.

**Text transfer:** optional seeds can be varied using observed success and failure. For fixed weights, call any resulting statistic *performance change*, not evidence of policy learning. A designer or harness choosing seeds must remain visible in the attribution of agency.

### 4. OMNI-EPIC — archive and generated environments, with a major demonstration caveat

[Faldor et al., arXiv:2405.15568v3](https://arxiv.org/html/2405.15568v3), §§3.1–3.6, §§4–5, §6.

Foundation models generate tasks and environment code, including reset, reward and success functions. An archive retains successes and failures, providing stepping stones and novelty comparisons. Actual learning uses specialist DreamerV3 RL policies, initialized from a related successful policy for new tasks. Generated-code errors and failed learning feed revision loops.

The 200-iteration long run uses **simulated learning**: no RL training, assuming generated executable tasks are solvable. Separate shorter runs perform learning. Thus generation breadth is not evidence of equally broad acquired competence. The persistent unit is an archive of tasks, code and policies; environments reset rather than forming one enduring lived space. Generated reward and success functions also need semantic validation.

**Text transfer:** archive attempted projects, failures and reusable artifacts; suggest small variations near demonstrated abilities. Keep generation, executable validity, solvability and demonstrated completion as separate outcomes. Dynamically generating arbitrary code is unnecessary for a bounded text world.

### 5. AgentGym/AgentEvol — explicit weight-learning counterexample

[Xi et al., arXiv:2406.04151v1](https://arxiv.org/html/2406.04151v1), §§3–4.2, §5.1. This note specifically follows the June 2024 version; the later ACL title is “Evaluating and Training.”

AgentGym standardizes diverse instruction-driven environments and trajectories. AgentEvol first behaviorally clones expert trajectories, then alternates collecting environment interactions with reward-weighted supervised fine-tuning. The paper explicitly separates exploration/data collection from parameter optimization, retaining original/general data during learning. Its environment mix includes TextCraft and ScienceWorld.

This is actual weight change through an explicit training pipeline, not memory appearing because interaction continued. It depends on prior instruction-following ability, expert trajectories and reward signals. Cross-task benchmark success does not establish free play or continuity of a single world.

**Text transfer:** a consistent action/observation interface and complete trajectories aid evaluation. A future decision to train on those trajectories would be a distinct experiment. Fixed 135M+LoRA deployment does not instantiate AgentEvol.

## Design lessons for this model and intended world

These are proposed adaptations, not demonstrated capabilities of the present model:

- Preserve **world state**, **external notes/recipes**, **current prompt context**, and **model/adaptor weights** as four separately recorded things. Only the last is weight learning. World continuity alone can produce apparent progress because later actions encounter earlier artifacts.
- Make construction and tending first-class, ordinary actions: create a named arrangement, move or alter components, inspect its state later, repair or extend it. Persistent IDs and explicit state changes can support this without rendering. None of these papers directly validates meaningful long-term tending by a 135M model.
- Offer optional ideas/puzzles alongside an idle/inspect/create path. Log whether a project originated in user text, a seed, harness selection, or the model's own emitted action. Externally choosing each next objective can silently convert free exploration into a task curriculum.
- Prefer short, stable commands and immediate machine-derived feedback. Require no unverified natural-language explanation for an action to take effect. Introduce recipe retrieval only after measuring basic command use; retrieval and privileged harness repair can otherwise account for the apparent competence.
- Evaluate revisitation and modification of existing artifacts, persistence across context boundaries, repeatability, failure recovery, and behavior with seeds absent. Compare equal budgets with and without external notes, recipes and goal suggestions. Novel command strings, verbose plans or endless seed variation are weak evidence of constructive exploration.

The strongest supported proposition is architectural: lasting artifacts plus bounded actions, useful feedback and explicit external memory can make continuing interaction cumulative. Whether this particular fixed model can exploit those affordances is an empirical question. The papers provide mechanisms and cautionary comparisons, not evidence that persistence creates motivation or general learning.

## Reading and verification limits

Read the linked arXiv HTML methods and relevant evaluation passages directly, rather than relying on abstracts or social summaries; project/repository links were opened for provenance. No code execution, environment installation, model run, paid API call, or benchmark reproduction was performed. Voyager's reset/transfer distinction, DiscoveryWorld's no-carryover protocol, OMNI's separate selector/policy, OMNI-EPIC's simulated-versus-actual learning, and AgentEvol's explicit gradient-training step were checked in the source text. This is a focused mechanism scout, not an exhaustive literature review or independent validation of published scores.
