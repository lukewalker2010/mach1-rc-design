"""Mach 1 RC - net-part rib / stabilator section generator (E5).

Regenerates wing rib DXF + CSV and stabilator STA DXF from the
authoritative re-baselined geometry (18_program_requirements.md s3.2/s3.3,
audit dispositions D14/D22). Every DXF contains only LWPOLYLINE entities.

Wing (biconvex 4% t/c, box spar hole 6 mm @ 30% chord):
    exposed half-span  = b/2 - R_fuse = 475 - 92.5 = 382.5 mm
    chord(y)  = 210 - (210 - 84) / 382.5 * y        [mm, y from fuselage side]
    thickness t = 0.04 * c
    airfoil   y(x) = (t/2) * 4 * (x/c) * (1 - x/c), max thickness at x/c = 0.50
    web       = outer contour offset inward 0.5 mm (vertical-normal approx),
               clamped to the camberline where the offset exceeds the local
               half-thickness (LE/TE knife edge; 3 mm flange bridges the skin bond)
    ribs      R0..R5 equally spaced every 76.5 mm from the fuselage side

Stabilator (biconvex 6% t/c, Ti 2.5 mm spar hole @ 30% chord):
    root chord 90 mm, tip chord = 90 * 15/35 = 38.571 mm (taper 0.4286),
    half-span 120 mm; C(z) = 90 - 51.4286 * z/120 ; t = 0.06 * C(z)

Run: /tmp/opencode/cq312/bin/python wing_manufacturing/gen_wing_ribs.py
"""

import math
import os

import ezdxf

HERE = os.path.dirname(os.path.abspath(__file__))
DXF_DIR = os.path.join(HERE, "dxf")
CSV_OUT = os.path.join(HERE, "rib_coordinates_v2.csv")

N_STATIONS = 21                 # 0..100% chord in 5% steps
WEB_OFFSET_MM = 0.5             # 0.5 mm carbon web, offset from outer skin
SPAR_HOLE_DIA_MM = 6.0          # box spar pass-through (18 s3.2)
STAB_SPAR_DIA_MM = 2.5          # Ti spar (18 s3.3)

WING_T_C = 0.04
STAB_T_C = 0.06

RIB_SPANS = [0.0, 76.5, 153.0, 229.5, 306.0, 382.5]   # mm from fuselage side
RIB_NAMES = [f"R{i}" for i in range(6)]

STAB_SECTIONS = [
    ("STA_ROOT", 0.0),          # span station z = 0 (root)
    ("STA_MID", 60.0),          # z = 60 mm (mid-span)
    ("STA_TIP", 120.0),         # z = 120 mm (tip)
]


def wing_chord(y_mm):
    return 210.0 - (210.0 - 84.0) / 382.5 * y_mm


def stab_chord(z_mm):
    return 90.0 - (90.0 - 90.0 * 15.0 / 35.0) / 120.0 * z_mm


def airfoil_y(c, xc, t_c):
    """Biconvex half-thickness at normalised chord station xc.

    y = (t/2) * 4 * xc * (1 - xc),  t = t_c * c.
    Max thickness (t/2) at xc = 0.50.
    """
    t = t_c * c
    return (t / 2.0) * 4.0 * xc * (1.0 - xc)


def outer_contour(c, t_c, n=N_STATIONS):
    """Closed outer airfoil contour points, LE -> upper -> TE -> lower -> LE."""
    fracs = [i / (n - 1) for i in range(n)]
    upper = [(xc * c, airfoil_y(c, xc, t_c)) for xc in fracs]
    lower = [(xc * c, -airfoil_y(c, xc, t_c)) for xc in reversed(fracs)]
    return upper + lower


def web_contour(c, t_c, n=N_STATIONS):
    """Inner web contour: outer contour offset inward by WEB_OFFSET_MM.

    Vertical-normal approximation: for this airfoil the surface slope is at most
    2*t/c = 0.08 (4.6 deg), so the perpendicular offset differs from the vertical
    offset by < 0.3%. Where the offset exceeds the local half-thickness (LE/TE,
    increasingly toward the tip) the web is clamped to the camberline so the
    net part is a valid closed contour that tapers to a point at LE/TE.
    """
    fracs = [i / (n - 1) for i in range(n)]
    upper = []
    lower = []
    for xc in fracs:
        y = airfoil_y(c, xc, t_c)
        upper.append((xc * c, max(y - WEB_OFFSET_MM, 0.0)))
        lower.append((xc * c, min(-y + WEB_OFFSET_MM, 0.0)))
    return upper + list(reversed(lower))


def spar_hole_points(c, dia_mm, segs=32):
    """Closed LWPOLYLINE circle approximation, hole centre at 30% chord."""
    r = dia_mm / 2.0
    cx = 0.30 * c
    return [(cx + r * math.cos(2.0 * math.pi * i / segs),
             r * math.sin(2.0 * math.pi * i / segs)) for i in range(segs)]


def write_wing_rib_dxf(name, span_y):
    c = wing_chord(span_y)
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    msp.add_lwpolyline(outer_contour(c, WING_T_C), format="xy", close=True)
    msp.add_lwpolyline(web_contour(c, WING_T_C), format="xy", close=True)
    msp.add_lwpolyline(spar_hole_points(c, SPAR_HOLE_DIA_MM), format="xy", close=True)
    doc.saveas(os.path.join(DXF_DIR, f"wing_rib_{name}.dxf"))


def write_sta_dxf(name, z):
    c = stab_chord(z)
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()
    msp.add_lwpolyline(outer_contour(c, STAB_T_C), format="xy", close=True)
    msp.add_lwpolyline(spar_hole_points(c, STAB_SPAR_DIA_MM), format="xy", close=True)
    doc.saveas(os.path.join(DXF_DIR, f"{name}.dxf"))


def write_rib_csv():
    rows = ["rib,span_y_mm,chord_mm,x_frac,upper_outer_y_mm,lower_outer_y_mm,"
            "upper_web_y_mm,lower_web_y_mm,spar_hole_dia_mm"]
    for name, span in zip(RIB_NAMES, RIB_SPANS):
        c = wing_chord(span)
        for i in range(N_STATIONS):
            xc = i / (N_STATIONS - 1)
            yo = airfoil_y(c, xc, WING_T_C)
            ywu = max(yo - WEB_OFFSET_MM, 0.0)
            ywl = min(-yo + WEB_OFFSET_MM, 0.0)
            rows.append(f"{name},{span:.1f},{c:.1f},{xc:.2f},"
                        f"{yo:.4f},{-yo:.4f},{ywu:.4f},{ywl:.4f},"
                        f"{SPAR_HOLE_DIA_MM:.1f}")
    with open(CSV_OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")


def summary():
    print("=== wing ribs (biconvex 4% t/c, web offset 0.5 mm, spar hole 6 mm @ 30% chord) ===")
    for name, span in zip(RIB_NAMES, RIB_SPANS):
        c = wing_chord(span)
        print(f"{name}: span_y={span:6.1f} mm  chord={c:6.1f} mm  "
              f"t_max={0.04 * c:5.2f} mm  t/c=4%  spar_x={0.30 * c:6.1f} mm")
    print("=== stabilator sections (biconvex 6% t/c, spar hole 2.5 mm @ 30% chord) ===")
    for name, z in STAB_SECTIONS:
        c = stab_chord(z)
        print(f"{name}: z={z:5.1f} mm  chord={c:6.3f} mm  t_max={0.06 * c:5.3f} mm")


def main():
    os.makedirs(DXF_DIR, exist_ok=True)
    for name, span in zip(RIB_NAMES, RIB_SPANS):
        write_wing_rib_dxf(name, span)
    for name, z in STAB_SECTIONS:
        write_sta_dxf(name, z)
    write_rib_csv()
    summary()


if __name__ == "__main__":
    main()
