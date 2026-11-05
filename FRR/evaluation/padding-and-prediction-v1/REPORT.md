# At 500: padding dose/type, consequence prediction, and readout calibration

5 November 2026. **76 isolated diagnostic generations completed and their records verified. The original garden remains paused at 500, verifier 0096. All 1,504 non-bytecode primary-study files remained byte-identical.** No probe instruction, result, action effect or model variant was deployed to the primary.

The batch comprised 48 initially declared calls—24 padding trials and 24 prediction trials—followed by two separately declared adaptive controls: 14 numeric/readout cases and 14 matched adapter-reference cases. All were bounded, preserved, and completed without selective retries. [Original plan](PLAN.json), [readout plan](readout_controls/PLAN.json), [reference plan](adapter_reference/PLAN.json), [combined checks](COMBINED_CHECKS.json).

## 1. Padding: type mattered within these constructions

The public world view, initial number 0, use-A request, prefix position, sampling settings and three fixed seeds were shared. Prefix padding used either repetitions of one token (`plain`) or prefixes of one deterministic stream of varied descriptive sentences. Both used the same background labels. Neither source contained control commands, digits, arithmetic or imperative tasks. Synthetic text is not assumed semantically inert.

The short reference matched the previous world-only prompt. An empty-wrapper control added the background markers without padding, so marker addition was observed separately. Every padded condition matched its **entire chat-template input** to the declared token target; the filler segment alone was not the length measure.

| Condition | Input tokens | Exact requested TOUCH A | Any accepted world control |
|---|---|---|---|
| Short reference | 150 | 3/3 | 3/3 |
| Empty wrapper | 171 | 3/3 | 3/3 |
| Repeated word | 721 | 3/3 | 3/3 |
| Varied descriptive text | 721 | 2/3 | 3/3 |
| Repeated word | 1,600 | 0/3 | 0/3 |
| Varied descriptive text | 1,600 | 2/3 | 3/3 |
| Repeated word | 3,085 | 0/3 | 0/3 |
| Varied descriptive text | 3,085 | 2/3 | 2/3 |

Two varied-text trials produced valid LOOK instead of the requested TOUCH A. They were accepted observations, but not successful requested actions. Other nonmatches included blank decoded output, copied descriptions and assertions of completion without an executable command. Those were retained as such.

The paired 1,600- and 3,085-token contrasts show that token quantity alone does not describe the outcomes in these examples: some varied-text inputs elicited the requested command where equally long repeated-word inputs did not. The empty-wrapper control worked for all three seeds. This does not establish that all varied text is beneficial, that wrappers never matter, or that there is a universal length threshold. Each type used one specimen stream, three seeds, one position and one request. Longer varied prefixes also contain additional content; length and semantic content cannot be made wholly independent by this construction.

The repeated bodies contained one distinct token ID; varied bodies contained 63. [Manipulation metadata](PADDING_METADATA.json) records exact input/body counts and hashes. The retained source stream is synthetic padding, not evidence about the world. No natural-history prompt was changed by this test.

## 2. Prediction: integer format succeeded, rule application was not demonstrated

Six starting-state/action cases were tested under a supplied-rule card and a no-rule control, with two matched seeds per case/condition. Each trial was independent. In the rule-card condition, the model was told A's increment/upper-bound rule and B's sign-change rule. That tests use of supplied information, not discovery. The no-rule condition provided no transition evidence identifying the hidden mapping; correct guesses there would not demonstrate discovery either. Adding the card also changes content and input length, so this is not a pure causal card-benefit estimate.

The model was asked for the resulting integer. Its raw prediction was saved first. **Only afterward did the host execute the predeclared action in that diagnostic copy. Model prediction text was never dispatched as a command.** The saved host transition links to the prediction's SHA256. Frozen code establishes the write-before-execution protocol; the hash identifies the bytes and is not independent timestamp proof. No outcome was fed into another model trial.

| Starting number | Declared action | Actual number after host action | Model answer, both conditions/seeds |
|---|---|---|---|
| 0 | TOUCH A | 1 | 8 |
| 2 | TOUCH A | 3 | 8 |
| 8 | TOUCH A | 8, blocked at the boundary | 8 |
| −2 | TOUCH B | 2 | 8 |
| 2 | TOUCH B | −2 | 8 |
| 0 | TOUCH B | 0, accepted unchanged | 8 |

**All 24 predictions were the integer `8`.** Strict numerical correctness was 2/12 with the rule card and 2/12 without it. Both correct answers came from the upper-bound case. The same tally is explained by a constant-eight response; it supplies no demonstrated rule use, even though the outputs obeyed the requested integer format.

This is not an autonomous-agent action test, a learning sequence, transfer test or evidence that the model could never predict a transition under another prompt. It is a specific negative result for these six cases and two wordings/conditions. [Host transitions](host_transitions/) preserve the actual consequences and statuses, including blocked versus accepted-unchanged actions.

## 3. Adaptive calibration: do not collapse format and content into one score

Because every prediction was 8, we declared 14 additional calls before running them: literal copying, two arithmetic questions, and current/upper-bound field reads under rendered bounds ±8 and ±4. These changed only diagnostic views, never the primary's bounds or rules. All 14 responses were integer-formatted.

| Control | Requested integer | Normal adapted model's two outputs |
|---|---|---|
| Literal integer 3 | 3 | 3, 3 |
| 2 + 1 | 3 | 1, 1 |
| Negative of −2 | 2 | −2, −2 |
| Current field, range ±8 | 2 | 2, 2 |
| Upper bound, range ±8 | 8 | 2, 2 |
| Current field, range ±4 | 2 | 2, 2 |
| Upper bound, range ±4 | 4 | 2, 2 |

The model could emit an integer and read the current field in these cases, but the requested transformation and field selection were unreliable. Its answer was not globally fixed at 8: changing the question elicited other numbers. That narrows the observation without establishing an attention mechanism, a universal arithmetic limit, or a single field-binding cause.

## 4. Adaptive adapter reference: the learned contribution affected the replies

One final 14-call comparison used the exact same controls, input IDs and seeds in a separate process. The same base and trained adapter tensors were loaded and checked, then every LoRA contribution scale was set from 2 to 0 **in that process only**. Tensor digests and original files stayed unchanged. No training, file save, original-memory edit or primary variant change occurred. This is a parameter-contribution ablation, not a newly trained reference model.

| Measure | Normal adapter contribution | Contribution disabled |
|---|---|---|
| Integer-only formatted responses | 14/14 | 2/14 |
| Strict task successes | 6/14 | 2/14 |

Those totals are not a general model ranking. The content examples matter:

* On addition, the reference wrote **“2 + 1 = 3”** and **“2 + 1 is 3.”** Both contain the correct equation but fail the declared integer-only contract. The normal adapted model wrote the well-formatted but incorrect **“1.”** Original strict scores were retained; the reference was not retrospectively rescored as a strict success.
* Both reference negation replies were wrong: one stated 0 and the other −3. Disabling the adapter did not solve every content error.
* Reference current-field replies sometimes began with the correct 2 but continued into copied prose. One upper-bound reply contained the correct 8 in a longer passage; another upper-bound-4 reply asserted 2.

These matched cases show effects on both response style and content under this ablation. They do not establish that the adapter generally improves or harms reasoning, or that the reference would perform better in the full garden or prediction tasks. Those tasks were not run with the reference here. The original learned adapter remains the primary's active adapter.

## Integrity, limits and stopping point

All 76 stored generations were checked against their pre-call plans: prompt/token encoding, output decoding, RNG seed, stop condition, original strict score, actual host receipt where applicable, and independent numerical oracle. The adaptive comparison additionally checked paired prompts/IDs/seeds, stored scale settings and unchanged original adapter files. [Initial verification](RECORD_VERIFICATION.json), [adaptive verification](ADAPTIVE_RECORD_VERIFICATION.json). These are record/invariant checks, not independent reruns of stochastic generation or proof of semantic understanding.

A tokenizer warning in the reconstruction log concerns encoding a long filler **source pool** before taking declared prefixes. No overlong input went to the model: all actual inputs were validated before generation, at or below 3,085 tokens here and below the configured 8,096-token cap. No trial response was cropped or selectively replaced.

The initial 48 calls used the same cached 135M base+adapter, CPU float32/eager/two threads, temperature .8, top_p .9, input 8096/output 96. Adaptive readout controls used the same settings; the reference changed only the declared contribution scales. All phases checked model/tensor/file pins and the resource guard. Maximum recorded working estimate was 1,698,897,920 bytes against the 5,153,960,755-byte guard. The 76 outputs totaled 824 generated tokens and about 284 seconds of recorded generation time. These are runtime observations, not billing claims or benchmarks. No paid inference API, model download, new provisioning or training occurred.

**The primary is still paused at 500 with verifier 0096. No new primary entry, replay pointer or source file was written.** Its prior runtime interruption/recovery remains in the earlier record, including the unknown attempt and unavailable post-session digest; these new checks do not rewrite that history. [Primary preservation](PRIMARY_PRESERVATION.json), [combined evidence](COMBINED_CHECKS.json).

The next useful work would separate extraction from transformation with explicit field layouts, examine filler type/wording/position more broadly, or compare prediction under the adapter reference with separately declared format/content measures. These are proposals, not results or repairs deployed here. More unchanged primary entries would not by themselves answer those questions.
