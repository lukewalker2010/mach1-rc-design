import math
import unittest

from tools.design_checks import mass_rows, mass_state
from tools.loads_recovery import (
    analytic_semispan, beam_loads, bending_ei_for_freq, cap_centroid_separation_mm,
    cantilever_bending_freq, chute_gate_speed, chute_steady_drag, isa_density,
    kinetic_energy, load_case_discrepancy, reduced_frequency, required_cap_area_mm2,
    required_cl, section_depth_mm, skid_stop_with_drogue, stall_speed,
    stop_distance, wheel_rev_per_s, wing_planform,
    torque_per_span,
)

G = 9.81


class LoadsTests(unittest.TestCase):
    def test_triangular_cut_centroid_and_mixed_relief_validation(self):
        pf = wing_planform()
        a = analytic_semispan(13.6,6,pf,"triangular",y0=.0925)
        self.assertAlmostEqual(a["arm_m"],(.475-.0925)/3)
        b = beam_loads(13.6,6,pf,"triangular")
        self.assertAlmostEqual(a["moment_nm"],b["root_moment_nm"],places=10)
        for kw in ({"mass_kg":-1,"n":6}, {"mass_kg":13.6,"n":float("nan")}):
            with self.assertRaises(ValueError):
                beam_loads(planform=pf,relief_scheme="uniform",**kw)

    def test_torque_sign_and_cap_force_couple(self):
        self.assertLess(torque_per_span(100,1000,.2,.4,.3,0),0)
        self.assertGreater(torque_per_span(100,1000,.2,.2,.3,0),0)
        # EACH 50 mm² cap at 200 MPa gives 10 kN; 10 mm couple -> 100 Nm.
        self.assertAlmostEqual(required_cap_area_mm2(-100,10,200),50)
        for args in ((.05,50,210),(.95,50,210),(.3,50,0)):
            with self.assertRaises(ValueError):
                cap_centroid_separation_mm(*args)
        with self.assertRaises(ValueError):
            isa_density(11000)
        with self.assertRaises(ValueError):
            required_cl(13.6,30,rho=float("nan"))
    def setUp(self):
        self.pf = wing_planform()                     # b 0.95, S 0.14, lambda 0.4
        self.pf0 = wing_planform(root_cut_m=0.0)
        self.full = mass_state(mass_rows())

    def test_planform_derived_from_contract(self):
        # c_r = 2S/(b(1+lambda)); c_t = lambda c_r; MAC = (2/3)c_r (1+l+l^2)/(1+l)
        self.assertAlmostEqual(self.pf["c_root_m"], 2 * 0.14 / (0.95 * 1.4), places=6)
        self.assertAlmostEqual(self.pf["c_tip_m"], 0.40 * self.pf["c_root_m"])
        self.assertAlmostEqual(self.pf["avg_chord_m"], 0.14 / 0.95, places=6)
        self.assertAlmostEqual(self.pf["mac_m"], (2/3) * self.pf["c_root_m"]
                               * (1 + 0.4 + 0.4**2) / 1.4, places=6)
        self.assertEqual(self.pf["root_cut_m"], 0.185 / 2)  # 18 sect.3.1 fuselage OD

    def test_numeric_matches_analytic_for_all_schemes(self):
        # Reference centroids: uniform b/4, triangular b/6, chord b/2 (1+2l)/(3(1+l)).
        for scheme, arm in (("uniform", 0.95 / 4), ("triangular", 0.95 / 6),
                            ("chord", 0.475 * (1 + 2 * 0.40) / (3 * (1 + 0.40)))):
            a = analytic_semispan(self.full["mass_kg"], 6, self.pf0, scheme)
            b = beam_loads(self.full["mass_kg"], 6, self.pf0, scheme)
            self.assertAlmostEqual(b["root_shear_n"], a["shear_n"], places=5)
            self.assertAlmostEqual(b["root_moment_nm"], a["moment_nm"], places=4)
            self.assertAlmostEqual(a["shear_n"], 6 * self.full["mass_kg"] * G / 2)
            self.assertAlmostEqual(a["moment_nm"], a["shear_n"] * arm, places=3)
        # R04 header contract: 6g centreline = 400.25 N / 81.48 N.m reappears.
        a6 = analytic_semispan(self.full["mass_kg"], 6, self.pf0, "chord")
        self.assertAlmostEqual(a6["shear_n"], 400.25, places=1)
        self.assertAlmostEqual(a6["moment_nm"], 81.48, places=1)

    def test_conservation_and_first_moment(self):
        # Chord-proportional beam cut at the fuselage side matches the closed
        # form for that cut (force and first moment), not just at the centreline.
        for n in (4, 6, 9):
            b = beam_loads(self.full["mass_kg"], n, self.pf)
            a = analytic_semispan(self.full["mass_kg"], n, self.pf, "chord",
                                  y0=self.pf["root_cut_m"])
            self.assertAlmostEqual(b["root_shear_n"], a["shear_n"], places=6)
            self.assertAlmostEqual(b["root_moment_nm"], a["moment_nm"], places=4)
        # Total force = n*W is fully conservative on the full half-span.
        a9 = analytic_semispan(self.full["mass_kg"], 9, self.pf0, "chord")
        self.assertAlmostEqual(a9["shear_n"], 9 * self.full["mass_kg"] * G / 2)

    def test_tail_download_adds_half_to_each_root(self):
        a0 = analytic_semispan(self.full["mass_kg"], 6, self.pf0, "chord")
        side = analytic_semispan(self.full["mass_kg"], 6, self.pf, "chord",
                                 y0=self.pf["root_cut_m"])
        for dl in (0.0, 50.0, -30.0):
            a1 = analytic_semispan(self.full["mass_kg"], 6, self.pf0, "chord",
                                   tail_download_n=dl)
            self.assertAlmostEqual(a1["shear_n"], a0["shear_n"] + dl / 2)
            s1 = analytic_semispan(self.full["mass_kg"], 6, self.pf, "chord",
                                   y0=self.pf["root_cut_m"], tail_download_n=dl)
            self.assertAlmostEqual(s1["shear_n"], side["shear_n"] + dl / 2 * side["fraction_outboard"])
            b = beam_loads(self.full["mass_kg"], 6, self.pf, tail_download_n=dl)
            self.assertAlmostEqual(b["root_shear_n"], s1["shear_n"], places=6)

    def test_inertial_relief_sign_and_like_distribution(self):
        # Like-lift relief cuts root shear by n*g*m_w/2 per half and scales the
        # bending moment by (1 - m_w/m_total) while keeping the lift centroid.
        mw = 0.50
        a0 = analytic_semispan(self.full["mass_kg"], 6, self.pf0, "chord")
        a1 = analytic_semispan(self.full["mass_kg"], 6, self.pf0, "chord", wing_mass_kg=mw)
        self.assertAlmostEqual(a0["shear_n"] - a1["shear_n"], 6 * G * mw / 2)
        self.assertAlmostEqual(a1["moment_nm"],
                               a0["moment_nm"] * (1 - mw / self.full["mass_kg"]), places=4)
        # Uniform relief (different scheme) still only subtracts n*g*m_w/2 of
        # shear; the moment change depends on the relief centroid and is negative.
        b_u = beam_loads(self.full["mass_kg"], 6, self.pf0, "chord",
                         wing_mass_kg=mw, relief_scheme="uniform")
        self.assertAlmostEqual(a0["shear_n"] - b_u["root_shear_n"], 6 * G * mw / 2)
        self.assertLess(b_u["root_moment_nm"], a0["moment_nm"])

    def test_cap_fit_reproduces_20_failure(self):
        s = cap_centroid_separation_mm(0.30, 50.0, 210.0, skin_mm=0.5, cap_thick_mm=1.0)
        self.assertAlmostEqual(s["centre_depth_mm"], 7.056, places=2)   # 20 sect.3
        self.assertAlmostEqual(s["outer_depth_mm"], 4.980, places=2)
        self.assertAlmostEqual(s["separation_mm"], 2.980, places=2)     # 20 sect.3
        self.assertLess(s["separation_mm"], 7.0)                        # FAILs the 7 mm proposal
        with_bond = cap_centroid_separation_mm(0.30, 50.0, 210.0, bond_mm=0.2)
        self.assertAlmostEqual(with_bond["separation_mm"], 2.9798 - 2 * 0.2, places=2)
        narrow = cap_centroid_separation_mm(0.30, 35.0, 210.0, bond_mm=0.2)
        self.assertGreater(narrow["separation_mm"], with_bond["separation_mm"])
        self.assertEqual(section_depth_mm(0.5, 210.0), 0.04 * 210)     # max thickness

    def test_cap_area_scales_with_m_d_and_sigma(self):
        a400 = required_cap_area_mm2(81.48, 2.980, 400)          # ~68.36 mm^2
        a800 = required_cap_area_mm2(81.48, 2.980, 800)
        self.assertAlmostEqual(a800, a400 / 2)
        self.assertAlmostEqual(required_cap_area_mm2(81.48, 5.056, 400), a400 * 2.980 / 5.056)
        self.assertAlmostEqual(required_cap_area_mm2(40.74, 2.980, 400), a400 / 2)
        self.assertAlmostEqual(a400, 81.48 * 1e3 / (2.980 * 400))  # N.mm/(mm*MPa)

    def test_4g_6g_versus_9g_discrepancy(self):
        rows = load_case_discrepancy()
        m6 = next(m for n, m in rows if n == 6)["moment_nm"]
        m9 = next(m for n, m in rows if n == 9)["moment_nm"]
        legacy = next(m for n, m in rows if not isinstance(n, int))["moment_nm"]
        self.assertAlmostEqual(m9, 122.22, places=1)
        self.assertAlmostEqual(legacy, 109.64, places=1)
        self.assertAlmostEqual(m9, 1.5 * m6, places=6)
        self.assertGreater(legacy / 100.0, 1.05)   # legacy trace already exceeds ~100 N.m

    def test_recovery_required_cl_and_stallare_inverse(self):
        self.assertAlmostEqual(required_cl(13.6, 30.0), 1.729, places=3)   # 25 R06
        self.assertAlmostEqual(required_cl(11.98, 30.0), 1.523, places=3)
        self.assertAlmostEqual(stall_speed(13.6, 0.8), 44.10, places=1)
        for clmax in (0.8, 1.2, 1.6):
            v = stall_speed(self.full["mass_kg"], clmax)
            self.assertAlmostEqual(required_cl(self.full["mass_kg"], v), clmax, places=9)
        self.assertLessEqual(stall_speed(13.6, 1.73), 30.0)               # flare case

    def test_wheel_rpm_energy_and_stop_distance(self):
        self.assertAlmostEqual(wheel_rev_per_s(70, 0.050) * 60, 26738, delta=1)  # 08 sect.1.4
        self.assertAlmostEqual(kinetic_energy(13.6, 30), 6120.0)
        self.assertAlmostEqual(kinetic_energy(13.6, 60), 4 * kinetic_energy(13.6, 30))
        self.assertAlmostEqual(stop_distance(30, 0.4 * G), 900 / (2 * 0.4 * G))
        self.assertAlmostEqual(skid_stop_with_drogue(13.6, 30, 0.4, chute_on=False),
                               stop_distance(30, 0.4 * G))

    def test_drogue_stop_shorter_than_skid_only(self):
        skid_only = skid_stop_with_drogue(13.6, 30, 0.4, chute_on=False)
        with_chute = skid_stop_with_drogue(13.6, 30, 0.4)
        self.assertLess(with_chute, skid_only)
        self.assertGreater(with_chute, 60)      # full mass fails the <=60 m requirement
        self.assertLess(skid_stop_with_drogue(11.98, 30, 0.4), with_chute)

    def test_chute_steady_drag_and_gate(self):
        # 08 sect.3.3 reference: 117 N @ 30 m/s; scales with V^2 and rho.
        self.assertAlmostEqual(chute_steady_drag(30.0, 1.225, 0.75, 0.283), 117.0, places=0)
        self.assertAlmostEqual(chute_steady_drag(60.0, 1.225, 0.75, 0.283),
                               chute_steady_drag(30.0, 1.225, 0.75, 0.283) * 4)
        self.assertAlmostEqual(chute_steady_drag(30.0, 0.905, 0.75, 0.283),
                               chute_steady_drag(30.0, 1.225, 0.75, 0.283) * 0.905 / 1.225)
        m06_10kft = chute_steady_drag(0.6 * 328.0, isa_density(3048.0))
        self.assertGreater(m06_10kft, 3000)     # 3.7 kN at the I-11 M0.6 gate
        self.assertAlmostEqual(chute_gate_speed(800.0), 78.4, places=1)
        # Steady drag of the 0.6 m ribbon at the 30-to-38 m/s final windows is < 1 kN.
        self.assertLess(chute_steady_drag(38.0), 1000)

    def test_aeroelastic_dimensional_sanity(self):
        lo, hi = cantilever_bending_freq(0.5, 0.475, 30), cantilever_bending_freq(0.5, 0.475, 300)
        self.assertLess(lo, hi)
        self.assertAlmostEqual(cantilever_bending_freq(0.5, 0.475, 100), 24.2, places=1)
        self.assertAlmostEqual(bending_ei_for_freq(25, 0.5, 0.475), 107, delta=1)
        k = reduced_frequency(25, 0.1564, 360.8)
        self.assertAlmostEqual(k, 0.0340, places=3)
        self.assertLess(k, 0.1)                     # not a flutter validity criterion
        self.assertGreater(reduced_frequency(25, 0.1564, 38.0), k)

    def test_unit_and_domain_limits(self):
        with self.assertRaises(ValueError):
            required_cl(13.6, 0.0)
        with self.assertRaises(ValueError):
            stall_speed(13.6, -0.1)
        with self.assertRaises(ValueError):
            wheel_rev_per_s(70, 0.0)
        with self.assertRaises(ValueError):
            kinetic_energy(-1, 30)
        with self.assertRaises(ValueError):
            wing_planform(taper=2.0)
        with self.assertRaises(ValueError):
            wing_planform(root_cut_m=0.5)           # beyond half-span
        with self.assertRaises(ValueError):
            skid_stop_with_drogue(13.6, 30, -0.1)
        with self.assertRaises(ValueError):
            beam_loads(13.6, 0, self.pf0)           # load factor positive
        with self.assertRaises(ValueError):
            cap_centroid_separation_mm(1.5, 50.0, 210.0)


if __name__ == "__main__":
    unittest.main()
