# Post-run reporting correction

The first invocation of the analysis helper failed before running because a text replacement had duplicated the `scheme_statuses` keyword. The draft source is retained as ANALYSIS_DRAFT.txt. The helper was corrected to keep rejected/terminal statuses separate from successful statuses. This did not touch the completed model run, runtime, raw replies, receipts, world state or verifier.
