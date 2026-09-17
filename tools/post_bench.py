"""Offline selected thrust/temperature screen, not G0 or flight qualification."""
import argparse
import csv
import hashlib
import math
from pathlib import Path

if __package__:
    from .bench_schema import EPS, emit_json, load_events, number, validate_events
else:
    from bench_schema import EPS, emit_json, load_events, number, validate_events

load_records = load_events


def screen_channel(rows, checks, channel, unit, start, end, rate, bounds=None):
    selected = [(r, c) for r, c in zip(rows, checks) if r.get("channel") == channel
                and (c["timestamp_s"] is None or start - EPS <= c["timestamp_s"] <= end + EPS)]
    issues = []
    if len(selected) < 2:
        issues.append("need at least two samples covering both gate endpoints")
    if len({r.get("source_id") for r, _ in selected}) != 1:
        issues.append("selected channel must have one source throughout gate")
    for row, check in selected:
        if check["errors"]:
            issues.append(f"line {check['line']}: " + "; ".join(check["errors"]))
        if row.get("unit") != unit:
            issues.append(f"line {check['line']}: expected unit {unit}")
        value = check["value"]
        if value is not None and unit == "K" and value <= 0:
            issues.append("temperature must be positive K")
        if value is not None and bounds and not bounds[0] < value < bounds[1]:
            issues.append(f"line {check['line']}: clipped/outside explicit calibrated bounds")
    points = [(c["timestamp_s"], c["value"]) for _, c in selected
              if c["timestamp_s"] is not None and c["value"] is not None]
    gaps = []
    if points:
        if abs(points[0][0] - start) > EPS or abs(points[-1][0] - end) > EPS:
            issues.append("missing first/last gate endpoint (no extrapolation)")
        for (a, _), (b, _) in zip(points, points[1:]):
            if b <= a or b - a > 1 / rate + EPS:
                gaps.append({"from_s": a, "to_s": b, "gap_s": b - a})
    else:
        issues.append("no finite data")
    if gaps:
        issues.append("source/channel continuity or required sample-rate failure")
    return {"channel": channel, "unit": unit, "required_rate_hz": rate,
            "sample_count": len(selected), "issues": issues, "gaps": gaps,
            "calibrated_bounds": bounds}, points


def screen(records, *, gate_start_s, gate_end_s=None, duration_s=20.0, duration_review=None,
           min_thrust_N, thrust_uncertainty_N, max_temp_K, temp_uncertainty_K,
           temp_rate_hz, thrust_rate_hz=500.0, thrust_channel="THRUST_N", temp_channel="TEMP_K",
           thrust_min_N=None, thrust_max_N=None, temp_min_K=None, temp_max_K=None):
    start = number(gate_start_s, "gate_start_s", nonnegative=True)
    duration = number(duration_s, "duration_s", positive=True)
    if duration != 20.0 and not (duration_review and duration_review.strip()):
        raise ValueError("nondefault duration requires --duration-review reference")
    end = start + duration if gate_end_s is None else number(gate_end_s, "gate_end_s", nonnegative=True)
    if end <= start:
        raise ValueError("gate end must follow start")
    threshold = number(min_thrust_N, "min_thrust_N", positive=True)
    fu = number(thrust_uncertainty_N, "thrust_uncertainty_N", positive=True)
    limit = number(max_temp_K, "max_temp_K", positive=True)
    tu = number(temp_uncertainty_K, "temp_uncertainty_K", positive=True)
    fr = number(thrust_rate_hz, "thrust_rate_hz", positive=True)
    tr = number(temp_rate_hz, "temp_rate_hz", positive=True)
    if fr < 500:
        raise ValueError("thrust rate must meet at least 500 Hz (26/33)")
    if not thrust_channel or not temp_channel or thrust_channel == temp_channel:
        raise ValueError("select distinct thrust and temperature channels")
    bounds = []
    for low, high in ((thrust_min_N, thrust_max_N), (temp_min_K, temp_max_K)):
        if (low is None) != (high is None):
            raise ValueError("supply both calibrated clipping bounds")
        if low is not None:
            low, high = number(low, "calibrated minimum"), number(high, "calibrated maximum")
            if low >= high:
                raise ValueError("calibrated bounds must increase")
        bounds.append(None if low is None else [low, high])
    checks = validate_events(records, require_hash=True)
    # Whole-file schema/hash/metadata faults cannot be hidden by choosing a window.
    integrity = [{"line": c["line"], "errors": c["errors"]} for c in checks if c["errors"]]
    thrust, fp = screen_channel(records, checks, thrust_channel, "N", start, end, fr, bounds[0])
    temp, tp = screen_channel(records, checks, temp_channel, "K", start, end, tr, bounds[1])
    if fp:
        thrust.update(min_raw_N=min(v for _, v in fp), max_raw_N=max(v for _, v in fp),
                      min_lower_bound_N=min(v for _, v in fp) - fu)
        if len(fp) >= 2 and all(b[0] > a[0] for a, b in zip(fp, fp[1:])):
            # Time weighting handles nonuniform samples. The lower-endpoint
            # rectangle is conservative relative to linear interpolation only.
            mean = math.fsum((b[0] - a[0]) * min(a[1], b[1]) for a, b in zip(fp, fp[1:])) / (fp[-1][0] - fp[0][0])
            thrust["time_weighted_lower_bound_N"] = mean - fu
        if thrust["min_lower_bound_N"] < threshold:
            thrust["issues"].append("sampled thrust lower bound below explicit threshold")
    if tp:
        temp.update(max_raw_K=max(v for _, v in tp), max_upper_bound_K=max(v for _, v in tp) + tu)
        if temp["max_upper_bound_K"] > limit:
            temp["issues"].append("raw maximum plus uncertainty exceeds temperature limit")
    duration_ok = end - start + EPS >= duration
    numerical_ok = duration_ok and not thrust["issues"] and not temp["issues"] and not integrity
    source_types = sorted({r.get("source_type", "") for r in records})
    physical_source = bool(records) and source_types == ["BENCH"]
    # SIMULATED/CALIBRATION/FLIGHT/missing/unknown cannot obtain SCREEN_PASS.
    status = "SCREEN_PASS" if numerical_ok and physical_source else "NONPHYSICAL" if numerical_ok else "FAIL"
    return {"status": status, "physical_qualified": False,
            "gate_start_s": start, "gate_end_s": end, "required_duration_s": duration,
            "duration_review": duration_review, "duration_ok": duration_ok,
            "numerical_checks_ok": numerical_ok, "source_types": source_types,
            "bench_provenance_eligible": physical_source,
            "limits": {"min_thrust_N": threshold, "thrust_uncertainty_N": fu,
                       "max_temp_K": limit, "temp_uncertainty_K": tu},
            "integrity_issues": integrity, "thrust": thrust, "temperature": temp,
            "scope": "Selected static thrust and ONE temperature channel only. SCREEN_PASS is not G0 qualification, the full G0 thermal suite, flight thrust, or release. Uncertainty inputs are positive expanded absolute bounds supplied by the reviewer, not fit residuals. Time-weighted force uses lower adjacent endpoints; intersample dynamics and bandwidth remain unverified."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    for flag in ("gate-start-s", "min-thrust-N", "thrust-uncertainty-N", "max-temp-K", "temp-uncertainty-K", "temp-rate-hz"):
        parser.add_argument("--" + flag, type=float, required=True)
    for flag in ("gate-end-s", "thrust-min-N", "thrust-max-N", "temp-min-K", "temp-max-K"):
        parser.add_argument("--" + flag, type=float)
    parser.add_argument("--duration-s", type=float, default=20.0)
    parser.add_argument("--duration-review")
    parser.add_argument("--thrust-rate-hz", type=float, default=500.0)
    parser.add_argument("--thrust-channel", default="THRUST_N")
    parser.add_argument("--temp-channel", default="TEMP_K")
    args = parser.parse_args(argv)
    try:
        records, raw = load_records(args.csv)
        result = screen(records, **{k: v for k, v in vars(args).items() if k not in ("csv", "output")})
        result["input_sha256"] = hashlib.sha256(raw).hexdigest()
        emit_json(result, args.output)
        return 0 if result["status"] == "SCREEN_PASS" else 1
    except (OSError, ValueError, UnicodeError, csv.Error, OverflowError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
