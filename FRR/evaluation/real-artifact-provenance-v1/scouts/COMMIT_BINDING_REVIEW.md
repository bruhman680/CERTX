# Independent bounded Git commit binding review

1 November 2026 America/Chicago; executed 2 November UTC. Read-only review of `/workspace/frr/evaluation/real-artifact-provenance-v1/{CAPTURE.json,POLICY.json,receipt.py,run.py,CHECKS.json,FREEZE.json}`. No network, model work, source-study edits, or Git object-database writes.

## Result

**All eight captured commit IDs have an exactly hash-matching reconstructed unsigned commit body.** Each result independently agrees under Python SHA1 and `git hash-object -t commit --stdin` (without `-w`). The matching bodies bind the captured ordered parents, tree ID, author and committer fields, timestamps and exact message to the selected Git object IDs under Git's SHA1 object-addressing scheme. This strengthens the original audit's explicitly limited tree/blob check; it does not retroactively change what that audit tested.

Every matching candidate uses **-0500** for both author and committer timezone offset, with **zero LF bytes appended** to the API message. UTC-normalized `+0000` candidates, with zero/one/two appended LFs, all failed. The API's ISO UTC timestamps preserved instants but did not retain original numeric offsets; treating the normalized text as original serialization would have produced incorrect hashes.

| Captured commit | Matching body bytes | Author/committer offset | Appended LF | Independent Git check |
|---|---:|---|---:|---|
| fdb0f707101364121650789912b47ca572e50d93 | 318 | -0500 / -0500 | 0 | match |
| a6687963ee55d19f59e581fb28569a3e141af54f | 310 | -0500 / -0500 | 0 | match |
| defbe7d6892a16b90785587e1f65d7b9d8692b9b | 322 | -0500 / -0500 | 0 | match |
| 3010deae5640b43017a7adca01b4499b7ace2d9f | 304 | -0500 / -0500 | 0 | match |
| 093f60cd9cc91512597f68966d55bb2fd4a3a933 | 308 | -0500 / -0500 | 0 | match |
| fb48d83c1ae9ef82edff082495630daaa90125f2 | 297 | -0500 / -0500 | 0 | match |
| 9a794f12668a8385bc8b9de000acd9cf3cd6058d | 322 | -0500 / -0500 | 0 | match |
| 0a7a7b103c746f11826cff3f29bfd17c1f9701a1 | 314 | -0500 / -0500 | 0 | match |

## Exact procedure and retained failures

Reproducer: `/workspace/review_commit_bindings.py`. Source capture SHA256 is retained in the output. For each captured commit, serialize UTF-8 headers in order `tree`, all `parent` headers in API order, `author`, `committer`, blank line, exact API message. Convert API ISO timestamps to Unix seconds. Assume no encoding, gpgsig, mergetag or other extra headers. Try independent author/committer offsets from -1200 to +1400 in 15-minute increments, plus distinct `-0000`; try zero/one/two appended LF bytes. Compute SHA1 over `commit <body-byte-length> NUL <body>`. Search all candidates rather than stopping at first match.

There are 33,708 candidates per commit, 269,664 total, with exactly one match per commit in this bounded candidate family. Full attempted parameter/hash records, including failures, are in `/workspace/git-commit-binding-offset-candidates-2026-11-01.json`. The earlier 24 failed +0000 candidates are retained separately in `/workspace/git-commit-binding-candidates-2026-11-01.json`.

Matching bodies are `/workspace/reconstructed-commit-<full-sha>.bin`. These are reconstructed bytes validated against captured object IDs; they were **not retrieved raw commit payloads**. Before a hash match, any candidate was only a serialization hypothesis. The exact matches provide content-address consistency under the same Git SHA1 assumptions as the tree/blob checks; they do not establish mathematical uniqueness of all possible byte strings or cryptographic identity of a person.

## Independent scope review

Read-only replay of `receipt.verify` passes with eight snapshots and selected head `fdb0f707101364121650789912b47ca572e50d93`. The frozen-input SHA256 map remains unchanged after this review. The source verifier correctly keeps semantic truth and author authentication false, bounds the first-parent frontier, and reports that raw commit bytes were not rehashed by that verifier. `CHECKS.json` remains an accurate historical description of its original procedure. This supplement supplies a separate stronger commit-binding check.

The original receipt hashes trees/blobs and follows the commit-to-tree and first-parent links supplied by API metadata. The supplemental matching bodies now bind those supplied links to the captured commit IDs. This does **not** authenticate the branch-head acquisition or prove that the selected pin is an externally mandated authoritative head; pin selection remains the declared policy. All eight commits are unsigned according to the captured API, and a hash match does not verify authorship. No evidence was obtained about post-cutoff branch state, uncaptured ancestors, other branches, or factual correctness of document claims.

The current implementation hardcodes `FRR/CURRENT_HANDOFF.md` tree traversal while comparing bundle/policy artifact-path strings. This is consistent with the fixed captured policy and bounded artifact study, but should not be described as a general arbitrary-path verifier. No change is needed for the declared single-artifact scope. Six mutation controls and nine tests are functional checks; this review replays the verifier and checks frozen hashes, and does not claim independent acquisition, a new empirical model trial, or broader test coverage.

Bounded review stopped after the eight captured commits. Original frozen files were not rewritten or relabeled.
