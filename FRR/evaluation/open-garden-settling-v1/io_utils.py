"""File records are independent of the model runtime."""
from pathlib import Path
import hashlib
import json

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def dump_new(p,v):
    with Path(p).open('x') as f:json.dump(v,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')

def append(p,v):
    with Path(p).open('a') as f:f.write(json.dumps(v,sort_keys=True,allow_nan=False)+'\n');f.flush()
