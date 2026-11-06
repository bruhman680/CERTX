"""Host-authored construction walkthrough; no model participates."""
import argparse
import json
from pathlib import Path
import tempfile

from world_store import World


PLAN = [
    "(put seed '(1 2 3))",
    '(define (twice x) (+ x x))',
    "(define (map-twice xs) (if (null? xs) '() (cons (twice (car xs)) (map-twice (cdr xs)))))",
    '(run-save doubled (map-twice seed))',
    '(define (twice x) (+ x 100))',
    '(run (map-twice seed))',
    '(define (first xs) (car xs))',
    "(run (first '()))",
    '(define (first xs) (if (null? xs) (list "absent") (list "present" (car xs))))',
    "(run (first '()))",
    "(put checkpoint '((2 3) ()))",
    '(define (step state) (let ((xs (car state))) (if (null? xs) state (list (cdr xs) (append (car (cdr state)) (list (+ (car xs) (car xs))))))))',
    '(define (advance state) (step state))',
    '(run-save checkpoint (advance checkpoint))',
    '(define (step state) state)',
    '(run-save checkpoint (advance checkpoint))',
    '(drop twice)',
    '(run (map-twice seed))',
    "(run-save failed-result (car '()))",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    profile = json.loads((Path(__file__).resolve().parents[1] / 'constants.json').read_text())
    rows, assertions = [], []
    with tempfile.TemporaryDirectory(prefix='cw-host-demo-') as directory:
        db = str(Path(directory) / 'world.sqlite')
        world = World(db, profile)
        for index, source in enumerate(PLAN, 1):
            if index == 15:
                before = world.snapshot()
                world.close()
                world = World(db, profile)
                assertions.append({'check': 'pause_reload_same_snapshot',
                                   'pass': before == world.snapshot()})
            before = world.snapshot()['id']
            receipt = world.submit(f'demo-{index:02}', before, source)
            rows.append({'command': source, 'receipt': receipt})
        assertions += [
            {'check': 'constructed_map', 'pass': rows[3]['receipt']['value'] == [2, 4, 6]},
            {'check': 'helper_revision_does_not_change_old_map', 'pass': rows[5]['receipt']['value'] == [2, 4, 6]},
            {'check': 'empty_list_error', 'pass': rows[7]['receipt']['error']['code'] == 'EMPTY_LIST'},
            {'check': 'guarded_revision', 'pass': rows[9]['receipt']['value'] == ['absent']},
            {'check': 'first_checkpoint', 'pass': rows[13]['receipt']['value'] == [[3], [4]]},
            {'check': 'pinned_continuation_after_reload', 'pass': rows[15]['receipt']['value'] == [[], [4, 6]]},
            {'check': 'dropped_alias_does_not_break_pinned_dependency', 'pass': rows[17]['receipt']['value'] == [2, 4, 6]},
            {'check': 'failed_result_not_published', 'pass': 'failed-result' not in world.snapshot()['aliases']},
        ]
        unexpected = [i + 1 for i, row in enumerate(rows)
                      if row['receipt'].get('error') and i + 1 not in (8, 19)]
        assertions.append({'check': 'no_unexpected_errors', 'pass': not unexpected})
        integrity = world.verify_integrity()
        world.close()
    result = {'schema': 'cw-host-demo-v1', 'model_participated': False,
              'scope': 'host-authored fixtures in a disposable world',
              'commands': rows, 'assertions': assertions,
              'all_pass': all(x['pass'] for x in assertions), 'integrity': integrity}
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'commands': len(rows), 'checks': len(assertions),
                      'all_pass': result['all_pass']}))
    if not result['all_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
