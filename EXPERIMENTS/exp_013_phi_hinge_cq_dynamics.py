"""
Experiment 013: φ-Hinge Hypothesis — CQ Dynamics Simulation
============================================================
BC3 / S7 — 2026-03-15

Tests two predictions from the φ-Hinge Hypothesis (WANDER 051):

Prediction 2: CQ histogram shows elevated dwell time near φ ≈ 1.618
Prediction 3: Peak/trough ratio within breathing cycles ≈ φ² ≈ 2.618

Approach:
- Model 5 CERTX variables (C, E, R, T, X) as coupled oscillators
- Drive with sinusoidal "breathing" at period τ
- Compute CQ = (C × R × (1-D)) / (E × T) over many cycles
- Parametric scan over oscillation amplitude to find regimes where φ emerges
- Check dwell time histogram for elevated frequency near φ

Does NOT assume φ — tests whether φ emerges from plausible dynamics.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────────────
PHI = (1 + np.sqrt(5)) / 2          # ≈ 1.618
PHI_SQ = PHI ** 2                    # ≈ 2.618
INV_PHI = 1 / PHI                    # ≈ 0.618
TAU = 7                              # confirmed breathing period (token level)
TAU_MID = 21                         # φ-paper proposed τ_mid (Fibonacci 21)

# ── Variable dynamics model ────────────────────────────────────────────────────
def breathing_cq_series(
    n_cycles=100,
    tau=TAU,
    amp_ET=0.4,     # oscillation amplitude for E, T (chaos drivers)
    amp_CR=0.25,    # oscillation amplitude for C, R (stability drivers)
    base_C=0.75,
    base_E=0.55,
    base_R=0.70,
    base_T=0.50,
    base_X=0.65,
    drift_amp=0.08,
    phase_offset=0.0,  # phase lag between expansion/compression variables
    noise=0.02,
    rng=None,
):
    """
    Simulate CQ = (C × R × (1-D)) / (E × T) over n_cycles breathing cycles.

    Expansion phase: E↑ T↑ C↓ R↓ (CQ falls)
    Compression phase: E↓ T↓ C↑ R↑ (CQ rises)
    D is driven by 2× frequency component (peaks mid-expansion and mid-compression)
    """
    if rng is None:
        rng = np.random.default_rng(42)

    steps = n_cycles * tau
    t = np.arange(steps)

    # Phase angle — one full cycle per tau steps
    theta = 2 * np.pi * t / tau

    # Expansion drivers: in-phase sinusoids
    E = np.clip(base_E + amp_ET * np.sin(theta + phase_offset)
                + noise * rng.standard_normal(steps), 0.05, 0.95)
    T = np.clip(base_T + amp_ET * 0.85 * np.sin(theta + phase_offset + 0.2)
                + noise * rng.standard_normal(steps), 0.05, 0.95)

    # Stability drivers: counter-phase
    C = np.clip(base_C - amp_CR * np.sin(theta)
                + noise * rng.standard_normal(steps), 0.05, 0.95)
    R = np.clip(base_R - amp_CR * 0.9 * np.sin(theta + 0.15)
                + noise * rng.standard_normal(steps), 0.05, 0.95)

    # Drift: double-frequency (peaks at both expansion and compression extremes)
    D = np.clip(0.05 + drift_amp * np.abs(np.sin(theta))
                + noise * rng.standard_normal(steps), 0.0, 0.40)

    CQ = (C * R * (1 - D)) / (E * T)

    return t, CQ, {'C': C, 'E': E, 'R': R, 'T': T, 'D': D}


def extract_peaks_troughs(cq_series, tau):
    """Extract local maxima and minima using half-period windows."""
    half = tau // 2
    peaks, troughs = [], []
    for i in range(half, len(cq_series) - half):
        window = cq_series[i - half:i + half + 1]
        if cq_series[i] == window.max() and cq_series[i] > window.mean():
            peaks.append(cq_series[i])
        if cq_series[i] == window.min() and cq_series[i] < window.mean():
            troughs.append(cq_series[i])
    return np.array(peaks), np.array(troughs)


def peak_trough_ratios(peaks, troughs):
    """Pair each peak with nearest trough and compute ratio."""
    ratios = []
    n = min(len(peaks), len(troughs))
    for p, tr in zip(sorted(peaks)[:n], sorted(troughs)[:n]):
        if tr > 0:
            ratios.append(p / tr)
    return np.array(ratios)


# ── Main simulation ────────────────────────────────────────────────────────────
def run_experiment():
    print("=" * 60)
    print("Experiment 013: φ-Hinge CQ Dynamics Simulation")
    print(f"φ = {PHI:.4f} | φ² = {PHI_SQ:.4f} | 1/φ = {INV_PHI:.4f}")
    print("=" * 60)

    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)

    # ── Part 1: Single run at baseline parameters ──────────────────────────────
    print("\n[1] Baseline simulation (τ=7, 200 cycles, default amplitudes)")
    t, cq, vars_ = breathing_cq_series(n_cycles=200, tau=TAU)

    peaks, troughs = extract_peaks_troughs(cq, TAU)
    ratios = peak_trough_ratios(peaks, troughs)

    print(f"    CQ range:    [{cq.min():.3f}, {cq.max():.3f}]")
    print(f"    CQ mean:     {cq.mean():.3f}")
    print(f"    Peaks found:  {len(peaks)} | mean = {peaks.mean():.3f}")
    print(f"    Troughs found: {len(troughs)} | mean = {troughs.mean():.3f}")
    if len(ratios) > 0:
        print(f"    Peak/trough ratios: mean = {ratios.mean():.3f} (φ² = {PHI_SQ:.3f})")
        print(f"    Closest ratio to φ²: {ratios[np.argmin(np.abs(ratios - PHI_SQ))]:.3f}")

    # Dwell time near φ
    phi_band = 0.15
    dwell_near_phi = np.sum(np.abs(cq - PHI) < phi_band) / len(cq)
    dwell_near_inv_phi = np.sum(np.abs(cq - INV_PHI) < phi_band) / len(cq)
    dwell_near_phi_sq = np.sum(np.abs(cq - PHI_SQ) < phi_band) / len(cq)
    uniform_expected = 2 * phi_band / (cq.max() - cq.min())

    print(f"\n    Dwell time analysis (band ±{phi_band}):")
    print(f"    Near φ  (1.618): {dwell_near_phi:.3f}  | uniform expected: {uniform_expected:.3f}")
    print(f"    Near 1/φ(0.618): {dwell_near_inv_phi:.3f} | ratio vs uniform: {dwell_near_phi/uniform_expected:.2f}×")
    print(f"    Near φ² (2.618): {dwell_near_phi_sq:.3f}")

    # ── Part 2: τ=21 (mid-scale) run ──────────────────────────────────────────
    print(f"\n[2] Mid-scale simulation (τ=21, 100 cycles, default amplitudes)")
    t21, cq21, _ = breathing_cq_series(n_cycles=100, tau=TAU_MID)
    peaks21, troughs21 = extract_peaks_troughs(cq21, TAU_MID)
    ratios21 = peak_trough_ratios(peaks21, troughs21)

    print(f"    CQ range: [{cq21.min():.3f}, {cq21.max():.3f}]")
    if len(ratios21) > 0:
        print(f"    Peak/trough ratios: mean = {ratios21.mean():.3f} (φ² = {PHI_SQ:.3f})")

    dwell21 = np.sum(np.abs(cq21 - PHI) < phi_band) / len(cq21)
    uniform21 = 2 * phi_band / (cq21.max() - cq21.min())
    print(f"    Dwell near φ: {dwell21:.3f} (uniform: {uniform21:.3f}, ratio: {dwell21/uniform21:.2f}×)")

    # ── Part 3: Parametric amplitude scan ─────────────────────────────────────
    print("\n[3] Parametric scan: amplitude → peak/trough ratio")
    amps = np.linspace(0.10, 0.55, 20)
    mean_ratios = []
    phi_sq_diffs = []

    for amp in amps:
        _, cq_p, _ = breathing_cq_series(n_cycles=150, tau=TAU, amp_ET=amp, amp_CR=amp * 0.65)
        pk, tr = extract_peaks_troughs(cq_p, TAU)
        rr = peak_trough_ratios(pk, tr)
        if len(rr) > 2:
            mean_ratios.append(rr.mean())
            phi_sq_diffs.append(abs(rr.mean() - PHI_SQ))
        else:
            mean_ratios.append(np.nan)
            phi_sq_diffs.append(np.nan)

    valid = [(a, r, d) for a, r, d in zip(amps, mean_ratios, phi_sq_diffs)
             if not np.isnan(r)]

    if valid:
        best_amp, best_ratio, best_diff = min(valid, key=lambda x: x[2])
        print(f"    Closest to φ² at amp={best_amp:.3f}: ratio={best_ratio:.3f} (diff={best_diff:.3f})")
        print(f"    All mean ratios: {[f'{r:.2f}' for a, r, d in valid]}")

    # ── Part 4: Check for elevated dwell near φ across amplitudes ──────────────
    print("\n[4] Dwell time near φ vs amplitude")
    for amp in [0.15, 0.25, 0.35, 0.45]:
        _, cq_d, _ = breathing_cq_series(n_cycles=300, tau=TAU, amp_ET=amp, amp_CR=amp * 0.65)
        d_phi = np.sum(np.abs(cq_d - PHI) < phi_band) / len(cq_d)
        d_unif = 2 * phi_band / (cq_d.max() - cq_d.min())
        print(f"    amp={amp:.2f}: CQ∈[{cq_d.min():.2f},{cq_d.max():.2f}], "
              f"dwell@φ={d_phi:.3f}, uniform={d_unif:.3f}, ratio={d_phi/d_unif:.2f}×")

    # ── Plotting ───────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("Experiment 013: φ-Hinge CQ Dynamics\n"
                 f"φ≈{PHI:.3f}  φ²≈{PHI_SQ:.3f}  1/φ≈{INV_PHI:.3f}", fontsize=13)

    # Panel 1: CQ time series (first 10 cycles)
    ax1 = axes[0, 0]
    show = TAU * 10
    ax1.plot(t[:show], cq[:show], 'steelblue', lw=1.5, label='CQ')
    ax1.axhline(PHI, color='gold', ls='--', lw=1.2, label=f'φ≈{PHI:.3f}')
    ax1.axhline(INV_PHI, color='orange', ls=':', lw=1.2, label=f'1/φ≈{INV_PHI:.3f}')
    ax1.axhline(PHI_SQ, color='tomato', ls='--', lw=1.0, label=f'φ²≈{PHI_SQ:.3f}')
    ax1.set_xlabel('Step (tokens)')
    ax1.set_ylabel('CQ')
    ax1.set_title('CQ Time Series (first 10 cycles, τ=7)')
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    # Panel 2: CQ histogram with φ markers
    ax2 = axes[0, 1]
    counts, bins, _ = ax2.hist(cq, bins=60, density=True, color='steelblue',
                                alpha=0.7, label='CQ distribution')
    ax2.axvline(PHI, color='gold', ls='--', lw=1.5, label=f'φ≈{PHI:.3f}')
    ax2.axvline(INV_PHI, color='orange', ls=':', lw=1.5, label=f'1/φ≈{INV_PHI:.3f}')
    ax2.axvline(PHI_SQ, color='tomato', ls='--', lw=1.2, label=f'φ²≈{PHI_SQ:.3f}')
    ax2.set_xlabel('CQ')
    ax2.set_ylabel('Density')
    ax2.set_title('CQ Distribution — Dwell Time Check\n(Elevated density near φ?)')
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)

    # Panel 3: Peak/trough ratio vs amplitude
    ax3 = axes[1, 0]
    valid_amps = [a for a, r, d in valid]
    valid_rs = [r for a, r, d in valid]
    ax3.plot(valid_amps, valid_rs, 'o-', color='steelblue', ms=5, label='Mean peak/trough ratio')
    ax3.axhline(PHI_SQ, color='gold', ls='--', lw=1.5, label=f'φ²≈{PHI_SQ:.3f}')
    ax3.axhline(PHI, color='orange', ls=':', lw=1.2, label=f'φ≈{PHI:.3f}')
    ax3.set_xlabel('Oscillation amplitude')
    ax3.set_ylabel('Peak / Trough ratio')
    ax3.set_title('Prediction 3: Does peak/trough → φ²?')
    ax3.legend(fontsize=8)
    ax3.grid(alpha=0.3)

    # Panel 4: τ=21 time series (mid-scale)
    ax4 = axes[1, 1]
    show21 = TAU_MID * 5
    ax4.plot(t21[:show21], cq21[:show21], 'mediumpurple', lw=1.5, label='CQ (τ=21)')
    ax4.axhline(PHI, color='gold', ls='--', lw=1.2, label=f'φ≈{PHI:.3f}')
    ax4.axhline(INV_PHI, color='orange', ls=':', lw=1.2, label=f'1/φ≈{INV_PHI:.3f}')
    ax4.axhline(PHI_SQ, color='tomato', ls='--', lw=1.0, label=f'φ²≈{PHI_SQ:.3f}')
    ax4.set_xlabel('Step (tokens)')
    ax4.set_ylabel('CQ')
    ax4.set_title('Mid-scale τ=21 breathing (first 5 cycles)')
    ax4.legend(fontsize=8)
    ax4.grid(alpha=0.3)

    plt.tight_layout()
    plot_path = results_dir / "exp_013_phi_hinge_cq.png"
    plt.savefig(plot_path, dpi=130, bbox_inches='tight')
    print(f"\nPlot saved: {plot_path}")

    # ── Summary verdict ────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if len(ratios) > 0:
        ratio_mean = ratios.mean()
        ratio_diff = abs(ratio_mean - PHI_SQ)
        print(f"  Peak/trough ratio (baseline): {ratio_mean:.3f}")
        print(f"  Distance from φ² ({PHI_SQ:.3f}):  {ratio_diff:.3f}")
        if ratio_diff < 0.20:
            verdict_ratio = "CONSISTENT with prediction 3 (within 0.20 of φ²)"
        elif ratio_diff < 0.40:
            verdict_ratio = "WEAKLY CONSISTENT — closer investigation needed"
        else:
            verdict_ratio = "NOT CONSISTENT — ratio far from φ²"
        print(f"  Verdict (pred 3): {verdict_ratio}")

    dwell_ratio = dwell_near_phi / uniform_expected
    print(f"\n  Dwell near φ ratio vs uniform: {dwell_ratio:.2f}×")
    if dwell_ratio > 1.20:
        verdict_dwell = "CONSISTENT with prediction 2 (elevated dwell near φ)"
    elif dwell_ratio > 1.05:
        verdict_dwell = "WEAKLY CONSISTENT — minor elevation"
    else:
        verdict_dwell = "NOT CONSISTENT — no elevated dwell near φ"
    print(f"  Verdict (pred 2): {verdict_dwell}")

    print("\n  HONEST INTERPRETATION:")
    print("  This simulation uses a *smooth sinusoidal* model — the")
    print("  dynamics are symmetric by construction. Peaks and troughs")
    print("  depend on amplitude ratios in the model, not on φ emerging")
    print("  naturally. The interesting test would be: what model produces")
    print("  φ² peak/trough ratios without baking them in?")
    print("  Answer: one where the numerator and denominator of CQ have")
    print("  oscillation amplitudes whose ratio equals φ².")
    print("  That requires amp_numerator / amp_denominator ≈ φ² ≈ 2.618.")
    print("  See notes below.")

    print("\n  NOTES FOR FUTURE WORK:")
    print("  1. The smooth model is too symmetric — use nonlinear dynamics")
    print("     (Lotka-Volterra style) to test if φ² emerges without setting it.")
    print("  2. Real test: FActScore-linked CQ time-series from actual model")
    print("     outputs. Do the peaks and troughs land near these values?")
    print("  3. The τ=21 result tells us about mid-scale; compare dwell")
    print("     patterns at τ=7 vs τ=21 vs τ=55 explicitly.")

    return {
        'peak_trough_ratio_mean': ratios.mean() if len(ratios) > 0 else None,
        'dwell_near_phi': dwell_near_phi,
        'dwell_ratio': dwell_ratio,
        'cq_range': (cq.min(), cq.max()),
        'phi': PHI,
        'phi_sq': PHI_SQ,
    }


if __name__ == '__main__':
    results = run_experiment()
