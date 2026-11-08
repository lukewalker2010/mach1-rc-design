"""Constructive mass/CG closure candidates for R05.

Baseline rows are 18 §3.4. The empty-CG violation (1.0458 m vs 0.995 m)
requires a dry-moment reduction of 0.6083 kg*m. Doc 31 shows nose ballast
alone cannot fix both fuel states at the controlled tank station 0.45 m.
Moving the fuel centroid aft relaxes the full-fuel constraint; these
candidates quantify what that would require.

This is a decision input, NOT an approved layout: the tank station and
engine mount are controlled interfaces. Run:
    python3 tools/cg_candidates.py [--json]
"""
import argparse
import json

CG_MIN = 0.955
CG_MAX = 0.995
FUEL_KG = 1.62

# name: (mass kg, station m) — 18 §3.4
BASE = {
    "engine": (4.90, 1.20),
    "afterburner": (0.83, 1.48),
    "wing": (0.50, 1.00),
    "stabilator": (0.10, 2.35),
    "ventral_fin": (0.10, 2.30),
    "fuselage": (2.50, 1.30),
    "fuel": (FUEL_KG, 0.45),
    "fuel_system": (0.50, 0.60),
    "avionics": (0.90, 0.25),
    "landing": (0.35, 0.80),
    "nose_ballast": (1.00, 0.10),
    "misc": (0.30, 1.00),
}


def cg(rows, fuel_kg, fuel_station):
    dry_m = sum(m for k, (m, _) in rows.items() if k != "fuel")
    dry_mom = sum(m * x for k, (m, x) in rows.items() if k != "fuel")
    mass = dry_m + fuel_kg
    moment = dry_mom + fuel_kg * fuel_station
    return mass, moment, moment / mass


def in_band(mass, moment):
    c = moment / mass
    return CG_MIN <= c <= CG_MAX


def scenario(overrides, fuel_station, fuel_kg=FUEL_KG):
    rows = dict(BASE)
    rows.update(overrides)
    full = cg(rows, fuel_kg, fuel_station)
    empty = cg(rows, 0.0, fuel_station)
    return {
        "full": {"mass": full[0], "moment": full[1], "cg": full[2]},
        "empty": {"mass": empty[0], "moment": empty[1], "cg": empty[2]},
        "feasible": in_band(full[0], full[1]) and in_band(empty[0], empty[1]),
    }


def dry_cg(rows):
    m, mom, c = cg(rows, 0.0, 0.45)
    return m, mom, c


def min_tank_station(mass_total=13.60, fuel_kg=FUEL_KG):
    """Tank centroid needed to close both endpoints when dry CG = CG_MAX.

    From 18/31: M >= mf*(CG_MAX - x_f)/(CG_MAX - CG_MIN).
    """
    return CG_MAX - mass_total * (CG_MAX - CG_MIN) / fuel_kg


def build_candidates():
    md, momd, cgd = dry_cg(BASE)
    reduction = momd - CG_MAX * md  # kg*m forward moment needed

    # Candidate A: move tank to 0.66 m; add nose ballast so empty CG = 0.995.
    ballast_a = (momd - CG_MAX * md) / (CG_MAX - 0.10)
    a = scenario({"nose_ballast": (1.00 + ballast_a, 0.10)}, 0.66)

    # Candidate B: move tank to 0.66 m and engine forward so empty CG = 0.995.
    engine_dx = (momd - CG_MAX * md) / BASE["engine"][0]
    b = scenario({"engine": (BASE["engine"][0], BASE["engine"][1] - engine_dx)}, 0.66)

    # Candidate A-margin: empty CG 0.985, full CG 0.965 (20 mm inside band).
    ballast_m = (momd - 0.985 * md) / (0.985 - 0.10)
    rows_m = dict(BASE)
    rows_m["nose_ballast"] = (1.00 + ballast_m, 0.10)
    m_dry_m = sum(m for k, (m, _) in rows_m.items() if k != "fuel")
    mom_dry_m = sum(m * x for k, (m, x) in rows_m.items() if k != "fuel")
    tank_m = (0.965 * (m_dry_m + FUEL_KG) - mom_dry_m) / FUEL_KG
    am = scenario({"nose_ballast": (1.00 + ballast_m, 0.10)}, tank_m)

    return {
        "dry": {"mass": md, "moment": momd, "cg": cgd,
                "required_reduction": reduction,
                "min_tank_station_at_cgmax": min_tank_station()},
        "A": {"params": {"fuel_station": 0.66, "nose_ballast": 1.00 + ballast_a}, **a},
        "B": {"params": {"fuel_station": 0.66, "engine_station": BASE["engine"][1] - engine_dx}, **b},
        "A_margin": {"params": {"fuel_station": tank_m, "nose_ballast": 1.00 + ballast_m}, **am},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = build_candidates()
    if args.json:
        print(json.dumps(data, indent=2))
        return 0
    d = data["dry"]
    print(f"baseline dry CG            : {d['cg']:.6f} m  (limit {CG_MAX})")
    print(f"required forward reduction : {d['required_reduction']:.4f} kg*m")
    print(f"min tank station @ dry=CGmax: {d['min_tank_station_at_cgmax']:.4f} m\n")
    for key in ("A", "B", "A_margin"):
        s = data[key]
        p = s["params"]
        print(f"{key}: fuel@ {p['fuel_station']:.3f} m, "
              f"params { {k: round(v,4) for k,v in p.items() if k not in ('fuel_station',)} }")
        print(f"   full {s['full']['mass']:.3f} kg CG {s['full']['cg']:.4f} m | "
              f"empty {s['empty']['mass']:.3f} kg CG {s['empty']['cg']:.4f} m | "
              f"{'PASS' if s['feasible'] else 'FAIL'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
