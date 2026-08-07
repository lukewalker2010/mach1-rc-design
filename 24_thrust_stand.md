# Thrust Stand Design (AB Bench Qualification Rig)

**Doc:** 24 — Thrust stand build package for the afterburner bench program
**Author:** E2 (Propulsion/Afterburner) with E3 (M&V)
**Date:** 2026-08-07
**Status:** 🟡 design complete; build + Phase 0.1–0.2 verification next
**Engine:** JetCat P550-PRO + afterburner (single engine)
**Gate:** 21 §6 — static wet thrust **F_s ≥ 700 N** at T7 = 1800 K ⇔ net wet ≥ 450 N M1-equivalent; design point F_s = **721 N**

> **Scope.** This is the physical rig that carries out 21 §4 Phases 0–5. Every measured quantity maps 1:1 onto the 21 §5 sensor table (T-1…S-1). All numbers here are produced by `tools/thrust_stand_check.py` (committed, AGENTS.md §4.4) or cite their authority line. Where a spec in 21 §5 cannot be met by an off-the-shelf part without over-spend, the deviation is **flagged, not silently accepted** (§10).

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

## 3. Structural Checks (from `tools/thrust_stand_check.py`)

| Check | Load | Capacity | Margin | Status |
|---|---|---|---|---|
| Load cell (T-1, 100 kg = 981 N) | gate 700 N | 981 N | 1.40× | PASS |
| Load cell vs design point | 721 N | 981 N | 1.36× | PASS |
| Rails (2× SBR12, 5g) | 193 N/rail | ≫ 50 kg/block | ≫ 2.5× | PASS |
| Base frame mid deflection (400 N, 600 mm) | 400 N | 0.121 mm < 1 mm | — | PASS |
| Engine mount bolts (4× M3 A2-70 shear) | 175 N/bolt | 2113 N | 12.1× | PASS |
| Engine mount bolts (bending, 0.35 m arm) | 224 N tension | 2113 N | 9.4× | PASS |
| M6 rod-end (clevis, 1.25× gate) | 875 N | ≥ 1500 N rating | ≥ 1.7× | PASS |
| Structural resonance f_n (cell in line) | — | 179 Hz est. | above 100 Hz | confirm Phase 0.2 |

**Resonance note.** The ~180 Hz engine+cell axial mode is comfortably above the 100 Hz control/logging band, so it will not alias into the thrust measurement at 500 Hz. Still, Phase 0.2 (21 §4) includes a **tap/impedance test** (hammer + accelerometer, or sine sweep) to confirm no stand mode sits at or near the engine spool frequency or its harmonics. If one is found, add mass or stiffen the bracket before any hot run.

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

**Channel budget (ADS1256, 8 diff channels, 24-bit):**

| Channel | 21 §5 | Rate |
|---|---|---|
| ch0 | T-1 thrust | 500 Hz |
| ch1–4 | P-1 ×4 | 100 Hz |
| ch5 | P-3 PT7 | 500 Hz |
| ch6 | F-1 flow | 100 Hz |
| ch7 | F-2 gravimetric | 10 Hz |

Total ADS1256 demand: (1+1)×500 + 4×100 + 100 + 10 = **1510 SPS ≪ 30 000 SPS chip limit** — the 24-bit front end is not a bottleneck. TCs (6× MAX31856 on one SPI bus, ~60 Hz/ch) are independent of the ADS1256. P-2 and S-1 on the Pi I²C/GPIO. Single time base: Pi `monotonic_ns()` stamped at each conversion; trigger edge timestamps the AB fuel-valve command so all channels align for the 0.5 s rolling post-mean (21 §5).

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

**Thermocouple rate deviation (flagged, see §10).** MAX31856 converts in 16.6 ms with 60 Hz rejection ⇒ **60 Hz/channel**, against the 21 §5 ≥ 100 Hz TC log spec. The physical R-type probes used for T7 have a thermal time constant of 1–2 s, so 60 Hz electronic rate fully resolves the burst transient — the 100 Hz number exceeds what the probe itself can respond to. Two options in §10: (a) accept the deviation with rationale (recommended, saves ~$2 000), or (b) NI 9214 class module for literal spec compliance.

**Trigger & interlock.** The AB fuel-valve solenoid drive line from the AB control board (16) is tapped: one copy feeds the solenoid, one edge-sensitive GPIO on the Pi starts/stops the gate-window logging and timestamps the command. The 21 §7 cooling-air interlock lives in the AB control board state machine (16 §7) — the stand DAQ records it, does not implement it.

---

## 6. Software (DAQ + Post-Processing)

All software is committed under `tools/` (AGENTS.md §4.4) and runs on the Pi under Python 3.11+.

**6.1 Acquisition daemon (`daq_bench.py`)** — threaded readers, one per interface, each timestamped with `time.monotonic_ns()`:

| Thread | Source | Output |
|---|---|---|
| ADS1256 | 8 diff channels @ 500 Hz (thrust/PT7) and 100 Hz (rest) | scaled engineering units |
| MAX31856 ×6 | 6 TCs @ 60 Hz | °C, CJC applied in hardware |
| HSC I²C ×2 | ±100 mbar | Pa |
| ECU UART | RPM, EGT, engine fuel flow, battery V | raw + scaled |
| GPIO edge | AB fuel-valve command | trigger timestamps |
| Servo PWM | iris position | % |

Master loop writes a single CSV row per tick (`t_s, ch0..ch7, tc0..tc5, p2a, p2b, rpm, egt, f_eng, ab_trigger, iris`). Raw data is kept for transients; steady-state values come from post-processing.

**6.2 Post-processor (`post_bench.py`)** — implements the 21 §5 rule verbatim:
- **0.5 s rolling mean** → steady-state F_s, T5, T7, PT7, flow.
- Raw samples preserved for transients (light-up, flame-out, abort).
- F_s gate test: `mean(F_s) over the gate window ≥ 700 N`, window = trigger-to-trigger minus 0.5 s settle (21 §6 tare/0.5 s window method).
- F_s → net_M1 conversion per 21 §6: `net_M1 = F_s × (ṁ_M1/ṁ_static) − ṁ_M1 × V∞` with ṁ_static from the measured gravimetric + engine flow.
- Run report (CSV + summary table) consumed by the 21 §8 gate statement and 18 §8 E2 test report.

**6.3 Calibration module (`cal_bench.py`)** — dead-weight thrust calibration of the load cell: apply known masses (0, 10, 25, 50, 70, 90 kg) through the rod-end, least-squares linear fit `F = a·counts + b`, report R², hysteresis, and creep (21 §4 Phase 0.1). Gravimetric cell calibrated with water in the tank. Pressure transducers zeroed/span-checked against a hand pump + reference gauge.

**6.4 Pre-run self-test** — before any hot run, the daemon runs a channel-verification script (21 §4 Phase 0.2): simulates signals on every channel, checks each reads within spec and the 500 Hz thrust path sustains rate, then arms the cooling-air interlock flag for display.

---

## 7. Calibration & Tare Procedure (21 §4 Phase 0.1 + 21 §7)

1. **Zero:** load cell unloaded, record 60 s zero; tolerance ±2 N.
2. **Dead-weight curve:** 0 → 900 N in ~5 steps and back (hysteresis); linearity ±1 N over 0–800 N required.
3. **Creep:** hold 500 N for 1 h; drift < ±2 N.
4. **Engine-off tare:** run engine idle 30 s, re-zero (absorbs line forces, pipe weight, stand friction) — 21 §7 tare procedure.
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

1. **TC log rate (21 §5 ≥ 100 Hz vs 60 Hz hardware).** MAX31856 = 60 Hz/channel; physical R-type probe τ = 1–2 s. **Recommendation:** accept the deviation (electronic rate ≫ probe response; 0.5 s rolling mean fully resolves the burst). Compliant alternative = NI 9214 class module (cDAQ-9174 + NI-9214, ≈ $2 500) if the program insists on the letter of the spec. E2/E3 to sign off in the 21 change log.
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
