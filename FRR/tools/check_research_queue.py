"""Check saved research queue consistency, not experiment completion or truth."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_queue(queue, root):
    root = root.resolve()
    entries = queue['entries']
    by_id = {entry['id']: entry for entry in entries}
    if len(by_id) != len(entries):
        raise ValueError('Duplicate queue ID')
    statuses = set(queue['status_values'])
    complete = {'completed_prior_scope', 'instrument_checked'}
    has_contact_record = complete | {'partial_contact'}
    for entry in entries:
        if entry['status'] not in statuses or type(entry['priority']) is not int:
            raise ValueError('Invalid status or priority')
        if entry['priority'] < 0:
            raise ValueError('Negative priority')
        for field in ['question', 'comparison', 'metrics', 'title']:
            if not entry[field]:
                raise ValueError(f'Missing {field}: {entry["id"]}')
        if (entry['status'] in has_contact_record) != bool(entry['result']):
            raise ValueError(f'Status/result mismatch: {entry["id"]}')
        for field in ['source', 'protocol', 'result']:
            if entry.get(field):
                relative = Path(entry[field])
                path = (root / relative).resolve()
                if relative.is_absolute() or not path.is_relative_to(root) or not path.is_file():
                    raise ValueError(f'Missing or invalid local {field}: {entry["id"]}')
        if not set(entry['depends_on']) <= set(by_id) or entry['id'] in entry['depends_on']:
            raise ValueError(f'Invalid dependencies: {entry["id"]}')
        if entry['status'] in {'blocked_inputs', 'awaiting_url', 'partial_contact'} and not entry['needs']:
            raise ValueError('Blocked entry lacks stated missing input')
    done, active = set(), set()

    def visit(item):
        if item in active:
            raise ValueError('Dependency cycle')
        if item in done:
            return
        active.add(item)
        for dependency in by_id[item]['depends_on']:
            visit(dependency)
        active.remove(item)
        done.add(item)

    for item in by_id:
        visit(item)
    return dict(entries=len(entries), completed_prior_contacts=sum(e['status']=='completed_prior_scope' for e in entries),
                checked_instruments=sum(e['status']=='instrument_checked' for e in entries),
                partial_contacts=sum(e['status']=='partial_contact' for e in entries),
                pending=sum(e['status'] not in complete for e in entries),
                dependencies_acyclic=True, local_references_resolve=True)


def main():
    queue = json.loads((ROOT/'evaluation/research-queue/QUEUE.json').read_text())
    result = check_queue(queue, ROOT)
    core = json.loads((ROOT/'evaluation/PRE_REFINEMENT_BASELINE_HASHES.json').read_text())
    for path, expected in core.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Core baseline changed: {path}')
    result['core_hashes_unchanged'] = True
    result['scope'] = 'Saved-plan structure only; no queued scientific test is executed by this check.'
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
