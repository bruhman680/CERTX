import unittest
from continue_block import decision
class Policy(unittest.TestCase):
 def session(self,**kw):return dict(stop_reason='curious_event_pause',weights_unchanged=True,training_updates=0,**kw)
 def test_validated_guest_error_continues(self):
  self.assertEqual(decision(self.session(host_status='REJECTED_VALIDATION'),{'status':'pass'}),'continue')
 def test_success_needs_no_researcher_approval(self):
  self.assertEqual(decision(self.session(host_status='PUBLISHED'),{'status':'pass'}),'continue')
 def test_integrity_failure_stops(self):
  self.assertEqual(decision(self.session(host_status='COMPUTED'),{'status':'fail'}),'stop_integrity')
 def test_operator_pause_respected(self):
  s=self.session();s['stop_reason']='pause_requested';self.assertEqual(decision(s,{'status':'pass'}),'stop_operator')
 def test_unknown_runtime_stop_retained(self):
  s=self.session();s['stop_reason']='interrupted_or_failed';self.assertEqual(decision(s,{'status':'pass'}),'stop_runtime')
if __name__=='__main__':unittest.main(verbosity=2)
