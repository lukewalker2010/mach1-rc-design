from pathlib import Path
import tempfile
import unittest

from tools.design_checks import evaluate, mass_rows, mass_state, point_inside, read_polylines, semispan_load


class DesignTests(unittest.TestCase):
    def test_mass_conservation_and_fuel_excursion(self):
        rows = mass_rows()
        full, empty = mass_state(rows), mass_state(rows, 0)
        self.assertAlmostEqual(full["mass_kg"], 13.6)
        self.assertAlmostEqual(full["moment_kg_m"], 13.2574)
        self.assertAlmostEqual(full["mass_kg"] - empty["mass_kg"], 1.62)
        self.assertAlmostEqual(full["moment_kg_m"] - empty["moment_kg_m"], 1.62 * 0.45)
        self.assertGreater(empty["cg_m"], 0.995)

    def test_wing_equilibrium_reference_cases(self):
        # Uniform half-wing: centroid at b/4. Triangular: at b/6.
        for taper, centroid in [(1, 0.95 / 4), (0, 0.95 / 6)]:
            load = semispan_load(13.6, 6, taper=taper)
            self.assertAlmostEqual(2 * load["shear_n"], 6 * 13.6 * 9.81)
            self.assertAlmostEqual(load["moment_nm"], load["shear_n"] * centroid)

    def test_containment_boundary_and_outside(self):
        polygon = [(0, 0), (2, 0), (2, 2), (0, 2)]
        for point in [(1, 1), (0, 1), (2, 2)]:
            self.assertTrue(point_inside(point, polygon))
        self.assertFalse(point_inside((3, 1), polygon))

    def test_actual_artifacts_expose_known_blockers(self):
        checks = {c.id: c for c in evaluate()}
        for id in ("CG-EMPTY", "FUSE-CONTINUITY", "HOLE-wing_rib_R5", "HOLE-STA_TIP", "SPAR-FIT", "PITOT-M1.0"):
            self.assertFalse(checks[id].passed, id)
        self.assertTrue(checks["CG-FULL"].passed)

    def test_truncated_dxf_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.dxf"
            path.write_text("0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n10\n")
            with self.assertRaises(ValueError):
                read_polylines(path)

    def test_empty_closed_dxf_is_not_a_valid_part(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.dxf"
            path.write_text("0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n90\n0\n70\n1\n0\nENDSEC\n0\nEOF\n")
            with self.assertRaises(ValueError):
                read_polylines(path)


if __name__ == "__main__":
    unittest.main()
