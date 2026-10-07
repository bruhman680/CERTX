# Observation scout: substrate traces, witness records, and fresh readers

Date: 2026-10-05. Status: source contact and experimental proposal; no empirical result.

## Surviving relationship

Place witnesses relative to the wave's causal path, not merely relative to a spatial label. A baseline station observes before arrival; a passage station observes contact; a residual station observes afterward; a fresh reader encounters the retained substrate without the generating history. A control field is independently prepared and unvisited.

A past-relative agent reads a record genuinely captured earlier, or performs later reconstruction. These are different evidential objects. A future-relative agent is introduced later, or installed now to read later. Neither entails backward physical causation.

## Established relatives and their limits

1. **Hermann and Krener (1977), Nonlinear Controllability and Observability.** [Author-hosted paper](https://www.math.ucdavis.edu/~krener/1-25/10.IEEETAC77.pdf). Function: distinguishability of system states from outputs under admissible inputs. For their smooth finite-dimensional setting, an observability rank condition supplies local weak observability. This is local state distinguishability, not automatic recovery of a unique whole history, nor robustness against noise or an incorrect model. Placement inference: choose measurements and interventions that distinguish the relevant candidate states; distance from a wave alone does not establish observability. Access: author PDF opened; browser text extraction was unavailable.

2. **Lipsitch, Tchetgen Tchetgen, and Cohen (2010), Negative controls: a tool for detecting confounding and bias in observational studies.** [Primary article abstract and causal diagrams](https://pubmed.ncbi.nlm.nih.gov/20335814/). Function: seek an apparent effect where the proposed causal mechanism cannot operate but relevant bias pathways remain. Their negative-control outcome should not be caused by the target exposure and should share relevant confounding causes with the main outcome. A null control cannot certify absence of all bias; a poorly matched control may miss the bias of interest. Placement inference: include an unvisited field subjected to the same handling and evaluation, and a sham passage probe. Access: abstract and diagram captions opened; PMC full-text access was blocked.

3. **CONSORT 2010 Statement, Schulz, Altman, and Moher.** [Primary reporting guideline](https://pmc.ncbi.nlm.nih.gov/articles/PMC2844794/). Function: make allocation, blinding, and evaluation procedures auditable. It asks which roles were blinded and how; it does not make the word "blind" a guarantee of unbiased measurement. Transfer here is a design adaptation, not a clinical theorem about substrates: specify exactly what readers, scorers, and experimenters can access. Access: indexed primary-source checklist inspected; direct PMC/BMJ retrieval was impeded. This is a historical source, not a claim that the 2010 guideline is the latest edition.

4. **RFC 3161, Internet X.509 Public Key Infrastructure Time-Stamp Protocol.** [Official standard](https://www.rfc-editor.org/info/rfc3161/). Function: preserve temporal provenance. Its protocol supports evidence that a datum existed before a particular time, conditional on the timestamp authority, time source, cryptography, and verification policy. It does not verify a sensor's physical accuracy or establish that a truthful observation produced the datum. Placement inference: distinguish sealed earlier records from later narratives. A local hash alone establishes neither trustworthy time nor physical truth. Access: official text opened, including introduction, authority requirements, and verification procedure.

These sources contribute different dependencies: state distinguishability, causal bias detection, role-specific information isolation, and record provenance. They do not independently validate a shared physical wake mechanism.

## Constructive test

Prepare independent substrate instances with randomized initial microstates. Record baselines before treatment allocation is revealed to readers. Randomly apply wave A, wave B, or a sham. Choose A and B with equal immediate coarse summaries but different candidate retained traces. Cross passage-probe present/absent with treatment so measurement-created marks can be detected.

After passage, reset the actor. Randomize later readers to receive: (a) retained field only, (b) earlier record only, (c) both, or (d) a deliberately mismatched field and record. Add field-erasure and sham-erasure conditions. Readers receive no treatment IDs, expected answer, generating seed, or scoring labels. Strip filenames and metadata that expose allocation. Freeze a reader or decoding rule on separate calibration cases and evaluate on fresh cases.

Primary outcome: discrimination of A versus B on held-out cases, relative to the same reader on sham fields. Report performance by initial-state family and probe condition, not only a pooled average. The field-only comparison tests a substrate carrier; record-only tests testimony; both tests their combination; mismatch tests whether testimony overrides substrate evidence. Erasure tests whether the nominated carrier is necessary under the intervention. Failure of discrimination does not show absence of every retained trace: the reader or observable may be insufficient.

Support for continuity through the substrate requires field-only discrimination after actor reset, no access to witness logs, and appropriate loss of discrimination after carrier erasure. Claims remain scoped to the observable, reader family, preparation distribution, horizon, and erasure intervention. Retained information about history is not by itself proof that it changes later dynamics; add a downstream-action comparison when behavioral memory is claimed.

## Placement constraints

- Before/upstream is trustworthy only if reflected signals, shared controllers, and feedback cannot contaminate the supposed baseline before sealing.
- Probe disturbance needs a probe/no-probe comparison; a stationary witness can still change the field.
- Reconstruction from a later trace may identify a compatible family of histories rather than one true past.
- Common initialization and shared evaluation prompts can create agreement without transmission.
- No universally uncompromised location is asserted. Define which interference channels are excluded and which remain unresolved.

Next contact: implement this factorial design in a substrate with explicit initial-state and probe models, then test an independently chosen reader. This proposal is not yet executed.
