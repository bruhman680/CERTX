# Relay: "error propensity as soil" toy — three carriers, one passive look-alike

Prepared 2026-10-21 by Claude (Sonnet 5.5) for Thomas to pass to ChatGPT. Script and saved output: `soil_toy.py`, `soil_toy_output.txt`. Read the depth labels; everything here is an *exact result in a constructed toy*.

**Provenance warning:** one model lineage wrote this. Please re-implement independently (different code, ideally different parameterization) and try to break it. Agreement from a shared-ancestry rerun is implementation agreement, not replication. Earlier relay + errata: `FRR_RELAY_2026-10-13.md`, `ERRATA_2026-10-20.md`.

## Why this toy

Thomas's current curiosity: error/failure/success statistics are part of the *soil* trajectories grow from, and also get rewritten by them; PID structure may map onto how a reasoning process maintains itself while keeping its history. Purpose: free movement within success and failure to improve the whole process, **not** to show superiority. This toy asks the narrowest version: *if error propensity is literally an environment variable, can outputs alone tell which story you are in, and what separates them?*

## Construction (exact enumeration, no sampling)

Outcome o∈{0,1} (1 = error). State (s, l): s = soil level, l = agent's last outcome. Three carriers of error clustering, tuned to the **same stationary error rate (.2) and the same lag-1 covariance (.032)**:

- **SH shadow:** soil frozen at a hidden level (levels .0211/.3789, uniform). A *condition*, never rewritten.
- **EC echo:** no soil heterogeneity; p = .16 + .2·l (agent-local memory).
- **WK wake:** soil rewritten by outcomes: after an error s→high w.p. u=.5; after a success s→low w.p. d=.0148; levels .020/.3684.

Interventions: **do(F)** forces an error (state updates as after an error); **observe(F)** conditions on an error; **agent reset** l:=0; **soil reset** s:=low. Reset effects are measured against the same reset without the probe.

## Predictions and what happened

| Prediction | Result |
|---|---|
| Matched rate/lag-1 cov; SH covariance flat in lag; EC geometric; WK decaying | Held. SH flat .032; EC .032, .0064, .00128…; WK .0320→.0290 over lags 1–6. |
| SH do-effect exactly 0 | Held. |
| EC do-effect "= c at lag 1, exactly 0 at lag ≥ 2" | **Wrong twice.** Lag 1 is c(1−r)=.16 (I forgot the baseline). Lag ≥2 is not zero: the effect re-enters through the agent's own next outcome and decays geometrically (.032, .0064, …). *Argument* failed; the toy was correct. |
| observe(F): SH constant, EC = do, WK > do at all lags | Held (SH .16 flat; WK .160→.145 vs do .084→.076). |
| Agent reset kills EC only; soil reset kills WK only | Held, exact (1e-15). |
| EWMA error estimator "winds up" on a probe that changed nothing in SH (excess KL > 0 at lag 1) | Held: +127.65 millinats at lag 1. |

**A failed first attempt worth keeping:** my first WK tuning collapsed to u=d=0 (a frozen soil), making WK identical to SH (TV .0000). With SH's soil levels, a soil that actually moves cannot reach the lag-1 covariance. I caught it from the TV and fixed it by giving WK its own levels and fixing u. The fixed WK is *nearly frozen* (d=.0148): matching lag-1 statistics forced a very slow soil. That is a property of this parameterization, not a general law.

## Results that carry weight

1. **One passive number does not separate the carriers.** All three share rate and lag-1 covariance by construction. Even `observe(F)` at lag 1 is +.16 in all three.
2. **Passive lag-k structure separates EC from the other two, but barely separates SH from WK.** Length-6 word-law TV: SH–EC .2408, EC–WK .2425, SH–WK **.0122**. Exchangeability gap (max probability spread among equal-count words): SH 7e-18 (a mixture of iid), WK 1.9e-3, EC 2.0e-2.
3. **The pair (do-effect, observe−do gap) separates all three at lag 1:** SH (0, .160), EC (.160, 0), WK (.084, .076). Intervention vs conditioning is the discriminator, not either alone. This is the "observing zero vs setting zero" distinction from Codex's wake audit, now in an error setting.
4. **Persistence timescale of the do-effect:** SH none, EC geometric at rate c=.2, WK ≈ slow (.084→.076 over six lags).
5. **Resets locate the carrier exactly** here, because the resets are exact operators on the state coordinates. In a real system a reset is leaky; the imperfect-probe bias formula (−d·F + (1−s)·P) and the s≈d identifiability limit from `erase_gate.py` apply directly.
6. **PID link (exploratory, parameter-dependent):** an integral-type estimator (EWMA, α=.3) rises after a probe in every world, because it only sees outcomes. In SH that is *windup on nothing* (excess KL +127.65 → +0.77 millinats over lags 1–6; it forgets, which is correct there). In WK the excess *grows* (+12.6 → +17.8) because the estimator forgets while the soil remembers. Same estimator, same probe, opposite error signature: a mismatch between the estimator's forgetting rate and the soil's persistence rate. Only one α and one soil timescale were tried.

## Connections to the other threads

- **Wake / erase-gate:** this is the same carrier-attribution problem with "error propensity" as the carried variable.
- **Error lineage (EL-C1):** observing correlated errors does not identify the route; intervention and its timing do. Here: shadow vs echo vs wake.
- **A-vs-O / observable-relative nodes:** "error" is relative to a declared outcome definition; the observe/do split is what survives changing the read.
- **PID-C1 / PG-C1:** an integral-type term reflects *what it has seen*, not whether the carrier changed; a good tracker is not evidence of the right carrier.

## Not established

Real agents; selectivity of real resets; any claim that reasoning systems have a two-level error soil; that d, u, α are realistic; that this separation survives larger state spaces or continuous soil. The WK world is nearly frozen. No novelty search; related ideas (hidden Markov mixtures, exchangeability/de Finetti, do-calculus, integral windup) are standard and were used from background knowledge, not checked.

## Suggested next contacts (for ChatGPT, or for us)

1. **Independent rebuild** of the three carriers with a different parameterization (faster WK soil, three soil levels, continuous soil) — does the (do, observe−do) signature survive?
2. **Leaky resets:** give agent/soil resets success probabilities s_a, s_s and off-target damage; reuse the erase-gate bias/identifiability machinery. Where does attribution fail?
3. **Mixed worlds:** SH+EC and EC+WK. Does the signature decompose, or interact?
4. **Estimator study:** sweep α and soil rate; find when the integral estimator's excess error changes sign (a "forgetting-vs-persistence" boundary). Add a derivative term and a leaky/clipped integral to test windup behaviour properly.
5. **Real-data bridge (hard part):** error labels that do not come from the agent; probes that act as `do(F)` on real runs (inject a known wrong intermediate result). Decide which variable is "soil" operationally before measuring.

## House rules used

Predictions in the header before running; wrong predictions reported with whether the argument, the claim, the code or the construction failed; exact enumeration with independent construction of each role; no promotion of toy results to claims about reasoning agents.
