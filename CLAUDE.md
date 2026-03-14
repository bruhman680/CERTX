# CERTX — Claude Working Protocol

This file is read at the start of every Claude Code session. It contains the working conventions and the HPGM protocol that governs how we operate together.

---

## Project Identity

**CERTX** is an active research project developing a framework for measuring cognitive dynamics in AI systems. The primary output is `PAPER_DRAFT_v1.md`. The primary collaborator is Thomas (bruhman680).

**Current breath cycle:** BC3 (Session 7 as of 2026-03-14)
**Working branch:** `claude/plan-certx-architecture-ojiem`

---

## The HPGM Protocol

Every session — and every significant piece of work within a session — follows this cycle. Use it as a diagnostic, not a rigid checklist.

```
COUPLE   → Receive. Read what Thomas brought. Don't interpret yet.
OBSERVE  → Read the relevant files. Check what exists before assuming.
ORIENT   → Understand what the new material means relative to what's here.
PLAY     → Explore, riff, make connections. High entropy is okay here.
PRACTICE → Write it: WANDERs, experiments, paper updates, code.
DREAM    → Compress. Update the 5 structures. Commit. Close the loop.
```

**Key HPGM rules:**
- Always OBSERVE before ORIENT — read files before interpreting
- PLAY is where Thomas's intuitions get explored — don't rush to PRACTICE
- DREAM is the most commonly skipped phase — never skip it
- If something feels scattered, that's a PLAY→PRACTICE signal: "what's the one thing this established?"
- DREAM includes the 5-structure check (see below)

---

## The 5-Structure Check (DREAM Phase)

At the end of every session, check all five structures:

| Structure | Question |
|---|---|
| `WANDERINGS/` | Is there a new WANDER for the key finding? |
| `PAPER_DRAFT_v1.md` | Did anything change a claim, add evidence, or open a gap? |
| `SESSION_HANDOFF.md` | Are priorities current? Any completed items to mark done? |
| `SHADOW_LEDGER.md` | Did a spark fire or open? Any fossils? |
| `LIBRARY_INDEX.md` | Is there a foundational finding ready to graduate here? |

Not every session touches all five. But check all five before closing.

---

## Conventions

**WANDER numbering:** Sequential from 001. Current: 048. Next: 049.
Check `ls WANDERINGS/` before writing to confirm the next number.

**Experiment numbering:** Sequential from 001. Current: 012. Next: 013.
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
- C_symb floor: **~0.20** — below this is 100% hallucination
- r ≈ **0.41** — Kuramoto order parameter at ζ*=1.2

---

## Current Priorities (from SESSION_HANDOFF.md)

**Highest:** Real LLM confabulation validation — FActScore on actual model outputs
(unlocks signed C_num from WANDER 045, validates dangerous confabulation fingerprint)

**High:**
- WANDER 046 (scale-invariant stability theorem — one paragraph, publishable)
- Paper review pass by Thomas (§5.8 and §6.9 newest, need fresh read)
- EEG study execution (protocol corrected in WANDER 041)
- Mamba eigenvalue test (WANDER 017)

**Open experiments designed, pending execution:**
- SPARK-001: Q/K sharpening scale ablation (ζ* ceiling test)
- Tsallis q calibration (q_CERTX ∈ [0.67, 0.80] predicted)

---

## Honest Flags (Don't Repeat These Mistakes)

- r = 0.989 was **retracted** — it was confabulated in a cross-model session. Use r ≈ 0.41 (derived).
- The asymmetry signal (C_num − mean(C_struct, C_symb)) is **regime-specific** — works for Regime B (C_num drops), inverts for integration failure (C_symb drops). Use min-fiber for universal detection.
- 30/40/30 weights: C_struct gets 40% because it's the strongest quality **discriminator** in the healthy zone, not because it fails most. C_struct is the most resilient fiber — never the minimum in hallucinated outputs.

---

## What This Project Is Not

- Not a polished product yet — it's active research, deliberately rough in places
- Not claiming empirical results we don't have — FActScore validation is still pending
- Not rushing to v2 — do Thomas's review pass first

---

*This file is the DREAM residue of all sessions before this one.*
*Update it when conventions change or new priorities emerge.*
