# Scouting the difference between an open world and an unscaffolded inhabitant

14 November2026, America/Chicago. Targeted three-source primary-literature scout. This is selected-section reading, not a benchmark reproduction or implementation audit. Zero model calls, sandbox actions, installs or main-garden changes. The source versions and access limits are recorded in SOURCES.json.

## Three source contacts

**ReAct,2210.03629v3.** The method separates environmental observations, executable actions, and language that changes the conversational context without directly changing the environment. Its main prompting setup uses frozen PaLM-540B with human-written example trajectories; decision-making thoughts may occur sparsely rather than in a mandatory alternation. The paper also reports that prompted ReAct was the worst of four methods for PaLM-8B/62B in its HotpotQA comparison, before task-specific finetuning on3,000 successful trajectories changed that result. This is evidence that body, prompting and training condition matter, not a scale law or a direct result about135M. Read: version/abstract, introduction, §2, selected §3.2–3.3 and §4 setup material. No prompts or code were copied into our garden. [Versioned primary paper](https://arxiv.org/html/2210.03629v3).

**Voyager,2305.16291v2.** Its GPT-4-based Minecraft system avoids parameter finetuning but uses an automatic curriculum, executable skill library/retrieval, code-generation guidelines, environmental state reports, errors and a separate success-verification critic. The curriculum receives explicit exploration directives; generated tasks and suggested repairs are part of the mechanism. The paper reports limitations including stuck code generation, mistaken verification and hallucinated items/APIs. Its parameter-frozen adaptation is therefore a concrete example of scaffolded context/artifact accumulation, not a bare pretrained model left in a world. Read: version/abstract, introduction, §§2.1–2.3,3.1, selected3.4 and §4, plus selected appendix prompt/ablation descriptions. No software or services were run. [Versioned primary paper](https://arxiv.org/html/2305.16291v2).

**FormatSpread,2310.11324v2.** This study varies meaning-preserving prompt formatting in few-shot tasks. It holds example choice/order fixed while testing model families including LLaMA-2, Falcon and GPT-3.5. It reports substantial variation and possible reversals of apparent model comparisons across formats, and distinguishes answer-prefix from probability-ranking evaluation. Its prompt-equivalence notion is human semantic equivalence, not a claim of equal model processing. Read: version/abstract/introduction, selected §§3–4.3 and the beginning of appendixC's grammar limitation. No implementation or numeric result was reproduced. This motivates sensitivity controls, not a prediction of the size of an FRR effect or a guarantee of neutral padding. [Versioned primary paper](https://arxiv.org/html/2310.11324v2).

## Inferences for this design, separate from the source findings

The sources do not establish that our135M body will benefit from an FRR prompt. They expose rival explanations and help avoid borrowing an outcome without its enabling conditions.

1. **Keep three ledgers conceptually distinct.** The input exposed to the model, actual environment consequences and external observer interpretation are different objects. Generated explanatory language is not a captured internal execution state. A ReAct-style trace or Voyager critic would add a mechanism if introduced; neither is an observational necessity.
2. **Do not borrow a curriculum merely because it accompanies successful open-world work.** Voyager's explicit goals, suggested tasks, skill retrieval and critic conflict with the intended primary comparison if silently added. They can inform separate later experiments, but are not the minimalist default.
3. **Compare the whole FRR presentation before claiming its specific principle caused anything.** No-FRR versus FRR initially changes wording, length, role exposure and perhaps emphasis. A full-source arm and explicitly named adaptation can be compared as distinct interventions. More text or a shorter prompt should not be presumed better for the small body.
4. **Keep histories and opportunities matched.** Do not give the FRR branch fresh input while the control inherits repeated unsuccessful writing. Within each branch, preserve actual consequences continuously rather than resetting only the disappointing arm.
5. **Treat a later formatting/placement test as decomposition, not proof of inert controls.** If an initial difference is worth pursuing, predeclare a small alternative presentation and retain all outcomes. Searching until one FRR wording wins and reporting that winner would change the question.

## Strongest concrete improvement to the first protocol

Freeze a compact **exposure ledger** before model calls: exact body/revision and decoder, supported starting-world identity, complete initial messages, FRR text/hash/name, placement/role, tokenizer input length, history policy and per-branch call budget. Log whether any input is omitted to fit capacity; do not silently give one arm less usable history because its orientation is longer.

For the first open pilot, compare one no-FRR branch with one fixed adaptation under the same fresh framing and inherited filesystem. A full unmodified source arm is useful if budget permits, but it is not a neutral length control and should not be expected to win. This is exploratory evidence of a context intervention, not statistical proof of a framework's value. A later specific claim needs held-out situations and relevant consequences, not only different prose.

The observable sequence should distinguish inert writing, complete action expression, attempted execution, actual receipt, durable file change and later reuse. There need be no demanded action or score returned to the inhabitant. This preserves the user's intended exploration while allowing unsuccessful and inactive trajectories to remain interpretable data.

## Boundaries of this scout

No source studied our exact135M model, FRR text, rolling history, decoder or sandbox. No cited method was replicated. Papers' comparative numbers are not our baseline and were not adopted as success thresholds. Search results and third-party summaries were used to locate primary sources only; they are not independent evidence. No claim of novelty or general impossibility follows from this small search.

The strongest supported conclusion is methodological: **published open-world successes contain specific coupling and prompting mechanisms; supplying an orientation must be measured as an intervention, not mistaken for a property the pretrained model already had.**
