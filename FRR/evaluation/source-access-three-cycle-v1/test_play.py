import unittest
from play_tools import calculate,dispatch
import play
class Play(unittest.TestCase):
 def test_arithmetic_and_rejections(self):
  self.assertEqual(calculate('(2+3)*4/2'),10)
  for t in ('__import__("os")','2**99','True','1/0','999999999999999','[1]'):
   self.assertEqual(dispatch('TRY '+t,[],play.parent.dispatch)['kind'],'calculation_error')
 def test_notes_keep_unverified_status(self):
  n=dispatch('NOTE maybe a different route',[],play.parent.dispatch);self.assertEqual(n['status'],'unverified_model_note');self.assertEqual(dispatch('READ NOTES',[dict(host_result=n)],play.parent.dispatch)['notes'],['maybe a different route'])
  self.assertFalse(dispatch('ordinary wandering',[],play.parent.dispatch)['executed'])
 def test_optional_charter_and_same_journal(self):
  self.assertIn('Tools are optional',(play.R/'PLAY_CHARTER.md').read_text());self.assertEqual(play.Journal(play.ENV).state()[1].__len__(),51)
  self.assertIn('STABLE PLAY CHARTER',play.play_render([]));self.assertTrue(play.parent.dispatch('READ SETUP','tools_optional')['executed'])
if __name__=='__main__':unittest.main()
