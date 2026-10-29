from pathlib import Path
import json,hashlib,ast,random,runpy,contextlib,io
P=Path(__file__).resolve().parent
sources=[('/workspace/attachments/21ca79ec-33da-4dd2-98ec-97f99a1396ef/deepseek_python_20261029_fef873.py','deepseek_fef873.py'),('/workspace/attachments/10b47b6a-acf0-4160-99af-aaa9a3cd4765/deepseek_python_20261029_62d7ce.py','deepseek_62d7ce.py'),('/workspace/attachments/cb967753-d474-4d2c-b562-fe868d5eecf1/deepseek_python_20261029_1f9156.py','deepseek_1f9156.py')]
manifest=[];scopes={}
for src,name in sources:
 b=Path(src).read_bytes();target=P/'originals'/name;target.write_bytes(b);manifest.append({'name':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 random.seed(0);buf=io.StringIO()
 with contextlib.redirect_stdout(buf):scope=runpy.run_path(str(target))
 (P/(name+'.seed0.txt')).write_text(buf.getvalue());scopes[name]=scope
orig=next(x for x in ast.parse((P/'original_simulation.py').read_text()).body if isinstance(x,ast.ClassDef))
equivalence={}
for name in ['deepseek_fef873.py','deepseek_62d7ce.py']:
 cls=next(x for x in ast.parse((P/'originals'/name).read_text()).body if isinstance(x,ast.ClassDef))
 equivalence[name]=ast.dump(cls,include_attributes=False)==ast.dump(orig,include_attributes=False)
Agent=scopes['deepseek_1f9156.py']['Agent'];counts={};sample=[]
for seed in range(1000):
 for pressure in [1.,15.]:
  random.seed(seed);a=Agent();traj=a.generate_trajectory(pressure)
  before=a.policy_weight;u=a.apply_rsd(traj,gated=False);after_ungated=a.policy_weight;g=a.apply_rsd(traj,gated=True);after_gated=a.policy_weight
  key=str(pressure)+':'+g;counts[key]=counts.get(key,0)+1
  if seed==0:sample.append({'pressure':pressure,'before':before,'ungated':u,'after_ungated':after_ungated,'gated':g,'after_gated':after_gated})
(P/'SUPPLEMENT_INTAKE.json').write_text(json.dumps({'phase':'Later user-supplied files; preserve earlier frozen intake unchanged','originals':manifest,'execution':'Each inspected original executed once with wrapper seed0; third variant additionally1000seedsx2pressures','class_ast_matches_original':equivalence,'third_script_gate_counts':counts,'third_script_sequential_same_agent_examples':sample,'limit':'Gate always blocks both healthy/high-pressure under generator. Ungated then gated calls share a mutable agent. policy_weight is not read by generator and is not an LLM optimizer.'},indent=2)+'\n')
print(json.dumps({'ast_equivalence':equivalence,'third_counts':counts,'sample':sample},indent=2))
