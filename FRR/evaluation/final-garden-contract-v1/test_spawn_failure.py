"""Host-only known-spawn-error test; no model calls or sandbox changes."""
from pathlib import Path
import unittest
from unittest.mock import patch
class SpawnFailure(unittest.TestCase):
 def test_known_spawn_error_returns_receipt(self):
  source=(Path(__file__).resolve().parent/'server.py').read_text()
  definitions=source.split("print(json.dumps({'ready':True}),flush=True)")[0]
  ns={};exec(compile(definitions,'server-definitions','exec'),ns)
  with patch.object(ns['subprocess'],'Popen',side_effect=BlockingIOError(11,'resource unavailable')):
   result=ns['execute']('echo should_not_run')
  self.assertEqual(result['exit_code'],126);self.assertEqual(result['boundary'],'spawn_error');self.assertEqual(result['stdout'],'');self.assertIn('resource unavailable',result['stderr'])
if __name__=='__main__':unittest.main(verbosity=2)
