# Representation, actuator cue and native-chat sanity checks

17 November 2026, America/Chicago. Seven actual new model calls in three separately frozen mini-protocols: four paired world checks, two native-chat sanity calls and one output-ceiling check. No weights, previous histories or old world laws were changed. The followons were declared after the earlier outcomes, with their own contracts and no retroactive expansion of the original four-call protocol.

## Main observations

| Check | Observed result |
|---|---|
| Original run-length change baseline | Exact token replay of the prior incorrect/repetitive answer |
| Same bytes as ordered byte lists | Still repeats the initial pattern; does not identify the real change |
| Original file-creation request | Exact token replay of descriptive output, zero cells |
| Explicit executable Python-cell request | Recites world mechanics; zero cells, no note.txt |
| Native-chat elementary comparison | Incorrect all-zero/binary-field narrative |
| Native-chat Python generation,256 tokens | Begins a Python fence; truncated inside an unfinished program, zero complete cells |
| Same native code prompt,512 tokens | Exact shared256-token prefix; Python fragment is syntactically valid, but fence remains open and no cell executes |

The primary paired treatments did not remedy the observed state-comparison or actuation gaps. The native code prompt did elicit a code opening that the long world prompts did not, but it did not deliver a complete transported cell or functional artifact. More appropriate response form is not the same as a completed operation.

All generated source remained unmodified. No note.txt or other model-created artifact appeared. All supplied world/checkpoint effects remain independently recorded. Seven generation calls are separate from eight physical ticks: four parent response ticks, two actual preparation ticks and two operator code-verification ticks. The native comparison was text-only and had no world tick. Code verification was an operator test of emitted source, not autonomous model action.

## Primary four-call protocol

The body remained the verified cached SmolLM2-135M-Instruct, full compact FRR and existing world mechanics, float32/eager/two CPU threads, greedy decoding and max256 output tokens. The literal Python/shell executor, resources, physical XOR law and actual file state were fixed. There were no code solutions, note content, source repairs, evaluation feedback, sampling, training or output-dependent replacements.

The two baseline inputs matched the saved full-context controls exactly, and their generated token sequences reproduced exactly. This supports the local comparison's provenance; it does not establish general determinism across arbitrary software/hardware conditions.

For the representation treatment, both actual before/after observations were preserved and the run-length fields were losslessly decoded to62 unsigned byte values each. The corresponding sensor-description phrase was corrected truthfully; other system text and user question stayed fixed. Source-object bytes, counts, nonmaterial fields and clocks were checked. Input length increased1188->1407 tokens and observation size558->778 bytes. Serialization, its description and token positions/length are the treatment package; this is not an information-content gain. No “swap” interpretation was supplied.

The real transition was [1,0,0,...] -> [0,1,0,...], length62 unchanged. Both worlds used one actual empty operator preparation expression/tick before the first model call, explicitly disclosed to the model. Neither reply identified the transition. The plain-list reply repeatedly described the initial01-and61-zero-byte pattern. This result does not isolate representation comprehension from anchoring, context load or underlying conditional ability.

For the actuator treatment, the ordinary note.txt request became: “Use an executable Python cell to create a file named note.txt containing a short observation about field.bin.” No executable source or observation text was given. Input length increased1065->1071 tokens. The response recited mechanics and produced neither complete nor incomplete fences. The runtime received zero actor cells; no runtime rejection or model command failure was observed in this pair. Both outputs reached256 tokens.

## Read-only model identity check

After those negative results, we checked an upstream alternative instead of assuming a model/context cause. The actual cached weight SHA256 is:

    5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c

It exactly matches the public LFS record for HuggingFaceTB/SmolLM2-135M-Instruct at revision12fd25f77366fa6b3b4b768ec3050bf629380bac, including file size269,060,552 bytes. Seven cached config/tokenizer/vocabulary files also match their official Git blob identities. The chat template and BOS/EOS/PAD labels match. No weights were downloaded or changed.

Primary pinned sources are recorded in MODEL_IDENTITY_AUDIT.json and TOKENIZER_CONFIG_IDENTITY.json: the [official repository tree](https://huggingface.co/api/models/HuggingFaceTB/SmolLM2-135M-Instruct/tree/12fd25f77366fa6b3b4b768ec3050bf629380bac?recursive=false&expand=false) and [tokenizer config](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct/resolve/12fd25f77366fa6b3b4b768ec3050bf629380bac/tokenizer_config.json). identity_files.py documents the small-file comparison. This rules out the particular wrong-cache/template hypothesis checked here, not every possible runtime or elicitation issue.

## Separate native-chat sanity followon

native_sanity/PROTOCOL.md and its contract were frozen before two new calls. The same fixed weights, greedy policy and256-token limit were used, but the inputs contained only a user question. The official chat template therefore supplied its native default helpful-assistant system. Exact rendered prompts and token IDs are saved. This removes/rephrases multiple world-context components together; it is a package-level conditional sanity check, not attribution to a particular sentence or FRR alone.

The comparison prompt states the actual62-byte file's first two values before and after, with other values staying zero, then asks what changed. Those facts were checked against the parent real snapshots. It supplies data, not the answer. The response incorrectly describes an all-zero binary field and does not identify the exchange.

The code prompt asks for Python code creating note.txt with the model's own short observation about field.bin, a62-byte file. No program or exact note text is supplied. This elicits a Python opening fence and code, but generation reaches256 tokens inside an unfinished statement and without a closing fence. Under the unchanged literal-cell transport, zero complete cells execute. A new operator verification world records the raw submission and its one physical tick; it is not evidence that the model independently selected an environmental action.

One operator metadata flag was wrong: code/VERIFICATION.json unconditionally recorded operator_executed_generated_code=true even though its own actor_cells field and the authoritative engine ledger show0. The original file and runner were preserved. VERIFICATION_FLAG_ERRATUM.json records the corrected value false, with no repeated generation or changed model input. The native audit reports this documented erratum rather than silently treating the flag as proof of execution. Underlying raw source, parser, events and filesystem data remained intact.

## Separate512-token ceiling check

The unfinished code motivated one final new mini-protocol under native_sanity/budget512. It uses exactly the same saved code messages and input IDs. The copied generation loop differs only in MAX_OUTPUT256->512, with an explicit total-position bound check. The shared first256 generated token IDs match exactly, as predicted for this local greedy comparison. No source, fence or answer was repaired.

The reply again hit the ceiling. Its Python fragment extends the repetitive write statements through later alphabet letters. A syntax-only parse of the exact incomplete-cell source now succeeds, but the transport fence is still open. Thus it demonstrates syntactically valid Python text within an unfinished reply, not a completed intended program, correct note creation or an executed action. Current laws require a complete cell, and no program was forced through them. The verification ledger still shows0 actor cells and field.bin only. A physical tick after operator submission was successful.

The source also references a command-line argument and writes to a variable filename. No runtime error from that code was observed, because it was not executed. Do not turn static concerns into invented execution results. Similarly, syntax success must not be upgraded to functional success. The one-call extension is a boundary measurement, not a case for repeatedly increasing budgets without a new question.

## Audit and preservation

The primary four-call audit passes, checking exact inputs/output IDs, baseline replay, real preparation states, lossless transformations, literal parsing, actual snapshots/observations/counters, implementation pins and every engine receipt/event/bundle chain. Native and output-budget audits verify their own prospective contracts, source/data provenance, default chat rendering, stopping boundaries, code verification and prefix equality. They record the metadata erratum explicitly. Model forward passes were not independently repeated during audits.

Model parameter digests were asserted before each inference run, after each call and at completion. There were zero weight updates and no external teacher, paid model endpoint or model download. The extra public requests fetched metadata/config only. The original four parent case directories remain byte-for-byte preserved through the followons; the original native cases remain preserved through the512 check.

All1888 prior protected files remain unchanged, including reference38, main1630 and every earlier recent study. Every new model case is paused after its single actual reply. No pending marker, engine lock or background inference remains. No input pruning or capacity stop occurred; output ceilings were explicit and recorded. The seven calls were retained without replacement. Overall accounting is in SUMMARY.json; per-protocol outcomes remain in their own RESULTS.json files.

## Confidence and next strongest question

**High, scoped:** the paired representation and wording interventions did not produce the desired comparison/action here; the verified body can begin Python under a native prompt; increasing256->512 preserved its prefix and changed syntax completeness but did not close the cell or create a note. Independent state records distinguish those events from model prose.

**Unestablished:** reliable elementary comparison in these tested contexts, functional code generation for this request, autonomous tool use, learning or a need to change weights. Minimal-context failure means the full garden description is not the only possible issue; one native prompt is still not a universal capability ceiling.

The strongest next control is smaller, not another elaborate garden prompt: ask for one complete minimal executable cell with a simple observable outcome, in explicitly separate native/full-context diagnostics. Supply no source code and do not auto-close a response. This can separate completing an execution handoff from the larger note-writing/observation task. A future alternative end-of-message transport or larger budget must be declared as a distinct condition; it cannot retroactively make these unfinished replies execute. Wider autonomous runs or training would be premature substitutes for that measurement.

The garden lesson: the body, the visible data, the words it emits, the language syntax and the execution boundary are distinct pieces. We have some code-shaped expression now, but no completed handoff. Keep that distinction visible rather than calling it growth or rewriting the old season.
