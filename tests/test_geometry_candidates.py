import csv
import math
import tempfile
import unittest
from pathlib import Path
from tools import geometry_candidates as g


class GeometryTests(unittest.TestCase):
    def test_area_mac_independent_quadrature(self):
        n = 10000
        dy = .475/n
        c = [g.wing_chord_at_y((i+.5)*dy) for i in range(n)]
        area = 2*sum(c)*dy
        self.assertAlmostEqual(area, .14, places=10)
        self.assertAlmostEqual(2*sum(v*v for v in c)*dy/area, g.WING_MAC_M, places=9)
        self.assertAlmostEqual(g.WING_EXPOSED_ROOT_CHORD_M, .1859279778393352)
        self.assertAlmostEqual(g.wing_area_exposed(), .1033279778393352)

    def test_sweep_translation_does_not_change_chord(self):
        y = .0925
        self.assertAlmostEqual(g.wing_le_station(y, .95)-.95, y/math.sqrt(3))
        self.assertEqual(g.wing_le_station(-y, .95), g.wing_le_station(y, .95))
        self.assertAlmostEqual(g.wing_chord_at_exposed_y(0), g.wing_chord_at_y(y))

    def test_c0_c1_all_junctions_and_derivative(self):
        for x, r in g.FUSE_KNOTS:
            self.assertAlmostEqual(g.fuse_radius(x), r, places=12)
            self.assertAlmostEqual(g.fuse_radius_derivative(x), 0, places=12)
        for x, _ in g.FUSE_KNOTS[1:-1]:
            h = 1e-7
            self.assertAlmostEqual(g.fuse_radius(x-h), g.fuse_radius(x+h), places=10)
            self.assertAlmostEqual(g.fuse_radius_derivative(x-h), g.fuse_radius_derivative(x+h), places=5)
        for i in range(1,2600):
            x = i/1000
            self.assertGreater(g.fuse_radius(x), 0)
            self.assertLessEqual(g.fuse_radius(x), .0925)
            h = 1e-7
            fd = (g.fuse_radius(x+h)-g.fuse_radius(x-h))/(2*h)
            self.assertAlmostEqual(fd, g.fuse_radius_derivative(x), places=6)

    def test_actual_packaging_failures_are_retained(self):
        self.assertFalse(g.engine_clearance_at_station(.3)["duct_fits"])
        self.assertFalse(g.engine_clearance_at_station(1.05)["engine_fits"])
        self.assertTrue(g.engine_clearance_at_station(1.39)["engine_fits"])
        self.assertFalse(g.wing_carry_through_clearance(1.05, 140, 140)["fits"])
        with self.assertRaises(TypeError):
            g.wing_carry_through_clearance(1.05)

    def test_finite_width_and_half_thickness(self):
        self.assertAlmostEqual(g.biconvex_half_thickness(90,.3,.06), 2.268)
        for s in (0,76.5,153,229.5,306,382.5):
            self.assertFalse(g.wing_spar_containment(s)["fits"])
            self.assertLess(g.wing_spar_hole_containment(s)["centre_margin_mm"], 0)
        self.assertFalse(g.stab_spar_hole_containment(120)["fits"])
        self.assertLess(g.stab_spar_hole_containment(120)["centre_margin_mm"], 0)
        self.assertTrue(g.stab_spar_hole_containment(0)["fits"])
        r = g.wing_spar_containment(0)
        self.assertAlmostEqual(r["available_separation_mm"], r["spar_depth_mm"]-2)

    def test_invalid_domains(self):
        for bad in (float("nan"), float("inf"), -1):
            for func in (g.fuse_radius, g.fuse_radius_derivative, g.wing_chord_at_y,
                         g.wing_chord_at_exposed_y, g.stab_chord_at_z):
                with self.subTest(func=func, bad=bad), self.assertRaises(ValueError):
                    func(bad)
        with self.assertRaises(ValueError):
            g.wing_spar_containment(382.5, 80)

    def test_exports_match_equations(self):
        with tempfile.TemporaryDirectory() as td:
            for export in (g.export_wing_stations_csv, g.export_fuse_stations_csv,
                           g.export_stab_stations_csv):
                p = Path(td)/"candidate.csv"
                export(p)
                with p.open() as f:
                    rows = list(csv.DictReader(f))
                self.assertTrue(rows)
                for row in rows:
                    if "radius_mm" in row:
                        self.assertAlmostEqual(float(row["radius_mm"]), g.fuse_radius(float(row["x_mm"])/1000)*1000, places=5)
                    if "span_from_fuse_mm" in row:
                        self.assertAlmostEqual(float(row["chord_mm"]), g.wing_chord_at_exposed_y(float(row["span_from_fuse_mm"]))*1000, places=5)
