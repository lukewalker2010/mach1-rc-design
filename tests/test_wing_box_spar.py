import csv
import unittest

from tools import wing_box_spar as wb
from tools.design_checks import point_inside, read_polylines


class BoxSparTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = wb.station_table()

    def test_root_contract_and_cap_force_stress(self):
        root = self.rows[0]
        self.assertAlmostEqual(root["moment_nm"], 150.0, places=6)
        self.assertAlmostEqual(root["width_mm"], 76.30, delta=0.02)
        self.assertAlmostEqual(root["separation_mm"], 4.92, delta=0.01)
        stress = root["moment_nm"] * 1000 / (
            root["separation_mm"] * root["cap_area_mm2"]
        )
        self.assertAlmostEqual(stress, wb.SIGMA_SENSITIVITY_MPA, places=5)

    def test_every_station_has_positive_fit(self):
        for row in self.rows:
            with self.subTest(station=row["station"]):
                self.assertGreater(row["separation_mm"], 0)
                self.assertGreater(row["inner_height_mm"], 0)
                self.assertGreaterEqual(row["width_mm"], wb.MIN_CAP_WIDTH_MM)
                self.assertGreater(row["box_le_mm"], 0)
                self.assertLess(row["box_te_mm"], row["chord_mm"])
                self.assertLess(row["box_le_mm"], row["box_te_mm"])
                self.assertLessEqual(row["width_mm"], 0.8 * row["chord_mm"])

    def test_tip_has_fit_not_zero_thickness(self):
        tip = self.rows[-1]
        self.assertAlmostEqual(tip["cap_thickness_mm"], 0.4, places=8)
        self.assertGreater(tip["inner_height_mm"], 1.0)

    def test_rib_segments_are_contained_without_spar_holes(self):
        for row in self.rows:
            c = row["chord_mm"]
            xs = [c * i / 100 for i in range(101)]
            envelope = (
                [(x, wb.airfoil_half_mm(c, x)) for x in xs]
                + [(x, -wb.airfoil_half_mm(c, x)) for x in reversed(xs)]
            )
            segments = wb.rib_segments(row)
            self.assertEqual(set(segments), {"front", "rear"})
            for side, polygon in segments.items():
                with self.subTest(station=row["station"], side=side):
                    outside = [p for p in polygon if not point_inside(p, envelope)]
                    self.assertEqual(outside, [])
                    twice_area = sum(
                        ax * by - bx * ay
                        for (ax, ay), (bx, by) in zip(
                            polygon, polygon[1:] + polygon[:1]
                        )
                    )
                    self.assertGreater(abs(twice_area), 1e-6)

    def test_committed_csv_and_dxf_match_candidate(self):
        csv_path = wb.OUT_DIR / "stations.csv"
        self.assertTrue(csv_path.exists())
        with csv_path.open(newline="") as stream:
            saved = list(csv.DictReader(stream))
        self.assertEqual(len(saved), len(self.rows))
        for row, saved_row in zip(self.rows, saved):
            self.assertEqual(row["station"], saved_row["station"])
            for side in ("front", "rear"):
                path = wb.OUT_DIR / f"rib_{row['station']}_{side}.dxf"
                contours = read_polylines(path)
                self.assertEqual(len(contours), 1)
                self.assertEqual(contours[0], wb.rib_segments(row)[side])


if __name__ == "__main__":
    unittest.main()
