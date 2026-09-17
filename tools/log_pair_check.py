"""Offline concurrent-log consistency screen; metadata does not prove independence."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

if __package__:
    from .bench_schema import emit_json, load_events, number, validate_events
else:
    from bench_schema import emit_json, load_events, number, validate_events


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_log(path):
    records, raw = load_events(path)
    return records, raw, list(records[0]) if records else []


def check_timestamp_integrity(records, path_label):
    # The shared validator checks per(source/channel) sequence and source time.
    return [f"{path_label} line {c['line']}: {error}"
            for c in validate_events(records, require_hash=True) for error in c["errors"]]


def check_clock_alignment(records_a, records_b, *, offset_s=None, uncertainty_s=None,
                          tolerance_s=None, calibration_ref=None):
    supplied = [offset_s is not None, uncertainty_s is not None, tolerance_s is not None,
                bool(calibration_ref and calibration_ref.strip())]
    if not any(supplied):
        return {"status": "UNRESOLVED", "reason": "calibrated offset, absolute uncertainty, tolerance and reference required"}
    if not all(supplied):
        raise ValueError("supply all clock offset/uncertainty/tolerance/reference arguments")
    offset = number(offset_s, "clock offset")
    uncertainty = number(uncertainty_s, "clock uncertainty", positive=True)
    tolerance = number(tolerance_s, "alignment tolerance", positive=True)
    # Offset convention: A time = B time + offset. Each channel must cover the
    # common overlap; begin/end differences are never estimates of clock error.
    ranges = []
    for records, shift in ((records_a, 0), (records_b, offset)):
        channels = {}
        for row in records:
            try:
                t = number(row.get("timestamp_s"), "timestamp_s", nonnegative=True) + shift
            except ValueError:
                return {"status": "FAIL", "reason": "invalid source timestamp"}
            channels.setdefault((row.get("source_id"), row.get("channel")), []).append(t)
        ranges.extend((min(ts), max(ts)) for ts in channels.values())
    overlap = max(0.0, min(b for _, b in ranges) - max(a for a, _ in ranges) - 2 * uncertainty) if ranges else 0.0
    return {"status": "CONSISTENT" if overlap > 0 and uncertainty <= tolerance else "FAIL",
            "offset_s_B_to_A": offset, "uncertainty_s": uncertainty, "tolerance_s": tolerance,
            "conservative_common_overlap_s": overlap, "calibration_ref": calibration_ref,
            "scope": "Supplied calibrated offset model must bound residual clock/latency error across the entire run. Overlap is coverage, not clock calibration. No clock drift estimate or authenticity verification."}


def calibration_documents(paths):
    documents = {}
    for path in paths:
        raw = Path(path).read_bytes()
        doc = json.loads(raw)
        sensors = doc.get("sensor_ids") if isinstance(doc, dict) else None
        if not isinstance(sensors, list) or not sensors or any(not isinstance(s, str) or not s.strip() for s in sensors):
            raise ValueError("calibration document requires nonempty sensor_ids list")
        documents[hashlib.sha256(raw).hexdigest()] = set(sensors)
    return documents


def check_pair(a, b, *, raw_a=None, raw_b=None, calibration_evidence=None,
               clock_offset_s=None, clock_uncertainty_s=None, alignment_tolerance_s=None,
               clock_calibration_ref=None):
    issues, unresolved = [], []
    integrity_a = check_timestamp_integrity(a, "A")
    integrity_b = check_timestamp_integrity(b, "B")
    issues.extend(integrity_a + integrity_b)
    if not a or not b:
        issues.append("both logs must contain events")
    if a == b or (raw_a is not None and raw_b is not None and raw_a == raw_b):
        issues.append("identical file contents/records fail independence screen")
    for key in ("run_id", "test_id", "config_hash", "source_type"):
        av, bv = {r.get(key) for r in a}, {r.get(key) for r in b}
        if len(av) != 1 or av != bv or not all(av):
            issues.append(f"same constant {key} required in concurrent logs")
    for key in ("logger_id", "source_id", "sensor_id", "acquisition_path"):
        av, bv = {r.get(key) for r in a}, {r.get(key) for r in b}
        if not av or not bv or not all(av | bv) or av & bv:
            issues.append(f"missing or overlapping {key}; distinct acquisition paths required")
    types = {r.get("source_type") for r in a + b}
    if not types or not types <= {"BENCH", "FLIGHT"}:
        issues.append("nonphysical source provenance")
    if calibration_evidence is None:
        unresolved.append("sensor-specific calibration documents not supplied")
    else:
        for row in a + b:
            sensors = calibration_evidence.get(row.get("cal_hash"), set())
            if row.get("sensor_id") not in sensors:
                issues.append("calibration hash/document does not cover sensor " + str(row.get("sensor_id")))
        issues = list(dict.fromkeys(issues))
    alignment = check_clock_alignment(a, b, offset_s=clock_offset_s,
                                      uncertainty_s=clock_uncertainty_s,
                                      tolerance_s=alignment_tolerance_s,
                                      calibration_ref=clock_calibration_ref)
    if alignment["status"] == "UNRESOLVED":
        unresolved.append("clock alignment unresolved")
    elif alignment["status"] == "FAIL":
        issues.append("clock uncertainty/overlap screen failed")
    return {"status": "FAIL" if issues else "UNRESOLVED" if unresolved else "CONSISTENCY_CANDIDATE",
            "physical_qualified": False, "independence_proven": False,
            "issues": issues, "unresolved": unresolved, "alignment": alignment,
            "log_a": {"records": len(a), "sha256": hashlib.sha256(raw_a).hexdigest() if raw_a is not None else None},
            "log_b": {"records": len(b), "sha256": hashlib.sha256(raw_b).hexdigest() if raw_b is not None else None},
            "scope": "Concurrent metadata, integrity and supplied clock-model consistency only. Different hashes and IDs do not prove physical independence; shared valid calibration documents may cover both sensors. Config/calibration hashes are raw references, not authenticity or seal-custody verification. No clock drift, altitude-loss or mission qualification."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_a", type=Path)
    parser.add_argument("log_b", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--calibration-record", type=Path, action="append")
    parser.add_argument("--clock-offset-s", type=float)
    parser.add_argument("--clock-uncertainty-s", type=float)
    parser.add_argument("--alignment-tolerance-s", type=float)
    parser.add_argument("--clock-calibration-ref")
    args = parser.parse_args(argv)
    try:
        a, raw_a, _ = load_log(args.log_a)
        b, raw_b, _ = load_log(args.log_b)
        evidence = calibration_documents(args.calibration_record) if args.calibration_record else None
        result = check_pair(a, b, raw_a=raw_a, raw_b=raw_b, calibration_evidence=evidence,
                            clock_offset_s=args.clock_offset_s, clock_uncertainty_s=args.clock_uncertainty_s,
                            alignment_tolerance_s=args.alignment_tolerance_s,
                            clock_calibration_ref=args.clock_calibration_ref)
        emit_json(result, args.output)
        return 0 if result["status"] == "CONSISTENCY_CANDIDATE" else 1
    except (OSError, ValueError, UnicodeError, csv.Error, OverflowError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
