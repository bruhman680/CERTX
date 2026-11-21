# Language garden design proposal

20 November 2026, America/Chicago. Planning draft. No new small-model world, inference run, parameter update or automatic scheduler has been activated.

The proposed garden gives the existing pretrained model a persistent space for language and symbols. Its purpose is to observe expression, continuity, revision and possible transfer while preserving errors and freedom to leave questions unresolved. The recent computational garden and every completed experiment remain separate historical systems.

## Purpose and working hypothesis

Candidate seed, preserved from the user discussion:

> Explore symbols and their relationships. Learn to predict and understand them as best you can.

This is an invitation, not a requirement to solve a puzzle, demonstrate progress, narrate an inner state or follow a reasoning checklist. The model already has pretrained linguistic structure; this is not a blank learner acquiring language from scratch.

The user's broad intuition remains an originating research idea, not a claim refuted by the scope of our first design. A testable starting hypothesis is that experience with relationships in one symbolic setting can support useful behavior in another setting that preserves some of those relationships. Generalization to arbitrary other systems is not established. We should ask which structure transfers, which evidence is available, and which changes defeat the transfer. Prediction, coherent narration, record recall and parameter learning remain distinct observations.

## Recommended first world

Use an append-only authored text record. Writing has a real mechanical effect: new text is retained and can become part of subsequent input. It does not automatically make its propositions externally true. The model may invent, contradict, speculate, revise or write a story without a semantic approver deciding whether its contribution enters history.

The durable record contains original contributions with author, order, branch identity and links where available. These fields are host bookkeeping, not a required response template. The model need not tag every sentence, produce JSON, explain its choices or use code fences. Fictional characters and quoted voices remain part of their actual author's text. A revision adds a record; it does not erase what was previously written. No semantic compiler translates prose into a canonical physical world.

This is a genuine inscription space with observable history. It is not yet an independently evolving simulated universe. If future questions require consequences independent of narration, add a separately disclosed minimal symbolic substrate or external observation stream. That is a distinct design decision and intervention, not a hidden narrator deciding what becomes true.

## What belongs to the world and what belongs to observation

World mechanics concern persistence, actual available context, scheduling and physical resource bounds. Research annotations concern what we think a passage means. Keep the latter outside model-facing conversation unless an explicitly planned feedback contact supplies particular evidence.

An observer may record a quoted span as a claim about earlier text, a fictional event, a hypothetical, a prediction or unresolved. Those are provisional interpretations and may overlap. An imagined moon eating a key is not automatically a factual error. A claim that a particular earlier message contained those words can be checked against the record. Incompatible statements need matched entity/time/frame before being called a contradiction.

Record-integrity audits verify bytes, order, authorship and accessible input. They do not certify truth or understanding. Narrative follow-through on an outcome the model itself authors is different from successful prediction against an independently determined outcome. Append order, exact retrieval and link existence are already possible structural consequences, though success there would support archive literacy rather than a broad discovery claim.

## Continuity and context

Durable history, model-visible input and model parameters are separate carriers. Saving the whole record does not make every old passage present in attention. Save each exact rendered input and its selection policy alongside the full history.

For an initial observation window, prefer a small enough run to include every earlier contribution without summaries, retrieval, discarded turns or context replacement. Measure the complete native-template input, seed, author metadata, host cues and prior outputs, reserving the explicit generation allowance within the supported total context. Pause before the next call cannot fit; raw prose length alone is not the input budget. This makes continuity inspectable and avoids adding a memory-management system before its need is observed. A later recall interface, omission policy, summary or independently revisitable branch must be specified as a new mechanism and evaluated for this body's ability to use it.

A causal language model still requires host calls and input assembly. A repeated cue such as “Continue.” is a host-authored intervention, not spontaneous autonomous time. The exact turn-advance cue and stop handling must be fixed and disclosed before a pilot. EOS normally ends an instruction-model reply; it is not by itself evidence of a chosen rest. Empty output, an expressed stop and a host budget pause must not be merged into one behavioral interpretation.

## Model and FRR placement

The reference body remains SmolLM2-135M-Instruct with its existing instruction-tuning and native assistant template. The compact FRR runtime is currently guidance for the research team, not a hidden change in that body's weights or runtime. The proposed symbol seed does not itself implement gradient learning.

For a first language pilot, the simplest candidate uses the native framing plus the candidate seed. Adding full/compact/fragment FRR text to the small model would be an explicitly labeled comparison, not a silently assumed upgrade. Short English exposure motivates an accessible interface; it does not establish superiority over code, long narrative competence or autonomous exploration.

## Learning path

First investigate fixed-weight, context-supported behavior in a persistent record. Observe whether earlier material is used, revised, echoed, ignored or transformed. Preserve tutorials, repetition, contradictions and failures without automatically redesigning the world in response to an early pattern.

Actual parameter or adapter training is a later, separate experiment. It requires provenance-tagged examples, an objective, gradients, optimizer steps and saved changed tensors. Preserve the entire exploratory record independently of which examples might later enter training. Keep an original checkpoint/no-update comparator and test fresh-context retention, transfer and degradation. CPU feasibility and useful training throughput remain unmeasured. Self-generated statements are not independent evidence for their own correctness.

## Possible later contacts

These are optional researcher investigations, not obligations or progression gates for the inhabitant:

- Accessible-history versus omitted-history continuations can test whether a relation's use depends on supplied records. Keep original history preserved; withholding in a detached control is not deletion of the primary garden.
- A target using new symbols but the same operation structure can test bounded representation robustness. A near-target changing exactly one operation challenges rigid copying. Target evidence must reveal the changed operation before asking for a new consequence.
- A later true training comparison can distinguish changed-parameter retention from active context, retrieval, caches and environmental persistence.

Predeclare each contact separately after natural observations identify a consequential question. Record offered, accepted, declined and uninterpretable contacts separately. Nonparticipation is not an ability failure; unequal participation can leave comparisons unresolved. Repeatedly selecting prompts against the same hidden answer does not supply held-out transfer evidence.

## Open decisions before a runnable blueprint

1. Is the authored text record sufficient as the first world, or is an independently changing symbolic substrate essential from the start? Recommendation: record first, with its limits explicit.
2. What exact turn-advance cue and stop behavior will make host participation visible? A candidate must be inspected before activation.
3. What short observation window and output bound allow complete history to remain visible? A small fixed window is an operational budget, not a developmental law or deadline for improvement.
4. Where does FRR enter the small-model comparison, if at all? Recommendation: keep researcher guidance and resident-model context separately declared.

The proposed first artifact after this design review is a minimal blueprint specifying those mechanics and a frozen observational window. The present documents are not an executable world or authorization inferred for a particular training run.
