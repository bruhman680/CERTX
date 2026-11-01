import unittest,itertools
from design import cases,fixture
from ledger import resolve
class Checks(unittest.TestCase):
 def test_cases(self):
  for c in cases():
   r=resolve(c['events'],c['target']);self.assertEqual((r['verdict'],r['state']),(c['expected_verdict'],c['expected_state']),c['kind'])
 def test_all_permutations(self):
  for kind,events,v,s in fixture('Cress'):
   expected=resolve(events,'Cress')
   for order in itertools.permutations(events):
    got=resolve(list(order),'Cress');self.assertEqual((got['verdict'],got['state'],got['heads'],got['status_events']),(expected['verdict'],expected['state'],expected['heads'],expected['status_events']),kind)
 def test_missing_not_deletion(self):
  by={c['kind']:c for c in cases() if c['target']=='Cress'}
  for k,v in [('recorded_missing','KNOWN'),('remove_field','PARTIAL'),('delete_record','DELETED')]:self.assertEqual(resolve(by[k]['events'],'Cress')['verdict'],v)
 def test_source_not_mutated(self):
  import copy
  for c in cases():
   old=copy.deepcopy(c['events']);resolve(c['events'],c['target']);self.assertEqual(old,c['events'])
if __name__=='__main__':unittest.main()
