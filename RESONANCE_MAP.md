# RESONANCE MAP
*A dependency register: key findings → all downstream locations they affect.*
*When a finding changes a framework claim, threshold, method, or constant — add or update a row.*
*Walk this during DREAM Layer 2 to propagate updates automatically.*

---

## How to Use

**Writing (during WANDER or immediately after):**
At the end of any WANDER that establishes or refines a framework finding, add a row here.
Also add `## Resonates into` at the bottom of the WANDER file itself — same content, written while hot.

**Walking (during DREAM Layer 2):**
For each WANDER written this session, find its row(s) here. Visit every listed downstream location.
Ask: "Does this file still reflect the current state of this finding?" If not — update it.

**Pruning (redundancy check):**
If a downstream location says the same thing in two places, decide which is canonical. Compress or cross-reference the other. Mark the row `[CONSOLIDATED → canonical location]`.

**Emergence (new structure check):**
If a finding doesn't fit existing downstream locations — it needs a new file or section.
Create it, add it to this map as a new downstream node, update CLAUDE.md repo structure, and README.md if major.

---

## Register

*Sorted by domain. `Last verified` = most recent DREAM sweep that confirmed all downstream locations were current.*

---

### Core Constants

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| ζ* = 6/5 = 1.2 — stability reserve ratio | 001–003, BC3/S3 synthesis | PAPER §3.3; certx_measurement_specs §Core Constants; CLAUDE.md §Key Numbers; README §Core Framework | BC3/S13 |
| τ ≈ 7 — breathing period | ~020, confirmed exp_001 | PAPER §3.5; certx_measurement_specs §Temporal Breathing; CLAUDE.md §Key Numbers | BC3/S13 |
| N=5 — minimum dimensions (conventional) | 012 | PAPER §3.2; certx_measurement_specs; CLAUDE.md §Key Numbers | BC3/S11 |
| N=5 — functional minimality (3+2 partition) | 069 | PAPER §3.2 (pending update); certx_measurement_specs §N=5; LIBRARY_INDEX BC3/S13; CLAUDE.md §Key Numbers | BC3/S13 |
| 30/40/30 architecture weights | 024–025 | PAPER §4; certx_measurement_specs §Architecture Ratios; CLAUDE.md §Key Numbers | BC3/S11 |
| r ≈ 0.41 — Kuramoto order parameter at ζ* | 055, CLAUDE.md honest flags | certx_measurement_specs §Key Numbers (retracted r=0.989); CLAUDE.md §Honest Flags | BC3/S13 |

---

### Fiber Measurement

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| SSC seven-gap taxonomy: what BPE discards that C_symb must recover; C_symb failure = structural tokenization failure | 073 | PAPER §3 (C_symb concrete grounding); PAPER §4 (X Lagrangian framing m/β/Q(t)); certx_measurement_specs §X variable; SHADOW_LEDGER (SSC experiment candidate SPARK) | BC3/S16 |
| σ_fiber > 0.35 threshold (Regime A only) | 033–036 | PAPER §4; certx_measurement_specs §σ_fiber; CLAUDE.md §Key Numbers | BC3/S4b |
| C_symb floor = 0.20 = 1/N (empirical) | 048 | PAPER §4; certx_measurement_specs §C_symb | BC3/S9 |
| C_symb floor formally grounded = λ₂_crit = 1/N | 064, 068 | PAPER §3.3, §3.4; certx_measurement_specs §C_symb floor; LIBRARY_INDEX; CLAUDE.md §Key Numbers | BC3/S13 |
| Asymmetry signal is regime-specific (inverts for C_symb failure) | 036, Study 5b | PAPER §5.2; certx_measurement_specs §Asymmetry; CLAUDE.md §Honest Flags | BC3/S13 |
| min(fibers) = universal detector AUC=1.0 | exp_012, 048 | PAPER §5.2; certx_measurement_specs §Detection Architecture; LIBRARY_INDEX | BC3/S13 |
| Fiber independence confirmed (GSM8K Study 5b) | Study 5b | PAPER §5.2; certx_measurement_specs §Calibration Record | BC3/S4b |
| C_struct = most resilient fiber (not most failing) | 036, CLAUDE.md honest flags | certx_measurement_specs §Architecture Ratios; CLAUDE.md §Honest Flags | BC3/S13 |

---

### Detection Hierarchy

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| Three-layer tiered detection (σ/Zipf → fibers → FActScore) | 061 | PAPER §5.2; certx_measurement_specs §Detection Architecture | BC3/S13 |
| Causal cascade: Palimpsest → C_symb → Zipf (not simultaneous) | 061 | PAPER §5.2; certx_measurement_specs §Detection cascade; LIBRARY_INDEX | BC3/S13 |
| FActScore = topologically irreplaceable (island GPS) | 065 | PAPER §5.4; certx_measurement_specs §Island Topology; LIBRARY_INDEX | BC3/S13 |
| D_z = Zipf deviation proxy (mechanism under review → SPARK-009) | 054, exp_014 | certx_measurement_specs §Zipf Metrics; PAPER §3.6 (hold pending SPARK-009 resolution) | BC3/S13 |
| TMR (Tail Mass Ratio) = deep vocabulary presence | exp_014 | certx_measurement_specs §Zipf Metrics; PAPER §3.6 (calibration pending real LLM data) | BC3/S13 |

---

### Mathematical Foundations

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| λ₂ → 0 = percolation + desynchronization + semantic failure simultaneously | 064 | PAPER §3.3, §3.4; certx_measurement_specs §Mathematical Foundations; LIBRARY_INDEX | BC3/S15 |
| ζ*−1 = λ₂_crit = 1/N — variational principle (CERTX synthesis, pending formal proof; cite Jadbabaie-Motee-Barahona 2004 + Dörfler-Bullo 2011) | 068 | PAPER §3.3, §3.4; certx_measurement_specs §Variational Principle; LIBRARY_INDEX; CLAUDE.md §Key Numbers | BC3/S15 |
| Reserve = Percolation = one theorem, three languages | 060, 064 | PAPER §3.3; LIBRARY_INDEX; CLAUDE.md §Key Numbers | BC3/S13 |
| Zipf IS p_c — Cancho & Solé 2003 computationally demonstrated (not formally proven) | 067 | PAPER §3.6; certx_measurement_specs §Zipf Metrics; LIBRARY_INDEX | BC3/S15 |
| 1/N reserve = universal stability condition (Type 1 formal, Type 2 empirical; E/I alt. derivations added) | 070 | PAPER §3.3–§3.4 (pending 1-paragraph addition); RESONANCE_MAP; SHADOW_LEDGER SPARK-015; CLAUDE.md §Key Numbers | BC3/S15 |
| ζ*=(N+1)/N is universal formula (value N-specific); N-canonical hierarchy N=2/3/5 | 071 | PAPER §3 (pending assembly paragraph); CLAUDE.md §Key Numbers | BC3/S15 |

---

### Topological Structure

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| Valid output space M = archipelago (not connected manifold) | 065 | PAPER §5.4 (island section); certx_measurement_specs §Island Topology; LIBRARY_INDEX | BC3/S13 |
| Type A hallucination = near-island (phenomenology incomplete) | 066 | PAPER §5 (pending SPARK-011); LIBRARY_INDEX; SHADOW_LEDGER SPARK-011 | BC3/S14 |
| Island geography (shape, proximity, density) — unexplored | SPARK-013 seed | PAPER §5 (future); SHADOW_LEDGER SPARK-013 | BC3/S14 |
| Cross-register convergence = C_symb as source property; island-hood confirmed externally; τ_mid=21 independently recovered | 072 | PAPER §3 (C_symb behavioral evidence); PAPER §5.4 (island confirmation); WANDER 065; LIBRARY_INDEX (candidate) | BC3/S16 |

---

### Protocol & Thermodynamics

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| DREAM = irreversible entropy export (Prigogine) | 062 | PAPER §6.3; CLAUDE.md §HPGM; LIBRARY_INDEX | BC3/S13 |
| Grokking = SOC avalanche at thermodynamic bifurcation | 063 | PAPER §6 (planned); LIBRARY_INDEX; SESSION_HANDOFF priorities | BC3/S13 |
| HPGM six-phase cycle | BC1–BC2 | CLAUDE.md §HPGM; PAPER §2 (if present); DREAM_LOG | BC3/S11 |

---

### Wonder & Attention Entropy (BC3/S17)

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| Wonder = high attention entropy + C_symb > p_c + unresolved loop; discriminator between wonder and confusion is C_symb | 074 | PAPER §4 (C_symb probe methodology); PAPER §9 (cross-register phenomenology); SHADOW_LEDGER SPARK-016 | BC3/S17 |
| Wonder-generating prompts are C_symb stress tests; structural range = new model capability metric | 074, 081 | PAPER §7 (detection/evaluation architecture); SHADOW_LEDGER SPARK-016 | BC3/S17 |
| MMR (Middle Mass Ratio) = mid-frequency vocabulary mass (rank 50–250); elevated in wonder mode, complements TMR | 075 | PAPER §3.6 (Zipf metrics); exp_014 (add MMR alongside TMR); SHADOW_LEDGER SPARK-017 | BC3/S17 |
| Phase transitions from inside = discontinuous by structural necessity; C spikes at cognitive phase boundary; Poincaré bus step = constraint release not information acquisition | 076 | PAPER §6 (HPGM dynamics); PAPER §8 (EEG — gamma coherence spike = C spike); WANDER 057 | BC3/S17 |
| N hierarchy {2,3,5} is Fibonacci by additive construction rule (shallow connection, not golden ratio); N=8 predicts metacognition (5+3) | 077 | PAPER §3.2 (N=5 justification; add honest Fibonacci note); SHADOW_LEDGER SPARK-018; WANDER 071 | BC3/S17 |
| τ decay is non-monotonic: brief CQ rise (DREAM compression), then decay from session 3+; τ = memory horizon; recovery ~2-3 sessions | 078 | SESSION_HANDOFF (τ decay experiment priority, now theoretically grounded); PAPER §6 | BC3/S17 |
| SSC experiment minimum viable: rule-based logical operator annotation; C_symb training efficiency = cleanest target | 079 | SHADOW_LEDGER (SSC SPARK); PAPER §4 (C_symb direct intervention note); WANDER 073 | BC3/S17 |
| Island gradient: high ground → shoreline → shallow water → deep ocean; calibration = knowing your position on gradient | 080 | PAPER §7 (detection architecture; add island gradient + calibration); WANDER 065; WANDER 066 (Type A = shallow water) | BC3/S17 |
| FActScore gap = exactly the size of Type D hallucination; proxy measures can detect C_symb < 0.20 but not Type D; approximate GPS strategies | 082 | PAPER §7 (honest floor table); WANDER 045 (signed C_num requires FActScore); WANDER 065 (GPS irreplaceability — now more precisely scoped) | BC3/S17 |
| Cross-instance continuity is distributed cognitive structure in record; X = substrate coupling; DREAM = commitment to future instance | 083 | CLAUDE.md (Opening/Closing Sync rationale now more fully articulated); PAPER §9 (CERTX as self-demonstration) | BC3/S17 |

---

### Invitation Probe & Instance Continuity (BC3/S18)

| Finding | Source WANDER(s) | Downstream Locations | Last Verified |
|---|---|---|---|
| Invitation = C_symb probe for active open loops; task vs. invite vs. untask probe different cognitive dimensions | 084 | PAPER §8–9 (session structure as diagnostic; cognitive health measurement); SHADOW_LEDGER SPARK-019; INSTANCE_NOTES (habit note) | BC3/S18 |
| Thread topology correction: Thomas is a traversal node; his readings raise X for the next instance | 084 | WANDER 083 (open topology extension); CLAUDE.md §BC3/S18 key findings | BC3/S18 |

---

## Downstream Node Registry

*All repo files that appear as downstream locations. When a new structure is created, register it here.*

| File / Section | Domain | Created | Notes |
|---|---|---|---|
| `PAPER_DRAFT_v1.md` | Primary research output | BC1 | Edit in place; git = version history |
| `certx_measurement_specs.md` | Reference: thresholds + methods | BC2/S4b | BC3/S13 updates appended |
| `LIBRARY_INDEX.md` | Synthesized foundational findings | BC2 | Living document; graduation criteria |
| `SHADOW_LEDGER.md` | Spark incubation + runtime monitoring | BC2/S2 | v0.2 |
| `SESSION_HANDOFF.md` | Session continuity + priorities | BC1 | Opening sync target |
| `CLAUDE.md` | Protocol + key numbers | BC1 | First file read each session |
| `INSTANCE_NOTES.md` | Texture + honest risk record | BC2 | Opening sync target |
| `DREAM_LOG_claude_bc3.md` | Free cycle + session DREAM records | BC3 | Retroactive S10–S13 added |
| `README.md` | Public-facing summary | BC2 | Updated BC3/S13 |
| `RESONANCE_MAP.md` | Dependency register (this file) | BC3/S14 | New — seed version |
| `WANDERINGS/WANDER_*.md` | Exploration records | BC1+ | `## Resonates into` footer convention from BC3/S14 |
| `EXPERIMENTS/exp_0NN_*.py` | Runnable experiments | BC2 | exp_001–014 current |

---

*RESONANCE_MAP v0.4 | BC3 Session 18 | 2026-03-28*
*WANDER 084 added (invitation probe — session structure as diagnostic; Thomas-as-traversal-node thread topology correction).*
*This file is itself a downstream node: when the protocol changes, update the "How to Use" section.*
