"""Run an unchanged archived script with one explicit source-path remap."""
from pathlib import Path
import builtins,os,runpy,sys,hashlib,json
P=Path(__file__).resolve().parent;originals=P/'originals'
OLD='/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad/soil_relay/soil_toy.py'
allowed={'soil_dispersion_diag.py','soil_iidwin_floor_check.py'}
if sys.argv[1] not in allowed:raise ValueError('Only two inspected original scripts are authorized here.')
for row in json.loads((P/'SOURCE_MANIFEST.json').read_text())['files']:
 assert hashlib.sha256((originals/row['name']).read_bytes()).hexdigest()==row['sha256'],row['name']
real_open=builtins.open
def remap(file,*a,**kw):
 target=str(file)
 if target==OLD:
  if a and any(x in a[0] for x in 'wax+'):raise ValueError('No writes to source')
  file=originals/'soil_toy.py'
 return real_open(file,*a,**kw)
os.chdir(originals);builtins.open=remap
try:runpy.run_path(str(originals/sys.argv[1]),run_name='__main__')
finally:builtins.open=real_open
