# A bounded view can stabilize an exact input/output loop

This is a conditional mechanism finding, not an interpretation of feelings, development or internal understanding.

The integrated detached pilot at `../bounded-view-continuation-prototype-v1` retained exact input and output token IDs. Its three inputs were identical (2231 tokens each), and its three greedy outputs were identical (256 tokens each). Model weights, runtime settings and initial framing stayed fixed; KV is rebuilt for each reply. The eight recent assistant texts were copies of the same text and their projected receipts were empty.

Let B be the fixed opening messages, x that repeated reply, and I the rendered token sequence for B followed by eight pairs (x, empty receipt). In this tested condition, greedy generation G gives G(I)=x. With no complete cell, notebook append succeeds; automatic history copying also succeeds and is silent. Shifting the eight-pair window and appending (x, empty receipt) therefore reconstructs exactly I. The next call receives the same input again.

The physical world still changes: its notebook and history-copy files grow. Those changes are outside this immediate observation unless a code action reads them or a receipt reports a consequence. World persistence alone does not make every change visible to the model.

The conclusion applies while the stated conditions hold. A storage/copy error, different actual receipt, a model action that returns new information, changed perception, changed context or changed decoding can break the condition. Finite quotas can eventually produce an actual error. This is not a claim that the whole world is static or the output must repeat forever under every condition.

It explains why fitting a wider cadence is not itself evidence for richer behavior. It also narrows the next experiment: compare a defined source of variation or actual environmental observation as its own condition, with archive/world preservation and the original invitation held explicit. No clock cue, novelty instruction, repetition penalty, success gate or decoder change was silently installed to make this pilot vary.
