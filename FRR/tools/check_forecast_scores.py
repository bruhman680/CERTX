"""Known-answer software fixtures only; these are not agent measurements."""
import unittest

from forecast_scores import score_forecasts


class ForecastScoreChecks(unittest.TestCase):
    def test_brier_can_improve_without_reliability_improving(self):
        base = score_forecasts([.5, .5, .5, .5], [0, 1, 0, 1])
        perfect = score_forecasts([0., 1., 0., 1.], [0, 1, 0, 1])
        self.assertAlmostEqual(base['brier_loss'], .25)
        self.assertAlmostEqual(perfect['brier_loss'], 0.)
        self.assertAlmostEqual(base['empirical_reliability_exact_groups'], 0.)
        self.assertAlmostEqual(perfect['empirical_reliability_exact_groups'], 0.)
        self.assertAlmostEqual(perfect['empirical_resolution_exact_groups'], .25)

    def test_wrong_confident_forecasts(self):
        value = score_forecasts([.9, .1, .9, .1], [0, 1, 0, 1])
        self.assertAlmostEqual(value['brier_loss'], .81)
        self.assertAlmostEqual(value['empirical_reliability_exact_groups'], .81)

    def test_decomposition_uses_exact_forecast_groups(self):
        value = score_forecasts([.2, .2, .7, .7, .7], [0, 1, 1, 0, 1])
        self.assertAlmostEqual(value['decomposition_error'], 0., places=14)
        self.assertEqual([g['count'] for g in value['exact_probability_groups']], [2, 3])

    def test_invalid_data_is_rejected(self):
        for probability in [float('nan'), float('inf'), -.01, 1.01, True, '0.5']:
            with self.subTest(probability=probability), self.assertRaises(ValueError):
                score_forecasts([probability], [1])
        for outcomes in [[2], [True], ['1']]:
            with self.subTest(outcomes=outcomes), self.assertRaises(ValueError):
                score_forecasts([.5], outcomes)
        for probabilities, outcomes in [([], []), ([.5], []), ([.5], [0, 1])]:
            with self.subTest(size=(len(probabilities), len(outcomes))), self.assertRaises(ValueError):
                score_forecasts(probabilities, outcomes)


if __name__ == '__main__':
    unittest.main(verbosity=2)
