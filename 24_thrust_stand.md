# Thrust Stand Design (AB Bench Qualification Rig)

**Doc:** 24 — Thrust stand build package for the afterburner bench program
**Author:** E2 (Propulsion/Afterburner) with E3 (M&V)
**Date:** 2026-08-07
**Status:** 🔴 CONCEPT ONLY — structural/DAQ/software release open (2026-09-16)
**Engine:** JetCat P550-PRO + afterburner (single engine)
**Development target:** 21 §6 conditional model: static wet **F_s ≥700 N**.
This does **not** demonstrate ≥450 N flight thrust; see 25 R07 and 26 §4.

> **September review overrides the detailed concept claims below:** ADS1256
> provides four differential pairs/eight single-ended inputs, not eight pairs;
> the proposed direct-wired sensors exceed its input pins. MAX31856's 60 Hz
> rejection is not its conversion rate. Section 3 uses unqualified extrusion,
> bolt and stiffness assumptions. Section 6 now links implemented **offline**
> programs; physical acquisition/control drivers remain absent. Do not build these tables as a
> released package. Required corrections/evidence: 25 R11–R13, 26 §4 and 27.

> **Scope.** This is the historical proposed rig for 21 §4 Phases 0–5, not a
> qualified physical assembly. Tables retain concept dimensions and costs for
> redesign review. The current `tools/thrust_stand_check.py` screens the known
> deficiencies; it no longer reports the former strength/rate PASS claims.

---

## 1. Stand Requirements (from 21)

| Requirement | Spec | Source |
|---|---|---|
| Gate thrust F_s | ≥ 700 N static wet @ 1800 K (design 721 N) | 21 §6 |
| Thrust log rate | ≥ 100 Hz bursts; **500 Hz Phase 5 gate** | 21 §4, §5 |
| Sensor set | T-1…S-1 (load cell, 6 TCs, 5 bar abs ×4 + PT7, ±100 mbar ×2, turbine flow, 2 kg gravimetric, iris pos) | 21 §5 |
| DAQ | 24-bit; 8-ch pressure analog; CAN/ECU datalink; trigger on AB fuel-valve command; 0.5 s rolling post-mean | 21 §5 |
| Cooling-air interlock | AB fuel valve cannot open unless cooling flow confirmed | 21 §7 |
| Environment | Outdoor pad or ventilated cell; exhaust cleared downrange; extinguisher + blast deflector | 21 §7, §11 below |

Design loads used in the structural checks (17 §2a vibration case): **5g dynamic** on engine+AB (5.87 kg) plus 2.0 kg carriage = **7.9 kg ⇒ 386 N**, 193 N per rail.

---

## 2. Mechanical Architecture

```
         ┌──────────────────────────────────────────────────────┐
         │  40x40 Al T-slot base frame, ~600 mm span (2 rails)  │
         │                                                      │
         │  ┌──────────────┐  thrust axis (X)  ┌────────────┐   │
         │  │  FIXED mount │◄── S-type cell ──►│  ROD-END   │   │
         │  │  (bracket)   │   100 kg / 981 N  │  M6 clevis │   │
         │  └──────────────┘                   └─────┬──────┘   │
         │                                          │          │
         │  ┌────────────────────────────────────────▼───────┐ │
         │  │  CARRIAGE plate (6061, ~2 kg)  on 2x SBR12     │ │
         │  │  linear rails, 4 pillow blocks                 │ │
         │  │   ┌───────────────────────────────────────┐    │ │
         │  │   │  ENGINE MOUNT RING ADAPTER (7075)     │    │ │
         │  │   │  4x M3 A2-70 on 45 mm PCD (I-03)      │    │ │
         │  │   │  ┌───────────────────────────────┐    │    │ │
         │  │   │  │  JetCat P550-PRO (4.9 kg)     │    │    │ │
         │  │   │  │  + Afterburner (0.97 kg)      │    │    │ │
         │  │   │  └───────────────────────────────┘    │    │ │
         │  │   └───────────────────────────────────────┘    │ │
         │  └────────────────────────────────────────────────┘ │
         │  (flow exhausts downrange, clear of frame)          │
         └──────────────────────────────────────────────────────┘
```

**Load path.** Engine thrust (axial, +X) → engine mount ring adapter (4× M3 on 45 mm PCD, the SAME interface as the aircraft, I-03) → carriage plate → S-type load cell via M6 rod-end/clevis → fixed bracket bolted to the base frame. The two SBR12 linear rails carry **only** the vertical/lateral loads (weight + vibration) and let the axial thrust run straight into the load cell with negligible friction. **The load cell must see the full axial force — nothing else shunts it.**

**Mounting choice.** The engine bolts to the stand through the identical 45 mm PCD ring it uses in the airframe (17 §2a, I-03). This preserves the exact engine-mount load path and lets a Phase 4.1 dry run be representative of the aircraft installation. A 7075-T6 adapter plate reproduces the ring geometry; no modification of the engine itself.

**Rail sizing.** 2× SBR12 (12 mm) with 4 pillow blocks — static rating far above the 193 N/rail dynamic load; used because it is the standard low-cost linear-rail platform for jet test stands of this class.

---

## 3. Historical Structural Estimates (Qualification Claims Withdrawn)

The ratios below are retained from the original concept, **not current PASS
results**. They require the supplier/combined-load/anchor work in 25 R13.

| Check | Load | Capacity | Margin | Status |
|---|---|---|---|---|
| Load cell (T-1, 100 kg = 981 N) | target 700 N | 981 N | 1.40× | range only |
| Load cell vs design point | 721 N | 981 N | 1.36× | range only |
| Rails (2× SBR12, 5g) | 193 N/rail | ≫ 50 kg/block | ≫ 2.5× | UNVERIFIED |
| Base frame mid deflection (400 N, 600 mm) | 400 N | 0.121 mm (solid-square estimate) | — | invalid for extrusion |
| Engine mount bolts (4× M3 A2-70 shear) | 175 N/bolt | 2113 N | 12.1× | UNVERIFIED |
| Engine mount bolts (bending, 0.35 m arm) | 224 N tension | 2113 N | 9.4× | combined-load model missing |
| M6 rod-end (clevis, 1.25× target) | 875 N | ≥ 1500 N rating | ≥ 1.7× | actual part/rating pending |
| Structural resonance f_n (cell in line) | — | 179 Hz est. | above 100 Hz | confirm Phase 0.2 |

**Resonance correction.** The ~179 Hz value assumes cell stiffness; it is not a
measured mode. It can alias at 100 Hz sampling; at 500 Hz the Nyquist limit is
250 Hz and higher-frequency excitation still needs analog anti-alias filtering.
Measure fixture/engine modes and acquisition bandwidth (26 §4).

---

## 4. Instrumentation & Channel Map (exact mapping to 21 §5)

| 21 §5 ID | Sensor | Qty | Range | Output / interface | DAQ path | Log rate |
|---|---|---|---|---|---|---|
| T-1 | S-type load cell, 100 kg (Phidgets 3138_0) | 1 | 0–981 N | 2 mV/V bridge | ADS1256 ch0 (diff) | **500 Hz** |
| T-2 | K-type TC, Inconel sheath (T5 engine EGT) | 1 | 0–1300 °C | TC → MAX31856 | MAX31856 #0 | 60 Hz |
| T-3 | R-type TC (T7 AB exit) | 2 | 0–1700 °C | TC → MAX31856 | MAX31856 #1–2 | 60 Hz |
| T-4 | IR 2-colour pyrometer (liner wall) | 2 | 500–2000 °C | 4–20 mA / 0-5 V | ADS1256 (aux) | 10 Hz |
| T-5 | K-type TC (outer shell) | 3 | 0–500 °C | TC → MAX31856 | MAX31856 #3–5 | 60 Hz |
| P-1 | 0–5 bar abs transducer | 4 | 0–5 bar | **0–5 V analog** | ADS1256 ch1–4 | 100 Hz |
| P-2 | ±100 mbar differential | 2 | ±100 mbar | I²C (HSCDRRN…) | Pi I²C bus | 10 Hz |
| P-3 | PT7 AB inlet total pressure | 1 | 0–5 bar | **0–5 V analog** | ADS1256 ch5 | **500 Hz** |
| F-1 | Turbine flow meter (AB fuel) | 1 | 0.5–5 L/min | 0–5 V analog | ADS1256 ch6 | 100 Hz |
| F-2 | 2 kg load cell (gravimetric, tank) | 1 | 0–2 kg | 2 mV/V bridge | ADS1256 ch7 | 10 Hz |
| S-1 | Iris servo position | 1 | 0–100 % | PWM feedback | Pi GPIO capture | 10 Hz |
| — | ECU datalink (RPM, EGT, fuel flow) | 1 | — | serial (Xicou/JetCat) | Pi UART | 10 Hz |
| — | Trigger — AB fuel-valve command | 1 | logic | GPIO edge | Pi timestamp | — |

**Requested logical-channel budget (NOT a valid ADS1256 pin map):**

| Channel | 21 §5 | Rate |
|---|---|---|
| ch0 | T-1 thrust | 500 Hz |
| ch1–4 | P-1 ×4 | 100 Hz |
| ch5 | P-3 PT7 | 500 Hz |
| ch6 | F-1 flow | 100 Hz |
| ch7 | F-2 gravimetric | 10 Hz |

The requested aggregate is **1510 samples/s**, but this arithmetic does not
prove acquisition performance. ADS1256 provides four differential pairs or
eight single-ended inputs; two raw bridges plus six single-ended signals need
ten pins. Revise hardware/pin allocation, gains and conditioning, then demonstrate
settled conversion throughput and source timing. `monotonic_ns()` on register
reads is an arrival timestamp, not proof of new, aligned sensor conversions.

---

## 5. Electronics & DAQ Hardware

**Topology: Raspberry Pi 4 (DAQ host) + 1× ADS1256 24-bit ADC + 6× MAX31856 TC front-ends + I²C diff pressure + serial ECU link.** All parts verified available with prices in the BOM (§9). This is a bench rig — no flight-weight/size constraints, so a Pi + breakouts is the correct, cheap, serviceable choice versus a NI cDAQ (costs 20× for the same 24-bit result).

| Block | Part | Role |
|---|---|---|
| Host | Raspberry Pi 4 (4 GB) + 32 GB SD + 5 V PSU | DAQ, logging, UI, control signals |
| Fast ADC | Waveshare High-Precision AD/DA Board (ADS1256, 24-bit, 8ch) | thrust, pressures, flow, gravimetric at up to 500 Hz |
| TC front-ends | Adafruit MAX31856 ×6 (K + R types) | all 6 thermocouples, hardware CJC |
| Diff pressure | Honeywell HSCDRRN100MD4A3 ×2 | P-2 annulus / plenum |
| ECU link | Pi UART → JetCat ECU telemetry | RPM, EGT, fuel flow, battery V |
| Fuel flow | Omega FLR1012 (0.5–5 L/min, 0–5 V) | F-1 |
| Gravimetric | Phidgets FRC4160_0 (2 kg S-type) | F-2 fuel-tank hanger |
| Pressure | 0–5 bar abs 0–5 V analog (Omega PX309-100A5V class) ×5 | P-1 ×4 + PT7 |

**Pressure transducer choice.** 21 §5 P-1/PT7 = 0–5 bar abs, ±0.5 %, ≥ 100 Hz. A **0–5 V analog** transducer (Omega PX309-100A5V class, 0–100 psi abs, ±0.25 % BFSL) drops straight onto ADS1256 diff inputs — no I²C address juggling, no SPI fan-out, full 500 Hz on PT7. 100 psi abs ≈ 6.9 bar covers the 5 bar spec with headroom. The costlier low-flow/industrial "5 bar" digital units give no accuracy or rate benefit here.

**Thermocouple rate correction.** 60 Hz rejection is mains filtering, not a
16.6 ms conversion period. The historical 60 Hz entries in the channel table
are withdrawn; actual rate depends on the conversion/averaging mode and must
be measured at DRDY. Probe thermal response and electronic acquisition rate
are separate requirements. No replacement DAQ or rate deviation is qualified
by this document (26 §4).

**Trigger & interlock.** The AB fuel-valve solenoid drive line from the AB control board (16) is tapped: one copy feeds the solenoid, one edge-sensitive GPIO on the Pi starts/stops the gate-window logging and timestamps the command. The 21 §7 cooling-air interlock lives in the AB control board state machine (16 §7) — the stand DAQ records it, does not implement it.

---

## 6. Software (DAQ + Post-Processing)

The **offline** pipeline is implemented in [34](34_bench_software.md), which
defines the current schema, CLI, acceptance semantics and limitations:

| Program | Implemented behavior |
|---|---|
| `tools/daq_bench.py` | Preserve CSV/stdin acquisition events, per-channel sequence/time validation, no-clobber archive and metadata-inclusive hashes |
| `tools/cal_bench.py` | Paired ascending/descending cycles; force-domain residual/hysteresis/repeatability and explicit criteria |
| `tools/post_bench.py` | Selected thrust/temperature interval screen with positive uncertainty bounds, complete endpoints, source rates and raw thermal maxima |
| `tools/log_pair_check.py` | Same run/test/config, distinct declared acquisition paths, calibrated clock evidence and separate log hashes |

These tools do not contain physical drivers or ignition/actuator control. They
do not implement the former fictitious eight-differential-channel ADC loop or
60 Hz thermocouple conversions. Source-driver timing/pin allocation still needs
the hardware work in 33. There is **no static-to-flight thrust conversion**.
Simulated inputs cannot establish a physical result; a selected-channel screen
does not constitute the full G0 test suite. Fault-injection and installed
calibration/abort evidence remain required before hot testing.

---

## 7. Calibration & Tare Procedure (21 §4 Phase 0.1 + 21 §7)

1. **Zero:** load cell unloaded, record 60 s zero; tolerance ±2 N.
2. **Dead-weight curve:** 0 → 900 N in ~5 steps and back (hysteresis); linearity ±1 N over 0–800 N required.
3. **Creep:** hold 500 N for 1 h; drift < ±2 N.
4. **Engine-off tare:** zero with the engine stopped and production hoses/cables installed. Do not subtract actual idle thrust. Characterise line forces, friction and thermal drift through installed calibration (26 §4).
5. **Gate window:** data taken in 0.5 s windows after settle; engine fuel momentum on the stand < 2 N, neglected (21 §6).
6. **Rebalance:** if measured ṁ_static ≠ 0.95 kg/s, re-derive the F_s gate from the 21 §6 formula (never move the 450 N).

---

## 8. Safety & Operations

- **Blast deflector** downrange of the exhaust plane (steel plate or ceramic pad) sized for the 700 N/1800 K jet; clear the stand floor.
- **Fire suppression:** 2× CO₂ or ABC extinguishers, operator side, within 3 m; fuel storage away from the pad (21 §7).
- **Fuel:** dedicated Speck ZY-4S-12V pump (15) at 4 bar / ~24–27 g/s; manual shut-off valve at the tank; check-valve close-off verified (21 §4 Phase 2.5).
- **Personnel exclusion:** no one within the exhaust cone or 45° of it during a hot run.
- **Interlocks (16 §7, retained):** AB fuel valve blocked unless RPM ≥ 50 %, throttle ≥ 80 %, cooling flow confirmed, T5 < 650 °C, self-test OK. Abort = fuel valve closes + iris opens + throttle idle in < 0.5 s (21 §7).
- **Cool-down:** ≥ 5 min between AB runs; shell < 200 °C verified before re-light (21 §7).
- **First hot run** after a full dry-run day + DAQ channel verification + tap test.

---

## 9. Bill of Materials (verified links, prices as checked 2026-08-07)

> All links verified live on the date above. Items marked **[FAB]** are fabricated in-house. Exchange rates: £1 ≈ $1.30 applied at check time. Totals are list prices; shipping/tax extra.

### 9.1 Mechanical structure — $335

| # | Item | Spec | Qty | Unit | Total | Link (verified 2026-08-07) |
|---|---|---|---|---|---|---|
| S1 | Linear rail kit | 2× SBR12 rails + 4× SBR12UU blocks, 600 mm | 1 | $64.00 | $64.00 | MyCNCShop — https://www.mycncshop.com/sbr12-600mm-with-sbr12UU-block |
| S2 | Al T-slot profile | 80/20 40-4040, 40×40 mm, four open T-slots | 2×305 mm | $12.35 | $24.70 | 80/20 — https://8020.net/40-4040.html ($0.0405/mm) |
| S3 | Inside corner brackets | 80/20 40-4302, 40-series 2-hole | 4 | $8.05 | $32.20 | 80/20 — https://8020.net/40-4302-black.html |
| S4 | Carriage plate | 6061 aluminum sheet, 1/4 in (~6 mm) | 1 | $25 | $25 | McMaster-Carr — https://www.mcmaster.com/products/aluminum-sheets/material~aluminum-2/material~6061-aluminum/ |
| S5 | Engine mount ring adapter | 7075-T6, Ø45 mm PCD ring, 4× M3 | 1 | $50 | $50 | **[FAB]** (local CNC) |
| S6 | Fixed mount bracket | 6061, for load-cell back end | 1 | $15 | $15 | **[FAB]** |
| S7 | M6 rod-end/clevis | load-cell axial path | 2 | $9 | $18 | McMaster-Carr — https://www.mcmaster.com/products/rod-ends/shank-thread-size~m6/ |
| S8 | Fasteners + washers | M3/M5/M6, nylon + SS | 1 lot | $15 | $15 | McMaster-Carr — https://www.mcmaster.com/products/hex-head-screws/ (search) |
| S9 | Steel blast deflector plate | low-carbon steel sheet, 1/8 in (~3 mm), 12×12 in | 1 | $25 | $25 | McMaster-Carr — https://www.mcmaster.com/products/low-carbon-steel-sheets/ |
| S10 | Fire extinguishers | 2× CO₂/ABC | 2 | $33 | $66 | McMaster-Carr — https://www.mcmaster.com/products/fire-extinguishers/ (2 × ~$33) |

### 9.2 DAQ + electronics — $464

| # | Item | Spec | Qty | Unit | Total | Link (verified 2026-08-07) |
|---|---|---|---|---|---|---|
| D1 | Raspberry Pi 4 | 4 GB, with PSU + 32 GB SD | 1 | $75 | $75 | Raspberry Pi — https://www.raspberrypi.com/products/raspberry-pi-4-model-b/ |
| D2 | ADS1256 24-bit ADC board | Waveshare High-Precision AD/DA (8ch diff, 30 kSPS, DAC8552) | 1 | $34.99 | $34.99 | Waveshare — https://www.waveshare.com/high-precision-ad-da-board.htm |
| D3 | MAX31856 TC board | Adafruit, K/R/S/T etc., 24-bit, CJC | 6 | $17.50 | $105.00 | Adafruit — https://www.adafruit.com/product/3263 |
| D4 | Diff pressure sensor | Honeywell HSCDRRN100MD4A3, ±100 mbar, I²C, 0.25 % | 2 | $111.95 | $223.90 | Neutron USA — https://www.neutronusa.com/prod.cfm/3015545/rfcs |
| D5 | Wiring + breadboard + breakout | 1 lot | 1 | $25 | $25 | Adafruit — https://www.adafruit.com/category/57 |

### 9.3 Sensors (T/P/F per 21 §5) — $3,486

| # | Item | Spec | Qty | Unit | Total | Link (verified 2026-08-07) |
|---|---|---|---|---|---|---|
| X1 | **Thrust load cell** | Phidgets 3138_0 S-type, 100 kg C2, M6, ±0.1 % FS | 1 | $45 | $45 | Phidgets — https://www.phidgets.com/?prodid=229 |
| X2 | **T7 R-type TC** | EvoSensors R1X-WBWT-30G-EX-CB12-6-STWL, PtRh13/Pt, 0–1700 °C, 6 in leads | 2 | $300 | $600 | EvoSensors — https://evosensors.com/products/type-r-thermocouple-probe-platinum-rhodium-13-exposed-junction-6-to-24-inches-long-flexible-30-gage-solid-wire-with-alumina-ceramic-insulators-and-stripped-leads (£239 ≈ $300) |
| X3 | **T5 K-type TC (engine EGT)** | EvoSensors K1X-IN60-062-EX-18-MPCX, 1/16 in Inconel sheath, exposed junction | 1 | $50 | $50 | EvoSensors — https://evosensors.com/products/type-k-thermocouple-probe-1-16-diameter-18-inch-long-inconel-sheath-with-an-exposed-junction-and-miniature-connector (0–900 °C sheath; 1300 °C spec = bare-wire only, see §10.4) |
| X4 | T5 shell K-type (3×) | Adafruit #270 K-type glass-braid bead probe, 0–500 °C | 3 | $9.95 | $29.85 | Adafruit — https://www.adafruit.com/product/270 |
| X5 | P-1 / PT7 pressure | Omega PX309-100A5V, 0–100 psi abs (≈6.9 bar), 0–5 V, ±0.25 % BFSL | 5 | $435.42 | $2 177.10 | DwyerOmega — https://www.dwyeromega.com/en-us/general-purpose-stainless-steel-pressure-transducers/PX309/p/PX309-100A5V |
| X6 | F-1 AB fuel flow | Omega FLR1012, 0.5–5 L/min, 0–5 V, ±1 % FS | 1 | $543.85 | $543.85 | Omega — https://in.omega.com/pptst/FLR1000.html |
| X7 | F-2 gravimetric load cell | Phidgets FRC4160_0 S-type, 2 kg C2 | 1 | $40 | $40 | Phidgets — https://www.phidgets.com/?prodid=1304 |

> **Gravimetric F-2 note.** The 21 §5 spec (0–2 kg, ±0.5 %) is met by the Phidgets 2 kg C2 cell hanging the AB fuel tank on the stand (drop-tube feed to the Speck pump). Weight-loss-per-run reconciles against the turbine meter integral (21 §6 ṁ_static).

### 9.4 Cost-reduced alternatives (equivalent function)

| Item | Part | Price | Why alternative |
|---|---|---|---|
| P-1/PT7 pressure | TE MS4525DO, 0–100 psi abs, 0.25 % | ~$100 ea | digital I²C/SPI; needs 5× on one bus and a breakout — more wiring for ~$1 700 saving; use only if budget-constrained |
| 100 kg cell | Makerfabs S-type, 100 kg | $23.60 | unverified thread spec; buy Phidgets for the gate channel |

### 9.5 Cost summary

| Group | Total |
|---|---|
| Mechanical structure | $335 |
| DAQ + electronics | $464 |
| Sensors (T/P/F) | $3 486 |
| **Stand total** | **$4 285** |
| Cost-reduced P-1/PT7 option | −$1 700 ⇒ ~$2 585 |

**Critical-path / single-source items (★):** X1 thrust load cell (Phidgets 3138_0), X2 R-type TCs (EvoSensors), X5 PT7 transducer (Omega PX309-100A5V), X6 turbine flow (FLR1012), S5 engine mount ring adapter [FAB]. **Order X1, X2, X6 first** — the R-type TCs and the turbine meter have weeks-long lead times.

---

## 10. Deviations & Open Items (flagged, not silent)

1. **TC log rate:** the former 60 Hz claim and proposed alternative's compliance
   were not substantiated. Establish actual conversion/averaging latency,
   aggregate rate and probe response separately (26 §4); then resolve the
   requirements with E2/E3 using measured evidence.
2. **F-1 range unit (21 §5 "0.5–6 L/h").** Static AB fuel = 23.6 g/s ⇒ **≈ 1.8 L/min**; the spec unit is wrong. Corrected to 0.5–5 L/min in this design (FLR1012, X6). Flagged for 21 §5 correction; the 0.5–6 L/h number as written is not met by any turbine meter and is not physically meaningful.
3. **100 psi abs vs "0–5 bar" (21 §5 P-1/PT7).** 100 psi = 6.9 bar covers the 5 bar spec with margin; a dedicated 0–5 bar abs 0–5 V part is scarce. Re-verify P-1 taps (spray ring, flame holder, liner mid, exit) really see ≤ 5 bar abs in Phase 1.1 cold flow before committing all five.
4. **T-2 probe rating vs 1300 °C spec (21 §5).** A sheathed K-type is limited to ~900–1070 °C by the Inconel sheath; the 1300 °C spec applies to bare K-type wire only. T5 measured regime (datasheet limit ≤ 750 °C, 21 §7) is well inside the sheathed rating, so the exposed-junction Inconel probe (X3) is correct for the actual engine EGT. Flagged for 21 §5 wording.
5. **F_s margin 1.36–1.40×.** A 100 kg cell is the largest cheap S-type; if Phase 5.1 approaches 980 N (over-load), the cell must be swapped before the gate — budget a spare or verify the design point stays ≤ 720 N.
6. **Stand mode test (Phase 0.2).** 179 Hz axial mode est.; must be confirmed and separated from engine spool frequencies before any hot run (§3).
7. **P-1 500 Hz vs 100 Hz.** PT7 is logged at 500 Hz (extra margin); P-1 ×4 at 100 Hz per spec. No change needed.

---

## 11. Build Sequence (ties to 21 §4 Phase 0)

| Step | Work | Verifies |
|---|---|---|
| 1 | Fabricate S5 mount ring + S6 bracket; assemble S1–S4 frame | geometry, rail alignment |
| 2 | Wire DAQ: D1–D5, X1, X4, X6, X7, P-2 | channel count, power |
| 3 | Load-cell dead-weight calibration (cal_bench.py) | 21 Phase 0.1 (linearity, hysteresis, creep) |
| 4 | DAQ channel verification (simulated signals) | 21 Phase 0.2 (each channel in spec, 500 Hz sustained) |
| 5 | Tap/impedance test | §3 resonance separation |
| 6 | Fuel pump calibration (4/5/6 bar) + iris calibration | 21 Phase 0.3–0.4 |
| 7 | Dry run 100 % throttle, AB fitted | 21 Phase 4.1; F_dry ≈ 550 N |
| 8 | **Gate runs (21 §5.1–5.5)** | F_s ≥ 700 N @ 500 Hz, T7 1800 ±50 K, shell < 200 °C |

---

## Cross-References

- Bench program & gate: 21 §4–8 (Phases, sensor table, F_s gate 700 N, safety)
- Fuel pump & ignition: 15 (Speck ZY-4S-12V, EV14, check valves, purge)
- AB control electronics & interlocks: 16 §5–7 (state machine, interlock table)
- Thermal limits: 17 §1e, 21 §7 (shell < 200 °C, T5 ≤ 750 °C, T7 ≤ 1900 K)
- Engine mount geometry: 17 §2a (4× M3, 45 mm PCD), INTERFACES I-03
- Structural checks: `tools/thrust_stand_check.py` (committed, reproduces §3)
- AB weight reconciliation: 21 §9 item 6 (0.97 kg vs 18 §3.4 0.83 kg, P0)
