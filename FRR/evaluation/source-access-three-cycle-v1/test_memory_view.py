import unittest,json
import memory_view as m
import routine,capacity
class MemoryView(unittest.TestCase):
 def test_exact_tail_and_archive_preserved(self):
  events=routine.Journal(routine.ENV).state()[1];self.assertEqual(len(events),75);self.assertEqual(m.view_steps(events),list(range(63,75)))
  q=routine.view_render(events);self.assertIn('Earlier entries remain archived, not erased',q)
  self.assertEqual(routine.seed_render(events),capacity.seed_render(events))
 def test_older_exact_records_and_bounded_payload(self):
  events=routine.Journal(routine.ENV).state()[1];x=routine.view_dispatch('READ HISTORY 0 2',events);self.assertEqual(x['kind'],'history_receipt')
  for record,original in zip(x['records'],events[:2]):
   self.assertEqual(record['reply'],original['reply']);self.assertEqual(record['observation'],original['observation']);self.assertEqual(record['feedback'],original['feedback'])
  for command in ('READ HISTORY 0 75','READ HISTORY 9 8','READ HISTORY 74 77'):
   self.assertEqual(routine.view_dispatch(command,events)['kind'],'history_error')
  self.assertEqual(routine.view_dispatch('READ HISTORY 0 2; delete',events)['kind'],'record_receipt')
 def test_no_recursive_receipt_copy_and_unchanged_tools(self):
  events=[dict(step=0,observation='x',reply='READ HISTORY 0 1',feedback='y',host_result=dict(kind='history_receipt',executed=True,records=[dict(secret='not recursively copied')]))]
  x=routine.view_dispatch('READ HISTORY 0 1',events);self.assertTrue(x['records'][0]['full_host_result_omitted']);self.assertNotIn('records',x['records'][0]['host_result_projection'])
  self.assertEqual(routine.view_dispatch('TRY 2 + 3',[])['result'],5)
 def test_five_step_checks_required(self):
  m.require_checked(80,dict(next_step=80),dict(status='pass'),5)
  for cursor,latest,n in ((80,75,5),(80,80,6)):
   with self.assertRaises(AssertionError):m.require_checked(cursor,dict(next_step=latest),dict(status='pass'),n)
if __name__=='__main__':unittest.main()
