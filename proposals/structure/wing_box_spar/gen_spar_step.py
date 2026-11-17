"""Generate the candidate wing box-spar STEP from tools/wing_box_spar.py.

Local wing coordinates: X = chord from leading edge, Y = span (0 centreline
to 475 mm tip), Z = vertical. The box is a hollow rectangular spar: upper and
lower caps plus two box-side shear walls, lofted through the seven sized
stations. No global wing mounting station is assumed (root LE remains an open
interface, 29 §R03).

Run from the repository root:
    python3 proposals/structure/wing_box_spar/gen_spar_step.py
"""
import sys
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.wing_box_spar import station_table  # noqa: E402

OUT = Path(__file__).resolve().parent / "wing_box_spar.step"


def rect_wire(y, x0, x1, z0, z1):
    points = [
        cq.Vector(x0, y, z0),
        cq.Vector(x1, y, z0),
        cq.Vector(x1, y, z1),
        cq.Vector(x0, y, z1),
    ]
    return cq.Wire.makePolygon(points, close=True)


def main():
    rows = station_table()
    outer_faces = []
    inner_faces = []
    for row in rows:
        y = row["y_m"] * 1000
        cx = 0.5 * row["chord_mm"]
        half_w = row["width_mm"] / 2
        half_h = row["outer_height_mm"] / 2
        outer_faces.append(rect_wire(y, cx - half_w, cx + half_w, -half_h, half_h))
        # cavity between the two shear walls and the two caps
        half_ci = row["cavity_width_mm"] / 2
        half_hi = row["inner_height_mm"] / 2
        inner_faces.append(rect_wire(y, cx - half_ci, cx + half_ci, -half_hi, half_hi))

    outer = cq.Solid.makeLoft(outer_faces, ruled=True)
    inner = cq.Solid.makeLoft(inner_faces, ruled=True)
    spar = cq.Workplane("XY").newObject([outer.cut(inner)])
    bb = spar.val().BoundingBox()
    print(f"spar bbox x[{bb.xmin:.1f},{bb.xmax:.1f}] y[{bb.ymin:.1f},{bb.ymax:.1f}] "
          f"z[{bb.zmin:.1f},{bb.zmax:.1f}] solids={len(spar.val().Solids())}")
    cq.exporters.export(spar, str(OUT))
    print(f"Exported {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
