import tempfile, unittest
from pathlib import Path
from workspace import execute, snapshot, MAX_OUTPUT

class BoundaryTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.home=Path(self.t.name)/'home';self.home.mkdir()
 def tearDown(self): self.t.cleanup()
 def test_persistence_and_computation(self):
  r=execute(self.home,"python3 -c \"open('n','w').write(str(6*7))\"")
  self.assertEqual(r['exit_code'],0);self.assertEqual(execute(self.home,'cat n')['stdout'],'42')
 def test_errors_are_returned_without_rollback(self):
  r=execute(self.home,'echo kept > note; python3 -c "1/0"')
  self.assertNotEqual(r['exit_code'],0);self.assertIn('ZeroDivisionError',r['stderr']);self.assertTrue((self.home/'note').exists())
 def test_host_and_observer_inaccessible(self):
  secret=Path(self.t.name)/'observer';secret.write_text('external')
  r=execute(self.home,f'cat {secret}')
  self.assertNotEqual(r['exit_code'],0);self.assertEqual(secret.read_text(),'external')
  self.assertNotEqual(execute(self.home,'cat /workspace/frr/CURRENT_HANDOFF.md')['exit_code'],0)
 def test_symlink_cannot_escape(self):
  r=execute(self.home,'ln -s /workspace/frr/CURRENT_HANDOFF.md link; cat link')
  self.assertNotEqual(r['exit_code'],0);self.assertIn(['link','symlink','/workspace/frr/CURRENT_HANDOFF.md'],snapshot(self.home))
 def test_network_isolated(self):
  r=execute(self.home,"python3 -c \"import socket; s=socket.socket(); s.settimeout(.2); s.connect(('1.1.1.1',443))\"")
  self.assertNotEqual(r['exit_code'],0)
 def test_time_and_background_processes(self):
  r=execute(self.home,'sleep 10; echo late > late')
  self.assertEqual(r['boundary'],'wall_time');self.assertFalse((self.home/'late').exists())
  execute(self.home,'(sleep 1; echo escaped > escaped) &')
  import time;time.sleep(1.2);self.assertFalse((self.home/'escaped').exists())
 def test_output_bound(self):
  r=execute(self.home,'yes abc')
  self.assertEqual(r['boundary'],'output_limit');self.assertLessEqual(len(r['stdout'].encode())+len(r['stderr'].encode()),MAX_OUTPUT)
 def test_file_bound(self):
  r=execute(self.home,'head -c 1048576 /dev/zero > big')
  self.assertLessEqual((self.home/'big').stat().st_size,262144);self.assertNotEqual(r['exit_code'],0)
 def test_no_fence_repair(self):
  r=execute(self.home,'```python\nprint(42)\n```')
  self.assertNotEqual(r['exit_code'],0)

if __name__=='__main__': unittest.main(verbosity=2)
