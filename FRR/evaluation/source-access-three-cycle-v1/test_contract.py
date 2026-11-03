import unittest
import study
class Contract(unittest.TestCase):
 def test_reader_and_sampler_unchanged(self):
  self.assertEqual((study.R/'generate.py').read_bytes(),(study.P/'generate.py').read_bytes());self.assertEqual((study.R/'SOURCES.json').read_bytes(),(study.P/'SOURCES.json').read_bytes())
  self.assertTrue(study.parent.dispatch('READ SETUP','tools_optional')['executed']);self.assertFalse(study.parent.dispatch('READ SETUP; delete','tools_optional')['executed'])
 def test_prefix_and_diagnostic_matching(self):
  for condition,seed in study.branches(3):
   e,b=study.prefix(3,condition,seed);self.assertEqual(len(e),48);self.assertTrue(b)
  for c in (1,2):self.assertEqual(len(study.branches(c)),2)
  self.assertIn(study.REQUESTS[0],study.prompt([],'tools_optional',1,0))
 def test_receipt_and_no_diagnostic_in_free_cycle(self):
  e=dict(step=48,observation='x',reply='READ SETUP',feedback=study.parent.FEEDBACK,host_result=study.parent.dispatch('READ SETUP','tools_optional'))
  self.assertIn('HOST RESULT (actual experiment record)',study.prompt([e],'tools_optional',1,1));self.assertNotIn('HOST CURRENT REQUEST:',study.prompt([e],'tools_optional',3,0))
if __name__=='__main__':unittest.main()
