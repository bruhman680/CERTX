# Does neighborhood information beat ordinary temporal smoothing?

**One completed discriminating research loop.** Pre-outcome specification: `SOCIAL2_LAG_PLAN.md`. Source: `SOCIAL2_LAG_probe.py`. Full seed rows: `SOCIAL2_LAG_results.json`. Twelve fresh paired seeds 11000–11011 × 2 regrowth regimes × 8 observation arms, each 1,500 neural-training ticks plus 2,000 frozen deterministic deployment ticks. **192 matched deployments**, not 192 research loops. Per-cell neural weights were checked unchanged after evaluation; the historic Living Garden was not touched.

Each supplement contributes 50% to the resource observation (other 50% is own current resource). All copying/message rules are hand-coded and causal (no future data).

| Supplement to current own resource | Stable mean energy at t2000 | Stable floor share | Mild-shift mean energy | Mild floor share |
| --- | ---: | ---: | ---: | ---: |
| None: own current only | .1653 | .130 | .0176 | .325 |
| Own resource, one step old | .1080 | .197 | .0221 | .344 |
| **Neighborhood mean, one step old** | **.2080** | .065 | .0284 | .329 |
| Neighborhood mean, current | .1952 | .084 | .0235 | .314 |
| Globally shuffled cell, one step old | .1743 | .079 | .0194 | .332 |
| Neighborhood mean, five steps old | .1434 | .126 | .0199 | .340 |
| Own resource, five steps old | .1141 | .067 | **.0299** | **.215** |
| Neighborhood mean with time lag shuffled 1–5 | .2053 | **.050** | .0281 | .295 |

In the stable regime, one-step-stale neighborhood mean outperformed both own-one-step temporal smoothing and globally shuffled stale observations in **12/12 paired seeds**. It also outperformed current neighborhood mean in aggregate. This supports a **spatial signal contribution** for this frozen neural controller beyond generic input smoothing under stable rules.

In the mild regrowth-shift regime, one-step-stale neighborhood information still outperformed own-one-step averaging in 11/12 seeds and global-old placebo in 12/12. But the strong *own-five-step-lag* control attained mean energy .0299 and 21.5% floor, versus .0284 and 32.9% floor for neighbor-one-step. Hence **timing/lag structure itself is a competing explanation**, especially after the shift. The original shifted baseline remains near depletion. This is not sustained high-energy self-repair.

At t500, stable own-only .0805, stale-neighbor .1364, own-stale .0647, global-stale .1053; mild own-only .0175, stale-neighbor .0270, own-stale .0217, global-stale .0196. Thus the stable spatial difference is evident before the 2,000-tick horizon.

**FRR interpretation:** The cell's policy is learned, but *who and when to listen* is designer-specified. The observation can gain value by carrying locally coupled environmental state—yet a delayed observation can also change policy phase or smooth oscillatory resource signals. No spontaneous communication, learned social learning, or collective intelligence has been demonstrated. The original earlier finding 'fresher information is always better' does not generalize from direct resource targeting to this learned classifier; these are different controllers.

**Next test burden:** Factor spatial radius and lag jointly on stable and shifted worlds; add local-shuffle maintaining marginal distributions but breaking actual neighbor identity; measure per-action resource yield and first-order autocorrelation to explain which phase shifts improve behavior. Test a small information-gated feature only after these controls. Avoid premature claims about emergent distributed memory.

