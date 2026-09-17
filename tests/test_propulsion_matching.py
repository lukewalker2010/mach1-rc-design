#!/usr/bin/env python3
"""Regression tests for tools/propulsion_matching.py (25 R07/R08 evidence).

Stdlib unittest only. Test textbook gas-dynamic limits against independently
derived closed-form results, and energy/ram conservation properties.
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import propulsion_matching as pm


class TestChokedRelations(unittest.TestCase):
    def test_critical_pressure_ratio_air(self):
        # gamma=1.4 -> (1.2)^3.5 = 1.8929 (standard textbook value)
        self.assertAlmostEqual(pm.critical_pressure_ratio(1.4), 1.8929, places=4)

    def test_choked_mass_flow_closed_form(self):
        # mdot = Cd Pt A*/sqrt(Tt) * sqrt(g/R) * ((g+1)/2)^(-(g+1)/(2(g-1)))
        Pt, Tt, A, g, R = 500e3, 1800.0, 2.376e-3, 1.33, 298.0
        f = math.sqrt(g / R) * ((g + 1.0) / 2.0) ** (-(g + 1.0) / (2.0 * (g - 1.0)))
        expected = Pt * A / math.sqrt(Tt) * f
        self.assertAlmostEqual(pm.choked_mass_flow(Pt, Tt, A, g, R), expected, places=9)

    def test_pt_required_inverts_choked_mass_flow(self):
        mdot, Tt, A, g, R = 1.149, 1800.0, pm.AREA55, pm.G_PROD, pm.R_PROD
        Pt = pm.pt_required_for_choked_massflow(mdot, Tt, A, g, R)
        back = pm.choked_mass_flow(Pt, Tt, A, g, R)
        self.assertAlmostEqual(back, mdot, places=6)

    def test_choked_is_independent_of_downstream_pressure(self):
        # lower ambient must not change the choked mass flow
        choked_low = pm.nozzle_flow(3.0e5, 1800.0, pm.AREA55, 40e3, pm.G_PROD, pm.R_PROD)
        choked_high = pm.nozzle_flow(3.0e5, 1800.0, pm.AREA55, 69.7e3, pm.G_PROD, pm.R_PROD)
        self.assertTrue(choked_low["choked"] and choked_high["choked"])
        self.assertAlmostEqual(choked_low["mdot"], choked_high["mdot"], places=9)

    def test_unchoked_momentum_matches_rhoAV(self):
        # unchoked convergent nozzle at Pe==Pa: F = mdot*Ve exactly (pressure term 0)
        res = pm.nozzle_flow(1.2e5, 1000.0, pm.AREA45, 80e3, pm.G_AIR, pm.R_AIR,
                             Cd=1.0, eta=1.0)
        self.assertFalse(res["choked"])
        self.assertAlmostEqual(res["F_pressure"], 0.0, places=9)
        self.assertAlmostEqual(res["F_momentum"], res["mdot"] * res["Ve"], places=9)


class TestRamAndBookkeeping(unittest.TestCase):
    def test_zero_flight_speed_zero_ram(self):
        res = pm.nozzle_flow(300e3, 1800.0, pm.AREA55, pm.PA_10KFT, pm.G_PROD, pm.R_PROD)
        gross, ram, net, tot = pm.flight_net(res, res['mdot']-0.0493, 0.022, 0.0273, Vinf=0.0)
        self.assertEqual(ram, 0.0)
        self.assertEqual(net, gross)

    def test_ram_uses_air_not_fuel(self):
        res = pm.nozzle_flow(300e3, 1800.0, pm.AREA55, pm.PA_10KFT, pm.G_PROD, pm.R_PROD)
        air = res['mdot'] - 0.0493
        _, ram, _, _ = pm.flight_net(res, air, 0.022, 0.0273, Vinf=328.0)
        self.assertAlmostEqual(ram, air * 328.0, places=6)

    def test_fuel_adds_exit_momentum_without_ram_penalty(self):
        # Adding 0.0493 kg/s of onboard fuel must raise gross by mdot_f*Ve and
        # leave ram (air-only) unchanged.
        res = pm.nozzle_flow(300e3, 1800.0, pm.AREA55, pm.PA_10KFT, pm.G_PROD, pm.R_PROD)
        g_no, ram_no, net_no, _ = pm.flight_net(res, res['mdot'], Vinf=328.0)
        g_ab, ram_ab, net_ab, _ = pm.flight_net(res, res['mdot']-0.0493, 0.022, 0.0273, Vinf=328.0)
        self.assertEqual(g_ab, g_no)
        self.assertAlmostEqual(net_ab-net_no, 0.0493*328)
        self.assertAlmostEqual(ram_no-ram_ab, 0.0493*328)
        with self.assertRaises(ValueError):
            pm.flight_net(res, 1.10, 0.022, 0.0273)


class TestHeatBalance(unittest.TestCase):
    def test_round_trip_energy_conservation(self):
        # module round trip on a consistent mass basis gives back T7 exactly
        mf = pm.fuel_for_temperature_rise(1.10, pm.CP_PROD, 800.0, pm.LHV, pm.ETA_COMB)
        T7 = pm.heat_addition(1.10, pm.CP_PROD, mf, pm.LHV, pm.ETA_COMB, pm.T5_DRY)
        self.assertAlmostEqual(T7, 1800.0, places=6)

    def test_fuel_flow_accounts_for_added_mass_enthalpy(self):
        mf = pm.fuel_for_temperature_rise(1.122, pm.CP_PROD,
                                          1800.0 - 1000.0, pm.LHV, pm.ETA_COMB)
        self.assertAlmostEqual(1.122*1200*(1000-298.15) + mf*43e6*0.9,
                               (1.122+mf)*1200*(1800-298.15), places=6)
        self.assertGreater(mf, 0.0273)

    def test_zero_fuel_no_heating(self):
        self.assertAlmostEqual(pm.heat_addition(1.10, pm.CP_PROD, 0.0, pm.LHV,
                                                pm.ETA_COMB, 1000.0), 1000.0, places=6)


class TestThermalConservation(unittest.TestCase):
    def test_no_external_cooling_equilibrates_at_shell(self):
        s = pm.shell_blanket_composite(610, 0.05, 0.005, 0, 268, 0)
        self.assertAlmostEqual(s['T_composite'], 610, places=2)
        self.assertFalse(s['pass_100C'])

    def test_liner_balance_conserves_wall_energy(self):
        r = pm.liner_wall_balance(hg=579.0, Tg=1800.0, eps_g=0.25, hc=125.0,
                                  Tc=516.0, Tsh=610.0, eps_c=0.3, kw=18.0, tw=0.001)
        self.assertTrue(r["converged"])
        gas = r["q_conv_gas"] + r["q_rad_gas"]
        back = r["q_conv_back"] + r["q_rad_back"]
        self.assertAlmostEqual(gas, back, places=1)
        self.assertAlmostEqual(r["q"], gas, places=1)

    def test_shell_blanket_composite_conserves_energy(self):
        s = pm.shell_blanket_composite(610.0, k_b=0.05, t_b=0.005, h_ext=15.0,
                                       T_amb=268.0, eps_f=0.15)
        self.assertTrue(s["converged"])
        self.assertAlmostEqual(s["q_cond"], s["q_ext"], places=2)

    def test_prescribed_endpoint_is_not_a_solution(self):
        # coolant can never carry 19.2 kW with only 0.0253 kg/s over 187 K
        Q_cool = 0.0253 * 1000.0 * (610.0 - 423.0)
        Q_claimed = 382e3 * math.pi * 0.080 * 0.20
        self.assertLess(Q_cool, Q_claimed)


class TestDomainsAndNozzleBoundary(unittest.TestCase):
    def test_cd_scales_both_flow_branches_not_pressure_area(self):
        for pt in (100e3, 300e3):
            a = pm.nozzle_flow(pt, 1800, pm.AREA55, pm.PA_10KFT)
            b = pm.nozzle_flow(pt, 1800, pm.AREA55, pm.PA_10KFT, Cd=0.8)
            self.assertAlmostEqual(b['mdot'], 0.8*a['mdot'])
            self.assertEqual(b['F_pressure'], a['F_pressure'])

    def test_choking_continuity_and_zero_pressure_drop(self):
        pt = 1e5*pm.critical_pressure_ratio()
        a = pm.nozzle_flow(pt, 1000, pm.AREA45, 1e5)
        b = pm.nozzle_flow(pt*(1-1e-9), 1000, pm.AREA45, 1e5)
        self.assertAlmostEqual(a['mdot'], b['mdot'], places=8)
        self.assertEqual(pm.nozzle_flow(1e5, 1000, pm.AREA45, 1e5)['mdot'], 0)

    def test_nonfinite_and_range_rejection(self):
        for v in (float('nan'), float('inf'), -1, 0):
            with self.assertRaises(ValueError):
                pm.nozzle_flow(3e5, v, pm.AREA55, 69700)
        for kwargs in ({'gamma': 1}, {'Cd': 1.1}, {'eta': -0.1}):
            with self.assertRaises(ValueError):
                pm.nozzle_flow(3e5, 1800, pm.AREA55, 69700, **kwargs)
        with self.assertRaises(ValueError):
            pm.nozzle_flow(60000, 1800, pm.AREA55, 69700)
        with self.assertRaises(ValueError):
            pm.fuel_for_temperature_rise(1.1, 1200, 1e6, 43e6, 0.9)


if __name__ == "__main__":
    unittest.main()
