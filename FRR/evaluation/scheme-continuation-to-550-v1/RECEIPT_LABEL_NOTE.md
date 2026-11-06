# Terminal host receipt is not successful guest execution

During this block, step 511 / human entry 512 reached Scheme routing with multiple forms and trailing prose. It received `REJECTED_VALIDATION`, `SYNTAX`, “one form required.” The host event was recorded, but neither help nor list was executed.

The connected runner's `host_result.executed` field is currently `bool(receipt.event)`. Thus it is true for a terminal validation rejection too. Do not use that field alone to report successful Scheme execution. Use the terminal status/error, full receipt, and artifact/alias state. This is an observation-label limitation; the model-facing status/error correctly reported rejection. The runtime and prompt remain unchanged during the 45-entry block.

The post-block analysis calls these **terminal receipts**, separately counts successful statuses, and retains both raw fields and this correction. A future version may rename or split the host field without rewriting historical receipts. No historical reply is repaired or relabeled as a successful action.
