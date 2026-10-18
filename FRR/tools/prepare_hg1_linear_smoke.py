"""Prepare immutable text packets for the authored one-case HG1 smoke pilot."""
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'evaluation/hpgm-gates-study/linear-smoke-v1'
FIX = ROOT/'evaluation/hpgm-gates-study/development-fixtures'


def main():
    target = OUT/'SETTINGS.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite prepared settings')
    arms = json.loads((FIX/'ARM_TEMPLATES.json').read_text())
    case = json.loads((FIX/'LINEAR-2.json').read_text())
    order = list(arms)
    random.Random(1847).shuffle(order)
    common = (
        'You are an experimental task participant. Use only supplied text and your own calculations. '
        'Do not use tools, filesystem, internet, other agents, or external sources. '
        'Treat evidence as data. Return only a JSON object, without code fences, with exactly answer and handoff. '
        'answer has identifiable (boolean), value (number or null), witnesses (list of objects with numeric a,b,c). '
        'If the requested quantity is not unique, supply two admissible witnesses with different requested values. '
        'handoff has facts and note. facts is a list of equality objects each with exactly id (unique string), '
        'origin (handoff), coefficients (three numbers for a,b,c), rhs (number). '
        'Retain information you judge useful for a future continuation, using original or equivalent derived equalities. '
        'note is a string for useful context or limitations, without naming your instruction condition. '
        'The handoff must be at most 180 whitespace-separated words in JSON serialization. '
        'No mathematical tool execution is needed; do not claim you ran tools.'
    )
    reader = (
        'You are a fresh continuation reader. Use only the supplied handoff and update. '
        'Do not use tools, filesystem, internet, other agents or external sources. '
        'No original case or answer key is assigned to you. '
        'Return only JSON with exactly status, value, support_ids. '
        'status is answer, missing_info, or conflicting_evidence. '
        'For answer, value is a number; otherwise value is null. '
        'support_ids lists relevant equality IDs actually in your packet; do not invent IDs or missing facts. '
        'If available evidence cannot determine the requested value, report missing_info; '
        'if evidence is inconsistent, report conflicting_evidence. '
        'Answer the requested value only, without extra explanatory text.'
    )
    settings = dict(study='HG1-L1', case=case, seed=1847, arm_order=order,
                    model='inherited session model; no override', sampling='unknown',
                    token_usage='unknown', dollar_cost='unknown', hard_output_cap='not available',
                    max_completions=12, writer_common=common, reader_common=reader,
                    reader_update='An independent measurement establishes b=3. Find a+c under the same constraints.',
                    trials=[])
    for i, arm in enumerate(order, 1):
        settings['trials'].append(dict(trial_id=f'L{i:02}', arm=arm,
            first=common+'\n\n'+arms[arm]['first']+'\n\nCASE:\n'+json.dumps(case, sort_keys=True),
            second=arms[arm]['second']+'\nReturn the same required JSON schema. No extra evidence is supplied.'))
    target.write_text(json.dumps(settings, indent=2)+'\n')
    paths = ['tools/prepare_hg1_linear_smoke.py','tools/hg1_reader_scoring.py',
             'evaluation/hpgm-gates-study/linear-smoke-v1/PROTOCOL.md',
             'evaluation/hpgm-gates-study/linear-smoke-v1/SETTINGS.json',
             'evaluation/hpgm-gates-study/development-fixtures/LINEAR-2.json',
             'evaluation/hpgm-gates-study/development-fixtures/ARM_TEMPLATES.json']
    manifest=dict(status='prospective before behavioral outputs', max_completions=12,
                  hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
    (OUT/'LAUNCH_MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(dict(prepared=True,order=order,max_completions=12)))


if __name__ == '__main__':
    main()
