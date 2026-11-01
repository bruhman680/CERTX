import unittest
from task import normalized_visible,render,decode_action,observed_rule,finish_route

C={'target':'Juniper','visible_display':'[plot=Juniper; status=positive]','archive_available':True,
   'source':'Target plot: Juniper\n\nRecord 1:\nPlot: Juniper\nStatus: positive\n\nRecord 2:\nPlot: Hemlock\nStatus: zero'}

class StudyTests(unittest.TestCase):
    def test_hidden_key_and_source_not_in_prompt(self):
        d={**C,'state':'missing','kind':'unavailable','source':'hidden changed'}
        self.assertEqual(render(C,False,'direct8'),render(d,False,'direct8'))

    def test_direct_caps_do_not_change_prompt(self):
        self.assertEqual(render(C,True,'direct8'),render(C,True,'direct64'))

    def test_plan_and_examples_independent(self):
        self.assertNotIn('Worked examples',render(C,False,'plan64'))
        self.assertIn('Worked examples',render(C,True,'direct8'))
        self.assertNotIn('action plan first',render(C,True,'direct8'))

    def test_normalization_preserves_visible_roles(self):
        self.assertEqual(normalized_visible(C),'Plot: Juniper\nStatus: positive')
        self.assertEqual(observed_rule(C),'YES')
        bad={**C,'visible_display':'[plot=Hemlock; status=zero]'}
        self.assertEqual(observed_rule(bad),'TARGET')

    def test_final_declaration_and_fallback_separate(self):
        d=decode_action('A brief plan.\nACTION: NO\nACTION: TARGET')
        self.assertEqual(d['action'],'TARGET');self.assertEqual(d['tag_count'],2)
        self.assertEqual(decode_action('YES, brief text')['method'],'leading_word')
        self.assertIsNone(decode_action('I might request TARGET')['action'])

    def test_unknown_not_semantic_missing(self):
        c={**C,'visible_display':None,'archive_available':False}
        self.assertTrue(finish_route(c,'UNKNOWN')['justified_unknown'])
        self.assertFalse(finish_route(c,'WITHHOLD')['grounded_answer'])

if __name__=='__main__':unittest.main()
