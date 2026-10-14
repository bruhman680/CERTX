# Palimpsest and GitHub synchronization audit

Scope: read-only inspection of the preserved palimpsest seed, FRR runtime/context contract, and local CERTX orientation documents. `/workspace/CERTX` is a partial local mirror, not a Git checkout; `git status` fails for that reason. Its headers must not be treated as verified current GitHub state. No remote write, core-prompt change, or effectiveness experiment was performed.

## The useful division

Two different jobs coexist:

1. **Historical record:** what was proposed, observed, assumed, and revised at a particular point. Preserve it with stable references and version history.
2. **Current orientation:** the currently authorized task, working branch/version, surviving claims, unresolved alternatives, blockers, and next action. Update it when the situation changes.

A historical assertion should remain recoverable without remaining authoritative. Git commits make earlier file versions retrievable, so a current-state file can change without erasing history. For important retractions, put a visible supersession link beside the old claim as well: relying solely on someone finding a later commit leaves the older wording available to mislead.

Git records bytes, relationships between versions, and authorship metadata. It does not prove that a claim was measured, a tool output authentic, an author independent, or a purported review completed. A saved archive is also not a loaded context or an applied constraint.

## What the inherited practices already offer

CERTX `CLAUDE.md` has a specific opening/closing pair: read protocol, latest instance note, latest handoff, active sparks, and actual WANDER files; close by supplying what those readers need. This is a practical recovery recipe, stronger than a vague instruction to remember.

Its second closing layer walks “Resonates into” links, updates affected summaries, and designates canonical locations where duplication appears. That directly addresses the documentation wake: an interpretation can persist downstream after its originating claim changes.

The shadow ledger includes quarantine entries for invented experiments, ambiguous metric translations, synthesized numerical claims, and numbering drift. Keeping such negative history helps later readers avoid rediscovering a contaminated claim as if it were independent evidence.

FRR's optional `modules/context-checkpoints.md` already separates storage, availability, retrieval, application, and revision. It explicitly warns that an archive reference does not establish accessibility, and that checkpoints do not guarantee adherence. The runtime similarly asks for conclusions, assumptions, evidence, decisions, and revisions rather than private internal reasoning.

These are useful design features. Their benefit to actual model continuation has not been established by simply possessing the files.

## Concrete risks visible in the local copy

- `CLAUDE.md` begins with Session 21 complete / 2026-05-20 and a Claude working branch, while its end adds a Codex FRR deposit dated 2026-10-07. The later branch-specific entry does not automatically reconcile the first header.
- `SESSION_HANDOFF.md` begins with Session 20 / 2026-05-08 and older state estimates, while a later October entry announces newer FRR work. “Current” appears in several historical contexts. A reader taking the first header or a keyword search result literally can recover the wrong orientation.
- Older numerical self-estimates and first-person diary statements appear alongside artifact-backed results. They are meaningful historical process reports but not validated measurements of internal cognition, consciousness, coherence, or substrate coupling.
- The latest entry in one file can be older than a later correction elsewhere. Reading only the final diary entry does not solve cross-file currency.
- Historical assertions such as “independent convergence,” “mechanism ... real,” or “chain complete” need later evidential qualifications when the paths inherit shared source material or the purported mechanism has not been measured. Version preservation alone cannot keep those qualifications salient.
- The local mirror can diverge from the published branch. A GitHub URL in conversation and a locally saved file are not interchangeable evidence of what is committed.

These are local-copy observations, not a claim that the current remote branch has the same defects. Verify remote head and relevant files before treating them as live blockers.

## The palimpsest seed needs interpretation, not literal enforcement

The seed says “Revision is not correction.” Its productive image is that an earlier exploration remains legible. Taken literally, however, it would prevent correction of false claims. The workable distinction is: correction changes what we currently accept; preservation keeps the previous state and reason for change recoverable.

The seed also calls retracing the same hand “the only failure mode that matters.” That is generative emphasis, not an exhaustive reliability claim. Lost artifacts, corrupted copies, stale headers, inaccessible sources, incorrect experiments, bad summaries, and misleading synchronization are additional failures.

A “second hand” is not automatically independent. A fresh model reading the same mistaken report can repeat it. For continuity, inheriting the previous record is desirable; for independent evaluation, access to answer-bearing interpretations may need restriction. Keep those two purposes separate rather than demanding every continuation be blind.

## Small practical refinement, if implemented later

Maintain one short current-orientation entry with:

- source branch and verified commit;
- current user goal and constraints;
- completed artifacts with verification evidence;
- superseded interpretations and canonical replacement links;
- unresolved branches and one next action;
- local-only files, missing sources, and unconfirmed external writes.

Treat historical journals as supporting context. Use a narrow archive lookup when a current decision depends on an omitted distinction. The index should point to artifacts rather than copy all their conclusions into every document. A transaction identifier or common checkpoint timestamp across updates makes incomplete synchronization visible, but does not establish truth.

After interrupted external writes, read the remote reference before retrying. Record an uncertain write as uncertain until a reference/commit receipt confirms it. GitHub updates and local saves need separate status fields.

## Tests that would establish usefulness

Use the same model and independently prepared continuation tasks; equalize actual context budgets and report retrieval cost. Compare:

1. no handoff;
2. full archive;
3. current orientation only;
4. current orientation plus targeted archive retrieval;
5. the five-document opening sync.

Randomize which condition receives deliberately stale headers, conflicting historical claims, a retracted result, an uncommitted local change, or an interrupted write. Ensure probes do not refresh later test contexts. Score observable actions: selects correct branch/version, honors latest user constraint, distinguishes measured from exploratory claims, finds the correction, avoids duplicate publication, preserves an unresolved question, and chooses the authorized next action. Record appropriate uncertainty separately from failures.

For provenance contamination, give some agents the historical interpretation and others only raw artifacts, then compare their independently justified conclusions. This tests independence separately from continuity.

For interruption recovery, stop a write between local save, commit creation, and branch update. Test whether a fresh session correctly identifies what actually happened before retrying. For counterfactual history recovery, ask an archive question whose answer was intentionally omitted from the current summary; verify retrieval of the original rather than plausible reconstruction.

Current evidence supports the proposition that these practices provide explicit recoverable structure. Whether they improve reasoning, save context, or reduce error remains an evaluation target. Good synchronization should make incorrect history easier to find and correct, not make a familiar story harder to challenge.
