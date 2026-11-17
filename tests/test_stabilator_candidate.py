import csv
import unittest

from tools import stabilator_candidate as sc
from tools.design_checks import point_inside, read_polylines


class StabilatorCandidateTests(unittest.TestCase):
    def test_section_geometry_matches_baseline(self):
        self.assertAlmostEqual(sc.chord_mm(0), 90.0)
        self.assertAlmostEqual(sc.chord_mm(120), 90 * 15 / 35, places=9)
        self.assertAlmostEqual(sc.section_fit(0)["max_section_thickness_mm"], 5.4, places=9)
        self.assertAlmostEqual(sc.section_fit(120)["max_section_thickness_mm"], 2.314, places=3)
        self.assertAlmostEqual(sc.section_fit(120)["hinge_thickness_mm"], 1.944, places=3)

    def test_tapered_spar_fits_all_stations(self):
        for name, z in sc.STATIONS:
            fit = sc.section_fit(z)
            with self.subTest(section=name):
                self.assertTrue(fit["fits"])
                self.assertGreater(fit["edge_margin_mm"], 0.2)
        self.assertAlmostEqual(sc.spar_diameter_mm(0), 2.5)
        self.assertAlmostEqual(sc.spar_diameter_mm(120), 1.4)

    def test_tip_hole_is_the_former_failure_boundary(self):
        # Constant 2.5 mm spar at the tip: radius 1.25 > half-thickness 0.972.
        half = sc.half_thickness_mm(120)
        self.assertAlmostEqual(half, 0.972, places=3)
        self.assertGreater(1.25, half)
        self.assertLess(sc.section_fit(120)["hole_diameter_mm"] / 2, half)

    def test_committed_sections_and_dxf(self):
        csv_path = sc.OUT_DIR / "sections.csv"
        self.assertTrue(csv_path.exists())
        with csv_path.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual([r["section"] for r in rows], [n for n, _ in sc.STATIONS])
        for name, z in sc.STATIONS:
            outline = sc.section_contour(z)
            hole = sc.spar_hole(z)
            contours = read_polylines(sc.OUT_DIR / f"{name}.dxf")
            self.assertEqual(len(contours), 2)  # outer skin + spar hole, no bearing pockets
            self.assertEqual(contours[0], outline)
            self.assertEqual(contours[1], hole)
            outside = [p for p in hole if not point_inside(p, outline)]
            self.assertEqual(outside, [])

    def test_tapered_spar_volume_is_small(self):
        self.assertAlmostEqual(sc.spar_volume_mm3(), 367.9, delta=0.2)


if __name__ == "__main__":
    unittest.main()
