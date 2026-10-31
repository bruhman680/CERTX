"""Authored exact-output and rejection cases, frozen before real contact."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from evidence_ancestry import query
from evidence_threshold import load_json


def graph(edges, asked):
    return {'graph_id': 'authored', 'edge_semantics': 'child declares parent',
            'nodes': [{'id': n, 'parents': p} for n,p in edges.items()], 'query': asked}


class AncestryTests(unittest.TestCase):
    def answer(self, edges, asked):
        return query(graph(edges, asked), Path('.'))['maximal_common_ancestors']

    def test_tree(self):
        self.assertEqual(self.answer({'r':[], 'a':['r'], 'b':['a'], 'c':['a']}, ['b','c']), ['a'])

    def test_two_incomparable_lcas(self):
        self.assertEqual(self.answer({'r':[], 'a':['r'], 'b':['r'], 'x':['a','b'], 'y':['a','b']}, ['x','y']), ['a','b'])

    def test_shortcut_depth_trap(self):
        # b has an arbitrarily deep route plus root shortcut; a is shallow.
        # Both are maximal; no depth metric may discard a.
        edges={'r':[], 'd1':['r'], 'd2':['d1'], 'b':['r','d2'], 'a':['r'], 'x':['a','b'], 'y':['a','b']}
        self.assertEqual(self.answer(edges, ['x','y']), ['a','b'])

    def test_transitive_common_ancestor_removed(self):
        self.assertEqual(self.answer({'r':[], 'a':['r'], 'x':['r','a'], 'y':['r','a']}, ['x','y']), ['a'])

    def test_self_and_one_query(self):
        self.assertEqual(self.answer({'r':[], 'a':['r']}, ['a']), ['a'])
        self.assertEqual(self.answer({'r':[], 'a':['r']}, ['r','a']), ['r'])

    def test_multiple_roots(self):
        self.assertEqual(self.answer({'a':[], 'b':[]}, ['a','b']), [])

    def test_cycles_all_components(self):
        for edges in ({'a':['a']}, {'a':['b'], 'b':['a']}, {'ok':[], 'a':['b'], 'b':['a']}):
            with self.subTest(edges=edges), self.assertRaisesRegex(ValueError,'Cycle'):
                self.answer(edges, [next(iter(edges))])

    def test_unknown_parent_and_query(self):
        for edges,asked in [({'a':['missing']},['a']), ({'a':[]},['missing'])]:
            with self.subTest(edges=edges), self.assertRaises(ValueError): self.answer(edges,asked)

    def test_duplicate_and_shape(self):
        base=graph({'a':[]},['a'])
        variants=[{**base,'nodes':base['nodes']*2}, graph({'a':['a','a']},['a']), graph({'a':[]},['a','a']), {**base,'extra':1}, graph({'a':[]},[])]
        for variant in variants:
            with self.subTest(variant=variant), self.assertRaises(ValueError): query(variant,Path('.'))

    def test_artifact_integrity_path_and_symlink(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root=Path(directory); (root/'ok').write_bytes(b'bound'); (Path(outside)/'secret').write_bytes(b'bound')
            (root/'link').symlink_to(Path(outside)/'secret')
            digest=hashlib.sha256(b'bound').hexdigest()
            def bound(path,sha=digest):
                g=graph({'a':[]},['a']);g['nodes'][0]['artifact']={'path':path,'sha256':sha};return g
            self.assertEqual(query(bound('ok'),root)['maximal_common_ancestors'], ['a'])
            for path,sha in [('ok','0'*64),('ok','invalid'),('../escape',digest),('/etc/passwd',digest),('link',digest),('missing',digest)]:
                with self.subTest(path=path,sha=sha), self.assertRaises((ValueError,OSError)): query(bound(path,sha),root)

    def test_strict_json(self):
        for value in (b'{"a":1,"a":2}', b'{"a":NaN}'):
            with self.assertRaises(ValueError): load_json(value)

    def test_node_limit(self):
        with self.assertRaises(ValueError): self.answer({str(i):[] for i in range(257)},['0'])

if __name__ == '__main__': unittest.main(verbosity=2)
