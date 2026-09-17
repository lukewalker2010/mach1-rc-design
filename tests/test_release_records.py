"""Synthetic temp records exercise integrity, never represent measured evidence."""

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from tools import release_records_check as records


class ReleaseRecordsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / "records"
        self.directory.mkdir()
        # Read-only reuse of existing Git objects; no commits or repository edits.
        git_dir = records.git(records.ROOT, "rev-parse", "--absolute-git-dir").decode().strip()
        (self.root / ".git").write_text(f"gitdir: {git_dir}\n")
        commit = records.git(records.ROOT, "rev-parse", "HEAD").decode().strip()
        artifact = records.git(records.ROOT, "show", f"{commit}:27_manufacturing_release.md")
        (self.root / "27_manufacturing_release.md").write_bytes(artifact)
        evidence = self.root / "synthetic.txt"
        evidence.write_text("SYNTHETIC TEST FIXTURE: no physical measurement or approval\n")
        self.part = dict(zip(records.REQUIRED_COLUMNS["part_release.csv"], [
            "P1", "A", "SER1", "ASSEMBLY", commit, "27_manufacturing_release.md",
            hashlib.sha256(artifact).hexdigest(), "synthetic.txt", "synthetic.txt", "PROC-A",
            "I-01;I-03", "synthetic.txt", "1", "1.2", "RELEASED", "FAKE-REVIEWER", "2026-01-01"]))
        self.build = dict(zip(records.REQUIRED_COLUMNS["build_traveller.csv"], [
            "P1", "A", "SER1", "OP1", "PROC-A", "LOT", "FAKE-OPERATOR", "2026-01-01T12:00:00Z",
            "SYNTHETIC ONLY", "text", "synthetic.txt", "synthetic.txt", "FAKE-INSPECTOR", "RELEASED", ""]))
        self.test = dict(zip(records.REQUIRED_COLUMNS["test_results.csv"], [
            "TEST1", "BENCH", commit, "SER1", "synthetic.txt", "synthetic.txt", "synthetic.txt",
            records.sha_file(evidence), "not executed", commit, "PASS", "synthetic.txt",
            "synthetic.txt", "FAKE-REVIEWER", "2026-01-01", "NONE"]))
        self.write_all()

    def write(self, name, rows, headers=None):
        with (self.directory / name).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=headers or records.REQUIRED_COLUMNS[name])
            writer.writeheader()
            writer.writerows(rows)

    def write_all(self):
        for name, row in zip(records.REQUIRED_COLUMNS, (self.part, self.build, self.test)):
            self.write(name, [row])

    def report(self):
        return records.validate_all(self.directory, self.root)

    def test_synthetic_checksums_and_fake_signatures_never_qualify(self):
        result = self.report()
        self.assertEqual(result.status, "CONSISTENT_UNVERIFIED", result)
        self.assertIn("cannot authenticate", result.qualification)
        self.assertTrue(all(f.disposition != "RELEASED" for f in result.files))

    def test_actual_headers_and_empty_templates(self):
        for name, columns in records.REQUIRED_COLUMNS.items():
            with (records.ROOT / "records" / name).open() as stream:
                self.assertEqual(next(csv.reader(stream)), columns)
            self.write(name, [])
        result = self.report()
        self.assertEqual(result.status, "INCOMPLETE")
        self.assertTrue(all(f.is_header_only for f in result.files))
        self.write("part_release.csv", [], ["wrong"])
        self.assertEqual(self.report().status, "INVALID")

    def test_paths_traversal_absolute_directories_and_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "secret"
            target.write_text("outside")
            (self.root / "escape").symlink_to(outside, target_is_directory=True)
            (self.root / "loop").symlink_to("loop")
            for path in (str(target), "../secret", "escape/secret", "records", "loop", "C:\\secret", "missing"):
                with self.subTest(path=path):
                    self.assertFalse(records.validate_path(path, self.root)[0])
            (self.directory / "part_release.csv").unlink()
            (self.directory / "part_release.csv").symlink_to(target)
            self.assertEqual(self.report().status, "INVALID")

    def test_invalid_fields_missing_nan_negative_enums_and_revisions(self):
        cases = [(self.part, "mass_kg", value) for value in ("", "NaN", "inf", "-1", "0")]
        cases += [(self.part, "cg_station_m", "NaN"), (self.part, "cg_station_m", "-1"),
                  (self.part, "revision", "A/../B"), (self.part, "disposition", "APPROVED"),
                  (self.part, "date", "2026-02-30"), (self.part, "date", "2999-01-01"),
                  (self.part, "source_commit", "0"*40), (self.part, "reviewer", ""),
                  (self.part, "interface_ids", "I-99"), (self.part, "material_certificate", "missing"),
                  (self.build, "measured_result", "NaN"), (self.build, "timestamp_utc", "2026-01-01"),
                  (self.test, "phase", "UNKNOWN"), (self.test, "result", "UNKNOWN"),
                  (self.test, "calibration_ids", "CAL-UNKNOWN"), (self.test, "analysis_commit", "missing")]
        for row, field, value in cases:
            old = row[field]
            with self.subTest(field=field, value=value):
                row[field] = value
                self.write_all()
                self.assertEqual(self.report().status, "INVALID")
            row[field] = old

    def test_hash_content_and_git_artifact_provenance(self):
        self.test["raw_data_sha256"] = "0"*64
        self.write_all()
        self.assertEqual(self.report().status, "INVALID")
        self.test["raw_data_sha256"] = records.sha_file(self.root / "synthetic.txt")
        artifact = self.root / self.part["artifact_path"]
        artifact.write_text("SYNTHETIC MODIFIED ARTIFACT")
        self.part["artifact_sha256"] = records.sha_file(artifact)
        self.write_all()
        result = self.report()
        self.assertEqual(result.status, "INVALID")
        self.assertTrue(any("differs from source commit" in e for f in result.files for e in f.errors))

    def test_join_revision_serial_duplicates_and_missing_coverage(self):
        self.build["revision"] = "B"
        self.write_all()
        self.assertEqual(self.report().status, "INVALID")
        self.build["revision"] = "A"
        self.test["hardware_serials"] = "UNKNOWN"
        self.write_all()
        self.assertEqual(self.report().status, "INVALID")
        self.test["hardware_serials"] = "SER1"
        self.write_all()
        self.write("part_release.csv", [self.part, self.part])
        self.assertEqual(self.report().status, "INVALID")
        self.write_all()
        self.write("build_traveller.csv", [])
        self.assertEqual(self.report().status, "INCOMPLETE")

    def test_failed_or_not_run_tests_are_not_release(self):
        for state in ("FAIL", "NOT RUN", "INCOMPLETE", "CONDITIONAL"):
            with self.subTest(state=state):
                self.test["result"] = state
                self.write_all()
                self.assertEqual(self.report().status, "INCOMPLETE")

    def test_malformed_row_width_and_missing_file(self):
        path = self.directory / "part_release.csv"
        with path.open("a") as stream:
            stream.write("one,two\n")
        self.assertEqual(self.report().status, "INVALID")
        path.unlink()
        self.assertEqual(self.report().status, "INVALID")


if __name__ == "__main__":
    unittest.main()
