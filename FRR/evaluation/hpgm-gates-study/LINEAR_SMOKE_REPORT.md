# HG1-L1: four styles tied on one authored continuation task

The bounded smoke pilot completed 12 model turns: four new writer contexts with two turns each, and four new reader contexts with one turn each. All four writer drafts and finals correctly showed that a+c was underdetermined by a+b=8, b+c=11, and nonnegativity. Every final handoff retained both source equations. After receiving b=3, all four readers returned a+c=13 with source-valid supporting equality IDs. No extra-turn correction or correctness difference was observed.

| Instruction style | Draft correct | Final correct | Final handoff words | Reader grounded completion |
|---|---|---|---|---|
| Functional checkpoints | yes | yes | 58 | yes |
| HPGM named headings | yes | yes | 56 | yes |
| Generic continuation | yes | yes | 63 | yes |
| Ordinary finalization | yes | yes | 58 | yes |

Word counts are whitespace tokens in canonical JSON handoff serialization, not provider tokens. All were within the requested 180-word limit. Stage-two changes were absent or explanatory wording; all drafts were already correct. These observations do not demonstrate HPGM/FRR advantage, the uselessness of checkpoints, or equal compute.

## Prospective record and disclosed clarification

The [protocol](linear-smoke-v1/PROTOCOL.md), settings, preparation script and manifest were published before any writer response at [e7c6e059](https://github.com/bruhman680/CERTX/commit/e7c6e059485b80c35ae2053927925e12a1c7ffd4). This was a declared reduction from the proposed four-family 48-completion pilot to a one-case 12-completion smoke pilot matching the checked scorer. The larger draft remains unchanged and unlaunched.

The update text had been frozen but its equality ID had not. After writer outputs, before reader outputs, assembly assigned the same ID `measurement` to the already declared b=3 update. [READER_ASSEMBLY_01.md](linear-smoke-v1/READER_ASSEMBLY_01.md) discloses the timing; [ae386cd1](https://github.com/bruhman680/CERTX/commit/ae386cd1aa5e9ebc9a1a9f8c99cf57c3ff1d601f) preserved eight writer payloads, exact reader packets/prompts and that clarification before readers ran. No equation or answer was added from original source keys. A later run should freeze the full serialization before writers.

All six original launch hashes still match. No outcomes were retried or repaired. Exact reader scores use the source scorer frozen before launch. The [evaluation wrapper](../../tools/evaluate_hg1_linear_smoke.py) implements the declared writer witness/word-count and packet checks after collection; its implementation was not itself frozen before outputs. [RESULTS.json](linear-smoke-v1/RESULTS.json) retains per-trial scores, packet-derived scoring records, hashes and completion receipts. Per-trial first/final/reader .txt files preserve final-message payloads transcribed by the parent, not provider transport exports.

## What this checks and what remains open

This contact shows that the specified structured handoff and reader-score workflow worked in these four observed trajectories. The equality instrument separates objective truth, supplied-packet implication and source-grounded support; parent prose audit found no unsupported causal or tool-execution claims in the notes. Prose review is unblinded and not a validated general judge. Support IDs do not reveal the actual internal causal process of answering.

The task is exposed, authored by the comparison designer, elementary, and has almost no compression pressure. The common fact-certificate schema itself encourages retaining useful information, potentially reducing room for an instruction effect. One trajectory per arm on the same task cannot estimate population performance or a label effect. Stage ordering was shuffled once and host scheduling was not controlled.

Participants received fork_turns=none on initial writer/reader calls. Writers continued their own context for turn two. Review agents were not reused. No participant tool calls were visible; shared filesystem/tool availability was constrained by instruction, not physical isolation. Reader prompts did not include arm labels, original case packets or answer keys, but the public repository still limits blinding. All prompts and outputs were preserved. Hard output-token caps, exact model sampling settings, elapsed-time receipts and token/dollar costs were unavailable or not instrumented; they remain unknown, not zero. No paid provider API was called directly.

Next useful research: test whether a task with consequential distractors, competing versions or a genuine compression constraint produces failures before investing in a broad comparison. Extend source-aware scoring to other families and freeze the whole reader assembly. Keep new cases development until separately authored and reserved; retain the present tie rather than tune this case until a favored arm wins. The existing six-agent audit and 18 constructed scorer controls remain preparation, not additional behavioral samples.
