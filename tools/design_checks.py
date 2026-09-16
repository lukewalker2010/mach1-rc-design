"""Reproducible checks against committed design artifacts, not a flight release.

Run from any directory: python3 /path/to/tools/design_checks.py [--strict]
Default exits zero on successful analysis, even for design failures. --strict
exits 1 on any failed check; malformed/missing inputs exit 2. No CAD dependencies.
"""
import argparse
import csv
from dataclasses import asdict, dataclass
import json
import math
from pathlib import Path

if __package__:
    from .airdata import pitot_ratio
else:
    from airdata import pitot_ratio

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    id: str
    passed: bool
    actual: float
    criterion: str
    source: str


def mass_rows(root=ROOT):
    """Read the authoritative component rows directly from 18 §3.4.

    Never use its hand-entered total as an input. Fail if the table is absent
    or malformed rather than silently running a different aircraft's analysis.
    """
    text = (root / "18_program_requirements.md").read_text(encoding="utf-8")
    section = text.split("### 3.4 Mass budget", 1)[1].split("## 4.", 1)[0]
    rows = []
    for line in section.splitlines():
        cells = [s.strip() for s in line.strip().strip("|").split("|")]
        if not line.startswith("|") or len(cells) != 4:
            continue
        if cells[0] == "Component" or cells[0].startswith(("---", "**Total")):
            continue
        mass, station = float(cells[1]), float(cells[2])
        if not all(math.isfinite(x) for x in (mass, station)) or mass <= 0 or not 0 <= station <= 2.6:
            raise ValueError(f"invalid mass row: {cells[0]}")
        rows.append((cells[0], mass, station))
    if len(rows) != 12 or len({r[0] for r in rows}) != 12:
        raise ValueError("expected 12 unique component rows in 18 §3.4; review parser after table changes")
    if sum(name.startswith("Fuel (") for name, _, _ in rows) != 1:
        raise ValueError("expected exactly one fuel row")
    return rows


def mass_state(rows, fuel_fraction=1.0):
    if not math.isfinite(fuel_fraction) or not 0 <= fuel_fraction <= 1:
        raise ValueError("fuel fraction must be in [0, 1]")
    masses = [(m * (fuel_fraction if n.startswith("Fuel (") else 1), x) for n, m, x in rows]
    mass = sum(m for m, _ in masses)
    moment = sum(m * x for m, x in masses)
    return {"mass_kg": mass, "moment_kg_m": moment, "cg_m": moment / mass}


def semispan_load(mass_kg, n, span_m=0.95, taper=0.4):
    """Centreline cantilever, chord-proportional lift, no tail/inertial relief.

    Each half-wing carries n*W/2. Not the joint at the fuselage side and not a
    complete structural load envelope (torsion, gusts and tail trim remain open).
    """
    if not all(math.isfinite(x) and x > 0 for x in (mass_kg, n, span_m)) or not 0 <= taper <= 1:
        raise ValueError("invalid wing load inputs")
    shear = n * mass_kg * 9.81 / 2
    centroid = span_m / 2 * (1 + 2 * taper) / (3 * (1 + taper))
    return {"shear_n": shear, "moment_nm": shear * centroid, "centroid_m": centroid}


def read_polylines(path):
    """Read closed, straight LWPOLYLINEs from the existing ASCII DXF entities.

    Deliberately narrow audit reader: unsupported entities/bulges fail rather
    than being approximated. This is not a general DXF/CAD validator.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) % 2:
        raise ValueError(f"truncated DXF: {path}")
    pairs = [(int(lines[i].strip()), lines[i + 1].strip()) for i in range(0, len(lines), 2)]
    entities, active, current, point_x = [], False, None, None
    for i, (code, value) in enumerate(pairs):
        if (code, value) == (2, "ENTITIES") and i and pairs[i - 1] == (0, "SECTION"):
            active = True
            continue
        if not active:
            continue
        if code == 0:
            if current is not None:
                if not current["closed"] or current["count"] != len(current["points"]) or point_x is not None:
                    raise ValueError(f"invalid/open polyline in {path}")
                points = current["points"]
                twice_area = sum(ax * by - bx * ay for (ax, ay), (bx, by) in zip(points, points[1:] + points[:1]))
                if len(set(points)) < 3 or abs(twice_area) < 1e-8:
                    raise ValueError(f"degenerate polyline in {path}")
                entities.append(current["points"])
            if value == "ENDSEC":
                return entities
            if value != "LWPOLYLINE":
                raise ValueError(f"unsupported entity {value} in {path}")
            current = {"points": [], "closed": False, "count": 0}
            continue
        if current is None:
            raise ValueError(f"invalid ENTITIES section in {path}")
        if code == 70:
            current["closed"] = bool(int(value) & 1)
        elif code == 90:
            current["count"] = int(value)
        elif code == 42 and float(value) != 0:
            raise ValueError(f"bulged polyline in {path}")
        elif code == 10:
            if point_x is not None:
                raise ValueError(f"missing vertex y-coordinate in {path}")
            point_x = float(value)
        elif code == 20:
            if point_x is None or not all(math.isfinite(v) for v in (point_x, float(value))):
                raise ValueError(f"invalid vertex in {path}")
            current["points"].append((point_x, float(value)))
            point_x = None
    raise ValueError(f"missing ENTITIES end in {path}")


def point_inside(point, polygon):
    """Even/odd polygon containment, boundaries accepted within 1e-8 mm."""
    x, y = point
    inside = False
    for (ax, ay), (bx, by) in zip(polygon, polygon[1:] + polygon[:1]):
        dx, dy = bx - ax, by - ay
        length = math.hypot(dx, dy)
        if length and abs(dx * (y - ay) - dy * (x - ax)) / length < 1e-8:
            if min(ax, bx) - 1e-8 <= x <= max(ax, bx) + 1e-8 and min(ay, by) - 1e-8 <= y <= max(ay, by) + 1e-8:
                return True
        if (ay > y) != (by > y) and x < ax + (y - ay) * dx / dy:
            inside = not inside
    return inside


def evaluate(root=ROOT):
    checks = []

    def add(id, passed, actual, criterion, source):
        checks.append(Check(id, bool(passed), float(actual), criterion, source))

    rows = mass_rows(root)
    for fraction, name in [(1, "FULL"), (0, "EMPTY")]:
        state = mass_state(rows, fraction)
        add(f"CG-{name}", 0.955 <= state["cg_m"] <= 0.995, state["cg_m"],
            "0.955 <= CG <= 0.995 m", "18 §3.4 component rows; AGENTS §2")
    full = mass_state(rows)
    add("MTOW", full["mass_kg"] <= 25, full["mass_kg"], "mass <= 25 kg", "18 §1 C1")

    # Inspect the actual current DXF holes, not an idealised regenerated shape.
    dxf = root / "wing_manufacturing/dxf"
    for name in [f"wing_rib_R{i}" for i in range(6)] + ["STA_ROOT", "STA_MID", "STA_TIP"]:
        contours = read_polylines(dxf / f"{name}.dxf")
        expected = 3 if name.startswith("wing") else 2
        if len(contours) != expected:
            raise ValueError(f"{name}: expected {expected} contours; update audit for new drawing revision")
        # Wing: hole must fit inside web, not merely the outer mould line.
        envelope = contours[1] if expected == 3 else contours[0]
        outside = sum(not point_inside(p, envelope) for p in contours[-1])
        add(f"HOLE-{name}", outside == 0, outside, "0 hole vertices outside material envelope",
            f"wing_manufacturing/dxf/{name}.dxf")

    with (root / "wing_manufacturing/rib_coordinates_v2.csv").open(newline="") as stream:
        rib_rows = list(csv.DictReader(stream))
    sections = {}
    for row in rib_rows:
        sections[row["rib"]] = (float(row["span_y_mm"]), float(row["chord_mm"]))
    if len(sections) != 6:
        raise ValueError("expected six wing rib stations")
    stations = sorted(sections.values())
    # Documented y=0 at fuselage side: extend root chord through hidden centre.
    area = (2 * sum((y2-y1)*(c1+c2)/2 for (y1,c1),(y2,c2) in zip(stations, stations[1:]))
            + 185 * stations[0][1]) / 1e6
    add("WING-AREA", math.isclose(area, 0.14, rel_tol=0.01), area,
        "within 1% of 0.14 m² (audit tolerance)", "rib_coordinates_v2.csv + generator side-root convention; 18 §3.2")

    # Doc 20's proposed cap-centroid spacing; even centre chord location fails.
    depth = 0.04 * stations[0][1] * 4 * 0.3 * 0.7
    max_sep = depth - 2 * 0.5 - 1.0  # skin offset each side; cap centroid thickness
    add("SPAR-FIT", max_sep >= 7, max_sep, "available cap-centroid separation >= 7 mm",
        "20 §2 (1 mm caps); gen_wing_ribs.py 0.5 mm offset, parabolic section")

    # Audit the committed mould table: internal zero radius severs the fuselage.
    table = (root / "fuselage_manufacturing/01_mould_coordinates.md").read_text()
    table = table.split("### 1.5 Master station", 1)[1].split("### 1.6", 1)[0]
    radii = []
    for line in table.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 3 and cells[0].isdigit():
            x, r, _ = map(float, cells)
            if 0 < x < 2600:
                radii.append(r)
    if len(radii) != 51:
        raise ValueError("expected 51 interior mould stations")
    add("FUSE-CONTINUITY", min(radii) > 0, min(radii), "all interior radii > 0 mm",
        "fuselage_manufacturing/01_mould_coordinates.md §1.5")

    for mach in (1.0, 1.1):
        impact = 69700 * (pitot_ratio(mach) - 1)
        add(f"PITOT-M{mach:.1f}", impact <= 3447, impact, "qc <= 3447 Pa (23 specified range)",
            "23 §1; 18 §2.1 static 69700 Pa; tools/airdata.py")
    cl_landing = full["mass_kg"] * 9.81 / (0.5 * 1.225 * 30**2 * 0.14)
    add("LANDING-LIFT", cl_landing <= 0.8, cl_landing,
        "required CL <= 0.8 (screening assumption, NOT measured CLmax)",
        "18 §5.4 speed 30 m/s, §3.2 area; sea-level density 1.225 kg/m³")
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        checks = evaluate()
    except (OSError, ValueError, IndexError, KeyError) as exc:
        parser.exit(2, f"Input error: {exc}\n")
    if args.json:
        print(json.dumps({"scope": "design screening, not release", "checks": [asdict(c) for c in checks]}, indent=2, allow_nan=False))
    else:
        for c in checks:
            print(f"{'PASS' if c.passed else 'FAIL'} {c.id}: {c.actual:.6g}; {c.criterion}\n  {c.source}")
        print("Design screening only: passing checks do not constitute manufacturing or flight release.")
    return int(args.strict and any(not c.passed for c in checks))


if __name__ == "__main__":
    raise SystemExit(main())
