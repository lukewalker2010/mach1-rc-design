import unittest

from tools import ab_cooling


class CoolingTests(unittest.TestCase):
    def test_per_hole_flow_matches_doc17_reference(self):
        # Doc 17 quotes 2.47e-4 kg/s for a choked 1 mm hole at 2 bar / 423 K.
        self.assertAlmostEqual(ab_cooling.choked_hole_flow(), 2.47e-4, places=6)

    def test_schedule_bleed_inside_band(self):
        data = ab_cooling.summarize()
        self.assertTrue(data["within_band"], data)
        self.assertGreaterEqual(data["bleed_fraction"], ab_cooling.BLEED_MIN)
        self.assertLessEqual(data["bleed_fraction"], ab_cooling.BLEED_MAX)

    def test_hole_count_scales_with_corrected_flow(self):
        # At 1.10 kg/s the 2.3-3.0% band needs roughly 102-134 holes, not 65.
        data = ab_cooling.summarize()
        self.assertAlmostEqual(data["holes_for_2.3pct"], 102.4, delta=1.0)
        self.assertAlmostEqual(data["holes_for_3.0pct"], 133.6, delta=1.5)

    def test_schedule_totals(self):
        self.assertEqual(sum(ab_cooling.ROW_HOLES), 112)
        self.assertEqual(len(ab_cooling.ROW_X_MM), len(ab_cooling.ROW_HOLES))


if __name__ == "__main__":
    unittest.main()
