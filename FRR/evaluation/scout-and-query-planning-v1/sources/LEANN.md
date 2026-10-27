# LEANN source scout

## Identity and access

Verified title: **LEANN: A Low-Storage Overhead Vector Index**, arXiv **2506.08276v2**, dated **25 November 2025**. The paper's code link names `yichuan-w/LEANN`; the maintained repository is `StarTrail-org/LEANN` and links back to the same paper. Repository inspection is pinned to **a63f484a0b00627fbc641b500ee377d35344eb72**, committed **26 October 2026**. This later software snapshot is not the paper's experimental artifact.

Three selected primary resources: [paper v2](https://arxiv.org/html/2506.08276v2), [pinned README](https://github.com/StarTrail-org/LEANN/blob/a63f484a0b00627fbc641b500ee377d35344eb72/README.md), and [pinned API](https://github.com/StarTrail-org/LEANN/blob/a63f484a0b00627fbc641b500ee377d35344eb72/packages/leann-core/src/leann/api.py). Accessed 27 October 2026; zero search queries. Read depth and checks are recorded in `LEANN_SOURCES.json`.

## Primary-paper-derived summary (176 words)

LEANN reduces vector-index overhead by retaining a pruned proximity graph and highly compressed product-quantization (PQ) representations instead of all dense embeddings. Two-level search uses approximate distances to select candidates, recomputes their exact embeddings with the construction encoder, and batches recomputation across traversal steps. High-degree nodes retain more edges. Optional exact-vector caching trades storage for latency; sharded construction bounds peak storage.

The main workload uses 60 million passages from 76 GB of Wikipedia text. Table 1 reports 4 GB of index components versus HNSW's 188 GB; original corpus and model storage are additional. At 90% Recall@3, Table 2 reports NQ retrieval of 2.48 seconds versus HNSW's 0.05, with generation taking 20.86 seconds. These are storage/latency tradeoffs, not universally fast retrieval. Appendix C averages 20 random queries and uses exact search as retrieval ground truth. Table 2's HotpotQA retrieval share is 23.4%, qualifying prose claiming less than 20% overhead. Mac HotpotQA reaches 50.1% (Table 4). Appendix B retains soft-deleted nodes for traversal and leaves rebuild policies for future work. Evaluation does not establish embedding-drift compatibility or memory truthfulness.

Evidence locators: §§3–6; Table 1; §7.1–7.3/Table 2; Appendices B.2–B.3, C.2–C.4, D.3. [Paper](https://arxiv.org/html/2506.08276v2).

## Repository evidence, kept separate from paper claims

The pinned `api.py` writes passage text, IDs, and metadata to `.passages.jsonl`, plus an offset map; it reads passage text back for results. Metadata records model name, embedding mode/options, dimensions, and schema version `1.1` (lines 598–692). The inspected serializer has no dedicated weight/tokenizer revision digest; options are open-ended. Compact HNSW updates explicitly require rebuilding (lines 958–964). IVF removal compacts passage records (lines 927–949); this is not proof of comprehensive erasure. IDs default to insertion positions, with an optional truncated content hash (lines 543–568). The README offers local and remote embedding/generation providers, so locality depends on configuration. [Pinned API](https://github.com/StarTrail-org/LEANN/blob/a63f484a0b00627fbc641b500ee377d35344eb72/packages/leann-core/src/leann/api.py), [README](https://github.com/StarTrail-org/LEANN/blob/a63f484a0b00627fbc641b500ee377d35344eb72/README.md).

## Original transfers to FRR (proposal, not paper findings; 172 words)

Treat retrieval infrastructure as a costed, replaceable view of retained evidence. Budget source bytes, passage snapshots and metadata, index/PQ bytes, model weights or endpoint access, caches, build peaks, query recomputation, and latency separately. A small index does not imply small total memory or permission to discard originals.

Require a manifest tying each passage to source/version/location and each graph/PQ artifact to encoder weights, tokenizer, preprocessing, chunking, and build configuration. Changing any representation dependency should invalidate or explicitly migrate derived artifacts; a schema number or model name alone is insufficient provenance. Preserve evidence snapshots when reproducibility requires them, with deletion policy covering copies and caches.

Before considering LEANN as an optional backend, compare it with an ordinary retained-source baseline under equal total storage and measured query budgets. Include cold/warm latency, short generations, missing source/model access, edits, deletions, and encoder changes. Score answer support and successful contradiction/version handling separately from ANN recall. Connect to JEM's representation boundary and OPST's distinction between internal agreement and external correctness. No installation or backend adoption follows from this scout.

## Limits

Read-only source review; no install, index build, benchmark reproduction, model download, or private data access. Paper HTML inspected rather than PDF; displayed figures were interpreted through captions, tables, and surrounding methods text, without extracting chart values. API inspection covers selected functions, not backend/native code, provider implementation, concurrent update behavior, secure erasure, or end-to-end model revision enforcement. No claim that uninspected code lacks those mechanisms. README marketing claims were not adopted as evaluation results.
