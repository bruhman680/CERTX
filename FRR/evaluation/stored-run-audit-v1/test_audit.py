"""Mutation challenges on disposable copies; historical files never edited."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from stored_run_audit import evaluate

HERE = Path(__file__).resolve().parent
BASE = json.loads((HERE / 'contract.json').read_text())


class AuditChallenge(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.c = copy.deepcopy(BASE)
        for name in ('raw', 'keys'):
            self.c[name]['path'] = name
            (self.root / name).write_bytes((ROOT / BASE[name]['path']).read_bytes())
        self.rows = [json.loads(s) for s in (self.root / 'raw').read_text().splitlines()]
        self.keys = json.loads((self.root / 'keys').read_text())

    def write(self, rows=None, keys=None):
        if rows is not None:
            (self.root / 'raw').write_text(''.join(json.dumps(r)+'\n' for r in rows))
        if keys is not None:
            (self.root / 'keys').write_text(json.dumps(keys))
        self.rehash()

    def rehash(self):
        for name in ('raw', 'keys'):
            self.c[name]['sha256'] = hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def result(self):
        return evaluate(self.c, self.root)

    def test_real_record_and_row_order(self):
        expected = json.loads((HERE / 'EXPECTED.json').read_text())
        out = self.result()
        for k, v in expected.items():
            self.assertEqual(out[k], v)
        self.write(rows=list(reversed(self.rows)))
        self.assertEqual(self.result()['summary'], out['summary'])
        self.assertEqual(self.result()['rows'], out['rows'])

    def test_missing_extra_and_duplicate_runs(self):
        for rows in (self.rows[:-1], self.rows+[self.rows[0]], self.rows[:-1]+[self.rows[0]]):
            with self.subTest(count=len(rows)):
                self.write(rows=rows)
                self.assertEqual(self.result()['stage'], 'cohort_mismatch')

    def test_keys_missing_duplicate_unknown_label(self):
        for keys in (self.keys[:-1], self.keys[:-1]+[self.keys[0]]):
            self.write(keys=keys)
            self.assertEqual(self.result()['stage'], 'cohort_mismatch')
        bad = copy.deepcopy(self.keys)
        bad[0]['expected'] = 'MAYBE'
        self.write(keys=bad)
        self.assertEqual(self.result()['stage'], 'invalid_source')

    def test_tamper_without_rebinding(self):
        (self.root / 'raw').write_bytes((self.root / 'raw').read_bytes()+b' ')
        self.assertEqual(self.result()['stage'], 'source_hash_mismatch')

    def test_wrong_identity_even_with_new_hash(self):
        self.rows[0]['arm'] = 'other_model'
        self.write(rows=self.rows)
        self.assertEqual(self.result()['stage'], 'identity_mismatch')

    def test_bool_wrong_length_negative_tokens(self):
        for update in ({'input_tokens':True}, {'output_tokens':3}, {'generated_token_ids':[-1,2]}):
            rows = copy.deepcopy(self.rows)
            rows[0].update(update)
            self.write(rows=rows)
            self.assertEqual(self.result()['stage'], 'invalid_source')

    def test_unrecognized_is_not_removed(self):
        self.rows[2]['text'] = 'YES, because I think so'
        self.write(rows=self.rows)
        out = self.result()['summary']
        self.assertEqual(out['calls'], 10)
        self.assertEqual(out['labels'], {'YES':9, 'UNRESOLVED':1})
        self.assertEqual(out['label_matches'], 3)
        self.assertEqual(out['match_fraction'], {'numerator':3, 'denominator':10})

    def test_empty_text_remains_in_denominator(self):
        self.rows[2]['text'] = ''
        self.write(rows=self.rows)
        self.assertEqual(self.result()['summary']['labels']['UNRESOLVED'], 1)

    def test_case_whitespace_policy_and_token_limit(self):
        self.rows[0]['text'] = ' \nno\t'
        self.rows[0]['stop'] = 'token_limit'
        self.write(rows=self.rows)
        out = self.result()['summary']
        self.assertEqual(out['label_matches'], 5)
        self.assertEqual(out['stops'], {'token_limit':1, 'eos':9})

    def test_unsupported_stop_and_nonstring_text(self):
        for update in ({'stop':'timeout'}, {'text':None}):
            rows = copy.deepcopy(self.rows)
            rows[0].update(update)
            self.write(rows=rows)
            self.assertEqual(self.result()['stage'], 'invalid_source')

    def test_root_escape_and_absolute(self):
        for path in ('../outside.jsonl', '/tmp/outside.jsonl'):
            self.c['raw']['path'] = path
            self.assertEqual(self.result()['stage'], 'invalid_contract')

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside)/'raw'
            target.write_text('[]')
            (self.root/'link').symlink_to(target)
            self.c['raw']['path'] = 'link'
            self.assertEqual(self.result()['stage'], 'invalid_contract')

    def test_unsupported_parser_or_cohort(self):
        for field, value in [('parser','extract_any_yes'), ('expected_run_ids',[]),
                             ('expected_run_ids',['x','x'])]:
            c = copy.deepcopy(self.c)
            c[field] = value
            self.assertEqual(evaluate(c,self.root)['stage'], 'invalid_contract')

    def test_duplicate_json_nonfinite_blank_and_utf8(self):
        for data in (b'{"run_id":"a","run_id":"b"}\n', b'{"x":NaN}\n',
                     b'\n', b'\xff'):
            (self.root/'raw').write_bytes(data)
            self.rehash()
            self.assertEqual(self.result()['stage'], 'invalid_source')

    def test_unavailable_file(self):
        (self.root/'raw').unlink()
        self.assertEqual(self.result()['stage'], 'source_unavailable')


if __name__ == '__main__':
    unittest.main()
