# Witness-calibration primary-source scout

Completed 2026-10-26. Budget: exactly two search queries; two selected primary works. This scout read no local experiment data, outcomes, grids, or tuning artifacts and ran no experiments. No dependencies were installed and no public messages were sent.

## Conclusion

A defensible interpretation is **conditional set identification**: independent role-anchor measurements restrict uncertain coefficients; intersect the compatible sets and check the resulting uncertainty before inversion. This does not establish a task-performance guarantee. A finite inverse of the coefficient point estimate is weaker than nonsingularity certified throughout a valid uncertainty set. Shared measurement bias outside the declared error model can defeat inclusion even when witnesses agree.

## Selected primary works and access

1. M. Milanese and A. Vicino (1996), *Optimal Estimation Theory for Dynamic Systems with Set Membership Uncertainty: An Overview*, in *Bounding Approaches to System Identification*, chapter 2, pp. 5–27. [Primary university-hosted PDF](https://www.ladispe.polito.it/corsi/Seminar/c3l04/material/MiVi96.pdf). **Abstract/indexed-text access only.** The search index exposed the chapter title, author affiliations, book/year and introductory abstract; HTTPS and HTTP web opens timed out, and a direct HTTPS request returned HTTP 503. No full-methods or theorem claim is made. The accessible abstract describes uncertainty through bounded additive noise, including integral and componentwise bounds, as an alternative to a probabilistic description. The 1991 article with the same title also appeared in search results; it was not selected or separately read. This distinction matters for bibliographic accuracy.

2. Ulrike von Luxburg and Volker H. Franz (2009), *A Geometric Approach to Confidence Sets for Ratios: Fieller’s Theorem, Generalizations, and Bootstrap*, *Statistica Sinica* 19, 1095–1117. [Publisher metadata](https://www3.stat.sinica.edu.tw/sstest/j19n3/j19n312/j19n312.html); [accessible author preprint, arXiv:0711.0198v1 (2007)](https://arxiv.org/pdf/0711.0198). **Selected full methods read:** preprint §§1–4, pp. 1–14, including Construction 1/Theorem 1, Fieller inversion in §2.2, Construction 2/Theorem 5, and rectangle Construction 3/Theorem 6. The university-hosted published-preprint PDF timed out in web access and returned direct HTTP 503. No bootstrap methods, simulations, empirical tables, or results were read. The methods allow bounded, disconnected unbounded, or wholly unbounded ratio sets. Exact Gaussian coverage assumes independent identically distributed paired Gaussian observations; the general construction inherits the quality of its projected-mean confidence sets. The conservative rectangle construction relies on valid marginal sets and a union bound, rather than assuming independence of the two coordinates. These are statistical assumptions of that paper, not properties established for the present witnesses.

## Transfer to the proposed calibration (scout deductions)

These deductions are mathematical design checks, not claims proved about this repository by either source.

- Let `C_j` contain coefficient matrices consistent with anchor witness `j`, its measurement model, and its declared error bounds. Use `C = intersection_j C_j`. If the true matrix belongs to **every** `C_j`, it belongs to `C`. No statistical independence is needed for this logical implication. Calling witnesses independent may describe their provenance, but does not itself prove the error bounds, exclusion of shared bias, or true-matrix inclusion.
- A point inverse only checks the chosen estimate. A uniform margin such as `inf_{A in C} sigma_min(A) > 0` certifies nonsingularity throughout `C`. A validated outer enclosure can give a sufficient certificate. Failing an enclosure check can be inconclusive; it need not prove that the true matrix is singular. An empty intersection flags model/bound incompatibility and does not authorize choosing an uncalibrated point estimate.
- The lateral Fieller lesson is to retain uncertainty through inversion and permit an uninformative answer near a small denominator. For matrices the relevant obstruction is proximity to singularity. The scalar confidence construction is an analogy; it does not supply the matrix certificate, an empirical probability, or a task guarantee.
- An omitted common bias can shift all compatible sets away from truth while leaving their intersection tight and nonempty. Agreement and apparent conditioning then do not rescue coverage. Include justified bias uncertainty in the model or label this condition invalid; do not silently interpret agreement as validation.
- Coefficient-set inclusion, stable raw-signal recovery, accuracy after a projector, and downstream task quality are separate claims. A projection can suppress or preserve particular error directions, while task quality depends on the target/readout and margins. No monotonic task improvement follows from a raw-signal accuracy gain alone.

## Exact discovery and read log

Search tool: `mcp__codex_apps__search_service_web_run`, one batched call containing exactly these two queries:

1. `Milanese Vicino 1991 optimal estimation theory dynamic systems unknown but bounded uncertainty parameter set membership pdf`
2. `von Luxburg Franz 2009 geometric approach confidence sets ratios Fieller arxiv`

Relevant returned primary links were the two selected works above. Follow-up operations were URL opens only, plus two direct URL retrieval attempts. The arXiv PDF returned 24 pages/1,259 parsed lines; methods inspected through parsed line 591 (preprint pp. 1–14). The initial open exposed lines 0–379 and a follow-up at line 380 exposed lines 225–591. The publisher metadata page exposed lines 0–18. Only the indexed abstract was available for the Milanese/Vicino chapter. `SOURCES.json` records the same boundaries and failures. No additional search query or third primary work was selected.
