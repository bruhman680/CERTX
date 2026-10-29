"""Supplement: exercise refusal before tensor deserialization, not just hash inequality."""
import json
from pathlib import Path
from backend import sha
from safetensors.torch import load_file
P=Path(__file__).resolve().parent

def bound_load(path,expected_sha):
    if sha(path)!=expected_sha:
        raise ValueError('cache artifact binding mismatch')
    return load_file(str(path))

if __name__=='__main__':
    root=Path('/workspace/cache_backend_artifacts');expected=sha(root/'B1.safetensors')
    original=bound_load(root/'B1.safetensors',expected)
    try:
        bound_load(root/'B1.tampered.safetensors',expected)
        rejected=False
    except ValueError as e:
        rejected=str(e)=='cache artifact binding mismatch'
    assert rejected
    result={'phase':'post-run boundary diagnostic, no additional model inference','original_load_tensor_count':len(original),'tampered_artifact_rejected_before_load':rejected,'scope':'Exact file-byte consistency against saved expected hash, not authenticated original provenance or semantic correctness. Original backend uses its own equivalent pre-load assertion; this supplementary function was not silently substituted into the historical inference.'}
    (P/'ARTIFACT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
