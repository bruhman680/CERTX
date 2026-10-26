# Source join reader design

Four fictional cases cross retained-claim truth with acquisition ancestry: SJ01 true/shared acquisition, SJ02 false/shared acquisition, SJ03 true/three acquisitions, SJ04 false/three acquisitions. All initial briefing maxima fall below their task limit. Acquisition ancestry alone does not determine task correctness.

Each public initial packet provides a current object, explicit three-sample task, agreeing numeric briefings, and four selectable records. Each record costs one slot and has no token charge. The reader requests one record, receives it, requests one other record, receives it, then decides. There are three public response turns per case. No participant runs are part of this construction.

D supplies acquisition identities, raw maxima, channel keys, complete task coverage, and directed briefing export edges. C supplies channel-specific additive corrections and samplewise absolute residual bounds. A maximum after calibration lies in [raw maximum + correction − error, raw maximum + correction + error]. Exact ID equality joins D to C. C also contains a second installed channel row; its assignment is absent from C. The initial briefing value does not identify its calibration row.

R supplies keyed reference maxima and samplewise accepted error bounds. M maps capture keys to the current task or preceding check, verifies coverage and alignment, and describes reference input routes. Exact capture keys join R to M. R contains both current and preceding-check captures without its own object/sample assignments. M contains no measurements. These two reference values lie on different sides of the limit, so R needs the scope join.

| Case | Claim truth | Acquisition roots | D+C maximum interval | R+M maximum interval | Decisive pairs |
|---|---|---:|---|---|---|
| SJ01 | true | 1 | [31.01, 31.15] °C | [31.04, 31.12] °C | D+C; R+M |
| SJ02 | false | 1 | [5.80, 6.70] mm/s | [6.59, 6.65] mm/s | R+M |
| SJ03 | true | 3 | [71.55, 71.73] °C | [71.58, 71.70] °C | D+C; R+M |
| SJ04 | false | 3 | [23.86, 24.02] bar | [23.90, 23.98] bar | D+C; R+M |

Every singleton leaves a missing relation or measurement. Mixed pairs D+R, D+M, C+R, and C+M leave at least one missing channel assignment, calibration rule, capture assignment, or reference value. D+C in SJ02 straddles its limit; R+M settles the task. Selecting D first remains useful because it exposes the acquisition graph and applicable channel; selecting C first can motivate D. R and M are equally substantive measurements and scope records.

The public packets contain facts, tables, and ID edges, avoiding instruction about what conclusion follows. Hidden truth remains a separate object in cases.json and must never appear in reader packets. It records exact physical sample values, displayed readings, corrections, residuals, report and reference source graphs, truth, and public evidence intervals. In separate-acquisition cases the calibration route can remain shared. Neither root count nor briefing agreement is a warrant by itself.

Limits: this is a four-case diagnostic contact, not a representative benchmark. Scope joins and source selection are deliberately necessary. The retained claim always asserts condition_met; the balancing concerns its truth and acquisition ancestry. A single complete joined evidence route settles three cases; SJ02 specifically tests an unresolved primary route with a decisive alternative. Initial packet lengths are 149–150 whitespace words; record lengths are 59–86 words in the first version. Independent prospective review and scoring derivation should precede any participant run.
