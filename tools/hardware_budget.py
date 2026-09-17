"""Instrumentation, power and DAQ budget checks for 33.

Covers readiness items R09 (pressure chain ranges), R10 (2S->12 V boost rail)
and R11 (ADS1256/MAX31856 channel, gain and timing allocation). Figures are
PLANNING calculations; exact pressure options/static specs remain unverified
(see 33 for evidence and source conflicts). No part is qualified, no
hardware test result is implied. Reproduction: python3 tools/hardware_budget.py

Sources (retrieved 2026-09-16):
  - ISA troposphere pressure model (ISA standard atmosphere, 0-11 km).
  - airdata.pitot_ratio for qc = p_s*(pt/ps - 1), NASA normal-shock relations.
  - TE MS4525DO datasheet ENG_DS_MS4525DO_B11 (via mouser/futureelectronics),
    TE product pages 4525DO-DS3BJ050DP / 4525DO-DS5AI001DP.
  - TE MS5803-02BA product catalog page (CAT-BLPS0010); MS5611-01BA equivalent
    family via DigiKey product highlight.
  - Pololu U3V50F12 (item #2568) product/specs pages.
  - TI ADS1256 product page/datasheet Rev. K.
  - Analog Devices MAX31856 datasheet (19-7534; Rev 0; 2/15).

A note on the AB pump: the "Speck ZY-4S-12V" model named in 15/18/22 was not
found in the Speck Pumpen catalog on 2026-09-16. Until a real pump part,
motor type and driver datasheet are sourced, the motor-drive/boost sizing for
the pump is STOPPED (pump_drive_qualified() == False) per ASSIGNMENT E.
"""
import math

try:
    from tools.airdata import pitot_ratio
except ModuleNotFoundError:  # direct script execution from the repository root
    from airdata import pitot_ratio

# --------------------------------------------------------------------------
# ISA troposphere static pressure model (planning envelope)
# --------------------------------------------------------------------------
T0_K = 288.15
P0_PA = 101325.0
LAPSE = 0.0065           # K/m, troposphere up to 11 km
G0 = 9.80665             # m/s^2
R_AIR = 287.05           # J/(kg K)


def isa_static_pa(alt_m):
    """ISA troposphere static pressure at geometric altitude alt_m (0-11 km)."""
    if not 0.0 <= alt_m <= 11000.0:
        raise ValueError("alt_m must be within troposphere 0..11000 m")
    temp_k = T0_K - LAPSE * alt_m
    return P0_PA * (temp_k / T0_K) ** (G0 / (LAPSE * R_AIR))


def qc_at(alt_m, mach):
    """Impact pressure qc = p_pitot - p_static (Pa) for this Mach and altitude."""
    if not 0.0 <= mach <= 3.0:
        raise ValueError("mach must be within 0..3 numerical domain")
    return isa_static_pa(alt_m) * (pitot_ratio(mach) - 1.0)


# Planned flight envelope for range selection. This is the PLANNING envelope
# (ground up to 12 kft, M up to 1.2 transient), not a release envelope. The
# certification dash itself is M 1.05-1.10 at 10-12 kft per 18 section 2.
ENVELOPE_ALT_M = [0.0, 2438.4, 3048.0, 3657.6]          # 0, 8, 10, 12 kft
ENVELOPE_MACH = [0.3, 0.5, 0.8, 0.9, 1.0, 1.1, 1.2]
SPEED_ALT_LABELS = {0.0: "0 (SL)", 2438.4: "8 kft", 3048.0: "10 kft",
                    3657.6: "12 kft"}


def pressure_envelope():
    """Max qc over the planning envelope plus its (alt, Mach) location."""
    worst = {"qc_pa": 0.0, "alt_m": None, "mach": None}
    for alt in ENVELOPE_ALT_M:
        for mach in ENVELOPE_MACH:
            qc = qc_at(alt, mach)
            if qc > worst["qc_pa"]:
                worst = {"qc_pa": qc, "alt_m": alt, "mach": mach}
    return worst


# --------------------------------------------------------------------------
# Pressure sensor range / margin checks (R09)
# --------------------------------------------------------------------------
def check_pressure_sensor(name, full_scale_pa, accuracy_frac, counts,
                          min_req_pa, max_req_pa, proof_pa=None, sensor_min_pa=0.0):
    """Margin/quantization check for one sensor against a required band.

    full_scale_pa: measurable span. accuracy_frac: e.g. 0.0025 span.
    counts: ADC counts across FS (14-bit -> 16384; 24-bit -> 16777216)
    giving the ideal per-count quantization. proof_pa: proof pressure.
    Datasheet RMS resolution (resolution_pa) may be reported separately; it is
    coarser than ideal quantization for delta-sigma parts.
    """
    for val, label in ((full_scale_pa, "full scale"), (accuracy_frac, "accuracy"),
                       (counts, "counts"), (min_req_pa, "min req"),
                       (max_req_pa, "max req")):
        if not math.isfinite(val) or val < 0:
            raise ValueError(f"{label} must be finite and non-negative")
    if accuracy_frac > 1.0:
        raise ValueError("accuracy_frac must be <= 1")
    if counts < 2 or full_scale_pa <= 0:
        raise ValueError("full_scale_pa must be positive and counts >= 2")
    if not isinstance(counts, int) or isinstance(counts, bool):
        raise ValueError("counts must be an integer")
    if max_req_pa <= 0 or min_req_pa > max_req_pa:
        raise ValueError("required band must be ordered with positive maximum")
    if not math.isfinite(sensor_min_pa) or sensor_min_pa < 0:
        raise ValueError("sensor minimum must be finite and nonnegative")
    if proof_pa is not None and (not math.isfinite(proof_pa) or proof_pa <= 0):
        raise ValueError("proof pressure must be finite and positive")
    margin = (sensor_min_pa + full_scale_pa) / max_req_pa
    lsb_pa = full_scale_pa / counts
    accuracy_pa = accuracy_frac * full_scale_pa
    errors = []
    if min_req_pa < sensor_min_pa:
        errors.append("minimum requirement below sensor measurement range")
    if max_req_pa > sensor_min_pa + full_scale_pa:
        errors.append(f"max requirement {max_req_pa:.0f} Pa exceeds FS {full_scale_pa:.0f} Pa")
    if proof_pa is not None and max_req_pa > proof_pa:
        errors.append(f"max requirement {max_req_pa:.0f} Pa exceeds proof {proof_pa:.0f} Pa")
    usable = dict(usable_min_pa=min_req_pa, usable_max_pa=max_req_pa,
                  note="usable calibrated bounds must come from the calibration record")
    return {"name": name, "full_scale_pa": full_scale_pa,
            "coverage_margin": margin, "max_req_pa": max_req_pa,
            "lsb_pa": lsb_pa, "accuracy_pa": accuracy_pa,
            "errors": errors, "usable_bounds": usable}


# Candidate codes exist on TE pages; supply/address/transfer/proof and total
# error band require exact ordering-table confirmation. No procurement release.
MS4525DO_50PSI = dict(name="TE 4525DO-DS3BJ050DP (qc hi)",
                      full_scale_pa=50.0 * 6894.757, accuracy_frac=0.0025,
                       counts=14745, proof_pa=300.0 * 6894.757)
MS4525DO_1PSI = dict(name="TE 4525DO-DS5AI001DP (qc lo)",
                     full_scale_pa=1.0 * 6894.757, accuracy_frac=0.0025,
                      counts=13107, proof_pa=None)
MS5803_02BA = dict(name="TE MS5803-02BA (static, specs unverified)", full_scale_pa=80000.0,
                   accuracy_frac=0.003125, counts=16777216, proof_pa=None)
# MS5803-02BA accuracy is absolute: +-2.5 mbar over 300-1100 mbar.

# --------------------------------------------------------------------------
# 2S -> 12 V rail (R10)
# --------------------------------------------------------------------------
# Planning electrical loads from 23 section 5 (declared planning values, not
# measured ratings). Pump figures come from the ORIGINAL load table and carry
# a planning-only status because the pump part itself is unverified.
AB_PUMP_PLANNING = dict(operating_a_12v=1.5, max_a_12v=1.8)
AB_SOLENOID_12V_A = 0.5
PACK_V_NOMINAL = 7.4
# Assumption, NOT an approved discharge limit: worst-case planning pack
# voltage used for the boost input-current check. BMS/ECU low-voltage cutoffs
# are a separate qualification.
PACK_V_MIN_ASSUMPTION = 6.0
CONV_12V_EFF_PLANNING = 0.85
# Pololu U3V50F12 (item #2568), product page 2026-09-16: boosted 12 V output,
# min input 2.9 V, max input current/switch 5 A; output current is thermally
# limited and must be taken from the efficiency/output-current table of the
# measured unit.
U3V50F12 = dict(name="Pololu U3V50F12 (#2568)", min_vin_v=2.9, max_switch_a=5.0,
                supply_price_usd_2026_09_16=29.95)


def rail_input_current(output_v, output_a, input_v, efficiency):
    """Battery-side current for a switched rail (energy conservation)."""
    if not all(math.isfinite(v) for v in (output_v, output_a, input_v, efficiency)):
        raise ValueError("rail inputs must be finite")
    if output_v <= 0 or output_a < 0 or input_v <= 0 or not 0 < efficiency <= 1:
        raise ValueError("invalid voltage/current/efficiency")
    return output_v * output_a / (input_v * efficiency)


def engine_supply_window(supply_min_v, supply_max_v):
    """Voltage-only check: JetCat P550-PRO datasheet V1.1 02/2023 p1.

    Primary source: https://www.jetcat.de/jetcat/anleitungen/P550-PRO-Datasheet.pdf
    Names 10–35 VDC. Current, startup, transients and exact installed variant
    require the manufacturer's installation specification; this is not sizing.
    """
    if not all(math.isfinite(v) and v > 0 for v in (supply_min_v, supply_max_v)) or supply_min_v > supply_max_v:
        raise ValueError("supply voltage window must be finite, positive and ordered")
    return {"supply_min_v": supply_min_v, "supply_max_v": supply_max_v,
            "datasheet_min_v": 10.0, "datasheet_max_v": 35.0,
            "voltage_window_compatible": supply_min_v >= 10 and supply_max_v <= 35,
            "physical_qualified": False,
            "source": "JetCat P550-PRO datasheet V1.1 02/2023 p1; exact installed variant/current/startup unverified"}


def boost_12v_budget(input_v=PACK_V_MIN_ASSUMPTION,
                     efficiency=CONV_12V_EFF_PLANNING,
                     converter=U3V50F12):
    """Input current for the 12 V rail (solenoid alone, pump alone, both)."""
    if not math.isfinite(input_v) or not converter["min_vin_v"] <= input_v <= 12:
        raise ValueError("boost input must be finite and within minimum..12 V")
    if not math.isfinite(converter["max_switch_a"]) or converter["max_switch_a"] <= 0:
        raise ValueError("invalid converter current screen")
    sol = rail_input_current(12.0, AB_SOLENOID_12V_A, input_v, efficiency)
    pump_op = rail_input_current(12.0, AB_PUMP_PLANNING["operating_a_12v"],
                                 input_v, efficiency)
    pump_max = rail_input_current(12.0, AB_PUMP_PLANNING["max_a_12v"],
                                  input_v, efficiency)
    both = sol + pump_op
    rows = {"solenoid_only_a": sol, "pump_operating_a": pump_op,
            "pump_max_a": pump_max, "pump_op_plus_solenoid_a": both,
            "pump_max_plus_solenoid_a": pump_max + sol}
    limits = {k: ("UNQUALIFIED: below typical input-current screen" if v <= converter["max_switch_a"]
                  else "EXCEEDS typical input-current screen; UNQUALIFIED")
              for k, v in rows.items()}
    return rows, limits


def pump_drive_qualified():
    """False: Speck ZY-4S-12V could not be verified on 2026-09-16."""
    return {"qualified": False, "model": "Speck ZY-4S-12V (from 15/18/22)",
            "reason": ("not found in Speck Pumpen catalog pages searched 2026-09-16; "
                       "motor type/driver unknown; no guessed BLDC ESC; boost rail "
                       "sizing for the pump motor is STOPPED pending a real pump "
                       "part with a driver/motor datasheet")}


# --------------------------------------------------------------------------
# DAQ channel / pin / rate checks (R11)
# --------------------------------------------------------------------------
class ADS1256ChannelCount:
    """Feasibility check of a wiring map against ADS1256 input pins.

    ADS1256 provides four differential pairs or eight single-ended inputs on
    the same AIN0..AIN7 pins (TI ADS1256 datasheet Rev. K / product page). A
    differential pair consumes two pins; a single-ended signal consumes one.
    """

    def __init__(self, diff_pairs, se_channels):
        if not all(type(x) is int and x >= 0 for x in (diff_pairs, se_channels)):
            raise ValueError("channel counts must be non-negative integers")
        self.diff_pairs = diff_pairs
        self.se_channels = se_channels

    def pins_needed(self):
        return self.diff_pairs * 2 + self.se_channels

    def feasible(self):
        return self.pins_needed() <= 8

    def summary(self):
        return {"diff_pairs": self.diff_pairs, "se_channels": self.se_channels,
                "pins_needed": self.pins_needed(),
                "pins_available": 8, "feasible": self.feasible()}


def ads1256_input_conditioning(vref_v, pga, signal_min_v, signal_max_v,
                               avdd_v=5.0, buffer_on=False, common_mode_v=None):
    """TI Rev K p3: differential +/-2*VREF/PGA; check BOTH input pins.
    If common_mode_v is None, AINN=0 (SE); otherwise AINP/N=CM +/- signal/2.
    Reference pins themselves, source impedance and external filters need review.
    """
    values = (vref_v, pga, signal_min_v, signal_max_v, avdd_v)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("ADC inputs must be finite")
    if not 0.5 <= vref_v <= 2.6 or pga not in (1, 2, 4, 8, 16, 32, 64) or signal_max_v < signal_min_v or not 4.75 <= avdd_v <= 5.25:
        raise ValueError("invalid vref/gain/signal limits")
    if not isinstance(buffer_on, bool):
        raise ValueError("buffer_on must be boolean")
    if common_mode_v is not None and not math.isfinite(common_mode_v):
        raise ValueError("common mode must be finite")
    window_v = 2 * vref_v / pga
    peak = max(abs(signal_min_v), abs(signal_max_v))
    if peak <= window_v:
        span_ok = True
        divider = None
    else:
        span_ok = False
        divider = window_v / peak
    abs_lo_v, abs_hi_v = (0.0, avdd_v - 2.0) if buffer_on else (-0.1, avdd_v + 0.1)
    pins = [0.0, signal_min_v, signal_max_v] if common_mode_v is None else [
        common_mode_v + sign * v / 2 for sign in (-1, 1) for v in (signal_min_v, signal_max_v)]
    abs_ok = all(abs_lo_v <= pin <= abs_hi_v for pin in pins)
    return {"window_v": window_v, "span_fits": span_ok,
            "needed_divider": divider, "absolute_ok": abs_ok,
            "pin_limits_v": (abs_lo_v, abs_hi_v), "qualified": False}


# ADS1256 has discrete rate settings, not arbitrary rates up to 30 kSPS. The
# per-board scheduling overhead for multiplexing/SPI is a planning allowance,
# NOT a measured throughput; DRDY-measured throughput is the qualification.
SCHEDULE_OVERHEAD_FRACTION = 0.95
# TI Rev K Table 14, fCLKIN=7.68 MHz, fSCLK=fCLKIN/4, WREG/SYNC/WAKEUP.
ADS1256_MUX_SPS = {30000: 4374, 15000: 3817, 7500: 3043, 3750: 2165,
                  2000: 1438, 1000: 837, 500: 456, 100: 98, 60: 59,
                  50: 50, 30: 30, 25: 25, 15: 15, 10: 10, 5: 5, 2.5: 2.5}


def check_board_rate(rate_hz, requested_sps):
    if rate_hz <= 0 or requested_sps < 0 or not math.isfinite(rate_hz + requested_sps):
        raise ValueError("rates must be finite and positive")
    if rate_hz not in ADS1256_MUX_SPS:
        raise ValueError("unsupported ADS1256 data rate at 7.68 MHz")
    throughput = ADS1256_MUX_SPS[rate_hz]
    return {"rate_hz": rate_hz, "requested_sps": requested_sps,
            "mux_throughput_sps": throughput, "qualified": False,
            "schedulable": requested_sps <= throughput * SCHEDULE_OVERHEAD_FRACTION,
            "headroom_planning_fraction": SCHEDULE_OVERHEAD_FRACTION}


# MAX31856 conversion timing. From the ANALOG DEVICES datasheet
# (19-7534, Rev 0, 2/15), Electrical Characteristics and "Typical conversion
# times" note: tCONV (thermocouple + cold junction) for a 1-shot / first
# conversion in auto mode is 143-155 ms (60 Hz) or 169-185 ms (50 Hz);
# conversions 2..n in auto mode are 82-90 ms (60 Hz) or 98-110 ms (50 Hz).
# Averaging adds TYPICAL (samples-1)*33.33 ms (first, 60 Hz) or *16.67 ms (auto 2..n).
# Fault-test time (OCFAULT, CJ enabled): 13.3 typ/15 max ms (RS<5k) or
# 33.4 typ/37 max ms (RS 5-40k, RC<2ms); RC>2ms uses 125ms maximum.
# Automatic tests occur every 16 conversions. The 16.6 ms figure is the averaging
# increment of the 60 Hz filter, NOT a conversion period.
MAX31856_TABLE = {
    "first_or_oneshot": {"60Hz": (0.143, 0.155), "50Hz": (0.169, 0.185)},
    "auto_2_to_n": {"60Hz": (0.082, 0.090), "50Hz": (0.098, 0.110)},
}
MAX31856_AVERAGE_INCREMENT = {"60Hz": 0.01667, "50Hz": 0.020}
MAX31856_FAULT_TEST = {"RS_lt_5k_CJ": (0.0133, 0.015), "RS_5k_40k_CJ": (0.0334, 0.037)}


def max31856_period(filter_hz, averaging=1, mode="auto", fault_rs=None):
    """Planning interval: maximum base + TYPICAL averaging increments.
    fault_rs adds a test-containing interval (CJ enabled), not an average rate.
    Auto fault tests occur every 16 conversions. Not a guaranteed max with averaging.
    """
    if filter_hz not in (50, 60):
        raise ValueError("filter_hz must be 50 or 60")
    if averaging not in (1, 2, 4, 8, 16) or isinstance(averaging, bool):
        raise ValueError("averaging must be 1, 2, 4, 8 or 16")
    if mode not in ("auto", "oneshot", "first"):
        raise ValueError("mode must be 'auto', 'first' or 'oneshot'")
    key = "first_or_oneshot" if mode in ("oneshot", "first") else "auto_2_to_n"
    if mode == "auto" and averaging == 1:
        key = "auto_2_to_n"
    base = MAX31856_TABLE[key][f"{filter_hz}Hz"][1]
    avg_inc = MAX31856_AVERAGE_INCREMENT[f"{filter_hz}Hz"]
    if mode in ("oneshot", "first"):
        avg_inc = {60: 0.03333, 50: 0.040}[filter_hz]
    total = base + (averaging - 1) * avg_inc
    if fault_rs is not None:
        if fault_rs == "<5k":
            total += MAX31856_FAULT_TEST["RS_lt_5k_CJ"][1]
        elif fault_rs == "5-40k":
            total += MAX31856_FAULT_TEST["RS_5k_40k_CJ"][1]
        elif fault_rs == "5-40k_slow":
            total += 0.125  # Table 4, RC > 2 ms, CJ enabled
        else:
            raise ValueError("fault_rs must be '<5k', '5-40k' (RC<2ms), '5-40k_slow' or None")
    return total


def drdy_requires_source_clock():
    """DRDY must gate reads; register-read arrival stamps are not conversions."""
    return ("source-clock DRDY interval is the acquisition period; repeated "
            "register reads without DRDY are arrival stamps, not conversion "
            "evidence (26 section 4).")


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
def report():
    env = pressure_envelope()
    qc_hi = check_pressure_sensor(MS4525DO_50PSI["name"],
                                  MS4525DO_50PSI["full_scale_pa"],
                                  MS4525DO_50PSI["accuracy_frac"],
                                  MS4525DO_50PSI["counts"], 0.0, env["qc_pa"],
                                  MS4525DO_50PSI["proof_pa"])
    qc_lo = check_pressure_sensor(MS4525DO_1PSI["name"],
                                  MS4525DO_1PSI["full_scale_pa"],
                                  MS4525DO_1PSI["accuracy_frac"],
                                  MS4525DO_1PSI["counts"], 0.0,
                                  1.0 * 6894.757)
    static_min = isa_static_pa(3657.6)
    static_max = isa_static_pa(0.0)
    ms5803 = check_pressure_sensor(MS5803_02BA["name"], MS5803_02BA["full_scale_pa"],
                                    MS5803_02BA["accuracy_frac"], MS5803_02BA["counts"], static_min,
                                    static_max, MS5803_02BA["proof_pa"], sensor_min_pa=30000.0)
    ms5803["spec_status"] = "unverified assumed band/accuracy; raw 24-bit count is NOT pressure resolution"
    ms5803["lsb_pa"] = None
    boost, boost_limits = boost_12v_budget()
    pump = pump_drive_qualified()
    bench_map = {"bridge_ads1256": ADS1256ChannelCount(2, 0).summary(),
                 "pressure_ads1256": ADS1256ChannelCount(0, 6).summary(),
                 "single_board_all_10pins": ADS1256ChannelCount(2, 6).summary()}
    return {"pressure_envelope": env,
             "engine_supply": engine_supply_window(PACK_V_MIN_ASSUMPTION, 8.4),
            "sensors": {"qc_hi": qc_hi, "qc_lo": qc_lo, "static": ms5803},
            "boost_12v": {"rows": boost, "limits": boost_limits,
                          "converter": U3V50F12,
                          "pack_v_min_assumption": PACK_V_MIN_ASSUMPTION,
                          "note": "planning assumption, not an approved discharge limit"},
            "pump_drive": pump,
            "daq_channel_map": bench_map,
            "max31856": {"period_s_oneshot_60hz_max": max31856_period(60, 1, "oneshot"),
                         "period_s_auto_60hz_max": max31856_period(60, 1, "auto"),
                         "ti_ads1256_confirmed": ("4 differential pairs / 8 single-ended "
                                                  "inputs on AIN0..7; single-cycle "
                                                   "settling per Tables 13/14; +/-2*VREF/PGA")}}


if __name__ == "__main__":
    r = report()
    env = r["pressure_envelope"]
    print(f"Planning pressure envelope: max qc = {env['qc_pa']:.0f} Pa at "
          f"M{env['mach']:.1f}, alt {env['alt_m']:.0f} m "
          f"({SPEED_ALT_LABELS[env['alt_m']]})")
    for name, s in r["sensors"].items():
        res = f", conditional Pa/count {s['lsb_pa']}" if s['lsb_pa'] is not None else ", pressure resolution UNVERIFIED"
        print(f"  {s['name']}: FS {s['full_scale_pa']:.0f} Pa, coverage "
              f"{s['coverage_margin']:.2f}x, acc {s['accuracy_pa']:.0f} Pa{res} "
              f"{'RANGE SCREEN ONLY; UNQUALIFIED' if not s['errors'] else 'ERROR: ' + '; '.join(s['errors'])}")
    p = r["pump_drive"]
    print(f"Pump drive QUALIFIED={p['qualified']}: {p['reason']}")
    engine = r["engine_supply"]
    print(f"P550-PRO direct 2S supply ({engine['supply_min_v']}–{engine['supply_max_v']} V) "
          f"within manufacturer 10–35 V: {engine['voltage_window_compatible']}; architecture OPEN")
    rows = r["boost_12v"]["rows"]
    lims = r["boost_12v"]["limits"]
    print(f"12V boost rail at pack {r['boost_12v']['pack_v_min_assumption']} V "
          f"(planning assumption, eff {CONV_12V_EFF_PLANNING}):")
    for k in rows:
        print(f"  {k}: {rows[k]:.2f} A  {lims[k]}")
    print(f"  converter: {r['boost_12v']['converter']['name']}, switch "
          f"{r['boost_12v']['converter']['max_switch_a']} A, min Vin "
          f"{r['boost_12v']['converter']['min_vin_v']} V")
    for k, m in r["daq_channel_map"].items():
        print(f"  {k}: {m['diff_pairs']} diff + {m['se_channels']} SE -> "
              f"{m['pins_needed']} pins, feasible={m['feasible']}")
    print(f"  MAX31856 one-shot/60Hz max period: "
          f"{r['max31856']['period_s_oneshot_60hz_max']*1000:.0f} ms; auto 2..n: "
          f"{r['max31856']['period_s_auto_60hz_max']*1000:.0f} ms")
    print("Planning calculations only: calibration, thermal, EMI, startup/stall "
          "and DRDY throughput hardware tests still gate release.")
