# Experiments 02 — two-route reproduction and finite horizons

## Result and provenance

Executed an isolated byte-identical copy of recovered `2026-10-05/graph_two_route_probe.py`; originals unchanged. SHA256 comparison is in `outputs/experiments-02/provenance.sha256`. Read NOW, FRR compact seed and artifact/boundary/evidence sections, recovered working note and recovery note, continuation handoff/history; inspected assembled screenshot and reconstruction introductions to retain their provenance boundaries. No remote contact, downloads, credentials or writes. This is execution replication and sensitivity analysis of shared input, not independent empirical confirmation.

Actual commands:

```sh
mkdir -p /workspace/frr-distributed-2026-10-07/outputs/experiments-02
cp /workspace/recovered-originals/2026-10-05/graph_two_route_probe.py /workspace/frr-distributed-2026-10-07/outputs/experiments-02/graph_two_route_probe.py
python /workspace/frr-distributed-2026-10-07/outputs/experiments-02/graph_two_route_probe.py > /workspace/frr-distributed-2026-10-07/outputs/experiments-02/original.stdout.txt
cd /workspace/frr-distributed-2026-10-07/outputs/experiments-02
python horizon_probe.py > horizon.stdout.txt
```

The seed-1005, 200,000-step output exactly reproduces the working note:

| gamma | positive mean-field branch | choices | sign switches | final z |
|---|---:|---|---:|---:|
| .7 | 0 | 100129 / 99871 | 37503 | -.492291 |
| .8 | 0 | 99736 / 100264 | 16637 | -.936839 |
| .9 | 1.915008 | 60130 / 139870 | 31 | -1.999691 |

## Horizon sensitivity actually executed

The new local wrapper imports the copied original. Parameters remain beta=2,w=.2; seeds 0..29 start at z=0. Each horizon replays the same seeded prefix, so horizons are dependent and not three independent sample sets. Output JSON retains protocol and seed lists.

| gamma | H | switches min / median / max | zero-switch runs / 30 | route-1 fraction range |
|---|---:|---|---:|---|
| .7 | 1000 | 156 / 185.5 / 225 | 0 | .402–.580 |
| .7 | 10000 | 1747 / 1863.5 / 1960 | 0 | .4799–.5320 |
| .7 | 200000 | 36964 / 37570.5 / 38052 | 0 | .495335–.505500 |
| .8 | 1000 | 50 / 82.5 / 116 | 0 | .295–.622 |
| .8 | 10000 | 719 / 839 / 970 | 0 | .4441–.5442 |
| .8 | 200000 | 16124 / 16743 / 17298 | 0 | .491940–.514475 |
| .9 | 1000 | 0 / 1.5 / 11 | 14 | .019–.984 |
| .9 | 10000 | 0 / 2 / 19 | 6 | .0188–.9792 |
| .9 | 200000 | 2 / 15 / 43 | 0 | .023270–.977445 |

At .9 many short runs look locked in field sign even while taking both routes. At 200,000 all selected seeds cross sign, yet the route-fraction range remains broad. This finite ensemble is not a phase diagram, mixing-time estimate, or proof of long-run occupation proportions. Original switch count includes crossings during initial establishment; it does not separately measure escape from an equilibrated basin.

## Distinct mathematical statements

For 0<=gamma<1, w>0, finite beta>=0, and z0=0, |z|<=M=w/(1-gamma). Each route's conditional probability is >=q=sigma(-beta M)>0. Thus probability of never choosing a specified route during H steps is <=(1-q)^H, without an independence assumption. At .9, q=.01798621, and this upper bound at H=1000 is 1.31095e-8. Rare-route selection is not a field-sign escape.

For a stronger escape bound, choose integer L with gamma^L<1/2. Starting anywhere in the positive field interval [0,M], L consecutive route-2 choices yield z_L<=M(2 gamma^L-1)<0. Conditional block probability is >=q^L. Therefore the probability of staying positive for H steps is <=(1-q^L)^floor(H/L); the symmetric statement holds for a negative start. At gamma .7/.8/.9, L=2/4/7, and q^L=.0435175/.000201905/6.08944e-13. At .9 the H=200000 bound is .9999999826, mathematically valid but practically uninformative. For every fixed admissible parameter, it tends to zero as H grows; it is not uniform as gamma approaches 1. The .7 JSON value 0 for this bound is floating-point underflow, not an exact zero probability. This block argument excludes permanent one-sign trapping almost surely in the ideal stochastic model; it does not estimate practical escape time tightly.

The deterministic map F(z)=gamma*z+w*tanh(beta*z/2) is the conditional expected next field, not an exact recurrence for the unconditional ensemble mean: E[F(z)] generally differs from F(E[z]). Its derivative at zero is gamma+w*beta/2. For positive beta,w the zero branch loses stability above threshold .8; at equality the linear derivative is 1 but the negative cubic tanh correction still attracts zero with slower convergence. Above threshold the deterministic nonzero branches are fixed points; they are not absorbing states of the random recurrence.

## Surviving relationship, rival and residual

Action deposits alter the carrier read by later choice. This feedback survives execution and parameter/horizon pressure within the supplied construction. The two-route difference is sufficient here because softmax reads only the difference and common decay cancels total field. Nothing executed establishes a general graph disconnection, spectral threshold, or shared optimizer/context mechanism.

A serious rival to interpreting finite apparent confinement as a newly permanent law is ordinary stochastic metastability of a reinforced choice process: .9's low switching and positive probability floor support this rival directly. Persistence is deliberately encoded in the generator; success validates behavior of that construction, not discovery of environmental memory in a new substrate. Residual: the conservative block escape bound is extremely loose at .9, and the switch metric combines initial sign formation, near-zero recrossings, and basin transitions.

## Concrete reversible improvement

Implemented locally: separate horizon/seed wrapper plus machine-readable output and provenance hash; delete its isolated folder to reverse, originals remain unchanged.

Recommended next, not implemented: predeclare an initial basin state, a sign-crossing or opposite-basin hitting criterion, horizon and censoring rule; measure first-passage times with censored runs explicitly retained. Pair retained-field, reset-field and beta=0 read-disabled controls using common random uniforms. Beta=0 is a particularly useful rival: field remains written but stops influencing route choice. This would localize the read/write feedback rather than equate any persistent field with a consequential wake. No larger cube is necessary for the present horizon question; keep other substrate analogies open rather than force synthesis.

Sources: recovered original script and October 5 working note (shared artifact lineage), FRR v0.5 candidate (method, not empirical evidence), recovery/handoff/history notes (continuity metadata). All new results are local executions on October 7, 2026.
