import unittest

from tools.power_budget import estimate, input_current


class PowerTests(unittest.TestCase):
    def test_energy_conservation_across_rails(self):
        current = input_current(12, 2.3, 6, 0.8)
        self.assertAlmostEqual(current * 6 * 0.8, 12 * 2.3)
        self.assertAlmostEqual(input_current(5, 1.7, 5, 1), 1.7)

    def test_declared_peak_includes_logic_and_pump_maximum(self):
        budget = estimate()
        self.assertAlmostEqual(budget["declared_peak_a"], 4 + 2 + 8.5 / (7.4 * 0.9) + 27.6 / (7.4 * 0.85))

    def test_invalid_efficiency(self):
        for efficiency in (0, -0.1, 1.1, float("nan")):
            with self.assertRaises(ValueError):
                input_current(12, 2, 7.4, efficiency)


if __name__ == "__main__":
    unittest.main()
