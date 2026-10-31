"""Optional read-only ancestry query over an explicitly declared local DAG."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from evidence_threshold import load_json
from station_registry import read_bound, exact, text, MAX_BYTES

RULESET = 'declared-evidence-ancestry-0.1'
LIMITATIONS = [
    'All edges are caller declarations; results apply only to this supplied graph.',
    'Omitted edges or nodes can change common ancestors; empty output does not establish independence.',
    'Byte hashes bind local files, not authenticity, source truth, causal independence or confidence.',
    'Flat registry shared hashes do not establish a complete actual derivation graph.',
]


def query(manifest, root):
    """Return all maximal common ancestors; parent reachability includes self."""
    root = Path(root).resolve()
    if not exact(manifest, 'graph_id edge_semantics nodes query') or not text(manifest['graph_id']) or not text(manifest['edge_semantics']):
        raise ValueError('Invalid graph envelope.')
    nodes, requested = manifest['nodes'], manifest['query']
    if not isinstance(nodes, list) or not 1 <= len(nodes) <= 256:
        raise ValueError('Expected 1..256 nodes.')
    parents = {}
    for node in nodes:
        if not isinstance(node, dict) or set(node) not in ({'id', 'parents'}, {'id', 'parents', 'artifact'}):
            raise ValueError('Invalid node fields.')
        name, links = node['id'], node['parents']
        if not text(name) or name in parents or not isinstance(links, list) or not all(text(x) for x in links) or len(set(links)) != len(links):
            raise ValueError('Invalid or duplicate node/parents.')
        parents[name] = set(links)
        if 'artifact' in node:
            read_bound(node['artifact'], root)
    if any(p not in parents for links in parents.values() for p in links):
        raise ValueError('Unknown parent.')
    if not isinstance(requested, list) or not requested or not all(text(x) and x in parents for x in requested) or len(set(requested)) != len(requested):
        raise ValueError('Invalid or unknown query node.')
    # Iterative elimination avoids recursion limits and validates disconnected components.
    remaining = set(parents)
    ancestors = {}
    while remaining:
        ready = sorted(n for n in remaining if not (parents[n] & remaining))
        if not ready:
            raise ValueError('Cycle in declared graph.')
        for n in ready:
            ancestors[n] = {n}.union(*(ancestors[p] for p in parents[n]))
            remaining.remove(n)
    common = set.intersection(*(ancestors[n] for n in requested))
    maximal = sorted(c for c in common if not any(c != d and c in ancestors[d] for d in common))
    return {'ruleset': RULESET, 'status': 'computed', 'graph_id': manifest['graph_id'],
            'edge_semantics': manifest['edge_semantics'], 'query': requested,
            'ancestor_includes_self': True, 'common_ancestors': sorted(common),
            'maximal_common_ancestors': maximal, 'node_count': len(nodes),
            'edge_count': sum(map(len, parents.values())), 'limitations': LIMITATIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    try:
        with args.manifest.open('rb') as stream:
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError('Manifest exceeds one MiB.')
        result = query(load_json(data), args.root)
        result.update(manifest_sha256=hashlib.sha256(data).hexdigest(),
                      tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      json_loader_sha256=hashlib.sha256(Path(__file__).with_name('evidence_threshold.py').read_bytes()).hexdigest())
    except (ValueError, OSError, TypeError) as exc:
        result = {'ruleset': RULESET, 'status': 'rejected', 'reason': str(exc), 'limitations': LIMITATIONS}
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'computed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
