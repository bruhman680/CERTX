# Amendment 01: numeric parser bound after initial instrument run

Initial code/protocol/fixtures were deposited at commit 2c4c4e966722d49f94a2db59f9d62525398bd4d0 before 44 evaluations. Those evaluations completed with all expected dispositions and unchanged launch hashes; their receipts/results/log remain unmodified. No participant trial occurred.

Post-run code review found that limiting input string length and checking rational bit length after Fraction(text) does not bound exponent expansion during parsing. A short exponent expression can request a very large number. Extreme exponent payloads were not executed on the initial parser. The authored cases did not cover this failure mode, so their success did not establish adequate resource bounds.

Repair: before Fraction parses a supplied numeric string, accept only plain signed integer, integer fraction or integer-leading decimal syntax, with the existing text-length bound. Exponent syntax, leading-dot decimals and nonnumeric forms remain unresolved. Arithmetic-expression AST restrictions remain unchanged. This is a disclosed checker repair, not proof of complete hostile-input security. The CLI is a local trusted-workspace tool, not a hardened remote service.

Ruleset names 0.1/0.2 denote adapter capabilities. Exact checker SHA identifies this source revision. Original launch hashes intentionally no longer match the repaired source; preserve the initial receipt's original unchanged-at-run result rather than rerunning its one-shot script and overwriting history. A separate hardening manifest and output record the repaired checker replay.

Before expanded execution, freeze repaired source, new check script, original contracts/keys and this note. Replay all 44 authored dispositions, add exponent/long/malformed-number rejection and valid plain-number controls, and verify local CLI behavior against a correct and a contradicted claim. CLI exit zero means a receipt was produced, not that the claim passed: automation must inspect verdict. Preserve normal stdout/stderr and both sets of outputs. No retuning of scientific predictions or core FRR changes.
