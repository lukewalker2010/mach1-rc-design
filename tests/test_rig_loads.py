"""Analytic regression cases, not measured rig/fastener qualification."""

import math
import unittest

from tools import rig_loads as rig


class RigLoadsTests(unittest.TestCase):
    def test_biaxial_unsymmetric_group_all_six_equilibria(self):
        coords = [rig.BoltCoord("a", 1, 2), rig.BoltCoord("b", 4, 3),
                  rig.BoltCoord("c", 2, 7), rig.BoltCoord("d", 6, 8)]
        loads = (110, 42, -71, 83, -29, 93)
        result = rig.bolt_group_loads(coords, *loads)
        for actual, expected in zip(result["recovered_N_Nm"], loads):
            self.assertAlmostEqual(actual, expected, places=10)
        # Translation of the coordinate origin must not change centroidal loads.
        translated = [rig.BoltCoord(b.label, b.x+13, b.y-8) for b in coords]
        self.assertEqual(result, rig.bolt_group_loads(translated, *loads))

    def test_square_hand_solution_and_torsion_vector_sum(self):
        coords = [rig.BoltCoord(str(i), x, y) for i, (x, y) in
                  enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)])]
        out = rig.bolt_group_loads(coords, axial_N=40, shear_x_N=8,
                                   moment_x_Nm=8, torsion_Nm=16)
        self.assertEqual([f["axial_signed_N"] for f in out["bolts"]], [8, 8, 12, 12])
        self.assertEqual([f["shear_x_N"] for f in out["bolts"]], [4, 4, 0, 0])
        self.assertEqual([f["shear_y_N"] for f in out["bolts"]], [-2, 2, 2, -2])
        self.assertAlmostEqual(out["bolts"][0]["shear_N"], math.sqrt(20))

    def test_engine_thrust_and_full_dynamic_weight_are_not_bypassed(self):
        out = rig.full_analysis()
        for case in out["engine_mount_arm_sweep"]:
            self.assertAlmostEqual(sum(b["axial_signed_N"] for b in case["bolts"]), 721)
            self.assertAlmostEqual(case["recovered_N_Nm"][3], 5.87*5*9.81*case["cg_arm_m"])
        self.assertIsNone(out["allowables"])
        self.assertEqual(out["status"], "SCREENING_ONLY_UNQUALIFIED")

    def test_beam_hand_calculation_both_supports_and_units(self):
        # P=120 N, L=2 m, EI=600 N m²: simple delta=1/30 m, M=60 Nm.
        simple = rig.beam_analysis(2, 120, 200e9, 3e-9, .02)
        fixed = rig.beam_analysis(2, 120, 200e9, 3e-9, .02, "fixed_fixed")
        self.assertAlmostEqual(simple["deflection_m"], 1/30)
        self.assertAlmostEqual(simple["max_stress_Pa"], 200e6)
        self.assertEqual(simple["reaction_each_N"]*2, 120)
        self.assertAlmostEqual(fixed["deflection_m"]*4, simple["deflection_m"])
        self.assertEqual(fixed["max_moment_Nm"], 30)
        self.assertAlmostEqual(rig.EXTRUSION["I_m4"], 1.3787e-7)
        self.assertAlmostEqual(rig.EXTRUSION["weight_kg_m"], 2.359037483, places=9)

    def test_interaction_uses_both_supplied_allowables(self):
        self.assertAlmostEqual(rig.combined_interaction(5, 3, 1, 1, 10, 6), .5)
        self.assertAlmostEqual(rig.combined_interaction(5, 3, 1, 1, 10, 3), 1.25)

    def test_anchor_uplift_and_contact_equilibrium(self):
        # 100 Nm, 1m base, W=60 -> tension 70, bearing 130 (not a negative bolt).
        result = rig.overturning_analysis(100, 1, 4, 1, 60)
        self.assertEqual(result["anchor_tension_each_active_N"], 35)
        self.assertEqual(result["anchor_tension_each_inactive_N"], 0)
        self.assertEqual(result["bearing_compression_N"], 130)
        self.assertEqual(result["shear_each_N"]*4, 100)
        self.assertEqual(result["vertical_residual_N"], 0)
        self.assertEqual(result["moment_residual_Nm"], 0)
        reverse = rig.overturning_analysis(-100, 1, 4, 1, 60)
        self.assertEqual(reverse["tension_row"], "+X")
        self.assertEqual(reverse["anchor_row_total_tension_N"], 70)
        for thrust in (0, 20, 30):
            seated = rig.overturning_analysis(thrust, 1, 4, 1, 60)
            self.assertFalse(seated["uplift"])
            self.assertEqual(seated["moment_residual_Nm"], 0)

    def test_invalid_inputs_fail_closed(self):
        for bad in (None, math.nan, math.inf, -1, 0, True):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                rig.beam_analysis(1, 1, bad, 1, 1)
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                rig.combined_interaction(1, 1, 1, 1, 1, bad)
        for call in (lambda: rig.bolt_tensile_stress_area(.0031),
                     lambda: rig.bolt_circle_coords(.045, 0),
                     lambda: rig.beam_analysis(1, 1, 1, 1, 1, "unknown"),
                     lambda: rig.overturning_analysis(1, 1, 3),
                     lambda: rig.overturning_analysis(1, 1, downward_load_N=-1),
                     lambda: rig.bolt_group_loads([rig.BoltCoord(str(i), i, 2*i) for i in range(4)])):
            with self.assertRaises(ValueError):
                call()


if __name__ == "__main__":
    unittest.main()
