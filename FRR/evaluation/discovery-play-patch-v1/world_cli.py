"""Host-only prototype CLI. Never points at the current primary environment by default."""
import argparse,json
from dataclasses import asdict
from pathlib import Path
from world import Rules,view
from journal import Journal
p=argparse.ArgumentParser();p.add_argument('command',choices=('init','step','inspect','verify','recover'));p.add_argument('--directory',required=True);p.add_argument('--reply');a=p.parse_args();path=Path(a.directory).resolve();primary=Path('/workspace/frr/evaluation/source-access-three-cycle-v1/cycle3/environment').resolve()
if path==primary or primary in path.parents:raise SystemExit('Host prototype cannot write into the continuous primary')
if a.command=='init':j=Journal.create(path);print(json.dumps(dict(status='created_host_world',state=j.replay()[0])))
else:
 j=Journal(path)
 if a.command=='step':
  if a.reply is None:raise SystemExit('--reply required')
  print(json.dumps(j.apply(a.reply)))
 elif a.command=='recover':print(json.dumps(j.recover()))
 elif a.command=='inspect':print(view(j.replay()[0]['number'],j.rules()))
 else:print(json.dumps(dict(status='pass',state=j.replay()[0],scope='Host journal check, not model behavior')))
