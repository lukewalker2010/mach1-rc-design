import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.airdata import pitot_ratio
from tools.design_checks import ROOT


class CommandLineTests(unittest.TestCase):
    def test_strict_design_failure_is_machine_readable(self):
        run = subprocess.run([sys.executable, str(ROOT / "tools/design_checks.py"), "--strict", "--json"],
                             cwd=tempfile.gettempdir(), text=True, capture_output=True)
        self.assertEqual(run.returncode, 1, run.stderr)
        report = json.loads(run.stdout)
        self.assertTrue(any(not c["passed"] for c in report["checks"]))

    def test_flight_csv_report_and_raw_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "flight.csv"
            with path.open("w", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(["sample_id", "t_s", "static_pa", "impact_pa", "probe_temp_k", "valid"])
                for i in range(251):
                    writer.writerow([i, i / 50, 69700, 69700 * (pitot_ratio(1.1) - 1), 330, 1])
            command = [sys.executable, str(ROOT / "tools/flight_log_check.py"), str(path),
                       "--static-uncertainty-pa", "100", "--impact-uncertainty-pa", "100",
                       "--static-min-pa", "20000", "--static-max-pa", "110000",
                       "--impact-max-pa", "150000", "--recovery-factor", "0.98"]
            run = subprocess.run(command, cwd=folder, text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            report = json.loads(run.stdout)
            self.assertEqual(report["status"], "CANDIDATE")
            self.assertEqual(report["input_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            # Wrong sensor range must reject, rather than accepting clipped data.
            command[command.index("150000")] = "3447"
            run = subprocess.run(command, cwd=folder, text=True, capture_output=True)
            self.assertEqual(run.returncode, 1, run.stderr)
            path.write_text("wrong,header\n1,2\n")
            run = subprocess.run(command, cwd=folder, text=True, capture_output=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn("Input error", run.stderr)


if __name__ == "__main__":
    unittest.main()
