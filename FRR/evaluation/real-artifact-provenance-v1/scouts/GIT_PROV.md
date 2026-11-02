# Git / PROV knowledge scout — 1 November 2026 America/Chicago

Read-only research for CERTX/FRR. Host date is 2 November UTC. No FRR edits, paid APIs, model downloads, or experiments. Read the cloud runtime skill and networking reference, inspected `/etc/codex/network-policy.json` (unrestricted HTTP; VPN false), and checked environment status (current observations; enforced unrestricted policy). Read the local `evaluation/revision-authority-settle-v1/REPORT.md` for context.

## Five actionable findings

### 1. Preserve a snapshot receipt before inferring an edit operation

**Direct evidence:** Git's [Git Objects chapter](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) describes commits as pointing to snapshot trees, with parent commits, metadata and message. The [commit-tree manual](https://git-scm.com/docs/git-commit-tree) accepts a supplied tree and explicit parents; multiple parents designate a merge.

**Inference for FRR:** A Git parent edge records ancestry. It does not declare the ledger's patch/replacement semantics or establish the truth of file contents. A commit can retain an identical artifact blob while changing unrelated files. Conversely an entire document can be rewritten under the same path. A merge's tree can choose one parent's artifact wholesale.

**Useful checks:** Pin commit SHA, tree SHA, path, blob SHA and bytes. Compare each candidate snapshot directly to the blob stored at the selected commit, rather than reconstructing it solely from a human description or diff. Keep unchanged-path commits distinguishable from content-changing commits. Treat file absence separately from unreadable/missing objects.

### 2. Names and timestamps are claims; signatures need a separate authorization policy

**Direct evidence:** The [Git manual's commit environment variables](https://git-scm.com/docs/git#Documentation/git.txt-GIT_AUTHOR_NAME) let callers set author/committer names, emails and dates. The [verify-commit manual](https://git-scm.com/docs/git-verify-commit) describes validating a commit's GPG signature.

**Inference for FRR:** An owner-matching author string is not authenticated identity; the newest declared timestamp is not an externally established clock. Even successful signature verification would require an explicit signer-to-authority policy and does not make the signed claim factually correct. A selected branch can be authoritative for “what this branch currently records” without being authoritative for empirical truth.

**Useful checks:** Separate `declared_author`, signature result, accepted signer/policy, and question scope. Counterexamples: future-dated parent, backdated child, spoofed allowlisted author, correctly signed but false status. None should silently collapse into “newest is true.”

### 3. A displayed file history can omit evidence and alter apparent parentage

**Direct evidence:** The [git-log history simplification documentation](https://git-scm.com/docs/git-log#_history_simplification) gives examples where path filtering prunes merge sides. It also documents parent rewriting in history modes. The [diff-tree rename options](https://git-scm.com/docs/git-diff-tree#Documentation/git-diff-tree.txt--M) infer renames using similarity thresholds, with 50% default.

**Inference for FRR:** Two adjacent entries returned by a file-history query need not be direct commit parents. A path rename is not stored semantic identity. An apparently linear file history can hide the branches whose contents were discarded by a merge.

**Useful checks:** Read actual commit-object parent IDs; retain them even when a parent does not change this path. Inspect the bounded full commit graph before interpreting file-history neighbors. Record rename detection options and preserve old/new paths and object IDs. Compare a merge's artifact with each actual parent; do not assume the result combines all claims.

### 4. PROV revision, derivation, activity and invalidation have different meanings

**Direct evidence:** [PROV-DM §2.1.2 and §5.2.2](https://www.w3.org/TR/prov-dm/#term-Revision) says revision is a derivation retaining substantial original content. Use plus generation alone is insufficient for derivation: influence is required. Activities are processes; entities are their inputs/outputs. [Invalidation §5.1.8](https://www.w3.org/TR/prov-dm/#term-Invalidation) can denote expiry even when an artifact remains physically present. Agent association records responsibility, not an authentication protocol.

**Inference for FRR:** Store the document snapshot, editing/extraction activity, agent claim and semantic relation separately. A Git successor need not meet PROV's revision meaning. Deleting a current path is not proof that an old archived claim became false. Conversely, bytes surviving in history do not mean a policy/status remains applicable.

**Useful checks:** Distinguish copied quotation from independent confirmation; distinguish a surviving archived voucher/document from current validity; do not infer content derivation merely because one activity used an old file while generating a new one. Keep original bytes available after current-state expiry.

### 5. Provenance consistency is a narrower result than verified truth

**Direct evidence:** [PROV-CONSTRAINTS §1.2](https://www.w3.org/TR/prov-constraints/#purpose) defines validity as a consistent history, explicitly distinguishing this from logical validity. [§7.1](https://www.w3.org/TR/prov-constraints/#equivalence) makes valid instances equivalent under reordering of statements and attributes (with stated details and exceptions). Constraints concern uniqueness, ordering, impossibility and types.

**Inference for FRR:** A graph can pass structural checks while all sources are mistaken or fabricated. Preserve separate outcomes for coherent provenance, authorized source, materialized state and warranted factual endorsement. The existing reversal-invariance result fits an order-independent interpretation but is not proof that the real source facts are correct or that the ledger implements PROV.

**Useful checks:** Two structurally coherent contradictory claims remain a conflict; reordering received records must not change graph/state receipts under the declared contract; authentication failure must not be presented as a graph error or a factual refutation.

## Source access and limits

All eight primary pages linked above were actually opened through the web tool, with follow-up page searches around the cited definitions. No secondary summaries were relied on. Paraphrases above are marked as direct documentary evidence; proposed FRR implications and tests are explicitly inferences. The proposed checks were not run by this scout. The actual CERTX artifact history is being inspected separately by the main agent; this note makes no claim about that history's contents, signatures, completeness or author authority.

Practical receipt boundary: **stored bytes / actual ancestry → declared interpretation → authentication and authority scope → factual endorsement**. Each transition needs its own evidence or explicit assumption.
