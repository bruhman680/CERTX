import json,tempfile,unittest
from pathlib import Path
from interface import receive,interpret
class SeparationTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name);self.home=self.root/'world';self.home.mkdir();self.obs=self.root/'observer';self.obs.mkdir()
 def tearDown(self): self.t.cleanup()
 def test_prose_and_commands_remain_thought(self):
  for n,text in enumerate(['perhaps... unfinished','echo wrong > accidental','```python\nprint(42)\n```','{"action":"shell","source":']):
   r=receive(self.home,self.obs,n,text);self.assertEqual(r['kind'],'notebook');self.assertFalse(r['execution_requested']);self.assertEqual(r['visible_feedback'],'')
  self.assertFalse((self.home/'accidental').exists());self.assertIn('unfinished',(self.home/'notebook.txt').read_text())
 def test_explicit_action_changes_world(self):
  text=json.dumps({'action':'shell','source':'echo planted > seed'})
  r=receive(self.home,self.obs,0,text);self.assertEqual(r['kind'],'shell');self.assertEqual((self.home/'seed').read_text(),'planted\n')
 def test_program_error_is_visible(self):
  r=receive(self.home,self.obs,0,json.dumps({'action':'shell','source':'python3 -c "1/0"'}));self.assertIn('ZeroDivisionError',r['visible_feedback'])
 def test_no_hidden_retry(self):
  text=json.dumps({'action':'shell','source':'echo once >> count'});receive(self.home,self.obs,0,text)
  with self.assertRaises(FileExistsError):receive(self.home,self.obs,0,text)
  self.assertEqual((self.home/'count').read_text(),'once\n')
 def test_no_host_write_through_notebook_symlink(self):
  protected=self.root/'protected';protected.write_text('unchanged');(self.home/'notebook.txt').symlink_to(protected)
  receive(self.home,self.obs,0,'thought');self.assertEqual(protected.read_text(),'unchanged')
 def test_notebook_changes_do_not_rewrite_evidence(self):
  receive(self.home,self.obs,0,'old thought')
  receive(self.home,self.obs,1,json.dumps({'action':'shell','source':'rm notebook.txt'}))
  self.assertFalse((self.home/'notebook.txt').exists());self.assertEqual(json.loads((self.obs/'000000_RAW.json').read_text())['text'],'old thought')
 def test_extra_fields_and_other_actions_are_not_dispatched(self):
  for text in ['{"action":"shell","source":"echo x","note":1}','{"action":"other","source":"echo x"}']:
   self.assertIsNone(interpret(text))
if __name__=='__main__':unittest.main(verbosity=2)
