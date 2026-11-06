# Language contract: a restricted R7RS-small Scheme authoring surface

5 November 2026 (client date; host UTC 6 November). Proposed contract for a restricted R7RS-small Scheme subset, not full R7RS conformance. Numerical deployment limits require host measurement. Implementation and validation status are reported separately. No model/primary-state change is part of this language specification.

## 1. Standard boundary

The selected authoring language is a restricted subset of [R7RS-small Scheme](https://standards.scheme.org/corrected-r7rs/r7rs.html). Its [§4](https://standards.scheme.org/corrected-r7rs/r7rs-Z-H-6.html) supplies the selected variable, quote, call, conditional and binding forms; [§3](https://standards.scheme.org/corrected-r7rs/r7rs-Z-H-5.html) supplies lexical scope, Scheme truth and proper tail recursion; [§6](https://standards.scheme.org/corrected-r7rs/r7rs-Z-H-8.html) supplies primitive names/behavior. This proposal selects left-to-right operand evaluation, a sequential order permitted by Scheme.

The grammar and primitive table are exhaustive whitelists. Excluded: symbols as values, characters as independent values, improper/cyclic lists, other numbers, vectors, first-class procedures, source `lambda`, closures, computed operators, `apply`, `eval`, macros, quasiquote, local definitions, multiple body expressions, mutation, I/O, imports, continuations, guest exception handlers and mutually recursive groups. Unlisted syntax is rejected, never delegated to host Scheme. Procedure artifacts are not guest values. Runtime strings never select code or host operations. Persistence commands are separate host actions.

## 2. Source grammar and bounded reader

One host request contains one complete action; its embedded Scheme expression or definition uses the grammar below. Whitespace is ASCII space, tab, CR or LF; separators are required wherever token concatenation would change tokens. Parentheses, quote and double quote delimit tokens. No comments, directives, reader extensions or bracket alternatives are admitted in v1. These are reader restrictions, not claims about the complete Scheme grammar.

```ebnf
integer    = ["+" | "-"], digit, {digit} ;
boolean    = "#t" | "#f" ;
name       = letter, {letter | digit | "-" | "_" | "?"} ;
letter     = "A".."Z" | "a".."z" ;
scalar     = integer | boolean | string ;
datum      = scalar | "(", {datum}, ")" ;
constant   = scalar | "'", datum | "(", "quote", datum, ")" ;
expr       = constant | name
           | "(", "if", expr, expr, expr, ")"
           | "(", "let", "(", "(", name, expr, ")", ")", expr, ")"
           | "(", callee, {expr}, ")" ;
callee     = name | "+" | "-" | "*" | "=" | "<" | "<=" | ">" | ">=" ;
definition = "(", "define", "(", name, {name}, ")", expr, ")" ;
```

`digit` is ASCII 0–9. Decimal literals with leading zeroes and an optional plus are accepted and canonicalized: `+003` is integer 3 and `-0` is integer 0. A bare `()` is not an expression; `'()` is the empty list. Quotation admits only the `datum` grammar: `'tag`, `'(a 1)`, `''()` and quoted executable syntax are rejected because symbols are outside this value subset. `(list "tag" 1)` is supported. Unquoted `(1 2)` is not a list literal or valid call.

A `string` is double-quoted Unicode scalar text. Raw quote/backslash must be escaped; raw control scalars U+0000–001F and U+007F must use escapes. Supported Scheme escapes are `\a`, `\b`, `\t`, `\n`, `\r`, `\"`, `\\` and `\xHEX;` with one or more hexadecimal digits denoting a scalar. Escaped surrogates, values above U+10FFFF, JSON `\u` escapes, backslash-newline continuations and unknown escapes are rejected. Input bytes must be valid UTF-8; no normalization or case folding occurs. This is a restricted Scheme string reader, not JSON. JSON used by the enclosing host envelope is a distinct encoding layer.

Names are case-sensitive. Reserved names are `if let quote define` and all primitives in §5; none may be procedure names, parameters or `let` binders. Parameters are distinct. A procedure's own name cannot be a parameter/local binder in its body. Other lexical values may be shadowed. A local value in operator position gives `NOT_CALLABLE`; procedure identifiers in value position give `UNSUPPORTED_VALUE`.

Bound UTF-8 bytes before parsing; bound token bytes, nesting, datum/AST nodes and decimal digits during reading, before expensive conversion. Parse and resolve every branch: unresolved names/arity fail even in dead branches, while unselected valid branches incur no runtime work.

## 3. Values, scope and dependency capture

The disjoint value types are `Integer`, `Boolean`, `Text` and `List`; `List` is a finite sequence of supported values, recursively. Integers are mathematically exact with `bitlen(n) = max(1, floor(log2(abs(n)))+1)` for nonzero n and 1 for zero. The configured `integer_bits` limits `bitlen`; sign is not an extra magnitude bit. No coercion, rounding, wrapping or saturation occurs. Boolean values are distinct from integers: host `true` must not accidentally become integer 1.

Text is a sequence of Unicode scalar values, not UTF-8 bytes, UTF-16 code units or grapheme clusters. `string-length` and `substring` count scalars. Bounds are zero-based and half-open: `0 <= start <= end <= string-length`. No normalization means composed `"é"` and decomposed `"e\x301;"` are unequal, of lengths 1 and 2. `"A😀é"` has scalar length 3 and UTF-8 length 7; `(substring "A😀é" 1 2)` returns `"😀"`.

Lexical scope is static. A definition captures all nonlocal data/procedure references from the host's recorded immutable alias snapshot at definition admission. Free value names must resolve to data artifacts; free call names must resolve to procedure artifacts. Missing/wrong-kind dependencies reject the definition, including in dead branches. Top-level runs resolve names once from their own snapshot. Arguments and `let` values are explicit local inputs; there is no ambient world lookup while running. All procedure/data revisions reachable through captured references are retained/pinned by the storage contract. Definitions may not capture an unresolved draft or a future definition.

A call to the definition's own name compiles to local self, denoting the new revision regardless of the old alias. Nonself calls pin existing revisions. Thus dependency publication is acyclic apart from local self; references to older revisions remain fixed. No `@version` syntax or `SELF` keyword exists. Snapshot capture is a host module policy, not ordinary mutable Scheme top-level rebinding.

## 4. Evaluation and errors

Each expression returns one supported value or fails. Calls evaluate operands left to right, then check argument types left to right, then domains. Known arities are checked at resolution. Parameters bind positionally in a fresh environment without caller locals. There is no runtime parser or symbol lookup.

`if` evaluates its condition and exactly one branch. **Only `#f` is false**: 0, empty list and empty text are true. `not` tests this falsity. `let` evaluates its initializer once in the outer environment, then its body once in the extended environment. Tail positions are the run/procedure body and selected `if` branches/`let` bodies inheriting tail position. Tail calls must reuse continuation space but consume fuel. Evaluation uses explicit bounded state, never host recursion.

Errors are host-owned diagnostics, never guest values and never successful checkpoints. Proposed stable language codes:

| Code | Trigger |
|---|---|
| `SYNTAX` | Invalid reader token, unsupported form, wrong special-form shape or unsupported quoted datum |
| `UNBOUND_NAME` | No lexical or snapshot binding |
| `NAME_CONFLICT` | Reserved/duplicate/forbidden binder |
| `DEPENDENCY_KIND` | Data/procedure reference resolves to the wrong artifact kind |
| `NOT_CALLABLE` | Lexically bound value used as operator |
| `UNSUPPORTED_VALUE` | Procedure used as data or attempted improper-list result |
| `ARITY` | Call outside the admitted primitive/user signature |
| `TYPE` | Runtime argument has wrong supported type |
| `EMPTY_LIST` | `car`/`cdr` applied to empty list |
| `DIVIDE_BY_ZERO` | Zero divisor |
| `INDEX_RANGE` | Invalid scalar substring bounds |
| `INTEGER_LIMIT`, `VALUE_LIMIT` | Exact result exceeds declared representational cap |
| `OUT_OF_FUEL`, `ALLOCATION_LIMIT`, `FRAME_LIMIT` | Declared execution resource exhausted |

Errors/caps are world diagnostics, not standardized Scheme diagnostics. Reservation may fail before an operation; after operands, check types before domains before result work. Oversize exact integers report `INTEGER_LIMIT`, never wrapping. Storage/infrastructure errors are separate.

## 5. Primitive whitelist

Signatures below deliberately restrict the standard numeric tower and proper-list domain. Extra arities listed by Scheme but not admitted here are excluded calls. The spellings and selected behavior follow [R7RS standard procedures, §§6.1–6.7](https://standards.scheme.org/corrected-r7rs/r7rs-Z-H-8.html). All values are immutable in this world; identity/mutation observations are unavailable.

| Primitive | Accepted arguments and result |
|---|---|
| `+`, `*` | Zero or more integers; left fold with identities 0 and 1 |
| `-` | One or more integers; unary negation or left-associated subtraction |
| `floor-quotient`, `floor-remainder` | Two integers a,b with b nonzero; q=floor(a/b), r=a-bq; return q or r |
| `=`, `<`, `<=`, `>`, `>=` | Two or more integers; adjacent numerical relation must hold for all pairs |
| `equal?` | Two arbitrary supported values; structural equality, equal types, exact integer equality, scalar text equality, recursive ordered list equality |
| `not` | One arbitrary value; Scheme falsity test |
| `integer?`, `boolean?`, `string?`, `list?` | One arbitrary value; exact type predicate |
| `list` | Zero or more arbitrary values; list in operand order |
| `cons` | Arbitrary value and proper list; prepend; a nonlist second argument would create an unsupported improper pair and gives `UNSUPPORTED_VALUE` |
| `car`, `cdr` | One nonempty list; first value or remaining proper list |
| `null?` | One arbitrary value; true only for empty list |
| `length` | One proper list; integer element count |
| `append` | Zero or more proper lists; concatenate in argument order; all nonlist arguments rejected, including standard Scheme's optional improper final tail |
| `string-length` | One text; integer scalar count |
| `string-append` | Zero or more texts; concatenation |
| `substring` | Text, integer start, integer end; scalar slice under §3 bounds |

No `/` or truncating division is admitted. Negative arithmetic fixes `q=floor(a/b)` and `r=a-bq`:

| a,b | floor-quotient | floor-remainder |
|---|---|---|
| -7,3 | -3 | 2 |
| 7,-3 | -3 | -2 |
| -7,-3 | 2 | -1 |

Always `abs(r)<abs(b)` and nonzero r has b's sign.

## 6. Resolved AST and canonical value contract

The source reader produces an unresolved bounded syntax tree. Resolution creates only the following canonical tagged arrays; all child-array orders are significant:

```text
["lit", V]
["var", name]
["data", immutable_data_revision_id]
["if", condition, consequent, alternate]
["let", name, initializer, body]
["prim", primitive_name, [argument_ASTs...]]
["call", immutable_procedure_revision_id, [argument_ASTs...]]
["self", [argument_ASTs...]]
```

A procedure artifact includes ordered parameters, declared name, resolved body, source and dependency manifest. Local `self` avoids self-hash recursion. Every `var` has a lexical binder; `data`/`call` IDs are kind-checked. No top-level run contains `self`; no executable artifact contains unresolved/dynamic aliases. Quote/shortquote compile to the same `lit`; nested literal values have separate bounds.

Canonical guest values use JSON arrays: `["int","-3"]`, `["bool",true]`, `["text","abc"]`, `["list",[V1,V2,...]]`. Integer decimal strings have no plus, leading zeroes or negative zero. The canonical UTF-8 JSON function `C` is defined in STATE_EXECUTION.md: strings contain scalar text without normalization and use the specified canonical escaping; object keys are sorted, arrays are ordered, and no JSON numerical quantities are used. This JSON is the artifact/wire representation, not guest source. `size(V)` below is the byte length of `C(V)`.

## 7. Proposed deterministic cost model `cw-cost-1`

Accounting formulas are versioned; numerical limits are host-policy inputs recorded per invocation. Fuel is abstract work, not CPU time. Charge 1 before entering each AST node and another 1 before invoking each user body. After operands and type/domain checks, charge primitive surcharge below before work. Returns/bookkeeping add zero: they can only pop/update continuations created by charged node entries and cannot loop independently.

Let `b(n)=bitlen(n)`, `S=sum(size(argument))`, and `A=number of arguments`. All table quantities are mathematical nonnegative counters; resource accounting cannot overflow host integers.

| Primitive | Additional fuel |
|---|---|
| `+`, `-` | For unary `-`: `1+b(x)`; for zero-argument `+`: 1; otherwise sum `1+max(b(acc),b(next))` over left-fold binary operations, plus 1 for a single-argument identity case |
| `*` | Zero arguments: 1; otherwise sum `1+b(acc)*b(next)` over left fold starting with identity 1 |
| `floor-quotient`, `floor-remainder` | `1+(b(a)+1)*(b(b)+1)` |
| Numeric comparisons | `1+sum(max(b(x_i),b(x_(i+1))))` over all adjacent pairs, regardless of early mismatch |
| `equal?` | `1+S`, regardless of early mismatch |
| Type predicates, `not`, `null?`, `car` | 1 |
| `cdr`, `length`, `string-length`, `substring` | `1+S` |
| `list`, `cons`, `append`, `string-append` | `1+A+S` |

For `+` with one operand the identity case costs 1. For `-` with two or more, the first operand is initial accumulator. For `+` with two or more, the first operand is initial accumulator. Every intermediate integer accumulator obeys `integer_bits`; no reassociation bypasses that cap. Comparisons evaluate and validate every argument even if an earlier adjacent comparison fails.

Allocation counts cumulative logical bytes, not live heap. Charge `size(V)` for every evaluated literal, primitive result (including shared `car` results/booleans), and first materialization of each captured data revision per invocation. No refunds; cached references, lexical lookup, argument forwarding and user returns add zero. Repeated list subvalues count fully regardless of physical sharing.

Before bulk work reserve its fuel and conservative output/workspace bytes from bounded argument metadata, or perform bounded elementary work. Release unused reservation; debit exact logical result bytes. Conservative reservation can fail even when the final value would fit. Arithmetic computes exactly in bounded buffers derived from operand bits, then checks result caps. Cached sizes/depths must be validated by bounded traversal. Hash/serialization and physical process/time/memory watchdogs are separate; logical allocation does not establish peak RAM.

The abstract stack has three frame kinds: `If(yes,no,env)`, `Let(name,body,env)` and `Args(callee,remaining,values,env)`. `if` pushes `If` for its condition, pops it and enters one branch. `let` pushes `Let` for its initializer, pops it and enters its body with the extended environment. Nonempty calls push one `Args`, update it while collecting operands, then pop it before invocation; zero-operand calls push none. User invocation replaces the current environment with parameters and enters the body under the existing continuation; there is no separate return frame. Returning resumes a waiting frame or completes at the empty stack.

`frames_used = stack_length+1` for the current environment; check before pushes, record the maximum. Tail calls replace environments without growing the stack. The fixture separately caps environment bindings, argument count, source/value depth, dependencies, results and physical memory. Saved-environment bytes have no separate meter: their finite bound follows from these caps, bounded frame count and logical allocation. Concrete layout must preserve these abstract receipts; this is not full Scheme conformance or a measured isolation guarantee.

Parsing/resolution/hashing/storage/observation budgets are not fuel. Reserve a failure receipt before admission. Exhaustion publishes no successful result/checkpoint and never saves a mid-VM state. Deployment must supply every cap and visit total; this proposal adopts no numerical quota.

## 8. Concrete intended examples and incremental editing

These examples use valid source under this proposed contract; they are manually reasoned expectations, **not execution results**. Host wrappers are specified in INTERFACE_EVALUATION.md; `define` is the top-level definition action recognized by the host, with Scheme-compatible definition syntax.

```scheme
(define (twice x) (+ x x))
(define (four x) (twice (twice x)))
(run (four 3))
```

Expect 12. Redefining `twice` with `(* x 3)` leaves old `four` unchanged; redefining `four` explicitly adopts the current helper.

```scheme
(define (first xs) (car xs))
(run (first '()))
(define (first xs)
  (if (null? xs) (list "absent") (list "present" (car xs))))
(run (first '()))
(run (first '(7)))
```

Expect `EMPTY_LIST`, then values `("absent")` and `("present" 7)`. Only the selected `if` branch executes. `(if #f (floor-quotient 1 0) 7)` returns 7; `(if 0 7 8)` also returns 7.

```scheme
(define (sum xs)
  (if (null? xs) 0 (+ (car xs) (sum (cdr xs)))))
(run (sum '(2 3 4)))
```

Expect 9. Recursion stays within this revision; this non-tail-recursive example retains pending operand frames.

```scheme
(define (chunk state)
  (let ((remaining (car state)))
    (let ((output (car (cdr state))))
      (if (null? remaining)
          state
          (list (cdr remaining)
                (append output (list (twice (car remaining)))))))))
(put checkpoint '((2 3) ()))
(run (chunk checkpoint))
```

Expect `((3) (4))`. `(run-save checkpoint (chunk checkpoint))` atomically publishes this state; the next run expects `(() (4 6))`. Host envelopes supply snapshot CAS; source supplies no hash token. Keep the procedure revision in checkpoint project metadata/receipts. Old `chunk` pins old `twice`; exhaustion creates no checkpoint.

Small edits use complete short `define` replacements; old revisions remain inspectable. Split large programs into pinned helpers. Store incomplete drafts as ordinary text through `put`. Optional future host `define-from` could compile a bounded text artifact, after separate specification; it is neither guest `eval` nor a base command.
