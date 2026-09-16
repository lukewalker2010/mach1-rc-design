import unittest

from tools.airdata import pitot_ratio
from tools.flight_log_check import evaluate

CONFIG = dict(static_uncertainty_pa=100, impact_uncertainty_pa=100,
              static_min_pa=20000, static_max_pa=110000, impact_max_pa=150000,
              recovery_factor=0.98)


def samples(n=251, mach=1.1):
    return [dict(sample_id=str(i), t_s=str(i / 50), static_pa="69700",
                 impact_pa=str(69700 * (pitot_ratio(mach) - 1)), probe_temp_k="330", valid="1")
            for i in range(n)]


class FlightLogTests(unittest.TestCase):
    def test_duration_is_time_not_sample_count(self):
        self.assertEqual(evaluate(samples(250), **CONFIG)["status"], "INSUFFICIENT")
        report = evaluate(samples(), **CONFIG)
        self.assertEqual(report["status"], "CANDIDATE")
        self.assertAlmostEqual(report["longest_window_s"], 5)

    def test_missing_invalid_and_saturated_samples_break_window(self):
        rows = samples()
        del rows[125]
        self.assertEqual(evaluate(rows, **CONFIG)["status"], "INSUFFICIENT")
        for field, value in [("valid", "0"), ("impact_pa", "150000"),
                             ("impact_pa", "nan"), ("static_pa", "0"), ("probe_temp_k", "-1")]:
            rows = samples()
            rows[125][field] = value
            self.assertEqual(evaluate(rows, **CONFIG)["status"], "INSUFFICIENT")

    def test_dropped_sequence_breaks_window_even_with_regular_clock(self):
        rows = samples()
        for i in range(125, len(rows)):
            rows[i]["sample_id"] = str(i + 1)
        self.assertEqual(evaluate(rows, **CONFIG)["status"], "INSUFFICIENT")

    def test_uncertainty_prevents_marginal_record_claim(self):
        self.assertEqual(evaluate(samples(mach=1.0001), **CONFIG)["status"], "INSUFFICIENT")

    def test_duplicate_or_reset_clock_rejected(self):
        for field in ("sample_id", "t_s"):
            rows = samples()
            rows[125][field] = rows[124][field]
            with self.assertRaises(ValueError):
                evaluate(rows, **CONFIG)

    def test_empty_and_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([], **CONFIG)
        with self.assertRaises(ValueError):
            evaluate(samples(), **(CONFIG | {"impact_uncertainty_pa": 0}))


if __name__ == "__main__":
    unittest.main()
