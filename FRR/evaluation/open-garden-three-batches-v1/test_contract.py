import unittest,importlib.util
from pathlib import Path
import study
class Contract(unittest.TestCase):
 def test_interface_identity(self):
  p=Path(__file__).resolve().parent.parent/'open-notebook-continuation-v1/study.py';s=importlib.util.spec_from_file_location('parent_study',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
  for name in ('HEADER','OBS','FEEDBACK'):self.assertEqual(getattr(study,name),getattr(m,name))
  events=[dict(step=14,observation='old',reply='<<<\nYES\n>>>',feedback=study.FEEDBACK)]
  self.assertEqual(study.render(events),m.render(events))
 def test_parent_checkpoints(self):
  import json
  ps=list((study.P/'run/notebooks').glob('*_CHECKPOINT.json'));self.assertEqual(len(ps),4)
  for p in ps:
   c=json.loads(p.read_text());self.assertEqual(c['next_step'],15);self.assertEqual(len(c['events']),15)
 def test_batch_boundaries(self):
  self.assertEqual([n for n in range(16,31) if n%5==0],[20,25,30])
if __name__=='__main__':unittest.main()
