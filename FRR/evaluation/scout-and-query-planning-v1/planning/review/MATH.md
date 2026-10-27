# Prospective independent mathematical review

Prepared before implementation execution or inspection of output. This is a toy-model derivation, not validation of any cited paper. Let p = Pr(qP=1), r = Pr(qR=1), with qP and qR independent and all remaining latent bits independent fair bits.

## Observation and certainty invariants

Worlds are the 128 assignments to (T,qP,qR,X,Y,u,v), retaining each assignment with its exact prior weight, including assignments that produce identical observations. P=X; C=(qP, X xor T if qP=1 else u); R=Y; M=(qR, Y xor T if qR=1 else v). Zero-mass worlds are excluded when testing posterior support.

A history determines T exactly if and only if it includes P and C with observed qP=1, or R and M with observed qR=1. To see necessity, absent either usable pair, each observed good cipher has an unobserved independent pad, and each bad cipher has independent noise. The unobserved pads can be flipped with T while preserving every observation. This gives a support-preserving bijection between T=0 and T=1 worlds. Consequently every unresolved posterior has Pr(T=0)=Pr(T=1)=1/2; it is never merely biased toward one target.

Every single record has zero target information and zero certainty probability. C and M reveal their respective qualities, which can inform action choice, but the policy cannot inspect a latent quality before the record is acquired. P,R and cross-side record pairs cannot resolve T. Observing both good pairs yields consistent recovered targets because the data are generated from a single T.

## Independent closed-form root values

Each entry below is (resolution probability, expected query count), optimized lexicographically over resolution first and expected count second. Stop is permitted. For 0<p,r<1 write a=max(p,r), b=min(p,r), s=p+r-pr.

| Budget | Adaptive | Fixed subset, no contingent stopping | Quality oracle |
| --- | --- | --- | --- |
| 0 | (0,0) | (0,0) | (0,0) |
| 1 | (0,0) | (0,0) | (0,0) |
| 2 | (a,1+a) | (a,2) | (s,2s) |
| 3 | (s,2+b-pr) | (a,2) | (s,2s) |
| 4 | (s,2+b-pr) | (s,4) | (s,2s) |

For p=r=0 every mode and every budget has (0,0). The table's interior assumption matters at other boundary priors; the specified experiment uses only interior priors and the all-bad boundary.

At budget 2, scout the quality record on the higher-quality side. If good, complete its pair; otherwise stop. The cost is 1+a. At budget 3, scout that same side, complete it immediately when good, otherwise scout the other side and complete only when good. Cost is 2+ b - pr. The all-bad branch stops after two scouts. At budget 4, the same policy is sufficient; a fourth query cannot help. An optimal policy cannot improve success beyond s because worlds with both qualities zero never resolve under any query set.

For fixed subsets, only complete pairs matter. A third record cannot add a second pair, so budget 3 gains nothing over the best budget-2 subset. Budget 4 gains both pairs. A fixed selected subset is charged its full size on every world, including those already resolved partway through; empty is allowed and wins resolution-zero ties.

The quality oracle is privileged: qP,qR are supplied before any queries at zero cost. With budget at least 2 it picks a good pair whenever one exists, taking two queries; otherwise it stops without queries. Its free quality evidence is independent of T, so it cannot resolve with budget 0 or 1.

### Numeric predictions (exact rationals)

| Prior (p,r) | B2 adaptive | B3/B4 adaptive | B2/B3 fixed | B4 fixed | B2+ oracle |
| --- | --- | --- | --- | --- | --- |
| (1/2,1/2) | (1/2,3/2) | (3/4,9/4) | (1/2,2) | (3/4,4) | (3/4,3/2) |
| (3/4,1/4) | (3/4,7/4) | (13/16,33/16) | (3/4,2) | (13/16,4) | (13/16,13/8) |
| (1/4,3/4) | (3/4,7/4) | (13/16,33/16) | (3/4,2) | (13/16,4) | (13/16,13/8) |
| (0,0) | (0,0) | (0,0) | (0,0) | (0,0) | (0,0) |

Symmetry under swapping (P,C,p) with (R,M,r) requires identical values for the two asymmetric priors. Resolution and optimal lexicographic value cannot worsen with larger budget. Expected count alone need not be monotonic when the primary success objective increases.

## Exact Bellman and replay checks

At belief b and remaining budget k, stop returns (1,0) exactly when positive-weight support has one T value, otherwise (0,0). For each unqueried record and k>0, group compatible worlds by its observable value, weight each child by exact mass/parent mass, and return (sum child success, 1+sum child query count). Choose greatest success, then least count; action-name tie breaks do not alter these objectives. Cache keys must represent the complete information state, remaining budget, and queried records.

Independent replay must reconstruct observations solely from saved latent worlds, route only through actual observation branches, check action availability/budget, and count every world's original prior mass. It should compare aggregate success and cost against a separately implemented exact solver and these closed forms. Oracle replay may use free qualities; ordinary replay must not use them until C or M is queried.
