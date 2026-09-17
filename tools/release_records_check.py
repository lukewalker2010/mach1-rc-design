#!/usr/bin/env python3
"""R16 record integrity checker, not an approval/authenticity or release authority.

Exact existing CSV schemas. Exit 0: structurally consistent, still UNVERIFIED;
1: incomplete evidence; 2: invalid input/integrity/join. No command in a CSV is run.
Conventions and unavoidable schema limitations: 35_manufacturing_rig.md.
"""

import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLUMNS = {
    "part_release.csv": "part_number revision serial_or_lot parent_assembly source_commit artifact_path artifact_sha256 drawing_path material_certificate process_revision interface_ids inspection_record mass_kg cg_station_m disposition reviewer date".split(),
    "build_traveller.csv": "part_number revision serial_or_lot operation_id instruction_revision material_lot operator timestamp_utc measured_result units acceptance_source evidence_path inspector disposition deviation_id".split(),
    "test_results.csv": "test_id phase configuration_commit hardware_serials test_card_path calibration_ids raw_data_path raw_data_sha256 analysis_command analysis_commit result uncertainty_record inspection_record reviewer date next_permitted_test".split(),
}
VALID_DISPOSITIONS = {"RELEASED", "CONDITIONAL", "REJECTED", "NOT RUN", "INCOMPLETE", "OPEN", "PENDING", "QUARANTINE"}
VALID_TEST_RESULTS = {"PASS", "FAIL", "NOT RUN", "INCOMPLETE", "CONDITIONAL"}
VALID_TEST_PHASES = {*(f"G{i}" for i in range(8)), "COUPON", "PROOF", "BENCH", "GROUND", "FLIGHT", "DEVELOPMENT"}
REVISION = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}\Z")
COMMIT = re.compile(r"[0-9a-f]{7,40}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
PATH_FIELDS = {"artifact_path", "drawing_path", "material_certificate", "inspection_record",
               "test_card_path", "evidence_path", "raw_data_path", "uncertainty_record",
               "acceptance_source"}


@dataclass
class FileCheck:
    filename: str
    exists: bool = False
    is_header_only: bool = False
    row_count: int = 0
    schema_ok: bool = False
    disposition: str = "INCOMPLETE"
    errors: list = field(default_factory=list)
    rows: list = field(default_factory=list, repr=False)


@dataclass
class ValidationReport:
    records_dir: str
    files: list
    summary: dict
    status: str
    qualification: str = "UNVERIFIED: hashes and names cannot authenticate approvals or measured evidence"


def confined_file(value, root):
    """Reject absolute, traversal, Windows forms, directories and symlink escape."""
    if not isinstance(value, str) or not value or "\\" in value or ":" in value or "\x00" in value:
        raise ValueError("invalid repository-relative path")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError("absolute/traversal path")
    try:
        target = (root / p).resolve(strict=True)
        target.relative_to(root.resolve(strict=True))
        if not target.is_file():
            raise ValueError("path must be a regular file")
    except (OSError, RuntimeError, ValueError) as exc:
        raise ValueError(f"missing/non-file/escaping evidence: {value}") from exc
    return target


def validate_path(value, root):
    try:
        confined_file(value, root)
        return True, "confined file exists"
    except ValueError as exc:
        return False, str(exc)


def validate_mass_cg(mass_str, cg_str):
    try:
        mass, cg = float(mass_str), float(cg_str)
        if not math.isfinite(mass) or mass <= 0 or not math.isfinite(cg) or cg < 0:
            raise ValueError()
    except (TypeError, ValueError, OverflowError):
        return False, "mass must be finite >0; global +X station finite >=0"
    return True, "numeric only; part CG is not an aircraft CG qualification"


def git(root, *args):
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                                timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("cannot verify Git provenance") from exc
    if result.returncode:
        raise ValueError("Git provenance object/path not found")
    return result.stdout


def commit_id(value, root):
    if not COMMIT.fullmatch(value):
        raise ValueError("commit must be 7-40 lowercase hex characters")
    return git(root, "rev-parse", "--verify", f"{value}^{{commit}}").decode().strip()


def sha_file(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def tokens(value):
    parts = value.split(";")
    if any(not p or p != p.strip() for p in parts) or len(set(parts)) != len(parts):
        raise ValueError("expected unique, nonblank semicolon-separated values")
    return parts


def validate_file(filepath, filename, root):
    check = FileCheck(filename)
    if filename not in REQUIRED_COLUMNS:
        check.disposition = "INVALID"
        check.errors.append("unknown schema")
        return check
    try:
        relative = filepath.absolute().relative_to(root.resolve()).as_posix()
        safe = confined_file(relative, root)
        check.exists = True
        with safe.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream, strict=True)
            check.rows = list(reader)
            check.schema_ok = reader.fieldnames == REQUIRED_COLUMNS[filename]
        if not check.schema_ok:
            raise ValueError("headers must exactly match existing schema (including order, no duplicates)")
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        check.errors.append(str(exc))
        check.disposition = "INVALID"
        return check
    check.row_count = len(check.rows)
    check.is_header_only = not check.rows
    if not check.rows:
        check.errors.append("header-only template: no physical or approval evidence")
        return check
    incomplete = False
    for i, raw in enumerate(check.rows, 2):
        def error(message):
            check.errors.append(f"line {i}: {message}")
        if None in raw or any(v is None for v in raw.values()):
            error("row width differs from header")
            continue
        row = {k: v.strip() for k, v in raw.items()}
        check.rows[i-2] = row
        optional = {"deviation_id"} if filename == "build_traveller.csv" else set()
        for key in REQUIRED_COLUMNS[filename]:
            if key not in optional and not row[key]:
                error(f"missing required {key}")
        state = row.get("disposition", row.get("result"))
        allowed = VALID_TEST_RESULTS if filename == "test_results.csv" else VALID_DISPOSITIONS
        if state not in allowed:
            error("unknown result/disposition enum")
        if state in {"NOT RUN", "INCOMPLETE", "OPEN", "PENDING", "CONDITIONAL", "QUARANTINE", "REJECTED", "FAIL"}:
            incomplete = True
        if "phase" in row and row["phase"] not in VALID_TEST_PHASES:
            error("unknown phase enum")
        for key in ("revision", "process_revision", "instruction_revision"):
            if key in row and not REVISION.fullmatch(row[key]):
                error(f"invalid {key}")
        for key in PATH_FIELDS & row.keys():
            ok, detail = validate_path(row[key], root)
            if not ok:
                error(f"{key}: {detail}")
        for key in ("source_commit", "configuration_commit", "analysis_commit"):
            if key in row:
                try:
                    commit_id(row[key], root)
                except ValueError as exc:
                    error(f"{key}: {exc}")
        if "date" in row:
            try:
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["date"]):
                    raise ValueError()
                if date.fromisoformat(row["date"]) > datetime.now(timezone.utc).date():
                    raise ValueError()
            except ValueError:
                error("invalid/future calendar date")
        if "timestamp_utc" in row:
            try:
                stamp = datetime.fromisoformat(row["timestamp_utc"].replace("Z", "+00:00"))
                if stamp.utcoffset() is None or stamp.utcoffset().total_seconds() != 0 or stamp > datetime.now(timezone.utc):
                    raise ValueError()
            except (ValueError, OverflowError):
                error("timestamp must be a real, nonfuture UTC datetime")
        for path_key, hash_key in (("artifact_path", "artifact_sha256"), ("raw_data_path", "raw_data_sha256")):
            if hash_key in row:
                try:
                    if not SHA256.fullmatch(row[hash_key]):
                        raise ValueError("invalid SHA-256 format")
                    if sha_file(confined_file(row[path_key], root)) != row[hash_key]:
                        raise ValueError("SHA-256 mismatch")
                except (OSError, ValueError) as exc:
                    error(f"{hash_key}: {exc}")
        if filename == "part_release.csv":
            ok, detail = validate_mass_cg(row["mass_kg"], row["cg_station_m"])
            if not ok:
                error(detail)
            try:
                if row["interface_ids"] != "NONE":
                    if any(v not in {f"I-{j:02d}" for j in range(1, 13)} for v in tokens(row["interface_ids"])):
                        raise ValueError("unknown interface ID")
                source = commit_id(row["source_commit"], root)
                confined_file(row["artifact_path"], root)
                blob = git(root, "show", f"{source}:{row['artifact_path']}")
                if hashlib.sha256(blob).hexdigest() != row["artifact_sha256"]:
                    raise ValueError("artifact differs from source commit")
            except ValueError as exc:
                error(str(exc))
        if filename == "test_results.csv":
            try:
                tokens(row["hardware_serials"])
                for certificate in tokens(row["calibration_ids"]):
                    confined_file(certificate, root)
            except ValueError as exc:
                error(f"hardware/calibration references: {exc}")
        if filename == "build_traveller.csv":
            # Measured result may be text (e.g. visual inspection). Numerical
            # NaN/Inf are never measurements. Signed readings can be legitimate.
            try:
                result = float(row["measured_result"])
                if not math.isfinite(result):
                    error("nonfinite measured result")
            except ValueError:
                pass
            if state in {"CONDITIONAL", "REJECTED", "QUARANTINE"} and not row["deviation_id"]:
                error("deviation disposition requires deviation_id")
    check.disposition = "INVALID" if check.errors else "INCOMPLETE" if incomplete else "CONSISTENT_UNVERIFIED"
    return check


def validate_all(records_dir=ROOT / "records", root=ROOT):
    root = Path(root).resolve()
    records_dir = Path(records_dir).absolute()
    files = [validate_file(records_dir / name, name, root) for name in REQUIRED_COLUMNS]
    parts, builds, tests = files

    def reject(check, message):
        check.errors.append(message)
        check.disposition = "INVALID"

    # Never attempt joins over malformed rows/schemas.
    if all(f.schema_ok and f.disposition != "INVALID" for f in files):
        key = lambda r: (r["part_number"], r["revision"], r["serial_or_lot"])
        part_map, serials = {}, {}
        for row in parts.rows:
            if key(row) in part_map:
                reject(parts, f"duplicate part/revision/serial: {key(row)}")
            part_map[key(row)] = row
            serials.setdefault(row["serial_or_lot"], []).append(row)
        operations, built, tested, test_ids = set(), set(), set(), set()
        for row in builds.rows:
            identity = (*key(row), row["operation_id"])
            if identity in operations:
                reject(builds, f"duplicate operation {identity}")
            operations.add(identity)
            if key(row) not in part_map:
                reject(builds, f"orphan/revision-mismatched traveller {key(row)}")
            elif row["disposition"] == "RELEASED":
                built.add(key(row))
        for row in tests.rows:
            if row["test_id"] in test_ids:
                reject(tests, f"duplicate test_id {row['test_id']}")
            test_ids.add(row["test_id"])
            for serial in tokens(row["hardware_serials"]):
                matches = serials.get(serial, [])
                if len(matches) != 1:
                    reject(tests, f"unknown/ambiguous hardware serial {serial}")
                    continue
                part = matches[0]
                try:
                    config = commit_id(row["configuration_commit"], root)
                    blob = git(root, "show", f"{config}:{part['artifact_path']}")
                    if hashlib.sha256(blob).hexdigest() != part["artifact_sha256"]:
                        raise ValueError("configuration artifact differs from joined part revision")
                except ValueError as exc:
                    reject(tests, str(exc))
                if row["result"] == "PASS":
                    tested.add(key(part))
        for row in parts.rows:
            if row["disposition"] == "RELEASED" and (key(row) not in built or key(row) not in tested):
                parts.disposition = "INCOMPLETE" if parts.disposition != "INVALID" else "INVALID"
                parts.errors.append(f"missing released traveller/passing test link for {key(row)}")
    status = ("INVALID" if any(f.disposition == "INVALID" for f in files) else
              "INCOMPLETE" if any(f.disposition == "INCOMPLETE" for f in files) else "CONSISTENT_UNVERIFIED")
    summary = {state: sum(f.disposition == state for f in files)
               for state in ("INVALID", "INCOMPLETE", "CONSISTENT_UNVERIFIED")}
    return ValidationReport(str(records_dir), files, summary, status)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records-dir", type=Path, default=ROOT / "records")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate_all(args.records_dir)
    if args.json:
        data = asdict(report)
        for check in data["files"]:
            check.pop("rows")
        print(json.dumps(data, indent=2, allow_nan=False))
    else:
        print(f"R16: {report.status}")
        for check in report.files:
            print(f"{check.filename}: {check.disposition}, {check.row_count} rows")
            for error in check.errors:
                print(f"  {error}")
        print(report.qualification)
    return {"CONSISTENT_UNVERIFIED": 0, "INCOMPLETE": 1, "INVALID": 2}[report.status]


if __name__ == "__main__":
    raise SystemExit(main())
