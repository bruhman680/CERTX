"""Authored adversarial instrument checks; not model performance or source truth."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import tempfile
import subprocess
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import evidence_threshold as tool


class ThresholdTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / 'evidence'
        self.root.mkdir()
        self.artifact = {'entity': 'Parcel Elm', 'scope': 'run-A', 'unit': 'kg',
                         'observations': [{'state': 'measured', 'value': '6'}]}
        self.contract = {'claim_id': 'pass-Elm', 'entity': 'Parcel Elm', 'scope': 'run-A',
                         'criterion': {'id': 'minimum-six', 'operator': 'at_least',
                                       'minimum': '6', 'unit': 'kg'},
                         'evidence': {'path': 'measurement.json', 'sha256': '0' * 64}}

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, artifact=None, raw=None):
        if raw is None:
            raw = json.dumps(self.artifact if artifact is None else artifact).encode()
        (self.root / 'measurement.json').write_bytes(raw)
        self.contract['evidence']['sha256'] = hashlib.sha256(raw).hexdigest()
        return tool.assess(self.contract, self.root)

    def test_grid_negative_zero_equality_and_positive(self):
        for minimum in [-8, -1, 0, 1, 8]:
            for delta in [-1, 0, 1]:
                with self.subTest(minimum=minimum, delta=delta):
                    self.contract['criterion']['minimum'] = minimum
                    self.artifact['observations'][0]['value'] = minimum + delta
                    got = self.write()
                    self.assertEqual(got['verdict'], 'supported' if delta >= 0 else 'contradicted')
                    self.assertEqual(got['stage'], 'compared')

    def test_exact_decimal_boundary_not_binary_float(self):
        self.contract['criterion']['minimum'] = '0.10000000000000000000000000000000000001'
        self.artifact['observations'][0]['value'] = '0.10000000000000000000000000000000000000'
        self.assertEqual(self.write()['verdict'], 'contradicted')
        self.artifact['observations'][0]['value'] = self.contract['criterion']['minimum']
        self.assertEqual(self.write()['verdict'], 'supported')

    def test_explicit_missing_is_unresolved_not_failure(self):
        for observations in [[{'state': 'missing'}], [{'state': 'missing'}, {'state': 'missing'}]]:
            with self.subTest(observations=observations):
                self.artifact['observations'] = observations
                got = self.write()
                self.assertEqual((got['verdict'], got['stage']), ('unresolved', 'missing_measurement'))

    def test_empty_observations_differ_from_source_explicit_missing(self):
        self.artifact['observations'] = []
        got = self.write()
        self.assertEqual((got['verdict'], got['stage']), ('unresolved', 'no_observations'))
        self.assertEqual(got['missing_count'], 0)
        self.artifact['observations'] = [{'state': 'missing'}]
        got = self.write()
        self.assertEqual((got['verdict'], got['stage']), ('unresolved', 'missing_measurement'))
        self.assertEqual(got['missing_count'], 1)

    def test_deep_json_fails_closed_for_artifact_and_cli_contract(self):
        # This input is well inside the one-MiB byte cap but exceeds recursive parsing depth.
        raw = b'[' * 10000 + b'0' + b']' * 10000
        self.assertLess(len(raw), tool.MAX_ARTIFACT_BYTES)
        got = self.write(raw=raw)
        self.assertEqual((got['verdict'], got['stage']), ('unresolved', 'invalid_evidence'))
        contract_file = self.root / 'deep-contract.json'
        contract_file.write_bytes(raw)
        process = subprocess.run([sys.executable, str(Path(tool.__file__)), str(contract_file),
                                  '--root', str(self.root)], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0)
        got = json.loads(process.stdout)
        self.assertEqual((got['verdict'], got['stage']), ('unresolved', 'invalid_contract'))
        self.assertNotIn('Traceback', process.stderr)

    def test_conflicts_with_or_without_same_pass_direction(self):
        for observations in [[{'state': 'measured', 'value': '5'}, {'state': 'measured', 'value': '4'}],
                             [{'state': 'measured', 'value': '5'}, {'state': 'measured', 'value': '7'}],
                             [{'state': 'missing'}, {'state': 'measured', 'value': '7'}]]:
            with self.subTest(observations=observations):
                self.artifact['observations'] = observations
                got = self.write()
                self.assertEqual((got['verdict'], got['stage']), ('unresolved', 'conflicting_measurements'))

    def test_duplicate_equal_values_remain_one_comparison_not_independence(self):
        self.artifact['observations'] = [{'state': 'measured', 'value': '6.00'},
                                         {'state': 'measured', 'value': 6}]
        got = self.write()
        self.assertEqual(got['verdict'], 'supported')
        self.assertEqual(got['measured_count'], 2)
        self.assertNotIn('independent_evidence_count', got)

    def test_measurement_rejects_bool_float_nonfinite_and_unsupported_notation(self):
        for value in [True, False, 6.0, float('nan'), float('inf'), '-Infinity', 'NaN', '1e3', '', ' 6 ', {}, [], '9' * 129]:
            with self.subTest(value=repr(value)):
                self.artifact['observations'] = [{'state': 'measured', 'value': value}]
                got = self.write()
                self.assertEqual(got['verdict'], 'unresolved')
                self.assertEqual(got['stage'], 'invalid_evidence')

    def test_invalid_minimum_rejects_contract_before_artifact(self):
        for value in [True, 6.0, float('nan'), float('inf'), 'NaN', '1e3', None]:
            with self.subTest(value=repr(value)):
                self.contract['criterion']['minimum'] = value
                got = tool.assess(self.contract, self.root)
                self.assertEqual(got['stage'], 'invalid_contract')
                self.assertFalse(got['binding']['artifact_sha256'])

    def test_identity_and_units_exact_no_conversion_or_whitespace_repair(self):
        for field, value in [('entity', 'Parcel Ash'), ('scope', 'run-B'), ('unit', 'g'), ('unit', ' kg')]:
            with self.subTest(field=field, value=value):
                artifact = copy.deepcopy(self.artifact)
                artifact[field] = value
                got = self.write(artifact)
                self.assertEqual(got['stage'], 'identity_mismatch')
                self.assertTrue(got['binding']['artifact_sha256'])
                self.assertFalse(got['binding']['entity_scope_unit'])

    def test_hash_mismatch_precedes_json_parse(self):
        self.write(raw=b'not JSON')
        self.contract['evidence']['sha256'] = '0' * 64
        got = tool.assess(self.contract, self.root)
        self.assertEqual(got['stage'], 'artifact_mismatch')
        self.assertFalse(got['binding']['artifact_sha256'])

    def test_bound_duplicate_json_fields_rejected(self):
        raw = b'{"entity":"Parcel Elm","entity":"Parcel Ash","scope":"run-A","unit":"kg","observations":[]}'
        self.assertEqual(self.write(raw=raw)['stage'], 'invalid_evidence')

    def test_strict_contract_reader_rejects_nonfinite_and_duplicate_fields(self):
        for raw in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}']:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    tool.load_json(raw)

    def test_schema_does_not_treat_unrecognized_fields_as_valid_facts(self):
        for change in ['extra_artifact', 'extra_observation', 'unknown_state', 'not_list']:
            with self.subTest(change=change):
                artifact = copy.deepcopy(self.artifact)
                if change == 'extra_artifact':
                    artifact['unverified_source_claim'] = True
                elif change == 'extra_observation':
                    artifact['observations'][0]['unit'] = 'g'
                elif change == 'unknown_state':
                    artifact['observations'][0] = {'state': 'unknown'}
                else:
                    artifact['observations'] = {'state': 'missing'}
                self.assertEqual(self.write(artifact)['stage'], 'invalid_evidence')

    def test_contract_extra_field_or_operator_rejected(self):
        contract = copy.deepcopy(self.contract)
        contract['extra'] = True
        self.assertEqual(tool.assess(contract, self.root)['stage'], 'invalid_contract')
        self.contract['criterion']['operator'] = 'approximately_at_least'
        self.assertEqual(tool.assess(self.contract, self.root)['stage'], 'invalid_contract')

    def test_absolute_path_parent_escape_and_symlink_escape_rejected(self):
        outside = Path(self.tmp.name) / 'outside.json'
        outside.write_text('{}')
        link = self.root / 'escape.json'
        link.symlink_to(outside)
        for path in [str(outside), '../outside.json', 'escape.json']:
            with self.subTest(path=path):
                self.contract['evidence']['path'] = path
                self.assertEqual(tool.assess(self.contract, self.root)['stage'], 'invalid_contract')

    def test_missing_file_does_not_mean_contradicted(self):
        got = tool.assess(self.contract, self.root)
        self.assertEqual((got['verdict'], got['stage']), ('unresolved', 'evidence_unavailable'))

    def test_input_bound_enforced_even_with_matching_hash(self):
        self.assertEqual(self.write(raw=b' ' * (tool.MAX_ARTIFACT_BYTES + 1))['stage'], 'invalid_evidence')

    def test_receipt_binds_contract_but_does_not_authenticate_truth(self):
        got = self.write()
        old_hash = got['contract_sha256']
        self.contract['criterion']['id'] = 'revised-minimum-id'
        changed = tool.assess(self.contract, self.root)
        self.assertNotEqual(changed['contract_sha256'], old_hash)
        self.assertIn('not extracted or authenticated', ' '.join(got['limitations']))
        self.assertEqual(got['checker_sha256'], hashlib.sha256(Path(tool.__file__).read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main(verbosity=2)
