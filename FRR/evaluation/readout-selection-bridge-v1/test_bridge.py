import unittest
from bridge import parse

class BridgeTests(unittest.TestCase):
    def test_target_selection_changes_with_header_not_position(self):
        body = '\n\nRecord 1:\nPlot: Oak\nStatus: positive\n\nRecord 2:\nPlot: Beech\nStatus: missing'
        self.assertEqual(parse('Target plot: Oak'+body)['crop'], 'Plot: Oak\nStatus: positive')
        self.assertEqual(parse('Target plot: Beech'+body)['crop'], 'Plot: Beech\nStatus: missing')

    def test_duplicate_target_rejected(self):
        with self.assertRaises(ValueError):
            parse('Target plot: Oak\n\nRecord 1:\nPlot: Oak\nStatus: positive\n\nRecord 2:\nPlot: Oak\nStatus: missing')

    def test_unrecognized_grammar_rejected(self):
        with self.assertRaises(ValueError):
            parse('Target plot: Oak; status=positive')

if __name__ == '__main__':
    unittest.main()
