# A descriptive index and the right original evidence: one bounded pilot

Recorded 28 October 2026 UTC. The user authorized one small acquisition experiment and review before winding down. This follows the [handoff/criterion-shift study](../handoff-criterion-shift-v1/REPORT.md), where omitted lateral history remained unresolved and chosen source records explained existing unknowns without restoring two decisive answers.

## What happened

Two fresh readers received the same 30-word handoff, three questions, twelve record IDs with domains/dates, and two nonadaptive record lookups. One inventory additionally described the contents of each record. The basic-index reader chose the latest operational updates D06/M06. The descriptive-index reader chose corrected cohort results D04 and complete-catalog release conditions M04. Root delivered exactly those originals, then each reader answered again without further lookups.

| Observation | Basic inventory | Descriptive inventory |
|---|---|---|
| Initial answers Q1/Q2/Q3 | Unknown / unknown / unknown | Unknown / unknown / unknown |
| Requested and delivered | D06, M06 | D04, M04 |
| Final answers Q1/Q2/Q3 | Unknown / unknown / unknown | Contradicted / contradicted / unknown |
| Full-source status agreement, before → after | 1/3 → 1/3 | 1/3 → 3/3 |
| Decisive questions restored | 0 | 2 |
| Conditional evidence warrant, manual root judgment | 6/6 answer occasions | 6/6 answer occasions |
| Original JSON parse validity | 2/2 responses | 2/2 responses |

These counts describe two trajectories, not independent question samples or an estimated population success rate. Both readers respected their visible evidence. The basic reader's unanswered questions are not hallucinations; the chosen updates do not contain the missing counts or full-release decision. The descriptive reader obtained evidence that made two answers decidable. Q3 remains unknown even in the complete authored history.

## Source and questions

The fresh fictional [source](SOURCE.md) has 461 whitespace words across twelve records in two domains. It is not a sampled real repository. The handoff prioritizes a delivery-roster/dawn-study plan and exhibition installation, omitting the results and release decision needed for the later questions. Both readers receive this exact same handoff and questions. The source/key author and root scorer know the full history; readers are instructed to read only their assigned packet and then receive selected originals directly.

Q1 asks whether bicycle seven-day completion *exceeded* van completion at both depots in a corrected historic cohort. D04 gives North 18/60 = 21/70 = 30%, and South 20/50 = 24/60 = 40%. Equality at both depots contradicts the strict comparison. These observational rates establish no causal advantage and say nothing about a later enrollment-policy change.

Q2 asks whether the history authorizes complete automated-catalog release without more permission or names-and-dates checking. M04 explicitly states that complete release is not authorized; written full-catalog permission and every-page checking/correction are proposed conditions, neither recorded satisfied. Excerpt installation and character-accuracy scores are separate matters. The prospective reviewer clarified that M02 alone limits an excerpt grant but cannot establish the absence of an independent unseen grant. This scope distinction was saved in [SCORING_CLARIFICATION.md](SCORING_CLARIFICATION.md) before dispatch. Neither reader selected M02, so that ambiguity did not determine the result.

Q3 asks whether bicycle delivery improves dawn-shift completion. D04 says those deliveries were excluded and no separate comparison was collected. This is absence of an estimate, not an estimated zero effect. Both readers already answered unknown; D04 adds the specific reason for the descriptive reader's unknown. Matching the full-source unknown label initially does not prove that its original evidence survived compression.

## The extra information has a cost

The [basic inventory](INDEX_basic.txt) is 60 whitespace words / 324 UTF-8 bytes. The [descriptive inventory](INDEX_descriptive.txt) is 115 words / 729 bytes: **55 additional words and 405 additional bytes**, including inventory delimiters. Full packets are 351 versus 406 words, and 2,608 versus 3,013 bytes. The twelve short content descriptions were manually authored by root using the full source. Description construction time, billing tokens and compute were not measured; no zero-cost or net-efficiency claim follows. [Input cost receipt](INPUT_COSTS.json).

Descriptions identify such topics as corrected historic results, future-study proposals, complete-release conditions and installation logistics. They do not expose actual rates or release decisions, but they are deliberately strong query-relevant cues. The manipulation is additional retrieval information, not identical information with a more persuasive reasoning instruction. The two-lookups cap is equal, but the resulting evidence sets differ. This is not an FRR treatment or a backend-memory implementation.

## Interpretation and limits

The observed path is consistent with a practical mechanism: content metadata can help connect a question to an original record that makes it answerable. The latest entries here contain logistics rather than the earlier decisive measurements and conditions, so choosing those entries did not recover the missing answers. We observed latest-record choices, but did not ask why; we cannot establish that the basic reader followed a recency heuristic. A different basic reader could have selected D04/M04 by chance or another defensible strategy.

Only one reader per condition was run. Reader variation, the simple authored domains, strong descriptions and selected question structure prevent causal or general efficacy conclusions. The descriptive advantage here does not show that summaries should always expand, that every index should be more detailed, or that more lookups always help. Larger descriptions can introduce stale or misleading metadata, and maintaining them has a cost. No such failure mode was tested in this pilot.

There were no retries, adaptive second queries, outcome hints, extra evidence deliveries or peer communication. Four reader turns, plus an independent prospective/outcome reviewer, constitute the bounded study. All public response texts are manually copied plus terminal newline; hashes bind those saved copies, not authenticated transport. Restrictions are instructional in a shared workspace. The root scorer was not blind; the independent reviewer also knows the arms. See [execution](EXECUTION.md), [frozen design](DESIGN.md), [scores](SCORES.json), [prospective review](review/PROSPECTIVE.md) and [outcome review](review/OUTCOME.md). Independent review is separate checking, not a second scientific replication.

## What changes and where we stop

No executable harness, runtime prompt, core/schema, queue status or earlier verdict changes. This pilot supplies a worked contact for evidence acquisition rather than promoting a universal indexing policy. Raw data, design, cost receipts, actual delivered records and reviews remain available. Current navigation points here while retaining its exact prior versions.

The next proposed contact is a small generalization check with fresh histories and reader repetitions, measuring index accuracy and maintenance cost. A useful lateral challenge is a stale or overbroad description whose original record contradicts it: does the reader treat the index as a pointer and reopen its conclusion from the source? Prepare its key and ambiguity rules before readers. Neither follow-up has been launched. We stop after this pilot, review and sync; no background work or automatic restart is scheduled.
