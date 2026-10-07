# Mathematics 01 — typed cube and minimal noncommuting witness

## Scope and evidence

I inspected NOW.md; the FRR v0.5 compact seed, Boundary/Order/Uniformity, equivalence/congruence discussion, Cross-Domain Weave Test, and residual-location passage; CONTINUATION_HANDOFF.md; RECOVERED_CODEX_HISTORY.md; and RECOVERY_NOTE.md. I executed an exhaustive four-state mathematical toy below. Its output is `outputs/mathematics-01/exhaustive-cube.json`. I did not execute garden, graph, optimizer, transformer, or inferred boundary code. Repository events and supplied-model claims here remain inherited evidence, not independently reproduced results. Recovery-note pause statements are historical and superseded by NOW.

**Finding:** FRR already correctly distinguishes an intertwining defect from an ordinary commutator and from causal diagnosis. A typed square is sufficient for its present compression claim. A cube can add a translation-equivariance control, but duplicating a square along a relabeling axis adds no independent evidence or third mechanism.

## Explicit eight-vertex cube

Use indices `(i,j,k) in {0,1}^3`: i marks compressed representation, j marks elapsed time (0 or 1), k marks relabeled domain. Every vertex with i=0 has space `X_{jk}={0,1}^2`; every vertex with i=1 has space `Y_{jk}={0,1}`. These are distinct typed copies even when their carrier sets coincide. Interpret `(x,e)` as focal bit and surrounding-field bit only inside this toy.

Compression edges: `q_{jk}(x,e)=x`, from X to Y. Time edges on X: `T_k(x,e)=(e,e)`. Time edges on Y: candidate `B_k(y)=y`. Translation edges on X: `F_j(x,e)=(1-x,1-e)`; on Y: `f_j(y)=1-y`. All maps are total on the stated finite spaces. No intervention, infinite horizon, stochastic trapping, or approximation limit is assumed. Observation is the final focal bit after exactly one step. Compare Y endpoints with discrete metric `d(a,b)=|a-b|`; exact tolerance is epsilon=0.

The two compression/time faces have defect

`delta_k(x,e)=d(q_{1k} T_k(x,e), B_k q_{0k}(x,e))=|e-x|`.

The other four faces commute exactly: compression/translation because `q F=f q`; micro time/translation because `T F=F T`; macro time/translation because `B f=f B`. This partitions the six faces, rather than calling the cube globally commuting when one route happens to match.

At `(0,1)`, the three-edge route time→compression→translation ends at 0; compression→time→translation ends at 1. Its defect is 1. Exact equality and any epsilon<1 fail for this specified B. Exhaustive enumeration found defects 0,1,1,0 on states `(0,0),(0,1),(1,0),(1,1)` and verified both nontrivial translation identities on every state. The macro identity follows directly from B=id; the output's macro-translation field is a tautological check, not additional computational evidence.

This cube adds useful pressure only if translation is itself being claimed as structure-preserving. Otherwise report the compression/time square alone. A nontrivial cross-substrate translation would require separately specified domain laws and observables; bit complement cannot establish one.

## Minimal witness and guarantee independent of macro-model choice

The smallest deterministic obstruction to a macro-transition through a surjective compression has three microstates and two macrostates. Let X={a,b,c}, Y={0,1}, q(a)=q(b)=0, q(c)=1; let T(a)=a, T(b)=c, T(c)=c. Then equal compressed inputs have unequal compressed successors. No function B:Y→Y satisfies `qT=Bq` globally. With fewer than three microstates, a noninjective surjection has a singleton image; every projected future remains in that singleton, so the obstruction is impossible. This minimality concerns cardinality under these assumptions, not physical dimension or every possible notion of noncommutation.

The four-state cube uses one additional microstate for a clean focal/field product and complement symmetry. In it, `(0,0)` and `(0,1)` share q=0 while successors project to 0 and 1. Consequently choosing a different B cannot repair the global defect. Restricting to domain e=x does repair it for B=id, and that domain is forward invariant under T. Thus failure is domain-relative.

For distribution-valued macro predictions K(0), the two required outcomes are point masses at 0 and 1. Triangle inequality in total variation gives `max(TV(K(0),delta_0),TV(K(0),delta_1)) >= 1/2`. Uniform tolerance below 1/2 is impossible even with randomization. This is a proved finite-toy bound; it is not a bound for garden or transformer data.

## Surviving relation, rival, and causal limit

What survives is the congruence criterion: compression supports autonomous macro evolution precisely when projected successors agree across every allowed fiber (and every allowed intervention). The failure witness makes the otherwise hidden field relevant to next-step prediction. Keeping `(x,e)` as the state repairs this particular compression with no need for a memory variable.

The serious rival to a field-wake interpretation is inadequate present-state measurement: e is simply an omitted current coordinate. Nothing in this cube shows an earlier action changed e, that e persists after focal reset, or that an agent learned. A different macro model, observation horizon, or restricted domain can also explain route mismatch. Defect alone cannot discriminate these accounts. Testing a wake additionally requires a specified field-writing intervention, focal reset holding the field fixed, field reset, and subsequent matched-input evolution. Those are recommendations, not executed evidence.

The handoff's garden soil/archive warning and reconstruction writer-placement reversal reinforce why such controls matter, but their claims are inherited and concern different substrates. Source ancestry supplies continuity, not independent confirmation.

## Concrete source repair (proposed insertion, not applied)

Insert after the Cross-Domain Weave Test equation:

> Before drawing a cube, assign each vertex a space and each edge a typed map. Specify the common applicable domain, observation horizon, intervention family, endpoint comparison, and tolerance. Audit all relevant faces and compare complete routes with the same source and endpoint. A cube is useful when its third operation introduces an additional testable dependency; otherwise retain a square. A small endpoint defect supplies no causal diagnosis or behavioral guarantee without a stated conversion bound.

Then add a boxed three-state witness from this report immediately after the congruence condition, with the sentence:

> This failure prevents autonomous macro evolution on the declared domain; it does not establish where or how the omitted distinction originated.

This preserves FRR's open-play and dormancy permissions: typing is required only once diagrams bear formal or evidential weight, not as a prerequisite to every exploratory association. No original source was modified.
