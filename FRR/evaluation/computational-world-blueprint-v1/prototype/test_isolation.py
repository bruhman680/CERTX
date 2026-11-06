import json
from pathlib import Path
import tempfile
import unittest

from world_cli import run_isolated
from world_store import World


class IsolationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cw-isolation-test-')
        self.db = str(Path(self.temp.name) / 'world.sqlite')
        self.profile = json.loads((Path(__file__).resolve().parents[1] / 'constants.json').read_text())
        world = World(self.db, self.profile)
        self.initial = world.snapshot()['id']
        world.close()

    def tearDown(self):
        self.temp.cleanup()

    def test_worker_commits_and_retry_is_exact(self):
        source = '(run-save result (+ 2 3))'
        first = run_isolated(self.db, self.profile, 'process-1', self.initial, source)
        self.assertEqual(first['status'], 'PUBLISHED')
        self.assertEqual(first['value'], 5)
        again = run_isolated(self.db, self.profile, 'process-1', self.initial, source)
        self.assertEqual(first, again)

    def test_watchdog_never_fabricates_success_or_retries(self):
        outcome = run_isolated(self.db, self.profile, 'killed-1', self.initial,
                               '(run-save result (+ 2 3))', timeout=0)
        self.assertTrue(outcome.get('controller', {}).get('watchdog'))
        self.assertNotEqual(outcome['status'], 'PUBLISHED')
        world = World(self.db, self.profile)
        try:
            self.assertEqual(world.snapshot()['id'], self.initial)
            self.assertNotIn('result', world.snapshot()['aliases'])
        finally:
            world.close()

    def test_oversize_not_admitted(self):
        result = run_isolated(self.db, self.profile, 'too-large', self.initial,
                              'x' * (self.profile['max_source_bytes'] + 1))
        self.assertEqual(result['status'], 'NOT_ADMITTED')
        self.assertEqual(result['error']['code'], 'SUBMISSION_BYTES')

    def test_surrogate_rejected_before_worker(self):
        result = run_isolated(self.db, self.profile, 'bad-unicode', self.initial, '\ud800')
        self.assertEqual(result['status'], 'NOT_ADMITTED')
        self.assertEqual(result['error']['code'], 'SYNTAX')

    def test_killed_conflicting_retry_never_returns_old_success(self):
        first = run_isolated(self.db, self.profile, 'same-id', self.initial, '(run 7)')
        self.assertEqual(first['value'], 7)
        other = run_isolated(self.db, self.profile, 'same-id', self.initial, '(run 8)', timeout=0)
        self.assertEqual(other['status'], 'REQUEST_ID_CONFLICT')
        self.assertIsNone(other['value'])

    def test_compact_view_marks_omission(self):
        from world_cli import compact_observation
        receipt = {'status': 'COMPUTED', 'value': 'x' * 8000,
                   'error': None, 'world_snapshot': self.initial}
        view = compact_observation(receipt, self.profile)
        self.assertTrue(view['truncated'])
        self.assertIsNone(view['value'])
        self.assertLessEqual(len(json.dumps(view).encode()), self.profile['max_observation_bytes'])


if __name__ == '__main__':
    unittest.main()
