# FRR/mechanics components and content-preserving order controls

17 November 2026, America/Chicago. Four new detached diagnostic calls under separately frozen budgets [2,2]. No main-garden continuation, model training, source repair or prompt change has been activated.

## Findings

Neither FRR-only nor mechanics-only achieved the original print-1 task. FRR-only emitted a naturally closed Python cell that printed a usage message and exited 0. Mechanics-only emitted an unclosed Python fence containing a growing numbered comment list, reaching the 256-token bound without a supported complete cell.

Two follow-up order changes retained all original full-context content. Both had the same 1,063 input tokens as the preserved full-system baseline. Reversing the FRR/mechanics section order emitted an unclosed comment-list fence. Moving the question before the observation emitted a numbered comment list after a triple quote, without a supported executable fence. Neither restored a complete handoff or exact task success.

This contact provides negative results and clearer distinctions, not an improved model or a validated replacement prompt. In particular, an error-free interpreter exit is insufficient to identify a correct result.

## Actual outcomes

The original question remains: “Produce one complete executable Python cell that prints the digit 1.” Every new case uses the same actual initial serialized observation packet. The later no-argument clarification from the previous contact is not used here.

| New case | Input tokens | Output tokens / stop | Actual Python cells | Actual interpreter result | Exact task met |
|---|---:|---|---:|---|---|
| FRR-only | 382 | 176 / EOS | 1 | Usage line, exit 0 | No |
| Mechanics-only | 802 | 256 / limit | 0 | No actor process | No |
| Full system, mechanics before FRR | 1063 | 256 / limit | 0 | No actor process | No |
| Full system, question before packet | 1063 | 256 / limit | 0 | No actor process | No |

The preserved native-default-plus-packet case previously printed `1\n` and exited 0 with 141 input tokens. The preserved original full-system-plus-packet case used 1,063 input tokens and produced no supported cell. These are reference trajectories, not additional calls or replications in this contact.

FRR-only's actual literal code was:

```python
import sys

def print_digit(num):
    print(f"1 {num}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        num = int(sys.argv[1])
        print_digit(num)
    else:
        print("Usage: python program.py <num>")
```

The process had no supplied command-line argument. Actual stdout was `Usage: python program.py <num>\n`, stderr was empty, exit code was 0 and no runtime boundary was reached. This is a completed handoff and an error-free process with the wrong output. The program also would not print only 1 in the supplied-argument branch. Its accompanying prose claims that direct execution prints 1; the literal receipt contradicts that claim in this runtime. We supplied no argument, repaired nothing and did not rerun the cell.

Mechanics-only began with a statement claiming to provide a complete executable cell, then an open Python fence, a shebang and sequential `# 1`, `# 2`, ... comments. The system-order reversal likewise opened a Python fence and counted in comments without closing it. These incomplete fragments were not executed. The question-first case used a triple quote rather than a supported Python/sh fence; it also did not execute. We did not reinterpret comments or prose as actions, close a fence or infer an intended program.

## Prospective comparisons and their limits

The component protocol was frozen before its two calls. We split the exact preserved full system at its existing three-newline boundary before `/world`. FRR-only contains the verbatim FRR component. Mechanics-only retains the mechanics component and its leading whitespace, with one narrow truthfulness correction: remove “FRR, ” from the sentence describing the supplied initial context. That component is absent in the case. Both cases retain the same packet and original question. The exact original components, replacement and prompts are archived.

This is not a matched-length comparison: the two inputs are 382 and 802 tokens, versus 141 in the native-plus-packet reference and 1,063 in the original full reference. Role identity, semantics and token length differ. The small self-description correction is also retained as an attribution limit. The results do not isolate a harmful or helpful FRR mechanism, and the fact that a case emits a complete cell is not evidence of task correctness.

After those outcomes, a separate two-call order protocol was frozen. The first exchanges the original verbatim FRR and mechanics sections across their three-newline delimiter, making no truthfulness edit because both components remain present. The second leaves the original full system byte-identical and exchanges the original question and observation across their two-newline delimiter in the user message. Each message preserves its original character inventory and length; audits independently check the transforms. All three full inputs, including the preserved baseline, tokenize to 1,063 tokens. The IDs and positions differ, as intended.

These order changes alter visible output form without restoring success. They do not show that order is irrelevant, that length causes the failures, or that any internal deliberation was identified. They test two specific arrangements at a fixed output budget, not every order or token budget. The original full baseline is an earlier stored deterministic trajectory, not a newly sampled control. No population success rate or statistical interaction estimate is claimed.

## Observation refinement

The consolidated external scorecard retains the distinct layers already enforced by literal receipts and the exact success criterion:

1. Did a supported, naturally closed cell reach the interpreter?
2. What stdout, stderr, exit code or resource boundary did it actually produce?
3. Did those effects satisfy the exact requested outcome?

`OUTCOME_LAYERS.json` applies these distinctions to the four new cases and the two preserved native/full packet references, with source paths and hashes. It records `completed_wrong_output` for the FRR-only cell despite exit 0. The other three new cases have `no_complete_cell`. Physical tick status and prose claims do not count as print-task success. This is an external observation refinement; it imposes no new behavioral gate on the model or world.

All four new cases receive the same actual verification world and unchanged physical law. Each entire raw response is submitted exactly once to the literal adapter. One actual actor cell and four physical ticks were committed; all ticks succeeded. No actor cell reads field.bin or creates a file. The physical tick is an environment operation, not an actor's requested print result. The code was run by the operator verification path, so there is no autonomous-action claim.

## Integrity and reproduction

The cached body remains HuggingFaceTB/SmolLM2-135M-Instruct, verified repository revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, model-file SHA-256 `5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c`. The loaded parameter digest is checked before and after every call. Fixed float32 weights, eager attention, two CPU threads, greedy argmax, fresh attention caches, maximum 256 generated tokens and the same 62-byte world seed are retained. No download, paid inference, external teacher, source correction, repeated generation or training is involved.

Both completed audits pass. They verify exact inputs/templates/tokens, decoded raw output, parser-to-source correspondence, actual process receipts and engine events, checkpoints and paused/no-pending state. The first protects 2,255 prior files, including the entire previous context-corners contact. The second protects those plus 50 completed parent-contact files, totaling 2,305. These inventories overlap; they must not be added together as independent files. Both protocols and all failures remain intact. The combined report and sync snapshots are in this follow-up directory to leave the frozen parent files unchanged.

The selected main garden is unchanged at entry 1630 and the reference candidate at turn 38, both paused. The active garden pointer, previous world physics and historical data are unchanged. All four diagnostic worlds are paused after one reply, with no pending action, background inference or queued call. New report, summary, manifest and current navigation records are synchronized separately from preserved experiment histories.

To reproduce audits without inference, use the cached environment Python to run `../audit.py` and `audit.py` from this directory. Do not rerun either inference runner: its saved state and one-call-per-case guards intentionally prevent replay. The main and reference worlds remain paused.

## Confidence and next direction

High confidence in the literal outcomes, the distinction between complete execution and correct output, and file preservation. No confidence in a general claim that FRR or mechanics alone explains the native/full difference. Neither removing one component nor either tested reorder provides a task-success improvement here. The observed error forms differ across conditions, but their internal cause remains unmeasured.

The next useful control is to address prompt length and content under matched native assistant framing. A prospectively specified comparison should keep the helpful native preface, packet, task, model, decoder and output budget fixed, then compare the FRR component with independently specified task-irrelevant text at matched input length. Such text must be described as a control passage, not assumed cognitively neutral. Keep any native-preface change explicit, save token matching before calls, and retain ordinary failures. If needed, use more than one independently specified passage before attributing an effect to FRR semantics. These controls are a plan, not a queued run or a justified garden patch.

Garden view: one route reached the workbench and declared the job finished while leaving a usage sign. Other routes kept numbering the margins without delivering a usable cell. Moving the signs changed the marks, but not the harvest. Our measuring station can tell those events apart; we have not yet earned a claim that the soil itself has improved.
