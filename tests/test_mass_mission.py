"""Tests for mass_mission.py — fuel-state CG sweep, tolerances, mission budget.

Uses traceable test-only fixtures where possible; actual 18 S3.4 rows for
integration tests. No fabricated flight profiles as evidence.
"""
import csv
import itertools
import math
import os
import tempfile
import unittest

from tools.design_checks import mass_rows, mass_state
from tools.mass_mission import (
    FUEL_MASS_KG,
    CG_MAX_M,
    CG_MIN_M,
    MTOW_KG,
    TANK_STATION_MAX_M,
    TANK_STATION_MIN_M,
    ab_sensitivity,
    admissible_dry_moment,
    admissible_fuel_station,
    combined_analysis,
    fuel_state_sweep,
    joint_ballast_analysis,
    parse_mission_csv,
    tank_relocation_sweep,
    tolerance_sweep,
    ballast_mtow_proof,
    _subset_rows,
)


class TestFuelStateSweep(unittest.TestCase):
    def test_full_and_empty_match_design_checks(self):
        rows = mass_rows()
        sweep = fuel_state_sweep(rows, n_points=50)
        self.assertEqual(len(sweep), 51)
        full = sweep[0]
        empty = sweep[-1]
        self.assertAlmostEqual(full["fuel_fraction"], 1.0)
        self.assertAlmostEqual(empty["fuel_fraction"], 0.0)
        dc_full = mass_state(rows, 1)
        dc_empty = mass_state(rows, 0)
        self.assertAlmostEqual(full["cg_m"], dc_full["cg_m"], places=6)
        self.assertAlmostEqual(empty["cg_m"], dc_empty["cg_m"], places=6)
        self.assertAlmostEqual(full["mass_kg"], dc_full["mass_kg"], places=6)
        self.assertAlmostEqual(empty["mass_kg"], dc_empty["mass_kg"], places=6)

    def test_cg_monotonically_increases_with_burn(self):
        rows = mass_rows()
        sweep = fuel_state_sweep(rows)
        cgs = [s["cg_m"] for s in sweep]
        for i in range(len(cgs) - 1):
            self.assertGreaterEqual(cgs[i + 1], cgs[i] - 1e-12)

    def test_full_in_band_empty_out_of_band(self):
        rows = mass_rows()
        sweep = fuel_state_sweep(rows)
        self.assertTrue(sweep[0]["in_band"])
        self.assertFalse(sweep[-1]["in_band"])

    def test_mass_conservation_across_sweep(self):
        rows = mass_rows()
        sweep = fuel_state_sweep(rows)
        for s in sweep:
            fuel_kg = s["fuel_fraction"] * FUEL_MASS_KG
            expected_mass = mass_state(rows, s["fuel_fraction"])["mass_kg"]
            self.assertAlmostEqual(s["mass_kg"], expected_mass, places=6)

    def test_cg_exits_band_below_fuel_fraction(self):
        rows = mass_rows()
        sweep = fuel_state_sweep(rows)
        in_band_count = sum(1 for s in sweep if s["in_band"])
        out_band_count = sum(1 for s in sweep if not s["in_band"])
        self.assertGreater(out_band_count, 0)
        self.assertGreater(in_band_count, 0)


class TestToleranceSweep(unittest.TestCase):
    def test_extrema_against_all_independent_corners(self):
        rows = [("Forward", 1., .2), ("Aft", 2., 1.8), ("Fuel (test)", .4, .5)]
        for fraction, idx in ((1.,0), (0.,-1)):
            corners = []
            for masses in itertools.product((.9,1.1),(1.9,2.1)):
                for offsets in itertools.product((-.01,.01), repeat=3):
                    ms = (*masses,.4*fraction)
                    corners.append(sum(m*(r[2]+ds) for m,r,ds in zip(ms,rows,offsets))/sum(ms))
            bound = tolerance_sweep(rows,.1,.01)[idx]
            self.assertAlmostEqual(bound["fwd_cg_m"], min(corners), places=12)
            self.assertAlmostEqual(bound["aft_cg_m"], max(corners), places=12)

    def test_bounds_envelope_nominal(self):
        rows = mass_rows()
        tol = tolerance_sweep(rows)
        self.assertEqual(len(tol), 51)
        for t in tol:
            self.assertLessEqual(t["fwd_cg_m"], t["aft_cg_m"])

    def test_tolerance_widens_cg_range(self):
        rows = mass_rows()
        sweep = fuel_state_sweep(rows)
        tol = tolerance_sweep(rows)
        nominal_range = sweep[-1]["cg_m"] - sweep[0]["cg_m"]
        tol_range = tol[-1]["aft_cg_m"] - tol[0]["fwd_cg_m"]
        self.assertGreater(tol_range, nominal_range)


class TestAdmissibleDryMoment(unittest.TestCase):
    def test_current_exceeds_band(self):
        rows = mass_rows()
        result = admissible_dry_moment(rows)
        self.assertFalse(result["in_band"])
        self.assertGreater(result["margin_to_min_kg_m"], 0)
        self.assertLess(result["margin_to_max_kg_m"], 0)

    def test_admissible_range_consistent(self):
        rows = mass_rows()
        result = admissible_dry_moment(rows)
        self.assertLess(result["admissible_moment_min_kg_m"],
                        result["admissible_moment_max_kg_m"])
        expected_min = result["dry_mass_kg"] * CG_MIN_M
        expected_max = result["dry_mass_kg"] * CG_MAX_M
        self.assertAlmostEqual(result["admissible_moment_min_kg_m"], expected_min, places=4)
        self.assertAlmostEqual(result["admissible_moment_max_kg_m"], expected_max, places=4)


class TestAdmissibleFuelStation(unittest.TestCase):
    def test_baseline_feasible(self):
        rows = mass_rows()
        result = admissible_fuel_station(rows)
        self.assertTrue(result["i06_feasible"])

    def test_overrides_dry_moment(self):
        rows = mass_rows()
        # A moderate reduction in dry moment shifts the required fuel station range forward
        empty = mass_state(rows, 0)
        reduced_dm = empty["moment_kg_m"] - 0.3  # reduce by 0.3 kg.m
        result_default = admissible_fuel_station(rows)
        result_reduced = admissible_fuel_station(rows, dry_moment_override=reduced_dm)
        # Reduced dry moment requires more forward fuel to keep full CG in band
        self.assertGreater(result_reduced["fuel_station_min_m"],
                           result_default["fuel_station_min_m"])
        # And allows more aft fuel too
        self.assertGreater(result_reduced["fuel_station_max_m"],
                           result_default["fuel_station_max_m"])


class TestABSensitivity(unittest.TestCase):
    def test_0p97_worse_than_0p83(self):
        rows = mass_rows()
        result = ab_sensitivity(rows)
        self.assertGreater(result["alternate_0.97"]["empty_cg_m"],
                           result["baseline_0.83"]["empty_cg_m"])
        self.assertGreater(result["sensitivity"]["delta_empty_cg_mm"], 0)

    def test_both_empty_out_of_band(self):
        rows = mass_rows()
        result = ab_sensitivity(rows)
        self.assertFalse(result["baseline_0.83"]["empty_in_band"])
        self.assertFalse(result["alternate_0.97"]["empty_in_band"])

    def test_both_full_in_band(self):
        rows = mass_rows()
        result = ab_sensitivity(rows)
        self.assertTrue(result["baseline_0.83"]["full_in_band"])
        self.assertTrue(result["alternate_0.97"]["full_in_band"])


class TestTankRelocationSweep(unittest.TestCase):
    def test_empty_cg_invariant(self):
        rows = mass_rows()
        sweep = tank_relocation_sweep(rows)
        empty_cgs = [s["empty_cg_m"] for s in sweep]
        for cg in empty_cgs:
            self.assertAlmostEqual(cg, empty_cgs[0], places=6)

    def test_full_cg_varies_with_station(self):
        rows = mass_rows()
        sweep = tank_relocation_sweep(rows)
        full_cgs = [s["full_cg_m"] for s in sweep]
        self.assertNotAlmostEqual(full_cgs[0], full_cgs[-1], places=4)

    def test_full_cg_increases_aft_tank(self):
        rows = mass_rows()
        sweep = tank_relocation_sweep(rows)
        for i in range(len(sweep) - 1):
            self.assertLessEqual(sweep[i]["full_cg_m"],
                                 sweep[i + 1]["full_cg_m"] + 1e-9)


class TestJointBallastAnalysis(unittest.TestCase):
    def test_mtow_constructive_counterexample_and_bounds(self):
        rows = mass_rows()
        proof = ballast_mtow_proof(rows)
        self.assertAlmostEqual(proof["minimum_full_mass_kg"],22.0725)
        lo, hi = proof["station_interval_at_mtow_m"]
        b = proof["additional_mass_at_mtow_kg"]
        candidate = rows+[("Additional ballast",b,(lo+hi)/2)]
        self.assertAlmostEqual(mass_state(candidate)["mass_kg"],25.)
        self.assertTrue(all(p["in_band"] for p in fuel_state_sweep(candidate)))
        self.assertTrue(joint_ballast_analysis(rows,(lo+hi)/2)["feasible"])
        for s in (.955,.995,2.6):
            self.assertFalse(joint_ballast_analysis(rows,s)["feasible"])
        self.assertFalse(joint_ballast_analysis(rows+[("Extra",15.,1.)],.92)["feasible"])

    def test_nose_ballast_infeasible(self):
        rows = mass_rows()
        result = joint_ballast_analysis(rows, ballast_station_m=0.10)
        self.assertFalse(result["feasible"])

    def test_min_exceeds_max(self):
        rows = mass_rows()
        result = joint_ballast_analysis(rows, ballast_station_m=0.10)
        self.assertGreater(result["b_min_for_empty_cg_max_kg"],
                           result["b_max_for_full_cg_min_kg"])

    def test_gap_increases_with_aft_ballast(self):
        rows = mass_rows()
        fwd = joint_ballast_analysis(rows, ballast_station_m=0.10)
        mid = joint_ballast_analysis(rows, ballast_station_m=0.50)
        # Aft ballast is less effective at moving CG forward, so gap grows
        gap_fwd = fwd["b_min_for_empty_cg_max_kg"] - fwd["b_max_for_full_cg_min_kg"]
        gap_mid = mid["b_min_for_empty_cg_max_kg"] - mid["b_max_for_full_cg_min_kg"]
        self.assertGreater(gap_mid, gap_fwd)


class TestMissionCSVParser(unittest.TestCase):
    def test_rejects_inconsistent_initial_cg(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write_csv([dict(phase="test",duration_s=1,engine_flow_g_s=0,
                ab_flow_g_s=0,initial_fuel_kg=1.62,initial_cg_m=.98)],td)
            with self.assertRaisesRegex(ValueError,"initial CG"):
                parse_mission_csv(path,mass_rows())

    def test_rejects_empty_and_truncated_records(self):
        with tempfile.TemporaryDirectory() as td:
            path = self._write_csv([],td)
            with self.assertRaisesRegex(ValueError,"no phases"):
                parse_mission_csv(path,mass_rows())
            with open(path,"a") as f:
                f.write("test,1,0\n")
            with self.assertRaises(ValueError):
                parse_mission_csv(path,mass_rows())

    def test_uses_supplied_fuel_capacity(self):
        rows = [("Dry",1.,1.),("Fuel (test)",.5,.5)]
        with tempfile.TemporaryDirectory() as td:
            path = self._write_csv([dict(phase="test",duration_s=10,engine_flow_g_s=10,
                ab_flow_g_s=0,initial_fuel_kg=.5,initial_cg_m=1.25/1.5)],td)
            phases = parse_mission_csv(path,rows)
            self.assertAlmostEqual(phases[0]["mass_kg"],1.4)
            self.assertAlmostEqual(phases[0]["cg_m"],1.2/1.4)

    def _write_csv(self, rows, directory):
        path = os.path.join(directory, "mission.csv")
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "phase", "duration_s", "engine_flow_g_s", "ab_flow_g_s",
                "initial_fuel_kg", "initial_cg_m"])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return path

    def test_valid_mission(self):
        rows = mass_rows()
        with tempfile.TemporaryDirectory() as td:
            # Climb: 30s dry (engine_only 25 g/s) -> burn 0.750 kg, remaining 0.870
            # Dash: 5s AB (25+27=52 g/s) -> burn 0.260 kg, remaining 0.610
            # Return: 60s dry (25 g/s) -> burn 1.500 kg (overdraw, needs check)
            # Use conservative numbers that stay within tank
            csv_path = self._write_csv([
                {"phase": "climb", "duration_s": "30", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "0", "initial_fuel_kg": "1.62",
                 "initial_cg_m": "0.9748"},
                {"phase": "dash", "duration_s": "5", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "27", "initial_fuel_kg": "0.870",
                  "initial_cg_m": "1.005439689"},
                {"phase": "return", "duration_s": "20", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "0", "initial_fuel_kg": "0.610",
                  "initial_cg_m": "1.016910246"},
            ], td)
            phases = parse_mission_csv(csv_path, rows)
            self.assertEqual(len(phases), 3)
            self.assertEqual(phases[0]["phase"], "climb")
            self.assertAlmostEqual(phases[0]["fuel_burned_kg"], 0.750, places=4)
            self.assertAlmostEqual(phases[1]["fuel_burned_kg"], 0.260, places=4)
            self.assertAlmostEqual(phases[2]["fuel_burned_kg"], 0.500, places=4)
            self.assertAlmostEqual(phases[2]["fuel_remaining_kg"], 0.110, places=4)

    def test_rejects_negative_duration(self):
        rows = mass_rows()
        with tempfile.TemporaryDirectory() as td:
            csv_path = self._write_csv([
                {"phase": "bad", "duration_s": "-5", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "0", "initial_fuel_kg": "1.62",
                 "initial_cg_m": "0.9748"},
            ], td)
            with self.assertRaises(ValueError):
                parse_mission_csv(csv_path, rows)

    def test_rejects_overdraw(self):
        rows = mass_rows()
        with tempfile.TemporaryDirectory() as td:
            csv_path = self._write_csv([
                {"phase": "bad", "duration_s": "9999", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "27", "initial_fuel_kg": "1.62",
                 "initial_cg_m": "0.9748"},
            ], td)
            with self.assertRaises(ValueError):
                parse_mission_csv(csv_path, rows)

    def test_rejects_fuel_continuity_break(self):
        rows = mass_rows()
        with tempfile.TemporaryDirectory() as td:
            csv_path = self._write_csv([
                {"phase": "a", "duration_s": "10", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "0", "initial_fuel_kg": "1.62",
                 "initial_cg_m": "0.9748"},
                {"phase": "b", "duration_s": "10", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "0", "initial_fuel_kg": "1.50",
                 "initial_cg_m": "0.9800"},
            ], td)
            with self.assertRaises(ValueError):
                parse_mission_csv(csv_path, rows)

    def test_rejects_exceeds_tank_capacity(self):
        rows = mass_rows()
        with tempfile.TemporaryDirectory() as td:
            csv_path = self._write_csv([
                {"phase": "bad", "duration_s": "1", "engine_flow_g_s": "0",
                 "ab_flow_g_s": "0", "initial_fuel_kg": "2.0",
                 "initial_cg_m": "0.9748"},
            ], td)
            with self.assertRaises(ValueError):
                parse_mission_csv(csv_path, rows)

    def test_rejects_nan_value(self):
        rows = mass_rows()
        with tempfile.TemporaryDirectory() as td:
            csv_path = self._write_csv([
                {"phase": "bad", "duration_s": "abc", "engine_flow_g_s": "25",
                 "ab_flow_g_s": "0", "initial_fuel_kg": "1.62",
                 "initial_cg_m": "0.9748"},
            ], td)
            with self.assertRaises(ValueError):
                parse_mission_csv(csv_path, rows)

    def test_rejects_missing_columns(self):
        rows = mass_rows()
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "bad.csv")
            with open(path, "w") as f:
                f.write("phase,duration_s\nclimb,30\n")
            with self.assertRaises(ValueError):
                parse_mission_csv(path, rows)


class TestSubsetRows(unittest.TestCase):
    def test_ab_override(self):
        rows = mass_rows()
        modified = _subset_rows(rows, ab_mass_kg=1.5)
        for name, mass, station in modified:
            if name.startswith("Afterburner"):
                self.assertAlmostEqual(mass, 1.5)

    def test_fuel_station_override(self):
        rows = mass_rows()
        modified = _subset_rows(rows, fuel_station_m=0.55)
        for name, mass, station in modified:
            if name.startswith("Fuel ("):
                self.assertAlmostEqual(station, 0.55)

    def test_no_mutation(self):
        rows = mass_rows()
        original = [(n, m, s) for n, m, s in rows]
        _subset_rows(rows, ab_mass_kg=1.0, fuel_station_m=0.3)
        self.assertEqual([(n, m, s) for n, m, s in rows], original)


class TestCombinedAnalysis(unittest.TestCase):
    def test_returns_all_keys(self):
        rows = mass_rows()
        report = combined_analysis(rows)
        expected_keys = {"sweep", "tolerance", "dry_moment", "fuel_station",
                         "ab_sensitivity", "tank_sweep", "ballast_analysis", "ballast_mtow_proof"}
        self.assertEqual(set(report.keys()), expected_keys)

    def test_dry_moment_consistency(self):
        rows = mass_rows()
        report = combined_analysis(rows)
        dm = report["dry_moment"]
        empty = mass_state(rows, 0)
        self.assertAlmostEqual(dm["dry_mass_kg"], empty["mass_kg"], places=6)
        self.assertAlmostEqual(dm["dry_moment_kg_m"], empty["moment_kg_m"], places=6)


class TestDeterministic(unittest.TestCase):
    def test_invalid_inputs(self):
        for n in (0,-1,1.5,True):
            with self.assertRaises(ValueError):
                fuel_state_sweep(mass_rows(),n)
        for v in (-.1,float("nan"),float("inf"),.1):
            with self.assertRaises(ValueError):
                tolerance_sweep(mass_rows(),mass_tol=v)
        with self.assertRaises(ValueError):
            fuel_state_sweep([])

    def test_sweep_reproducible(self):
        rows = mass_rows()
        s1 = fuel_state_sweep(rows)
        s2 = fuel_state_sweep(rows)
        self.assertEqual(s1, s2)


if __name__ == "__main__":
    unittest.main()
