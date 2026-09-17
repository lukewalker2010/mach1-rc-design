"""Principal integration tests: independent workstreams must describe one baseline."""
import unittest

from tools import geometry_candidates as geometry
from tools import loads_recovery as loads
from tools.design_checks import mass_rows, mass_state, semispan_load
from tools.hardware_budget import engine_supply_window
from tools.mass_mission import fuel_state_sweep


class WorkstreamConsistencyTests(unittest.TestCase):
    def test_geometry_and_loads_share_centreline_planform(self):
        plan = loads.wing_planform()
        self.assertAlmostEqual(plan["c_root_m"], geometry.WING_ROOT_CHORD_M)
        self.assertAlmostEqual(plan["c_tip_m"], geometry.WING_TIP_CHORD_M)
        self.assertAlmostEqual(plan["mac_m"], geometry.WING_MAC_M)
        for y in (0, 0.0925, 0.25, 0.475):
            self.assertAlmostEqual(loads.chord_at(y, plan), geometry.wing_chord_at_y(y))

    def test_integrated_loads_match_original_equilibrium(self):
        mass = mass_state(mass_rows())["mass_kg"]
        for n in (4, 6, 9):
            expected = semispan_load(mass, n)
            actual = loads.analytic_semispan(mass, n, loads.wing_planform(), "chord")
            self.assertAlmostEqual(actual["shear_n"], expected["shear_n"])
            self.assertAlmostEqual(actual["moment_nm"], expected["moment_nm"])

    def test_mission_and_screening_share_actual_mass_table(self):
        rows = mass_rows()
        for actual in fuel_state_sweep(rows, n_points=10):
            expected = mass_state(rows, actual["fuel_fraction"])
            for field in ("mass_kg", "moment_kg_m", "cg_m"):
                self.assertAlmostEqual(actual[field], expected[field])

    def test_engine_datasheet_invalidates_direct_2s_ecu_supply(self):
        for volts in (6.0, 7.4, 8.4):
            self.assertFalse(engine_supply_window(volts, volts)["voltage_window_compatible"])
        self.assertTrue(engine_supply_window(12, 24)["voltage_window_compatible"])
        self.assertFalse(engine_supply_window(12, 24)["physical_qualified"])
        self.assertFalse(engine_supply_window(12, 36)["voltage_window_compatible"])
        for low, high in ((0, 12), (12, 10), (float("nan"), 24)):
            with self.assertRaises(ValueError):
                engine_supply_window(low, high)


if __name__ == "__main__":
    unittest.main()
