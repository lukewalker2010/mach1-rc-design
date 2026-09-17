#!/usr/bin/env python3
"""Fuel-state CG sweep, tolerance analysis and parametric mission budget for Mach 1 RC.

R05 closure deliverable: demonstrates whether the CG band 0.955-0.995 m can be
met across all fuel states given the 18 S3.4 mass table, I-06 tank station range
(350-600 mm), mass/station tolerances, and AB 0.83 vs 0.97 kg accounting.

Also provides a mission budget CSV parser for fuel-mass-conserving phase analysis.

Run: python3 tools/mass_mission.py [--mission FILE.csv] [--json]
CLI reads the authoritative 18 S3.4 rows via design_checks.mass_rows.
"""
import argparse
import csv
import json
import math
from pathlib import Path

if __package__:
    from .design_checks import mass_rows, mass_state
else:
    from design_checks import mass_rows, mass_state

ROOT = Path(__file__).resolve().parents[1]

FUEL_MASS_KG = 1.62
FUEL_STATION_M = 0.45
AB_MASS_BASELINE_KG = 0.83
AB_MASS_ALTERNATE_KG = 0.97
TANK_STATION_MIN_M = 0.35
TANK_STATION_MAX_M = 0.60
CG_MIN_M = 0.955
CG_MAX_M = 0.995
MTOW_KG = 25.0


def _validate_rows(rows):
    if not rows:
        raise ValueError("empty mass table")
    for name, mass, station in rows:
        if not isinstance(name, str) or not name or not math.isfinite(mass) or mass <= 0 or not math.isfinite(station) or not 0 <= station <= 2.6:
            raise ValueError("invalid component mass/station")
    fuels = [(m, s) for n, m, s in rows if n.startswith("Fuel (")]
    if len(fuels) != 1 or len(rows) < 2:
        raise ValueError("requires one fuel row and non-fuel mass")
    return fuels[0]


def _points(n, minimum):
    if not isinstance(n, int) or isinstance(n, bool) or n < minimum:
        raise ValueError("invalid sweep point count")


def _subset_rows(rows, ab_mass_kg=None, fuel_station_m=None):
    _validate_rows(rows)
    if ab_mass_kg is not None and (not math.isfinite(ab_mass_kg) or ab_mass_kg <= 0):
        raise ValueError("AB mass must be positive and finite")
    if fuel_station_m is not None and (not math.isfinite(fuel_station_m) or not 0 <= fuel_station_m <= 2.6):
        raise ValueError("invalid fuel station")
    result = []
    for name, mass, station in rows:
        m = mass
        s = station
        if name.startswith("Afterburner") and ab_mass_kg is not None:
            m = ab_mass_kg
        if name.startswith("Fuel (") and fuel_station_m is not None:
            s = fuel_station_m
        result.append((name, m, s))
    return result


def fuel_state_sweep(rows, n_points=50):
    _validate_rows(rows)
    _points(n_points, 1)
    results = []
    for i in range(n_points + 1):
        f = 1.0 - i / n_points
        state = mass_state(rows, f)
        cg = state["cg_m"]
        results.append({
            "fuel_fraction": round(f, 6),
            "mass_kg": state["mass_kg"],
            "moment_kg_m": state["moment_kg_m"],
            "cg_m": cg,
            "in_band": CG_MIN_M <= cg <= CG_MAX_M,
        })
    return results


def tolerance_sweep(rows, mass_tol=0.05, station_tol=0.005):
    """Independent box bounds, not correlated all-light/all-heavy corners.

    Fuel mass is known at each fraction; every station has the stated error.
    For a trial CG c, extremise sum(m_i*(x_i-c)) by choosing each mass bound
    according to the sign of x_i-c. Its unique zero is the ratio extremum.
    """
    _validate_rows(rows)
    if any(not math.isfinite(v) or v < 0 for v in (mass_tol, station_tol)):
        raise ValueError("tolerances must be finite and nonnegative")
    if any(mass_tol >= m for n, m, s in rows if not n.startswith("Fuel (")):
        raise ValueError("mass tolerance permits nonpositive component mass")
    results = []
    for i in range(51):
        f = 1.0 - i / 50.0
        def bound(maximise):
            terms = []
            for name, mass, station in rows:
                fuel = name.startswith("Fuel (")
                m = mass*f if fuel else mass
                if m == 0:
                    continue
                dm = 0 if fuel else mass_tol
                terms.append((m-dm, m+dm, station+(station_tol if maximise else -station_tol)))
            lo, hi = min(t[2] for t in terms), max(t[2] for t in terms)
            for _ in range(80):
                c = (lo+hi)/2
                residual = sum((upper if ((x > c) == maximise) else lower)*(x-c)
                               for lower, upper, x in terms)
                if residual > 0:
                    lo = c
                else:
                    hi = c
            return (lo+hi)/2
        fwd_cg, aft_cg = bound(False), bound(True)
        results.append({
            "fuel_fraction": round(f, 4),
            "fwd_cg_m": fwd_cg,
            "aft_cg_m": aft_cg,
            "fwd_in_band": CG_MIN_M <= fwd_cg <= CG_MAX_M,
            "aft_in_band": CG_MIN_M <= aft_cg <= CG_MAX_M,
            "both_in_band": CG_MIN_M <= fwd_cg and aft_cg <= CG_MAX_M,
        })
    return results


def admissible_dry_moment(rows):
    _validate_rows(rows)
    empty = mass_state(rows, 0)
    dry_mass = empty["mass_kg"]
    dry_moment = empty["moment_kg_m"]
    dry_cg = empty["cg_m"]
    moment_min = dry_mass * CG_MIN_M
    moment_max = dry_mass * CG_MAX_M
    return {
        "dry_mass_kg": dry_mass,
        "dry_moment_kg_m": dry_moment,
        "dry_cg_m": dry_cg,
        "admissible_moment_min_kg_m": moment_min,
        "admissible_moment_max_kg_m": moment_max,
        "margin_to_min_kg_m": dry_moment - moment_min,
        "margin_to_max_kg_m": moment_max - dry_moment,
        "in_band": CG_MIN_M <= dry_cg <= CG_MAX_M,
    }


def admissible_fuel_station(rows, dry_moment_override=None):
    fuel_mass, _ = _validate_rows(rows)
    empty = mass_state(rows, 0)
    dry_mass = empty["mass_kg"]
    dm = dry_moment_override if dry_moment_override is not None else empty["moment_kg_m"]
    if not math.isfinite(dm):
        raise ValueError("dry moment must be finite")
    full_mass = dry_mass + fuel_mass
    s_min = (full_mass * CG_MIN_M - dm) / fuel_mass
    s_max = (full_mass * CG_MAX_M - dm) / fuel_mass
    feasible = s_min <= TANK_STATION_MAX_M and s_max >= TANK_STATION_MIN_M
    actual_min = max(s_min, TANK_STATION_MIN_M)
    actual_max = min(s_max, TANK_STATION_MAX_M)
    return {
        "dry_moment_kg_m": dm,
        "dry_mass_kg": dry_mass,
        "fuel_station_min_m": s_min,
        "fuel_station_max_m": s_max,
        "i06_feasible": feasible,
        "i06_actual_min_m": actual_min if feasible else None,
        "i06_actual_max_m": actual_max if feasible else None,
    }


def ab_sensitivity(rows):
    results = {}
    for label, ab_mass in [("baseline_0.83", AB_MASS_BASELINE_KG),
                           ("alternate_0.97", AB_MASS_ALTERNATE_KG)]:
        modified = _subset_rows(rows, ab_mass_kg=ab_mass)
        full_state = mass_state(modified, 1)
        empty_state = mass_state(modified, 0)
        half_state = mass_state(modified, 0.5)
        results[label] = {
            "ab_mass_kg": ab_mass,
            "full_cg_m": full_state["cg_m"],
            "full_mass_kg": full_state["mass_kg"],
            "empty_cg_m": empty_state["cg_m"],
            "empty_mass_kg": empty_state["mass_kg"],
            "half_cg_m": half_state["cg_m"],
            "full_in_band": CG_MIN_M <= full_state["cg_m"] <= CG_MAX_M,
            "empty_in_band": CG_MIN_M <= empty_state["cg_m"] <= CG_MAX_M,
        }
    delta = results["alternate_0.97"]["empty_cg_m"] - results["baseline_0.83"]["empty_cg_m"]
    results["sensitivity"] = {
        "delta_empty_cg_m": delta,
        "delta_empty_cg_mm": delta * 1000,
        "note": ("0.14 kg AB increase shifts empty CG aft; "
                 "0.97 may double-count pump ($80 in 5.2) and fuel system (0.50 in 3.4)"),
    }
    return results


def tank_relocation_sweep(rows, n_points=26):
    _validate_rows(rows)
    _points(n_points, 2)
    results = []
    for i in range(n_points):
        s = TANK_STATION_MIN_M + i * (TANK_STATION_MAX_M - TANK_STATION_MIN_M) / (n_points - 1)
        modified = _subset_rows(rows, fuel_station_m=s)
        full_state = mass_state(modified, 1)
        empty_state = mass_state(modified, 0)
        results.append({
            "tank_station_m": round(s, 4),
            "tank_station_mm": round(s * 1000, 1),
            "full_cg_m": full_state["cg_m"],
            "full_in_band": CG_MIN_M <= full_state["cg_m"] <= CG_MAX_M,
            "empty_cg_m": empty_state["cg_m"],
            "empty_in_band": CG_MIN_M <= empty_state["cg_m"] <= CG_MAX_M,
        })
    return results


def joint_ballast_analysis(rows, ballast_station_m=0.10):
    """Additional ballast only; intersect both endpoint linear inequalities."""
    _validate_rows(rows)
    if not math.isfinite(ballast_station_m) or not 0 <= ballast_station_m <= 2.6:
        raise ValueError("ballast station outside fuselage")
    dry = mass_state(rows, 0)
    full = mass_state(rows, 1)
    dry_mass = dry["mass_kg"]
    dry_moment = dry["moment_kg_m"]
    full_mass = full["mass_kg"]
    full_moment = full["moment_kg_m"]

    actual_min, actual_max = 0., MTOW_KG-full_mass
    for state in (dry, full):
        for a, rhs in ((ballast_station_m-CG_MAX_M, CG_MAX_M*state["mass_kg"]-state["moment_kg_m"]),
                       (CG_MIN_M-ballast_station_m, state["moment_kg_m"]-CG_MIN_M*state["mass_kg"])):
            # a*b <= rhs; reversing a's sign reverses the mass bound.
            if a > 0:
                actual_max = min(actual_max, rhs/a)
            elif a < 0:
                actual_min = max(actual_min, rhs/a)
            elif rhs < 0:
                actual_max = -1.
    feasible = actual_min <= actual_max

    if feasible and actual_min <= actual_max:
        b = actual_min
        cg_empty = (dry_moment + b * ballast_station_m) / (dry_mass + b)
        cg_full = (full_moment + b * ballast_station_m) / (full_mass + b)
    else:
        cg_empty = cg_full = None

    return {
        "ballast_station_m": ballast_station_m,
        "b_min_for_empty_cg_max_kg": (dry_moment-CG_MAX_M*dry_mass)/(CG_MAX_M-ballast_station_m) if ballast_station_m < CG_MIN_M else None,
        "b_max_for_full_cg_min_kg": (full_moment-CG_MIN_M*full_mass)/(CG_MIN_M-ballast_station_m) if ballast_station_m < CG_MIN_M else None,
        "feasible": feasible,
        "ballast_range_kg": [actual_min, actual_max] if feasible else None,
        "resulting_empty_cg_m": cg_empty,
        "resulting_full_cg_m": cg_full,
        "dry_mass_kg": dry_mass,
        "full_mass_kg": full_mass,
    }


def ballast_mtow_proof(rows):
    """Necessary mass bound plus a constructive ballast interval at MTOW.

    For fixed fuel centroid x_f < CG_MIN, empty CG <= CG_MAX implies
    full CG <= CG_MAX - m_f*(CG_MAX-x_f)/M_full. Thus M_full must be
    >= m_f*(CG_MAX-x_f)/(CG_MAX-CG_MIN), irrespective of dry layout.
    """
    mf, xf = _validate_rows(rows)
    if xf >= CG_MIN_M:
        raise ValueError("proof requires fuel ahead of CG band")
    dry, full = mass_state(rows, 0), mass_state(rows, 1)
    b = MTOW_KG-full["mass_kg"]
    minimum = mf*(CG_MAX_M-xf)/(CG_MAX_M-CG_MIN_M)
    if b <= 0:
        interval = None
    else:
        lo = max(0., *((CG_MIN_M*(s["mass_kg"]+b)-s["moment_kg_m"])/b for s in (dry, full)))
        hi = min(2.6, *((CG_MAX_M*(s["mass_kg"]+b)-s["moment_kg_m"])/b for s in (dry, full)))
        interval = [lo, hi] if lo <= hi else None
    return dict(minimum_full_mass_kg=minimum, additional_mass_at_mtow_kg=b,
                station_interval_at_mtow_m=interval)


def combined_analysis(rows):
    return {
        "sweep": fuel_state_sweep(rows),
        "tolerance": tolerance_sweep(rows),
        "dry_moment": admissible_dry_moment(rows),
        "fuel_station": admissible_fuel_station(rows),
        "ab_sensitivity": ab_sensitivity(rows),
        "tank_sweep": tank_relocation_sweep(rows),
        "ballast_analysis": joint_ballast_analysis(rows),
        "ballast_mtow_proof": ballast_mtow_proof(rows),
    }


MISSION_FIELDS = {"phase", "duration_s", "engine_flow_g_s", "ab_flow_g_s",
                  "initial_fuel_kg", "initial_cg_m"}


def parse_mission_csv(path, rows):
    fuel_mass, _ = _validate_rows(rows)
    path = Path(path)
    raw = path.read_bytes()
    reader = csv.DictReader(raw.decode("utf-8-sig").splitlines())
    if not reader.fieldnames or not MISSION_FIELDS <= set(reader.fieldnames) or len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise ValueError(f"required columns: {','.join(sorted(MISSION_FIELDS))}")

    dry = mass_state(rows, 0)
    phases = []
    prev_fuel = None
    for line_no, row in enumerate(reader, 2):
        phase = row["phase"]
        if not phase or not phase.strip() or None in row:
            raise ValueError(f"line {line_no}: invalid phase or surplus fields")
        try:
            duration_s = float(row["duration_s"])
            engine_flow = float(row["engine_flow_g_s"])
            ab_flow = float(row["ab_flow_g_s"])
            initial_fuel = float(row["initial_fuel_kg"])
            initial_cg = float(row["initial_cg_m"])
        except (ValueError, KeyError, TypeError) as exc:
            raise ValueError(f"line {line_no}: {exc}")

        if not all(math.isfinite(x) for x in [duration_s, engine_flow, ab_flow, initial_fuel, initial_cg]):
            raise ValueError(f"line {line_no}: non-numeric or NaN values")
        if duration_s < 0 or engine_flow < 0 or ab_flow < 0 or initial_fuel < 0:
            raise ValueError(f"line {line_no}: negative values not allowed")
        if initial_fuel > fuel_mass + 1e-9:
            raise ValueError(f"line {line_no}: initial_fuel {initial_fuel} exceeds tank {FUEL_MASS_KG}")

        if prev_fuel is not None and abs(initial_fuel - prev_fuel) > 1e-9:
            raise ValueError(f"line {line_no}: initial_fuel {initial_fuel} != prev remaining {prev_fuel}")

        expected_cg = mass_state(rows, initial_fuel/fuel_mass)["cg_m"]
        # CSV CG is a redundant consistency field, rounded to 0.1 mm maximum.
        if abs(initial_cg-expected_cg) > 0.00005:
            raise ValueError(f"line {line_no}: initial CG disagrees with mass table")
        total_flow_g = (engine_flow + ab_flow) * duration_s
        if not math.isfinite(total_flow_g):
            raise ValueError(f"line {line_no}: fuel calculation overflow")
        fuel_burned_kg = total_flow_g / 1000.0
        fuel_remaining_kg = initial_fuel - fuel_burned_kg

        if fuel_remaining_kg < -1e-9:
            raise ValueError(f"line {line_no}: overdraw {fuel_remaining_kg:.6f} kg")
        fuel_remaining_kg = max(fuel_remaining_kg, 0.0)

        fuel_frac = fuel_remaining_kg / fuel_mass
        state = mass_state(rows, fuel_frac)
        cg_m = state["cg_m"]
        mass_kg = state["mass_kg"]

        phases.append({
            "phase": phase,
            "duration_s": duration_s,
            "engine_flow_g_s": engine_flow,
            "ab_flow_g_s": ab_flow,
            "fuel_burned_kg": fuel_burned_kg,
            "fuel_remaining_kg": fuel_remaining_kg,
            "cg_m": cg_m,
            "mass_kg": mass_kg,
            "in_band": CG_MIN_M <= cg_m <= CG_MAX_M,
        })
        prev_fuel = fuel_remaining_kg

    if not phases:
        raise ValueError("mission has no phases")
    return phases


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--mission", type=Path, help="Mission budget CSV file")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    try:
        rows = mass_rows()
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Input error: {exc}\n")

    if args.mission:
        try:
            phases = parse_mission_csv(args.mission, rows)
        except (OSError, ValueError) as exc:
            parser.exit(2, f"Mission CSV error: {exc}\n")
        if args.json:
            print(json.dumps({"phases": phases}, indent=2, allow_nan=False))
        else:
            print("MISSION PHASES (mass-conserving, CG tracked)")
            for p in phases:
                flag = "IN-BAND" if p["in_band"] else "OUT"
                print(f"  {p['phase']}: {p['duration_s']:.1f}s, burned {p['fuel_burned_kg']:.4f} kg, "
                      f"remaining {p['fuel_remaining_kg']:.4f} kg, CG {p['cg_m']:.4f} m [{flag}]")
            print("MISSION ANALYSIS: planning scenario only; not flight evidence.")
        return 0

    report = combined_analysis(rows)

    if args.json:
        print(json.dumps(report, indent=2, allow_nan=False))
        return 0

    dm = report["dry_moment"]
    print("R05 CG/MASS RESOLUTION ANALYSIS")
    print("=" * 60)
    print(f"Dry mass: {dm['dry_mass_kg']:.3f} kg, moment: {dm['dry_moment_kg_m']:.4f} kg.m, CG: {dm['dry_cg_m']:.4f} m")
    print(f"  Admissible moment range: [{dm['admissible_moment_min_kg_m']:.4f}, {dm['admissible_moment_max_kg_m']:.4f}] kg.m")
    print(f"  Current excess above max: {-dm['margin_to_max_kg_m']:.4f} kg.m")
    print(f"  Margin above min: {dm['margin_to_min_kg_m']:.4f} kg.m")
    print(f"  In band: {'PASS' if dm['in_band'] else 'FAIL'}")

    fs = report["fuel_station"]
    print(f"\nFuel station for full CG band:")
    print(f"  Required range: [{fs['fuel_station_min_m']:.4f}, {fs['fuel_station_max_m']:.4f}] m")
    print(f"  I-06 available: [{TANK_STATION_MIN_M:.2f}, {TANK_STATION_MAX_M:.2f}] m")
    print(f"  I-06 feasible: {'YES' if fs['i06_feasible'] else 'NO'}")
    if fs['i06_feasible']:
        print(f"  Feasible overlap: [{fs['i06_actual_min_m']:.4f}, {fs['i06_actual_max_m']:.4f}] m")

    ba = report["ballast_analysis"]
    print(f"\nJoint ballast analysis (station {ba['ballast_station_m']:.2f} m):")
    print(f"  Min ballast for empty CG <= {CG_MAX_M}: {ba['b_min_for_empty_cg_max_kg']:.4f} kg")
    print(f"  Max ballast for full CG >= {CG_MIN_M}: {ba['b_max_for_full_cg_min_kg']:.4f} kg")
    print(f"  Feasible: {'YES' if ba['feasible'] else 'NO'}")
    print(f"  Fixed-fuel MTOW bound/construction: {report['ballast_mtow_proof']}")
    if ba['feasible']:
        print(f"  Ballast range: [{ba['ballast_range_kg'][0]:.4f}, {ba['ballast_range_kg'][1]:.4f}] kg")
        print(f"  Resulting empty CG: {ba['resulting_empty_cg_m']:.4f} m")
        print(f"  Resulting full CG: {ba['resulting_full_cg_m']:.4f} m")

    ab = report["ab_sensitivity"]
    print(f"\nAB sensitivity (0.83 vs 0.97 kg):")
    for key in ("baseline_0.83", "alternate_0.97"):
        d = ab[key]
        print(f"  {key}: full CG {d['full_cg_m']:.4f} m [{'PASS' if d['full_in_band'] else 'FAIL'}], "
              f"empty CG {d['empty_cg_m']:.4f} m [{'PASS' if d['empty_in_band'] else 'FAIL'}]")
    print(f"  Delta empty CG: {ab['sensitivity']['delta_empty_cg_mm']:.1f} mm")
    print(f"  Note: {ab['sensitivity']['note']}")

    sweep = report["sweep"]
    full_pass = all(s["in_band"] for s in sweep)
    print(f"\nFull sweep ({len(sweep)} points): {'ALL IN BAND' if full_pass else 'OUT OF BAND at some fuel fractions'}")
    for s in sweep:
        if not s["in_band"]:
            print(f"  f={s['fuel_fraction']:.3f}: CG {s['cg_m']:.4f} m")

    tol = report["tolerance"]
    tol_all = all(t["both_in_band"] for t in tol)
    print(f"\nTolerance sweep (+-50 g mass, +-5 mm station): {'ALL IN BAND' if tol_all else 'EXCEEDS BAND'}")

    print("\nANALYSIS COMPLETE: see 31_mass_cg_resolution.md for interpretation.")
    print("ANALYSIS ONLY: does not constitute design release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
