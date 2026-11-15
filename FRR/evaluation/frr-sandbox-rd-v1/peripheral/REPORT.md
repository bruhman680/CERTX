# Peripheral scout: open exploration still has mechanisms

Read14 November2026, America/Chicago. Bounded three-source primary-literature scout; zero model calls, sandbox actions, installs or external code execution. The main garden was not opened or changed. Two versioned papers were read in selected HTML sections; one older paper was accessible only through its institutional abstract. This is a methodological contact, not a reproduction or full literature review.

## Three useful contrasts

**Lehman and Stanley, Abandoning Objectives: Evolution Through the Search for Novelty Alone (2011).** The institutional abstract describes evolutionary search driven by behavioral novelty rather than progress toward a final task objective, with maze and locomotion experiments. It explicitly presents an alternative means of guiding search. This does not describe a system with no selection pressure. Full-text access failed in this scout, so technical details of its novelty metric, archive update rules and experimental implementation are not promoted to independently checked facts. [Institutional record](https://stars.library.ucf.edu/facultybib2010/1530/), [publication DOI](https://doi.org/10.1162/EVCO_a_00025).

**Forestier et al., Intrinsically Motivated Goal Exploration Processes with Automatic Curriculum Learning,1708.02190v3.** The architecture represents goals as parameterized fitness functions, selects experiments through a goal policy, updates policies from outcomes, and reuses experience across goals. Its experimental intrinsic reward measures competence progress; modular object/temporal representations are explicit design choices. Reported exploration coverage counts reached bins in chosen outcome spaces. No particular final target is supplied, but learning machinery and the representation of possible goals are supplied. This differs from merely exposing a fixed-weight language model to a world. [Versioned paper, §§2,3,4.3.1](https://arxiv.org/html/1708.02190v3).

**Burda et al., Large-Scale Study of Curiosity-Driven Learning,1808.04355v1.** Curiosity is an implemented prediction-error reward, paired with PPO policy training and selected observation features. The authors remove episode-end information in their pure-exploration setting because such signals can reveal task structure. They also demonstrate attraction to uncontrollable stochastic changes: novelty/surprise can grow without useful control. Thus, no extrinsic task reward does not mean no optimization objective, and a varying observation stream is not sufficient evidence of useful learning. [Versioned paper, §§2,2.2–2.3,5](https://arxiv.org/html/1808.04355v1).

## What transfers to our experiment without importing their objectives

The following are our methodological inferences, not results those papers established for SmolLM2-135M or FRR:

1. **Separate observer descriptions from agent drives.** We can measure effect diversity outside the world without returning a novelty score or selecting the model's next actions by it. Installing a curiosity reward, a goal-sampling curriculum or optimizer would create a different condition and should not be hidden inside an FRR prompt comparison.
2. **A behavior descriptor is a scientific choice.** In our existing world, every literal notebook append changes file bytes and the world hash. Fifty identical replies can therefore produce fifty distinct world states. Raw hash diversity would misleadingly call automatic storage growth exploration. Preserve those hashes, but report automatic note operations separately from model-initiated cells, non-note effects and any later reuse. A notebook deliberately changed by a model cell belongs in the latter action record as well; do not discard it because its pathname is notebook.txt.
3. **Observation is an exposure condition.** A new file or changing hidden resource only affects generation if some information about it reaches the model. Record what was available in the world separately from what was supplied or demonstrably accessed. Do not add unannounced sensory summaries to make a branch more interesting.
4. **Stops and resets belong in the experimental description.** Operational time budgets and integrity pauses need not become goal-related feedback. A completion flag, reset or success signal returned to the model may supply information even without a numerical reward. Keep actual resource/error consequences, but do not add a semantic success gate to the open world.
5. **Novelty, controllability and retention are different.** Unfamiliar words or changing states may be noise, automatic recording or a genuine new operation. Repeatedly accessing and using a model-created artifact supports a different claim from merely creating it once. No single diversity count should stand in for all of these observations.

## Strongest small contribution to the first pilot

Keep the proposed matched no-FRR/FRR comparison free of new reward/training mechanisms. In external readout, retain at least three separate channels: literal automatic notebook storage; model-originated executable attempts and their actual effects; and evidence of later access/reuse. Mark repair as not elicited when a branch never encounters an actual error followed by another opportunity, rather than inventing a failure to force that category.

The immediate primary question remains whether the declared FRR context changes observed trajectories under matched mechanics. These peripheral papers explain why open-ended systems often require explicit mechanisms; they do not establish that a prompt supplies those mechanisms or that lack of change proves the pretrained model incapable.

## Access and scope

SOURCES.json records exact URLs, versions, selected read depth and failed access attempts. No benchmark numbers were replicated, no code was inspected or executed, and no cited learning mechanism was added to the model. Results on neuroevolution, robotics or PPO agents are contrasts, not direct evidence for this fixed-weight language-model body.
