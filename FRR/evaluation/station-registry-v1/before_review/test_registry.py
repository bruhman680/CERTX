"""Adversarial scope, binding and strict parsing checks; no model calls."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import station_registry as registry


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.receipt = json.loads((ROOT / 'evaluation/narrow-training-pilot-v1/original_test/RECEIPT.json').read_text())
        self.entry = {'station_id': 'original', 'question': 'Positive recorded count?',
                      'recipe': 'Exact labels, eight generated tokens.', 'state': 'Original; no update.',
                      'receipt': self.bind('receipt.json', self.receipt), 'ancestry': []}
        self.manifest = {'registry_id': 'test', 'stations': [self.entry]}

    def tearDown(self):
        self.temp.cleanup()

    def bind(self, path, value):
        data = json.dumps(value).encode()
        (self.root / path).write_bytes(data)
        return {'path': path, 'sha256': hashlib.sha256(data).hexdigest()}

    def result(self):
        return registry.build(self.manifest, self.root)

    def test_full_denominator_and_preservation(self):
        out = self.result()
        self.assertEqual(out['status'], 'indexed')
        station = out['stations'][0]
        self.assertEqual(station['reported_receipt'], self.receipt)
        self.assertEqual(station['scoped_summary']['summary']['calls'], 48)
        self.assertEqual(station['scoped_summary']['unresolved_outputs'], 36)
        self.assertEqual(station['state'], self.entry['state'])

    def test_changed_receipt_bytes_withholds(self):
        (self.root / 'receipt.json').write_text('{}')
        station = self.result()['stations'][0]
        self.assertEqual(station['status'], 'unresolved')
        self.assertNotIn('scoped_summary', station)

    def test_duplicate_json_and_nan_rejected(self):
        for data in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}'):
            (self.root / 'receipt.json').write_bytes(data)
            self.entry['receipt']['sha256'] = registry.sha(data)
            self.assertEqual(self.result()['stations'][0]['status'], 'unresolved')

    def test_unknown_ruleset_or_extra_claim_not_projected(self):
        for key, value in (('ruleset', 'future-9'), ('universal_truth', True)):
            receipt = copy.deepcopy(self.receipt)
            receipt[key] = value
            self.entry['receipt'] = self.bind('receipt.json', receipt)
            station = self.result()['stations'][0]
            self.assertEqual(station['status'], 'unresolved')
            self.assertNotIn('scoped_summary', station)
            self.assertEqual(station['reported_receipt'], receipt)

    def test_forged_summary_or_dropped_rows_rejected(self):
        for alter in ('matches', 'drop', 'bool', 'duplicate', 'fraction', 'labels'):
            receipt = copy.deepcopy(self.receipt)
            if alter == 'matches': receipt['summary']['label_matches'] = 48
            if alter == 'drop': receipt['rows'].pop()
            if alter == 'bool': receipt['summary']['calls'] = True
            if alter == 'duplicate': receipt['rows'][1]['run_id'] = receipt['rows'][0]['run_id']
            if alter == 'fraction': receipt['summary']['match_fraction']['denominator'] = 0
            if alter == 'labels': receipt['summary']['labels'] = {'YES': 48}
            self.entry['receipt'] = self.bind('receipt.json', receipt)
            self.assertEqual(self.result()['stations'][0]['status'], 'unresolved', alter)

    def test_absolute_traversal_and_symlink_escape(self):
        for path in ('/etc/hosts', '../outside.json'):
            self.entry['receipt']['path'] = path
            self.assertEqual(self.result()['stations'][0]['status'], 'unresolved')
        (self.root / 'escape').symlink_to('/etc/hosts')
        self.entry['receipt']['path'] = 'escape'
        self.assertEqual(self.result()['stations'][0]['status'], 'unresolved')

    def test_bad_ancestry_leaves_station_unresolved(self):
        self.entry['ancestry'] = [{'role': 'keys', 'path': 'absent', 'sha256': '0' * 64}]
        self.assertEqual(self.result()['stations'][0]['status'], 'unresolved')

    def test_shared_receipt_and_keys_warn_without_pooling(self):
        other = copy.deepcopy(self.entry)
        other['station_id'] = 'different-task'
        other['question'] = 'Different declared question; no contradiction inference.'
        self.manifest['stations'].append(other)
        out = self.result()
        self.assertEqual(out['status'], 'indexed')
        self.assertTrue(out['ancestry_warnings'])
        self.assertEqual(len(out['stations']), 2)
        self.assertFalse({'answer', 'confidence', 'vote', 'summary', 'contradiction'} & out.keys())

    def test_unknown_manifest_fields_and_duplicate_ids(self):
        self.manifest['vote'] = True
        self.assertEqual(self.result()['status'], 'unresolved')
        del self.manifest['vote']
        self.manifest['stations'].append(copy.deepcopy(self.entry))
        self.assertEqual(self.result()['status'], 'unresolved')

    def test_input_size_bound(self):
        data = b' ' * (registry.MAX_BYTES + 1)
        (self.root / 'receipt.json').write_bytes(data)
        self.entry['receipt']['sha256'] = registry.sha(data)
        self.assertEqual(self.result()['stations'][0]['status'], 'unresolved')

    def test_source_conditional_scope_and_assumptions_preserved(self):
        receipt = json.loads((ROOT / 'evaluation/complete-verification-path-v1/checked_run/DEMO_RECEIPT.json').read_text())
        self.entry['receipt'] = self.bind('receipt.json', receipt)
        station = self.result()['stations'][0]
        self.assertEqual(station['status'], 'indexed')
        self.assertEqual(station['scoped_summary']['kind'], 'reported_conditional_answer')
        self.assertEqual(station['scoped_summary']['declared_model'], receipt['declared_model'])

    def test_cli_strict_manifest_and_read_only(self):
        path = self.root / 'manifest.json'
        path.write_text('{"registry_id":"x","registry_id":"y","stations":[]}')
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        run = subprocess.run([sys.executable, str(ROOT / 'tools/station_registry.py'), str(path), '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)['status'], 'unresolved')
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})


if __name__ == '__main__':
    unittest.main(verbosity=2)
