# Review and small comparison repair

Coordinator reviewed the adapter, protocol, challenges and source rows. No independent or masked review took place. Historical outcomes were already known, so this is not a blinded performance experiment.

The first aggregate-comparison snippet raised AssertionError because it compared stop-count dictionaries literally: the old summary includes `token_limit: 0`, whereas the new Counter summary omits zero-count categories. The expected new receipt and all 15 challenge groups already passed. No source, receipt, expectation, frozen adapter or key changed. The retained comparison script compares count dictionaries over the union of keys, treating absent counts as zero. It then passed. This is a representation mismatch in the comparison, not a changed model result.

The adapter checks metadata consistency only. It does not decode token IDs, verify that the text came from those tokens, validate cache bytes or rerun inference. A caller who deliberately rebinds both fabricated sources and a contract can supply a fabricated cohort. Input hashes prevent unnoticed change relative to the declared binding, not fabrication or caller selection bias. Key labels are supplied judgments, not experimentally proven truth.
