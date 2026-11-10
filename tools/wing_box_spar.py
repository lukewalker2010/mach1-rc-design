"""Fit-first closed box-spar candidate for R02/R03/R04.

The rejected 50 mm cap at 30% chord cannot fit a 4% biconvex wing. This
candidate puts the spar at maximum thickness (50% chord), sizes cap width
iteratively from the actual moment and available cap-centroid separation,
and uses front/rear rib segments outside the closed spar box instead of
impossible round spar holes. The box has upper/lower caps and two shear webs
at its chordwise edges, so it also provides a closed torsion cell.

Conservative load screen: chord-proportional lift, 9g centreline distribution
scaled so the centreline root moment is at least the 150 N.m interface
reference. Sigma=400 MPa is an INPUT SENSITIVITY, not a laminate allowable.
Skin=0.5 mm and bond=0.2 mm per face are retained from doc 30. No strength,
buckling, fatigue, bonded-joint or flutter qualification is claimed.

Run: python3 tools/wing_box_spar.py [--write]
"""
import argparse
import csv
import math
from pathlib import Path

if __package__:
    from .loads_recovery import (
        beam_loads, cap_centroid_separation_mm, required_cap_area_mm2,
        section_depth_mm, wing_planform,
    )
else:
    from loads_recovery import (
        beam_loads, cap_centroid_separation_mm, required_cap_area_mm2,
        section_depth_mm, wing_planform,
    )

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "proposals/structure/wing_box_spar"
MASS_KG = 13.60
ROOT_CONTRACT_NM = 150.0
SIGMA_SENSITIVITY_MPA = 400.0
SKIN_MM = 0.5
BOND_MM = 0.2
WEB_THICK_MM = 1.0  # each of the two box-side shear walls
MIN_CAP_WIDTH_MM = 2.0
SPAR_U = 0.50
STATIONS = (
    ("C0", 0.0),
    ("R0", 0.0925),
    ("R1", 0.0925 + 0.3825 / 5),
    ("R2", 0.0925 + 2 * 0.3825 / 5),
    ("R3", 0.0925 + 3 * 0.3825 / 5),
    ("R4", 0.0925 + 4 * 0.3825 / 5),
    ("R5", 0.475),
)


def cap_thickness_mm(y_m):
    """Proposed taper: 1.0 mm at centreline to 0.4 mm at the tip."""
    if not 0 <= y_m <= 0.475:
        raise ValueError("station outside half-span")
    return 1.0 - 0.6 * y_m / 0.475


def design_loads():
    pf = wing_planform(root_cut_m=0.0)
    result = beam_loads(MASS_KG, 9, pf, "chord")
    scale = max(1.0, ROOT_CONTRACT_NM / result["root_moment_nm"])
    return result, scale


def chord_mm_at(y_m):
    pf = wing_planform(root_cut_m=0.0)
    half = pf["semi_m"]
    return 1000 * (pf["c_root_m"] + (pf["c_tip_m"] - pf["c_root_m"]) * y_m / half)


def size_cap(moment_nm, chord_mm, cap_thick_mm, sigma_mpa=SIGMA_SENSITIVITY_MPA):
    """Iterate cap width because available separation depends on its footprint."""
    if moment_nm < 0 or not math.isfinite(moment_nm):
        raise ValueError("moment must be finite and nonnegative")
    width = MIN_CAP_WIDTH_MM
    for _ in range(100):
        fit = cap_centroid_separation_mm(
            SPAR_U, width, chord_mm, skin_mm=SKIN_MM,
            bond_mm=BOND_MM, cap_thick_mm=cap_thick_mm,
        )
        if fit["separation_mm"] <= 0:
            raise ValueError("cap/skin/bond stack leaves no positive separation")
        required = max(
            MIN_CAP_WIDTH_MM,
            required_cap_area_mm2(moment_nm, fit["separation_mm"], sigma_mpa) / cap_thick_mm,
        )
        if abs(required - width) < 1e-10:
            width = required
            break
        width = required
    else:
        raise RuntimeError("cap sizing did not converge")
    fit = cap_centroid_separation_mm(
        SPAR_U, width, chord_mm, skin_mm=SKIN_MM,
        bond_mm=BOND_MM, cap_thick_mm=cap_thick_mm,
    )
    inner_height = fit["outer_depth_mm"] - 2 * (SKIN_MM + BOND_MM + cap_thick_mm)
    if inner_height <= 0:
        raise ValueError("box inner height is not positive")
    if width > 0.8 * chord_mm:
        raise ValueError("cap footprint leaves impractical leading/trailing ribs")
    return {
        "width_mm": width,
        "cap_area_mm2": width * cap_thick_mm,
        "separation_mm": fit["separation_mm"],
        "outer_depth_mm": fit["outer_depth_mm"],
        "inner_height_mm": inner_height,
        "box_le_mm": (SPAR_U * chord_mm - width / 2),
        "box_te_mm": (SPAR_U * chord_mm + width / 2),
        "u_lo": fit["u_lo"],
        "u_hi": fit["u_hi"],
    }


def station_table():
    loads, scale = design_loads()
    rows = []
    for name, target in STATIONS:
        index = min(range(len(loads["y"])), key=lambda i: abs(loads["y"][i] - target))
        y = loads["y"][index]
        chord = chord_mm_at(y)
        moment = loads["moment"][index] * scale
        shear = loads["shear"][index] * scale
        cap_t = cap_thickness_mm(y)
        cap = size_cap(moment, chord, cap_t)
        web_area = 2 * cap["inner_height_mm"] * WEB_THICK_MM
        rows.append({
            "station": name,
            "y_m": y,
            "chord_mm": chord,
            "moment_nm": moment,
            "shear_n": shear,
            "cap_thickness_mm": cap_t,
            "web_area_mm2": web_area,
            "web_shear_mpa": shear / web_area,
            **cap,
        })
    return rows


def cap_volume_mm3():
    """Upper+lower cap volume for one half-wing, by station trapezoids."""
    rows = station_table()
    volume = 0.0
    for a, b in zip(rows, rows[1:]):
        dy = (b["y_m"] - a["y_m"]) * 1000
        area_a = a["width_mm"] * a["cap_thickness_mm"]
        area_b = b["width_mm"] * b["cap_thickness_mm"]
        volume += 2 * (area_a + area_b) / 2 * dy
    return volume


def airfoil_half_mm(chord_mm, x_mm):
    if not 0 <= x_mm <= chord_mm:
        raise ValueError("x outside chord")
    return section_depth_mm(x_mm / chord_mm, chord_mm) / 2


def web_half_mm(chord_mm, x_mm):
    return max(airfoil_half_mm(chord_mm, x_mm) - SKIN_MM, 0.0)


def rib_segments(row, points_per_side=41):
    """Front/rear closed net-rib contours outside the spar box; no spar hole."""
    chord = row["chord_mm"]
    front_end = row["box_le_mm"] - WEB_THICK_MM / 2
    rear_start = row["box_te_mm"] + WEB_THICK_MM / 2
    if not 0 < front_end < rear_start < chord:
        raise ValueError("spar box leaves invalid rib segments")

    def xs(a, b):
        return [a + (b - a) * i / (points_per_side - 1) for i in range(points_per_side)]

    def closed_segment(a, b):
        xs_ = xs(a, b)
        upper = [(x, web_half_mm(chord, x)) for x in xs_]
        lower = [(x, -web_half_mm(chord, x)) for x in reversed(xs_)]
        return upper + lower

    return {"front": closed_segment(0.0, front_end),
            "rear": closed_segment(rear_start, chord)}


def point_inside(point, polygon):
    x, y = point
    inside = False
    for (x1, y1), (x2, y2) in zip(polygon, polygon[1:] + polygon[:1]):
        if (y1 > y) != (y2 > y):
            cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < cross:
                inside = not inside
    return inside


def write_outputs():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = station_table()
    fields = list(rows[0])
    with (OUT_DIR / "stations.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    try:
        import ezdxf
    except ImportError:
        return OUT_DIR / "stations.csv"
    for row in rows:
        for side, polygon in rib_segments(row).items():
            doc = ezdxf.new("R2010")
            doc.modelspace().add_lwpolyline(polygon, format="xy", close=True)
            doc.saveas(OUT_DIR / f"rib_{row['station']}_{side}.dxf")
    return OUT_DIR / "stations.csv"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.write:
        print(f"wrote {write_outputs().relative_to(ROOT)} and front/rear rib DXFs")
    print("station   chord    M(9g/150)  cap_t  width  sep    box inner  web tau")
    for r in station_table():
        print(f"{r['station']:4s} {r['chord_mm']:8.2f} {r['moment_nm']:9.2f} "
              f"{r['cap_thickness_mm']:6.2f} {r['width_mm']:7.2f} "
              f"{r['separation_mm']:6.2f} {r['inner_height_mm']:8.2f} "
              f"{r['web_shear_mpa']:9.2f}")
    print(f"Cap volume, both wings: {2 * cap_volume_mm3() / 1000:.2f} cm^3")
    print("SENSITIVITY ONLY: sigma=400 MPa input, not a qualified allowable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
