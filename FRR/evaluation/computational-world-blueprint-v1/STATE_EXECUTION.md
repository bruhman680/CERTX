# State, execution and recovery contract — v1

Client date: 5 November 2026, America/Chicago (host UTC 6 November). This document specifies behavior; it does not itself establish implementation or test success. It concretizes `../computational-world-three-cycle-v1/DESIGN.md` and `CYCLE3_EXECUTION_REVIEW.md`. `LANGUAGE.md` owns the documented R7RS-small Scheme subset and exact evaluator/cost rules; host persistence commands are application APIs, not Scheme library procedures. MUST marks a normative requirement. Numeric fixture values belong only to the versioned `constants.json`; they are provisional, unmeasured test choices rather than production recommendations.

## 1. Immutable world, aliases and canonical IDs

The guest world is `(world_id, artifacts, aliases)`: a stable host-assigned world identifier, immutable revision records keyed by content ID, and mutable friendly names pointing to those revisions. Artifact kinds are `data` and `procedure`. Drafts/notes are ordinary text/list data. A procedure record contains original submitted source text, declared name, ordered parameters, resolved AST, sorted direct dependencies and language/evaluator versions. No revision is overwritten. Rebinding a name does not retarget historical callers.

Canonical encoding `C` is JSON encoded as UTF-8 without BOM/whitespace. Arrays retain order; unique object keys sort by unsigned UTF-8 bytes. Strings contain Unicode scalar values without normalization. Escape quote and backslash; U+0000–001F use lowercase `\u00hh`; escape no other characters. Reject lone surrogates. Allowed JSON types are string, array, object, boolean and null: all integers/counters are decimal strings, with no leading zero, plus or negative zero. Source integers may have alternate spellings; this canonical representation may not.

Runtime values encode as `["int","-3"]`, `["bool",true]`, `["text","abc"]`, `["list",[V1,V2,...]]`. Value size is exactly `len(C(value))`. Source Scheme strings and canonical JSON strings use different escape grammars.

For kind `k` and record `R`, define `ID(k,R) = k + ":" + hex(SHA256(UTF8("cw-v1/"+k) || 0x00 || C(R)))`. Records contain a schema identifier but never their own ID. Kinds include `art`, `snapshot`, `request`, `capture`, `event`. Hash the full artifact including original source; equivalent programs with different source whitespace may have different IDs. Detecting equal IDs with unequal bytes is a fatal integrity error, never overwrite. Retain original canonical bytes; hashes alone do not reconstruct data.

Resolved AST forms are in LANGUAGE.md. External data/procedure references contain exact artifact IDs. Dependency manifests equal the direct references derived from the AST; verify kinds, existence and reachable-graph caps. Self recursion uses the ordinary procedure name in Scheme, compiled to the local `["self",args]` AST edge. Exclude that edge from external dependencies and hash the finite record once. At invocation the local edge denotes the containing revision. Never put its eventual own ID inside its hashed record. Nonself dependency edges form a DAG; mutually recursive publication is excluded.

A snapshot record contains schema, world ID, sorted artifact IDs, and `[name,id]` alias entries sorted by UTF-8 name bytes. Its content ID identifies exact guest visibility. Audit history and budgets are excluded: an inspection can add a receipt without changing the snapshot. Retain the snapshot records needed by admitted requests. Receipts, requests, captures and snapshots occupy bounded host audit/metadata space, separate from guest artifacts.

`drop` removes an alias only. No v1 operation deletes artifacts, snapshots, request identities or receipts. Dropping a name does not reclaim revision bytes, including dependencies/checkpoints. No silent garbage collection, retention expiry or history pruning is permitted. Complete export includes manifests, referenced bytes and audit/request records; export does not authorize deletion. Deduplicated identical artifacts add no artifact bytes, but requests/aliases/receipts still incur their own charges.

## 2. Request envelope and capture

The host generates an envelope for each new author action:

```
{
 "schema":"cw-request-1", "world_id":"...", "request_id":"...",
 "expected_world_snapshot":"snapshot:...", "command":"<exact submitted text>",
 "language_version":"...", "evaluator_version":"...", "cost_version":"cw-cost-1",
 "profile_id":"...", "limits":{"limit_name":"decimal allowance"}
}
```

Request IDs are 128-bit opaque host-generated tokens encoded as 32 lowercase hex digits, unique within the world. Hash the entire canonical envelope as a `request` record. The host adapter supplies IDs/snapshots; the agent does not guess them. Retrying preserves all bytes and limits. A consciously revised action receives a new request ID. Every command requires whole-world snapshot equality before execution, including reads. This CAS is stronger than a per-alias expected-target check; mutation syntax needs no separate CAS argument.

The command surface is `put`, Scheme-compatible `define`, `run`, `run-save`, `inspect`, `list`, `drop`, `help`; exact syntax is in the public protocol. Publication/inspection wrappers are not callable inside guest code. Before evaluation, resolve free data names and procedure operators from the recorded immutable snapshot, replacing them with exact revision IDs. Stored procedures contain no unresolved aliases. No guest evaluation reads the current alias map, host filesystem, network, clock or ambient mutable state.

A captured invocation contains snapshot ID, root procedure ID or resolved expression AST, explicit positional arguments/literals, sorted direct/reachable dependency IDs, versions and effective limits. Store its canonical bytes and capture ID in bounded retained metadata. Materialized input values are retained in the request/capture or referenced immutable data artifacts. A source hash alone is insufficient. Caps independently cover procedure source, reachable dependency graph and total library.

| Command | Successful guest effect | Status |
| --- | --- | --- |
| `put`, `define` | Insert immutable data/procedure if absent; bind target alias. | `PUBLISHED` |
| `run` | None; bounded value in receipt. | `COMPUTED` |
| `run-save` | Insert bounded result data and bind declared alias. | `PUBLISHED` |
| `inspect`, `list`, `help` | None; bounded projection/page. | `OBSERVED` |
| `drop` | Remove named alias; missing alias is an explicit no-op success. | `ALIAS_DROPPED` |

All effects, terminal request status, usage/capacity charges, resulting snapshot and receipt commit atomically. A pure run commits its audit outcome while leaving guest state unchanged. A later publication must resubmit bounded data via `put`; there is no unlimited staging cache or implicit retained result handle. A failed `run-save` publishes no successful result/checkpoint, even if computation finished before storage admission failed.

## 3. Admission, at-most-once and recovery

V1 serializes requests per world: at most one admitted unfinished request. Before admission allow only bounded envelope checks, hashing and request-index lookup. Check request identity before checking the current snapshot:

| Existing ID | Matching canonical request hash | Different hash |
| --- | --- | --- |
| Absent | Attempt admission. | Not applicable. |
| `ADMITTED` / `STARTED` | `PENDING`; never start another worker. | `REQUEST_ID_CONFLICT`. |
| Terminal | Return identical retained receipt; no execution/publication/action charge. | `REQUEST_ID_CONFLICT`. |

A conflict is a bounded `cw-transport-1` diagnostic containing request ID, stored/supplied hashes and `commit_certainty:"existing_request_only"`. It creates no new ledger event and does not modify the original request. Invalid envelope or exhausted admission capacity returns bounded `NOT_ADMITTED` with reason and `commit_certainty:"not_admitted"`; no durable receipt is promised. These responses remain possible when audit space is full. Delivery attempts have independent finite byte/rate allowances.

Admission atomically reserves the maximum terminal receipt plus bounded request/capture/snapshot/index metadata, charges one visit action, and persists `ADMITTED` with exact envelope/hash/snapshot/reservation. Guest storage cannot borrow this reserve. Only after admission perform command parsing, snapshot checking, validation and capture. Persist `STARTED` before evaluator entry; an ID can enter it once.

On restart, an unfinished `ADMITTED`/`STARTED` request is finalized `FAILED_HOST_ABORT` with unchanged guest state unless reconciliation finds its full terminal transaction committed. Do not resume or reexecute it. Pure execution has no effects outside the terminal transaction. This provides at-most-once execution as well as publication; interrupted computation is lost.

A storage exception never proves rollback. Reconcile the durable request index: if terminal, return that exact receipt; if definitely uncommitted, commit a no-world-change infrastructure failure using the reserved slot; if certainty is unavailable, return transport `UNKNOWN_COMMIT`. It has no invented receipt ID/after-state. Block new admissions until resolved, and retry/reconcile the same ID. Unknown admission durability follows the same rule. A definitely aborted original publication whose failure receipt is durably committed is `FAILED_STORAGE_KNOWN`.

## 4. Execution and limits

Use explicit evaluator control/continuations, not unbounded host recursion. LANGUAGE.md defines `cw-cost-1`: one fuel unit before each entered AST node, one additional unit before user-procedure invocation, and its exact primitive surcharge after operands/type/domain checks. Other evaluator bookkeeping costs zero fuel but cannot loop independently of charged progress. Tail calls reuse continuation space. One shared budget/cost version governs captures, evaluation, receipts and replay.

Before a charge, check all required allowances; fail before performing an unfunded operation and do not debit its unperformed charge. Already performed work remains charged. An already computed value may return through zero-cost bookkeeping with zero remaining fuel. Logical allocation cumulatively charges canonical produced-value bytes under LANGUAGE.md; it is not refunded and is not a claim about host RAM. Frame, argument, environment, value, integer, AST and depth limits apply independently.

Separate finite limits cover submission/source bytes, nodes/depth, procedure/reachable dependency bytes, fuel, allocation, frames, integer bits, value/result/trace bytes, output pages, artifact entries/bytes, aliases, host request/capture/snapshot metadata and audit records. Finite visit totals cover admitted actions, evaluator fuel/allocation, observations and model tokens. Pausing/reloading does not reset totals. A profile supplies every cap and is frozen within an experimental condition.

Host parsing, resolution, hashing, serialization, index traversal and writes consume a separate common host-work budget. Charge one unit per processed byte plus one per visited syntax/graph/index entry; overlapping processing stages each charge their own work. Hashing charges bytes fed, encoding bytes emitted, copying bytes copied, parsing bytes scanned plus nodes produced, graph traversal edges examined plus nodes visited. Implementation-specific extra traversals must also be bounded/charged. Reserve conservative work/workspace before bulk routines or perform bounded incremental work. Failure-event serialization has separately reserved host work inaccessible to guest work. Physical process-memory/time watchdogs are separate measured safeguards; interruption is `FAILED_HOST_ABORT`, not a guest error or successful checkpoint.

| Phase | Checked before work | Effect on failure |
| --- | --- | --- |
| Admission | Envelope bounds, ID lookup, audit/metadata reserve, visit action. | `NOT_ADMITTED`, or uncertain transport outcome. |
| Validation/capture | Expected snapshot, syntax/resolution, source/graph/capture bounds. | Funded validation/precondition/limit event; no guest change. |
| Evaluation | Durable start, exact versions, fuel/allocation/frame/value bounds. | Funded guest/limit/host-abort event; no guest change. |
| Staging | Exact result/event encoding, prospective guest capacity, snapshot CAS. | Funded limit/precondition event; discard candidate. |
| Commit | Atomic durable transaction. | Known failure event or `UNKNOWN_COMMIT`; never partial visible publication. |
| Delivery | Projection/page and visit observation allowance. | Bounded delivery error; stored outcome unchanged. |

## 5. Reproducible receipts and exact transitions

Each admitted request with a known terminal outcome has exactly one canonical event core:

```
{
 "schema":"cw-event-1", "world_id":"...", "request_id":"...", "request_hash":"request:...",
 "status":"COMPUTED", "phase":"commit", "commit_certainty":"committed",
 "before_world":"snapshot:...", "after_world":"snapshot:...",
 "audit_before":{"sequence":"17","head":"event:..."}, "audit_after_sequence":"18",
 "capture_id":null, "versions":{"language":"...","evaluator":"...","cost":"cw-cost-1","profile":"..."},
 "limits":{}, "usage":{"eval_fuel":"0","logical_alloc_bytes":"0","peak_frames":"0","host_work":"0","artifact_bytes_added":"0","observation_bytes":"0"},
 "result":{"value":null,"artifact_ids":[],"alias_changes":[],"projection":null},
 "error":null, "trace":{"retained_bytes":"0","truncated":false},
 "host_outcome":{"watchdog":false,"interruption":null}
}
```

Compute `e=ID(event,core)`. The reproducible receipt wrapper is `{schema:"cw-receipt-1",receipt_id:e,event:core,audit_after:{sequence:core.audit_after_sequence,head:e}}`. Hash the core, not this self-describing wrapper. `audit_before.head` links the previous event; genesis has sequence `"0"`, head `"GENESIS"`. Thus before/after audit state is exact without a self-referential digest.

`error` is null or `{code,limit,source_span,details}` with bounded typed fields; unavailable fields are null. Source spans are half-open UTF-8 byte offsets in retained source. Diagnostics never embed unbounded source/stacks. `result.value` holds only a bounded pure-run value; saved values are retrieved by artifact ID. Alias changes record name/before/after, using null for absence. Preserve exact performed usage and failing limit; discard staged results. Reserve enough space for a full canonical result or fail `FAILED_LIMIT`, never truncate the canonical value into apparent success. Long source/capture bytes remain in separately reserved records referenced by ID.

Usage in the event includes its initially prepared deterministic observation size; later deliveries/retries use a separate visit meter without rewriting the receipt. Release unused reservation after terminal commit, retaining actual bytes forever. Wall timestamps/operator prose/delivery attempts are operational metadata outside the event core. Trace truncation is explicit.

Let current guest snapshot be `s`, audit `(n,h)`, and terminal event ID `e`:

| Case | Guest before → after | Audit before → after | Outcome |
| --- | --- | --- | --- |
| `put`/`define`/`run-save` success | `s → s'`, possibly same on dedup/no-op | `(n,h) → (n+1,e)` | `PUBLISHED`; effects and receipt atomic. |
| Pure run / read/help | `s → s` | `(n,h) → (n+1,e)` | `COMPUTED` / `OBSERVED`. |
| Drop | `s → s'` | `(n,h) → (n+1,e)` | `ALIAS_DROPPED`; revisions retained. |
| Stale snapshot | `s → s` | `(n,h) → (n+1,e)` | `FAILED_PRECONDITION`; no evaluation. |
| Syntax/name/dependency invalid | `s → s` | `(n,h) → (n+1,e)` | `REJECTED_VALIDATION`. |
| Runtime type/domain/arithmetic error | `s → s` | `(n,h) → (n+1,e)` | `FAILED_EVALUATION`. |
| Any admitted fuel/allocation/frame/size/publication cap | `s → s` | `(n,h) → (n+1,e)` | `FAILED_LIMIT`; exact cap and performed usage. |
| Known storage abort / recovered unfinished request | `s → s` | `(n,h) → (n+1,e)` | `FAILED_STORAGE_KNOWN` / `FAILED_HOST_ABORT`. |
| Unknown durable outcome | Unknown to caller | Unknown to caller | `UNKNOWN_COMMIT`; reconcile before admission. |
| Same ID/hash retry / conflicting ID reuse | Unchanged | Unchanged | Existing receipt / `REQUEST_ID_CONFLICT`. |
| Capacity failure before admission | Unchanged | Unchanged | `NOT_ADMITTED`; no promised event. |

## 6. Replay, pause and checkpoints

Replay requires retained canonical request/capture/input/dependency bytes, snapshot, exact language/evaluator/cost versions and limits. Missing versions/data yield `REPLAY_UNAVAILABLE`; never substitute current aliases/helpers. Deterministic guest replay reproduces value or error code/span, ordered retained trace prefix, fuel/allocation and limit boundary. Cost-formula changes require a new cost version; profile changes are explicit interventions. Host watchdog/storage faults are infrastructure history, not deterministic guest results.

Replay verification runs read-only in an isolated scratch world with separate budgets. It does not reactivate the original live request ID. Equal guest results do not imply equal event hashes, which also include request/audit/world identity. Full restore verifies canonical bytes, snapshots, ledger chain and request index before new admissions.

Pause stops admission between known terminal actions and preserves state and budget totals. Resolve pending commit uncertainty before reporting a clean pause. Reload runs no code automatically. Exhaustion, failure and host abort save no VM/continuation/partial output. An explicit checkpoint is normally completed, quota-charged data published through `run-save`/`put`, containing algorithm progress and pinned procedure/input references as ordinary data. A later request consumes it explicitly; the host supplies no magical resume operation. IDs inside text do not become executable dependencies automatically. No unlimited staging cache, active-VM persistence, deletion or implicit budget reset exists in v1.


## Implemented interrupted-counter rule

If a process aborts without returning evaluator counters, its recovered receipt records those counters as null and marks them unavailable. Separate quota charge fields conservatively consume up to that invocation’s allowance (bounded by remaining visit quota); they are not claimed as measured work. Recovery never fabricates zero executed work from missing counters. The host prototype and hard-exit check implement this distinction.
