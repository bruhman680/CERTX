# Prospective source review

26 October 2026, before main execution. **PASS for the exact source/protocol/schema hashes below.** Reviewer read all of `experiment.py`, `SCHEMA.md` and `PROTOCOL.md`, then reread the final assertion block and scalar-only ambiguity revisions. Reviewer did not import or execute the experiment, fit or score source data, or inspect outcomes. This is source review, not independent numerical replay or empirical replication.

## Reviewed byte identities

| File | SHA256 |
|---|---|
| `experiment.py` | `4c85d0ac8512ae7808e922c678f1427ac4b72434c99b0bbe2b4e014c765e8a8d` |
| `PROTOCOL.md` | `5931aab0aa9749e918d08ff3e39fcdc8132c53cdc9643626e59cf3b61b8b4c70` |
| `SCHEMA.md` | `83184270868ec714cde9594a113cedf1f33f98765f8e0302a605dfbbc8713c1c` |

Any later scientific source or contract change needs a documented delta review before execution; the hashes identify the scope of this approval.

## Findings

The implementation matches the declared 144-row grid: four exact coefficient probes, three bias pairs, four contracts and three norm ratios. Each coefficient/bias world shares its two primary scalar readings across methods and norm ratios. The separate ambiguity witness writes exactly eight supplementary rows at rho=1 into the summary; these are excluded from main-grid aggregates. Source, schema and protocol now consistently restrict its observational equivalence to the two primary scalar readings and explicitly disclaim full-vector equivalence.

The four contracts use total-bias radii `.02`, `.15`, `.01`, `.01`, respectively. There is no extra residual-noise term. REFERENCE reads the actual two role biases as its authored reference observations; BAD_REFERENCE supplies zeros. Both carry two extra scalar measurements and explicit role-authority assumptions. Source correctly evaluates contract validity and coefficient coverage against the actual fixture while issuing gate/raw certificates without using coverage or actual error as decision inputs.

The coefficient intervals subtract reversed bias endpoints; gap endpoints subtract opposite role endpoints. Gate strictly excludes exact zero and tests nonempty intervals. Point means use uncorrected readings for BLIND/WIDE and subtract references for REFERENCE/BAD_REFERENCE. The reconstruction's nuisance coefficient `-da/h`, signal gain `(g-da)/h`, squared actual relative error `((da*rho)^2+db^2)/h^2`, and fixed-point box envelope match the independent derivation and protocol. The raw budget is exact `1/10`, compared by squares `1/100`, separately from the nonsingularity gate.

Zero point denominator gives unavailable inversion and null error/envelope fields; gate withholding leaves an otherwise available diagnostic point intact. Raw certification requires a passing gate and sufficient envelope. False raw certification is evaluated against actual error only after that decision. No missing inversion is encoded as zero error, and square roots are used solely for display. Fraction construction, interval arithmetic, coverage, comparisons and squared-error decisions remain exact.

Main totals and subgroup summaries use only the 144 main rows. Counts distinguish actual singularity, passing gate, withholding, point availability, coefficient coverage, conditional-envelope validity and raw certification. Prospective expected-count assertions are consistent with the structural grid and do not tune the method. The implementation refuses to overwrite existing result artifacts; provenance and runtime capture are explicitly the invoking controller's responsibility.

## Interpretation boundary

No blocking computational issue found. This approval assumes the supplied orthogonality, nonzero signal norm, known rho, scalar response model, role assignments and reference-transport bounds. REFERENCE's exact centering and BAD_REFERENCE's failure are authored controls; neither estimates real reference reliability. A passing conditional gate or raw certificate does not validate those assumptions. The honest WIDE and REFERENCE contracts differ in both total declared uncertainty and supplied observations; descriptions must account for both. No retrieval, learned-language, probability, semantic-authority or durable behavioral claim follows.
