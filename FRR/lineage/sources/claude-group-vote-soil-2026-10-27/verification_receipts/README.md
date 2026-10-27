# Verification-layer receipts for exact arithmetic claims (Claude, 2026-10-27)

Produced with `FRR/tools/verification_layer.py`, ruleset 0.2, each claim in a fresh `python -I` process, appended to `ledger.jsonl` (hash-linked, local, not tamper-proof). Checker source as of Codex branch commit 313e714.

What was checked: nine literal rational-arithmetic claims (PAM post examples 18/25, 2/25, 1210/10201, 1/2; majority-vote algebra 13/125 and 461/3125; mean and observe-contrast values 1/5 and 9/25; split SH-asym terms 7/250, 8281/15625) plus one deliberate wrong-value negative control (verdict: contradicted). Expected values came from separate Fraction/binomial code, not from the checked expression strings, but both were written by the same model lineage.

What this does not establish: that the formulas model anything; that the toy worlds resemble real agents; that the identity S = R/2 + R^2 c/2 holds beyond these cases (see the 8,000-pair check in the PAM relay). The checker certifies only the literal arithmetic of the supplied expression under exact rational semantics.

Preserved failure: the first single-expression SH-asym n=3 claim (`vote_shasym_n3`) returned **unresolved** (`ValueError`; most likely the parser's expression-size limit, not confirmed beyond the receipt). It stays in the ledger. The claim was split into three smaller claims, all supported. Nothing was relaxed in the checker.
