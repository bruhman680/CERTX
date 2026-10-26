# Independent exact audit

Status: **PASS**. Rebuilt all 144 rows and every grouped count independently using Fraction; compared 10432 exact leaves. Main implementation was neither read nor imported.

The reconstruction was also computed directly in two dimensions with n=(rho,0), s=(0,1). Its squared error was a vector dot product. The envelope was independently maximized over all four coefficient-rectangle corners, then checked against the stated algebraic formula. All reference measurement costs and shared primary readings were checked.

The envelope is conditional on coefficient coverage, orthogonality and the known norm ratio. Those are supplied assumptions. Corner maximization keeps the point denominator h fixed; it does not claim uniform inversion stability over all compatible worlds. The audit evaluates false certificates against the authored actual model, without probability claims.

Both observed-equivalent worlds and all eight contract diagnostics were rebuilt: primaries are exactly (28/25,22/25), while the true gaps are 0 and -6/25. Valid references differ only because additional authoritative observations were supplied.

| Contract | Rows | Covered | Gate pass | Raw certified | False raw |
|---|---:|---:|---:|---:|---:|
| BLIND | 36 | 12 | 30 | 19 | 5 |
| WIDE | 36 | 36 | 18 | 7 | 0 |
| REFERENCE | 36 | 36 | 27 | 18 | 0 |
| BAD_REFERENCE | 36 | 12 | 30 | 22 | 8 |

All expected rows and summaries, individual mismatches, exact check count and auditor hash are retained in AUDIT.json. Display square roots and explanatory prose are not treated as exact arithmetic; their underlying rational quantities are checked.
