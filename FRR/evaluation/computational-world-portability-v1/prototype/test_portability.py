import copy
import json
from pathlib import Path
import tempfile
import unittest

import scheme_core as sc
from world_cli import compact_observation
from world_store import World
from world_bundle import BundleError, export_world, import_world, digest, packed


def datum(value):
    if type(value) is bool:
        return '#t' if value else '#f'
    if type(value) is int:
        return str(value)
    if type(value) is list:
        return '(' + ' '.join(datum(x) for x in value) + ')'
    return '"' + ''.join('\\"' if c == '"' else '\\\\' if c == '\\'
                          else '\\x%x;' % ord(c) if ord(c) < 32 else c for c in value) + '"'


class PortableWorldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cw-portable-')
        self.root = Path(self.temp.name)
        self.profile = json.loads((Path(__file__).resolve().parents[1] / 'constants.json').read_text())
        self.world = World(self.root / 'source.sqlite', self.profile)
        self.sequence = 0

    def tearDown(self):
        self.world.close()
        self.temp.cleanup()

    def submit(self, source):
        self.sequence += 1
        return self.world.submit('test-' + str(self.sequence), self.world.snapshot()['id'], source)

    def pages(self, target, field, count=37, run=False):
        cursor, chunks, previous_end = '', [], 0
        before = self.world.snapshot()['id']
        for _ in range(500):
            command = ('(page-run '+datum(target)+' '+datum(cursor)+' '+str(count)+')') if run else (
                '(page '+datum(target)+' '+field+' '+datum(cursor)+' '+str(count)+')')
            receipt = self.submit(command)
            self.assertEqual(receipt['status'], 'OBSERVED', receipt.get('error'))
            page = receipt['value']
            self.assertEqual(page['offset'], previous_end)
            self.assertEqual(page['end'] - page['offset'], len(page['chunk']))
            self.assertLessEqual(len(json.dumps(compact_observation(receipt, self.profile), ensure_ascii=False).encode()),
                                 self.profile['max_observation_bytes'])
            self.assertFalse(compact_observation(receipt, self.profile)['truncated'])
            self.assertEqual(self.world.snapshot()['id'], before)
            chunks.append(page['chunk']); previous_end = page['end']
            if page['complete']:
                self.assertIsNone(page['next_cursor'])
                return ''.join(chunks)
            self.assertGreater(page['end'], page['offset'])
            cursor = page['next_cursor']
        self.fail('paging did not finish')

    def test_unicode_source_and_nested_data_reconstruct_exactly(self):
        source = '(define (message x) (string-append '+datum('λ🙂' * 240)+' x))'
        self.assertEqual(self.submit(source)['status'], 'PUBLISHED')
        self.assertEqual(self.pages('message', 'source'), source)
        value = ['λ🙂\x01"\\' * 24, [1, [True, False, -7]], []]
        self.assertEqual(self.submit('(put sample (quote '+datum(value)+'))')['status'], 'PUBLISHED')
        text = self.pages('sample', 'value', count=19)
        self.assertEqual(sc.value_from_wire(json.loads(text)), value)

    def test_pure_omitted_result_is_retrievable_without_rerun(self):
        value = '🙂' * 1000
        receipt = self.submit('(run '+datum(value)+')')
        self.assertEqual(receipt['status'], 'COMPUTED')
        self.assertTrue(compact_observation(receipt, self.profile)['truncated'])
        request = receipt['event']['request_id']
        before = self.world.snapshot()
        text = self.pages(request, '', count=128, run=True)
        self.assertEqual(sc.value_from_wire(json.loads(text)), value)
        self.assertEqual(self.world.snapshot(), before)

    def test_cursor_binding_and_invalid_counts(self):
        self.submit('(put x "abcdefghijk")')
        page = self.submit('(page x value "" 3)')['value']
        cursor = page['next_cursor']
        self.submit('(put y 3)')
        result = self.submit('(page x value '+datum(cursor)+' 3)')
        self.assertEqual(result['error']['code'], 'CURSOR')
        for command in ('(page x value "bogus" 3)', '(page x value "" #t)',
                        '(page x value "" 0)', '(page x source "" 3)',
                        '(page-run "missing" "" 3)'):
            self.assertIsNotNone(self.submit(command)['error'])

    def test_dropped_alias_retains_revision_page_access(self):
        self.submit('(put old (quote (1 2 3)))')
        identity = self.world.snapshot()['aliases']['old']['id']
        self.submit('(drop old)')
        self.assertEqual(sc.value_from_wire(json.loads(self.pages(identity, 'value'))), [1, 2, 3])

    def test_small_observation_cap_shrinks_escaped_pages(self):
        self.world.close()
        self.profile['max_observation_bytes'] = 1200
        self.world = World(self.root / 'small.sqlite', self.profile)
        value = '\x01🙂' * 100
        self.submit('(put text '+datum(value)+')')
        self.assertEqual(sc.value_from_wire(json.loads(self.pages('text', 'value', 512))), value)

    def populate(self):
        self.submit('(define (helper x) (+ x x))')
        self.submit('(define (outer x) (helper x))')
        self.submit('(define (helper x) (+ x 100))')
        self.submit('(put checkpoint (quote ((3) (4))))')
        self.submit('(define (advance state) (let ((xs (car state))) (list (cdr xs) (append (car (cdr state)) (list (outer (car xs)))))))')
        expected = self.world.snapshot()['id']
        receipt = self.world.submit('original-run', expected, '(run-save result (outer 3))')
        self.assertEqual(receipt['value'], 6)
        self.submit("(run-save failure (car '()))")
        return expected, receipt

    def bundle(self):
        path = self.root / 'world.json'
        export_world(self.world, path)
        return path

    def test_export_rebuild_exact_state_history_and_retry(self):
        expected, receipt = self.populate()
        snapshot = self.world.snapshot()
        audit = self.world.audit()
        bundle = self.bundle()
        self.assertEqual(self.world.snapshot(), snapshot)
        result = import_world(bundle, self.root / 'rebuilt.sqlite', self.profile)
        self.assertEqual(result['snapshot'], snapshot['id'])
        rebuilt = World(self.root / 'rebuilt.sqlite', self.profile)
        try:
            self.assertEqual(rebuilt.snapshot(), snapshot)
            self.assertEqual(rebuilt.audit(), audit)
            self.assertEqual(rebuilt.submit('original-run', expected, '(run-save result (outer 3))'), receipt)
            out = rebuilt.submit('new', snapshot['id'], '(run (outer 4))')
            self.assertEqual(out['value'], 8)
            check = rebuilt.submit('checkpoint', snapshot['id'], '(run checkpoint)')
            self.assertEqual(check['value'], [[3], [4]])
            step = rebuilt.submit('continue', snapshot['id'], '(run-save checkpoint (advance checkpoint))')
            self.assertEqual(step['value'], [[], [4, 6]])
        finally:
            rebuilt.close()

    def test_import_refuses_existing_target_unchanged(self):
        bundle = self.bundle()
        destination = self.root / 'existing.sqlite'
        destination.write_bytes(b'preserve-existing-bytes')
        with self.assertRaises(BundleError):
            import_world(bundle, destination, self.profile)
        self.assertEqual(destination.read_bytes(), b'preserve-existing-bytes')

    def modified(self, change, reseal=False):
        bundle = json.loads(self.bundle().read_text())
        change(bundle)
        if reseal:
            for table, rows in bundle['tables'].items():
                bundle['manifest'][table] = {'rows': len(rows), 'sha256': digest(rows)}
            bundle['sha256'] = digest({k: v for k, v in bundle.items() if k != 'sha256'})
        path = self.root / 'changed.json'
        path.write_bytes(packed(bundle))
        return path

    def test_corrupt_checksum_fails_without_publishing(self):
        source = self.modified(lambda b: b['tables']['meta'][0].update(value='corrupted'))
        destination = self.root / 'never.sqlite'
        with self.assertRaises(BundleError):
            import_world(source, destination, self.profile)
        self.assertFalse(destination.exists())

    def test_missing_dependency_fails_even_with_resealed_checksums(self):
        self.populate()
        def change(b):
            b['tables']['artifacts'].pop(0)
        source = self.modified(change, reseal=True)
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', self.profile)
        self.assertFalse((self.root / 'never.sqlite').exists())

    def test_unsupported_version_and_unsettled_request_rejected(self):
        self.populate()
        source = self.modified(lambda b: b['versions'].update(cost='unknown'), reseal=True)
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', self.profile)

    def test_unsettled_request_rejected_without_recovery_or_import(self):
        self.populate()
        source = self.modified(lambda b: b['tables']['requests'][0].update(state='STARTED'), reseal=True)
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', self.profile)
        self.assertFalse((self.root / 'never.sqlite').exists())

    def test_resealed_counter_tampering_rejected(self):
        self.populate()
        def change(b):
            next(row for row in b['tables']['meta'] if row['key'] == 'visit_fuel')['value'] = '0'
        source = self.modified(change, reseal=True)
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', self.profile)

    def test_resealed_receipt_projection_tampering_rejected(self):
        self.populate()
        def change(b):
            row = next(row for row in b['tables']['requests'] if row['id'] == 'original-run')
            receipt = json.loads(row['receipt']); receipt['value'] = 999
            row['receipt'] = json.dumps(receipt)
        source = self.modified(change, reseal=True)
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', self.profile)

    def test_bundle_size_and_duplicate_keys_rejected(self):
        source = self.root / 'invalid.json'
        source.write_text('{"schema":"x","schema":"x"}')
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', self.profile)
        small = dict(self.profile, max_bundle_bytes=10)
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', small)

    def test_mismatched_profile_rejected(self):
        source = self.bundle()
        changed = dict(self.profile, max_steps=self.profile['max_steps'] + 1)
        with self.assertRaises(BundleError):
            import_world(source, self.root / 'never.sqlite', changed)


if __name__ == '__main__':
    unittest.main()
