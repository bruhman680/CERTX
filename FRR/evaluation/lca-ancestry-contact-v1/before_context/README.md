# Optional declared ancestry contact

The existing six-station registry stays unchanged. This separate read-only tool answers: within an explicitly supplied partial DAG, which nodes are common ancestors with no lower common ancestor? It returns every such node, including several incomparable results. Empty results are valid and do not establish independence.

From the repository root:

```sh
python tools/evidence_ancestry.py evaluation/lca-ancestry-contact-v1/manifest.json --root .
python evaluation/lca-ancestry-contact-v1/test_ancestry.py
```

Successful queries print JSON with status computed and exit 0. Rejected input prints status rejected and exits 1. Output goes to stdout; the tool itself does not write registry state or artifacts. `--root` is the boundary for byte-bound artifact paths. An artifact is optional; supplied path and lowercase SHA256 must match local bytes. Manifest and artifact limits are one MiB each, with at most 256 declared nodes.

The exact manifest schema is illustrated in manifest.json: graph_id and edge_semantics describe caller scope, nodes contain unique id and parents (child→parent), and query contains one or more existing node IDs. Each node can additionally carry artifact {path, sha256}. Ancestor includes self. Parent lists and query IDs cannot repeat. Cycles anywhere, unknown nodes, extra fields, duplicate JSON keys, bad hashes and unsafe paths reject. Node IDs are identities; equal hashes do not merge nodes automatically.

RESULT.json is the frozen contact: the original/adapted test DERIVATION records each literally declare the same raw/key parents. Both shared parent artifacts are returned. These are four caller-declared nodes and four edges, not the complete station, source, model or experiment history. PROTOCOL.md gives exact semantics and acceptance criteria; RESEARCH_SCOUT.md links primary sources; REPORT.md states results and limits. FREEZE.json was written before tests and query. CHECKS.json verifies it after contact.
