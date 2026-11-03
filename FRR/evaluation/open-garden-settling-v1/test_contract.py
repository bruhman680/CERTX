import unittest,importlib.util,json
from pathlib import Path
import study
class Contract(unittest.TestCase):
 def test_same_model_input_contract(self):
  s=importlib.util.spec_from_file_location('parent',study.P/'study.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
  for key in ('HEADER','OBS','FEEDBACK'):self.assertEqual(getattr(study,key),getattr(m,key))
  e=[dict(step=34,observation='x',reply='<<<\nY\n>>>',feedback=study.FEEDBACK)];self.assertEqual(study.render(e),m.render(e))
 def test_sampler_only_input_limit_changed(self):
  r=Path(__file__).resolve().parent;self.assertEqual((r/'generate.py').read_text().replace('3072','2048'),(study.P/'generate.py').read_text())
 def test_parent_indices_and_capacity(self):
  cps=[json.loads(p.read_text()) for p in (study.P/'run/notebooks').glob('*_CHECKPOINT.json')];self.assertEqual(sorted(c['next_step'] for c in cps),[32,33,35,35]);self.assertGreaterEqual(json.loads((study.BASE/'config.json').read_text())['max_position_embeddings'],3168)
if __name__=='__main__':unittest.main()
