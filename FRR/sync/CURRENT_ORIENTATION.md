# Orientation: paused at 450; diagnostic kept separate

5 November 2026. [Handoff](../CURRENT_HANDOFF.md), [run](../evaluation/discovery-400-to-450-v1/REPORT.md), [checks](../evaluation/discovery-400-to-450-v1/CHECKS.json), [diagnostic](../evaluation/world-control-diagnostic-v1/REPORT.md).

Same active world_routine.py / discovery-play-patch-v1. Primary paused at 450, verifier 0085 passes 402 saved generations plus 48 origin. Ten new five-entry windows passed. Old notebook prefix/source records preserved; no job/lock remains. Fifty new entries: 0 world requests, 0 legacy executions, number 0; stops {'token_limit': 39, 'eos': 11}. No setup change, reset, training or paid inference API.

Ten diagnostic generations at snapshot400 never entered primary history. Short LOOK/use-A prompts each worked 2/2; full-context requested trials did not execute a control. Short/full differ in a prompt bundle, not solely history length. Command expression/execution is observed in copies; rule inference/transfer is untested. Model/adapter weights stayed unchanged. Follow-up probes were adaptive and separately declared.

Next proposals: isolate prompt components or test prediction explicitly, recorded as a separate condition. Continue the unchanged primary only on later authorization, with five-entry checks and broad summaries. Never rerun the old installer/finished driver or merge probe/demo data. Latest handoff supersedes old status descriptions.
