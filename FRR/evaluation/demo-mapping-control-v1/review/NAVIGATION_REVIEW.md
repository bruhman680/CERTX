# Navigation review: distinguish current state from historical directives

Review date: 29 October 2026, America/Chicago. Scope: read-only assessment of `CURRENT_HANDOFF.md` and `sync/CURRENT_ORIENTATION.md`; no navigation files edited by this reviewer.

## Observed issue

Both entry points contain successive opening paragraphs labelled “Latest contact” or “Latest completed contact.” They usually explain that earlier labels are historical, but this relies on every reader carrying the scope forward through a long document. Both also contain older operative-looking stop language. In particular, the handoff's “Resume and next move” section still describes the probe-witness episode as the current pause, while the orientation calls that episode the “Current rest checkpoint.” Those statements were valid in their original episode. They are stale as present-state navigation after later completed studies and the user's current explicit resumption.

This is an observed textual ambiguity, not evidence that a particular agent actually disobeyed the user or that navigation caused experimental errors. Fixing it can clarify document semantics without establishing a measured reasoning improvement.

## Recommended bounded repair

1. Preserve both pre-edit files byte-for-byte under the new contact's `navigation_before` directory. Record SHA-256 and original path; verify the archived bytes equal the pre-edit bytes. Do not rewrite the archive to make it look cleaner.
2. Put one explicit current-state block at the top of each editable entry point: update date, latest **completed** contact, current work/state, strongest next **proposed** contact, and source/checkpoint links. Keep “proposed,” “running,” “completed” and “paused” distinct. At final sync reflect the actual finished state rather than leaving a “running” label.
3. Remove or relabel earlier active-looking “latest/current/rest/resume” directives in the editable navigation. Preserve historical summaries as dated/identified completed contacts, or link to a history/index rather than stacking all their once-current instructions. A broad sentence that says “everything below is historical” is less clear than labelling the relevant section.
4. State that the user's newest instruction determines whether work resumes or pauses. Saved proposals are not automatic jobs, and an old pause is not a permanent refusal to act. Preserve the financial boundary: included tools/free resources only; separately billed services require explicit authorization.
5. Keep all scientific reports, raw outputs, original failures, reconciliation deposits, code versions and queue verdicts unchanged. A navigation repair does not promote a prompt, close a research family, rerun a study or overturn the historical CR strict ordered-replay failure.
6. Validate every link in the new navigation. A byte-identical archive moved into a deeper directory retains its **old relative-link base**: record the original location and a stable Git commit link for readable history. Do not silently transform archived links while claiming exact preservation.

## Useful minimum current block

The exact wording belongs to the coordinator after final results. A sufficient pattern is: “Updated [date]. Latest completed contact: [link]. Present state: [completed/paused/running, as observed]. Current next proposal: [link/status]. Historical navigation is archived at [link, original path/hash]. Historical stop instructions describe their own episodes; the user's latest direction governs this session.”

## Review outcome

Confident recommendation: repair the two navigation entry points with preserved originals and validated links. No change to scientific conclusions is warranted by this review. No benefit test is required for making the present-state labels internally consistent; any later claim that the repair improves agent performance would need its own evaluation.
