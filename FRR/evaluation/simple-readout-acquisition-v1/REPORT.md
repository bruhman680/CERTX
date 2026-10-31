# Simple acquisition before harder source binding

31 October 2026 UTC. Local CPU, pinned SmolLM2-135M-Instruct. Completed; no default model promotion.

The little model **can learn this explicit three-way mapping**. All four fresh adapters reach 12/12 seen and 12/12 study-held-out sources, with 4/4 correct in each state on each split. That includes the ordinary `WITHHOLD` label. Earlier harder-task failures cannot be explained by a universal inability to emit that label or learn any balanced three-way task. This contact does not identify the cause of those earlier failures.

| Interface | Original seen free | Original held-out free | Trained seen free | Trained held-out free |
|---|---:|---:|---:|---:|
| alias_0 | 0/12 | 2/12 | 12/12 | 12/12 |
| alias_1 | 0/12 | 0/12 | 12/12 | 12/12 |
| alias_2 | 2/12 | 4/12 | 12/12 | 12/12 |
| canonical | 0/12 | 0/12 | 12/12 | 12/12 |

The constant-class reference is4/12. All trained choice-sum and choice-mean readouts also score 12/12 on both splits. Before training, allowed-choice sum readout scores 3–4/12 per split, while free generation is frequently invalid. The full denominator, raw text, first tokens, choice scores and per-class counts remain in [raw records](run/RAW.jsonl) and [summary](run/SUMMARY.json).

## What was actually learned

Each source has one plot name and an explicitly written `Status: positive`, `Status: zero`, or `Status: missing`. The instruction supplies the status-to-answer mapping. Four training names crossed with three statuses give 12 unique sources. Four other names give 12 study-held-out sources in the same syntax. Those names occurred in earlier research; this is not a global novelty claim. Each name has all three states, preventing a name-only constant association from solving the slice.

One arm maps to YES/NO/WITHHOLD. Three arms rotate positive/zero/missing across A/B/C; these cover three cyclic permutations, not all six assignments. They share one seed, initial tensors, source order and base: they are interface variations, **not independent seed replications**. The canonical arm succeeds too, so this does not demonstrate an alias advantage or a necessity for one-token labels.

`missing` is supplied literally. Success does **not** establish detecting an absent field, recognizing insufficient evidence, calibrated abstention, arithmetic, causal identification, two-record selection, broad FRR benefit, or durable memory. No FRR-versus-no-FRR prompt intervention is present.

## Procedure and numerical readout

[Protocol](PROTOCOL.md), [data](DATA.json), [plan](PLAN.json), and implementation were [frozen](FREEZE.json) before tokenizer/model load and all new forwards. All four use the unchanged pinned base revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, rank 4/alpha 8q/vLoRA, dropout 0,230400 trainable parameters. Seed 73103; AdamW lr 0.001, weight decay 0.01, gradient clip 1; microbatch 1, one example per class accumulated per update.48 updates per arm,12 epochs over12 unique sources,48 presentations per state. Sequence-mean complete assistant-label+EOS cross-entropy. Same update/example budget, not the same tokens or time. No output-dependent retry, accuracy early stopping or checkpoint choice.

Actual tokenization matters: A/B/C each use one token; YES uses two, NO one, WITHHOLD four. EOS adds one. Maximum complete sequence is66 tokens for code arms and73for canonical. No truncation occurred. This is a whole interface comparison, not a clean causal test of token count.

Free generation is greedy with an8 token cap and EOS stopping. Exact stripped labels alone count as valid; invalid outputs remain in denominator. Separately, score each allowed complete answer including EOS:

`score(label) = sum_t log P(label_t | prompt, earlier label tokens)`

Choose the largest sum. A separate mean-logprob diagnostic normalizes by answer length and is not the same probability criterion. Constrained scoring forces one of the allowed classes; it is neither calibrated confidence nor warranted epistemic withholding. Complete-label correctness and first-token correctness are recorded separately.

## Execution, checking and preservation

Training took 264.041 seconds across 192 optimizer updates/576 supervised example presentations.192 free generations plus192three-choice scoring batch forwards (576 teacher-forced candidate sequences). Generation inputtokens12408, outputtokensincludingEOS807; these exclude candidate-scoring/training tokens and are not total compute or billing measures. Readout/scoring elapsed167.545 seconds excludes loading and other work.

[Artifact audit](CHECKS.json) checked192rows: source statuses reparsed, prompts/tokenization/decodes/scores recomputed, frozen inputs match, all four initial adapter tensors equal, all frozen base digests unchanged, adapter finiteness and checkpoint/optimizer byte hashes match. It also verified3391 earlier local files unchanged before navigation sync. Sampled max working estimate1678835712 bytes, processRSS1228013568 bytes. These are phase samples, not continuously measured peaks. Memory/time guards did not trigger.

Three focused fixture/metric tests pass; no separate empirical replication or blinded review. Local checkpoint binaries and optimizer bytes are retained, with published manifests/hashes. Full terminal KV tensors are intentionally not stored in this readout contact; exact token IDs, prompts, labels, scores and pinned state are. The older cache-transfer histories are unchanged. Optimizer pickle data was not loaded by the audit.

## Next contact and practice

The [two-record bridge](../readout-selection-bridge-v1/REPORT.md) reloads these saved final adapters in a separate process, supplies a target header and distractor record, and compares full source with source-parsed crop. Its outcome-informed [single-record frame control](../readout-selection-bridge-v1/frame-control/REPORT.md) separates a further question about changed format. No further training occurs in either.

The useful habit is to establish a basic readout before attributing a harder failure solely to transfer. Retain missingness, class coverage, free output and allowed-choice ranking as different observations. The [optional guidance](../../examples/seen-source-acquisition-before-transfer.md) is refined with these scoped contacts; no universal pass threshold, core/schema/default change or truth authority is added. Grok’s substrate-depth relay remains parked and unvetted.

No separately paid API, rental, installation or model download. Usage/account billing is not visible. Repeated toy success is a foothold for a learning ladder, not a general reasoning result.

## Portable current-contact snapshot

A separately created local snapshot at `/workspace/frr_capsules/simple-readout-and-selection-v1.tar.gz` packages these two studies, all four initial/final adapters and optimizer-state bytes, and their source/data/logs. [Receipt and member hashes](CAPSULE_RECEIPT.json) identify the exact snapshot. It excludes dense base weights, Python runtime and other older research; original absolute workspace paths need adjustment on a new machine. All regular members are reread and verified without extraction or optimizer unpickling. This is not a clean-environment/optimizer-resume rehearsal or an independent backup until copied off workspace. Your older desktop capsule is unchanged and contains a different pair of research adapters. Later publication/sync receipts are outside the snapshot’s creation boundary.
