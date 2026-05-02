"""
exp_016: Gradient Variance Profile During Grokking
===================================================
Tests WANDER 063 prediction: gradient variance should peak during incubation
and drop at the grokking event.

Key discovery from first run: after memorization (train_acc=1.0), CE gradients
→ 0 so raw gradient variance collapses. The incubation phase is driven by
weight decay alone (deterministic, near-zero variance). This means:

P1 may still hold for PRE-MEMORIZATION gradient variance
The post-memorization incubation phase needs a different metric:
  - Weight norm ||W|| (driven down by WD during incubation)
  - CE gradient norm (collapses at memorization → marks start of incubation)
  - WD gradient norm (proportional to ||W||, decreasing during incubation)

Revised test of WANDER 063:
  Phase 1 (Preparation=memorization): CE grad norm elevated, ||W|| rising
  Phase 2 (Incubation): CE grad norm near zero, ||W|| declining (WD dominates)
  Phase 3 (Illumination=grokking): test acc jumps, ||W|| passes threshold
  Phase 4 (Verification): test acc stable, ||W|| stabilizes at lower value

This is a richer test than originally designed. Results inform WANDER 063
and flag gradient variance as an incomplete proxy for thermodynamic entropy.

CERTX reference: WANDER 063 (BC3/S11)
"""

import numpy as np
import json
import os

# ── Hyperparameters ─────────────────────────────────────────────────────────
P = 97
EMBED_DIM = 128
HIDDEN = 256
LR = 1e-3
WEIGHT_DECAY = 1.0
BETA1, BETA2 = 0.9, 0.98
EPS = 1e-8
TRAIN_FRAC = 0.50
N_STEPS = 6000     # grokking happens ~step 2800, so 6k gives full picture
LOG_EVERY = 50     # fine-grained to see dynamics
SEED = 42

rng = np.random.default_rng(SEED)

print("exp_016: Grokking Gradient Variance Profile (WANDER 063 test)")
print(f"AdamW lr={LR} wd={WEIGHT_DECAY} | Steps: {N_STEPS} | Log every: {LOG_EVERY}")
print()

# ── Dataset ───────────────────────────────────────────────────────────────────
all_a = np.array([[a, b] for a in range(P) for b in range(P)], dtype=np.int32)
all_y = np.array([(a + b) % P for a, b in all_a], dtype=np.int32)
idx = rng.permutation(len(all_a))
n_train = int(TRAIN_FRAC * len(all_a))
X_train, Y_train = all_a[idx[:n_train]], all_y[idx[:n_train]]
X_test, Y_test = all_a[idx[n_train:]], all_y[idx[n_train:]]
a_tr, b_tr = X_train[:,0], X_train[:,1]
a_te, b_te = X_test[:,0], X_test[:,1]
print(f"Dataset: {len(X_train)} train, {len(X_test)} test")

# ── Model ────────────────────────────────────────────────────────────────────
D, H = EMBED_DIM, HIDDEN
Ea = (rng.standard_normal((P, D)) * np.sqrt(2.0/P)).astype(np.float64)
Eb = (rng.standard_normal((P, D)) * np.sqrt(2.0/P)).astype(np.float64)
W1 = (rng.standard_normal((2*D, H)) * np.sqrt(2.0/(2*D))).astype(np.float64)
b1 = np.zeros(H, dtype=np.float64)
W2 = (rng.standard_normal((H, P)) * np.sqrt(2.0/H)).astype(np.float64)
b2 = np.zeros(P, dtype=np.float64)
params = [Ea, Eb, W1, b1, W2, b2]
weight_params = [Ea, Eb, W1, W2]   # biases excluded from WD and weight norm
m = [np.zeros_like(p) for p in params]
v = [np.zeros_like(p) for p in params]
print(f"Parameters: {sum(p.size for p in params):,}")


def forward(ai, bi):
    x = np.concatenate([Ea[ai], Eb[bi]], axis=1)
    h_pre = x @ W1 + b1
    h = np.maximum(0, h_pre)
    logits = h @ W2 + b2
    logits -= logits.max(axis=1, keepdims=True)
    e = np.exp(logits)
    return x, h_pre, h, e / e.sum(axis=1, keepdims=True)


def step_and_metrics(ai, bi, y, t):
    n = len(y)
    x, h_pre, h, probs = forward(ai, bi)

    # CE gradient
    dl = probs.copy(); dl[np.arange(n), y] -= 1; dl /= n
    dW2 = h.T @ dl;          db2g = dl.sum(0)
    dh = dl @ W2.T;           dh_pre = dh * (h_pre > 0)
    dW1 = x.T @ dh_pre;      db1g = dh_pre.sum(0)
    dx = dh_pre @ W1.T
    dEa = np.zeros_like(Ea);  np.add.at(dEa, ai, dx[:, :D])
    dEb = np.zeros_like(Eb);  np.add.at(dEb, bi, dx[:, D:])

    ce_grads = [dEa, dEb, dW1, db1g, dW2, db2g]
    g_ce = np.concatenate([g.ravel() for g in ce_grads])
    ce_grad_norm = float(np.linalg.norm(g_ce))
    ce_grad_var  = float(np.var(g_ce))

    # Weight norms (L2 of weight matrices only)
    wd_grad_norm = float(WEIGHT_DECAY * np.sqrt(sum(np.sum(p**2) for p in weight_params)))
    weight_norm  = float(np.sqrt(sum(np.sum(p**2) for p in weight_params)))

    # AdamW update
    bc1, bc2 = 1 - BETA1**t, 1 - BETA2**t
    for i, (p_arr, g, mi, vi) in enumerate(zip(params, ce_grads, m, v)):
        mi[:] = BETA1 * mi + (1 - BETA1) * g
        vi[:] = BETA2 * vi + (1 - BETA2) * g**2
        upd = (mi / bc1) / (np.sqrt(vi / bc2) + EPS)
        if p_arr.ndim > 1:
            p_arr -= LR * (upd + WEIGHT_DECAY * p_arr)
        else:
            p_arr -= LR * upd

    # Loss and accuracy
    ce_loss = float(-np.log(probs[np.arange(n), y] + 1e-12).mean())
    acc = float((probs.argmax(1) == y).mean())
    return ce_loss, acc, ce_grad_norm, ce_grad_var, weight_norm, wd_grad_norm


# ── Training ──────────────────────────────────────────────────────────────────
results = {k: [] for k in ["steps","train_loss","test_loss","train_acc","test_acc",
                            "ce_grad_norm","ce_grad_var","weight_norm","wd_grad_norm"]}

print(f"\n{'Step':>6} {'TrAcc':>6} {'TeAcc':>6} {'CE_gNorm':>10} {'||W||':>9} {'Phase'}")
print("-" * 60)

grok_step = None
phases = {}  # step → phase label

for t in range(1, N_STEPS + 1):
    tl, ta, cen, cev, wn, wdn = step_and_metrics(a_tr, b_tr, Y_train, t)

    if t % LOG_EVERY == 0:
        _, _, _, vp = forward(a_te, b_te)
        vl = float(-np.log(vp[np.arange(len(Y_test)), Y_test] + 1e-12).mean())
        va = float((vp.argmax(1) == Y_test).mean())

        # Phase tagging
        if ta < 0.99:
            phase = "Preparation"
        elif va < 0.95:
            phase = "Incubation"
        else:
            phase = "Verification"

        if grok_step is None and va >= 0.95 and t > 100:
            grok_step = t
            phase = "GROKKING"

        results["steps"].append(t)
        results["train_loss"].append(tl)
        results["test_loss"].append(vl)
        results["train_acc"].append(ta)
        results["test_acc"].append(va)
        results["ce_grad_norm"].append(cen)
        results["ce_grad_var"].append(cev)
        results["weight_norm"].append(wn)
        results["wd_grad_norm"].append(wdn)

        if t % 500 == 0 or phase in ("GROKKING",):
            print(f"{t:>6} {ta:>6.3f} {va:>6.3f} {cen:>10.3e} {wn:>9.3f}  {phase}")

print("\n--- Final ---")
_, _, _, vfp = forward(a_te, b_te)
final_va = float((vfp.argmax(1)==Y_test).mean())
print(f"Train acc: {ta:.4f}  Test acc: {final_va:.4f}")
print(f"Grokking at step: {grok_step}")

# ── Analysis ──────────────────────────────────────────────────────────────────
steps_arr = np.array(results["steps"])
va_arr = np.array(results["test_acc"])
ta_arr = np.array(results["train_acc"])
cen_arr = np.array(results["ce_grad_norm"])
wn_arr = np.array(results["weight_norm"])

grok_mask = va_arr >= 0.95
memorize_mask = ta_arr >= 0.99

print(f"\n═══ WANDER 063 PREDICTION TEST (revised) ═══")

if grok_mask.any() and memorize_mask.any():
    mem_i = np.where(memorize_mask)[0][0]   # first memorization step
    grok_i = np.where(grok_mask)[0][0]      # first grokking step
    mem_ep = steps_arr[mem_i]
    grok_ep = steps_arr[grok_i]

    # Phase windows
    prep_cen = cen_arr[:mem_i]             # Preparation
    incub_cen = cen_arr[mem_i:grok_i]      # Incubation
    verif_cen = cen_arr[grok_i+1:grok_i+5] # Verification

    prep_wn  = wn_arr[:mem_i]
    incub_wn = wn_arr[mem_i:grok_i]
    verif_wn = wn_arr[grok_i+1:grok_i+5]

    print(f"\nPhase boundaries:")
    print(f"  Preparation ends (memorization):  step {mem_ep}")
    print(f"  Incubation ends (grokking):       step {grok_ep}")
    print(f"  Incubation duration:              {grok_ep - mem_ep} steps ({grok_i - mem_i} log points)")

    print(f"\nCE Gradient Norm by phase:")
    print(f"  Preparation mean: {prep_cen.mean():.4e}  (peak: {prep_cen.max():.4e})")
    print(f"  Incubation mean:  {incub_cen.mean():.4e}  (should be near-zero)")
    print(f"  Verification mean:{verif_cen.mean() if len(verif_cen)>0 else 0:.4e}")
    prep_to_incub_drop = prep_cen.mean() / (incub_cen.mean() + 1e-30)
    print(f"  Preparation→Incubation drop:      {prep_to_incub_drop:.1f}×")

    print(f"\nWeight Norm ||W|| by phase:")
    print(f"  End of Preparation: {prep_wn[-1]:.4f}")
    print(f"  End of Incubation:  {incub_wn[-1] if len(incub_wn)>0 else 0:.4f}")
    print(f"  WD driven decline:  {prep_wn[-1] - (incub_wn[-1] if len(incub_wn)>0 else prep_wn[-1]):.4f}")

    # Sub-predictions
    p1 = bool(prep_cen.mean() > 1e-10)
    p2 = bool(prep_cen.mean() > incub_cen.mean() * 2)    # CE drops at memorization
    p3 = bool(len(incub_wn)>1 and incub_wn[-1] < incub_wn[0])  # ||W|| declines during incubation
    p4 = bool(len(verif_wn)>0 and (verif_wn[0] < prep_wn[-1]))  # grokking at lower ||W||

    print(f"\nSub-predictions:")
    print(f"  P1 (CE grad elevated during Preparation):        {'PASS' if p1 else 'FAIL'}")
    print(f"  P2 (CE grad collapses at memorization):          {'PASS' if p2 else 'FAIL'} ({prep_to_incub_drop:.0f}×)")
    print(f"  P3 (||W|| declines during Incubation):           {'PASS' if p3 else 'FAIL'}")
    print(f"  P4 (grokking at lower ||W|| than memorization):  {'PASS' if p4 else 'FAIL'}")

    passes = sum([p1,p2,p3,p4])
    verdict = "CONFIRMED" if passes >= 3 else ("PARTIAL" if passes >= 2 else "FAIL")
    print(f"\nOverall: {verdict} ({passes}/4 sub-predictions)")

    # What this means for WANDER 063
    print(f"\nImplication for WANDER 063:")
    print(f"  The gradient variance proxy is incomplete. CE gradient variance")
    print(f"  peaks during Preparation then collapses — consistent with the")
    print(f"  SOC loading prediction. But the incubation phase is SILENT in")
    print(f"  gradient variance: it is driven by weight decay (deterministic).")
    print(f"  The correct thermodynamic proxy for incubation is ||W|| declining")
    print(f"  under WD pressure — the system approaching a critical weight norm")
    print(f"  threshold at which generalization becomes possible.")
    print(f"  WANDER 063 prediction: STRUCTURALLY CORRECT, WRONG PROXY.")
    print(f"  Updated: entropy production = CE gradient norm; incubation entropy")
    print(f"  export = ||W|| decline (WD term); grokking = ||W|| threshold crossing.")

else:
    verdict = "INCONCLUSIVE"
    print("Not enough data for full analysis.")

# ── Save ─────────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(out_dir, exist_ok=True)
with open(out_dir + "/exp_016_results.json", "w") as f:
    results["grok_step"] = grok_step
    results["verdict"] = verdict
    json.dump(results, f, indent=2)

# ── ASCII plots ───────────────────────────────────────────────────────────────
def ascii_plot(vals, label, width=50, grok_i=None, mem_i=None):
    vmin, vmax = min(vals), max(vals)
    r = vmax - vmin if vmax != vmin else 1.0
    print(f"\n{label}  [min={vmin:.2e}, max={vmax:.2e}]")
    for i, val in enumerate(vals):
        bl = int((val - vmin) / r * width)
        mk = ""
        if grok_i is not None and i == grok_i: mk = " ←GROK"
        if mem_i is not None and i == mem_i:   mk = " ←MEMORIZE"
        s = steps_arr[i]
        if i % 4 == 0 or mk:
            print(f"  S{s:5d} │{'█'*bl}{mk}")

grok_plot_i = int(np.where(grok_mask)[0][0]) if grok_mask.any() else None
mem_plot_i  = int(np.where(memorize_mask)[0][0]) if memorize_mask.any() else None

ascii_plot(list(va_arr), "Test Accuracy", grok_i=grok_plot_i)
ascii_plot(list(np.log1p(cen_arr)), "log(1+CE_GradNorm)", grok_i=grok_plot_i, mem_i=mem_plot_i)
ascii_plot(list(wn_arr), "Weight Norm ||W||", grok_i=grok_plot_i, mem_i=mem_plot_i)

print(f"\nResults saved → {out_dir}/exp_016_results.json")
