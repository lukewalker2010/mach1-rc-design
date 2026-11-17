"""Feasible stabilator net-section candidate for R02/I-05.

Legacy geometry: 6% biconvex, root chord 90 mm, tip 38.571 mm, half-span
120 mm, hinge at 30% chord, 2.5 mm constant spar. A constant 2.5 mm hole
breaks out of the tip (half-thickness 0.972 mm < 1.25 mm radius) and the
8 mm bearing pockets cannot fit inside the section.

Candidate: keep the 6% section and 30% hinge line but taper a Ti-6Al-4V spar
from 2.5 mm at the root to 1.4 mm at the tip, and move the hinges into
external clevises outside the aerosurface. The section then contains only the
tapered spar hole, which fits at every station. Full-depth Ti laminate is
assumed to carry the surface loads; no strength or flutter qualification is
claimed.

Run: python3 tools/stabilator_candidate.py [--write]
"""
import argparse
import csv
import math
from pathlib import Path

if __package__:
    from .loads_recovery import section_depth_mm
else:
    from loads_recovery import section_depth_mm

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "proposals/structure/stabilator_candidate"
ROOT_CHORD_MM = 90.0
TIP_CHORD_MM = 90.0 * 15.0 / 35.0
HALF_SPAN_MM = 120.0
T_C = 0.06
HINGE_U = 0.30
ROOT_SPAR_MM = 2.5
TIP_SPAR_MM = 1.4
HOLE_CLEARANCE_MM = 0.1
STATIONS = (("STA_ROOT", 0.0), ("STA_MID", 60.0), ("STA_TIP", 120.0))


def chord_mm(z_mm):
    if not 0 <= z_mm <= HALF_SPAN_MM:
        raise ValueError("station outside half-span")
    return ROOT_CHORD_MM + (TIP_CHORD_MM - ROOT_CHORD_MM) * z_mm / HALF_SPAN_MM


def spar_diameter_mm(z_mm):
    if not 0 <= z_mm <= HALF_SPAN_MM:
        raise ValueError("station outside half-span")
    return ROOT_SPAR_MM + (TIP_SPAR_MM - ROOT_SPAR_MM) * z_mm / HALF_SPAN_MM


def half_thickness_mm(z_mm):
    return section_depth_mm(HINGE_U, chord_mm(z_mm), T_C) / 2


def section_fit(z_mm):
    c = chord_mm(z_mm)
    half = half_thickness_mm(z_mm)
    spar = spar_diameter_mm(z_mm)
    hole_radius = spar / 2 + HOLE_CLEARANCE_MM / 2
    margin = half - hole_radius
    return {
        "chord_mm": c,
        "max_section_thickness_mm": 2 * section_depth_mm(0.5, c, T_C) / 2,
        "hinge_thickness_mm": 2 * half,
        "spar_diameter_mm": spar,
        "hole_diameter_mm": 2 * hole_radius,
        "edge_margin_mm": margin,
        "fits": margin > 0,
    }


def section_contour(z_mm, n=21):
    c = chord_mm(z_mm)
    fracs = [i / (n - 1) for i in range(n)]
    upper = [(u * c, section_depth_mm(u, c, T_C) / 2) for u in fracs]
    lower = [(u * c, -section_depth_mm(u, c, T_C) / 2) for u in reversed(fracs)]
    return upper + lower


def spar_hole(z_mm, segs=40):
    c = chord_mm(z_mm)
    radius = spar_diameter_mm(z_mm) / 2 + HOLE_CLEARANCE_MM / 2
    cx = HINGE_U * c
    return [(cx + radius * math.cos(2 * math.pi * i / segs),
             radius * math.sin(2 * math.pi * i / segs)) for i in range(segs)]


def spar_volume_mm3():
    """One side, tapered-rod frustum integration in 1 mm steps."""
    volume = 0.0
    n = int(HALF_SPAN_MM)
    for i in range(n):
        z0, z1 = i, i + 1
        a0 = math.pi * (spar_diameter_mm(z0) / 2) ** 2
        a1 = math.pi * (spar_diameter_mm(z1) / 2) ** 2
        volume += (a0 + a1) / 2 * (z1 - z0)
    return volume


def write_outputs():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, z in STATIONS:
        fit = section_fit(z)
        rows.append({"section": name, "z_mm": z, **fit})
    with (OUT_DIR / "sections.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    try:
        import ezdxf
    except ImportError:
        return OUT_DIR / "sections.csv"
    for name, z in STATIONS:
        doc = ezdxf.new("R2010")
        msp = doc.modelspace()
        msp.add_lwpolyline(section_contour(z), format="xy", close=True)
        msp.add_lwpolyline(spar_hole(z), format="xy", close=True)
        doc.saveas(OUT_DIR / f"{name}.dxf")
    return OUT_DIR / "sections.csv"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.write:
        print(f"wrote {write_outputs().relative_to(ROOT)} and section DXFs")
    print("section   z    chord   t_max   t@30%   spar   hole   edge margin")
    for name, z in STATIONS:
        f = section_fit(z)
        print(f"{name:8s} {z:5.0f} {f['chord_mm']:7.2f} {f['max_section_thickness_mm']:7.3f} "
              f"{f['hinge_thickness_mm']:7.3f} {f['spar_diameter_mm']:6.2f} "
              f"{f['hole_diameter_mm']:6.2f} {f['edge_margin_mm']:9.3f}  "
              f"{'PASS' if f['fits'] else 'FAIL'}")
    print(f"Ti spar volume per side: {spar_volume_mm3():.1f} mm^3")
    print("External clevis assumed; strength/flutter not qualified.")
    return 0 if all(section_fit(z)["fits"] for _, z in STATIONS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
