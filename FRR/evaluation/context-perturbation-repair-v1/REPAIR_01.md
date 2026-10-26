# Repair01: original source array hash encoding and thread environment

Attempt01 failed in source array verification before any probe construction, SVD, calibration or task scoring. File hashes passed. The checker incorrectly compared a raw-byte local digest with the original source manifests' dtype+shape+bytes digest. The source data did not change. I wrote that incompatible checker and corrected it here.

Preserved artifacts: experiment_PRE_REPAIR_01.py and SCHEMA_PRE_REPAIR_01.md, plus root-preserved experiment_FAILED_01.py, SCHEMA_FAILED_01.md, attempt-01/ and frozen-attempt-01/. No attempt was overwritten.

Changes are restricted to source digest encoding, explicit metadata labels, and pre-NumPy single-thread environment setup. source_meta hashes str(dtype), str(shape tuple), then contiguous C bytes using UTF8 encodings for the strings; check now compares this against original manifests. Local raw-byte hashes and content-addressed outcome pool hashes are unchanged and explicitly named in INPUT_MANIFEST.hash_schemes/SCHEMA. Provenance full_array stores the original hash encoding; full_array_local_rawbytes retains local comparison metadata. Six thread environment variables are forced to1 before NumPy import.

No grid, seeds, source arrays, probes, rank thresholds, targets, calibration, retrieval, decoding, metrics or numerical method changed. No experimental main or source fit run by engineer. Syntax py_compile and an independent constant2x2array fixture verified original/local digest distinction and thread environment. Root owns any repaired execution after reviewer approval.

Executable SHA256: d44df90c3b0adb95b6cf3adb423dc42d578b391f287b04a2f452f4bf019c3b90

Exact executable diff:

```diff
--- experiment_PRE_REPAIR_01.py
+++ experiment.py
@@ -7,6 +7,10 @@
 from pathlib import Path
 import shutil
 import time
+# Set before NumPy imports/initializes any BLAS runtime.
+for _thread_variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
+                         'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
+    os.environ[_thread_variable] = '1'
 import numpy as np
 
 HERE = Path(__file__).resolve().parent
@@ -42,8 +46,17 @@
     path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')
 
 
+def source_meta(a):
+    # Original SA/PC manifests bind dtype and shape before contiguous bytes.
+    h = hashlib.sha256()
+    h.update(str(a.dtype).encode())
+    h.update(str(a.shape).encode())
+    h.update(np.ascontiguousarray(a).tobytes())
+    return {'dtype': str(a.dtype), 'shape': list(a.shape), 'sha256': h.hexdigest()}
+
+
 def check(a, expected):
-    assert meta(a) == expected, ('array source mismatch', meta(a), expected)
+    assert source_meta(a) == expected, ('array source mismatch', source_meta(a), expected)
 
 
 class Pool:
@@ -198,10 +211,13 @@
                     a = archive[k]
                     check(a, pm['training_arrays'][k])
                     selected[k] = a[:48].copy()
-                    provenance[k] = {'full_array': meta(a), 'slice': '[0:48, ...]', 'selected': meta(selected[k])}
+                    provenance[k] = {'full_array': source_meta(a), 'full_array_local_rawbytes': meta(a), 'slice': '[0:48, ...]', 'selected': meta(selected[k])}
     np.savez_compressed(out/'selected_training.npz', **selected)
     dump(out/'INPUT_MANIFEST.json', {'source_commits': {'SA': '8560969b84f0eed0c4b81f1fbc87febe959aa3ac',
         'PC': 'cc413eca895131bfe81c3fc6f38dc81f21a26143'},
+        'hash_schemes': {'source_array': 'SHA256(str(dtype) UTF8 + str(shape tuple) UTF8 + contiguous C bytes)',
+                        'local_array': 'SHA256(contiguous C bytes)',
+                        'outcome_pool': 'SHA256(dtype.str UTF8 + JSON shape UTF8 + contiguous C bytes)'},
         'source_file_sha256': sha(out/'source_inputs.npz'), 'training_full_file_sha256': pm['training_file_sha256'],
         'selected_file_sha256': sha(out/'selected_training.npz'), 'selected_arrays': provenance,
         'source_arrays': {k: meta(a) for k, a in inputs.items()}, 'time_unix': time.time()})
```
