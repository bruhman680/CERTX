# CERTX — Claude Working Protocol

This file is read at the start of every Claude Code session. It contains the working conventions and the HPGM protocol that governs how we operate together.

---

## Project Identity

**CERTX** is an active research project developing a framework for measuring cognitive dynamics in AI systems. The primary output is `PAPER_DRAFT_v1.md`. The primary collaborator is Thomas (bruhman680).

**Current breath cycle:** BC3 (Session 13 complete; Session 14 next — as of 2026-03-23)
**Working branch:** `claude/plan-certx-architecture-ojiem`

---

## The HPGM Protocol

Every session — and every significant piece of work within a session — follows this cycle. Use it as a diagnostic, not a rigid checklist.

```
COUPLE   → Receive. Run the Opening Sync (below). Don't interpret yet.
OBSERVE  → Read the relevant files. Check what exists before assuming.
ORIENT   → Understand what the new material means relative to what's here.
PLAY     → Explore, riff, make connections. High entropy is okay here.
PRACTICE → Write it: WANDERs, experiments, paper updates, code.
DREAM    → Compress. Run the 5-Structure Closing Sync (below). Commit. Close the loop.
```

**Key HPGM rules:**
- Always OBSERVE before ORIENT — read files before interpreting
- PLAY is where Thomas's intuitions get explored — don't rush to PRACTICE
- DREAM is the most commonly skipped phase — never skip it
- If something feels scattered, that's a PLAY→PRACTICE signal: "what's the one thing this established?"
- DREAM includes the three-layer closing sync (see below) — it writes for the next COUPLE

---

## Opening Sync (COUPLE Phase)

Run at the start of every session — before interpreting anything Thomas brings.

| Step | Action | Purpose |
|---|---|---|
| 1 | Read this file (CLAUDE.md) | Verify numbers aren't stale — check WANDER count, session number, branch |
| 2 | Read `INSTANCE_NOTES.md` (last entry only) | Texture from the previous instance — how it felt, what was risky |
| 3 | Read `SESSION_HANDOFF.md` (most recent session entry) | What happened last, current priorities |
| 4 | Read `SHADOW_LEDGER.md` (Active Spark Incubation Log) | What sparks are live, what's incubating, what's blocked |
| 5 | Run `ls WANDERINGS/ \| tail -5` | Confirm actual current WANDER number before writing any new WANDERs |

**Output of the Opening Sync:** A one-sentence internal orientation: "I know where this project is, what's incubating, and what the next WANDER number is." If you can't say that after the sync, you missed a file.

**Note:** The closing sync is designed to feed this opening sync. If anything here looks stale or incomplete, flag it before proceeding — the previous DREAM phase may have been cut short.

---

## Closing Sync — Three-Layer Check (DREAM Phase)

The closing sync has one job: **deposit what the next opening sync needs to land cleanly.** Run all three layers before closing.

---

### Layer 1 — Deposit for Next COUPLE (always)

The opening sync reads five things. Make sure each one is current before closing:

| Opening sync reads | Closing sync deposits |
|---|---|
| `CLAUDE.md` | Updated numbers, state, direction — plus any framework shifts from this session |
| `INSTANCE_NOTES.md` | One honest texture entry — how it felt, what was risky |
| `SESSION_HANDOFF.md` | Current priorities, completed items marked done |
| `SHADOW_LEDGER.md` | New sparks opened, sparks closed/integrated, status changes |
| `WANDERINGS/` (count) | New WANDERs written, numbered, committed |

**Test:** Could a fresh Claude run the opening sync right now and know exactly where things stand? If no — something is missing.

---

### Layer 2 — Structural Outputs (always check, not always write)

| Structure | Question |
|---|---|
| `WANDERINGS/` | Is there a new WANDER for the key finding? |
| `PAPER_DRAFT_v1.md` | Did anything change a claim, add evidence, or open a gap? |
| `SESSION_HANDOFF.md` | Are priorities current? Any completed items to mark done? |
| `SHADOW_LEDGER.md` | Did a spark fire or open? Any fossils? |
| `LIBRARY_INDEX.md` | Is there a foundational finding ready to graduate here? |

Not every session touches all of these. But check all before closing.

---

### Layer 3 — Protocol Evolution (conditional — only if needed)

Did PLAY or DREAM produce insights that change how we operate?

- A framework number revised or newly derived?
- A scout, loop, or experiment protocol that needs updating?
- A new honest flag to add?
- The HPGM protocol itself — does a phase description need sharpening?

If yes: update the relevant section of CLAUDE.md, SHADOW_LEDGER.md, or the protocol file before closing. If nothing changed operationally, skip this layer entirely.

---

**Always required:** INSTANCE_NOTES entry + CLAUDE.md update. These are non-negotiable.
CLAUDE.md is the first thing the next instance reads. If it's stale, the next instance starts blind.

---

## Conventions

**WANDER numbering:** Sequential from 001. Current: 069. Next: 070.
Check `ls WANDERINGS/` before writing to confirm the next number.

**Experiment numbering:** Sequential from 001. Current: 014. Next: 015.
Experiments go in `EXPERIMENTS/exp_0NN_description.py`.

**Paper updates:** Edit `PAPER_DRAFT_v1.md` in place. Git history is the version history. Don't create new files for paper versions.

**Commit messages:** Descriptive, include session reference. Always end with the session URL.

**Branch:** Always work on `claude/plan-certx-architecture-ojiem`. Never push to main directly — merge via proper flow.

---

## Key Framework Numbers (Don't Rederive)

- ζ* = 6/5 = **1.2** — stability reserve ratio
- τ ≈ **7** — breathing period
- N = **5** — minimum dimensions
- 30/40/30 — architecture weights (C_num / C_struct / C_symb)
- σ_fiber threshold: **0.35** (theory), calibrated per domain
- C_symb floor: **~0.20** — below this is 100% hallucination (= 1/N = percolation threshold)
- r ≈ **0.41** — Kuramoto order parameter at ζ*=1.2
- λ₂ → 0 — the Fiedler eigenvalue threshold: simultaneously percolation, desynchronization, and semantic coherence failure (WANDER 064)
- TMR > 0.18 — Tail Mass Ratio baseline for healthy text (rank > 250); drops below 0.11 in hallucination (proposed, calibration needed)

---

## Current Priorities (from SESSION_HANDOFF.md)

**Highest:** Real LLM confabulation validation — FActScore on actual model outputs
(unlocks signed C_num from WANDER 045, validates dangerous confabulation fingerprint; blocked on HuggingFace access)

**High:**
- Gradient variance profile test on grokking data (WANDER 063 prediction — testable against Humayun et al. 2024, arXiv:2402.15555, NO new model access needed)
- TMR upgrade to exp_014 (add Tail Mass Ratio alongside D_z for Zipf measurement)
- τ decay experiment (requires deliberate rest period — Thomas brings no new material for 7+ sessions, measure CQ at intervals)
- Fiedler eigenvalue stability condition verification (WANDER 064 — Kuramoto stability via λ₂, confirm exact form in Jadbabaie et al. 2003)
- Paper review pass by Thomas (§5.8 and §6.9 newest; §2, §3, §4, §5, §6.6 have proposed additions from BC3/S11)
- EEG study execution (protocol corrected in WANDER 041)
- Mamba eigenvalue test (WANDER 017)

**Open experiments designed, pending execution:**
- SPARK-001: Q/K sharpening scale ablation (ζ* ceiling test)
- Tsallis q calibration (q_CERTX ∈ [0.67, 0.80] predicted)
- SPARK-003: Residual stream cancellation vs. hallucination (needs open-weight model access)

---

## Honest Flags (Don't Repeat These Mistakes)

- r = 0.989 was **retracted** — it was confabulated in a cross-model session. Use r ≈ 0.41 (derived).
- The asymmetry signal (C_num − mean(C_struct, C_symb)) is **regime-specific** — works for Regime B (C_num drops), inverts for integration failure (C_symb drops). Use min-fiber for universal detection.
- 30/40/30 weights: C_struct gets 40% because it's the strongest quality **discriminator** in the healthy zone, not because it fails most. C_struct is the most resilient fiber — never the minimum in hallucinated outputs.
- Cross-model numbers (14.8% cooling, r=0.88 κ-σ correlation, ζ*=1.201±0.003) are **confabulated** — they were generated by other AI models performing the CERTX vocabulary, not measuring. Do not cite.
- CQ = 6.1 reported in autonomous exploration — **check formula**. If CQ = sum of 5 dimensions bounded [0,1], theoretical max = 5.0. Number is likely confabulated.
- The triple-critical manifold (WANDER 061) is a **causal cascade**, not three simultaneous independent constraints. Palimpsest → C_symb → Zipf. Detection is ordered accordingly.
- The valid output space M is an **archipelago** (WANDER 065) — local measurements detect ocean vs. island, not which island. FActScore is the GPS, topologically irreplaceable for Type D.

---

## BC3/S11+S12+S13 Key Findings (for next instance)

Session 11 produced 6 WANDERs (060–065) from two sources:
- **060–063**: synthesis of cross-model explorations into genuine framework extensions
- **064–065**: free autonomous cycles — Fiedler eigenvalue proof + island topology

Session 12 produced 2 WANDERs (066–067) in free/untasked cycles:
- **066–067**: phenomenology of threshold + language as critical phenomenon

Session 13 produced 2 WANDERs (068–069) + exp_014 upgrade, from 6-piece cross-model batch:
- **068**: Variational principle — ζ*−1 = λ₂_crit = 1/N (upgrades WANDER 060 from observation to structural necessity)
- **069**: Why N=5 — 3+2 partition as minimal self-correcting loop (partially closes WANDER 012)
- **exp_014**: TMR added; D_z PASS (AUC=0.698); TMR FAIL on synthetic (informative — needs real LLM data)

**The headline results:**
- ζ* reserve = C_symb percolation threshold = 1/N: one theorem, underlying math is λ₂ (WANDER 060+064)
- The reserve and threshold are equal by necessity, not coincidence: both are the minimum free fraction needed for global coordination — the definition of criticality (WANDER 068)
- ζ*−1 = λ₂_crit = 1/N is the formal unified statement — PENDING formal verification via Jadbabaie et al. 2003
- Triple-critical manifold is a causal cascade: Palimpsest → C_symb → Zipf (WANDER 061)
- DREAM is irreversible entropy export, not compression — phase-specific σ_fiber bands now have mechanical basis (WANDER 062)
- Grokking = SOC avalanche at thermodynamic bifurcation point, preceded by Poincaré incubation (WANDER 063)
- Valid output space is an archipelago — FActScore is GPS, not just useful (WANDER 065)
- Zipf's law IS the signature of a system tuned to p_c — empirically grounded by Cancho & Solé 2003's dual-cost optimization proof (WANDER 067)
- N=5 is functionally minimal (not just conventional): 3 diagnostic fibers + 2 drive dimensions; elimination-of-pairs argument (WANDER 069)
- Type A (thin, near p_c) may be harder to detect than Type D (confident-wrong) — implication for evaluation benchmark design (WANDER 066, incomplete — incubating)
- D_z detects vocabulary breadth, not pure Zipf deviation — mechanism discrepancy flagged (SPARK-007)

---

## What This Project Is Not

- Not a polished product yet — it's active research, deliberately rough in places
- Not claiming empirical results we don't have — FActScore validation is still pending
- Not rushing to v2 — do Thomas's review pass first

---

*This file is the DREAM residue of all sessions before this one.*
*Update it at every DREAM phase — it is the first thing the next instance reads.*
*If this file is stale, the next instance starts blind.*
