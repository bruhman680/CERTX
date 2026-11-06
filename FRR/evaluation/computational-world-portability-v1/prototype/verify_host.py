"""Reproduce host checks; never loads or invokes a language model."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    study = here.parent
    files = [*sorted(here.glob('*.py')), study / 'constants.json']
    before = {str(p.relative_to(study)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

    class Result(unittest.TextTestResult):
        successes = []
        def addSuccess(self, test):
            super().addSuccess(test)
            self.successes.append(test.id())

    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(here), pattern='test_*.py')
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=Result).run(suite)
    unit = {'tests_run': result.testsRun, 'passed': len(result.successes),
            'failures': [(str(t), text) for t, text in result.failures],
            'errors': [(str(t), text) for t, text in result.errors],
            'test_ids': result.successes, 'all_pass': result.wasSuccessful()}
    (study / 'UNIT_CHECKS.json').write_text(json.dumps(unit, indent=2) + '\n')
    (study / 'HOST_TEST_LOG.txt').write_text(stream.getvalue())
    subprocess.run([sys.executable, str(here / 'check_reference.py'),
                    '--reference', args.reference, '--output', str(study / 'REFERENCE_CHECK.json')],
                   cwd=here, check=True, timeout=30)
    subprocess.run([sys.executable, str(here / 'run_demo.py'),
                    '--output', str(study / 'HOST_DEMO.json')], cwd=here, check=True, timeout=30)
    ref = json.loads((study / 'REFERENCE_CHECK.json').read_text())
    demo = json.loads((study / 'HOST_DEMO.json').read_text())
    after = {str(p.relative_to(study)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    combined = {'schema': 'cw-host-validation-v1', 'model_calls': 0,
                'unit_tests': unit['tests_run'], 'unit_pass': unit['all_pass'],
                'reference_cases': ref['case_count'], 'reference_matched': ref['matched'],
                'host_demo_commands': len(demo['commands']),
                'host_demo_checks': len(demo['assertions']), 'host_demo_pass': demo['all_pass'],
                'source_unchanged_during_validation': before == after,
                'source_sha256': after,
                'all_pass': unit['all_pass'] and ref['all_match'] and demo['all_pass'] and before == after,
                'limits': 'Finite trusted fixtures. Not full Scheme conformance, formal proof, adversarial security certification, complete blueprint acceptance or evidence of model competence.'}
    (study / 'CHECKS.json').write_text(json.dumps(combined, indent=2) + '\n')
    print(json.dumps({k: combined[k] for k in ('unit_tests', 'reference_cases', 'host_demo_checks', 'all_pass')}))
    if not combined['all_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
