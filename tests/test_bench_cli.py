"""Real subprocess CLI integration. Fixtures are synthetic, never physical evidence."""
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_bench_pipeline import acquisition, calibration, event

ROOT = Path(__file__).resolve().parents[1]


class BenchCLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def cli(self, tool, *args):
        result = subprocess.run([sys.executable, str(ROOT / "tools" / tool), *map(str, args)],
                                capture_output=True, text=True, timeout=30)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def write_rows(self, name, rows):
        path = self.dir / name
        fields = sorted({k for row in rows for k in row})
        with path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def pipeline(self, rows):
        source = self.write_rows("input.csv", rows)
        archive = self.dir / "archive.csv"
        ingest = self.cli("daq_bench.py", source, "-o", archive)
        self.assertIn(ingest.returncode, (0, 1), ingest.stderr)
        post = self.cli("post_bench.py", archive, "--gate-start-s", 0,
                        "--min-thrust-N", 700, "--thrust-uncertainty-N", 10,
                        "--max-temp-K", 1000, "--temp-uncertainty-K", 10, "--temp-rate-hz", 10)
        self.assertIn(post.returncode, (0, 1), post.stderr)
        report = json.loads(post.stdout)
        self.assertFalse(report["physical_qualified"])
        return json.loads(ingest.stdout), report

    def test_twenty_seconds_equal_multichannel_timestamps_simulated(self):
        ingested, post = self.pipeline(acquisition())
        self.assertEqual(ingested["rejected_count"], 0)
        self.assertEqual(post["status"], "NONPHYSICAL")
        self.assertTrue(post["numerical_checks_ok"])
        self.assertEqual(post["thrust"]["sample_count"], 10001)
        self.assertEqual(post["temperature"]["sample_count"], 201)

    def test_zero_thrust(self):
        rows = acquisition()
        for r in rows:
            if r["channel"] == "THRUST_N":
                r["value"] = "-0"
        _, post = self.pipeline(rows)
        self.assertEqual(post["status"], "FAIL")
        self.assertIn("threshold", str(post["thrust"]["issues"]))

    def test_wrong_units(self):
        rows = acquisition()
        for r in rows:
            if r["channel"] == "THRUST_N":
                r["unit"] = "V"
        _, post = self.pipeline(rows)
        self.assertIn("expected unit N", str(post["thrust"]["issues"]))
        self.assertEqual(post["status"], "FAIL")

    def test_source_reset_and_invalid_sample_preserved(self):
        rows = acquisition()
        rows[100]["sample_id"] = "0"
        rows[200]["valid"] = "0"
        rows[200]["value"] = "nan"
        ingested, post = self.pipeline(rows)
        self.assertEqual(ingested["records_count"], len(rows))
        self.assertGreater(ingested["rejected_count"], 0)
        with (self.dir / "archive.csv").open() as stream:
            archived = list(csv.DictReader(stream))
        self.assertEqual(archived[200]["value"], "nan")
        self.assertEqual(archived[200]["ingest_valid"], "0")
        self.assertEqual(post["status"], "FAIL")

    def test_missing_first_temperature(self):
        _, post = self.pipeline([r for r in acquisition() if not (r["channel"] == "TEMP_K" and r["sample_id"] == "0")])
        self.assertIn("endpoint", str(post["temperature"]["issues"]))
        self.assertEqual(post["status"], "FAIL")

    def test_missing_last_temperature(self):
        _, post = self.pipeline([r for r in acquisition() if not (r["channel"] == "TEMP_K" and r["sample_id"] == "200")])
        self.assertIn("endpoint", str(post["temperature"]["issues"]))
        self.assertEqual(post["status"], "FAIL")

    def test_19_998_seconds_is_not_twenty(self):
        _, post = self.pipeline(acquisition(19.998))
        self.assertEqual(post["status"], "FAIL")
        self.assertIn("endpoint", str(post["thrust"]["issues"]))

    def test_raw_temperature_spike_plus_uncertainty(self):
        rows = acquisition()
        next(r for r in rows if r["channel"] == "TEMP_K" and r["sample_id"] == "100")["value"] = "995"
        _, post = self.pipeline(rows)
        self.assertEqual(post["temperature"]["max_upper_bound_K"], 1005)
        self.assertEqual(post["status"], "FAIL")

    def test_500hz_required_not_50hz(self):
        rows = acquisition()
        rows = [r for r in rows if r["channel"] == "TEMP_K" or int(r["sample_id"]) % 10 == 0]
        for r in rows:
            if r["channel"] == "THRUST_N":
                r["sample_id"] = str(int(r["sample_id"]) // 10)
        _, post = self.pipeline(rows)
        self.assertTrue(post["thrust"]["gaps"])
        self.assertEqual(post["status"], "FAIL")

    def test_no_clobber_same_input_or_existing_output(self):
        path = self.write_rows("input.csv", [event()])
        before = path.read_bytes()
        result = self.cli("daq_bench.py", path, "-o", path)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(path.read_bytes(), before)
        other = self.dir / "existing.csv"
        other.write_text("keep this user data")
        self.assertEqual(self.cli("daq_bench.py", path, "-o", other).returncode, 2)
        self.assertEqual(other.read_text(), "keep this user data")

    def test_poisoned_archive_metadata_hash(self):
        source = self.write_rows("input.csv", [event(i) for i in range(3)])
        archive = self.dir / "archive.csv"
        self.assertEqual(self.cli("daq_bench.py", source, "-o", archive).returncode, 0)
        with archive.open() as stream:
            rows = list(csv.DictReader(stream))
        rows[1]["config_hash"] = "c" * 64
        poisoned = self.write_rows("poisoned.csv", rows)
        result = self.cli("log_pair_check.py", archive, poisoned)
        self.assertEqual(result.returncode, 1)
        self.assertIn("record_hash mismatch", str(json.loads(result.stdout)["issues"]))

    def test_calibration_cli_force_metrics_and_analysis_only(self):
        path = self.write_rows("cal.csv", calibration(-.01))
        result = self.cli("cal_bench.py", path)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "ANALYSIS_ONLY")
        self.assertAlmostEqual(report["inverse_slope_N_per_V"], -100)
        limited = self.cli("cal_bench.py", path, "--max-residual-N", 1, "--max-hysteresis-N", 1,
                           "--max-repeatability-N", 1, "--max-heldout-N", 1,
                           "--min-load-N", 0, "--max-load-N", 200)
        self.assertEqual(limited.returncode, 0, limited.stderr)
        report = json.loads(limited.stdout)
        self.assertEqual(report["status"], "METRICS_WITHIN_LIMITS")
        self.assertFalse(report["physical_qualified"])

    def test_pair_cli_same_test_config_shared_calibration_and_mismatch(self):
        cal = self.dir / "calibration.json"
        cal.write_text(json.dumps({"sensor_ids": ["SA", "SB"], "scope": "SYNTHETIC TEST DOCUMENT"}))
        digest = hashlib.sha256(cal.read_bytes()).hexdigest()
        archives = []
        for suffix in ("A", "B"):
            rows = [event(i, source_type="BENCH", source_id="ADC" + suffix,
                          logger_id="LOGGER" + suffix, sensor_id="S" + suffix,
                          cal_sensor_id="S" + suffix, acquisition_path="PATH" + suffix,
                          cal_hash=digest) for i in range(4)]
            source = self.write_rows(suffix + ".csv", rows)
            archive = self.dir / (suffix + "_archive.csv")
            self.assertEqual(self.cli("daq_bench.py", source, "-o", archive).returncode, 0)
            archives.append(archive)
        args = [*archives, "--calibration-record", cal, "--clock-offset-s", 0,
                "--clock-uncertainty-s", .0001, "--alignment-tolerance-s", .001,
                "--clock-calibration-ref", "synthetic model"]
        result = self.cli("log_pair_check.py", *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "CONSISTENCY_CANDIDATE")
        self.assertFalse(report["independence_proven"])
        self.assertFalse(report["physical_qualified"])
        rows = [dict(r, test_id="different-test") for r in rows]
        source = self.write_rows("different.csv", rows)
        archive = self.dir / "different_archive.csv"
        self.assertEqual(self.cli("daq_bench.py", source, "-o", archive).returncode, 0)
        args[1] = archive
        mismatch = self.cli("log_pair_check.py", *args)
        self.assertEqual(mismatch.returncode, 1)
        self.assertIn("test_id", str(json.loads(mismatch.stdout)["issues"]))

    def test_malformed_cli_errors_no_tracebacks(self):
        bad = self.dir / "bad.csv"
        bad.write_text('a,a\n1,2\n')
        for tool, args in (("daq_bench.py", [bad, "-o", self.dir / "out.csv"]),
                           ("cal_bench.py", [bad]), ("log_pair_check.py", [bad, bad]),
                           ("post_bench.py", [bad]), ("cal_bench.py", [self.dir / "missing.csv"])):
            with self.subTest(tool=tool):
                self.assertEqual(self.cli(tool, *args).returncode, 2)

    def test_invalid_numeric_options_and_json_output_no_clobber(self):
        cal = self.write_rows("cal.csv", calibration())
        self.assertEqual(self.cli("cal_bench.py", cal, "--max-residual-N", "nan").returncode, 2)
        output = self.dir / "analysis.json"
        output.write_text("existing review")
        self.assertEqual(self.cli("cal_bench.py", cal, "-o", output).returncode, 2)
        self.assertEqual(output.read_text(), "existing review")
        source = self.write_rows("input.csv", [event(i) for i in range(3)])
        archive = self.dir / "archive.csv"
        self.assertEqual(self.cli("daq_bench.py", source, "-o", archive).returncode, 0)
        self.assertEqual(self.cli("log_pair_check.py", archive, archive,
                                 "--clock-offset-s", "nan", "--clock-uncertainty-s", .1,
                                 "--alignment-tolerance-s", .2,
                                 "--clock-calibration-ref", "synthetic").returncode, 2)
        result = self.cli("post_bench.py", archive, "--gate-start-s", 0,
                          "--min-thrust-N", 700, "--thrust-uncertainty-N", 0,
                          "--max-temp-K", 1000, "--temp-uncertainty-K", 10, "--temp-rate-hz", 10)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
