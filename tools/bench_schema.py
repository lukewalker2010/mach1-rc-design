"""Shared offline acquisition-event schema; hashes are integrity, not authenticity."""
import csv
import hashlib
import io
import json
import math
import re
from pathlib import Path

FIELDS = ("source_id", "channel", "sample_id", "timestamp_s", "value", "unit",
          "valid", "source_type", "run_id", "test_id", "logger_id", "sensor_id",
          "acquisition_path", "config_hash", "cal_hash", "cal_sensor_id")
GLOBAL_METADATA = ("run_id", "test_id", "logger_id", "config_hash", "source_type")
CHANNEL_METADATA = ("sensor_id", "acquisition_path", "cal_hash", "cal_sensor_id", "unit")
SOURCE_TYPES = {"BENCH", "FLIGHT", "CALIBRATION", "SIMULATED"}
UNITS = {"N", "K", "Pa", "V", "kg", "kg/s", "m/s", "m", "s", "1", "A"}
EPS = 1e-9  # floating arithmetic tolerance only, never acquisition jitter allowance


def number(value, name, *, positive=False, nonnegative=False):
    try:
        result = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"{name} must be a finite number") from None
    if not math.isfinite(result) or (positive and result <= 0) or (nonnegative and result < 0):
        raise ValueError(f"{name} must be finite" + (" and positive" if positive else
                         " and nonnegative" if nonnegative else ""))
    return result


def canonical_hash(row):
    """Hash every CSV field except record_hash; sorted UTF-8 JSON, string values.

    Extra metadata and archive diagnostics are covered too. Delimiters cannot
    collide. This is not a signature and cannot authenticate a claimed source.
    """
    data = {str(k): str(v) for k, v in row.items() if k != "record_hash"}
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def read_csv(raw, required=()):
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")), strict=True)
    fields = reader.fieldnames
    if not fields or any(not f for f in fields) or len(fields) != len(set(fields)):
        raise ValueError("CSV needs a nonempty, unique header")
    if not set(required) <= set(fields):
        raise ValueError("missing CSV columns: " + ", ".join(sorted(set(required) - set(fields))))
    rows = []
    for row in reader:
        extra = row.pop(None, None)
        row = {k: v if v is not None else "" for k, v in row.items()}
        if extra is not None:
            row["extra_cells_json"] = json.dumps(extra)
        rows.append(row)
    return rows


def validate_events(rows, *, require_hash=False, max_gap_s=None, expected_source_id=None):
    """One result per input row; never filter, sort, repair or renumber events."""
    if max_gap_s is not None:
        max_gap_s = number(max_gap_s, "max_gap_s", positive=True)
    previous, metadata, global_metadata = {}, {}, None
    results = []
    for line, row in enumerate(rows, 2):
        errors = []
        for field in FIELDS:
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"missing {field}")
        if row.get("source_type") not in SOURCE_TYPES:
            errors.append("unknown or missing source_type")
        if row.get("unit") not in UNITS:
            errors.append("unknown or missing SI unit")
        if row.get("valid") != "1":
            errors.append("invalid sample (valid must be 1)")
        if row.get("extra_cells_json"):
            errors.append("extra CSV cells")
        if row.get("ingest_valid", "1") != "1" or row.get("ingest_errors", "[]") != "[]":
            errors.append("archived ingestion rejection")
        for field in ("config_hash", "cal_hash"):
            if not re.fullmatch(r"[0-9a-f]{64}", row.get(field, "")):
                errors.append(f"{field} must be lowercase SHA-256")
        if row.get("cal_sensor_id") != row.get("sensor_id"):
            errors.append("cal_sensor_id must identify this sensor")
        if require_hash or "record_hash" in row:
            if row.get("record_hash") != canonical_hash(row):
                errors.append("record_hash mismatch or missing")
        if expected_source_id and row.get("source_id") != expected_source_id:
            errors.append("unexpected source_id")
        gm = tuple(row.get(k) for k in GLOBAL_METADATA)
        if global_metadata is None:
            global_metadata = gm
        elif gm != global_metadata:
            errors.append("run/test/logger/config/source_type metadata changed")
        key = (row.get("source_id"), row.get("channel"))
        cm = tuple(row.get(k) for k in CHANNEL_METADATA)
        if key in metadata and metadata[key] != cm:
            errors.append("channel sensor/path/calibration/unit metadata changed")
        metadata.setdefault(key, cm)
        ts = seq = value = None
        try:
            ts = number(row.get("timestamp_s"), "timestamp_s", nonnegative=True)
        except ValueError as exc:
            errors.append(str(exc))
        if re.fullmatch(r"[0-9]+", row.get("sample_id", "")):
            seq = int(row["sample_id"])
        else:
            errors.append("sample_id must be a nonnegative acquisition integer")
        try:
            value = number(row.get("value"), "value")
        except ValueError as exc:
            errors.append(str(exc))
        if key in previous:
            pt, ps = previous[key]
            if ts is not None and pt is not None:
                if ts <= pt:
                    errors.append("non-increasing source/channel timestamp")
                elif max_gap_s is not None and ts - pt > max_gap_s + EPS:
                    errors.append("source/channel time gap")
            if seq is not None and ps is not None and seq != ps + 1:
                errors.append("source/channel sequence discontinuity")
        previous[key] = (ts, seq)
        results.append({"line": line, "errors": errors, "timestamp_s": ts,
                        "sample_id": seq, "value": value})
    return results


def load_events(path):
    raw = Path(path).read_bytes()
    return read_csv(raw, FIELDS + ("record_hash",)), raw


def emit_json(result, output=None):
    text = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if output is not None:
        with Path(output).open("x", encoding="utf-8") as stream:
            stream.write(text)
    print(text, end="")
