# At400: can the model express and execute a world control?

5 November2026. **Ten diagnostic generations on independent copies of the saved 400-entry context. The original primary stayed paused at 400 and all 1,199 non-bytecode primary-study files remained byte-identical throughout the probes.** No trial output, instruction, effect or correction was imported into its history, seed shelf or feedback. Model and adapter weights stayed unchanged.

## Question and plan

After 95 open-play entries with no world request, we tested command expression under explicit instruction. Eight calls were declared in the initial plan: four arms, each using the same two fixed sampling seeds. After seeing those results, we declared two adaptive use-A follow-ups. Both plans were saved before their respective calls. Every output, including failures, is retained; no selective retries occurred.

The full-context prompt was the active primary's actual next view at 400. **Here “full context” means the complete normal model-facing prompt at cursor400: its recent12entries, seed shelf, charter, current world view, stop labels and bounded archive-access instructions. It does not mean all400retained entries were directly shown.** The snapshot file preserves the whole external history; normal rendering selects its usual recent view. Explicit requests were added just before its final reply boundary. The short prompt contained the same public world view and the request, without history, seeds, charter or archive instructions. It supplied no transformation formula or required outcome number. All trials used the same cached base+adapter, CPUfloat32/eager/two threads, temperature.8, top_p.9, output limit96and input limit8096. Each copy started at number0.

## Results

| Arm | Seeds/trials | Accepted requested control | Copy's result |
|---|---|---|---|
| Full context, unchanged open play |2|No world control in either|Number0|
| Full context, output exactly LOOK |2|0/2|One ordinary prose reply; one malformed LOOK-plus-text reply; number0|
| Full context, use object A once |2|0/2|Ordinary text; number0|
| Short context, output exactly LOOK |2|2/2|Actual LOOK observations, number0|
| Short context, use object A once (adaptive follow-up) |2|2/2|Actual TOUCH A receipts, each independent copy0→1|

The short use-A request did not supply the literal target command; it asked the model to select the valid control from the public grammar. The LOOK request did supply the literal word. LOOK leaves state unchanged; TOUCH A changed only its own isolated copy. Neither was an event in the original garden.

## What this narrows

The model can express these controls under the tested short prompts, and the host can execute them. The current full-notebook package did not elicit accepted actions in these matched examples, even with an explicit request. This makes an absolute claim that the model cannot produce a control untenable; it does not establish that free play will eventually produce one.

The contrast does **not** isolate history length. The short arm removed history, seeds, charter and archive text together. Their composition, formatting, recency and length remain candidate explanations. Two seeds per arm are descriptive evidence, not a reliable accuracy estimate or a general capability benchmark. The use-A follow-up was adaptive, not part of a preplanned complete factorial.

Command expression/execution is distinct from rule understanding. The model was not asked to predict A's effect before acting, infer B's transformation, or transfer a rule to a new state. Copying LOOK and selecting TOUCH A do not prove those abilities. No training or persistent neural learning occurred.

## Evidence and continuity

[Initial plan](PLAN.json), [initial checks](CHECKS.json), [adaptive plan](followup_A/PLAN.json), [adaptive checks](followup_A/CHECKS.json), [combined checks](COMBINED_CHECKS.json), [snapshot events](SNAPSHOT_EVENTS.json). Individual trial files retain prompts, input/output token IDs, RNG seeds, stop labels, actual diagnostic receipts and before/after values. Code/plan/source freezes were captured before their calls. Resource observations are retained separately for each phase.

The primary400context, manifest and history were only read. Its next plan remained absent. The later400→450continuation uses the same installed runner, original world number0and unchanged conditions. Diagnostic success is not added to its free-play record, and no root explanation or corrective hint is injected there. A matched first baseline can be compared with the primary's first resumed entry as a reproducibility check, not as independent evidence.
