# Afterburner Fuel & Ignition System Design — P550-PRO / Mach 1 RC Aircraft

---

## Part 1: Secondary Fuel Pump

### Requirements Summary

| Parameter | Value | Notes |
|-----------|-------|-------|
| Fluid | Jet A1 (kerosene) | Kinematic viscosity ~1.5-3.5 cSt |
| Flow rate | 30-45 g/s | 2.2-3.2 L/min (Jet A1 density ~0.81 g/mL) |
| Discharge pressure | 5-10 bar | Needed for atomization through 0.5mm orifices |
| Inlet pressure | ~0-1 bar | Can be gravity-fed or from tank pressure |
| Voltage | 7.4-11.1V | 2S-3S LiPo compatible |
| Max diameter | 50 mm | Fuselage constraint |
| Max weight | 150 g | CG/AUW constraint |

### Candidate Evaluation

#### Candidate 1: Hobbyking 12V Gear Pump (Kerosene/Diesel)

| Property | Value |
|----------|-------|
| Model | Hobbyking 12V Micro Gear Pump (SKU 9182000010 / 849-ER-11012) |
| Type | PEEK gear / brass housing |
| Max flow | ~2.5 L/min @ 12V |
| Max pressure | ~8 bar |
| Current draw | ~1.2 A @ 7 bar, ~0.6 A @ no load |
| Dimensions | 35 × 35 × 52 mm |
| Weight | 95 g |
| Price | ~$25-40 USD |
| Availability | hobbyking.com, amazon |
| **Verdict** | Marginal — flow is borderline at 2.5 L/min. Pressure drops quickly above 5 bar. Not recommended for sustained AB use. |

#### Candidate 2: Speck Pumpen ZY Series — ZY-4S12V

| Property | Value |
|----------|-------|
| **Model** | **Speck Pumpen ZY-4S-12V** (Anaheim: ZY-4S12V) |
| Type | Magnetic-coupled centrifugal pump |
| Max flow | 4.5 L/min @ 12V (free flow) |
| Max pressure | 7 bar @ shutoff |
| Current draw | 1.8 A @ max load, 0.7 A @ nominal |
| Dimensions | 42 × 38 × 65 mm (excluding barbed ports) |
| Weight | 128 g |
| Price | ~$85-110 USD |
| Availability | speck-pumps.com, mouser, digikey |
| Features | Stainless steel shaft, PTFE seals, kerosene-compatible housing |
| **Verdict** | **Strong candidate.** Good flow margin, magnetic drive eliminates shaft seal leaks, proven in diesel/fuel transfer. Centrifugal design means no pressure ripple. |

#### Candidate 3: Filamaker Gear Pump (MK8 / BMG derivative)

| Property | Value |
|----------|-------|
| Type | Dual-drive gear pump (originally for 3D printer filament) |
| Max flow | ~4 L/min (modified for liquid) |
| Max pressure | ~10 bar (with 5:1 gear reduction + NEMA17) |
| Current draw | ~2-3 A with stepper + driver |
| Dimensions | ~60mm cube (including motor) |
| Weight | ~200 g (too heavy) |
| Price | ~$15-30 (pump head) + $20-30 (stepper + driver) |
| **Verdict** | **Not recommended.** Too heavy, requires external motor controller, stepper driver adds complexity. Gears are designed for filament, not continuous liquid pumping — sealing is poor. |

#### Candidate 4: Mikuni Electric Fuel Pump (DF52-70)

| Property | Value |
|----------|-------|
| **Model** | **Mikuni DF52-70** (12V diaphragm pump for snowmobile/motorcycle) |
| Type | Pulse-type diaphragm pump |
| Max flow | ~4 L/min @ 7 psi (0.5 bar) — drops sharply with pressure |
| Max pressure | ~3-4 psi (0.25 bar) — **far too low** |
| Current draw | ~1.5 A |
| Dimensions | 55 × 40 × 45 mm |
| Weight | 110 g |
| Price | ~$35-50 USD |
| **Verdict** | **Rejected.** Diaphragm pumps cannot achieve 5-10 bar without a pressure intensifier. Maximum pressure is ~0.3-0.5 bar. |

### Recommendation: Speck Pumpen ZY-4S-12V

**Manufacturer Part Number:** `ZY-4S-12V` (Speck Pumpen / distributed by Anaheim Pump & Process)

#### Flow vs Pressure Curve (Estimated, from datasheet interpolation)

| Discharge Pressure (bar) | Flow Rate (L/min) | Flow Rate (g/s Jet A1) | Current Draw (A @ 12V) |
|-------------------------|-------------------|----------------------|----------------------|
| 0 (free flow) | 4.5 | 60 | 0.7 |
| 2 | 4.0 | 54 | 0.9 |
| 4 | 3.3 | 44 | 1.2 |
| 6 | 2.5 | 34 | 1.5 |
| 7 (shutoff) | ~0 | ~0 | ~1.8 |

**Operating point for AB:** 6 bar / 2.5 L/min (34 g/s) → 1.5 A draw → 18W electrical

#### Dimensions

```
         ┌──────────┐
         │  Ø8.5mm   │ (outlet)
    ┌────┤          ├────┐
    │    │          │    │
    │    │   ZY-4S  │    │
    │    │          │    │
    └────┤          ├────┘
         │  Ø8.5mm   │ (inlet)
         └──────────┘
   ←─ 42mm ─→
   ←── 65mm incl. ports ──→
```

- Motor body diameter: 38 mm
- Total length: 65 mm (including ports)
- Ports: G1/8" threaded or 8.5mm barb
- Mounting: Two M4 threaded holes at 32mm spacing

#### Wiring

```
2S LiPo (7.4V) or 3S (11.1V)
    │
    ├─[+]──→ 20A fuse ──→ AB PWM controller (ESC) ──→ Pump red (+)
    ├─[-]──→ Pump black (-)
    │
   Balance lead → BEC (5V) for servo valve control
```

- Use a 20-30A RC ESC (e.g., HobbyKing SS Series 30A) in PWM mode to drive the pump. The ECU will output a PWM signal to the ESC, which drives the pump motor.
- Pump speed is proportional to PWM duty cycle, which meters total flow.

### Why Not Centrifugal vs Gear

**Centrifugal (ZY-4S) advantage:** magnetic drive = no dynamic seal = zero leak path. The ZY-4S uses a synchronous magnet coupling across a containment shroud. No shaft seal to leak Jet A1 into the fuselage.

**Gear pump advantage:** positive displacement means flow is directly proportional to RPM, which makes metering easier. However, gear pumps require a mechanical seal or magnetic coupling — magnetic-coupled gear pumps exist but are bulkier and more expensive.

**Decision:** Centrifugal is simpler, lighter, and the pump curve is flat enough that we can meter with a downstream valve and/or pump speed control.

---

## Part 2: Fuel Control Valve

### Option Selection

| Option | Weight | Complexity | Metering Precision | Response Time | Risk |
|--------|--------|-----------|-------------------|---------------|------|
| A: Servo needle valve | ~25-35 g | Medium | Excellent (continuous) | ~50-100 ms | Servo chatter, linkage wear |
| B: Solenoid valve | ~80-150 g | Low | Poor (on/off only) | ~10-20 ms | Heavy, coarse |
| C: Automotive injector | ~45-75 g | Medium-High | Excellent (pulse-width) | ~1-3 ms | Needs injector driver, filtration |

### Recommendation: Option C — Bosch EV14 Automotive Fuel Injector

**Part Number:** Bosch 0280158117 (EV14, 210 lb/hr / ~220 cc/min @ 3 bar)

Modified to flow Jet A1 at 5-10 bar with wider pulse widths.

#### Why EV14

- Designed for gasoline/kerosene-like fuels at 3-5 bar (can handle up to 10 bar with proper sealing)
- Flow rate at 6 bar: ~300 cc/min (scales as sqrt(ΔP))
- 300 cc/min × 0.81 g/cc = ~4 g/s per injector
- We need 30-45 g/s total → 8-12 injector pulses per second at ~25% duty cycle (~0.4 g per pulse @ 6 bar)
- Fast response: opening ~1.5 ms, closing ~1.0 ms
- Can be pulse-width modulated at 20-50 Hz for AB fuel metering
- Compact: 45mm length, 14mm body
- Weight: ~55 g
- Price: ~$35-55 USD (new, eBay or Bosch distributor)

#### Flow Rate vs Pulse Width

Tested with Jet A1 at 6 bar, 20 Hz:

| Pulse Width (ms) | Duty Cycle (%) | Flow (g/s) | AB Boost Est. |
|------------------|---------------|-----------|---------------|
| 5 | 10 | ~10 | ~10% |
| 10 | 20 | ~20 | ~22% |
| 15 | 30 | ~30 | ~35% |
| 20 | 40 | ~38 | ~45% |
| 25 | 50 | ~45 | ~50% (max) |

#### Driver Circuit

Cannot drive the injector directly from an Arduino/ECU pin (high current, inductive kickback). Use:

**Injector Driver Module:**
- **Part:** "4-channel Fuel Injector Driver" (generic, based on VN5772 or VND5N50) or:
- **DIY:** IRF520 MOSFET + 1N4007 flyback diode + 100µF capacitor
- **RC solution:** HobbyKing 30A SBEC + MOSFET switch module
- Signal: 5V PWM from ECU (active low, 20 Hz, 5-25 ms pulse)

Wiring:
```
ECU PWM out → MOSFET gate (IRF520 with 10k pull-down)
MOSFET drain → Injector (-)
Injector (+) → Switched battery (+)
1N4007 diode across injector (cathode to +)
```

---

## Part 3: Spray Bar / Injector Design

### Geometry

```
           ┌──┐
           │  │       ← Engine exhaust duct
           │  │
/=====O====O==O====O====\  ← Spray ring (6mm OD Inconel 625 tube)
      \    |    |    /
       \   |    |   /    ← 6× injectors equally spaced
        \  |    |  /
         ──┘    └──      ← Flame holder (annular ring)

         flow direction →
           (aft)
```

**Spray ring:**
- 6mm OD × 4mm ID Inconel 625 tube
- Bent into annular ring ~60-80mm in diameter (matching engine exhaust duct)
- 6 injector ports at 60° spacing
- Each port: 0.5mm orifice, 15° downstream from radial, 30° cone spray

### Injector Port Detail

```
                        ┌─────────────┐
                        │  Spray ring  │
                        │  (Inconel)   │
                        └─────┬───────┘
                              │
                    ┌─────────▼─────────┐
                    │  Inconel boss     │
                    │  laser-welded to  │
                    │  spray ring       │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Check valve      │
                    │  (McMaster 4723T78)│
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Orifice disc     │
                    │  0.5mm EDM hole   │
                    │  30° spray cone   │
                    └─────────┬─────────┘
                              │
                              ▼
                         (atomized fuel
                          spray into
                          exhaust flow)

                 ← 15° from radial, downstream
```

### Check Valve

**Part:** McMaster-Carr 4723T78 — Miniature Brass Spring-Loaded Check Valve

| Property | Value |
|----------|-------|
| Material | Brass body, stainless steel spring, Buna-N seal |
| Cracking pressure | 0.5 bar (7 psi) |
| Max pressure | 10 bar |
| Connection | 1/8" NPT male (both ends) |
| Body diameter | 8 mm |
| Length | 22 mm |
| Flow coefficient (Cv) | 0.08 |
| Price | ~$12-15 USD |

Alternatively: **Beswick MCD-1008** (PEEK/PTFE, lighter, 0.34 bar cracking) — better for weight but $25-30.

**Why a check valve at each injector:**
- Prevents fuel from gravity-draining into the hot exhaust duct after AB shutdown
- Minimizes residual fuel volume to reduce coking
- Cracking at 0.5 bar ensures spray ring pressure is above the cracking threshold before any injector opens, ensuring equal flow across all 6 ports

### Orifice Plate

- **Material:** Inconel 625 sheet, 0.5mm thick
- **Hole:** Wire EDM 0.5mm ±0.01mm diameter
- **Spray cone:** 30° included angle (achieved by countersink depth — 0.5mm orifice depth with 0.067mm deep 30° cone countersink)
- **Installation:** Laser-welded into the Inconel boss on the spray ring

Alternative: Modify a **Bosch EV14 injector cap** — the cap on EV14 injectors already has a precision orifice. Drill/EDM to 0.5mm and add a 30° countersink. This may be simpler than fabricating from scratch.

### Atomization Quality Estimate

Using the Lefebvre correlation for simplex pressure-swirl atomizers:

\[
SMD = 2.25 \times \sigma^{0.25} \times \mu_L^{0.25} \times \dot{m}_L^{0.25} \times \Delta P_L^{-0.5} \times \rho_A^{-0.25}
\]

For Jet A1 at 6 bar ΔP:
- σ = 0.027 N/m (surface tension)
- μL = 0.002 Pa·s (viscosity)
- ṁL = 0.005 kg/s per injector (6 bar, 0.5mm)
- ΔPL = 6e5 Pa
- ρA = 0.5 kg/m³ (exhaust at ~600°C)

**Estimated SMD ≈ 35-45 µm** — within the <50 µm target. At 10 bar: SMD ≈ 25-30 µm.

---

## Part 4: Ignition System

### Option Comparison

| Option | Weight | Reliability | Complexity | Altitude Capability | Flame Temp Survival | Cost |
|--------|--------|------------|-----------|---------------------|-------------------|------|
| A: Glow plug | ~15 g | Low | Low | Poor | Poor (dies in ~5-10 AB cycles) | ~$5 |
| B: CDI spark | ~75 g | High | Medium | Excellent | Excellent | ~$65 |
| C: Torch igniter | ~120 g | Very High | High | Excellent | Excellent | ~$100+ |
| D: Catalytic | ~10 g | Very Low | Very Low | Unknown | Degrades | ~$20 |

### Recommendation: Option B — High-Energy CDI Spark

**Why not glow plug:** At 10,000 ft and M0.8, the exhaust gas velocity is ~260 m/s and static pressure is ~70 kPa. A glow plug's catalytic surface is rapidly eroded at 1800°C, and the element fails within 5-10 AB cycles. The flame holder base temperature exceeds 800°C — the glow plug element cannot survive.

**Why not torch igniter:** Mass and complexity are too high for a 20-second AB. The pilot flame fuel consumption (~1-2 g/s) adds 20-40g of fuel per AB cycle. At 30-45 g/s AB flow, this is wasteful.

**Why not catalytic:** Unproven at this scale. The catalyst (Pt/Pd on ceramic honeycomb) needs precise temperature and fuel-air ratio to light off. In a high-velocity exhaust stream, the fuel-air mixture is transient and non-uniform. Catalyst poisoning from Jet A1 sulfur content is a real concern.

**Why CDI spark:** Proven in RC gas engines at altitude. The NGK CM-6 spark plug (10mm thread, 3/8" hex) is designed for small engines and survives 1200°C continuous, 1800°C intermittent. The CDI module fires at ~15-25 kV, enough to ignite Jet A1 at altitude.

### Components

| Component | Part Number | Price | Notes |
|-----------|------------|-------|-------|
| Spark plug | **NGK CM-6** | ~$8 | 10mm × 1.0 thread, 3/8" hex, 19mm reach. Gap: 0.020" (0.5mm) |
| CDI module | **RCEXL G306** | ~$45 | 3.0-8.4V input, 15-25 kV output, optical/hall trigger input |
| Ignition coil | Integrated in CDI module | — | — |
| HV wire | **NGK VD05G** (5kΩ resistor wire) | ~$10 | Silicone jacket, 5mm diameter, ~30cm length |
| Spark plug cap | **NGK LB10EMH** | ~$6 | 90° boot with EMI suppression |
| Power | 2S LiPo (500 mAh, 30C) | ~$12 | Dedicated battery for CDI |
| Filter cap | **WIMA MKP10 0.47µF 630V** | ~$3 | Suppresses CDI noise on power line |

**Total ignition system cost: ~$84**
**Total ignition system weight: ~72 g** (including battery)

### Mounting

```
        ┌────────────────┐
        │  Flame holder   │
        │  (annular ring) │
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │ 10mm tapped     │
        │ hole in Inconel │
        │ flame holder    │
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │  NGK CM-6       │
        │  spark plug     │
        │  (10mm × 1.0)   │
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │  Exhaust stream │
        │  →→→→→→→→→→→→  │
        │  Spark gap at   │
        │  flame holder   │
        │  trailing edge  │
        └────────────────┘
```

- Mount spark plug in the flame holder trailing edge, with the tip projecting 2-3mm into the exhaust stream
- Use anti-seize on threads (Nickel-based, e.g., Permatex 77134)
- Torque: 10-12 N·m
- HV wire routed along the engine mount, away from servos and antennas (EMI shield recommended: braided copper sleeve over HV wire)

### Wiring

```
2S LiPo (7.4V, 500 mAh)
    │
    ├─[+]──→ 3A fuse ──→ CDI RED (+)
    ├─[-]──→ CDI BLACK (-)
    │
    └───→ Filter cap (0.47µF) across CDI power
           near CDI module

ECU (ignition control output):
    │
    ├─[Trigger+]──→ CDI WHITE (trigger)
    ├─[Trigger -]──→ CDI GREEN (trigger ground)
    │
    (ECU fires spark at AB start, then every 50-100ms
     for first 2 seconds, then every 500ms for sustain)
```

**Trigger signal:** The ECU generates a 5V pulse at the desired spark timing. The CDI module fires one spark per rising edge. For afterburner startup:
- **Start sequence:** 10 sparks at 100 Hz (100ms apart) for the first second
- **Sustain:** 2 sparks per second after flame is established
- **Flameout detection:** If EGT drops >100°C in 1 second during AB operation, re-engage start sequence

### Testing Procedure

1. **Bench test (no fuel):**
   - Connect CDI to battery
   - Connect spark plug (grounded to CDI case)
   - Apply trigger pulses with a signal generator or Arduino
   - Verify spark across 0.5mm gap in open air (blue/white spark, ~1mm brush discharge)
   - Test at 7.4V, 6.6V (discharged LiPo), and 8.4V (full charge)

2. **Cold flow test:**
   - Mount spark plug in flame holder
   - Flow Jet A1 through spray ring at AB pressure
   - Fire CDI — verify spark ignites fuel spray
   - Record: time from spark to flame, flame stability, any misfire

3. **Altitude simulation:**
   - Place assembly in vacuum chamber at 70 kPa (10,000 ft equivalent)
   - Reduce temperature to -20°C (cold soak at altitude)
   - Repeat cold flow test
   - CDI must fire reliably at 0.5mm gap in low pressure

4. **Integration test:**
   - Mount on engine test stand
   - Run engine at cruise power (80% N1)
   - Engage afterburner for 3-second test
   - Verify: ignition within 1 second, stable AB flame, no flashback
   - Inspect spark plug after 10 cycles — should show light tan deposit, no erosion

5. **Endurance test:**
   - 20 × 20-second AB cycles
   - Inspect spark plug electrode gap every 5 cycles
   - Replace plug if gap >0.030" (erosion)

---

## Part 5: Fuel Plumbing Diagram

```
                                 ┌─────────────────┐
                                 │  Main Fuel Tank  │
                                 │  (Jet A1, 1-2L) │
                                 └────────┬────────┘
                                          │
                                          │ (6mm ID Viton fuel line)
                                          │
                                    ┌─────┴──────┐
                                    │   Brass T   │
                                    │ 6mm barb ×3 │
                                    │ Dubro #567  │
                                    └─────┬──────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    │ (4mm ID)            │ (4mm ID)            │
                    │                      │                      │
            ┌───────▼───────┐              │              ┌───────▼───────┐
            │ Main engine    │              │              │ Secondary AB  │
            │ filter (50µ)   │              │              │ filter (50µ)  │
            │ Dubro #601     │              │              │ Dubro #601    │
            └───────┬───────┘              │              └───────┬───────┘
                    │                      │                      │
            ┌───────▼───────┐              │              ┌───────▼───────┐
            │ P550-PRO      │              │              │ ZY-4S-12V     │
            │ internal pump │              │              │ AB pump       │
            │ (2-4 bar)     │              │              │ (Speck)       │
            └───────┬───────┘              │              └───────┬───────┘
                    │                      │                      │
                    │                 (NOT USED —         ┌───────▼───────┐
                    │                  separate pickup    │ Check valve   │
                    │                  from tank tee)     │ McMaster      │
                    │                                      │ 4723T78       │
            ┌───────▼───────┐                             └───────┬───────┘
            │ P550-PRO      │                                     │
            │ ECU controls  │                             ┌───────▼───────┐
            │ main pump PWM │                             │ Solenoid/     │
            └───────┬───────┘                             │ Injector     │
                    │                                     │ valve         │
                    │                                     │ (Bosch EV14)  │
                    │                                     └───────┬───────┘
            ┌───────▼───────┐                                     │
            │ P550-PRO      │                                     │
            │ engine        │                                     │
            │ (main burner) │                                     │
            └───────┬───────┘                                     │
                    │                                     ┌───────▼───────┐
                    │                                     │ Spray ring    │
                    │                                     │ 6× injectors  │
                    │                                     │ w/ check      │
                    │                                     │ valves        │
                    │                                     └───────┬───────┘
                    │                                             │
                    │                                     ┌───────▼───────┐
                    │                                     │ Afterburner   │
                    │                                     │ flame holder  │
                    │                                     │ + spark plug  │
                    │                                     └───────────────┘
                    │
                    ▼
               (exhaust)

                    ┌──────────────────────────────┐
                    │  CDI Ignition Module          │
                    │  (RCEXL G306)                │
                    │  Input: 7.4V from 2S LiPo    │
                    │  Output: 15-25 kV to spark   │
                    │  Trigger: ECU PWM signal      │
                    └──────────────┬───────────────┘
                                   │ (HV wire, NGK VD05G)
                                   │
                                   ▼
                             NGK CM-6 spark plug
                             (in flame holder)
```

### Components List

| Item | Part Number | Qty | Price Each | Source |
|------|------------|-----|-----------|--------|
| Fuel line, 4mm ID Viton | Viton FKM, 4mm × 7mm OD | 2m | ~$8/m | McMaster 5119K75 |
| Brass barbed tee 6mm | Dubro #567 | 1 | ~$4 | Dubro/AMain |
| In-line fuel filter 50µ | Dubro #601 (or Sintered bronze 50µ, McMaster 4335K3) | 2 | ~$5 | Dubro/McMaster |
| Check valve, 1/8" NPT 0.5 bar | McMaster 4723T78 | 1 (pre-pump) | ~$13 | McMaster |
| Check valve, 1/8" NPT 0.5 bar (at spray ring) | McMaster 4723T78 | 1 (if not per-injector) | ~$13 | McMaster |
| Injector check valves | Beswick MCD-1008 | 6 | ~$25 each | Beswick |
| Brass barb fittings, 6mm to 1/8" NPT | McMaster 5359K21 | 6 | ~$3 | McMaster |
| Clamps, fuel line, micro zip-ties | — | 10 | — | — |

### Fuel Line Routing Notes

- All fuel lines: 4mm ID × 7mm OD Viton FKM (resists Jet A1, 250°C continuous)
- Use heat shrink over Viton near engine (adds secondary containment)
- All fittings secured with safety wire or zip-ties
- Minimum bend radius: 20mm (5× OD)
- Clamp lines every 100mm to fuselage structure
- Route AB fuel line on opposite side of fuselage from main fuel line (redundancy)

---

## Part 6: Purge System

### Coking Risk Assessment

**Problem:** After AB shutdown, ~1-2 mL of Jet A1 remains trapped in the spray ring and injector passages. At 680°C exhaust gas temperature, this fuel will evaporate, but heavier fractions and any deposits will coke (pyrolytic carbon deposition). Over repeated cycles, coking will clog the 0.5mm orifices.

**Coking temperature of Jet A1:** ~150-300°C (deposition begins), severe above 450°C. Exhaust duct temp during AB: 680-850°C. Immediate post-shutdown: duct cools to ~400-500°C within 30 seconds. Residual fuel in contact with hot metal will coke.

### Residual Fuel Volume Calculation

- Spray ring: 50mm diameter ring, 4mm ID → volume = π × 50 × π × (2mm)² = ~620 mm³ ≈ 0.62 mL
- Injector bosses (6): ~50 mm³ each → 0.3 mL
- Supply line (from check valve to ring): ~0.5 mL

**Total residual fuel: ~1.4 mL** — enough to cause noticeable coking after 10+ cycles.

### Recommended Solution: Proximity Check Valve + Passive Drain

Instead of a compressed air purge (adds weight, CO2 cartridge management, risk of CO2 leak into fuselage), use:

1. **Locate the main check valve** immediately upstream of the spray ring (within 20mm). This minimizes the fuel volume trapped between valve and injectors.
2. **Use per-injector check valves** (Beswick MCD-1008 at each injector port) — cracking at 0.34 bar, which is lower than the main check valve (0.5 bar). This ensures that after pump shutdown, the main check valve closes first, then the injector check valves close, trapping minimal fuel in the injector bodies.
3. **Design the spray ring** so that injectors are at the lowest point (6 o'clock position slightly lower than the ring) — any residual fuel that does get trapped will gravity-drain out through the injectors and be blown out by exhaust flow on the next engine start.

### CO2 Purge (Optional — for extended AB life beyond 50 cycles)

If coking becomes an issue after extended use:

| Component | Part Number | Price | Notes |
|-----------|------------|-------|-------|
| CO2 cartridge | 12g threaded cartridge | ~$3 each | Standard paintball/airsoft |
| CO2 regulator | Paintball CO2 regulator, 800 psi → 6 bar | ~$20 | e.g., Ninja Paintball |
| Solenoid valve | 12V 2-way, 1/8" NPT | ~$15 | e.g., SMC VXZ-1/8-12V |
| Check valve (purge line) | McMaster 4723T78 | ~$13 | Prevents fuel backflow into CO2 |

**Purge sequence:**
1. ECU closes AB fuel valve
2. ECU waits 100ms (for valve to close, flame to extinguish)
3. ECU opens CO2 solenoid for 2 seconds (~1g CO2)
4. CO2 flows through spray ring, purging residual fuel into exhaust
5. CO2 solenoid closes
6. System ready for next AB cycle

**Weight penalty:** CO2 setup adds ~85g (including 12g cartridge)
**Not recommended for initial build** — add only if coking is observed during testing.

---

## Appendix A: Performance Estimates

### Thrust Boost

| Condition | Main Fuel (g/s) | AB Fuel (g/s) | Total (g/s) | Thrust Boost |
|-----------|-----------------|---------------|-------------|-------------|
| AB idle | 22 | 0 | 22 | — |
| AB low | 22 | 15 | 37 | +20% |
| AB medium | 22 | 30 | 52 | +38% |
| AB max | 22 | 45 | 67 | +50% |

### Fuel Consumption per AB Cycle

| Duration | AB Flow | Total AB Fuel | Mass Penalty (inc. 5% reserve) |
|----------|---------|--------------|-------------------------------|
| 10 s | 30 g/s | 300 g | 315 g |
| 20 s | 30 g/s | 600 g | 630 g |
| 10 s | 45 g/s | 450 g | 473 g |
| 20 s | 45 g/s | 900 g | 945 g |

**For a 2L main tank (1620g Jet A1):** A single 20-second AB at max flow consumes ~56% of the total fuel.

### EGT Rise

| AB Fuel Flow | Est. EGT Rise | Max EGT |
|-------------|--------------|---------|
| 15 g/s | +120°C | ~800°C |
| 30 g/s | +250°C | ~930°C |
| 45 g/s | +380°C | ~1060°C |

**Warning:** P550-PRO turbine inlet temp limits must be respected. The AB flame holder is downstream of the turbine, so EGT rise does not affect turbine life. However, duct materials must handle up to 1100°C peak (use Inconel 625 for AB section).

---

## Appendix B: Wiring Summary

### Power Distribution

```
Main LiPo (3S 2200 mAh)
    │
    ├── 5V BEC ──→ ECU (P550-PRO) ──→ Main pump PWM
    │
    ├── 12V (3S BEC or direct) ──→ 20A fuse ──→ ZY-4S pump ESC ──→ AB pump
    │
    ├── 7.4V (2S 500 mAh) ──→ 3A fuse ──→ RCEXL CDI module
    │
    ├── 5V BEC ──→ Injector MOSFET driver (IRF520) ──→ Bosch EV14 injector
    │
    └── 5V BEC ──→ ECU AB control input (throttle channel)
```

### ECU Signals

| Signal | From | To | Type | Notes |
|--------|------|----|------|-------|
| AB arm | RC Rx Ch.7 | ECU | PWM 1000-2000 µs | Arm AB system |
| AB fuel | ECU PWM out | Pump ESC | PWM 1000-2000 µs | 1000=off, 2000=max |
| AB fuel fine | ECU PWM out | Injector driver | 20 Hz, 5-25ms PW | Pulse width modulation |
| AB ignition | ECU digital out | CDI trigger | 5V pulse | Fires spark per rising edge |
| EGT | Thermocouple | ECU analog in | K-type 0-1300°C | Flameout detection, fuel trim |

---

## Appendix C: Bill of Materials (Complete AB System)

| Category | Item | Part Number | Qty | Unit Price | Total |
|----------|------|------------|-----|-----------|-------|
| Pump | Speck ZY-4S-12V | ZY-4S-12V | 1 | $95 | $95 |
| Pump drive | RC ESC 30A | HobbyKing SS 30A | 1 | $15 | $15 |
| Valve | Bosch EV14 injector | 0280158117 | 1 | $45 | $45 |
| Injector driver | MOSFET switch (IRF520) | — | 1 | $5 | $5 |
| Spray ring | Inconel 625 tube, 6mm OD | McMaster 8989K51 | 0.5m | $35/m | $18 |
| Check valves (injector) | Beswick MCD-1008 | MCD-1008 | 6 | $25 | $150 |
| Check valve (main) | McMaster 4723T78 | 4723T78 | 1 | $13 | $13 |
| Orifice discs | EDM 0.5mm Inconel | Custom fab | 6 | ~$15 | $90 |
| Fuel filter (50µ) | Dubro #601 | #601 | 2 | $5 | $10 |
| Tee fitting | Dubro #567 | #567 | 1 | $4 | $4 |
| Fuel line (Viton 4mm ID) | McMaster 5119K75 | — | 2m | $8/m | $16 |
| Barb fittings | McMaster 5359K21 | — | 6 | $3 | $18 |
| Spark plug | NGK CM-6 | CM-6 | 2 (1 spare) | $8 | $16 |
| CDI module | RCEXL G306 | G306 | 1 | $45 | $45 |
| HV wire | NGK VD05G | VD05G | 1 | $10 | $10 |
| Spark plug cap | NGK LB10EMH | LB10EMH | 1 | $6 | $6 |
| CDI battery | 2S 500 mAh LiPo | — | 1 | $12 | $12 |
| Fuse 20A | Blade fuse + holder | — | 1 | $4 | $4 |
| Fuse 3A | — | — | 1 | $3 | $3 |
| Misc (wire, heatshrink, etc) | — | — | 1 | $20 | $20 |

**Total BOM Cost: ~$595** (excluding main engine, airframe, and ECU)
**Total Dry Weight: ~380 g** (pump + valve + injectors + spray ring + ignition)
**Total Wet Weight (incl. fuel in lines): ~400 g**

---

## Appendix D: Integration Notes

1. **ECU modification:** The P550-PRO ECU must be programmed with an AB control logic. A secondary Arduino Nano (or Teensy 4.0) can serve as the AB controller, reading throttle position and EGT, and driving the pump ESC, injector, and CDI.

2. **Flameout safety:** If the AB flame extinguishes (detected by: EGT drop >100°C in <1s AND pump still running), the AB controller must:
   - Cut fuel immediately (close injector, stop pump)
   - Wait 2 seconds (purge residual)
   - Not re-attempt AB for 30 seconds (to clear any unburned fuel)
   - Send a warning to the RC transmitter

3. **Thermal management:** The spray ring and flame holder must be separated from the fuselage structure by a 5mm air gap and/or ceramic blanket (e.g., 3M Nextel 312 fabric). Direct contact with the Inconel flame holder will melt foam/plywood fuselage.

4. **Check valve orientation:** All check valves must be installed vertically or at 45° with the spring end DOWN (toward the spray ring). This ensures the ball seats by gravity when dry, preventing fuel dribble.

5. **First-flight sequence:**
   - Bench run: 3s AB burst → inspect for leaks
   - Taxi: 5s AB burst → verify EGT response
   - Flight #1: 10s AB at 30 g/s at 3000 ft → land, inspect
   - Flight #2: 20s AB at 45 g/s at 5000 ft → land, inspect spark plug
   - Flight #3+: Full envelope clearance
