# Targeted source contact for MS-L1

Primary-source search/open, not benchmark execution or an exhaustive memory survey.

[LongMemEval, ICLR2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf): read abstract/introduction and benchmark overview in the opened PDF. The benchmark separates information extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention, and describes indexing, retrieval and reading as distinct stages. This supports keeping recall, correct use and appropriate uncertainty separate in our questions. It does not validate our prototype. We did not rerun its500 questions, audit its dataset or verify its reported performance claims.

[Lost in the Middle, author PDF](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf): read abstract/introduction and multi-document experimental setup. The paper varies relevant-information position and context length on question-answering/key-value tasks; performance is position-sensitive for the studied models/settings. Our short missing-record test is different: missing content is not the same as present-but-poorly-used content. We do not infer that modern systems reproduce those historical model curves, nor test long-window position effects here.

Inference for our workflow: persistence, exposure, retrieval and successful task use need separate checks. A short handoff can be faithful for the old decision but insufficient for a new one. MS-L1 tests this narrow authored access distinction, not a full long-term-memory architecture or a general FRR advantage. Search results from forums/leaderboards were not treated as primary evidence. No external benchmark data was downloaded or used as a held-out claim.
