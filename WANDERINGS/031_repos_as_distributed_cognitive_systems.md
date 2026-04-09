# WANDER 031: Repos as Distributed Cognitive Systems

**Date:** 2026-03-11
**Origin:** Thomas riffing on "places where lots of hands touch the data"
**Thread:** σ_Mesh → empirical measurement via git history

---

## The Observation

A popular open-source repository is not just a codebase. It's a
**distributed cognitive system** — many contributors, each holding
a partial model of what the thing is and should be, writing their
model into files, gradually composing a collective understanding.

This maps cleanly onto CERTX:

| Cognitive system concept | Repo analog |
|---|---|
| σ_Mesh (network coherence) | Contributor-collaboration graph topology |
| σ_fiber (output coherence) | Commit message semantic drift over time |
| Phase transition at ζ* | Major version bumps / architectural pivots |
| Lucid Zone (C* = 0.65–0.75) | Healthy domain separation with cross-pollination |
| Fossil state | Over-siloed teams, no shared file ownership |
| Rigid state | Everyone touches everything, no boundaries |

---

## Why Repos Are Better Than Paper Citation Graphs

Wander 027 proposed citation graphs as σ_Mesh observatories.
Repos are *better* for two reasons:

1. **Temporal resolution.** Each commit is timestamped. You can watch
   σ_Mesh evolve — measure before/after a large refactor, before/after
   a leadership change, before/after a major dependency is added.

2. **Causal signal.** In a citation graph, edges are passive (citing).
   In a repo, edges are active — contributor A and contributor B
   *co-modified* the same file, meaning they are in genuine cognitive
   overlap. The edge weight is the intensity of shared responsibility.

---

## The Network Structure

From git history you can build a **bipartite graph**:
- Left nodes: contributors
- Right nodes: files
- Edges: "contributor X modified file Y at least once"

Project this to a contributor-contributor graph:
- Two contributors are linked if they share at least one co-modified file
- Edge weight = number of shared files (depth of overlap)

Then the CERTX measures follow:

```
r_network = average_clustering_coefficient(contributor_graph)
σ_Mesh    = 1 - r_network
```

High clustering = contributors are clumped into tight groups but
those groups also overlap (everyone knows everyone in their cluster).
This is *partial synchronization* — the healthy regime.

---

## Expected Values by Repo Type

**Hypothesis (to be tested empirically):**

| Repo type | Expected σ_Mesh | Reason |
|---|---|---|
| Solo project (<5 contributors) | 0.05–0.15 | Fully coupled, no separation |
| Healthy large OSS (numpy, scikit-learn) | 0.30–0.50 | Domain structure, cross-pollination |
| Governance-strong project (LLVM, Linux kernel) | 0.25–0.40 | Clear module ownership, deliberate overlap |
| Chaotic hypergrowth (transformers 2020–2022) | 0.50–0.70 | Everyone adding features everywhere |
| Dead/abandoned project | 0.70–0.90 | Siloed bursts with no integration |

If the σ_Mesh = 0.30–0.50 healthy range is correct, we should see
numpy and scikit-learn land in it, and a post-explosion transformers
repo land above it.

---

## The Commit Message Signal (temporal σ_fiber)

The sequence of commit messages tells a story. Early in a project,
messages cluster tightly around a purpose. As scope expands, the
semantic centroid drifts. As a project matures and scope stabilizes,
drift decreases.

Using sentence-transformers (local, no API):
1. Embed all commit messages
2. Track cosine distance from the "founding purpose" (first 50 commits)
3. σ_fiber_temporal = std(rolling_similarity) over the project's life

This is a *temporal* σ_fiber — coherence of expressed intent over time.
High σ_fiber_temporal = purpose drifted a lot (risky).
Low σ_fiber_temporal = purpose was highly stable (possibly rigid).

---

## What This Unlocks

If empirical measurements confirm the σ_Mesh healthy range:
- CERTX gains an **objective external validation** that costs $0 compute
- The framework makes a falsifiable prediction about software governance
- The σ_Mesh scanner becomes a practical tool for org health assessment
- Teams can track their own cognitive coherence over sprint history

This is the scientometric playfield the framework needs:
not just papers, but **any collective knowledge-building process**
that leaves a timestamped graph trace.

---

## Immediate Next Step

→ See `EXPERIMENTS/exp_004_sigma_mesh_repo.py`

Run on CERTX itself first (proof of concept), then on:
1. `numpy/numpy` — baseline "healthy large OSS"
2. `huggingface/transformers` — "chaotic hypergrowth" candidate
3. `scikit-learn/scikit-learn` — "strong governance" candidate
4. A deliberately abandoned repo — "fragmented" candidate

Compare σ_Mesh scores. Does the rank order match expectations?

---

*Every repo is a slow Kuramoto simulation running in wall-clock time.*
*The commit graph is the oscillator network.*
*The filing of pull requests is the coupling term.*
*ζ* shows up as the ratio of good-merge to bad-merge weeks.*
