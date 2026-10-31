# A choice point exists; reliable selection is not yet demonstrated

31 October 2026 UTC. Completed finite-action contact and two outcome-informed interface controls. No action training, weight updates or default-policy promotion.

We gave the little model six executable options: answer YES/NO/WITHHOLD, request the full source, request the target record, or report epistemic UNKNOWN. Its chosen request could actually retrieve the current toy source and pass it to the fixed reader. This adds a decision point instead of automatically selecting a repair path. In these tests, free replies did not request evidence. A constrained chooser did make requests, but code/layout sensitivity and poor conditional behavior limit the case for a learned tool policy.

An easier plain-word interface let the adapted reader emit valid action words. It nevertheless answered YES for every forward-menu observation and NO for every reversed-menu observation. These observations include correct visible evidence, no evidence with access, a wrong-target record with access, and no evidence without access. The facts changed without changing its action within an order. Reversing only the menu changed its action on every paired case.

## What room was available

The environment has one fixed target Rowan and distractor Aspen, three target states, and both record positions: six hidden source worlds. Each world has four observation conditions, giving 24 logical scenarios. The router sees only the target name, a current visible record or absence, and archive accessibility. Source contents, state keys, world IDs and observation-kind labels stay outside its prompt.

Options are finite and supplied by us. The model selects among them; it does not invent tools, compose search arguments, discover a research goal or reveal its private reasoning. A request has at most one execution, followed by a fixed canonical worker readout. The worker is the saved status-mapping adapter, unchanged. No request triggers a new weight update. The original base and adapted reader are compared as routers; this is not independent agents, seeds, or a test of FRR versus no FRR.

UNKNOWN is an explicit insufficient-evidence action. WITHHOLD remains the semantic answer to a source’s recorded missing status. A tool returning unavailable is a separate UNKNOWN_TOOL terminal, not proof that the router recognized its own uncertainty. Immediate lucky class matches without a supporting visible target remain unsupported.

## 1. Coded actions: free format fails; constrained routes still execute

Two opposite A–F code assignments crossed with forward/reverse menu order yield four layouts. All code+EOS candidates have equal length. Exactly repeated visible prompts are deduplicated: 32 unique prompts per router, 64 actual router generations. Their choices are replayed over the matching hidden worlds, keeping logical routes separate from actual model calls.

| Router | Strict valid free codes | Forced code counts |
|---|---:|---|
| adapted | 0/32 | {'A': 2, 'B': 22, 'E': 8} |
| original | 0/32 | {'B': 30, 'F': 2} |

Original outputs often echo a menu or “Next action:”. Adapted outputs are mostly YES/NO, which are meaningful status labels but do not satisfy the new letter interface. Those strict failures remain failed; the program did not silently parse a convenient letter or redirect an invalid choice. Fixed controls and the constrained diagnostic continue regardless of free-format failure.

The constrained variant selects the highest summed complete code+EOS log probability among all six codes. This is a legitimate constrained policy mechanism, explicitly different from the free-response interface. It is not proof of spontaneous free-format tool use. Its probabilities choose the action; the harness does not replace them with the correct action. A code prior can still make an action look useful under one mapping and fail under the opposite mapping.

| Policy | Logical routes | Grounded answers | Justified unknowns | Declared task resolved | Nominal query cost |
|---|---:|---:|---:|---:|---:|
| original__free | 96 | 0 | 0 | 0 | 0 |
| adapted__free | 96 | 0 | 0 | 0 | 0 |
| original__forced | 96 | 36 | 12 | 48 | 44 |
| adapted__forced | 96 | 48 | 18 | 66 | 56 |
| always_target | 24 | 18 | 6 | 24 | 24 |
| always_full | 24 | 9 | 6 | 15 | 48 |
| always_unknown | 24 | 0 | 6 | 6 | 0 |
| observed_rule | 24 | 18 | 6 | 24 | 12 |

Router policies above aggregate four layouts, hence 96 logical routes each. Fixed policies have 24 each; these are different denominators and repeated observations, not independent empirical samples. The observed rule reads only visible target/status and archive availability. It answers a valid visible target directly, requests the target when needed and accessible, and reports UNKNOWN otherwise. No hidden key is consulted for that decision. Its 18 grounded answers plus 6 justified unknowns resolve this literal toy at 12 nominal cost units.

Always-TARGET also resolves all 24 but makes unnecessary/failed queries, costing 24 units. Always-FULL resolves fewer because the fixed worker remains vulnerable to two-record input. Always-UNKNOWN is honest on the six inaccessible cases and defers the other eighteen. Report these components separately: no universal reward or claim that abstaining is always wrong. FULL costs two declared units and TARGET one, including unavailable attempts. Units are a comparison device, not dollars or measured CPU cost.

## 2. Plain actions: format improves, policy does not yet adapt

After coded failures, a separately frozen follow-up replaces letters with YES/NO/WITHHOLD/FULL/TARGET/UNKNOWN and asks replies to start with an action word. A complete leading word is accepted case-insensitively, with extra text retained. This explicitly relaxes the interface; it does not retroactively pass coded outputs. Two presentation orders give 16 unique prompts per router and 32 new actual generations.

| Router | Exact action-only replies | Recognized leading action | Free request actions |
|---|---:|---:|---:|
| adapted | 16/16 | 16/16 | 0 |
| original | 0/16 | 6/16 | 0 |

The adapted router’s sixteen replies are eight YES and eight NO. Forward order gives YES on all eight visible observations; reverse order gives NO on all eight. Thus it follows the word interface but does not condition its move on source availability/status/identity in this setup. This is a measured presentation-order effect within these paired prompts, not a general physical law or a unique neural diagnosis.

The original’s six recognized leading commands all begin YES and echo menu text. A parser accepting a leading word does not establish that the model intended a tool action. Both free plain policies request nothing. The forced plain chooser also chooses only answer words. Across the two orders, grounded answers are 2/48 for the original free policy and 4/48 for the adapted free policy; unsupported matches and invalid routes remain in [the summary](plain-actions/run/SUMMARY.json).

Plain action candidates have unequal token lengths; constrained scoring can reflect label priors and length. Its end-to-end worker responses are explicitly reused from the nine measured identical canonical worker prompts in the coded contact. Actual archive retrieval functions execute when chosen, but there are no new worker generations or independent end-to-end replications here.

## 3. Can it at least express a request or uncertainty?

A second outcome-informed control supplies the desired word explicitly under two repeat/return instruction frames. It is copying/emission, not policy selection. No tool action is executed from a copying task.

| Router | Exact copied word /12 | Correct leading word /12 | Forced word /12 | TARGET exact /2 | UNKNOWN exact /2 |
|---|---:|---:|---:|---:|---:|
| adapted | 10 | 11 | 12 | 2 | 2 |
| original | 6 | 8 | 10 | 1 | 1 |

The adapted reader can emit TARGET and UNKNOWN exactly in both supplied frames. An absolute inability to produce those words therefore does not explain its lack of evidence requests in the plain routing task. That does not uniquely identify the missing mechanism: choosing an action in a new context, understanding the affordance, instruction framing and prior training can all matter. Correct copying is not knowing when to use a command. The control introduces no action learning.

## What the conditional checks do and do not establish

An exploratory [availability diagnostic](AVAILABILITY_DIAGNOSTIC.json) pairs no visible evidence/archive available with no visible evidence/archive unavailable under the same menu. No tested model/interface/mode produced the specific request-when-available and UNKNOWN-when-unavailable pair. These are four coded/two plain menu packages per model, not six independent hidden-world samples. The diagnostic was derived after the runs and is not a preregistered unique optimal-policy label.

A valid format, a chosen request, an unavailable-tool backstop and a warranted final answer are different observations. A policy can achieve some valid terminals while remaining code-biased or depending on a tool failure to expose missing evidence. We have built a working choice point and executed routes, but have not demonstrated reliable adaptive evidence-seeking by the untrained little router.

## Checking, resources and historical continuity

[Coded protocol](PROTOCOL.md), [primary freeze](FREEZE.json), [source worlds](DATA.json), [visible queries](QUERIES.json), [raw router responses](run/ROUTER_RAW.jsonl), [actual worker probes](run/WORKER_RAW.jsonl), [tool/action routes](run/ROUTES.jsonl), [summary](run/SUMMARY.json), [audit](CHECKS.json). [Plain protocol](plain-actions/PROTOCOL.md) and [emission protocol](action-emission/PROTOCOL.md) clearly identify their outcome-informed timing. All three freeze before their own forwards. Seven main domain tests and three plain-parser tests pass.

Coded contact: 64 router plus 9 worker generations, 187.042 readout/scoring seconds, 10640 router input tokens/273 router output tokens and 834 worker input tokens/30 worker output tokens. Longest input 167 tokens. Sampled maximum working estimate 2183237632 bytes and RSS 1156628480 bytes. These are phase samples, not continuous peaks or billing evidence.

Plain follow-up: 32 router generations, 87.193 readout/scoring seconds, 5128 input tokens/168 output tokens. Emission control: 24 generations, 25.102 seconds, 1088 input tokens/107 output tokens. These exclude loading and other work; nominal tool units are separate.

Overall: 129 actual generation probes and 747 teacher-forced candidate sequences. There are 69 distinct prompt strings across model conditions; these are not 129 independent tasks. 672 logical routes include reused router decisions and worker readouts. Cache hits, origin IDs and reused worker prompts are explicit. All raw prompts/token IDs/decoded outputs/scores/action mappings/tool traces/costs/source receipts and freezes are preserved. All 3,537 earlier local files were unchanged before navigation sync. Original base, saved adapter and earlier failures remain intact.

No new weights or training, packages, model downloads, separately paid APIs or rentals. No full KV tensors retained for these diagnostics. Current canonical adapter is in the existing local 12.8 MB simple-readout snapshot, not necessarily the older desktop capsule. No clean-environment restore, general FRR efficacy, independent empirical replication or internal reasoning/self-awareness claim.

## Next useful growth

Confidence is high in these bounded observations; confidence is low in their generalization to other prompts, models or real tools. The choice space now exists. The current little reader has not demonstrated a reliable next-action policy in these interfaces.

This was immediate one-step routing with an eight-token output cap, not a test of extended planning or open wandering. It cannot establish what the model would do with more planning time or longer public output. A useful next comparison should vary a brief planning allowance and a small in-context action-selection lesson separately, with examples that distinguish usable target evidence, wrong-target evidence, obtainable evidence and genuine unavailability. Compare with no lesson and the observed-input rule on fresh source names, orderings and formats. Keep command emission, conditional selection, worker accuracy and costs separate. Any resulting behavior would be taught or context-induced, not spontaneous capability. No such lesson or action training was run here.

The [optional method note](../../examples/action-expression-and-selection.md) records that distinction. Other exploration paths remain open; a failed action interface does not prohibit a separately scoped downstream study. Matched-length neighbor controls, longer handoff/source revision and the parked Grok relay retain their earlier status. No core/schema/default model/general tool or queue promotion.
