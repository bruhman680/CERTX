"""Reconstruct the pre-connection host fixture using retained inventory and projections.

This copies data to a fresh destination; it never rewinds the primary.
"""
from pathlib import Path
import hashlib, json, shutil
D=Path(__file__).resolve().parent
G=D.parent/'source-access-three-cycle-v1'
PROJECTIONS={'cycle3/environment/STATE.json':'STATE.json',
 'cycle3/environment/NOTEBOOK.jsonl':'NOTEBOOK.jsonl',
 'cycle3/CURRENT_VERIFY.json':'CURRENT_VERIFY.json',
 'cycle3/environment/PAUSE':'PAUSE'}
def build_baseline(destination):
 destination=Path(destination);destination.mkdir(parents=True,exist_ok=False)
 inventory=json.loads((D/'before/PRIMARY_INVENTORY.json').read_text())
 for name,digest in inventory.items():
  source=D/'before'/PROJECTIONS[name] if name in PROJECTIONS else G/name
  assert hashlib.sha256(source.read_bytes()).hexdigest()==digest,name
  target=destination/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 return destination
