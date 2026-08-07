# Afterburner Bench Test Program (Build-Ready)

**Doc:** 21 — Afterburner bench qualification package
**Author:** E2 (Propulsion/Afterburner)
**Date:** 2026-08-06
**Status:** 🟡 baseline corrected; ready to build rig
**Engine:** JetCat P550-PRO + afterburner, single engine
**Condition under test (reference):** Mach 1 @ 10,000 ft

> **CORRECTED 2026-08-06 per 18 §2 and this doc: mass flow at M1/10kft is 1.10 kg/s (not 0.69).** All thrust, fuel-flow and thermal numbers below are derived from the corrected-flow model (18 §2.1, 13 Method B). The analysis script that produced every number is `tools/ab_bench_analysis.py` (committed, AGENTS.md §4.4). Where a value cannot be derived (empirical coefficients), the test that must produce it is named.

---

## 1. Corrected AB Performance Model (ṁ = 1.10 kg/s)

**Authority:** 18 §2.1 — corrected mass flow ṁ = 1.10 kg/s at M1/10 kft; Vj_dry = 566 m/s (TIT-limited, 13:123); T5,dry ≈ 1000 K (18 §2.1, 13:120); V∞ = a = 328 m/s (13:65).

Model (simple momentum, no pressure term — matches 18 §2.1, which shows the (Pe−Pa)Ae term ≈ negligible at ~1 N):

```
Vj(T7) = Vj_dry × √(T7/1000)        [Vj scales as √T for a choked, fixed-area nozzle]
gross  = ṁ × Vj                      [ṁ = 1.10 kg/s, wet]
ram    = ṁ × V∞ = 1.10 × 328         [V∞ = 328 m/s]
net    = gross − ram
boost  = net / 257 N                 [dry net @ M1/10kft, 18 §2.1]
```

### Computed table (from `tools/ab_bench_analysis.py`, verified 2026-08-06)

```
SEC 1: CORRECTED WET THRUST MODEL AT MDOT = 1.10 kg/s (M1 / 10 kft)
  Vj(T7) = Vj_dry*sqrt(T7/1000) = 566*sqrt(T7/1000)
  gross  = mdot*Vj        ram = mdot*Vinf = 1.10*328
  net    = gross - ram    boost vs dry net 257 N (18 sec 2.1)
  T7 K   Vj m/s   gross N   ram N   net N  boost
  1700    738.0     811.8   360.8   451.0  175%
  1800    759.4     835.3   360.8   474.5  185%
  1900    780.2     858.2   360.8   497.4  194%
```

Interpretation: the **boost column is net ÷ dry** (175% means net = 1.75 × 257 N = +75 %).

| T7 (K) | Vj (m/s) | Gross (N) | Ram (N) | **Net (N)** | vs dry 257 N |
|--------|----------|-----------|---------|-------------|--------------|
| 1700   | 738      | 812       | 361     | **451**     | +75 % |
| **1800** | **759** | **835**   | 361     | **474**     | **+85 %** |
| 1900   | 780      | 858       | 361     | **497**     | +94 % |

Key results:
- **Design point (T7 = 1800 K): net wet = 474 N** — inside the 18 §2.1 450–475 N band (design point 465 N).
- **The 450 N gate is met even at T7 = 1700 K (451 N)** — a useful thermal margin for the first qualification runs.
- The OLD model (0.69 kg/s, 17) gave ~300 N — that configuration cannot close the mission and is void.

---

## 2. Corrected AB Fuel Flow & O₂ Balance (T7 = 1800 K)

**Energy balance** (same equation as 17 §1a, corrected inputs):

```
ṁ_fuel = ṁ × cp × (T7 − T5) / (LHV × η)
       = 1.10 × 1200 × (1800 − 1000) / (43e6 × 0.90)
       = 0.0273 kg/s = 27.3 g/s
```

Note: **T5 = 1000 K** (18 §2.1, TIT-limited dry turbine-exit). 17 §1a used 973 K; 18 supersedes — the small difference changes the answer < 2 %.

**O₂ check** (exhaust O₂ mass fraction 0.155, from 14 % mole fraction; stoichiometric demand 3.40 kg O₂/kg fuel — 17 §1a, chemistry unchanged):

| Quantity | Value |
|----------|-------|
| ṁ_O₂ available | 1.10 × 0.155 = **0.171 kg/s** |
| ṁ_O₂ consumed | 0.0273 × 3.40 = **0.093 kg/s** |
| **Fraction consumed (φ, O₂-based)** | **54.4 %** — fuel-lean, safe margin |
| Static-SL bench fuel (ṁ = 0.95) | **23.6 g/s** |
| Per 5 s burst (AB only) | **136 g ≈ 168 ml** |
| Per 20 s burst (AB only) | **546 g ≈ 674 ml** |

**Pump check (Speck ZY-4S-12V, 15):** requirement 27.3 g/s at M1. Pump curve (15:90-91): 4 bar → 44 g/s (**1.61× margin**), 6 bar → 34 g/s (1.25×). Run the pump at **4 bar, ~27–34 g/s** for the M1 case; on the static bench, meter to **T7 = 1800 K** (~24 g/s). Abort authority and flow metering per 15.

---

## 3. Corrected Thermal Numbers (mass-flow-dependent)

**Liner (D = 0.08 m, L = 0.20 m, A = 0.0503 m²; 17 §1b geometry unchanged):**

```
Re = 4ṁ/(π D μ) = 4×1.10/(π×0.08×4e-5) = 438,000   (was 274,500 at 0.69)
Gnielinski: f = 0.0135, Nu = 578, h = Nu·k/D = 578 W/m²K
q_conv = h·(Tg−Tw) = 578 × 800 = 462 kW/m²   (was 318)
q_rad  = 0.25·σ·(1800⁴ − 1000⁴) = 135 kW/m²   (unchanged — T-dependent only)
q_total = 597 kW/m²   (was 453)
Q_total = 597,000 × 0.0503 = 30.0 kW   (was 22.8)
Q/AB_power = 30.0 / 1173 = 2.6 %   (unchanged ~3 %; AB power 1173 kW)
```

**Cooling bleed & film holes:**

```
Target film bleed 2.5 % of core: ṁ_film = 0.0275 kg/s   (was 0.0173)
Per-hole choked flow (1 mm, Cd 0.8, unchanged) = 2.47e-4 kg/s
→ 0.0275 / 2.47e-4 = 111 holes   (was 65)
q_conv-scaled alternative (bleed ∝ Re^0.8 ≈ 1.45×): 0.0251 kg/s → 102 holes
```

Recommend **~105–115 holes in 5–6 staggered rows** (row plan per 17 §1c scaled ×1.7), **confirmed empirically in Phase 1.3** (all holes flowing within ±10 %). Do not rely on the old 20-hole single row — with corrected q_total it leaves the liner unprotected.

**Annulus / shell (17 §1e, scaled):**

```
ṁ_cool_ann = 2.3 % × 1.10 = 0.0253 kg/s
V_ann = 0.0253/(0.574 × 0.00108) = 40.8 m/s
Re_ann = 7,500   →   h_ann = 125 W/m²K
Q through shell ≈ 4.7 kW → T_cool_out ≈ 610 K (337 °C)
```

Outer shell surface ≈ 337 °C — **above the 200 °C composite-contact limit**. Mitigation from 17 §1e is **mandatory**: 5 mm ceramic blanket (Cotronics 3633) + polished foil between shell and fuselage → fuselage < 100 °C. **Shell temperature is a measured PASS criterion (< 200 °C), not an assumption.**

**Ram scoop (17 §2c re-derived):** required cooling 3 % of core = **0.033 kg/s**; A = 0.033/(0.905×328×0.8) = 1.39e-4 m² → **equivalent Ø ≈ 13.3 mm** (was ~10.6 mm at 0.69).

**Film hole / bleed margin note:** bleed fraction-of-core is the tractable scaling (task directive); the physically derived requirement (∝ Re^0.8) is ~8 % lower. Final count = bench result.

---

## 4. Bench Test Matrix

Structure: 17 §3a Phases 1–4 retained, **corrected to ṁ = 1.10 kg/s**, plus a Phase 0 (rig/DAQ readiness) and Phase 5 (qualification). All durations are calendar/wall-clock days at full-rate test (one shift). **Minimum logging 100 Hz for thrust, EGT (T5), and T7 during AB bursts; 500 Hz for Phase 5 gate runs** (§5).

### Phase 0 — Rig & DAQ readiness

| Step | Test | Measurements | PASS/FAIL | Duration |
|------|------|--------------|-----------|----------|
| 0.1 | Thrust stand build & tare | Load-cell zero, hysteresis, creep at 500 N for 1 h | Tare stable ±2 N; linearity ±1 N over 0–800 N | 2 d |
| 0.2 | DAQ channel verification | All channels, simulated signals | Each channel reads within spec (§5); 100 Hz sustained | 1 d |
| 0.3 | Fuel pump calibration | Speck ZY-4S-12V flow vs PWM at 4/5/6 bar | Match 15:90-91 curve ±5 %; no pressure ripple >0.1 bar | 1 d |
| 0.4 | Iris actuator calibration | Throat dia vs servo position | 45 mm dry ↔ 55 mm wet, repeatable ±0.3 mm, fails open on power loss | 1 d |

### Phase 1 — Cold flow (air, no fuel, no engine)

| Step | Test | Measurements | PASS/FAIL | Duration |
|------|------|--------------|-----------|----------|
| 1.1 | Compressed air through AB at **1.10 kg/s equivalent** | ΔP across spray ring, flame holder, liner; T (≈300 K) | ΔP per component stable ±5 %; total AB back-pressure < 5 % of engine limit at 1.10 kg/s | 1 d |
| 1.2 | Flow sweep 0.2–1.2 kg/s | ΔP vs ṁ curve (component coefficients) | Monotonic, repeatable; supply capable of ≥1.0 kg/s (note: if bench air-limited, run 0.2–0.9 and extrapolate Re) | 1 d |
| 1.3 | Film-hole distribution at 1.10 kg/s | Flow per hole (drilled plates / surface-tension probes) | All ~105–115 holes within ±10 %; no dead holes | 1 d |
| 1.4 | Iris nozzle calibration at 0.6 kg/s | Throat area vs position, discharge coefficient Cd | Cd 0.95 ±0.05 dry/wet; throat 45/55 mm per §0.4 | 1 d |
| 1.5 | **Nozzle-matching check** | Exit static pressure vs ambient, choked check | Wet throat chokes at ≥0.6 kg/s (flag: volume-ratio 1800/1000 = 1.8 vs area ratio 1.49 — see §9 open item) | 1 d |

### Phase 2 — Fuel spray (no combustion)

| Step | Test | Measurements | PASS/FAIL | Duration |
|------|------|--------------|-----------|----------|
| 2.1 | Water spray, ambient | Cone angle, patternation | 30–60° cone, no dripping, uniform 6-port coverage | 1 d |
| 2.2 | Jet A1 spray at 4–6 bar | SMD (Malvern/patternator), flow/port | SMD < 50 µm; total flow 24–27 g/s at 4 bar (matches §2) | 1 d |
| 2.3 | Distribution across V-gutter | Circumferential coverage (paper target / quartz) | Uniform ±15 %, no wall wetting upstream of flame holder | 1 d |
| 2.4 | Low-pressure spray (0.7 bar, altitude-sim) | Atomization at 70 kPa | SMD < 60 µm; lightable | 1 d |
| 2.5 | Check-valve close-off | Residual dribble after pump off | < 0.1 g residual per port (coking control, 15 Part 6) | 1 d |

### Phase 3 — Ignition (no main-engine flow)

| Step | Test | Measurements | PASS/FAIL | Duration |
|------|------|--------------|-----------|----------|
| 3.1 | CDI/spark in still air | Spark at 0.5 mm gap, 7.4 V | Fires every trigger, blue-white | 1 d |
| 3.2 | Ignition at 70 kPa (altitude-sim chamber) | Time-to-light | < 2 s at 0.7 bar (17 §3a 3.2) | 1 d |
| 3.3 | Cross-fire igniter → V-gutter | Flame propagation | < 0.5 s full annulus light | 1 d |
| 3.4 | Ignition with airflow 0.1–0.6 kg/s | Blowout margin | Lights at ≥0.6 kg/s; stays lit (see 15 Appendix D flameout logic) | 1 d |
| 3.5 | **Ignition at 0.7–1.0 kg/s (M1-equivalent flow)** | Max ignition flow, relight in <1 s | Ignition reliable at ≥1.0 kg/s air (corrected to 1.10 target) | 1 d |

### Phase 4 — Integration with P550-PRO (engine test stand)

| Step | Test | Measurements | PASS/FAIL | Duration |
|------|------|--------------|-----------|----------|
| 4.1 | Dry run 100 % throttle, AB fitted, iris dry | EGT (T5), RPM, back-pressure, thrust | T5 ≤ 750 °C (datasheet 13:17); back-pressure < 5 % rise; F_dry static ≈ 550 N (datasheet) | 1 d |
| 4.2 | Iris cycle dry↔wet at 60–100 % throttle | Throat position, thrust response | No thrust upset in dry position; smooth wet transition; no surge | 1 d |
| 4.3 | Wet burst 3 s @ 75 % | T5, T7, thrust, shell T | Lights < 2 s; T7 1500–1700 K; T5 stays within limit | 1 d |
| 4.4 | Wet burst 5 s @ 100 % | **Thrust @ 100 Hz, T5, T7, PT7, shell T, fuel flow** | T7 = 1800 K ±50 K at 24–27 g/s; shell < 200 °C | 1 d |
| 4.5 | Wet burst 10 s @ 100 % | As 4.4 + thermal soak-back | T7 stable 1800 K ±50 K; shell < 200 °C; cooldown 5 min between runs | 1 d |
| 4.6 | Wet burst 20 s (max duration) | As 4.5 + post-run inspection | T7 held; shell < 200 °C; liner/iris no visible damage | 2 d |
| 4.7 | Repeat 4.4–4.6 × 3 cycles | Repeatability; liner condition per cycle | Within ±2 % thrust run-to-run; boroscope clean; spark gap < 0.030″ | 2 d |
| 4.8 | (Optional) Altitude-sim inlet: blower to Pt = 131.9 kPa, Tt = 322 K | Direct M1 measurement | Net ≥ 450 N with ram subtracted; proves conversion without mass-flow factor | 3 d |

### Phase 5 — Qualification (G0 gate, 18 §6)

| Step | Test | Measurements | PASS/FAIL | Duration |
|------|------|--------------|-----------|----------|
| 5.1 | **Gate run 1 — 20 s wet @ 1800 K** | **F_s @ 500 Hz, T7, T5, shell T, fuel** | **F_s ≥ 700 N (§6), T7 1800 ±50 K, shell < 200 °C** | 1 d |
| 5.2 | Cooldown 5 min; boroscope + shell check | Post-run inspection | No cracks, hole blockage, warp; shell label TL-200 un-tripped | — |
| 5.3 | **Gate run 2 — 20 s wet @ 1800 K** | As 5.1 | Same pass criteria | 1 d |
| 5.4 | **Gate run 3 — 20 s wet @ 1800 K** | As 5.1 | Same pass criteria | 1 d |
| 5.5 | 3-run summary | Mean F_s, mean T7, fuel per run | Report to 18 §8 (E2 test report) | — |

---

## 5. Instrumentation & DAQ List

Expanded from 17 §3b. **During AB bursts, thrust, EGT (T5), T7, PT7 and AB fuel flow must log at ≥100 Hz (500 Hz for Phase 5).** All other channels ≥10 Hz.

| # | Sensor | Qty | Range | Accuracy | Location | Log |
|---|--------|-----|-------|----------|----------|-----|
| T-1 | S-type load cell (thrust) | 1 | 0–1000 N (0–100 kg) | ±0.1 % FS (±1 N) | engine mount, axial | ≥100 Hz |
| T-2 | K-type TC, Inconel sheath (T5, engine EGT) | 1 | 0–1300 °C | ±0.4 % | engine exhaust, upstream of AB | ≥100 Hz |
| T-3 | R-type TC (T7, AB exit) | 2 | 0–1700 °C | ±0.25 % | AB exit plane, 2 radii | ≥100 Hz |
| T-4 | IR pyrometer 2-colour | 2 | 500–2000 °C | ±1 % | liner wall x=50, 150 mm | 10 Hz |
| T-5 | K-type TC (outer shell) | 3 | 0–500 °C | ±1 % | shell surface, 120/180/240 mm | 10 Hz |
| P-1 | Pressure transducer | 4 | 0–5 bar abs | ±0.5 % | spray ring, flame holder, liner mid, exit | 100 Hz |
| P-2 | Differential pressure | 2 | 0–100 mbar | ±1 % | annulus inlet→exit, film plenum | 10 Hz |
| P-3 | **PT7 — AB inlet total pressure** | 1 | 0–5 bar abs | ±0.5 % | AB inlet plane (before spray ring) | ≥100 Hz |
| F-1 | Turbine flow meter | 1 | 0.5–6 L/h | ±0.5 % | AB fuel line | ≥100 Hz |
| F-2 | Load cell (fuel tank, gravimetric) | 1 | 0–2 kg | ±0.5 % | fuel tank hanger | 10 Hz |
| S-1 | Servo position (iris) | 1 | 0–100 % | ±1 % | iris sync ring | 10 Hz |
| C-1 | High-speed camera (optional) | 1 | 1000 fps | — | quartz window, liner mid | sync |

**DAQ:** 24-bit thermocouple DAQ (NI 9214 class), 8-ch pressure analog, CAN/ECU datalink for RPM and engine fuel flow. Single time base; trigger on AB fuel-valve command. Post-process: 0.5 s rolling mean for steady-state values, raw for transients.

---

## 6. Thrust Measurement Method & the 450 N "at M1" Gate

**Method: static thrust stand, ram-drag-free, with explicit mass-flow correction.** The stand measures **static wet thrust F_s** (V∞ = 0 → no ram drag, gross = net on the stand). The M1 in-flight net is derived from F_s with the corrected-flow ratio:

```
net_M1 = F_s × (ṁ_M1 / ṁ_static) − ṁ_M1 × V∞
```

- ṁ_M1 = **1.10 kg/s** (18 §2.1)
- ṁ_static = **0.95 kg/s** (P550 datasheet 0.93 kg/s core, 13:15/67, + 0.023 kg/s AB fuel at T7 = 1800 K)
- V∞ = 328 m/s

The physical basis: gross thrust = ṁ × Vj(T7), and Vj depends on T7 and nozzle area only (not on ṁ), so for a fixed T7 the M1 gross = F_s × (ṁ_M1/ṁ_static).

**Pass gate (derived):** require

```
F_s ≥ (450 + ṁ_M1·V∞) × (ṁ_static/ṁ_M1) = (450 + 361) × 0.864 = 700 N
```

**Static gate F_s ≥ 700 N** at T7 = 1800 K ⇔ **net_M1 ≥ 450 N.** Design point: F_s = 0.95 × 759 = **721 N** → net_M1 = 475 N (consistent with §1).

Notes:
- A naive "F_s ≥ 450 + ram = 811 N" is **conservative** (it ignores the mass-flow ratio 1.16) and may be used as a stretch target, but the physically correct gate is **700 N**.
- The gate input ṁ_static is measured on the stand (fuel-tank gravimetric + engine fuel flow); if the measured ṁ_static differs from 0.95, **re-derive the F_s gate from the formula** (do not move the 450 N).
- **Alternative (Phase 4.8):** altitude-simulated inlet (blower producing Pt = 131.9 kPa, Tt = 322 K) measures net directly with ram subtracted. Preferred for final confirmation if the blower is available.

**Tare procedure:** zero load cell cold; run engine to idle 30 s, re-zero (account for line forces, pipe weight, thrust-stand friction); take data in 0.5 s windows; correct for engine fuel momentum on the stand (< 2 N, neglected in this model per 18 §2.1).

---

## 7. Safety & Operational Limits (corrected from 17 §3c–3d)

| Parameter | Limit | Rationale |
|-----------|-------|-----------|
| Max AB duration | **20 s** continuous | liner thermal limit; 18 §2.3 / INTERFACES §2 |
| Cool-down between AB runs | **5 min** | soak-back; shell must drop < 200 °C (18 §5.5, 17 §3c) |
| Engine EGT T5 | **≤ 750 °C (1023 K)** | P550 datasheet (13:17); at M1 full dry it is ~727 °C |
| AB exit T7 | **≤ 1900 K** (target 1800 ±50 K) | liner/material margin; 1700 K already passes §1 gate |
| Outer shell temperature | **< 200 °C** | composite/fuselage contact limit (17 §1e) |
| Min AB fuel pressure | 4 bar | atomization SMD < 50 µm (§2, 15 Part 3) |
| Purge after AB | 3 s dry air (CO₂ option 15 Part 6) | anti-coking; verify check valves close-off (§2.5) |
| Fuel pump duty | ≤ 4 bar / 34 g/s continuous | Speck ZY-4S-12V curve (15:90-91) |
| Abort | fuel valve closes + iris opens (wet) + throttle idle in <0.5 s | 18 §5.3; independent of AB state machine |

Cooling-air interlock: AB fuel valve cannot open unless annulus/film cooling flow confirmed (17 §3c-3d; pressure switch on cooling duct). Flameout: if T7 drops >100 K in <1 s with pump running → cut fuel, purge, 30 s no-relight (15 Appendix D).

---

## 8. GATE Statement (G0, feeds 18 §6)

> **PASS** = **3 successful 10–20 s wet runs** (recommended 20 s each) at T7 = 1800 K, full throttle, with:
> 1. **Static wet thrust F_s ≥ 700 N** (⇔ net wet thrust ≥ 450 N M1-equivalent, §6), AND
> 2. **Outer shell temperature < 200 °C** throughout and after soak-back, AND
> 3. **T5 ≤ 750 °C**, T7 = 1800 ±50 K, no flameout, no damage per post-run inspection (boroscope, spark gap, iris freedom).

Any run that trips an abort, exceeds T5/T7/shell limits, or shows liner damage resets the counter. **If the AB delivers only ~400 N M1-equivalent, the program cannot sustain M1.05 and must stop** (18 §2.3).

---

## 9. Open Items Requiring Empirical Re-Derivation (not hand-waved)

1. **Film-hole count 105–115** — 2.5 %-of-core scaling (111) vs Re^0.8 scaling (102). Final = Phase 1.3 distribution result.
2. **Iris wet throat 55 mm (area ratio 1.49)** — corrected volume ratio T7/T5 = 1800/1000 = **1.8**; nozzle-matching must be re-derived (Phase 1.5 / 4.2). **Interface I-03 dimensions unchanged**; this is a nozzle-matching flag, not an interface change.
3. **T5 = 1000 K assumption** (18 §2.1, vs 973 K in 17 §1a) — verify measured T5 at full dry throttle on the stand (Phase 4.1); if it differs, re-derive AB fuel flow (§2 formula, ~2 % sensitivity).
4. **ṁ_static = 0.95 kg/s** — measure on the stand and re-derive the F_s gate (§6 formula); do not move the 450 N.
5. **Wall stress margin** — corrected q_total (597 kW/m²) raises ΔT_wall to ~24 K → σ_th ~71 MPa → combined ~79 MPa vs 90 MPa yield → margin **1.14×** (vs 17's 1.45×). Corrugated liner + YSZ TBC (17 §1d options 1+3) are **required**, not optional. Structural re-verification is E2/E5 follow-up.
6. **Weight/CG** — restoring the dedicated Speck pump (§10, 17 §2d) raises the 17-revised AB system mass to ~0.97 kg vs **0.83 kg used in 18 §3.4** → P0 cross-team CG reconciliation (I-03 mass + station). Not edited in 18 per scope.
7. **Scoop Ø 13.3 mm** — sized for 3 % bleed at ṁ = 1.10; scoop drag + flow recovery (Cp 0.8) to be confirmed in Phase 1.1 (cold flow) and G3 flight tests.

---

## Appendix: Committed Analysis Script

Every number above is produced by `tools/ab_bench_analysis.py` (committed 2026-08-06), which recomputes §1 thrust, §2 fuel/O₂, §3 thermal scaling, and §6 gate conversion from the authority inputs (18 §2.1, 13:15/65/120/123, 15:90-91, 17 §1a-1e). Run:

```
/tmp/opencode/cq312/bin/python tools/ab_bench_analysis.py
```

---

## Cross-References

- Corrected model basis: 18 §2.1–2.3 (ṁ 1.10, net 450–475 N, gate G0)
- Fuel & ignition hardware: 15 (Speck ZY-4S-12V, EV14, CDI, purge)
- Thermal design & safety: 17 §1, §3 (corrected per §2–3 above and banner in 17)
- Mechanical design & CAD: 14 (corrected per banner in 14)
- Interface: INTERFACES.md I-03 (unchanged)
