"""Development/regression checks for prospective parser/comparator composition."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import pipeline


class PipelineTests(unittest.TestCase):
    def pair(self, measured, minimum='8 cm', record_id='T1'):
        with tempfile.TemporaryDirectory() as directory:
            return pipeline.compute_pair(measured, minimum, 'Rod Test', 'cm', record_id, directory)

    def test_single_sentence_and_list_claims(self):
        for text in ['7 cm', 'The measurement is 7 cm.', '7 cm; 9 cm',
                     'The measurements are 7 cm and 9 cm.']:
            with self.subTest(text=text):
                self.assertTrue(pipeline.parse_measurements(text, 'cm')['usable'])
        self.assertEqual([{'state': 'measured', 'value': '7'}, {'state': 'measured', 'value': '9'}],
                         pipeline.parse_measurements('7 cm; 9 cm', 'cm')['observations'])

    def test_sign_decimal_exponent_and_unmatched_digits_reject(self):
        for text in ['-1 cm', '+1 cm', '− 1 cm', '1.5 cm', '1e2 cm', '5 cm and 8',
                     '5 cm2', '5 cm/s', '5 cm^2', 'Item 2 measures 5 cm', '5 kg']:
            with self.subTest(text=text):
                self.assertFalse(pipeline.parse_measurements(text, 'cm')['usable'])

    def test_minimum_requires_single_numeric_quantity(self):
        self.assertEqual('8', pipeline.parse_minimum('The minimum is 8 cm.', 'cm')['value'])
        for text in ['MISSING', 'MISSING; 8 cm', '8 cm; 9 cm', '', 'unknown', '8 kg']:
            with self.subTest(text=text):
                self.assertFalse(pipeline.parse_minimum(text, 'cm')['usable'])

    def test_exact_comparison_and_equality(self):
        for value, expected in [('7', 'NO'), ('8', 'YES'), ('9', 'YES')]:
            with self.subTest(value=value):
                result = self.pair(value + ' cm')
                self.assertEqual(expected, result['action'])
                self.assertEqual('compared', result['stage'])
                self.assertEqual(value, result['receipt']['comparison']['value'])

    def test_conflicts_preserved_even_on_same_side(self):
        for text in ['7 cm; 9 cm', '9 cm; 10 cm', 'MISSING; 9 cm']:
            with self.subTest(text=text):
                result = self.pair(text)
                self.assertEqual('UNKNOWN', result['action'])
                self.assertEqual('conflicting_measurements', result['stage'])

    def test_duplicate_values_not_disagreement_or_independence(self):
        result = self.pair('9 cm; 9 cm')
        self.assertEqual('YES', result['action'])
        self.assertEqual(2, result['receipt']['measured_count'])

    def test_explicit_missing_is_not_parser_failure(self):
        result = self.pair('MISSING')
        self.assertEqual('UNKNOWN', result['action'])
        self.assertEqual('missing_measurement', result['stage'])
        invalid = self.pair('No usable field was returned.')
        self.assertEqual('UNKNOWN', invalid['action'])
        self.assertEqual('extraction_unusable', invalid['stage'])
        self.assertIsNone(invalid['receipt'])

    def test_invalid_minimum_withholds_even_when_measurement_missing(self):
        result = self.pair('MISSING', 'unavailable')
        self.assertEqual('UNKNOWN', result['action'])
        self.assertEqual('extraction_unusable', result['stage'])
        self.assertIsNone(result['receipt'])

    def test_generated_values_not_gold_repaired(self):
        result = self.pair('9 cm', '9 cm')
        self.assertEqual('9', result['receipt']['comparison']['minimum'])
        self.assertEqual('YES', result['action'])

    def test_exclusive_artifact_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            first = pipeline.compute_pair('9 cm', '8 cm', 'Rod Test', 'cm', 'T1', directory)
            saved = Path(first['artifact_path']).read_bytes()
            with self.assertRaises(FileExistsError):
                pipeline.compute_pair('7 cm', '8 cm', 'Rod Test', 'cm', 'T1', directory)
            self.assertEqual(saved, Path(first['artifact_path']).read_bytes())
            self.assertEqual([{'state': 'measured', 'value': '9'}],
                             json.loads(saved)['observations'])

    def test_unsafe_identifier_and_changed_checker_withhold(self):
        self.assertEqual('invalid_pipeline_context', self.pair('9 cm', record_id='../escape')['stage'])
        with mock.patch.object(pipeline, '_sha', return_value='changed'):
            self.assertEqual('checker_changed', self.pair('9 cm')['stage'])

    def test_documented_semantic_boundary(self):
        # This surface parser does not infer the truth of a sentence or negation.
        claim = pipeline.parse_measurements('The measurement is not 7 cm.', 'cm')
        self.assertTrue(claim['usable'])
        self.assertEqual('7', claim['observations'][0]['value'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
