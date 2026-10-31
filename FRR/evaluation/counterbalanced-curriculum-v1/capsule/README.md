# Local adapter capsule

Standard-library utility for a small, portable, deterministic tar.gz of two fixed adapter branches. It performs no model inference, tensor framework import, optimizer unpickling, network operation, deletion or source edit. Build only after the candidate exists and is complete.

```python
from capsule import build_adapter_capsule, verify_adapter_capsule
receipt = build_adapter_capsule(control_training_manifest, candidate_training_manifest, new_output_tar_gz)
verified = verify_adapter_capsule(new_output_tar_gz)
```

```sh
python /workspace/capsule_builder/capsule.py build CONTROL_TRAINING_MANIFEST CANDIDATE_TRAINING_MANIFEST NEW_OUTPUT.tar.gz
python /workspace/capsule_builder/capsule.py verify NEW_OUTPUT.tar.gz
cd /workspace/capsule_builder
python -m unittest -v test_capsule.py
```

Each source manifest uses the current runtime schema: `base_pin`, `checkpoint`, `checkpoint_files_sha256`, `initial_files_sha256`, `optimizer`, `optimizer_sha256`. The initial directory is `initial_adapter` beside its TRAINING_MANIFEST; final directory and optimizer file follow their manifest paths. Relative paths resolve from the training manifest's directory. No directory globbing includes arbitrary extra files. Both branches must declare identical base pins. Existing destinations, including symlinks, are refused; output parent must already exist. Validation occurs before exclusive output creation. A filesystem/write failure can leave a new partial output; it is deliberately not deleted or overwritten. Choose another new path after diagnosing it.

Exactly 13 regular members are allowed: CAPSULE.json and six per fixed `control`/`candidate` role: original TRAINING_MANIFEST.json; initial and final adapter.safetensors plus manifest.json; opaque optimizer_state.pt. Fixed safe member names, lexical ordering, uid/gid defaults, mode 0600 and zero timestamps yield deterministic archive bytes for identical source bytes. Capsule metadata includes declared base pin, member sizes/SHA256, exclusions and limitations. Source manifest absolute paths remain historical text; portable member lookup uses role/phase paths in the capsule, not those source paths.

Before packaging, source bytes must match training-declared hashes. Adapter bytes must also match each adapter manifest's declared hash, tensor names, dtype and shapes. F32 safetensors header sizes, exact byte coverage, offsets/nonoverlap and every value's finiteness are checked without loading a model. Other dtypes are intentionally rejected. Bounds: 32 MiB per file, 128 MiB summed payload, 1 MiB safetensors header. This targets the current ~1 MiB F32 adapters, not arbitrary model archives. Independent archive verification rejects unsafe/duplicate/nonregular members, validates all member hashes and the original training hashes again, and reruns adapter checks. Build verifies its in-memory archive before writing and rereads the new file afterward. Optimizer bytes are hash-checked only, never unpickled; optimizer numerical validity and resumability are untested.

**A local capsule is not an independent backup until copied off the workspace.** It explicitly excludes dense base weights, the old ~1.6 GB full-weight checkpoint, terminal KV caches and all other experimental history, code, data and logs. Those originals must remain preserved separately. Restoring needs the exact original dense base identified by model ID/revision/weight SHA256 and a compatible adapter/optimizer runtime. The capsule does not validate actual base availability, model behavior, source authority or experiment success, and it does not contain a self-sufficient runnable environment. Member hashes detect accidental changes relative to a trusted capsule; an attacker who can rewrite the complete capsule and its index can rewrite those hashes. No upload, paid storage or independent copy is performed.
