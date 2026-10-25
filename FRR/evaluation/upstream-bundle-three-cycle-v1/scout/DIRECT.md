# Direct scout: relation operators upstream of phase readout

Budget complete: two search queries, two primary works. No experiment outcomes read or experiments launched. Read selected methods, not all appendices or a fresh benchmark reproduction.

**[RotatE, arXiv:1902.10197v1](https://arxiv.org/pdf/1902.10197v1)**, ICLR2019. Sections3–4 define learned coordinatewise relation rotations and a distance objective over labelled knowledge-graph triples. The relation inventory and training task are supplied; this is not sentence-stance inference. OpenReview's PDF route presented a browser challenge; the primary arXiv PDF was accessible.

**[ComplEx, PMLR48](https://proceedings.mlr.press/v48/trouillon16.pdf)**, ICML2016. Sections2–4 and equations9–11 give a learned relation-conditioned score, an explicit real-coordinate expansion, and a low-rank learning formulation. Relation labels and observed facts are inputs. This is not a test of epistemic unknown status or an angle-only decoder.

## Design implications (our inference)

- The upstream object should include the task, relation/operator and representation constraints, before choosing a readout. Coordinate type alone does not specify that bundle.
- Keep the exact real-coordinate control. Convenient complex notation and useful structured learning are compatible with real arithmetic implementations.
- A scalar output is not inherently plain cosine. Avoid general impossibility claims about scalar retrieval based on one fixed symmetric score.
- Known context/binding blocks in our fixture are explicit structural access. Neither paper establishes that a natural-language encoder discovers that partition, nor that a global or scoped phase convention transfers to sentence negation.
- Declare what has been learned versus provided. Our oracle phase/codebook test can locate a readout boundary while leaving semantic learnability open.

Shared direct messages with the lateral scout and reviewer confirmed the need to distinguish labelled relational prediction from language semantics. Lateral sources independently emphasize supplied inductive bias and the difference between angular centres and probability calibration. These are complementary source interpretations, not independent replication of our proposed experiment.

Source metadata and access scope: [DIRECT_SOURCES.json](DIRECT_SOURCES.json). No new source search beyond this budget is proposed automatically.
