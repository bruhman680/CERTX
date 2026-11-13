# Three contacts after the pause

13 November 2026, America/Chicago.

The notebook garden remains paused at entry **1562**, original reference **1550**. No new world-facing condition was installed. These are detached inference and numerical diagnostics, not additional live entries.

1. **Output length:** three exact contexts, same cached 135M model and greedy decoder, up to 1,024 tokens. The first input still has no complete code cell at 1,024. Retained turn 12 and prospective turn 13 both stop naturally at 257 with unfinished fences. Retained 256-token prefixes match exactly; weights and active run unchanged. Length alone is not a sufficient demonstrated repair. [Full report](REPORT.md).
2. **Learner-state carryover:** four seeds, two paired physical contexts, baseline retained/reset × eligibility trace retained/reset × online/frozen. 64 numerical test worlds and 64,000 ticks. All arms lose mean final energy relative to frozen; every arm wins one seed and loses three. Stored state matters causally for trajectories, but keeping both carriers does not consistently rescue this protocol. This is a separate designed numerical controller, not the language model. [Report](../learning-state-carryover-v1/REPORT.md).
3. **Interruption guard:** seven injected Python-exception boundaries passed the tested blocking/recovery assertions. An abrupt child-process exit leaves a stale lock which blocks ordinary explicit recovery. The proposal protects against unnoticed continuation but is not a complete abrupt-death recovery workflow. No lock or pending record was silently removed; no deployment. [Report](../operator-guard-followup-v1/REPORT.md).

## Next directions

The strongest direct notebook question is the interaction of context, decoder and incomplete-output behavior. A detached decoder comparison could test whether the repeated unfinished program is specific to greedy selection; any sampling arms need explicit seeds and enough replication. Durable continuation chunks need separately specified semantics and exact-prefix checks. Neither should silently replace the active contract.

For operator reliability, specify dead-owner lock recovery and test ownership/concurrency before adopting the marker proposal. For numerical learning, a full-length reserved-seed carryover study would be stronger than interpreting the current four-seed exploratory test as definitive.

The older newest-Claude-relay search remains unresolved. No claim that it was found or read is made. All prior reports and historical state remain intact.
