import math
import unittest

from tools.airdata import airdata, mach_from_pressures, pitot_ratio


class AirDataTests(unittest.TestCase):
    def test_reference_ratios(self):
        self.assertEqual(pitot_ratio(0), 1)
        self.assertAlmostEqual(pitot_ratio(1), 1.8929291587, places=9)
        # M=2 normal shock: p2/p1=4.5, M2²=1/3; independent textbook state.
        self.assertAlmostEqual(pitot_ratio(2), 4.5 * (16/15)**3.5, places=10)
        self.assertLess(pitot_ratio(2), (1 + 0.2 * 4)**3.5)

    def test_sonic_continuity_and_round_trip(self):
        self.assertAlmostEqual(pitot_ratio(1 - 1e-9), pitot_ratio(1 + 1e-9), places=7)
        for mach in (0, 0.1, 0.8, 0.9999, 1, 1.0001, 1.1, 1.2, 2, 3):
            self.assertAlmostEqual(mach_from_pressures(69700, 69700 * (pitot_ratio(mach) - 1)), mach, places=10)

    def test_recovery_temperature(self):
        data = airdata(69700, 69700 * (pitot_ratio(1.1) - 1), 268.3 * (1 + 0.98 * 0.2 * 1.1**2), 0.98)
        self.assertAlmostEqual(data["static_temp_k"], 268.3)
        self.assertAlmostEqual(data["tas_m_s"], 1.1 * math.sqrt(1.4 * 287.05 * 268.3))

    def test_reject_invalid_inputs(self):
        for p, qc in [(0, 1), (-1, 1), (1, -1), (math.nan, 1), (1, math.inf), (1, 1000)]:
            with self.assertRaises(ValueError):
                mach_from_pressures(p, qc)
        for recovery in (0, -1, 1.01, math.nan):
            with self.assertRaises(ValueError):
                airdata(69700, 50000, 320, recovery)


if __name__ == "__main__":
    unittest.main()
