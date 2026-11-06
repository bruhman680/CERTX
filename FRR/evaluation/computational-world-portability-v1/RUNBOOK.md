# Isolated portability prototype

Run from `prototype/` with Python 3 standard library on Linux. Never use the original garden's directory/database. Use a fresh disposable destination; numerical profiles are retained and must match on reopen/import.

```bash
python -m unittest -v test_world test_isolation test_integrity test_portability
python world_cli.py --db /tmp/world-portable.sqlite --source '(put numbers (quote (1 2 3)))'
python world_cli.py --db /tmp/world-portable.sqlite --source '(page numbers value "" 32)'
python bundle_cli.py --db /tmp/world-portable.sqlite --export /tmp/world-portable.json
python bundle_cli.py --db /tmp/world-rebuilt.sqlite --import /tmp/world-portable.json
```

Use the returned `next_cursor` string verbatim in the next page command, with Scheme string escaping. Alias pages use `source` or `value`; immutable artifact IDs can be supplied as strings. Join `chunk` strings in offset order. For `canonical-tagged-json`, JSON-decode the joined text and decode its explicit guest-value tags. Source pages need no further decoding. Cursors become invalid when the guest snapshot changes. Inspection/audit activity alone does not change it.

For a successful pure run whose initial compact value was omitted, use `(page-run "original-request-id" "" 32)`. An execution error or non-COMPUTED receipt has no pure-result value to read. This reads a retained result; it does not run the program again.

Host `World.submit` requires the original request ID/source/expected snapshot for an exact retry. Import preserves those identities. New actions use new request IDs and the imported world's current snapshot. Existing databases/bundles are never overwritten by the transport API. Export is data-only; filenames and SQL are not interpreted from bundle members. Version/profile mismatch fails rather than silently adapting semantics.

The Chibi reference is only for trusted fixed fixtures. It is outside the guest path:

```bash
python verify_host.py --reference /workspace/world_blueprint_reference/chibi-reference
```

This rewrites the local check outputs; use a copy if preserving this published evidence. The earlier reference setup is documented in [the prior build](../computational-world-blueprint-v1/REFERENCE_SETUP.md).

`pilot.py` is a completed 10-call experiment, not a continuation driver. It refuses existing output/world directories. Do not delete its locks/records or rerun it over the saved plan. `verify_pilot.py` checks recorded outputs and independently rebuilt worlds with the cached tokenizer, without loading weights or generating responses. Any new model condition needs its own explicit plan and output directory.
