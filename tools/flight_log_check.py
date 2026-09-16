"""Offline Mach-duration screening of calibrated air-data CSV; NOT certification.

Required columns: sample_id,t_s,static_pa,impact_pa,probe_temp_k,valid
sample_id and t_s belong to newly acquired, synchronised pressure samples, not
logger ticks. valid is 0 or 1. Missing/stale/invalid data break the time window.
Uncertainty arguments are conservative absolute bounds from calibration.
"""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

if __package__:
    from .airdata import airdata, finite, mach_from_pressures
else:
    from airdata import airdata, finite, mach_from_pressures

FIELDS = {"sample_id", "t_s", "static_pa", "impact_pa", "probe_temp_k", "valid"}


def evaluate(rows, *, static_uncertainty_pa, impact_uncertainty_pa,
             static_min_pa, static_max_pa, impact_max_pa, recovery_factor,
             max_gap_s=0.02, duration_s=5.0):
    for name, value in [("static uncertainty", static_uncertainty_pa),
                        ("impact uncertainty", impact_uncertainty_pa),
                        ("static minimum", static_min_pa), ("static maximum", static_max_pa),
                        ("impact full scale", impact_max_pa), ("max gap", max_gap_s),
                        ("duration", duration_s), ("recovery factor", recovery_factor)]:
        finite(name, value)
    if static_min_pa >= static_max_pa or recovery_factor > 1:
        raise ValueError("invalid static range or recovery factor")
    previous_t = previous_id = start = None
    longest, best_start, best_end, count = 0.0, None, None, 0
    rejected = []
    for line, row in enumerate(rows, 2):
        count += 1
        sample_id, t = int(row["sample_id"]), float(row["t_s"])
        if sample_id < 0 or not math.isfinite(t) or t < 0:
            raise ValueError(f"line {line}: invalid acquisition timestamp/sequence")
        if previous_t is not None and (t <= previous_t or sample_id <= previous_id):
            raise ValueError(f"line {line}: non-increasing acquisition timestamp/sequence")
        if row["valid"] not in ("0", "1"):
            raise ValueError(f"line {line}: valid must be 0 or 1")
        gap = previous_t is not None and (t - previous_t > max_gap_s + 1e-9 or sample_id != previous_id + 1)
        if gap:
            start = None
        previous_t, previous_id = t, sample_id
        reason = None
        if row["valid"] == "0":
            reason = "sensor invalid"
        else:
            try:
                p, qc, temp = (float(row[k]) for k in ("static_pa", "impact_pa", "probe_temp_k"))
                result = airdata(p, qc, temp, recovery_factor)
                # Stay within calibrated ranges including uncertainty; equality
                # at a rail is rejected as potentially clipped, never accepted.
                if p - static_uncertainty_pa <= static_min_pa or p + static_uncertainty_pa >= static_max_pa:
                    reason = "static pressure outside calibrated range"
                if qc + impact_uncertainty_pa >= impact_max_pa:
                    reason = "impact pressure saturated/outside calibrated range"
                lower_mach = mach_from_pressures(p + static_uncertainty_pa, max(0, qc - impact_uncertainty_pa))
                if result["mach"] <= 1 or lower_mach <= 1:
                    reason = reason or "Mach lower bound not above 1"
            except (ValueError, OverflowError) as exc:
                reason = f"invalid air data: {exc}"
        if reason:
            rejected.append({"line": line, "t_s": t, "reason": reason})
            start = None
            continue
        if start is None:
            start = t
        elapsed = t - start  # N samples span N-1 intervals
        if elapsed > longest:
            longest, best_start, best_end = elapsed, start, t
    if not count:
        raise ValueError("empty flight log")
    return {"status": "CANDIDATE" if longest + 1e-9 >= duration_s else "INSUFFICIENT",
            "scope": "Mach-duration screening only; altitude, reciprocal runs and calibration review remain required",
            "samples": count, "longest_window_s": longest, "start_s": best_start, "end_s": best_end,
            "rejected_samples": rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    for flag in ("static-uncertainty-pa", "impact-uncertainty-pa", "static-min-pa", "static-max-pa",
                 "impact-max-pa", "recovery-factor"):
        parser.add_argument(f"--{flag}", required=True, type=float)
    args = parser.parse_args()
    try:
        raw = args.csv.read_bytes()
        reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames) or not FIELDS <= set(reader.fieldnames):
            raise ValueError(f"required unique CSV columns: {','.join(sorted(FIELDS))}")
        config = {k: v for k, v in vars(args).items() if k != "csv"}
        report = evaluate(reader, **config)
        report["input_sha256"] = hashlib.sha256(raw).hexdigest()
        report["configuration"] = config
        print(json.dumps(report, indent=2, allow_nan=False))
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, csv.Error) as exc:
        parser.exit(2, f"Input error: {exc}\n")
    return int(report["status"] != "CANDIDATE")


if __name__ == "__main__":
    raise SystemExit(main())
