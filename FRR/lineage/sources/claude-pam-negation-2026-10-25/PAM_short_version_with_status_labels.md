# Phase-aware memory: what is shown and what is proposed

Status key: DERIVED = follows from algebra. CHECKED = tested by code on constructed data. PROPOSED = an idea, not tested. OPEN = needs evidence.

Written in short, plain sentences. It was not checked against the ASD-STE100 dictionary.

## 1. The problem

- Cosine search on text embeddings can rank "The valve is open" close to "The valve is not open". Published studies report this negation blindness for some models. [OPEN for any one model. Measure it.]
- Unit-length normalization removes vector length. Whether length carries useful meaning, such as confidence or frequency, depends on the encoder. [OPEN]

## 2. What the resonance score does

- The score is S = R/2 + R²c/2. R measures energy balance. It is 1 when both norms are equal. c is cosine on the real and imaginary parts, written as real coordinates. [DERIVED, CHECKED]
- If both norms are equal, S = (1 + c)/2. This gives the same ranking and the same ties as cosine on the same numbers. [DERIVED]
- So the score does not fix negation. Phase can help only if an encoder puts polarity into phase. A real vector that keeps the same numbers carries the same information. [DERIVED]
- If norms differ, R can change the ranking. [DERIVED, CHECKED] Whether this is useful depends on what the norm means. [OPEN]
- Phase π is a sign flip. Real negation has scope: time, predicate, "not all" versus "all not". One sign flip does not cover this. [OPEN]

## 3. Retrieval posture

- Idea: the query carries a mode. Expansion keeps a wide match range. Convergence keeps a narrow one. [PROPOSED]
- The score has no bandwidth setting. You can narrow retrieval with a threshold, a softmax temperature, or a smaller top-k.
- For equal norms, a threshold t on S equals a threshold 2t − 1 on cosine. The temperature relation is T_S = T_c/2. [DERIVED]
- So a posture control does not need phase. A fair test compares it with these real-valued controls. [OPEN]

## 4. Other ideas (all PROPOSED, none tested)

- Agents exchange wave packets. Risk: opposite patterns sum to zero, so a dispute can disappear. Keep record IDs, status and source next to any sum. [Cancellation example DERIVED]
- Time as phase progression. Rotating coordinate pairs by a position-dependent angle is already used in rotary position embeddings (background knowledge, not checked here). A phase shared by the query and the record cancels in S. Only relative phase counts. [Common-phase invariance CHECKED]
- Hardware: FFT mapping is a possible path. No speed or energy data exists. [OPEN]

## 5. What is not shown

- No retrieval benchmark.
- No gain on negation.
- No gain for agents.
- The source paper uses phases supplied from outside. It reports scan-time results, not negation results.

## Source

Post with derivation, code and checks: bruhman680/CERTX, RM-C1 (commit 933af8b), FRR/evaluation/resonance-memory-contact-v1.
