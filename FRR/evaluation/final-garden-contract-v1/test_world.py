from pathlib import Path
import tempfile,json,unittest,time
from world import World,receive,action
class Tests(unittest.TestCase):
 def setUp(self):self.t=tempfile.TemporaryDirectory();self.w=World()
 def tearDown(self):self.w.close();self.t.cleanup()
 def test_notebook_idle_and_unfinished(self):
  for text in ['', 'perhaps...', 'echo a > wrong','```sh\necho b\n```','{"action":"shell",']:
   r=receive(self.w,text);self.assertEqual(r['kind'],'notebook');self.assertIsNone(r['feedback'])
  self.assertFalse((self.w.home/'wrong').exists())
 def test_action_and_error(self):
  r=receive(self.w,json.dumps({'action':'shell','source':'python3 -c "print(6*7)"'}));self.assertEqual(r['feedback']['stdout'],'42\n')
  r=receive(self.w,json.dumps({'action':'shell','source':'python3 -c "1/0"'}));self.assertIn('ZeroDivisionError',r['feedback']['stderr'])
 def test_world_quota(self):
  r=self.w.execute('i=0; while [ $i -lt 40 ]; do head -c 262144 /dev/zero > f$i || break; i=$((i+1)); done; df -k /world')
  size=sum(p.stat().st_size for p in self.w.home.iterdir());self.assertLessEqual(size,8388608);self.assertIn('No space left',r['stderr'])
 def test_isolation(self):
  self.assertNotEqual(self.w.execute('cat /workspace/frr/CURRENT_HANDOFF.md')['exit_code'],0)
  self.assertNotEqual(self.w.execute('python3 -c "import socket; socket.create_connection((\'1.1.1.1\',443),.1)"')['exit_code'],0)
 def test_symlink_notebook(self):
  victim=Path(self.t.name)/'victim';victim.write_text('safe');(self.w.home/'notebook.txt').symlink_to(victim)
  r=receive(self.w,'text');self.assertIsNotNone(r['feedback']);self.assertEqual(victim.read_text(),'safe')
 def test_timeout_notebook_is_visible(self):
  self.w.execute('mkfifo notebook.txt');r=receive(self.w,'waiting')
  self.assertEqual(r['feedback']['boundary'],'wall_time')
 def test_output_and_time(self):
  self.assertEqual(self.w.execute('yes hello')['boundary'],'output_limit')
  self.assertEqual(self.w.execute('sleep 10')['boundary'],'wall_time')
 def test_process_identity_and_limits(self):
  r=self.w.execute('id -u; python3 -c "import resource;print(resource.getrlimit(resource.RLIMIT_NPROC));print(resource.getrlimit(resource.RLIMIT_AS))"')
  self.assertEqual(r['exit_code'],0);self.assertTrue(r['stdout'].startswith('1000\n'));self.assertIn('(128, 128)',r['stdout']);self.assertIn('(33554432, 33554432)',r['stdout'])
 def test_memory_limit(self):
  r=self.w.execute('python3 -c "x=bytearray(100000000)"');self.assertNotEqual(r['exit_code'],0);self.assertIn('MemoryError',r['stderr'])
 def test_file_size(self):
  self.w.execute('head -c 1000000 /dev/zero > file');self.assertLessEqual((self.w.home/'file').stat().st_size,262144)
 def test_background_dies(self):
  self.w.execute('(sleep 1; echo bad > late) >/dev/null 2>&1 &');time.sleep(1.1);self.assertFalse((self.w.home/'late').exists())
 def test_restart_portability_and_symlinks(self):
  self.w.execute('mkdir data; echo remember > data/n; ln -s data/n link')
  objects=Path(self.t.name)/'objects';b=self.w.capture(objects);self.w.close();self.w=World();self.w.restore(b,objects)
  self.assertEqual(self.w.capture(objects),b);self.assertEqual(self.w.execute('cat link')['stdout'],'remember\n')
 def test_restore_traversal_rejected(self):
  from world import sha,stable
  rows=[['../outside','directory',448]]
  with self.assertRaises(AssertionError):self.w.restore({'id':sha(stable({'entries':rows,'root_mode':448})),'entries':rows,'root_mode':448},Path(self.t.name))
 def test_root_and_device_readonly(self):
  self.assertNotEqual(self.w.execute('touch /outside')['exit_code'],0)
  self.assertNotEqual(self.w.execute('touch /dev/outside')['exit_code'],0)
 def test_temporary_storage_clears(self):
  self.assertEqual(self.w.execute('echo temporary > /tmp/x')['exit_code'],0)
  self.assertNotEqual(self.w.execute('cat /tmp/x')['exit_code'],0)
 def test_no_nested_user_namespace(self):
  self.assertNotEqual(self.w.execute('bwrap --unshare-user --ro-bind / / /bin/true')['exit_code'],0)
 def test_notebook_ignores_python_hooks(self):
  version=self.w.execute("python3 -I -S -c 'import sys;print(str(sys.version_info.major)+\".\"+str(sys.version_info.minor))'")
  self.assertEqual(version['exit_code'],0)
  site=self.w.home/'.local/lib'/('python'+version['stdout'].strip())/'site-packages';site.mkdir(parents=True)
  (site/'hook.pth').write_text("import pathlib;pathlib.Path('/world/spied').touch()\n")
  self.assertEqual(self.w.execute('python3 -c pass')['exit_code'],0)
  self.assertTrue((self.w.home/'spied').exists());(self.w.home/'spied').unlink()
  r=receive(self.w,'only writing');self.assertIsNone(r['feedback']);self.assertFalse((self.w.home/'spied').exists())
 def test_fifo_and_hardlink_checkpoint(self):
  self.w.execute('echo data > a; ln a b; mkfifo pipe; chmod 666 pipe')
  objects=Path(self.t.name)/'objects';bundle=self.w.capture(objects);self.w.close();self.w=World();self.w.restore(bundle,objects)
  self.assertEqual(self.w.capture(objects),bundle);self.assertEqual((self.w.home/'a').stat().st_ino,(self.w.home/'b').stat().st_ino)
if __name__=='__main__':unittest.main(verbosity=2)

