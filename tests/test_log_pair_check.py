"""Synthetic metadata-contract tests; candidates never assert physical independence."""
import unittest

from tools.daq_bench import ingest
from tools.log_pair_check import check_pair, check_clock_alignment
from tests.test_bench_pipeline import event


def pair(source_type="SIMULATED", **changes_b):
    a = [event(i, source_type=source_type) for i in range(4)]
    b = [event(i, source_type=source_type, source_id="ADC_B", logger_id="LOGGER_B",
               sensor_id="SENSOR_B", cal_sensor_id="SENSOR_B", acquisition_path="PATH_B",
               **changes_b) for i in range(4)]
    return ingest(a)["records"], ingest(b)["records"]


PAIR_ARGS = dict(calibration_evidence={"b" * 64: {"SENSOR_A_THRUST_N", "SENSOR_B"}},
                 clock_offset_s=0, clock_uncertainty_s=.0001, alignment_tolerance_s=.001,
                 clock_calibration_ref="synthetic clock-model exercise")


class PairTests(unittest.TestCase):
    def test_same_valid_test_config_and_shared_cal_document_are_correct(self):
        # Exercise claimed BENCH metadata, not a physical recording or pass.
        a, b = pair("BENCH")
        result = check_pair(a, b, **PAIR_ARGS)
        self.assertEqual(result["status"], "CONSISTENCY_CANDIDATE")
        self.assertFalse(result["independence_proven"])
        self.assertFalse(result["physical_qualified"])
        self.assertEqual(result["issues"], [])

    def test_simulated_pair_is_nonphysical(self):
        self.assertEqual(check_pair(*pair(), **PAIR_ARGS)["status"], "FAIL")

    def test_mismatched_run_test_and_config_fail(self):
        for key, value in (("run_id", "other"), ("test_id", "other"), ("config_hash", "c" * 64)):
            result = check_pair(*pair("BENCH", **{key: value}), **PAIR_ARGS)
            self.assertEqual(result["status"], "FAIL")
            self.assertIn(key, str(result["issues"]))

    def test_clock_overlap_is_not_alignment(self):
        a, b = pair("BENCH")
        self.assertEqual(check_clock_alignment(a, b)["status"], "UNRESOLVED")
        self.assertEqual(check_pair(a, b)["status"], "UNRESOLVED")
        result = check_pair(a, b, **dict(PAIR_ARGS, clock_uncertainty_s=.002))
        self.assertEqual(result["status"], "FAIL")

    def test_identical_records_shared_paths_missing_metadata_and_poison(self):
        a, b = pair("BENCH")
        self.assertEqual(check_pair(a, a, **PAIR_ARGS)["status"], "FAIL")
        for key, value in (("acquisition_path", "PATH_A_THRUST_N"),
                           ("logger_id", ""), ("sample_id", "0"),
                           ("test_id", "poison"), ("config_hash", "c" * 64)):
            altered = [dict(r) for r in b]
            altered[2][key] = value
            self.assertEqual(check_pair(a, altered, **PAIR_ARGS)["status"], "FAIL")

    def test_calibration_document_must_cover_each_sensor(self):
        args = dict(PAIR_ARGS, calibration_evidence={"b" * 64: {"SENSOR_A_THRUST_N"}})
        result = check_pair(*pair("BENCH"), **args)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("cover sensor", str(result["issues"]))


if __name__ == "__main__":
    unittest.main()
