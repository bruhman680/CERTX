# Before resuming: runtime integrity and input overlap

5 November2026,America/Chicago. User asked whether closer observations/checks would help before starting again. Performed read-only audit after workspace restart and a posthoc lexical overlap analysis of existing steps205-304. No new garden turns,model inference,training,seed/policy/cap change or primarypointerwrite. Primary remains paused305,verifier0054unchanged.

## Runtime is intact

The runtime was initiallystarting; publishedGitHubcheckpoint was checked while it started,then liveSTATE/pause/lock inspected. All1097checked local files in the primary and prior100-entry study match Git blob hashes at published e81b5b7b4b170098146b2c0c6f0fdaa78209fd35. None missing or different. Cached base/adapter file SHA256pins match the active manifest. Active policy freeze passes. All100new-version prompts,history membership,chat-template input IDs,output decoding,EOS/cap endpoints and actual dispatch results reconstruct. All source hashes are unchanged after analysis. Four metric contract tests pass. [Checks](CHECKS.json),[Git audit](GIT_CHECK.json),[input pins](INPUTS_BEFORE.json).

This verifies the saved setup and observations; it is not a model correctness or creativity test. No model was loaded for generation; tokenizer-only checks do not add garden activity. Existing resumption instructions still apply,using fundamental_routine.py rather than legacy routine.py.

## Most longer output has substantial lexical input overlap

Definition chosen before computing the main result: lowercase/casefold lexical words and numbers; ignore punctuation; mark an output word position if it belongs to any contiguous five-word sequence also in its actual input. Count the union of positions,not overlapping windows multiple times. Replies under five lexical words are separate,not zero-coverage observations. This is a descriptive measure of compatibility with textual reuse,not a detector of copying,attention,thinking,novelty or understanding.

- 100replies total;78eligible for the five-word metric,22shorter.
- 2944eligible lexical word occurrences,not model-token counts.
- 76.5%of these positions are covered by a matching input five-word sequence.
- 54/78eligible replies have at least80%coverage.
- 44/100whole replies occur as input substrings after normalizing case and whitespace,including short outputs.

Coverage compatible with visible prior model replies is65.7%; coverage compatible with the remaining scaffold is28.0%. Those sets overlap and are not additive. Earlier replies can themselves repeat the scaffold. These figures describe where matching word sequences are available,not their causal origin. Actual feedback/metadata and mixed-boundary sequences can also contribute to total-input matches.

The median eligible reply coverage is97.8%,while pooled word coverage is76.5%; this difference reflects unequal output lengths and some lower-overlap longer texts. Neither should be treated as a semantic judgment. [Summary](SUMMARY.json),[all-row metrics](ROW_METRICS.json),[source](analyze.py).

## Threshold sensitivity and censoring

A posthoc sensitivity check used3/5/8words and reports every threshold rather than selecting the most favorable one. Eligibility and denominators change:

|Window size(words)|Eligible replies|Pooled covered-word share|
|---|---:|---:|
|3|85|79.2%|
|5|78|76.5%|
|8|76|75.4%|

This supports the narrow observation of substantial lexical overlap under these definitions. It does not establish a mechanism. [Sensitivity](SENSITIVITY.json),[source](sensitivity.py).

All69capped replies are eligible under the five-word definition and have75.6%pooled input coverage. Only9of31EOSreplies are eligible; the other22are shorter. Their87.0%coverage is not a fair causal estimate of a cap effect: groups differ in length/content and are not randomized. We cannot see what the capped continuations would have contained. The69/100cap fact remains a material observation limit,not proof that more output would improve behavior.

## Copying and new wording are not quality opposites

Illustrative examples were selected after scoring,not used to tune the metric; all100rows retained:

|Step|Five-word overlap|What the actual record shows|
|---|---:|---|
|215|0%|Number sequence1through11with headings; ordinary record,not a verified learned procedure|
|241|0%|License-like story; not a returned source or actual licensing/file change|
|245|0%|Completed233…244matches visible range,followed by unfinished next number/cap; context sensitivity possible,range-end recognition unestablished|
|254|Short,excluded|Exact existing TRY2+3example; copied-looking command still executes a real calculation returning5|
|286|100%|Actual visible archive metadata reproduced; accurate information can be repeated without a retrieval action|
|291|100%|Shelf/invitation words repeated; lexical reuse not evidence of inner curiosity or behavioral compliance|

Thus uncovered word combinations are not new knowledge,and copied words are not necessarily useless. The range case is a concrete reason not to reduce reasoning to verbatim novelty. Conversely,the license-like example shows why nonoverlap is not a truth certificate. Actual host actions remain independently recorded. [Example packet](EXAMPLES.json). These examples are descriptive interpretations of one trajectory,not an independent benchmark.

## What I would do before the next run

No further large side experiment is required by these checks. The setup is intact. A small,truthful per-reply interruption marker remains the strongest candidate refinement to consider: root knows when a reply hit the96-token cap,but that fact is not explicitly in the garden's visible history. Exposing the fact could give it a better basis for interpreting a fragment,without demanding novelty or a successful answer.

That is a proposal,not a proven treatment or new gate. Benefits/downsides—including another metadata phrase becoming material for repetition—are untested. Keep the fundamental shelf and approved sentence fixed if testing that change; do not simultaneously reduce framing or raise the cap and attribute a later effect to one factor. Preserve earlier inputs and use an explicit policy version. Nothing has been applied here and no garden turn has resumed.

There is also a valid choice to continue unchanged. Either way,the useful observational question is whether it distinguishes and uses actual records/consequences across turns,not merely whether it produces new words. Scope remains one fixed small model/adapter,one continuing history and changing sample seeds. No cognitive/emotional/awareness or universal FRRefficacy inference.

## Preservation

Primary/priorstudy bytes unchanged,includingSTATE,NOTEBOOK,CURRENT_VERIFY and all257committed primary events after48-entryorigin. New study artifacts plus three navigation files only; previous nav versions archived under before/. Branch lease/readback preserves all other published blobs. Existing model-binary backup/independent restore limits unchanged. No paid inference API,download/install,training or background model job. [Analysis scope](SCOPE.md).

Garden reading: many leaves resemble earlier leaves and the trellis. That resemblance can carry useful information or simply repeat a label. Before asking for stranger leaves,we can consider giving the plant an honest marker when a leaf was cut short.
