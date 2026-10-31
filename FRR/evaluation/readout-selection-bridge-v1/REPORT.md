# Learned mapping meets a neighboring record

31 October 2026 UTC. Completed follow-up; four fixed saved adapters, no new training.

All four readouts succeeded on the simple task. Adding a target header, a second record and a new instruction frame breaks that success. A deterministic source-selected crop restores exact labels on every evaluated case. This is a practical composite-input boundary, not a unique diagnosis of selection, attention, or memory.

| Interface | Full free /36 | Full allowed-choice sum /36 | Full invalid /36 | Fully correct conflicting header pairs /12 | Cropped free /36 |
|---|---:|---:|---:|---:|---:|
| alias_0 | 13 | 21 | 15 | 0 | 36 |
| alias_1 | 11 | 18 | 17 | 0 | 36 |
| alias_2 | 10 | 14 | 11 | 0 | 36 |
| canonical | 23 | 23 | 0 | 0 | 36 |

References: constant class 12/36; always-first or always-last 24/36. Both positional references get 12/24 conflicting individual decisions and 0/12 fully correct conflicting header pairs. Every full-source trained arm has 0/12 fully correct conflicting header pairs. Changing an answer is not the same as following the correct source: full-source answer changes occur in 4,0,1,1 conflicting pairs respectively for alias_0,alias_1,alias_2,canonical, with none fully correct.

## Design and limits

[Plan/protocol](PROTOCOL.md) and [source/code/checkpoint freeze](FREEZE.json) precede bridge forwards. The bridge was proposed after the first acquisition arm passed; all four final checkpoints were then included without selecting a winner. All acquisition results existed before the bridge freeze. No fresh original-base arm or retraining is introduced here.

Cross Oak/Beech state assignments (three states each), both record orders, and either target identity:36 unique full sources, balanced12 per target state. Identical body/different target-header pairing gives18 pairs,12 with disagreeing target statuses. This is explicit-status selection; no numeric inference or absent-field detection is required. These are self-authored finite fixtures, not independent samples of real-world reasoning.

Crop construction parses a narrow declared grammar, checks both record names, finds the target identity, and returns only that record in the original simple format. It never reads the authored gold-state key for selection. Duplicate/absent targets or text outside grammar are rejected. Three focused parser tests pass. It is an operational example of external evidence selection with a learned readout, not a newly generalized retrieval engine. **36cropped calls reduce to six unique strings, each repeated six times.** Treat36/36as exact results on those calls, not36 independent novel texts.

Full input and cropped input differ in record count, length, formatting and instruction. Therefore the full-to-crop contrast cannot isolate a single causal mechanism. The [single-record frame follow-up](frame-control/REPORT.md) was added explicitly after observing the first full/cropped failure, to test whether the new frame alone can interfere.

## Readout and checks

Use the exact frozen acquisition generation/scoring instrument, greedy8 tokens and complete-answer+EOS summed logprob. Candidate scoring forces a class and does not identify epistemic uncertainty. All failures and invalid outputs remain; [raw records](run/RAW.jsonl), [per-state/pair summary](run/SUMMARY.json). No further optimizer step or default promotion.

288 free generations plus288three-choice scoring batches/864candidate sequences;23760 generation inputtokens,713outputtokensincludingEOS. Largest input104 tokens. Readout/scoring elapsed260.046 seconds, excluding loading/other work. Sampled working maximum2199031808 bytes/RSS1205227520 bytes; not continuous peaks or billing.

[Audit](CHECKS.json) reparses source targets, verifies pairing and class balance, recomputes positional references and metrics, checks all prompts/token IDs/decoded outputs/score arithmetic, and verifies frozen dependency hashes. The fresh bridge process reloads each saved adapter and checks exact final parameter digests against acquisition manifests. That is a fresh-process checkpoint readback **in the same environment**, not a fresh-environment restore or optimizer-resume rehearsal. Saved weights remain unchanged. No full terminal KV tensors are stored for these readout calls.

No independent replication, proof of general FRR advantage, paid service, installation, download or original-model replacement. Existing source/history and the earlier failed reading gate remain intact. The strongest next step depends on the frame control, not a blanket instruction to shorten every source.

## Publication clarification of answer-change counts

`changed_answer_discordant_pairs` compares parsed states and treats an invalid response as `None`. Therefore a valid/invalid pair also counts as a change; the counts above are not counts of two different valid labels. Fully-correct-pair and exact-label metrics are unaffected. This explanatory note was added after the local snapshot was packed; its archived report is the preceding version identified by the snapshot member hash. Experimental code, raw outputs, metrics and snapshot bytes are unchanged.
