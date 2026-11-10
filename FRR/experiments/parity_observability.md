# Exact observability audit: noisy eight-state parity register

**Scope:** Mathematical construction and exact rational finite-state calculation, not an empirical claim about cognition.  
**Reproduction:** `python3 parity_observability.py` (standard library only).

## Model and result

Let \(S_t=(x_t,x_{t-1},x_{t-2})\in\{0,1\}^3\), with only the first bit \(Q(S_t)=x_t\) observed. Evolve by

\[
x_{t+1}=x_t\oplus x_{t-1}\oplus x_{t-2}\oplus\eta_t,\quad
\eta_t\stackrel{iid}{\sim}\operatorname{Bernoulli}(0.1).
\]

This is a genuine eight-state Markov chain. The exact 8×8 transition matrix is doubly stochastic, so the uniform microstate measure (each of eight states probability 1/8) is stationary. At that distribution, the two hidden bits are independent uniform conditional on current observation, and a perfect current-only or two-bit observer can predict the next visible bit at only 50% accuracy. An observer of the current and preceding two bits reaches the noise ceiling of 90%.

For current-bit projection \(Q\), a pair of same-visible states with opposite hidden parity have next-visible Bernoulli laws of parameters 0.1 and 0.9. Their total-variation distance is exactly **4/5 = 0.8**, violating strong lumpability.

## Exact finite-horizon marginal defects

For a horizon \(t\), compute \(d_Q(t)=\max_{u,v:Q(u)=Q(v)}\mathrm{TV}(P^tQ(u,\cdot),P^tQ(v,\cdot))\). This is the distance between *one future marginal* from paired microstates, not the full visible-path law.

| Horizon t | Exact defect | Decimal |
| --- | ---: | ---: |
| 1 | 4/5 | 0.8 |
| 2 | 16/25 | 0.64 |
| 3 | 16/25 | 0.64 |
| 4 | 0 | 0 |
| 5 | 64/125 | 0.512 |
| 6 | 256/625 | 0.4096 |
| 7 | 256/625 | 0.4096 |
| 8 | 0 | 0 |
| 9 | 1024/3125 | 0.32768 |
| 10 | 4096/15625 | 0.262144 |
| 11 | 4096/15625 | 0.262144 |
| 12 | 0 | 0 |

**Important subtlety:** the projected *marginal* defect can vanish at horizon four and reappear at horizon five. This is not a restoration of information after destruction. The different hidden states induce the same distribution of the fourth observed bit but different distributions at a later step; the full visible trajectory retains richer distinctions than a single-horizon marginal. A zero at one selected horizon does **not** imply strong lumpability, nor preservation of all path laws. Strong lumpability remains falsified at t=1.

## Exact predictive information

Under the stationary uniform measure:

- \(H(X_{t+1}\mid X_t)=1\) bit;
- \(H(X_{t+1}\mid X_t,X_{t-1})=1\) bit;
- \(H(X_{t+1}\mid X_t,X_{t-1},X_{t-2})=H_2(0.1)\approx0.4689955936\) bits;
- therefore the two extra historical observations provide \(I(X_{t+1};X_{t-1},X_{t-2}\mid X_t)=1-H_2(0.1)\approx0.5310044064\) bits of additional predictive information.

The information benefit is synergistic in this parity construction. If only one hidden bit is known, the other masks it. Access to both is necessary for this exact next-step advantage. Do not identify this with a universal three-fiber decomposition.

## Interpretive lineage

An observer can infer the complete microstate exactly from the last three visible observations; the environment does not expose the hidden bits in the current observation alone. A recurrent model need not explicitly label its hidden state as `(x_t,x_(t-1),x_(t-2))` to produce correct predictions. Predictively sufficient representations (in the sense of predictive state representations) can be evaluated by their future-observation predictions instead.

The result gives a precise example of task-relative information loss and recoverability:

1. **Projection loses a distinction**: current bit erases two prior bits.
2. **Dynamics makes the distinction consequential**: erased parity changes next-bit transition law.
3. **History restores predictive access**: a three-observation window recovers the relevant parity.
4. **Summary choice matters**: a one-horizon marginal can hide discrepancies visible in other horizons or joint paths.

This does not demonstrate biological memory, permanent learned memory, an FRR advantage, or any universal numerical constants. Testing learned retention requires model training and held-out trajectories; see the neural companion experiment.
