import unittest

from tools.hardware_budget import (
    AB_PUMP_PLANNING,
    ADS1256ChannelCount,
    MS4525DO_50PSI,
    PACK_V_MIN_ASSUMPTION,
    U3V50F12,
    ads1256_input_conditioning,
    boost_12v_budget,
    check_board_rate,
    check_pressure_sensor,
    isa_static_pa,
    max31856_period,
    pressure_envelope,
    pump_drive_qualified,
    qc_at,
    rail_input_current,
)


class PressureEnvelopeTests(unittest.TestCase):
    def test_qc_reproduces_review_values(self):
        # 25 R09 / 26: qc = 62.237 kPa at M1 and 78.960 kPa at M1.1 (p=69.7 kPa)
        self.assertAlmostEqual(qc_at(3048.0, 1.0), 62237.0, delta=50.0)
        self.assertAlmostEqual(qc_at(3048.0, 1.1), 78960.0, delta=80.0)

    def test_isa_sea_level_and_dash_altitude(self):
        self.assertAlmostEqual(isa_static_pa(0.0), 101325.0, delta=1.0)
        # 10 kft grid value consistent with 69.7 kPa used across the repo
        self.assertAlmostEqual(isa_static_pa(3048.0) / 1000.0, 69.7, delta=0.3)

    def test_qc_hi_sensor_covers_full_planning_envelope(self):
        env = pressure_envelope()
        check = check_pressure_sensor(MS4525DO_50PSI["name"],
                                      MS4525DO_50PSI["full_scale_pa"],
                                      MS4525DO_50PSI["accuracy_frac"],
                                      MS4525DO_50PSI["counts"], 0.0,
                                      env["qc_pa"], MS4525DO_50PSI["proof_pa"])
        self.assertEqual(check["errors"], [])
        self.assertGreater(check["coverage_margin"], 2.0)

    def test_oversized_and_undersized_ranges_fail(self):
        small = check_pressure_sensor("q", 20000.0, 0.0025, 16384, 0.0, 40000.0)
        self.assertTrue(small["errors"])
        # FS above requirement but below the proof-pressure bound is not a fail;
        # a requirement crossing proof pressure is.
        too_big = check_pressure_sensor("q", 500000.0, 0.0025, 16384, 0.0, 50000.0,
                                        proof_pa=20000.0)
        self.assertTrue(too_big["errors"])

    def test_sensor_check_validates_inputs(self):
        base = dict(name="x", full_scale_pa=100, accuracy_frac=0.01, counts=1000,
                    min_req_pa=0.0, max_req_pa=10)
        for field, value in (("full_scale_pa", 0.0), ("counts", 1), ("accuracy_frac", 1.5)):
            kwargs = dict(base)
            kwargs[field] = value
            with self.assertRaises(ValueError):
                check_pressure_sensor(**kwargs)


class PowerRailTests(unittest.TestCase):
    def test_energy_conservation(self):
        cur = rail_input_current(12, 2.0, 6.0, 0.85)
        self.assertAlmostEqual(cur * 6.0 * 0.85, 12.0 * 2.0)

    def test_solenoid_rail_well_within_converter(self):
        rows, limits = boost_12v_budget()
        self.assertLess(rows["solenoid_only_a"], U3V50F12["max_switch_a"])
        self.assertIn("UNQUALIFIED", limits["solenoid_only_a"])

    def test_planning_pack_voltage_is_assumption_not_bound(self):
        self.assertEqual(PACK_V_MIN_ASSUMPTION, 6.0)

    def test_pump_operating_with_solenoid_approaches_switch_limit(self):
        rows, _ = boost_12v_budget()
        # 12 V * (1.5 + 0.5) / (6.0 * 0.85) = 4.71 A planning input current
        self.assertAlmostEqual(rows["pump_op_plus_solenoid_a"], 4.706, places=2)
        self.assertGreaterEqual(rows["pump_op_plus_solenoid_a"] / U3V50F12["max_switch_a"],
                                0.9)

    def test_converter_minimum_voltage_enforced(self):
        with self.assertRaises(ValueError):
            boost_12v_budget(input_v=2.0)

    def test_pump_drive_is_not_qualified(self):
        q = pump_drive_qualified()
        self.assertFalse(q["qualified"])
        self.assertIn("ZY-4S", q["model"])

    def test_invalid_rail_inputs(self):
        for args in ((12, 2, 6, 0.0), (12, 2, 6, 1.1), (0, 2, 6, 0.8)):
            with self.assertRaises(ValueError):
                rail_input_current(*args)


class DacChanTests(unittest.TestCase):
    def test_known_ads1256_pin_counts(self):
        # 4 differential pairs or 8 single-ended inputs (TI datasheet)
        self.assertTrue(ADS1256ChannelCount(4, 0).feasible())
        self.assertTrue(ADS1256ChannelCount(0, 8).feasible())
        self.assertEqual(ADS1256ChannelCount(2, 0).pins_needed(), 4)
        self.assertEqual(ADS1256ChannelCount(0, 6).pins_needed(), 6)

    def test_impossible_single_board_allocation_fails(self):
        # 2 bridges (4 pins) + 6 SE signals (6 pins) = 10 pins > 8
        m = ADS1256ChannelCount(2, 6)
        self.assertEqual(m.pins_needed(), 10)
        self.assertFalse(m.feasible())

    def test_two_board_split_is_feasible(self):
        pairs = [ADS1256ChannelCount(2, 0), ADS1256ChannelCount(0, 6)]
        self.assertTrue(all(p.feasible() for p in pairs))
        self.assertEqual(sum(p.pins_needed() for p in pairs), 10)

    def test_invalid_counts_rejected(self):
        for a, b in ((-1, 0), (0, -1), (1.5, 0)):
            with self.assertRaises(ValueError):
                ADS1256ChannelCount(a, b)

    def test_conditioning_5v_signal_full_scale_and_buffer_limit(self):
        # TI p3: +/-2*Vref/PGA, buffer OFF permits 0..5 V at AVDD=5 V.
        r = ads1256_input_conditioning(2.5, 1, 0.0, 5.0)
        self.assertTrue(r["span_fits"])
        self.assertIsNone(r["needed_divider"])
        self.assertTrue(r["absolute_ok"])
        self.assertFalse(ads1256_input_conditioning(2.5, 1, 0, 5, buffer_on=True)['absolute_ok'])
        self.assertFalse(ads1256_input_conditioning(2.5, 1, -5.1, 0)['span_fits'])
        with self.assertRaises(ValueError):
            ads1256_input_conditioning(5, 8, 0, 0.01)

    def test_bridge_signal_fits_high_gain(self):
        # 2 mV/V at 5 V excitation = 10 mV full scale fits PGA=8 (+-0.3125 V)
        r = ads1256_input_conditioning(2.5, 8, -0.010, 0.010, common_mode_v=2.5, buffer_on=True)
        self.assertTrue(r["span_fits"])
        self.assertTrue(r['absolute_ok'])
        self.assertAlmostEqual(r['window_v'], 0.625)

    def test_board_rate_oversubscription_fails(self):
        ok = check_board_rate(2000, 1000)
        self.assertTrue(ok["schedulable"])
        bad = check_board_rate(1000, 900)
        self.assertFalse(bad["schedulable"])
        with self.assertRaises(ValueError):
            check_board_rate(1500, 1000)

    def test_max31856_timing_datasheet_table(self):
        # 1-shot / first conversion 60 Hz max 155 ms; auto 2..n 60 Hz max 90 ms
        self.assertAlmostEqual(max31856_period(60, 1, "oneshot"), 0.155, places=3)
        self.assertAlmostEqual(max31856_period(60, 1, "auto"), 0.090, places=3)
        # averaging 4 adds 3*16.67 ms in auto mode
        self.assertAlmostEqual(max31856_period(60, 4, "auto"), 0.090 + 3 * 0.01667,
                               places=3)
        # fault testing on each conversion adds its inset time
        self.assertAlmostEqual(max31856_period(60, 1, "oneshot", "<5k"),
                               0.155 + 0.015, places=3)
        with self.assertRaises(ValueError):
            max31856_period(480, 1, "oneshot")
        self.assertAlmostEqual(max31856_period(60, 4, 'oneshot'), 0.155+3*0.03333)
        self.assertAlmostEqual(max31856_period(50, 4, 'first'), 0.185+3*0.040)
        for n in (3, 0, float('inf'), float('nan')):
            with self.assertRaises(ValueError):
                max31856_period(60, n)

    def test_nonfinite_and_invalid_sensor_ranges(self):
        for kwargs in ({'max_req_pa': 0}, {'min_req_pa': 20}, {'proof_pa': float('nan')},
                       {'counts': 2.5}, {'full_scale_pa': float('inf')}):
            args = dict(name='x', full_scale_pa=100, accuracy_frac=0.01,
                        counts=1000, min_req_pa=0, max_req_pa=10)
            args.update(kwargs)
            with self.assertRaises(ValueError):
                check_pressure_sensor(**args)
        self.assertTrue(check_pressure_sensor('x', 80, .01, 100, 0, 100, sensor_min_pa=30)['errors'])
        with self.assertRaises(ValueError):
            ads1256_input_conditioning(2.5, 1, 0, float('nan'))


if __name__ == "__main__":
    unittest.main()
