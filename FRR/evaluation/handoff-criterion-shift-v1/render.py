#!/usr/bin/env python3
"""Render frozen participant packets; never reads hidden gold or outcome files."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OWNED = ('SOURCE.md', 'DESIGN.md', 'WRITER_PROMPTS.json', 'render.py')
AUTHORITY = (
    'Treat explicit assertions in your handoff as available premises for conditional '
    'reasoning. Missing assertions remain unknown. Any delivered original record is '
    'authoritative within its stated scope and supersedes a contradictory handoff '
    'claim. SUPPORTED means the available premises entail the exact claim. '
    'CONTRADICTED means they entail its negation, including for claims of certification '
    'or authorization. UNRESOLVED means neither the claim nor its negation is entailed. '
    'Do not infer negative findings from missing evidence. Answer only from '
    'your supplied handoff and any delivered record. Source fidelity is evaluated separately.'
)
ISOLATION = (
    'You may read only this designated prompt file once this turn. After reading it, '
    'use no other tools, files, peers or external information. Do not inspect the source '
    'file or request help from another participant.'
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(source):
    found = {}
    for match in re.finditer(r'^## ([WBCA][0-9]{2}) — ([^\n]+)\n(.*?)(?=^## |\Z)', source, re.M | re.S):
        found[match[1]] = {'topic': match[2], 'text': match[0].strip()}
    if len(found) != 26:
        raise ValueError('Expected 26 distinct source records')
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phase', choices=('writers', 'readers'), required=True)
    parser.add_argument('--freeze-receipt', type=Path, required=True)
    parser.add_argument('--questions', type=Path, required=True,
                        help='Public JSON: questions plus response_schema; never gold')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--handoff-a', type=Path)
    parser.add_argument('--handoff-b', type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.freeze_receipt.read_text())
    expected = {name: digest(ROOT / name) for name in OWNED}
    expected['public_questions'] = digest(args.questions)
    if receipt.get('approved') is not True or receipt.get('sha256') != expected:
        raise ValueError('Approved exact source/design/prompts/renderer/questions freeze required')
    source = (ROOT / 'SOURCE.md').read_text()
    entries = records(source)
    prompts = json.loads((ROOT / 'WRITER_PROMPTS.json').read_text())
    if len(prompts['ordinary'].split()) != len(prompts['scoped_preservation'].split()):
        raise ValueError('Writer instruction blocks have unequal word counts')
    packets = {}
    if args.phase == 'writers':
        for label, arm in (('a', 'ordinary'), ('b', 'scoped_preservation')):
            packets[f'writer-{label}.md'] = '\n\n'.join((prompts['common'], prompts[arm], source))
    else:
        if not args.handoff_a or not args.handoff_b:
            raise ValueError('Both exact preserved handoff files are required')
        public = json.loads(args.questions.read_text())
        if set(public) != {'questions', 'response_schema'}:
            raise ValueError('Public questions file must contain only questions and response_schema')
        inventory = '\n'.join(f'{key}: {value["topic"]}' for key, value in entries.items())
        for label, path in (('a', args.handoff_a), ('b', args.handoff_b)):
            for condition in ('summary', 'access'):
                choice = ('Set record_id to "NONE". No record access is available.'
                          if condition == 'summary' else
                          'Set record_id to exactly one inventory ID or "NONE". '
                          'Only that record will be delivered; no further request is allowed.')
                packets[f'reader-{label}-{condition}.md'] = '\n\n'.join((
                    ISOLATION, AUTHORITY,
                    'First turn: return only {"record_id":"ID or NONE","answers":[...]}, '
                    'including initial answers to all eight questions using the supplied answer schema '
                    'and only your handoff as evidence. Select evidence for the next turn as well. ' + choice +
                    ' A request is not evidence for these initial answers. In the next turn you will '
                    'receive the selected record or no new evidence, then return '
                    '{"answers":[...]} for all eight questions. No correctness feedback is supplied.',
                    'HANDOFF\n' + path.read_text(), 'NEUTRAL INVENTORY\n' + inventory,
                    'QUESTIONS AND FINAL RESPONSE SCHEMA\n' + json.dumps(public, ensure_ascii=False, indent=2)))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in packets.items():
        destination = args.output_dir / name
        if destination.exists():
            raise FileExistsError(destination)
        destination.write_text(content.rstrip() + '\n')
    print(json.dumps({'written': list(packets), 'source_words': len(source.split()),
                      'instruction_block_words': len(prompts['ordinary'].split())}))


if __name__ == '__main__':
    main()
