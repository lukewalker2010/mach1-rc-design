"""Continuous fuselage body-law candidate for R01 (smoothstep knots).

The released mould table uses R = 0.0925*sin(pi*x/0.85) for the nose, which
reaches R = 0 at x = 0.85 m and pinches the fuselage shut. This candidate
replaces that segment with a smoothstep through the same maximum radius so
the interior radius stays positive. It is a PROPOSAL: the intake throat still
does not fit the nose (29) and the controlled mould table is unchanged.

Run: python3 tools/fuselage_profile.py [--json]
"""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "proposals/geometry/fuselage_stations_v3.csv"
LENGTH_M = 2.60
STATION_STEP_MM = 50

# (x m, R m) — 29 §R01 candidate; maxima from 18 §3.1.
KNOTS = [
    (0.00, 0.0000),
    (0.85, 0.0925),
    (1.05, 0.0860),
    (1.39, 0.0925),
    (1.80, 0.0925),
    (2.60, 0.0550),
]


def radius(x):
    if x <= KNOTS[0][0]:
        return KNOTS[0][1]
    if x >= KNOTS[-1][0]:
        return KNOTS[-1][1]
    for (a, ra), (b, rb) in zip(KNOTS, KNOTS[1:]):
        if a <= x <= b:
            t = (x - a) / (b - a)
            return ra + (rb - ra) * (3 * t * t - 2 * t * t * t)
    raise ValueError(x)


def slope(x, h=1e-7):
    return (radius(x + h) - radius(x - h)) / (2 * h)


def stations():
    xs = list(range(0, int(LENGTH_M * 1000) + 1, STATION_STEP_MM))
    return [(x, radius(x / 1000.0)) for x in xs]


def summarize():
    interior = [r for x, r in stations() if 0 < x < int(LENGTH_M * 1000)]
    return {
        "length_m": LENGTH_M,
        "station_step_mm": STATION_STEP_MM,
        "stations": len(stations()),
        "max_radius_m": max(r for _, r in stations()),
        "min_interior_radius_m": min(interior),
        "nose_radius_m": radius(0.0),
        "tail_radius_m": radius(LENGTH_M),
        "continuous": min(interior) > 0,
        "knot_slopes": [round(slope(x), 9) for x, _ in KNOTS],
    }


def write_csv(path=OUT_CSV):
    rows = stations()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["x_mm", "R_mm", "OD_mm"])
        for x_mm, r_m in rows:
            writer.writerow([x_mm, round(r_m * 1000, 4), round(2 * r_m * 1000, 4)])
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true", help="regenerate the proposal CSV")
    args = parser.parse_args(argv)
    data = summarize()
    if args.write:
        p = write_csv()
        print(f"wrote {p.relative_to(ROOT)} ({data['stations']} stations)")
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"stations            : {data['stations']} (every {data['station_step_mm']} mm)")
        print(f"max radius          : {data['max_radius_m']*1000:.1f} mm")
        print(f"min interior radius : {data['min_interior_radius_m']*1000:.2f} mm")
        print(f"nose / tail radius  : {data['nose_radius_m']*1000:.1f} / {data['tail_radius_m']*1000:.1f} mm")
        print(f"knot slopes         : {data['knot_slopes']}")
        print("PASS: continuous" if data["continuous"] else "FAIL: pinch")
    return 0 if data["continuous"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
