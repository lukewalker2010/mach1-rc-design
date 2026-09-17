"""Offline load/voltage cycle analysis. Metrics are not a calibration certificate."""
import argparse
import csv
import hashlib
import math
from pathlib import Path

if __package__:
    from .bench_schema import emit_json, number, read_csv
else:
    from bench_schema import emit_json, number, read_csv

REQUIRED = ("cycle", "direction", "known_N", "measured_v", "valid")


def fit_linear(x_vals, y_vals):
    """Centred OLS voltage = slope_V_per_N * force + intercept_V."""
    if len(x_vals) != len(y_vals) or len(x_vals) < 2:
        raise ValueError("need at least two paired points")
    x = [number(v, "known_N") for v in x_vals]
    y = [number(v, "measured_v") for v in y_vals]
    xm, ym = math.fsum(x) / len(x), math.fsum(y) / len(y)
    dx, dy = [v - xm for v in x], [v - ym for v in y]
    denom = math.fsum(v * v for v in dx)
    if denom <= 0:
        raise ValueError("degenerate known-load range")
    slope = math.fsum(a * b for a, b in zip(dx, dy)) / denom
    return slope, ym - slope * xm


def compute_metrics(rows, *, max_residual_N=None, max_hysteresis_N=None,
                    max_repeatability_N=None, max_heldout_N=None,
                    min_load_N=None, max_load_N=None):
    limits = {"max_residual_N": max_residual_N, "max_hysteresis_N": max_hysteresis_N,
              "max_repeatability_N": max_repeatability_N, "max_heldout_N": max_heldout_N}
    for name, value in limits.items():
        if value is not None:
            limits[name] = number(value, name, positive=True)
    if (min_load_N is None) != (max_load_N is None):
        raise ValueError("supply both reviewed load-range endpoints")
    if min_load_N is not None:
        min_load_N = number(min_load_N, "min_load_N")
        max_load_N = number(max_load_N, "max_load_N")
        if max_load_N <= min_load_N:
            raise ValueError("reviewed load range must increase")
    points = []
    for line, row in enumerate(rows, 2):
        if any(row.get(k, "") == "" for k in REQUIRED):
            raise ValueError(f"line {line}: missing calibration field")
        if row["valid"] != "1":
            raise ValueError(f"line {line}: invalid calibration point; cannot silently discard")
        try:
            cycle = int(row["cycle"])
        except (ValueError, TypeError):
            raise ValueError(f"line {line}: cycle must be positive integer") from None
        if cycle < 1 or str(cycle) != str(row["cycle"]):
            raise ValueError(f"line {line}: cycle must be positive integer")
        if row["direction"] not in ("ASC", "DESC"):
            raise ValueError(f"line {line}: direction must be ASC or DESC")
        if row.get("unit", "V") != "V" or row.get("known_unit", "N") != "N":
            raise ValueError("calibration requires known_N in N and measured_v in V")
        points.append((cycle, row["direction"], number(row["known_N"], "known_N"),
                       number(row["measured_v"], "measured_v")))
    cycles = sorted({p[0] for p in points})
    if len(cycles) < 2 or cycles != list(range(1, len(cycles) + 1)):
        raise ValueError("need at least two complete, consecutive cycles starting at 1")
    if [p[0] for p in points] != sorted(p[0] for p in points):
        raise ValueError("cycles out of acquisition order")
    paired, common_levels, signs = {}, None, []
    for cycle in cycles:
        cp = [p for p in points if p[0] == cycle]
        asc, desc = [p for p in cp if p[1] == "ASC"], [p for p in cp if p[1] == "DESC"]
        if cp != asc + desc or len(asc) < 3 or len(desc) < 3:
            raise ValueError("each cycle needs ASC then DESC, at least three levels each")
        a, d = [p[2] for p in asc], [p[2] for p in desc]
        if any(b <= a0 for a0, b in zip(a, a[1:])) or any(b >= a0 for a0, b in zip(d, d[1:])):
            raise ValueError("load levels must strictly ascend then descend")
        if a != list(reversed(d)) or (common_levels is not None and a != common_levels):
            raise ValueError("same load levels required in both directions of every cycle")
        common_levels = a
        if min_load_N is not None and (a[0] > min_load_N or a[-1] < max_load_N):
            raise ValueError("cycles do not cover reviewed load range")
        for branch in (asc, list(reversed(desc))):
            diffs = [q[3] - p[3] for p, q in zip(branch, branch[1:])]
            if not (all(v > 0 for v in diffs) or all(v < 0 for v in diffs)):
                raise ValueError("constant or reversing sensor response within load sweep")
            signs.append(1 if diffs[0] > 0 else -1)
        paired[cycle] = {str(p[2]): q[3] - p[3] for p, q in zip(asc, reversed(desc))}
    if len(set(signs)) != 1:
        raise ValueError("sensor sensitivity sign changed between sweeps")
    x, y = [p[2] for p in points], [p[3] for p in points]
    slope, intercept = fit_linear(x, y)
    if slope == 0 or not math.isfinite(slope):
        raise ValueError("non-invertible sensor sensitivity")
    xm, ym = math.fsum(x) / len(x), math.fsum(y) / len(y)
    res = [(v - ym) / slope - (f - xm) for f, v in zip(x, y)]
    hyst = {str(c): {level: abs(v / slope) for level, v in levels.items()}
            for c, levels in paired.items()}
    repeatability = max((max(vals) - min(vals)) / abs(slope)
                        for direction in ("ASC", "DESC") for level in common_levels
                        for vals in [[p[3] for p in points if p[1] == direction and p[2] == level]])
    heldout = []
    for cycle in cycles:
        train = [p for p in points if p[0] != cycle]
        tx, ty = [p[2] for p in train], [p[3] for p in train]
        s, _ = fit_linear(tx, ty)
        if s == 0:
            raise ValueError("non-invertible held-out training fit")
        mx, my = math.fsum(tx) / len(tx), math.fsum(ty) / len(ty)
        heldout.extend(abs((p[3] - my) / s - (p[2] - mx)) for p in points if p[0] == cycle)
    metrics = {"max_residual_N": max(map(abs, res)),
               "max_hysteresis_N": max(v for levels in hyst.values() for v in levels.values()),
               "max_repeatability_N": repeatability, "max_heldout_N": max(heldout)}
    complete = all(v is not None for v in limits.values()) and min_load_N is not None
    status = ("METRICS_WITHIN_LIMITS" if all(metrics[k] <= limits[k] for k in metrics) else "FAIL") if complete else "ANALYSIS_ONLY"
    return {"status": status, "physical_qualified": False, "limits_N": limits,
            "reviewed_range_N": [min_load_N, max_load_N], "metrics_N": metrics,
            "slope_V_per_N": slope, "intercept_V": intercept,
            "inverse_slope_N_per_V": 1 / slope, "inverse_intercept_N": -intercept / slope,
            "conversion": "force_N = center_force_N + (voltage_V - center_voltage_V) / slope_V_per_N",
            "center_force_N": xm, "center_voltage_V": ym,
            "residuals_N": res, "residual_rms_N": math.sqrt(math.fsum(r*r for r in res) / len(res)),
            "hysteresis_per_cycle_N": hyst, "cycles": len(cycles), "known_levels_N": common_levels,
            "scope": "Fit diagnostics only; held-out means leave-one-cycle-out. Residuals are not expanded uncertainty; reference loads, drift, installation and authenticity require separate evidence."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    for flag in ("max-residual-N", "max-hysteresis-N", "max-repeatability-N", "max-heldout-N", "min-load-N", "max-load-N"):
        parser.add_argument("--" + flag, type=float)
    args = parser.parse_args(argv)
    try:
        raw = args.csv.read_bytes()
        result = compute_metrics(read_csv(raw, REQUIRED), **{k: v for k, v in vars(args).items() if k not in ("csv", "output")})
        result["input_sha256"] = hashlib.sha256(raw).hexdigest()
        emit_json(result, args.output)
        return 1 if result["status"] == "FAIL" else 0
    except (OSError, ValueError, UnicodeError, csv.Error, OverflowError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
