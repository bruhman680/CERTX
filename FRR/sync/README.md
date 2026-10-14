# Sync and preserved layers — prototype

DEPOSIT_EVENTS.jsonl imports six verified consecutive publication commits on our FRR branch. It is a partial record of deposits, not the full CERTX history, the full conversation, or a log of scientific truth. Git commit timestamps are recording times; they need not be the times the underlying work occurred.

Keep historical entries unchanged and append new deposit entries. Preserve corrections as new events referencing affected prior artifacts; current acceptance must be explicitly stated, never inferred from recency alone. This prototype validates local structure and append-prefix preservation; it supplies no cryptographic authority or prevention of administrators rewriting history.

tools/check_sync_history.py builds a commit-pinned navigation view and flags whether an orientation record covers the listed history. Archived originals and reports remain layers. Current orientation is a replaceable, scoped view with source pointers, not the historical record itself.

Run the tool against DEPOSIT_EVENTS.jsonl. Optionally pass --orientation-through COMMIT to check freshness and --previous FILE to verify the exact byte-prefix convention. A new topic absent from the orientation is a navigation omission, not automatically a false scientific claim.

Current task: examine usefulness of sync habits and palimpsest records. The upcoming research direction remains subject to the user's steering. A future agent must read the current task and verify relevant pinned artifacts; neither this index nor the prompt automatically loads them.

Source archive is local; published artifacts are linked through source commits. No controlled AI-continuation benefit has yet been measured. Real tests must match context/compute budgets and include stale summaries, corrected claims, missing artifacts, and independent branches.
