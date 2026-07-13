# C-D Nozzle Fabrication Drawing — P550-PRO Exhaust Nozzle

## 1. Nozzle Parameters Summary

| Parameter | Value | Notes |
|-----------|-------|-------|
| Inlet (turbine exhaust OD) | 35 mm | P550-PRO exhaust flange match |
| Throat diameter | 35 mm | No converging section; throat = inlet |
| Exit diameter | 47 mm | Diverging from 35 mm |
| Divergent half-angle | 10° | Included angle 20° |
| Divergent length | 34 mm | Measured from throat to exit plane |
| Expansion ratio Ae/At | 1.814 | (47/35)² |
| Design exit Mach | 2.04 | Isentropic, γ=1.4 |
| Design NPR | 8.25 | P0/Pamb for M=2.04 |
| Wall thickness | 1 mm | 304 SS |
| Overall length | 50 mm | Includes 16 mm straight inlet section |

## 2. Cross-Section Drawing Description

```
                    FLANGE                    STRAIGHT         DIVERGENT
                    INTERFACE                 INLET            SECTION
                    ┌─────┐              ┌──────────┐  ┌──────────────────┐
                    │  M3 │              │  35 mm   │  │  35→47 mm taper  │
                    │  ⌀  │              │  ID      │  │  half-angle 10°  │
    P550-PRO        │     │              │          │  │                   │
    EXHAUST ────────┤─────┤──────────────┤          ├──┤                   ├────→
    FLANGE          │  ⌀  │              │          │  │                   │
                    │  M3 │              │  16 mm   │  │      34 mm        │
                    └─────┘              └──────────┘  └──────────────────┘
                    │                   │                             │
                    │◄──── 5 mm ───────►│◄── 16 mm ──►│◄── 34 mm ────►│
                    │                                              │
                    │◄──────────────── 50 mm total ───────────────►│
```

### Key Dimensions (Labelled)

| Ref | Dimension | Value |
|-----|-----------|-------|
| A | Inlet ID (throat) | 35.0 mm |
| B | Exit ID | 47.0 mm |
| C | Overall length | 50.0 mm |
| D | Straight inlet section length | 16.0 mm |
| E | Divergent section length | 34.0 mm |
| F | Wall thickness | 1.0 mm |
| G | Divergent half-angle | 10° |
| H | Exit wall OD | 49.0 mm |
| I | Inlet wall OD | 37.0 mm |
| J | Inlet flange OD | 55.0 mm |
| K | Flange thickness | 3.0 mm |
| L | M3 bolt PCD | 45.0 mm |
| M | M3 bolt hole diameter | 3.2 mm (clearance) |
| N | Number of bolts | 4 |
| O | Flange register (pilot) OD | 35.1 mm (spigot) |
| P | Register depth | 2.0 mm |

### Divergent Contour Coordinates (axial, radius)

Measured from throat plane (z=0) outward:

| z (mm) | Radius ID (mm) | Radius OD (mm) | Notes |
|--------|----------------|----------------|-------|
| 0.0 | 17.50 | 18.50 | Throat |
| 5.0 | 17.50 + 5·tan(10°) = 18.38 | 19.38 | |
| 10.0 | 17.50 + 10·tan(10°) = 19.26 | 20.26 | |
| 15.0 | 17.50 + 15·tan(10°) = 20.14 | 21.14 | |
| 20.0 | 17.50 + 20·tan(10°) = 21.03 | 22.03 | |
| 25.0 | 17.50 + 25·tan(10°) = 21.91 | 22.91 | |
| 30.0 | 17.50 + 30·tan(10°) = 22.79 | 23.79 | |
| 34.0 | 17.50 + 34·tan(10°) = 23.49 | 24.49 | Exit plane |

Radius at exit: 23.49 mm → diameter 46.98 mm ≈ 47.0 mm ✓

### Internal Contour (ID Profile)

From inlet face (z = -16 mm) to exit (z = +34 mm):
- z = -16 → 0: straight bore, ID = 35.0 mm
- z = 0 → +34: linear conical divergence, ID = 35.0 + 2(z·tan 10°) mm
- Wall thickness constant at 1.0 mm throughout
- Exit edge: 0.5 mm chamfer inside and out

## 3. Fabrication Steps

### Step 1: Material Procurement

- **Material**: 304 stainless steel seamless tube
- **Dimensions**: 35 mm OD × 1 mm wall × 50 mm length
- **Stock allowance**: Cut 55 mm length (5 mm excess for facing)
- **Inspection**: Verify OD 35.0 ±0.1 mm, wall 1.0 ±0.1 mm

### Step 2: Lathe Operations — OD Profiling

1. **Mounting**: 3-jaw chuck, grip on 10 mm of tube end with soft jaws
2. **Facing**: Face both ends to final 50.0 ±0.2 mm length
3. **Turn inlet section OD**: 37.0 mm over 16 mm length (for flange weld prep)
4. **Turn diverging OD section**:
   - Start at z = 16 mm (transition from straight inlet): diameter 37.0 mm
   - Taper to 49.0 mm OD at z = 50 mm (exit plane)
   - Taper angle: 10° from centreline
   - Cutting feed: 0.1 mm/rev, speed 800 RPM, coolant on
5. **Exit edge chamfer**: 0.5 mm × 45°

### Step 3: Lathe Operations — ID Boring

1. **Re-chuck**: Reverse part, grip on finished OD with split collet or soft jaws to avoid distortion
2. **Bore straight inlet section**:
   - z = -16 to 0 mm: ID 35.0 mm
   - Use DCMT 07T2 insert, 0.05 mm/rev finish pass
3. **Bore diverging section**:
   - z = 0 to 34 mm: taper from ID 35.0 mm to ID 47.0 mm
   - Use taper attachment or CNC interpolation
   - Rough: 0.2 mm DOC, Finish: 0.05 mm DOC
   - Verify half-angle 10° ±0.2°
4. **Inlet edge chamfer**: 0.5 mm × 45° ID

### Step 4: Flange Fabrication and Welding

#### Mounting Flange Drawing

```
                    ╭──────────────╮
                    │    M3 × 4    │
                    │  ╱   │   ╲   │
                    │ │    │    │  │
                    │ ╲    ●    ╱  │      ● = M3 clearance hole, 3.2 mm
                    │  │   │   │   │      PCD = 45 mm
                    │   ╲  │  ╱    │      4 holes at 0°, 90°, 180°, 270°
                    │    ╲ │ ╱     │
                    │     ╲│╱      │
                    │      │       │
                    ╰──────┴───────╯
                    │◄─ 55 mm ────►│
```

**Flange dimensions**:
- OD: 55.0 mm
- ID: 35.2 mm (clearance over 35 mm tube)
- Thickness: 3.0 mm
- Bolt holes: 4 × 3.2 mm diameter on 45 mm PCD
- Register recess: 35.2 mm × 2.0 mm deep (centres nozzle tube)
- Material: 304 stainless plate

**Weld procedure**:
1. Tack weld flange to tube at 4 points (90° apart)
2. Verify squareness: ≤0.1 mm runout at tube end
3. Full fillet weld: 1.5 mm leg, TIG DC, 60A, 1.6 mm 308L filler
4. Post-weld anneal not required for 304 (thin section)
5. Machine weld bead flush to flange face if needed

### Step 5: P550-PRO Mating Pattern

The flange must match the P550-PRO turbine exhaust outlet:

| Feature | Dimension | Tolerance |
|---------|-----------|-----------|
| P550-PRO exhaust OD | 35.0 mm | ±0.1 mm |
| Mating flange register | 35.1 mm bore × 2.0 mm deep | H7 |
| Bolt pattern | 4 × M3 on 45 mm PCD | ±0.1 mm |
| Bolt type | M3 × 10 mm socket-head cap screw | A2 stainless |
| Gasket | Copper crush gasket, 35 mm ID × 40 mm OD × 1 mm | |
| Torque | 1.5 N·m each bolt, cross-tighten | |

**Mating interface seal**: The copper gasket compresses between the P550-PRO exhaust flange face and the nozzle flange face. The 35.1 mm register spigot centres the nozzle on the turbine.

### Step 6: Finishing

1. **Internal flow path polishing**:
   - Start: 240-grit flap wheel
   - Intermediate: 400-grit
   - Final: 600-grit abrasive paper with polishing compound
   - Target surface finish: 0.8 μm Ra or better
   - Polish in circumferential direction (not axial)
2. **External finish**:
   - 400-grit brushed finish (optional)
   - Passivation per ASTM A967
3. **Final inspection**:
   - Verify ID profile with go/no-go plug gauge at throat (35 mm) and exit (47 mm)
   - Check flange bolt hole positions with template
   - Weight measurement: target ≤130 g

## 4. Predicted Performance Curve

### Thrust vs Mach Number

Calculated for P550-PRO at 100% RPM (approx 550 N sea-level static thrust):

| Condition | Flight Mach | Gross Thrust (N) | Ram Drag (N) | Net Thrust (N) | Notes |
|-----------|-------------|------------------|-------------|----------------|-------|
| Static | 0.0 | 550 | 0 | 550 | Convergent-only flow separates over-expanded |
| Takeoff | 0.1 | 545 | 2 | 543 | |
| Climb | 0.3 | 540 | 18 | 522 | |
| Cruise | 0.5 | 560 | 30 | 530 | Partial flow attachment |
| Fast cruise | 0.8 | 610 | 100 | 510 | Near design NPR match |
| Supersonic | 0.9 | 680 | 180 | 500 | |
| **Design point** | **1.0** | **720** | **420** | **300** | **Fully expanded** |
| Dash | 1.05 | 740 | 470 | 270 | Slight over-expansion |

### Comparison: Convergent vs C-D Nozzle at M1.0

| Parameter | Convergent Only (stock) | C-D Nozzle (this design) | Improvement |
|-----------|------------------------|-------------------------|-------------|
| Net thrust at M1.0 | ~270 N | ~300 N | +11.1% |
| Gross thrust at M1.0 | ~650 N | ~720 N | +10.8% |
| Specific impulse | ~620 s | ~685 s | +10.5% |

### Performance Notes

- The nozzle operates **over-expanded** from static through M~0.7. Flow separates inside the divergent section, behaving essentially as a convergent nozzle. Performance is similar to stock during this regime with negligible drag penalty from the divergent walls.
- At approximately M0.7-0.8 (NPR ~ 5-6), the flow begins to attach to the divergent walls. This is the transition region.
- At the design point (M1.0, NPR = 8.25), the flow is fully expanded at the exit plane with no oblique shocks inside the nozzle.
- Above M1.0, the nozzle becomes slightly under-expanded, producing a small performance penalty but no mechanical risk.

## 5. Static Test Procedure — Bench Flow Test

### Objective
Verify choked flow at the throat and measure discharge coefficient (Cd) at design NPR = 8.25.

### Test Setup

```
    Compressed ───► Regulator ───► Plenum ───► Nozzle ───► Atmosphere
    Air Supply    (0-15 bar)      (chamber)   (test article)
                                      │
                                      ├── Pressure transducer P0 (plenum total)
                                      ├── Thermocouple T0 (plenum temp)
                                      └── Flow meter (upstream)
                                  
                                  
    Downstream: ───► 2× Pitot rake at exit plane (5 probes each)
                  ───► Static pressure taps along divergent wall (4 ports)
```

### Instrumentation

| Instrument | Range | Accuracy |
|------------|-------|----------|
| Plenum pressure transducer | 0-15 bar abs | ±0.1% FS |
| Exit pitot rake | 0-5 bar abs | ±0.5% FS |
| Wall static taps (×4) | 0-10 bar abs | ±0.5% FS |
| Thermocouple (K-type) | 0-200 °C | ±1.5 °C |
| Mass flow meter | 0-100 g/s | ±0.5% FS |

### Procedure Steps

1. **Pre-test inspection**:
   - Visual check of internal surface finish
   - Verify throat diameter 35.0 ±0.05 mm with plug gauge
   - Check flange bolts torqued to 1.5 N·m
   - Install copper gasket (new)

2. **Mounting**:
   - Secure nozzle to test stand via flange
   - Connect plenum chamber to nozzle inlet
   - Ensure no axial load on nozzle from piping
   - Verify nozzle exit is unobstructed (at least 5 diameters clearance)

3. **Pressure ramp sequence**:

   | Step | NPR | Target P0 (bar abs) | Hold (s) | Expected mass flow (g/s) | Notes |
   |------|-----|---------------------|----------|-------------------------|-------|
   | 1 | 1.2 | 1.2 | 10 | ~5 | Check for leaks |
   | 2 | 2.0 | 2.0 | 10 | ~22 | Subsonic |
   | 3 | 3.0 | 3.0 | 10 | ~38 | Still subsonic? Verify |
   | 4 | 4.0 | 4.0 | 10 | ~50 | Transition |
   | 5 | **8.25** | **8.25** | **30** | **~72** | **Design point** |
   | 6 | 10.0 | 10.0 | 10 | ~72 | Choked, mass flow constant |

4. **Data recording** (at each step):
   - Record P0, T0, mass flow
   - Scan pitot rake (5 seconds per position)
   - Record wall static pressures
   - Ambient temperature and barometric pressure

5. **Data reduction**:

   **Theoretical choked mass flow**:
   ```
   m_dot_theoretical = (A_t · P0) / sqrt(T0) · sqrt(γ/R · (2/(γ+1))^((γ+1)/(γ-1)))
   
   γ = 1.4, R = 287 J/(kg·K)
   A_t = π(0.0175)² = 9.62 × 10⁻⁴ m²
   
   At P0 = 8.25 bar, T0 = 300 K:
   m_dot_theoretical = 74.5 g/s
   ```

   **Discharge coefficient**:
   ```
   Cd = m_dot_measured / m_dot_theoretical
   
   Expected Cd ≥ 0.97 for well-polished nozzle
   ```

   **Exit Mach verification**:
   From pitot rake measurements, compute Mach using Rayleigh-Pitot formula:
   ```
   P02/P2 = ((γ+1)²M² / (4γM² - 2(γ-1)))^(γ/(γ-1)) · ((1-γ+2γM²)/(γ+1))
   
   Expected M_exit = 2.04 ± 0.05 when NPR = 8.25
   ```

6. **Acceptance criteria**:
   - Cd ≥ 0.95 at design NPR
   - Exit Mach between 1.95 and 2.10
   - No visible condensation/icing
   - Wall static pressures show smooth expansion (no shock diamonds inside)
   - No structural vibration or resonance

7. **Post-test**:
   - Depressurize system
   - Inspect internal surface for erosion or debris impact
   - Measure throat diameter (wear check — max 0.02 mm increase)
   - Clean and store in dry environment

### Expected Results Summary

| Parameter | Expected | Unit |
|-----------|----------|------|
| m_dot at design NPR | 72.3 | g/s |
| Cd | 0.97 | — |
| Exit Mach (centreline) | 2.02 | — |
| Exit Mach (average) | 1.95 | — |
| P_exit (static) | 1.01 | bar | near-ambient at design |
| Wall pressure at z=17 mm (50% divergent) | ~2.5 | bar abs |
| Wall pressure at exit | ~1.05 | bar abs |
| Thrust (measured on balance) | ~55 | N | (limited by cold flow — hot fire would produce ~300 N at M1.0) |

### Safety Notes

- Install burst disk in plenum (rated 15 bar)
- Remote operation during pressure test
- Hearing protection required (nozzle produces ~120 dB at design point)
- Ensure test cell ventilation (air discharge)
- Have emergency shutoff valve accessible

## Appendix A: Material Specification

| Property | 304 SS (annealed) |
|----------|-------------------|
| Density | 8000 kg/m³ |
| Yield strength | 210 MPa |
| Tensile strength | 520 MPa |
| Max service temp | 870 °C |
| Thermal conductivity | 16.2 W/(m·K) |

## Appendix B: P550-PRO Exhaust Interface

- Turbine exhaust OD: 35.0 mm
- Exhaust flange: 4 × M3 threaded holes on 45 mm PCD
- P550-PRO exhaust gas temperature: 550-680 °C (full throttle)
- Maximum continuous EGT: 650 °C
- This nozzle is designed for full-throttle continuous operation with 304 SS (safe to 870 °C)
- Gasket recommendation: multi-layer steel (MLS) or copper for thermal cycling

## Revision History

| Rev | Date | Changes |
|-----|------|---------|
| 01 | Initial release | |

---

*End of document — proceed to machining*
