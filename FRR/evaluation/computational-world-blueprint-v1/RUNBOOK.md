# Reproduce the isolated host prototype

Python 3 standard library and POSIX/Linux process limits are used. No model or inference API is required. Use a fresh disposable database; never point this prototype at the original garden or any existing research database. Prototype worlds pin their fixture profile, so changing `constants.json` requires a new isolated world.

From this study's `prototype/` directory:

```bash
python -m unittest -v test_world test_isolation test_integrity
python world_cli.py --db /tmp/my-isolated-world.sqlite --source '(define (twice x) (+ x x))'
python world_cli.py --db /tmp/my-isolated-world.sqlite --source '(run-save answer (twice 3))'
python world_cli.py --db /tmp/my-isolated-world.sqlite --source '(inspect answer)'
```

The CLI generates request IDs and captures the current expected snapshot unless explicit flags are supplied. Exact retry requires the **same request ID, source and original expected snapshot**, using `--request-id` and `--expected`. Do not retry an uncertain commit as a new action. The SQLite database and sidecar files are the prototype's durable state; `drop` removes an alias, not the retained history. Close the world before copying files, or use SQLite's proper backup facilities; portable application-level export is not yet implemented.

`World` is the in-process host API for trusted tests. Route later untrusted guest interactions through the process-bounded CLI/controller. The CLI's compact output may omit large values and marks that omission; full receipts remain host audit material. Complete guest retrieval of large results is unfinished.

To rerun the stored host validation including the independent reference:

```bash
python verify_host.py --reference /workspace/world_blueprint_reference/chibi-reference
```

That reference path belongs to this workspace. On a different machine use the pinned official Chibi source and the documented private-prefix setup in [REFERENCE_SETUP.md](REFERENCE_SETUP.md), then pass the resulting executable. Only the fixed trusted fixtures in `check_reference.py` may be sent to it. It is not a guest execution backend. The source/binary and build dependencies are not vendored in this study.

`verify_host.py` writes final check JSON/log files and uses temporary isolated worlds. `run_demo.py` runs the explicitly host-authored 19-action walkthrough. Neither invokes a model, changes model weights, or resumes the continuing garden.
