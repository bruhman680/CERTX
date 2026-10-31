import unittest
from evidence import parse, receipt, transition
from run_room import material

SOURCE = 'Target plot: Oak\n\nRecord 1:\nPlot: Oak\nStatus: positive\n\nRecord 2:\nPlot: Beech\nStatus: missing'

class RoomTests(unittest.TestCase):
    def test_bad_selection_remains_wrong_even_if_its_label_matches(self):
        p = parse(SOURCE)
        r = receipt(SOURCE, p['other_crop'], 'selected', 'positive')
        self.assertEqual(r['evidence'], 'TARGET_MISMATCH')
        self.assertEqual(r['label_consistency'], 'CONSISTENT')
        self.assertFalse(r['eligible_for_this_toy_acceptance'])

    def test_lucky_no_source_answer_is_not_grounded(self):
        self.assertFalse(receipt(SOURCE, 'unavailable', 'none', 'positive')['eligible_for_this_toy_acceptance'])

    def test_source_missing_state_is_not_uncertainty(self):
        missing = SOURCE.replace('Target plot: Oak', 'Target plot: Beech')
        self.assertTrue(receipt(missing, missing, 'full', 'missing')['eligible_for_this_toy_acceptance'])
        self.assertFalse(receipt(missing, 'unavailable', 'none', 'missing')['eligible_for_this_toy_acceptance'])

    def test_crop_with_changed_content_rejected(self):
        self.assertEqual(receipt(SOURCE, 'Plot: Oak\nStatus: zero', 'selected', 'zero')['evidence'], 'CONTENT_MISMATCH')

    def test_transition_accounts_for_regression_and_invalid(self):
        self.assertEqual(transition('zero', 'positive', 'positive'), 'wrong_to_correct')
        self.assertEqual(transition('positive', 'zero', 'positive'), 'correct_to_wrong')
        self.assertEqual(transition('zero', None, 'positive'), 'wrong_to_invalid')

    def test_crop_does_not_use_authored_gold_or_id(self):
        plan = {'mapping': {'positive': 'YES', 'zero': 'NO', 'missing': 'WITHHOLD'},
                'base_template': '{mapping}\n{source}', 'full_prefix': '',
                'proposal_prefix': 'Proposal:{proposal}\n', 'no_evidence_source': 'unavailable'}
        case = {'id': 'one', 'source': SOURCE, 'state': 'missing', 'cohort': 'fresh'}
        call = {'condition': 'baseline_selected', 'seed': 'none'}
        a, g, _ = material(case, call, plan)
        b, _, _ = material({**case, 'state': 'zero', 'id': 'two'}, call, plan)
        self.assertEqual(a['source'], b['source'])
        self.assertEqual(a['source'], 'Plot: Oak\nStatus: positive')
        self.assertEqual(a['state'], 'positive')

if __name__ == '__main__':
    unittest.main()
