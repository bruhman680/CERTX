# Final prose and result review

26 October 2026. **PASS: no required corrections identified.** Reviewed `REPORT.md` and `NEXT_CONTACT.md` against the saved main rows and summary, `EXECUTION.json`, the protocol/source review and independent auditor's report. Read a compact exact table of all 144 main rows, including coverage, gate, point error, envelope, raw certification and false certification. This review did not run or import the experiment, rerun its main, or reproduce the auditor's implementation. It is a prose/result consistency review by the earlier source reviewer, not another independent empirical replication.

## Verified result statements

The four report-table rows match saved summaries: coverage 12/36/36/12; passing gap gates 30/18/27/30; passing on true COPY 3/0/0/3; raw certificates 19/7/18/22; false raw certificates 5/0/0/8, in BLIND/WIDE/REFERENCE/BAD_REFERENCE order. Totals 96 covered, 105 passes, 39 withholds, 117 available and 27 unavailable points, 66 raw certificates and 13 false raw certificates match the artifacts. All nine nonsingular withholds are WIDE/WEAK. There are no empty intervals. The 75 conditional-envelope checks and 42 uncovered-envelope violations agree with saved results. Supplemental ambiguity rows remain excluded.

All three selected cases match their exact saved rows. CONTEXT/COMMON/rho=2 has actual squared error 9/500, BLIND envelope 1/2000 and BAD_REFERENCE envelope 1/8000. OPPOSED/COPY has h=-6/25, BLIND gap [-7/25,-1/5], BAD_REFERENCE gap [-13/50,-11/50], and error squared `(rho^2+1)/4`. REFERENCE/WEAK has zero actual point error, gap [2/25,3/25], and squared envelopes 1/80,1/50,1/20, each exceeding the fixed 1/100 squared budget. Display square roots are correctly rounded for the prose.

Execution metadata supports the reported sole main execution, exit zero, Python 3.12.14 and approximately .0595 seconds. The auditor reports 10,432 exact comparisons with no mismatch and covers all main and eight supplemental rows. The report attributes this correctly to a separate reimplementation; source/schema/specification and platform remain common.

## Scope and interpretation

The report distinguishes equal common offsets from role-opposed biases and accurately states that common offsets can preserve a gap while damaging raw values. It treats the gate and error envelope as conditional on coefficient coverage and supplied geometry; the fixed-denominator rectangle supremum is not confused with changing-denominator stability or richer observed-vector constraints.

The scalar ambiguity section explicitly restricts indistinguishability to the primary scalar readings and notes different Dprime vectors for fixed orthogonal latent components. It does not claim full-data impossibility. Reference centering, role authority, transport, bounds, known norm ratio and orthogonality are supplied information. Acquisition comparisons acknowledge changed uncertainty contracts and repeated reference patterns. The report makes no empirical reference-reliability, probability, retrieval, learned-language, efficacy or durable-habit claim.

`NEXT_CONTACT.md` remains a proposal rather than a launched participant study. It preserves source ancestry versus task authority, available versus insufficient evidence, equal-information comparisons and distinct repair/withholding outcomes. Neither document turns this authored exact toy into evidence of actual-agent benefit. Historical CR/PW and queue/memory status assertions are explicitly preservation statements; this final review does not independently reaudit the broader historical repository or queue.

No result, prose or contract change was requested. No additional execution is warranted for this review.
