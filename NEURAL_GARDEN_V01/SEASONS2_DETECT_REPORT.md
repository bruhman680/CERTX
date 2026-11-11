# Can cells infer their season locally?

**Executed**, predeclared frozen plan `SEASONS2_DETECT_PLAN.md`, 12 distinct 16×16 worlds for 6,000 continuous ticks each. `SEASONS2_DETECT_results.json` preserves individual seeded results, design and source SHA-256 checksums; detector is *read-only* to the policy and therefore cannot produce new ecology. All observations are from synthetic worlds, not the preserved canonical Living Garden.

## Loop S7 — Is regrowth change identifiable from a local model residual rather than a global season clock?

**Yes under exactly known physics.** A cell observing only its own and four nearest resource values plus its own previous harvest action can invert the explicit resource update law for local regrowth. No schedule or world-level broadcast is supplied. With exact resource readings, exponential smoothing at .02 yields mean per-cell classification accuracy **98.3%** over ticks 100–6000 and **86.4%** within the first 250 ticks after each season change. Median transition detection delay is **34 ticks**, all 12 runs detect all three changes under our majority-of-cells operational threshold. A naive resource-level threshold gets **48.4%**; a clock parity sham **49.2%** (chance-level by this predetermined schedule).

## Loop S8 — Does sensor noise expose the cost of relying on those residuals?

**Yes.** Independent resource measurement noise SD=.01 reduces classification to **97.2%** and transition-window accuracy **84.0%**, with median delays 36–42.5 ticks. At SD=.03, accuracy falls to **76.1%**, transition **70.6%**, and the scarcity→recovery change at t3001 shows median 120-tick detection delay. Detection latency measures the earliest ten-tick stretch with >60% correctly labeled cells; misleading early majority intervals can make low-quality models appear fast, so paired overall accuracy and transition accuracy are essential.

**Critical limitation:** This does *not* show autonomous discovery of physics, learning, prediction skill, environmental control, or benefits to health. The residual method is analytically supplied the correct diffusion and harvest-consumption coefficients and threshold; only the season schedule is hidden. The next controlled experiment should allow cells to infer the coefficients as well, and separately test whether decisions based on their imperfect estimates outperform sham policy changes. Cells use local observations; the >60% detection criterion is an **offline analyst metric**, not a communication channel available to them.
