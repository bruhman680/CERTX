"""Check append-only numeric parsing repair; no model calls or replay writes."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import unittest

P = Path(__file__).resolve().parent
sys.path.insert(0, str(P))
from replay_parser_v2 import parse


class ParserRepairTests(unittest.TestCase):
    def test_current_saved_extraction_texts_preserve_parse(self):
        spec = importlib.util.spec_from_file_location('original_replay', str(P / 'replay_extractions.py'))
        original = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(original)
        rows = list(map(json.loads, (P / 'RAW_OUTPUTS.jsonl').read_text().splitlines()))
        records = {r['id']: r for r in json.loads((P / 'RECORDS.json').read_text())}
        comparisons = 0
        for row in rows:
            if row['task'] not in {'measurement', 'minimum'}:
                continue
            r = records[row['record_id']]
            allow = row['task'] == 'measurement'
            with self.subTest(run=row['run_id']):
                self.assertEqual(parse(row['text'], r['unit'], allow), original.parse(row['text'], r['unit'], allow))
            comparisons += 1
        self.assertEqual(comparisons, 16)

    def test_signed_values_are_not_made_positive(self):
        for text in ['-1 cm', '+1 cm', '- 1 cm', '+ 1 cm', '−1 cm', '− 1 cm', 'The value is -1 cm.', 'The value is +1 cm.', '－1 cm']:
            with self.subTest(text=text):
                self.assertIsNone(parse(text, 'cm', True))

    def test_decimals_and_exponents_reject(self):
        for text in ['1.5 cm', '.5 cm', '1.0 cm', '1e3 cm', '1E+3 cm', '1 e3 cm', '1E-3 cm']:
            with self.subTest(text=text):
                self.assertIsNone(parse(text, 'cm', True))

    def test_multiple_values_and_wrong_units_reject(self):
        for text in ['1 cm and 2 cm', '1 cm, minimum 2 kg', '1 kg', '1 mm', '1 cm/s', '1 cm^2', '1 cm2', '1 cm²', '1 cm-long']:
            with self.subTest(text=text):
                self.assertIsNone(parse(text, 'cm', True))

    def test_explicit_missing_is_literal_and_optional(self):
        self.assertEqual(parse('MISSING', 'cm', True), {'state': 'missing'})
        self.assertEqual(parse(' missing. ', 'cm', True), {'state': 'missing'})
        for text in ['MISSING..', 'MISSING 1 cm', 'No measurement is recorded.', 'UNKNOWN']:
            with self.subTest(text=text):
                self.assertIsNone(parse(text, 'cm', True))
        self.assertIsNone(parse('MISSING', 'cm', False))

    def test_nominal_unsigned_claim_and_validation_boundary(self):
        self.assertEqual(parse('0 cm', 'cm', True), {'state': 'measured', 'value': '0'})
        self.assertEqual(parse('The requested measurement is 7 cm.', 'cm', True), {'state': 'measured', 'value': '7'})
        # Deliberately document the semantic gap; syntax alone is not entailment.
        self.assertEqual(parse('The measurement is not 7 cm.', 'cm', True), {'state': 'measured', 'value': '7'})
        self.assertIsNone(parse(7, 'cm', True))
        self.assertIsNone(parse('7 cm', 'cm', 1))
        self.assertIsNone(parse('7 cm', 'mm', True))


if __name__ == '__main__':
    unittest.main()
