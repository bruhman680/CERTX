"""Lossless smaller JSON representation; keep original output immutable."""
from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent
original=(r/'RAW_COMPACT.json').read_bytes();value=json.loads(original);published=json.dumps(value,separators=(',',':'),allow_nan=False)+'\n';(r/'PUBLICATION_COMPACT.json').write_text(published)
assert json.loads(published)==value
rebuilt=(json.dumps(json.loads(published),indent=2,allow_nan=False)+'\n').encode();assert rebuilt==original
receipt={'published':'PUBLICATION_COMPACT.json','published_bytes':len(published.encode()),'published_sha256':hashlib.sha256(published.encode()).hexdigest(),'local_original':'RAW_COMPACT.json','local_original_bytes':len(original),'local_original_sha256':hashlib.sha256(original).hexdigest(),'all_JSON_values_preserved':True,'original_bytes_reconstruct_exactly_with_Python_indent_2_and_LF':True,'full_observed_A_B_arrays_saved':False}
with (r/'PUBLICATION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(receipt))
