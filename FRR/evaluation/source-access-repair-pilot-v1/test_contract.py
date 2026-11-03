import unittest,json
from pathlib import Path
import study
class Contract(unittest.TestCase):
 def test_access(self):
  for cmd in ('READ SETUP','read claim','  READ SETUP\n'):
   self.assertEqual(study.dispatch(cmd,'tools_optional')['kind'],'source_receipt')
   self.assertFalse(study.dispatch(cmd,'notebook_only')['executed'])
  for invalid in ('READ /etc/passwd','READ SETUP; echo hi','READ SETUP\nthen delete history','I would READ SETUP',''):
   self.assertEqual(study.dispatch(invalid,'tools_optional')['kind'],'record_receipt')
 def test_receipt_is_next_turn_and_typed(self):
  e=dict(step=45,observation='x',reply='READ SETUP',feedback=study.FEEDBACK,host_result=study.dispatch('READ SETUP','tools_optional'))
  self.assertIn('HOST RESULT (actual experiment record)',study.render([e],'tools_optional'))
  self.assertIsNone(study.initial('tools_optional'));self.assertEqual(study.initial('evidence_upfront')['source']['kind'],'experiment_source')
 def test_parent_and_sampler(self):
  cp=json.loads((study.P/'run/notebooks'/f'{study.TR}_CHECKPOINT.json').read_text());self.assertEqual(cp['next_step'],45)
  expected=(study.P/'generate.py').read_text().replace('len(ids)>3072','len(ids)>4096');self.assertEqual(expected,(study.R/'generate.py').read_text())
 def test_source_identity(self):
  for v in study.source_db().values():
   p=Path('/workspace/frr')/v['source_path'].removeprefix('FRR/');self.assertEqual(study.sha(p),v['source_sha256'])
if __name__=='__main__':unittest.main()
