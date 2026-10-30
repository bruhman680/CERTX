# Selected primary-source contacts

Read 29 October 2026, America/Chicago. Screenshots are leads, not benchmark evidence.

## RuHarness

[When the Critic Falls Behind](https://arxiv.org/html/2610.36826v1), Hao Chen et al., v1. Inspected method §3, Table 1, splits and limitations. Diagnostic rubrics change while the task objective stays fixed; candidate selection uses separate validation. Table 1's held-out macro scores imply 4.5/5.3 percentage-point gains over the strongest listed baselines for its two backbones. All experiments use DeepAgent; wider transfer remains open. No replication here. Our adaptation is limited to versioned diagnostics with fixed acceptance criteria and distinct development/selection/final-evaluation roles.

## Parallel Language Models

[Parallel Language Models via Variational Decoding](https://arxiv.org/html/2610.26693v1), Felix Draxler et al., v1. Inspected §3.1/3.4, Tables 1/11 and Appendix E.4. Latent auxiliaries coordinate parallel token proposals. Training combines encoding and reconstruction losses. Exact and relaxed verification differ, so speed claims must retain their decoding rule. This is not an inference switch for our existing weights: conversion still trains, and their ablation favors joint training. No model/decoder installed here. Our conceptual takeaway: likelihood acceptance and factual source validity are distinct.

## Diagram

The user clarified this is a general harness reference. Its visible proposal/execution/verification/recording loops overlap existing FRR guidance. Small text is not reliably legible; bounded searching did not identify an exact original post. No numerical target or new algorithm is adopted from it. Further searching stopped at the user's direction.

## Scope

Selected primary readings, not systematic reviews, full proof/code audits or independent replications. The local guard derives from our recorded TP-C1 failure, not an implementation of either paper. No paper result transfers to our CPU model by analogy.
