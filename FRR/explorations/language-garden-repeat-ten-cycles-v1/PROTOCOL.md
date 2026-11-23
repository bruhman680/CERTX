# Ten cycles on direct symbol readout

Use the pinned SmolLM2-135M-Instruct language pilot in a separate experiment. One fresh context per case, greedy decoding, 256 generated tokens maximum, no feedback and no training. Each stage records the previous result hash and freezes its cases before any of its calls. The adaptive decision rules are fixed in design.py before cycle 1. The earlier persistent garden is outside the experiment.

Count exact stripped responses independently of content. For symbol content, take the first paragraph of a nonexact reply only when it names a single supplied candidate and begins with the named candidate or uses a declarative verb. For one/two answers, require a single unambiguous count in the first paragraph and an assertion or a standalone answer. Preserve all replies and audit the extraction. A content result means a reported answer even if the response also contains extra commentary. A cap is reported separately.

For each repeat probe, report always-First, always-Middle and always-Last as baselines on the identical rows. Compare both prompts on the same row when applicable. Report the final reserved panel by shape and mark which positions are decoys. Early panels inform design choices. The final panel is kept out of those choices and is a small within-task repeat, with no claim of cross-domain transfer.
