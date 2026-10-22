# Cycle1 protocol: witness access versus survival

Saved before numerical execution. Exact finite probability enumeration in floating point; no sampling, model API call or physical/agent validation. This is a new authored observation-model contact, informed by the preceding reset work but not a reproduction of its kernels.

Let survival S~Bernoulli(v). The gate satisfies P(G=1|S=1)=a1 and P(G=1|S=0)=a0. Joint probabilities: (S1,G1)=v*a1; (S1,G0)=v*(1-a1); (S0,G1)=(1-v)*a0; (S0,G0)=(1-v)*(1-a0). A zero-coded readout Z=S*G returns0 for inaccessible as well as readable absent state. A ternary readout explicitly distinguishes1,0,missing. A direct external witness reads S under stipulated perfect access.

Preselected examples:
- Equal zero-coded law: erasure-heavy(v=.2,a1=a0=1) versus access-heavy(v=1,a1=a0=.2).
- Equal ternary law: (v=.2,a1=1,a0=.25) versus(v=.8,a1=.25,a0=1); both yield p1=.2,p0=.2,missing=.6. Conditional-on-readable mean .5 is not survival .2 or .8 when selection depends on state.
- Under MCAR a1=a0=a>0, conditional readability recovers v; a=0 leaves v unidentified.

Without assumptions on gate selection, exact ternary population probabilities identify survival interval[p1,1-p0]. Check attainability by constructing a1=p1/v and a0=p0/(1-v) for endpoints and midpoint, handling v0/1 explicitly. Zero-coded probabilities identify interval[p1,1]. These are population sets, not confidence intervals.

Grid: v,a1,a0 in{0,.2,.4,.6,.8,1}:216 cells. Each joint law, observation law and set containment must agree with direct enumeration within1e-12. Check MCAR216 subset, counterexample equivalence and interval sharpness. No parameter retuning.

Restoration operators: preserve S and force G=1; alternatively rewrite S~Bernoulli(w) independently and force G=1, with w=.6. The preserving operator should reveal v, while the rewriting operator reveals w irrespective of prior survival. Save their explicit 4x4 transition matrices and direct post-restoration observation laws. A successful read after restoration alone cannot establish that restoration preserved state. External direct witness before restoration can distinguish the examples only under its direct-access assumptions.

No novelty, memory-carrier location, universally superior observation format or actual framework benefit claim. Missingness labels improve the observation contract but do not alone identify survival under state-dependent selection. Preserve raw results, code, runtime/checks and any failed execution; no GitHub/global navigation writes.
