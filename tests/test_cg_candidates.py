import unittest

from tools import cg_candidates as cc


class CgCandidateTests(unittest.TestCase):
    def test_baseline_reproduces_doc31(self):
        m, mom, c = cc.dry_cg(cc.BASE)
        self.assertAlmostEqual(m, 11.98, places=6)
        self.assertAlmostEqual(mom, 12.5284, places=6)
        self.assertAlmostEqual(c, 1.045776, places=6)
        full = cc.cg(cc.BASE, 1.62, 0.45)
        self.assertAlmostEqual(full[2], 0.974809, places=6)
        self.assertTrue(cc.in_band(*full[:2]))  # full state is in band
        empty = cc.cg(cc.BASE, 0.0, 0.45)
        self.assertFalse(cc.in_band(*empty[:2]))  # empty state is not

    def test_required_reduction_and_tank_station(self):
        data = cc.build_candidates()
        self.assertAlmostEqual(data["dry"]["required_reduction"], 0.6083, places=4)
        self.assertAlmostEqual(
            data["dry"]["min_tank_station_at_cgmax"], 0.6592, places=4
        )

    def test_candidates_close_both_endpoints(self):
        data = cc.build_candidates()
        for key in ("A", "B", "A_margin"):
            self.assertTrue(data[key]["feasible"], key)
            for state in ("full", "empty"):
                cg = data[key][state]["cg"]
                self.assertGreaterEqual(cg, cc.CG_MIN, (key, state))
                self.assertLessEqual(cg, cc.CG_MAX, (key, state))

    def test_candidate_details(self):
        data = cc.build_candidates()
        self.assertAlmostEqual(data["A"]["full"]["cg"], 0.9570, places=4)
        self.assertAlmostEqual(data["A"]["empty"]["cg"], 0.9950, places=4)
        self.assertAlmostEqual(data["B"]["params"]["engine_station"], 1.0759, places=4)
        self.assertAlmostEqual(data["B"]["full"]["mass"], 13.60, places=6)
        self.assertAlmostEqual(data["A_margin"]["full"]["cg"], 0.9650, places=4)
        self.assertAlmostEqual(data["A_margin"]["empty"]["cg"], 0.9850, places=4)


if __name__ == "__main__":
    unittest.main()
