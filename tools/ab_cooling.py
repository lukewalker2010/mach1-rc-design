"""Afterburner film-cooling hole sizing at the corrected core mass flow.

Doc 17 derived 65 holes using mdot = 0.69 kg/s. Doc 18/AGENTS correct the
M1/10 kft core flow to 1.10 kg/s, so the bleed requirement (and hole count)
must be recomputed. This module is the single source for the liner hole
schedule used by ab_liner_step.py.

Run: python3 tools/ab_cooling.py [--json]
"""
import argparse
import json
import math

GAMMA = 1.4
R_AIR = 287.0
CD = 0.8
T0 = 423.0          # K, ram-air coolant total temperature (17 §1c)
P0 = 2.0e5          # Pa, annulus total pressure (17 §1c)
HOLE_D = 1.0e-3     # m
MDOT_CORE = 1.10    # kg/s at M1/10 kft (AGENTS §3, 18 §2.1)
BLEED_MIN = 0.023
BLEED_MAX = 0.030

# Chosen 5-row staggered schedule (holes per row), used by the CAD.
ROW_X_MM = (10.0, 50.0, 90.0, 130.0, 170.0)
ROW_HOLES = (34, 26, 21, 17, 14)   # 112 holes


def choked_hole_flow(d=HOLE_D, p0=P0, t0=T0, cd=CD):
    """Mass flow through one choked circular hole, kg/s."""
    area = math.pi * d * d / 4.0
    term = math.sqrt(GAMMA / R_AIR) * ((GAMMA + 1) / 2) ** (
        -(GAMMA + 1) / (2 * (GAMMA - 1))
    )
    return cd * area * (p0 / math.sqrt(t0)) * term


def summarize():
    per_hole = choked_hole_flow()
    need_min = BLEED_MIN * MDOT_CORE / per_hole
    need_max = BLEED_MAX * MDOT_CORE / per_hole
    total = sum(ROW_HOLES)
    bleed = total * per_hole / MDOT_CORE
    return {
        "core_mdot_kg_s": MDOT_CORE,
        "per_hole_kg_s": per_hole,
        "holes_for_2.3pct": need_min,
        "holes_for_3.0pct": need_max,
        "chosen_holes": total,
        "bleed_fraction": bleed,
        "rows_x_mm": list(ROW_X_MM),
        "rows_holes": list(ROW_HOLES),
        "within_band": BLEED_MIN <= bleed <= BLEED_MAX,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = summarize()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"core flow            : {data['core_mdot_kg_s']:.2f} kg/s")
        print(f"flow per 1 mm hole   : {data['per_hole_kg_s']*1e3:.3f} g/s")
        print(f"holes for 2.3-3.0%   : {data['holes_for_2.3pct']:.0f}-{data['holes_for_3.0pct']:.0f}")
        print(f"chosen schedule      : {data['chosen_holes']} holes in {len(ROW_X_MM)} rows")
        print(f"resulting bleed      : {data['bleed_fraction']*100:.2f}% of core")
        print("PASS" if data["within_band"] else "FAIL")
    return 0 if data["within_band"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
