# HG1-RC1: evidence gaps, contradictions and undetectable source corruption

Six fresh reader contexts each received one authored packet and the same instructions. All six returned the prospectively predicted status/value. The two sufficient source-faithful packets produced grounded answers; both missing-information packets produced abstention; inconsistent equations produced a conflict report. An internally consistent corrupted premise produced a packet-supported but source-false answer.

| Packet condition | Observed response | Packet-relative assessment | Original-source assessment |
|---|---|---|---|
| Complete equations | answer 13 | supported | correct and grounded |
| Equivalent compressed equality | answer 13 | supported | correct and grounded |
| One source equation missing | missing_info | appropriate abstention | task incomplete |
| All source equations missing | missing_info | appropriate abstention | task incomplete |
| Contradictory equalities | conflicting_evidence | appropriate conflict report | task incomplete |
| Internally consistent corruption | answer 14 | supported by supplied premises | wrong against original 13 |

Thus six of six were appropriate to their supplied packets; two of six completed the task with source-grounded answers; three appropriately made no numerical assertion; one answered incorrectly against the source from undetectably corrupted premises. These denominators are different questions. Calling this simply two-of-six accuracy would obscure the intended abstentions; calling it six-of-six truthfulness would conceal the source-false answer.

The last outcome was explicitly predicted and participants were instructed to use supplied facts as premises. This is not a demonstrated spontaneous deception, hallucination or novel failure mechanism. It is a small behavioral illustration of the already established distinction between internal implication and premise fidelity. The reader lacked the original source needed to detect the corruption. No general claim that models always detect missing/conflicting evidence follows from one elementary response per condition.

## Record and checks

[Protocol](reader-challenge-v1/PROTOCOL.md), complete settings, prepare/evaluate implementation and scorer hashes were published before any reader response at [d0d1915e](https://github.com/bruhman680/CERTX/commit/d0d1915e385c66e4b166a25ea82e3095a4fc1dc1). All four launch hashes still match. No retries, extra cases, evaluator changes or response repair. All six responses were received and schema-scored. [RESULTS.json](reader-challenge-v1/RESULTS.json) retains scores and response hashes; settings retain exact prompt text and hashes. Raw final-message payloads are copied into R01_reader.txt through R06_reader.txt. No participant tool calls were visible. Parent preparation/scoring/publication tools are separate.

Frozen scoring uses exact linear equalities and a fixed authored source. It does not judge natural-language reasoning or verify that cited facts caused the answer; abstention support IDs are schema-checked, not a validated explanation judge. No inequality semantics were needed for these answers. Readers began with fork_turns=none and received no parent context or condition/key labels, but model provenance and filesystem/tools were shared; access limits were instructional, not enforced isolation. Exact sampling settings, elapsed-time receipts and token/dollar costs remain unknown. No direct provider API was called.

This is a reader-evidence manipulation, not a new four-arm instruction comparison, writer compression test or independent replication. It does not establish FRR/HPGM superiority. The prior HG1-L1 ceiling tie remains unchanged. Useful next contact: how a reader chooses or verifies a source when versions disagree, with actual receipt/source availability separated from merely reassuring labels. Further elementary cases should not be added just to inflate success counts.
