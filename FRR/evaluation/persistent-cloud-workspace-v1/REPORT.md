# Persistent cloud workspace: operational connection, limited model use

7 November 2026, America/Chicago. Prepared extension of the existing garden; the primary history remains paused at 750. This is a three-call isolated connection pilot, not entries 751–753 and not a second continuous season silently substituted for the original.

## Design informed by the history

Read the current handoff/orientation, the original published FRR seed, the palimpsest/source-weave analysis, the current primary runner/generator, the minimal Markov preparation and model-conditioning records. This is a targeted orientation, not an exhaustive rereading of all prior experiments.

FRR's useful contribution here is preserving a revisable idea and its trail, distinguishing analogy from mechanism, and giving artifacts room to contradict interpretation. The shadow/echo/wake and source-weave work cautions that observed persistence does not locate its cause. The garden's recent command-copying and example-attraction findings caution that instructional richness does not establish effective access. These guide our external experiment design; the FRR framework is not inserted into the model's prompt.

The world is a writable /world directory inside a Linux namespace. Shell and Python are inherited machinery. Every entire reply goes unchanged to /bin/sh; no Markdown extraction, repair, success target, novelty requirement, or researcher scoring. This is still an explicitly designed action language, not neutrality or a claim that the model invented its interpreter. Invented executable tools must actually operate through this machinery.

The complete factual model-facing boundary notice is in workspace.py and every raw pilot prompt. The model sees directory entry names and, after its first reply, its immediately preceding reply and actual stdout/stderr/exit status. It can read files using shell commands. Older model-authored replies are available as prior_replies.jsonl; prior researcher prompts, charters, assessments and the old user seed are not re-promoted as policy. Those old replies can themselves echo old prompts, so removing active instructions is not removing every historical influence.

transitions.json contains the three original historical eight-state matrices from the subreddit source established in ../minimal-markov-preparation-v1. LAWS.txt states indexing and transition semantics. No grouping, macro-state solution or score is provided. The matrices do not evolve automatically. They are finite computational material rather than an agent-controlled stochastic universe. Later comment variants are not mixed into this material. The original exact matrix has an absorbing state: a longer passive trajectory is not guaranteed to reveal all eight states.

## Conditions and results

Three real calls used cached SmolLM2-135M-Instruct, float32 CPU, two Torch threads, eager attention, T=.8, top-p=.9, 96 output tokens, 8096 input boundary, deterministic recorded seeds. No network model service, API key, external teacher, training or added adapter was used. Removing the canonical YES/NO/WITHHOLD LoRA is an explicit effective-model change relative to the old primary. The old weights/adapter/history remain available. This is not a matched causal comparison of adapters or prompts.

All three outputs were preserved before dispatch. The first combined assistant prose and an incomplete fenced shell example (exit 2). The second continued Markdown-like conversation guidance (exit 2). The third restated portions of the environment notice as prose (exit 127). No pilot output successfully created or modified a world file. There was no automatic repair or retry. These observations establish neither learning nor a lack of possible future learning.

Host tests independently verified persistent file changes, Python arithmetic, errors without rollback, host/observer inaccessibility, symlink isolation, unavailable external network, timeout/background-process termination, output limits, per-file limits and unchanged treatment of Markdown fences. Nine tests passed; several tests contain multiple assertions. These are infrastructure fixtures, not model behavior or artifacts imported into its pilot world.

All files in the original primary environment were hashed before and after: unchanged. Cursor 750 and its pause marker remain intact. The pilot world persists and is paused separately. Nothing is scheduled to continue in the background.

## Boundaries and limits

Bubblewrap isolates mount, PID, network and other namespaces, clears inherited environment variables and drops capabilities. /usr is read-only; /world is writable; /proc is namespace-local; /dev is freshly provided. Observer records, model weights and the research repository are outside the guest mounts. Unprivileged kernel isolation is an engineering boundary, not a proof against every kernel vulnerability.

Per-action wall time is 3 seconds. Per-process address space is 512 MiB, CPU 2 seconds, open files 64, user process count 64, individual file size 256 KiB; combined captured output is capped at 8192 bytes. /tmp has an 8 MiB tmpfs size. User process limits count other processes of the same UID and may constrain an action earlier. These are per-process limits, not an aggregate cgroup RAM/CPU guarantee. Processes/variables do not persist; files do.

World size 8 MiB and 2048 directory entries are checked between actions, not enforced as a hard filesystem quota. A single action can overshoot. The runner reports the overshoot and requires a pause; it does not silently erase model-created files. Before long autonomous operation, implement and test an aggregate storage/process-memory boundary. This prototype should not be presented as an indefinitely bounded cloud computer.

The pilot's in-memory weight check used parameter_digest(model,False). A loaded base model has trainable flags true even during inference, so that partition can be empty. Do not interpret that check as a complete in-memory weight audit. Disk weights were hashed before/after and there was no optimizer or training code; generation runs under torch.inference_mode. pilot_executed.py preserves exactly the executed source. pilot.py now compares both digest partitions for future pilots. This correction did not require repeating the model calls or rewriting their records.

## Strongest next contact

First compare a concise action-interface description with the current long factual notice on disposable, matched starting worlds. Preserve prose and fenced failures as observed outputs. If a small model can use the connection without concealed repair, activate a versioned phase after 750 with an explicit parent link, retaining every old record and documenting the changed adapter/prompt/actuation conditions. Carry its own files and action consequences forward, and keep our assessments external. Do not silently import this diagnostic world's outcomes as the primary model's experience.

If raw shell remains unusable, measure that mismatch rather than pretending a more permissive world fixes model capability. Alternatives include a demonstrated command example or constrained interface, each an explicit experimental condition rather than an invisible correction. No reasoning recipe or compulsory success criterion is needed to test basic access.

The supplied SDPO paper (Reinforcement Learning via Self-Distillation, arXiv:2601.20802v2) concerns distilling feedback-conditioned predictions into weights. Its relevance is a future learning experiment after usable actions and feedback are established; it does not validate this pilot or guarantee self-teaching by a 135M model. Persistent files, context adaptation and weight learning remain separate mechanisms.
