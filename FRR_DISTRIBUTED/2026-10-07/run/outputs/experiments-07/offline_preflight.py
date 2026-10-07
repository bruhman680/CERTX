"""No-network dependency preflight; does not execute the recovered probe."""
import importlib.util
import json
from pathlib import Path
import sys

result = {
    'python': sys.version.split()[0],
    'dependencies': {name: importlib.util.find_spec(name) is not None for name in ('torch', 'transformers')},
    'cache_roots': {},
    'model_execution': 'not_attempted',
    'network_requests': 0,
}
for root in (Path.home() / '.cache/huggingface', Path('/workspace/.cache/huggingface'), Path('/root/.cache/huggingface')):
    try:
        result['cache_roots'][str(root)] = root.is_dir()
    except PermissionError:
        result['cache_roots'][str(root)] = 'permission_denied_uninspected'
result['status'] = 'blocked_missing_dependencies' if not all(result['dependencies'].values()) else 'requires_explicit_local_model_path'
print(json.dumps(result, indent=2))
