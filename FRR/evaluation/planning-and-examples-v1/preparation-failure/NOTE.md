# Interpreter preparation failure, before any model forward

The first shell command used system `python prepare.py`. Its import of runtime_reference failed with ModuleNotFoundError: torch. Six focused tests had run with the correct venv interpreter. The subsequent newline-separated run command still attempted to start, then failed at missing FREEZE.json, before output-root creation/model load. Original run stdout/stderr are retained here.

Correction: invoke preparation with /workspace/cache_backend_venv/bin/python, then create the prior-file snapshot and execute the unchanged frozen implementation. No model-forward/result-based retry, install, package change or weight mutation occurred. This corrects the command interpreter, not the scientific protocol.
