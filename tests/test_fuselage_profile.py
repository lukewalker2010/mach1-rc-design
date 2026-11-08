import csv
import unittest

from tools import fuselage_profile as fp


class FuselageCandidateTests(unittest.TestCase):
    def test_endpoints_and_max(self):
        self.assertEqual(fp.radius(0.0), 0.0)
        self.assertAlmostEqual(fp.radius(2.60), 0.055, places=12)
        self.assertAlmostEqual(max(r for _, r in fp.stations()), 0.0925, places=12)

    def test_no_interior_pinch(self):
        data = fp.summarize()
        self.assertTrue(data["continuous"])
        self.assertGreater(data["min_interior_radius_m"], 0.0)

    def test_zero_slope_at_knots(self):
        for x, _ in fp.KNOTS:
            if x in (0.0, 2.60):
                continue
            self.assertAlmostEqual(fp.slope(x), 0.0, places=6)

    def test_station_table_shape(self):
        rows = fp.stations()
        self.assertEqual(len(rows), 53)
        self.assertEqual(rows[0][0], 0)
        self.assertEqual(rows[-1][0], 2600)
        self.assertTrue(all(b[0] - a[0] == 50 for a, b in zip(rows, rows[1:])))

    def test_committed_csv_matches_tool(self):
        path = fp.OUT_CSV
        self.assertTrue(path.exists(), path)
        with path.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 53)
        for row, (x_mm, r_m) in zip(rows, fp.stations()):
            self.assertEqual(int(row["x_mm"]), x_mm)
            self.assertAlmostEqual(float(row["R_mm"]), r_m * 1000, places=3)


if __name__ == "__main__":
    unittest.main()
