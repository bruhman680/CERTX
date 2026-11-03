import unittest,importlib.util,json
from pathlib import Path
import study
class Contract(unittest.TestCase):
 def test_same_rendering_and_sampler(self):
  spec=importlib.util.spec_from_file_location('parent',study.P/'study.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  e=[dict(step=37,observation='x',reply='<<< y >>>',feedback=study.FEEDBACK)];self.assertEqual(study.render(e),m.render(e))
  r=Path(__file__).resolve().parent;self.assertEqual((r/'generate.py').read_bytes(),(study.P/'generate.py').read_bytes())
 def test_resume_points(self):
  cps=[json.loads(p.read_text()) for p in (study.P/'run/notebooks').glob('*_CHECKPOINT.json')];self.assertEqual(sorted(x['next_step'] for x in cps),[35,36,38,38])
if __name__=='__main__':unittest.main()
