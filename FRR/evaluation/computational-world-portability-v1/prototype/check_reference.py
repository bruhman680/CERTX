"""Trusted-fixture differential check against an independently built Scheme.

Never pass model-generated source to the reference executable: it has host
capabilities. These fixtures and their definitions are authored in this file.
"""
import argparse
import json
import pathlib
import subprocess
import tempfile


DEFINITIONS = [
    '(define (twice x) (+ x x))',
    '(define (sumdown n acc) (if (= n 0) acc (sumdown (- n 1) (+ acc n))))',
    "(define (maptwice xs) (if (null? xs) '() (cons (twice (car xs)) (maptwice (cdr xs)))))",
]


def cases():
    expressions = []
    for a in (-7, -1, 0, 1, 7):
        for b in (-3, -1, 1, 3):
            for op in ('+', '-', '*', 'floor-quotient', 'floor-remainder'):
                expressions.append(f'({op} {a} {b})')
    expressions += [
        '(if #f 11 22)', '(if #t 11 22)', '(if 0 11 22)',
        "(if '() 11 22)", '(not 0)', '(not #f)',
        '(equal? #t 1)', '(equal? #f 0)',
        '(equal? (list 1 (list 2)) (list 1 (list 2)))',
        "(append '(1 2) '(3 4))", "(car '(7 8))", "(cdr '(7 8))",
        "(null? '())", '(list? 1)', '(integer? #t)', '(boolean? 1)',
        '(string-length "aλ🙂")', '(substring "aλ🙂" 1 3)',
        '(string-append "ab" "λ")',
        '(let ((x 2)) (let ((x (+ x 1))) (* x x)))',
        '(twice -3)', '(sumdown 40 0)', "(maptwice '(1 2 3 4))",
        '(if #t 9 (car (quote ())))',
    ]
    return expressions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    from scheme_core import parse_one, compile_definition, evaluate, Symbol

    root = pathlib.Path(__file__).resolve().parents[1]
    profile = json.loads((root / 'constants.json').read_text())
    namespace, artifacts = {}, {}
    for index, source in enumerate(DEFINITIONS):
        payload = compile_definition(parse_one(source, profile), namespace,
                                     artifacts.__getitem__, profile)
        identity = f'trusted-reference-procedure-{index}'
        artifacts[identity] = {'kind': 'procedure', 'payload': payload}
        namespace[payload['name']] = {'kind': 'procedure', 'id': identity}

    expressions = cases()
    scheme = '(import (scheme base) (scheme write))\n'
    scheme += '\n'.join(DEFINITIONS) + '\n'
    scheme += '(write (list\n' + '\n'.join(expressions) + '\n))\n(newline)\n'
    with tempfile.TemporaryDirectory(prefix='cw-reference-') as temp:
        source = pathlib.Path(temp) / 'trusted.scm'
        source.write_text(scheme, encoding='utf-8')
        result = subprocess.run([args.reference, str(source)], text=True,
                                capture_output=True, timeout=10, check=True)
    parsed = parse_one(result.stdout.strip(), profile)

    def reader_value(node):
        if isinstance(node, Symbol):
            raise AssertionError(f'unexpected symbol in reference output: {node}')
        if isinstance(node, list):
            return [reader_value(x) for x in node]
        return node

    expected = reader_value(parsed)
    if len(expected) != len(expressions):
        raise AssertionError('reference result count mismatch')
    rows = []
    for expression, want in zip(expressions, expected):
        actual = evaluate(parse_one(expression, profile), namespace,
                          artifacts.__getitem__, profile)
        # JSON distinguishes Boolean and integer results, unlike Python ==.
        match = json.dumps(actual['value'], ensure_ascii=False) == json.dumps(want, ensure_ascii=False)
        rows.append({'expression': expression, 'reference': want,
                     'prototype': actual['value'], 'match': match,
                     'steps': actual.get('steps'),
                     'work_units': actual.get('work_units')})
    report = {'schema': 'cw-reference-check-v1',
              'scope': 'trusted supported value-semantics fixtures only',
              'reference': 'Chibi Scheme 0.12.0',
              'reference_commit': '08e23be118e7de8cf29d606bc4793371c0ace680',
              'case_count': len(rows), 'matched': sum(r['match'] for r in rows),
              'all_match': all(r['match'] for r in rows),
              'rows': rows, 'definitions': DEFINITIONS,
              'limits': 'Does not validate persistence, cost accounting, unsupported forms, isolation or model competence.'}
    pathlib.Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('case_count', 'matched', 'all_match')}))
    if not report['all_match']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
