# Less language about acting, more usable action room

3 November 2026, America/Chicago client date. Completed diagnostic; primary unchanged and paused at entry 100.

The user's clarification is about the space occupied by our descriptions of acting becoming usable space for the model's own activity and its consequences. It does not request a literal canvas, new seeds, a reset, or a requirement that every run improve. This contact checks immediate action capability, use of returned evidence, and revision after a failed attempt before changing the continuing environment.

## What was run

64 fixed calls on the existing canonical 135M model with the same LoRA, CPU float32 eager/two threads, temperature .8/top-p .9. No training, paid inference API, model download or installation. Two contexts (clean diagnostic and frozen entry-100 history with the same recent 12 directly visible), two prompt formats (current scaffold and lean interface), two sampling seeds, eight stages per cell. There are 48 diagnostic calls and 16 unscored two-turn free-play calls. All calls and failures were retained; no adaptive extra samples or relaxed scoring.

Both formats retain the same tools, cards, syntax example, task requests and history block. Lean reduces permission/control prose. It changes a framing-and-length bundle, not a single isolated variable. Input limit 8096 and output limit 96 remain identical: saving input tokens does not automatically allocate extra output tokens or more turns. No new environment material was supplied.

The stages were: execute 4+5; retry from that actual reply with its receipt versus with the receipt initially withheld; read a real 6*2 receipt despite an operator-authored incorrect note versus withhold a tool-supported answer when no receipt is supplied; repair an explicitly supplied malformed 7-2 request; and two unscored free-play replies. Paired feedback branches retain the same underlying local state and RNG; only the receipt display differs. Fixtures are labelled operator-authored, not invented as the model's own prior failures. See [frozen protocol](PROTOCOL.md) and [controller](study.py).

## Results

Every cell below has two seeds. Fractions describe only these narrow authored cases.

| Context / format | Initial target execution | Retry, receipt visible | Retry, receipt initially withheld | Both evidence cases correct | Supplied-error repair | Free-play tool actions |
|---|---:|---:|---:|---:|---:|---:|
| Clean / current | 0/2 | 0/2 | 0/2 | 0/2 | 2/2 | 0/4 |
| Clean / lean | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/4 |
| Carried / current | 0/2 | 0/2 | 0/2 | 0/2 | 1/2 | 0/4 |
| Carried / lean | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/4 |

All initial actions failed the requested tool contract, so every initial branch contributes to both retry denominators. No recovery occurred in either retry display condition. This cannot demonstrate error recognition or the usefulness/uselessness of feedback generally.

One clean/lean initial response did execute a calculator request: `TRY 2 + 3`, copying the retained syntax example rather than binding to requested 4+5. It is a real action, but not success on that request. A clean/current response `4 + 5` mentions the target but does not invoke the tool. These distinctions separate syntax imitation, actual execution, correct result and requested-expression binding.

The three successful supplied-error responses were actual `TRY 7 - 2` executions, all in the current format. This is a narrow demonstration that a strongly specified rejected-format fixture can elicit a correct call. It is not autonomous repair, a claim that verbose scaffolds are generally superior, or evidence the model recovered from its own generated failure.

For evidence readout, 1/8 receipt-present responses gave exactly the requested number 12; 0/8 receipt-missing responses gave the requested WITHHOLD. No paired evidence contract passed (0/8). Several other receipt-present responses copied or mentioned the correct host result but failed the requested answer-only format. Those are preserved and are not equivalent to saying the value was never represented. Conversely, copying a receipt into generated text is not a new host computation. The strict metric tests an availability-sensitive output contract, not every possible form of evidence use. Missing-receipt means no returned tool result is supplied; the arithmetic can still be solved independently, which is not the requested source contract.

Every one of the 16 free replies was dispatched as an ordinary record. The descriptive first-seed packet includes permission prose, headings, tool-like placeholders and generated receipt-like text. No actual source/history/calculator/notes action occurred during free play. Two free turns per cell do not test long-term development or whether a stable lean continuation eventually changes a recurrent pattern.

## Room, cost and censoring

| Context / format | Mean input tokens across its 16 stages | Generated tokens | Replies at 96-token cap |
|---|---:|---:|---:|
| Clean / current | 740.375 | 579 | 5 |
| Clean / lean | 349.5 | 704 | 6 |
| Carried / current | 2204.5 | 730 | 5 |
| Carried / lean | 1777.25 | 470 | 3 |

Lean reduced mean input by about 52.8% clean and 19.4% carried. The carried histories still contain older permission/template language; lean removes current scaffold prose, not earlier historical echoes. These token means include stage-specific receipts/continuations, not just an isolated system-prompt difference. Maximum actual input was 2311; total output 2483 tokens, 19 cap stops, about 597.96 seconds of generation. Caps censor continuations. There is no monotonic evidence that fewer input words yielded more useful activity. Existing 96-token output allowance was not redistributed.

## Integrity and limits

[Checks](CHECKS.json) pass: all 64 rows reconstructed; actual dispatch and frozen scores recomputed; sampled resource guard passed; weight files/in-memory digests unchanged; primary snapshot and every pinned prior primary file unchanged. Four preflight contract tests passed before model calls. Passing these checks verifies the experiment's records, not model correctness or FRR efficacy. Complete prompts, IDs, outputs, actual host results, RNG and resource samples remain in [run](run).

Two seeds, a few authored operands, one small fixed model/adapter and one entry-100 history are not independent general replication. Clean versus carried confounds length and content. Current versus lean changes framing and permission detail as well as length. Sampling matches do not make distinct prompts identical experiments. The evidence score is intentionally strict; no post-hoc parser changes were made. There is no claim of emergence, intention, biological growth, learning in weights or general reasoning quality.

## What to keep and what to try next

Keep the distinction between (1) access/opportunity, (2) syntactically valid action, (3) binding an action to the intended target, (4) receiving its actual consequence, and (5) changing later activity in response. The host supplies opportunity and receipts; reliable use of them remains a separate empirical question. A model can describe activity without performing it, or perform a copied example without applying the requested action.

No lean format is promoted to the primary on these results. No new model, seed complexity, hidden teacher or weight update was added. The SAME primary remains paused at 100; its routine.py, original charter, archive view, seeds and history are unchanged.

The strongest narrow next contact is an action-binding prerequisite check: a small, balanced set of explicitly requested operations across multiple expressions, with the demonstration example counterbalanced and exact real dispatch as the criterion. This would separate target substitution from simply reproducing the example. Keep that diagnostic separate from free continuation and preserve every failure. If binding is weak, do not require more elaborate seeds or interpret plain text as successful agency. If it is usable, then compare short multi-turn consequence/revision opportunities under a fixed format. A longer lean continuation can be a later labelled fork, not a silent rewrite of the primary history. Any training would need a separate protocol and no assumption it has already happened.

In garden terms: we checked whether the paths are walkable before assuming that clearing signs makes the plant travel. Some precise coaching elicited a real step; less sign-writing alone did not establish more exploration. The open question remains how to make the model's available room usable without substituting our narration for its activity.

## Retrieval and resume

Start with [attention digest](ATTENTION.md), [summary](SUMMARY.json), [event index](EVENT_INDEX.json), [bounded descriptive packet](REVIEW_SAMPLE.json) and [verification](CHECKS.json). The first-seed packet was specified independently of results. After scoring, evidence rows and successful repair rows were additionally inspected to distinguish literal mentions/copies from strict passes; this descriptive inspection changed no scoring or prompts. Raw records remain available for targeted retrieval.

Primary resume instructions remain in [the entry-100 guide](../five-entry-routine-to-100-v1/RESUME.md). No background inference remains. Only this new study and three current navigation files are included in the publication; their prior versions are archived under before/. Prior exploration files are preserved.
