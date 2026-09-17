"""Synthetic regression data only: no test result is physical qualification."""
import copy
import unittest

from tools.bench_schema import canonical_hash, validate_events
from tools.daq_bench import ingest
from tools.cal_bench import compute_metrics, fit_linear
from tools.post_bench import screen


def event(i=0, channel="THRUST_N", t=None, **updates):
    row = dict(source_id="ADC_A", channel=channel, sample_id=str(i),
               timestamp_s=str(i / 500 if t is None else t),
               value="800" if channel == "THRUST_N" else "900",
               unit="N" if channel == "THRUST_N" else "K", valid="1",
               source_type="SIMULATED", run_id="synthetic-run", test_id="synthetic-test",
               logger_id="LOGGER_A", sensor_id="SENSOR_A_" + channel,
               acquisition_path="PATH_A_" + channel, config_hash="a" * 64,
               cal_hash="b" * 64, cal_sensor_id="SENSOR_A_" + channel)
    row.update(updates)
    return row


def acquisition(end=20.0):
    rows = [event(i) for i in range(round(end * 500) + 1)]
    rows += [event(i, "TEMP_K", i / 10) for i in range(int(end * 10) + 1)]
    return sorted(rows, key=lambda r: float(r["timestamp_s"]))


def calibration(slope=0.01):
    return [dict(cycle=str(cycle), direction=direction, known_N=str(force),
                 measured_v=str(0.5 + slope * force), valid="1")
            for cycle in (1, 2, 3) for direction in ("ASC", "DESC")
            for force in ((0, 100, 200) if direction == "ASC" else (200, 100, 0))]


SCREEN_ARGS = dict(gate_start_s=0, min_thrust_N=700, thrust_uncertainty_N=10,
                   max_temp_K=1000, temp_uncertainty_K=10, temp_rate_hz=10)


class AcquisitionTests(unittest.TestCase):
    def test_equal_multichannel_times_and_interleaved_stale_source(self):
        rows = [event(0), event(0, "TEMP_K"), event(1), event(1, "TEMP_K")]
        self.assertEqual(ingest(rows)["rejected_count"], 0)
        rows.append(event(1))
        report = ingest(rows)
        self.assertEqual(report["records_count"], 5)
        self.assertIn("non-increasing", str(report["rejected"]))
        self.assertIn("sequence", str(report["rejected"]))

    def test_raw_invalid_preserved_and_hash_covers_every_field(self):
        rows = [event(0), event(1, valid="0", value="nan"), event(2)]
        report = ingest(rows)
        self.assertEqual(len(report["records"]), 3)
        self.assertEqual(report["records"][1]["value"], "nan")
        self.assertEqual(report["records"][1]["ingest_valid"], "0")
        row = report["records"][0]
        for field in row:
            if field == "record_hash":
                continue
            poisoned = dict(row, **{field: row[field] + "changed"})
            self.assertNotEqual(canonical_hash(poisoned), row["record_hash"], field)

    def test_unknown_source_missing_sequence_and_wrong_source_preserved(self):
        rows = [event(source_type="UNKNOWN", sample_id="")]
        report = ingest(rows, expected_source_id="OTHER")
        self.assertEqual(report["records_count"], 1)
        self.assertEqual(report["valid_count"], 0)
        self.assertIn("unexpected source", str(report["rejected"]))

    def test_source_sequence_reset_and_holes(self):
        for sequence in ("0", "5", ""):
            rows = [event(0), event(1), event(2, sample_id=sequence)]
            self.assertGreater(ingest(rows)["rejected_count"], 0)

    def test_hash_poison_cannot_be_laundered_by_ingestion(self):
        row = event()
        row["record_hash"] = canonical_hash(row)
        row["source_type"] = "BENCH"
        archived = ingest([row])["records"]
        self.assertIn("record_hash mismatch", archived[0]["ingest_errors"])
        self.assertTrue(validate_events(archived, require_hash=True)[0]["errors"])


class CalibrationTests(unittest.TestCase):
    def test_centred_fit_large_offset(self):
        x = [1e12 + i for i in range(5)]
        slope, intercept = fit_linear(x, [2 * i + 3 for i in range(5)])
        self.assertEqual(slope, 2)
        self.assertEqual(intercept, 3 - 2e12)

    def test_reversible_negative_sensitivity_and_analysis_only(self):
        for sensitivity in (0.01, -0.01):
            result = compute_metrics(calibration(sensitivity))
            self.assertEqual(result["status"], "ANALYSIS_ONLY")
            self.assertAlmostEqual(result["inverse_slope_N_per_V"], 1 / sensitivity)
            self.assertLess(result["metrics_N"]["max_residual_N"], 1e-10)
            self.assertFalse(result["physical_qualified"])

    def test_force_units_and_per_cycle_hysteresis_cannot_cancel(self):
        rows = calibration()
        for row in rows:
            if row["direction"] == "DESC":
                row["measured_v"] = str(float(row["measured_v"]) + (0.1 if row["cycle"] != "2" else -0.1))
        result = compute_metrics(rows, max_residual_N=20, max_hysteresis_N=5,
                                 max_repeatability_N=50, max_heldout_N=50,
                                 min_load_N=0, max_load_N=200)
        self.assertAlmostEqual(result["metrics_N"]["max_hysteresis_N"], 10)
        self.assertEqual(result["status"], "FAIL")

    def test_heldout_detects_cycle_shift(self):
        rows = calibration()
        for r in rows:
            if r["cycle"] == "3":
                r["measured_v"] = str(float(r["measured_v"]) + 0.2)
        result = compute_metrics(rows)
        self.assertAlmostEqual(result["metrics_N"]["max_heldout_N"], 20)
        self.assertAlmostEqual(result["metrics_N"]["max_repeatability_N"], 20)

    def test_invalid_protocols_rejected(self):
        base = calibration()
        cases = [calibration(0), base[:-1], list(reversed(base))]
        for key, value in (("valid", "0"), ("cycle", "4"), ("known_N", "50"),
                           ("measured_v", "nan"), ("unit", "counts")):
            rows = copy.deepcopy(base)
            rows[1][key] = value
            cases.append(rows)
        for rows in cases:
            with self.subTest(rows=rows[:2]), self.assertRaises(ValueError):
                compute_metrics(rows)

    def test_explicit_range_and_all_thresholds_required_for_decision(self):
        result = compute_metrics(calibration(), max_residual_N=1)
        self.assertEqual(result["status"], "ANALYSIS_ONLY")
        with self.assertRaises(ValueError):
            compute_metrics(calibration(), min_load_N=0, max_load_N=300)


class PostTests(unittest.TestCase):
    def short_records(self, **updates):
        rows = [event(i, t=i / 500, **updates) for i in range(3)]
        rows += [event(i, "TEMP_K", i / 500, **updates) for i in range(3)]
        return ingest(sorted(rows, key=lambda r: float(r["timestamp_s"])))["records"]

    def short_args(self, **updates):
        return dict(SCREEN_ARGS, duration_s=.004, duration_review="synthetic regression", **updates)

    def test_simulated_twenty_seconds_never_screen_pass(self):
        result = screen(ingest(acquisition())["records"], **SCREEN_ARGS)
        self.assertTrue(result["numerical_checks_ok"])
        self.assertEqual(result["status"], "NONPHYSICAL")
        self.assertFalse(result["physical_qualified"])

    def test_no_short_duration_or_lower_rate_waiver(self):
        with self.assertRaises(ValueError):
            screen([], **SCREEN_ARGS, duration_s=1)
        with self.assertRaises(ValueError):
            screen([], **SCREEN_ARGS, thrust_rate_hz=50)

    def test_time_weighting_not_arithmetic_mean(self):
        rows = [event(i, t=t, value=str(v)) for i, (t, v) in enumerate([(0, 800), (.001, 900), (.003, 1000)])]
        rows += [event(i, "TEMP_K", t, value="900") for i, t in enumerate((0, .001, .003))]
        args = dict(SCREEN_ARGS, duration_s=.003, duration_review="synthetic arithmetic test", temp_rate_hz=500)
        result = screen(ingest(sorted(rows, key=lambda r: float(r["timestamp_s"])))["records"], **args)
        self.assertAlmostEqual(result["thrust"]["time_weighted_lower_bound_N"], (800 + 2 * 900) / 3 - 10)

    def test_calibrated_clipping_and_single_temperature_sample_fail(self):
        records = self.short_records()
        result = screen(records, **self.short_args(thrust_min_N=0, thrust_max_N=800))
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("clipped", str(result["thrust"]["issues"]))
        one_temp = [r for r in records if r["channel"] != "TEMP_K" or r["sample_id"] == "1"]
        self.assertEqual(screen(one_temp, **self.short_args())["status"], "FAIL")

    def test_only_bench_declaration_eligible_and_never_qualification(self):
        for provenance in ("SIMULATED", "CALIBRATION", "FLIGHT", "UNKNOWN", "", "BENCH"):
            result = screen(self.short_records(source_type=provenance), **self.short_args())
            self.assertEqual(result["status"] == "SCREEN_PASS", provenance == "BENCH")
            self.assertFalse(result["physical_qualified"])

    def test_explicit_short_gate_and_missing_hash_fail(self):
        records = self.short_records()
        result = screen(records, **SCREEN_ARGS, gate_end_s=.004)
        self.assertFalse(result["duration_ok"])
        records[0].pop("record_hash")
        self.assertEqual(screen(records, **self.short_args())["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
