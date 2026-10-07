# Source weave: material memory and gradient-history control

Date: 2026-10-05. Scope: a targeted source scout, not a novelty review or independent replication. Abstracts and available primary full text were inspected; optimizer chapter access was limited to its publisher summary. No FRR runtime changes.

## Preserved seed

Earlier action can leave a persistent environmental configuration that changes what a reset actor encounters. The inquiry asks when that configuration acts as a durable constraint, and whether disruption can preserve capacity to learn. This is a useful question without assuming one universal threshold.

## Source contacts

### 1. Memory formation in matter

Keim, Paulsen, Zeravcic, Sastry, and Nagel (2019), [author manuscript](https://arxiv.org/html/1810.08587v3), [journal](https://doi.org/10.1103/RevModPhys.91.035002).

Role: established overview and vocabulary bridge. Material memory concerns encoding, accessing, and erasing signatures of history. The review distinguishes fading memories from those retained until intervention; the latter need not be fundamental laws. Its worn-grass example is especially close to the seed: repeated traffic can erase distinctions between intermediate destinations, while regrowth can preserve them. This suggests a reversal: relaxation can help preserve distinguishable memories instead of merely destroying memory. Assumptions and readout protocols vary by material. This review neither supplies a universal gamma threshold nor makes optimizer and Transformer mechanics equivalent. Follow-up: inspect particular encoding and readout mechanisms rather than importing persistence alone.

### 2. Hysteresis and hierarchies

Sethna et al. (1993), [primary full text](https://arxiv.org/html/cond-mat/9210018v1), [journal](https://doi.org/10.1103/PhysRevLett.70.3347).

Role: mathematical example of structural memory with exact conditions. A zero-temperature random-field Ising model exhibits nested return-point memory. The proof uses partial ordering, the no-passing property, and adiabatic evolution. Returning to a prior extremal driving field within the permitted bounds recovers the earlier configuration. It does not say every hysteretic system has this property; the paper explicitly distinguishes systems whose hysteresis drifts. Repair for our seed: declare permitted interventions and driving bounds before calling a memory invariant. A reproducible constraint can be protocol-relative without disconnected phase space or infinite barriers.

### 3. Generic transient memory formation in disordered systems with noise

Keim and Nagel (2011), [author abstract](https://arxiv.org/abs/1101.2931), [journal](https://doi.org/10.1103/PhysRevLett.107.010603).

Role: failure-and-repair contact. A driven disordered model remembers several training inputs during a transient but eventually loses most despite continued training. Noise can prevent that loss. The example is a model of cyclically sheared non-Brownian suspensions. This supports a specific alternative to a one-way fluid-to-frozen story: reaching an organized steady state can remove discriminability among earlier inputs, while continued perturbation can preserve it. It does not establish that arbitrary noise improves arbitrary memory.

### 4. Multiple transient memories in experiments on sheared non-Brownian suspensions

Paulsen, Keim, and Nagel (2014), [author abstract](https://arxiv.org/abs/1404.4117), [journal](https://doi.org/10.1103/PhysRevLett.113.068301).

Role: empirical contact for the preceding model direction. The authors report suspension experiments consistent with multiple transient memories and stabilization by noise. This is stronger than a synthetic demonstration, but it comes from the same research lineage as source 3; it is not an independent discovery simply because its substrate is experimental. Translation to FRR remains an inference: preserving unresolved branches might benefit from controlled variation, but this paper does not measure conversational reasoning or justify indiscriminate branching.

### 5. Parameter Adaptation in Stochastic Optimization

Almeida, Langlois, Amaral, and Plakhov (1999), [publisher summary](https://www.cambridge.org/core/books/abs/online-learning-in-neural-networks/parameter-adaptation-in-stochastic-optimization/4E8D5E86F4E2634EE29CC363C0568222), [DOI](https://doi.org/10.1017/CBO9780511569920.007).

Role: older functional relative for adapting optimization controls to local behavior. The summary describes a derivation, applications to gradient descent variants, and optimization and online neural-network examples. Access here did not establish its exact gradient-statistic formula or theorem assumptions. Therefore it is an ancestry lead, not validation of GammaC-Adam or an assertion of formula identity. Follow-up: inspect the chapter or author manuscript before assigning a stronger equivalence.

## Repaired optimizer branch: mathematical candidate

Using identical nonnegative normalized temporal weights a_k for both moments gives m=sum(a_k g_k), v=sum(a_k g_k^2), and S=m^2/(v+epsilon). Weighted Cauchy-Schwarz proves 0<=S<=1. Differing Adam averaging windows do not provide that guarantee. v is a second moment; the corresponding variance is v-m^2.

This measures temporal consistency, not curvature or harmful fixation. For vectors, ||sum(a_k g_k)||^2 / (sum(a_k ||g_k||^2)+epsilon) gives a rotationally invariant version. These are mathematical candidates, not performance results.

Minimal discrimination: f_a(x)=a*x^2/2 at x_0=1/a has initial gradient 1 for every positive a. Alignment-based control therefore initially sees identical evidence while curvature varies arbitrarily. Ordinary gradient descent requires 0<eta*a<2, exposing why gradient consistency alone cannot guarantee stability. Compare AdamW, a corrected alignment controller, and a controller with independently measured directional curvature or trial-step loss change. Separate calibration cases from evaluation cases.

Persistent useful descent and persistent reliance on a spurious feature may also have indistinguishable training gradients. Held-out or distribution-intervention evidence is required to separate them. Momentum moments are optimizer state; weights are a separate persistence carrier. Reset each independently before attributing the effect to a parameter wake.

## Surviving relationship and unresolved remainder

Durable memory is a configuration with a write mechanism, readout, retention conditions, and erasure or overwrite conditions. Persistence and behavioral rigidity are separate targets. Exact invariance requires stronger conditions than long lifetime. Controlled perturbation may preserve multiple recoverable distinctions in some systems; it need not merely melt a harmful channel.

Remaining questions: which distinctions should an FRR artifact preserve; what intervention would reveal their erasure; and can deliberate variation preserve those distinctions without impairing task completion? These sources sharpen the questions but do not establish the proposed universal crystallization theory.
