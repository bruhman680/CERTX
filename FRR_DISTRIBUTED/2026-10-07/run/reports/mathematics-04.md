# Mathematics 04 — Long horizons and nonuniform limits

The surviving relationship is conditional: a changed accessible field can alter later possibilities, but a small short-horizon discrepancy does not certify indefinite retention, permanent exclusion, or size-uniform transfer. FRR v0.5 explicitly asks which constants deteriorate near a boundary and what converts residual size into the observable's error. The following exact examples supply that missing conversion and its failure modes. They are mathematical constructions, not empirical validation of the recovered graph, garden, optimizer, or transformer mechanisms.

## Exact counterexample: tiny transition defect, complete eventual loss

Let the state space be {alive, lost}, observation Y=1 on alive and 0 on lost, and initial state alive. Compare identity evolution Q with the row-stochastic transition

P_e = [[1-e, e], [0, 1]], 0<e<1.

The largest one-step total-variation discrepancy between P_e and Q is exactly e. At horizon H, E_P[Y_H]=(1-e)^H while E_Q[Y_H]=1. The observational error is exactly 1-(1-e)^H ≤ He. Thus, for every fixed finite H, the error tends to zero as e→0; uniformly over all H it equals 1 as a supremum. Every nonzero defect eventually produces absorption with probability one.

The operations do not commute:

lim_(e→0+) lim_(H→∞) (1-e)^H = 0,

lim_(H→∞) lim_(e→0+) (1-e)^H = 1.

There is no mysterious memory at the endpoint: the analyst changed the order of two limiting operations. A square comparing parameter limit and time limit is sufficient; three independent operations are not needed here.

Set e_N=1/N to expose size dependence. Fixed H yields survival tending to 1. H_N=N yields survival tending to exp(-1). H_N=N² yields survival tending to 0. The same family supports three incompatible endpoint narratives depending on how exposure scales. The executed arithmetic checks N=100,1000,10000: at H=100 survival rises from 0.36603 to 0.99005; at H=N it approaches 0.36788. Floating-point zeros for H=N² at larger N are underflow, not exact absorption at finite time. The analytic limit supplies the conclusion.

This construction does not assert the recovered two-route model has an absorbing state. Its handoff instead bounds rare-route conditional probability below by q>0 for fixed gamma<1 and finite beta. That bound implies probability of avoiding the rare route for H consecutive steps is at most (1-q)^H, without assuming independent choices. A small q gives long residence, not permanent exclusion. If q deteriorates as gamma→1 or beta increases, the necessary observation horizon deteriorates with it. Mean-field stable branches and stochastic route access remain distinct claims.

## Concrete repair: accumulate the defect and name the horizon

For two Markov kernels with maximal row total-variation defect e and common initial law, the standard telescoping/contraction argument gives TV(mu P^H,mu Q^H)≤min(1,He). An observable in [0,1] has expectation discrepancy no larger than that bound. This is a usable finite-horizon guarantee; claiming tolerance tau requires H e≤tau. A coupling or telescoping proof must be supplied in any application, since arbitrary nonlinear maps need not contract.

For deterministic maps with local defect e and Lipschitz constant L, the analogous recurrence E_(h+1)≤L E_h+e yields E_H≤e sum_(j=0)^(H-1)L^j. Only a uniform strict contraction L<1 provides the time-uniform bound e/(1-L). L=1 permits linear accumulation; L>1 permits exponential amplification. These conditions show why the same residual measurement cannot silently perform the jobs of local agreement and long-term causal accuracy.

Recommended report amendment: state H, parameter/size domain, observable, tolerance, defect norm, and stability conversion together. If no uniform stability constant exists, restrict the claim to the evaluated horizon and give a scaling family rather than an infinite-limit slogan. This report implements the tiny arithmetic witness, not a new application benchmark.

## Spectrum, writing, and the limit that survives

The reconstructed ring uses frozen positive conductances and x_(h+1)=(I-dt L_g)x_h+noise_h, with dt=0.20. For deterministic holding, symmetric L_g has eigenpairs (lambda_k,v_k), and

x_H=sum_k a_k (1-dt lambda_k)^H v_k.

The spectral gap supplies a slowest available nonconstant mode. It does not establish that writing excites that mode: a_k=<v_k,x_0> may vanish. A linear readout b observes sum_k a_k <b,v_k>(1-dt lambda_k)^H. The implemented sign decoder is nonlinear and additionally needs a margin/noise argument; these modal equations are diagnostic, not an accuracy theorem.

For a connected finite positive-weight ring under stable holding, nonconstant deterministic modes decay; the constant mode preserves total state. The nonzero learned floor therefore gives slow relaxation rather than literal disconnected message regions. Noise injected each step changes both signal-to-noise and the constant mode's behavior, so deterministic decay alone does not prove an exact stochastic accuracy limit.

The inspected README reports a smaller learned gap at N=64 (about 0.00118 versus 0.00963) but no useful learned-hold advantage for spike writers, while moving writers inside arcs changes retention strongly. This cautions against attributing performance to gap alone. An equally serious rival is constructed encoding/readout alignment: nearest-writer labels, only complementary polarities, and writer placement determine what counts as retained. The results and README share construction ancestry; their agreement is not independent corroboration.

At fixed spacing the uniform ring's gap is 4 sin²(pi/N), hence relaxation scales as N². At fixed physical domain with spacing 1/N, a consistent diffusion discretization rescales the Laplacian by N² and also changes explicit-step constraints. The three displayed sizes do not resolve which continuum or expanding-domain claim is intended. Repair by declaring geometry, scaling writing and holding exposure, crossing writer/boundary placement, and reporting modal overlaps plus decoder margins. A matched-spectrum field with different eigenvectors is a useful rival control; it is proposed here, not executed.

## Provenance and inspected evidence

Read: shared NOW; FRR compact seed and Boundary, Order, and Uniformity; CONTINUATION_HANDOFF; RECOVERED_CODEX_HISTORY; RECOVERY_NOTE; October 5 field-wakes handoff; the opening provenance/operator sections of Gemini ASSEMBLED_RECORD; adaptive-boundary README; experiment.py through its stability/reset verification and relevant pressure.py lines. These distinguish recovered originals, clipped screenshots, repository-event history, and inferred reconstruction. Historical pauses are superseded by NOW. No remote sources, remote writes, application reruns, or source independence are claimed. Executed only Python standard-library arithmetic; output is outputs/mathematics-04/nonuniform-limits.json. The reconstructed branch can remain dormant while these limits discipline any future claim.
