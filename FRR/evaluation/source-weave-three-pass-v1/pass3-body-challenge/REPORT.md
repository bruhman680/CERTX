# Pass 3: challenge the body-size explanation and specify what can persist

Read 14 November 2026. Three primary research contacts, with linked official release material treated as part of each contact. This is selected-section research, not reproduction or an exhaustive review. No model inference, model/dataset download, installation, training, external code execution, or main-world change occurred. Small documentation and metadata responses were read. Main remains paused at 1580.

## 1. TinyAgent's training count is still unresolved

[Paper v1](https://arxiv.org/html/2409.00608v1), dated 1 September 2024, already reports 80K training examples, separate 1K validation/test sets, and three training epochs. [Paper v3](https://arxiv.org/html/2409.00608v3), dated 25 October, retains those counts. The [pinned official README](https://github.com/SqueezeAILab/TinyAgent/blob/cc45c0e842f5d163c3df1c8f41d60e90e005867d/README.md), dated 4 September, says 40K use cases. The [official dataset card at revision 07aae412](https://huggingface.co/datasets/squeeze-ai-lab/TinyAgent-dataset/blob/07aae41269776824bba82519a84301648f726f2d/README.md) also says 40,000, with three epochs; repository metadata dates that revision to 30 May 2024. Its card describes generating instructions and then execution plans. The viewer fails to infer the JSON records and provides no usable row count. We did not download the training JSON.

**Our inference:** a release/paper mismatch is established; a reconciliation is not. Neither read source establishes two training examples per use case, 40K unique tasks expanded to 80K, or a particular later doubled release. Three epochs cannot explain a factor of two. Even the earlier paper version says 80K, so changing v3 alone does not resolve it. Preserve both claims and their units/dates. Do not use either as a verified count of the actual released checkpoint's training exposure.

This uncertainty does not erase the useful distinction from pass 1: task training and a restricted tool interface are explicit components of that system. It also prevents treating a reported training-set size as an independently checked causal explanation for its performance.

## 2. A tiny recursive puzzle solver is a counterexample to size-only reasoning

[Less is More: Recursive Reasoning with Tiny Networks](https://arxiv.org/html/2510.04871v1) is Alexia Jolicoeur-Martineau's paper, submitted 6 October 2025. Its two-layer network iterates an embedded answer and latent state with supervised answer and halting losses. Its Sudoku ablation includes a 5M variant; the headline ARC model has 7M parameters. These are trained puzzle models, not untrained language agents. Read depth: abstract, background, recursive pseudocode, sections 3–4.2 and ablation table 1; not the entire paper or benchmark reproduction.

The [official README at c011037](https://github.com/SamsungSAILMontreal/TinyRecursiveModels/blob/c01103738605ba39d1430519b1ee0c62f4c707f8/README.md) specifies data augmentation and substantial GPU training, including approximately 18 hours on an L40S for its smallest Sudoku setup. Its [model implementation](https://github.com/SamsungSAILMontreal/TinyRecursiveModels/blob/c01103738605ba39d1430519b1ee0c62f4c707f8/models/recursive_reasoning/trm.py) explicitly carries two latent tensors between updates and resets halted samples. This is within-puzzle state, not evidence of indefinite cross-episode memory. Repository commit date: 1 April 2026.

**Our inference:** small parameter count alone cannot establish an inability to execute complex, suitably trained computation. The relevant comparison includes architecture, learned update rule, input/output representation, training, recurrence depth and compute. Conversely, this puzzle result does not show that our fixed SmolLM2-135M can acquire code/file competence through extra silent turns, that it can act as TRM, or that a 7M grid solver can replace a general text agent. Extra iterations can also plateau or fail. The benefit has to be measured for the actual body and task.

## 3. Test-time training supplies a different state variable, not a prompt trick

[Learning to (Learn at Test Time): RNNs with Expressive Hidden States v4](https://arxiv.org/html/2407.04620v4), revised 31 August 2025, makes an inner model's weights the recurrent state and updates them with a self-supervised gradient step. Its outer language-model training learns the surrounding network and reconstruction views. Thus inner state updates during a sequence coexist with fixed outer parameters during evaluation. The paper's pseudocode initializes a learner for each sequence; permanent memory across arbitrary chat calls is not established. Version 4 explicitly notes substantial wall-clock costs and updates limitations; experiments were completed in v1. Read depth: metadata, introduction/limitations, method sections 2.1–2.3 and summary table of inner/outer loops; no code or benchmark reproduction. V1 method was initially opened, then checked against v4 rather than silently called current.

**Our inference:** recurrence and test-time learning are real design alternatives worth keeping in the map. They require their actual state/update/training contracts. They are not capabilities automatically activated by calling the same frozen Transformer repeatedly, nor evidence that the current environment secretly preserves an unobserved model-side learner.

## What this changes about our fixed-point finding

Our [bounded-view finding](../../bounded-view-contact-v1/FIXED_POINT.md) is a conditional statement about the measured implementation. Let the rendered input be I and fixed greedy generation be G. Fresh KV and unchanged weights make each call start from the same declared model-side state. In the tested window, G(I) = x, and appending x with an empty receipt reconstructs I. Silent changes to unobserved world files do not change that immediate input.

A stateful implementation instead has something like

    h_next = F(h, I)
    output = R(h_next, I)

The external input can stay identical while h changes. Then identical I alone does not imply identical output. Output change is possible, not guaranteed: state can converge, cycle, be ignored or become less useful. A complete fixed-point claim would include h as part of the state. Reinitializing h each call restores the original qualification. This mathematical distinction challenges an overbroad conclusion about all architectures while leaving the locally measured input/output loop intact.

There is also a difference between carrying a Transformer KV cache for an unchanged prefix, continuing the sequence with new tokens, retaining external files, and implementing a learned recurrent state update. Reusing a correct prefix cache is normally a computation-saving implementation choice; it does not by itself inject a new observation or produce a trained iterative solver.

## Concrete next contact and transfer limits

**Strongest low-cost diagnostic remains the detached history comparison already proposed in passes 1–2.** Hold the pinned 135M body, decoder, token budget, task and paired hidden nonce worlds fixed. Compare repeated history with fresh history, then multiple declared length/position/role-matched filler histories. Log exact inputs, emitted cells, actual reads, returned values and goal use separately. This tests a condition effect; it does not isolate architecture or latent learning. Rotate held-out paths/values before claiming transfer.

For a future *separate* recurrent-body experiment, first specify exactly which state persists, its reset boundaries and serialization, how the update was learned, and the matched compute budget. Compare reset-state versus carried-state on the same held-out task; log state hashes and stepwise goal outcomes. If different checkpoints or task training are introduced, call those additional interventions, not a one-variable recurrence test. No such model was downloaded, built or tested here, and it is not a prerequisite for the fresh-history diagnostic.

The present file mistake remains a narrow observed procedure error. Neither parameter count, neuroscience analogy, recursive terminology nor more elapsed turns is an adequate substitute for testing where the access–parse–extract–use chain fails. These contacts refine the experimental vocabulary and restrict premature explanations; they do not authorize a main-world change or demonstrate a repair.

## Access notes

ArXiv HTML, GitHub connector reads and the HF dataset landing page succeeded. HF pinned-card/API/resolve URLs failed through web access; a read-only standard-library HTTP fallback successfully read the small card and repository metadata at the same revision. The dataset viewer's FeaturesError is a source-side presentation failure, not a training-data audit or evidence of invalid records. All reading depths, dates, pins and failures are in SOURCES.json.
