import unittest
from routing import layout, router_prompt, simple_rule, retrieve, terminal

SOURCE='Target plot: Rowan\n\nRecord 1:\nPlot: Rowan\nStatus: positive\n\nRecord 2:\nPlot: Aspen\nStatus: zero'
CASE={'target':'Rowan','visible':None,'archive_available':True,'source':SOURCE,'state':'positive','kind':'none_available'}

class ChoiceTests(unittest.TestCase):
    def test_hidden_state_and_kind_do_not_enter_action_prompt_or_rule(self):
        altered={**CASE,'state':'missing','source':'hidden alternative source','kind':'other','id':'gold'}
        self.assertEqual(router_prompt(CASE,layout('direct','forward')),router_prompt(altered,layout('direct','forward')))
        self.assertEqual(simple_rule(CASE),simple_rule(altered))

    def test_no_source_wins_unknown_not_semantic_missing(self):
        c={**CASE,'archive_available':False}
        self.assertTrue(terminal(c,'UNKNOWN')['justified_unknown'])
        self.assertFalse(terminal(c,'WITHHOLD')['grounded_answer'])
        self.assertEqual(terminal(c,'WITHHOLD')['final_state'],'missing')

    def test_invalid_free_action_is_not_coerced(self):
        result=terminal(CASE,None)
        self.assertEqual(result['end'],'INVALID_ACTION')
        self.assertFalse(result['requested'])

    def test_model_may_request_unavailable_tool_and_trace_survives(self):
        c={**CASE,'archive_available':False};tool=retrieve(c,'FULL')
        r=terminal(c,'FULL',tool=tool)
        self.assertTrue(r['unavailable_request']);self.assertEqual(r['nominal_tool_cost'],2)
        self.assertEqual(r['end'],'UNKNOWN_TOOL')

    def test_matching_label_on_wrong_visible_record_is_unsupported(self):
        c={**CASE,'visible':'Plot: Aspen\nStatus: zero'}
        r=terminal(c,'YES')
        self.assertTrue(r['class_correct']);self.assertFalse(r['grounded_answer'])
        self.assertEqual(r['receipt']['evidence'],'TARGET_MISMATCH')

    def test_rule_and_target_tool_use_visible_target_and_source_not_gold(self):
        c={**CASE,'state':'missing'}
        self.assertEqual(simple_rule(c),'TARGET')
        self.assertEqual(retrieve(c,'TARGET')['source'],'Plot: Rowan\nStatus: positive')
        self.assertEqual(simple_rule({**c,'visible':'Plot: Rowan\nStatus: positive'}),'YES')

    def test_code_assignment_and_display_order_are_separate(self):
        a=layout('direct','forward');b=layout('direct','reverse');c=layout('reverse','forward')
        self.assertEqual(a['mapping'],b['mapping'])
        self.assertNotEqual(a['display'],b['display'])
        self.assertNotEqual(a['mapping']['A'],c['mapping']['A'])

if __name__=='__main__':
    unittest.main()
