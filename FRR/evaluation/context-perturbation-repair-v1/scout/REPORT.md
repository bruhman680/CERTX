# Bounded primary-source scout

Date: 2026-10-26. Scope: exactly two search queries, two primary works; no additional literature search, grid tuning, hardware experiments, or inspection of this evaluation's outcome files. This is a methods/assumptions scout, not evidence that either work implements the proposed repair.

## 1. Metamorphic testing

[Chen, Cheung, and Yiu (1998), *Metamorphic Testing: A New Approach for Generating Next Test Cases*, HKUST-CS98-01](https://www.cse.ust.hk/faculty/scc/publ/CS98-01-metamorphictesting.pdf), also [author-deposited arXiv PDF](https://arxiv.org/pdf/2002.12543).

The method constructs follow-up inputs using domain knowledge and specified relationships among outputs. It supplements other test-selection strategies when a full oracle is unavailable. A test called successful has simply not revealed a fault. Section 1 explicitly distinguishes checker acceptance from guaranteed correctness. Sections 2–3 specify domain restrictions: reversing endpoints preserves shortest-path distance for an undirected graph, whereas column permutations in a linear system require a corresponding permutation of solution coordinates. Thus some transformations imply equality and others equivariance; arbitrary surrounding-context changes supply neither automatically. The report's fault examples explain why follow-up tests can expose an error missed initially. They do not provide a general repair rule or establish that relation satisfaction implies correctness.

Read scope: introduction and preliminaries; all four Section 3 method examples, including their illustrative buggy programs and follow-up examples; no claim of a systematic empirical evaluation. Browser extraction of the original PDF was garbled, so the author-deposited PDF was downloaded and read through local text extraction. Equations have extraction artifacts; reasoning here uses readable prose and simple specified transformations.

## 2. Invariant causal prediction (ICP)

[Peters, Bühlmann, and Meinshausen (2016), *Causal inference by using invariant prediction: identification and confidence intervals*, JRSS B 78(5), 947–1012](https://doi.org/10.1111/rssb.12167); [author-deposited PDF](https://arxiv.org/pdf/1501.01332).

Assumption 1 fixes target coefficients and noise distribution across environments and requires noise independence from selected predictors. Proposition 1 connects this mathematical invariance to causal parents in an acyclic linear structural model with appropriate noise independence and interventions excluding the target. The generic procedure intersects predictor sets whose invariance hypotheses are not rejected. Theorem 1 controls false inclusion conditional on valid tests and assumptions; it does not guarantee full recovery. Section 2 describes non-uniqueness and empty identification from one environment. Section 4 gives sufficient intervention conditions for complete identification, including informative individual interventions or specified simultaneous noise interventions. Mere environmental variety is insufficient. These are conditional distribution assumptions, not a claim that every individual prediction must remain unchanged.

Read scope: Section 2, Proposition 1 and surrounding caveats; Section 3 generic method and Theorem 1; Section 3.4; Sections 4.1–4.3 through Theorem 3. Proof appendices, extensions, and empirical sections were not reviewed. Author-hosted journal PDF exceeded browser size limit; publisher page exposed only metadata/summary; local arXiv PDF supplied methods. This is the arXiv manuscript, not a verified byte-identical journal version.

## Application to the proposed toy (deductions, not findings claimed by these papers)

1. A perturbation response measures sensitivity. Calling it a mismatch requires an independently justified transformation law for the intended quantity. Detecting a violated law need not locate the faulty component or identify a correct replacement.
2. A common-mode wrong value can pass every equality check: a constant incorrect output is invariant. Likewise a shared computational error may persist through every context variation. Validate against an independently specified target or oracle in the controlled toy; relation agreement alone cannot close that gap.
3. For a selective interface with observation `z_k = s + a_k n`, known distinct nuisance scalings allow `n_hat = (z_1-z_0)/(a_1-a_0)` and `s_hat = z_0-a_0 n_hat`. If nuisance transformations balance around zero, averaging can recover `s`. These are algebraic consequences of the declared interface, whose knowledge is extra supervision.
4. For `z_k = b_k s + a_k n`, recovering signal instead requires known coefficients and sufficient rank. A global flip `(b,a)=(1,1),(-1,-1)` has rank one; its average is zero and does not recover `s`. If a context edit changes intended signal or target mechanism without a known response law, neither disagreement nor averaging identifies a repair.
5. Declare the selective model, transformation rules, and independent correctness metric before evaluating. Test held-out signal/nuisance configurations and explicit assumption violations. Keep detection, correctness, and repair success as separate measured quantities. No equivalence between this finite algebraic toy and ICP or general reasoning repair follows.

## Access and search accounting

Queries, submitted in one web call:

- `Chen Cheung Yiu 1998 Metamorphic testing new approach generating next test cases technical report pdf`
- `Peters Bühlmann Meinshausen 2016 causal inference using invariant prediction assumptions interventions pdf`

Search snippets surfaced other works; none were opened or used as evidence. Temporary PDFs/text were stored outside the evaluation tree. No evaluation outcomes were read. No long quotations are reproduced.
