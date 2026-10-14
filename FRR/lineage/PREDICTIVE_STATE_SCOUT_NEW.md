# Predictive-state scouting: hidden bits, windows, and sufficient predictions

Research pass: 2026-10-13 (user-facing date). Read the preserved Claude scripts and continuation note. This is a source-and-derivation pass, not an independent rerun of their simulations. No GitHub mutation performed.

## Relationship that survives

A finite hidden generator need not have a finite exact predictive representation. However, a large count of rounded next-symbol probabilities at one history depth neither proves infinite causal states nor identifies the carrier of persistence. Predictive representation, ergodicity, and environmental inheritance are separate questions.

## Primary sources actually read

1. Jurgens and Crutchfield, *Divergent Predictive States* (2021), [arXiv:2102.10487](https://arxiv.org/abs/2102.10487), full HTML sections II.2–II.4 and introductory mixed-state discussion, accessed at https://arxiv.org/html/2102.10487. Definition 3 distinguishes states by some finite future word, not only the next symbol. Their generically infinite-state claim concerns stationary ergodic hidden Markov processes and mixed-state measures; it is not a theorem that every noisy two-bit model has infinitely many causal states. Special synchronized or observationally redundant models remain possible.
2. Geiger and Temmel, *Lumpings of Markov chains, entropy rate preservation, and higher-order lumpability*, [arXiv:1212.4375v6](https://arxiv.org/abs/1212.4375v6), full HTML sections 2.1–2.5, especially Theorem 9 and strong k-lumpability definition, accessed at https://arxiv.org/html/1212.4375. Strong k-lumpability requires a k-th order projected Markov process for every initial hidden-state distribution. A stationary-only apparent closure is weaker. Their baseline setting is a finite irreducible aperiodic chain; the frozen-bit endpoint violates irreducibility.
3. Loomis and Crutchfield, *Topology, Convergence, and Reconstruction of Predictive States*, [arXiv:2109.09203](https://arxiv.org/abs/2109.09203), substantive HTML sections II–IV and mixed-state convergence discussion, accessed at https://arxiv.org/html/2109.09203. Predictive states are future measures conditioned on pasts. Stationarity supplies time independence; ergodicity supports empirical time frequencies; convergence rates are process-dependent. A statement that their method handles a frozen mixture is therefore unsupported. I did not locate an explicit blanket phrase excluding all nonergodic mixtures; the actual assumptions are the appropriate qualification.

These three are not three independent confirmations: two share an author and computational-mechanics lineage. Geiger–Temmel supplies a distinct Markov-projection criterion rather than evidence of physical substrate memory. No primary source in this pass was abstract-only. Prior reported Grassberger criticism was not investigated here and must remain abstract-only in its earlier account.

## One-step agreement: generic warning, model-specific exception

In general two states can share the next-symbol distribution but disagree later. For example, states A and B both emit a fair first bit; every outgoing transition from A enters C, which subsequently emits zeros forever, whereas every outgoing transition from B enters D, which emits ones forever. The first-bit laws match, but two-bit laws differ. This is a constructed finite generator example, not a claim about the supplied K.

The supplied K has an important exception. Let b be the posterior probability of hidden e=1 after the observed history, with last visible symbol y. The next-one probability is

- y=0: p=.15+.30 b, range [.15,.45].
- y=1: p=.90-.30 b, range [.60,.90].

The ranges are disjoint, and each branch is injective. Therefore exact p uniquely determines y and b. For a fixed supplied transition kernel, (y,b) determines the entire future conditional law. Hence exact one-step equality **does imply full-future equality in this model**. This resolves the earlier broad caution locally; it does not generalize to other K tables. Rounded equality does not have this guarantee, because rounding merges different beliefs. The scripts still count finite-history posterior predictions, not infinite-past recurrent predictive states.

At the deterministic echo endpoint h=1, the hidden bit becomes the preceding visible symbol after an update, so following the initial transient the visible process is at most second-order Markov. At the fair-hidden endpoint, the next visible probability depends only on its current visible symbol, giving first-order Markov closure. These are algebraic properties of the specified update ordering, not generic classifications of echo and shadow.

## Frozen mixture versus small positive noise

For the frozen-bit model e never changes. Its two communicating classes have different stationary visible switch rates. With the provided K:

- e=0: stationary probability of y=1 is .15/(.15+.10)=.60, switch rate 2(.15)(.10)/(.25)=.12.
- e=1: stationary probability of y=1 is .45/(.45+.40)=9/17, switch rate 2(.45)(.40)/(.85)=.4235294.

An equal mixture thus retains between-trajectory switch-rate standard deviation approaching half their difference, .1517647, as trajectory lengths grow. This explains the reported .15 without treating it as evidence of hiddenness generally. The scripts initially use uniform y rather than component-stationary y, so their exact finite-word distributions include an initial transient.

For hidden flips with 0<epsilon<1, and the positive entries of this K, the four-state joint chain (y,e) is irreducible; for 0<epsilon<1 it also has self-loops and is aperiodic. Its unique stationary process is ergodic. That is an exact transition-graph deduction. In the small-epsilon regime the expected number of hidden changes is epsilon*T, so epsilon*T much less than one can look frozen on a finite observation window. The autonomous hidden-bit eigenvalue is 1-2epsilon; its correlation decay timescale is -1/log|1-2epsilon|, approximately 1/(2epsilon) for small epsilon. This is a hidden-bit timescale, not automatically the whole joint-chain mixing time or a proof of the reported dispersion fit.

A 1/sqrt(epsilon*T) spread is plausible for a correlated additive statistic when an integrated autocorrelation time scales as 1/epsilon and the long-window asymptotic regime applies. Its coefficient, crossovers, initial conditions, and observable dependence require derivation or measurement. Noise erasing bimodality means switching becomes well sampled, not that the hidden bit ceases to exist.

## Better next contacts

1. Keep the exact one-step identifiability proof with this K; test alternate K with overlapping next-symbol ranges to make the generic multi-step distinction observable.
2. Compare conditional future blocks of lengths 1, 2, 4, 8 across history depths, state initialization, and rounding tolerances. Report TV error of any merged predictors rather than just their count.
3. Obtain the joint-chain stationary distribution and spectrum for each epsilon. Compare windows relative to the slow eigenmode; distinguish initialized finite-word laws from stationary laws.
4. Plot switch-rate variance against T at fixed epsilon and against epsilon at fixed T, using independent draw streams and uncertainty intervals. A window crossover is a scoped result, not a hidden-state detector.
5. At epsilon=0 analyze infinite-history behavior explicitly: each class's transition frequencies identify e almost surely, so the stationary infinite-past prediction can collapse to a finite class-plus-current-y representation even while finite-prefix posterior counts grow. This is the crucial boundary between a finite-history filter and an asymptotic predictive-state claim.
6. Add retained/cleared environment interventions only after specifying which state is focal and which is field. Passive predictive geometry alone cannot locate a wake.

Resting residual: observational distinguishability depends on the chosen future horizon and tolerance; mathematical state counts depend additionally on finite versus infinite conditioning history and stationary versus initialized measures. None of those axes is itself a universal memory ontology.
