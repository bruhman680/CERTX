import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys

from world_store import World, StoreError


class IntegrityChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cw-integrity-test-')
        self.db = str(Path(self.temp.name) / 'world.sqlite')
        self.profile = json.loads((Path(__file__).resolve().parents[1] / 'constants.json').read_text())
        self.world = World(self.db, self.profile)

    def tearDown(self):
        self.world.close()
        self.temp.cleanup()

    def test_second_owner_cannot_recover_live_world(self):
        before = self.world.snapshot()
        with self.assertRaises(StoreError) as caught:
            World(self.db, self.profile)
        self.assertEqual(caught.exception.code, 'WORLD_BUSY')
        self.assertEqual(self.world.snapshot(), before)

    def test_corrupt_artifact_detected_not_reinterpreted(self):
        receipt = self.world.submit('put', self.world.snapshot()['id'], '(put x 2)')
        self.assertEqual(receipt['status'], 'PUBLISHED')
        row = self.world.db.execute('SELECT id,record FROM artifacts').fetchone()
        changed = json.loads(row['record'])
        changed['payload'] = ['int', '3']
        self.world.db.execute('UPDATE artifacts SET record=? WHERE id=?',
                              (json.dumps(changed), row['id']))
        with self.assertRaises(StoreError):
            self.world.verify_integrity()

    def test_closed_world_passes_integrity_after_reload(self):
        self.world.submit('define', self.world.snapshot()['id'], '(define (f x) (+ x 1))')
        self.world.submit('run', self.world.snapshot()['id'], '(run-save y (f 2))')
        before = self.world.snapshot()
        self.world.close()
        self.world = World(self.db, self.profile)
        self.assertEqual(self.world.snapshot(), before)
        self.world.verify_integrity()

    def test_hard_exit_after_admission_recovers_without_running_again(self):
        before = self.world.snapshot()['id']
        self.world.close()
        script = '''
import json, os, sys
from world_store import World
import scheme_core
world = World(sys.argv[1], json.loads(sys.argv[2]))
scheme_core.evaluate = lambda *args, **kwargs: os._exit(70)
world.submit('interrupted', sys.argv[3], '(run-save result (+ 2 3))')
'''
        child = subprocess.run([sys.executable, '-c', script, self.db,
                                json.dumps(self.profile), before],
                               cwd=str(Path(__file__).resolve().parent),
                               capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 70, child.stderr.decode())
        self.world = World(self.db, self.profile)
        self.assertEqual(self.world.snapshot()['id'], before)
        self.assertNotIn('result', self.world.snapshot()['aliases'])
        result = self.world.submit('interrupted', before, '(run-save result (+ 2 3))')
        self.assertEqual(result['status'], 'FAILED_HOST_ABORT')
        self.assertEqual(result['error']['code'], 'HOST_RESTART')
        self.assertIsNone(result['event']['usage']['eval_fuel'])
        self.assertFalse(result['event']['usage']['interrupted_counters_available'])
        self.assertEqual(int(result['event']['usage']['quota_fuel_charged']), self.profile['eval_fuel'])
        self.world.verify_integrity()


if __name__ == '__main__':
    unittest.main()
