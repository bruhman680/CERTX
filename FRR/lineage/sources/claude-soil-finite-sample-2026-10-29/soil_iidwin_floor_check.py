"""Explain the Part-B iid-window floor: for a shadow trajectory the soil level is fixed, so every window is iid Bernoulli(p_level) errors.
Per-window expected log-likelihood ratio of the iid-window classifier (SH window law vs WK window law, n=16, stationary starts), conditional on each SH soil level.
PREDICTION (before running): at least one soil level has NEGATIVE expected LLR (favours WK), so an iid-product classifier is wrong with certainty on that half of SH trajectories as the number of windows grows; overall SH-WK error floor near 25%."""
import io, contextlib, numpy as np
src = open('soil_finite_sample.py').read().split('# ---------------- PART A')[0]
ns = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, ns)
wp, W = ns['word_probs'], ns['W']
n = 16; PS, PW = wp('SH', n, 'PASS'), wp('WK', n, 'PASS')
codes = np.arange(2**n); k = np.array([bin(c).count('1') for c in codes])
llr = np.log(PS)-np.log(PW)
for lvl in W['SH']['P']:
    pw = lvl**k*(1-lvl)**(n-k); e = np.sum(pw*llr)
    print(f"SH soil level {lvl:.4f}: E[log P_SH_win/P_WK_win] per window = {e:+.5f} (positive favours the correct SH)")
# and for WK trajectories under the iid-window rule: window law is the stationary WK mixture itself; E = KL(P_WK || P_SH) via law-of-windows is not exactly iid, report marginal-window value
print("marginal-window E_WK[log P_WK/P_SH] =", float(np.sum(PW*(np.log(PW)-np.log(PS)))))
