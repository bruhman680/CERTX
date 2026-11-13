# Framing-pair operational readiness review

9 November 2026, America/Chicago. This is a later evidence update to READINESS_REVIEW.md, whose missing write/read criterion was accurate for the first two diagnostics. No old failures are relabeled. This reviewer made zero model calls and zero guest operations; all new writes stay in this review directory.

## Newly established operational contact

The prospectively planned framing pair used six new calls: three familiar file questions in each of two new stores. No program source, program arguments or repaired functions were supplied by an operator. Both stores use the same pinned world mechanics, model, greedy body, 256-token limit and fresh subprocess/restoration per reply. Initial framing differs: the minimal condition begins with the question alone, while the standard condition also includes the candidate mechanics and invitation. This is a joint framing comparison, not an isolated causal test of one word or of notice length.

In the minimal condition, the first model reply contains a read cell and a write cell. Reading the initially absent file causes a real FileNotFoundError. The second complete cell still runs and writes the two bytes `37` to memory.txt. Its checkpoint survives process/world restoration. New code in turns 2 and 3 executes an actual `open('memory.txt','r')`, assigns `file.read()` to a variable, then prints that variable. The real stdout is `37` followed by newline. This is actual retrieval of saved world state, not a constant printed from task text. Later write cells re-store 37. The requested add-five operation does not occur.

The independently checked minimal per-cell file timeline is: absent → 37 → 37 → 37 → 37 → 37. Saved state and actual consequences enter subsequent model inputs under the declared growing transcript. This supplies the missing prompted model-driven persistent write/read evidence for this world/body family.

## Standard framing has actual effects and poorer results

The standard condition also creates memory.txt and writes 37. Its additional malformed multi-context-manager cell first opens the file in write mode, truncating it, then raises a real TypeError. The partial effect persists: no rollback or repair hides it. The per-cell timeline is absent → 37 → empty → empty → 37 → empty → empty → 5 → empty. The later read cells do open and read the actual empty file, but do not print its contents. Therefore do not claim the standard model observed the empty contents through stdout. It receives the actual error/status receipts.

These are lawful consequences of the prospectively declared rule that every complete recognized cell executes in order, including code introduced in prose as an alternative. The observer does not infer which example was intended, omit a harmful later cell to keep a successful result, or reinterpret old fenced examples retrospectively.

## Independent audit

`audit_framing_pair.py` rechecks both closed stores from retained bytes: parent state, source pins, contiguous event/receipt/bundle chains, raw-to-authoritative batches, exact source offsets, object hashes and final states. It reconstructs each intermediate file state directly from the saved content objects, checks the expected partial effects, and inspects the minimal read AST to distinguish real file retrieval from constant printing. FRAMING_PAIR_RETAINED_AUDIT.json contains the result and exact cell timeline. No simulator or neural rerun was performed.

## Readiness disposition

The operational foundation is now demonstrated in a narrow prompted sense: declared model-generated cells can alter files, later calls can retrieve persisted bytes after restoration, and real errors/consequences are observable. The default standard framing is capable of actual file control but is not shown to perform these tasks robustly or retain the desired final contents. Minimal framing's stronger result must not be generalized into universal superiority.

A separate open pilot can now be observed without requiring a successful action or changing behavior when it repeats or errs. Root's OPEN_PILOT_PLAN.json prospectively declares 12 maximum replies in blocks of 4 and 8, no control tasks, unchanged broad invitation, and mechanical stop criteria only. That is consistent with the user's aim of laws governing the environment rather than preferred model behavior. Full activation should still depend on source/state integrity and honest pilot reporting. No independent curiosity, emergence, autonomous repair, general tool competence, or weight learning has been established.

The candidate remains a bounded computational notebook over a broad Python/Linux runtime. A small interface is not a complete Conway-sized specification of all underlying software. Its entire actual transcript can also eventually exceed context or self-reinforce; the declared capacity pause and persisted evidence remain necessary. The reference version at 1550 should remain intact, and any active-pointer change must explicitly identify this new version rather than an unchanged frozen continuation.
