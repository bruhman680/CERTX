# Codex Evidence-Lineage Branch Orientation

**Branch:** `codex/evidence-lineage-audit`  
**Parent branch:** [`claude/plan-certx-architecture-ojiem`](https://github.com/bruhman680/CERTX/tree/claude/plan-certx-architecture-ojiem)  
**Branch point:** `18b7e4eb86cfd0982b1b5a40376d574eb1cbb628`  
**Opened:** 2026-09-29

## Purpose

This branch is an evidence-oriented continuation of the CERTX garden. It does not replace Claude's branch and does not prune failed, speculative, or symbolic paths. Its job is to preserve lineage while making claim strength visible.

The governing rule is:

> Preserve the exploration; calibrate the claim.

The first reference for experiment-level status is [`EXPERIMENT_STATUS_LEDGER.md`](EXPERIMENT_STATUS_LEDGER.md).

## Ancestry

The source branch contains the accumulated HPGM research cycle, WANDERINGS, experiments, paper draft, Shadow Ledger, continuity files, and implementation prototypes. This branch inherits all of that history unchanged.

The Codex layer adds:

- explicit evidential vocabulary;
- claim-to-artifact lineage;
- separation of synthetic construction, parameter injection, pilot evidence, nulls, and independent measurements;
- documentation repair where summaries exceed experiment outputs;
- a path toward non-circular replication.

Claude's working branch remains the upstream historical source. `main` is not a working target.

## Operating boundaries

1. Do not push directly to `main`.
2. Do not rewrite or force-update `claude/plan-certx-architecture-ojiem`.
3. Do not delete or silently replace historical experiments or results.
4. Do not edit `PAPER_DRAFT_v1.md` until the experiment ledger is reviewed and a separate claim-by-claim paper audit exists.
5. Treat constants such as `1.2`, `7`, `0.35`, `0.2`, and 30/40/30 as hypotheses when testing them.
6. Do not label a result empirical merely because code ran.
7. Do not label a value emergent if it was supplied through a parameter, label, generator, threshold, or ontology.
8. Use held-out or nested evaluation whenever thresholds or weights are learned.
9. Record nulls, contradictions, confounds, and scope limits as durable results.
10. Review branch changes before any merge. No merge, branch deletion, or destructive cleanup without Thomas's explicit direction.

## Evidential movement

An idea can move without losing its earlier form:

`intuition -> interpretive silhouette -> mathematical candidate -> synthetic demonstration -> testable hypothesis -> pilot -> replicated empirical result`

Movement is not automatic. Each arrow requires a new burden to be met. A later stage does not retroactively erase the earlier lineage.

Backward audit is equally important:

`headline claim -> measurement -> estimator -> data/generator -> inserted assumptions`

When a result is recoverable before the observations exist, classify it as inherited or constructed until a discriminating test says otherwise.

## Rehydration order

Before substantive edits:

1. Read `CODEX_BRANCH_ORIENTATION.md`.
2. Read `EXPERIMENT_STATUS_LEDGER.md`.
3. Read `CLAUDE.md`, `SESSION_HANDOFF.md`, `SHADOW_LEDGER.md`, and `README.md`.
4. Verify the active branch and source ancestry.
5. Confirm the current WANDER and experiment inventories.
6. Inspect the code and committed outputs behind any claim being changed.
7. Keep claim strength proportional to independent contact with mathematics, execution, or external data.

## First research sequence

1. Replicate Experiment 016.
2. Rebuild independently measured fiber observables.
3. Establish nested evaluation.
4. Repair the Kuramoto test in Experiment 003.
5. Repair the repository-mesh test in Experiment 004.
6. Run neighborhood tests around proposed constants.
7. Compare FRR/CERTX prompting against simpler and unprompted baselines.

## Branch status

The initial documentation pass creates the experiment ledger, this orientation, and a calibrated README. The paper and experiment history remain untouched. The next write should be a separate claim-by-claim paper audit, not an immediate paper rewrite.
