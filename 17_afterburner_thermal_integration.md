# Afterburner: Thermal Analysis, Integration Design & Test Program

**Date:** 2026-07-27 (corrected 2026-08-06)
**Engine:** JetCat P550-PRO with afterburner
**Condition:** Mach 1 @ 10,000 ft (3,048 m)

> **CORRECTED 2026-08-06 per 18 §2 and 21: mass flow at M1/10kft is 1.10 kg/s (not 0.69); see 21_afterburner_bench_program.md.** All mass-flow-scaled numbers in Part 1 are corrected to ṁ = 1.10 kg/s (T5 = 1000 K per 18 §2.1, not 973 K). §2d "eliminate fuel pump" is **VOID** (engine pump max 27.5 g/s < 27.3 g/s AB demand; 13:160); the dedicated Speck ZY-4S-12V pump (15) is restored. §2e CG discussion is superseded by 18 §3.4. Interface I-03 dimensions unchanged.

---

## Part 1: Thermal Analysis

### 1a. Flame Temperature

**Fuel chemistry** — Jet A1 approximated as C₁₂H₂₃:

```
C₁₂H₂₃ + 17.75 O₂ → 12 CO₂ + 11.5 H₂O
          (17.75 × 32 = 568 g O₂ per 167 g fuel)
          → 3.40 kg O₂ per kg fuel (stoichiometric)
```

**O₂ available in exhaust:**
- Mass flow ṁ_exh = 1.10 kg/s (at Mach 1, 10kft) — corrected per 18 §2.1 (was 0.69)
- O₂ mole fraction in exhaust: 14% → mass fraction = 0.14 × 32/28.97 = 0.155
- ṁ_O₂ = 1.10 × 0.155 = **0.171 kg/s**

**Energy balance:**

```
ṁ_fuel × LHV × η_comb = ṁ_exh × cp × ΔT

Solve for fuel flow to reach T_AB = 1800K:
  T_turbine_exit (EGT at full power, Mach 1) ≈ 1000 K  (18 §2.1, 13:120)
  ΔT = 1800 - 1000 = 800 K
  cp = 1200 J/kgK (combustion products)
  LHV = 43 MJ/kg (Jet A1)
  η = 0.90 (V-gutter flameholder)

ṁ_fuel = 1.10 × 1200 × 800 / (43e6 × 0.90) = 0.0273 kg/s = 27.3 g/s
```

**O₂ balance check:**
- O₂ consumed = 0.0273 × 3.40 = 0.093 kg/s
- O₂ available = 0.171 kg/s
- **54% of available O₂ consumed** — mixture is fuel-lean (φ_O₂ = 0.54)

**Result:**
| Parameter | Value |
|-----------|-------|
| T_turbine_exit | 1000 K (727°C) |
| ΔT_AB | 800 K |
| T_AB (design) | **1800 K (1527°C)** |
| AB fuel flow | **27.3 g/s** |
| Equiv. ratio (O₂-based) | 0.54 |

The afterburner operates fuel-lean relative to available O₂. Local stoichiometric pockets near injectors may reach ~2300K, but mixed-out bulk temperature is 1800K.

---

### 1b. Heat Flux to Liner Wall

**Liner geometry:** D = 80mm ID, L = 200mm, area A = π × 0.08 × 0.20 = 0.0503 m²

**Radiative heat flux:**

```
q_rad = ε_g × σ × (T_g⁴ − T_w⁴)
ε_g = 0.25 (H₂O + CO₂ at this scale)
σ = 5.67×10⁻⁸ W/m²K⁴
T_g = 1800 K (gas)
T_w = 1000 K (target wall temperature with cooling)

q_rad = 0.25 × 5.67e-8 × (1800⁴ − 1000⁴)
      = 0.25 × 5.67e-8 × (1.050e13 − 1.00e12)
      = 0.25 × 5.67e-8 × 9.50e12
      = 134,600 W/m² ≈ 135 kW/m²
```

**Convective heat flux (corrected to ṁ = 1.10 kg/s):**

```
Reynolds number:
  Re = 4 × ṁ / (π × D × μ)
     = 4 × 1.10 / (π × 0.08 × 4e-5)
     = 4.4 / 1.005e-5 = 437,700
```

Gnielinski correlation for turbulent pipe flow:
```
f = (0.79 × ln(Re) − 1.64)⁻²
  = (0.79 × 12.99 − 1.64)⁻²
  = (8.62)⁻² = 0.0135

Pr ≈ 0.7 (combustion products)

Nu = (f/8)(Re−1000)Pr / (1 + 12.7(f/8)^0.5 (Pr^(2/3)−1))
f/8 = 0.00168
Nu = 0.00168 × 436,700 × 0.7 / (1 + 12.7 × 0.0410 × (−0.2167))
   = 513.6 / 0.887 = 579

h = Nu × k / D = 579 × 0.08 / 0.08 = 579 W/m²K

q_conv = h × (T_g − T_w) = 579 × (1800 − 1000) = 463,200 W/m² ≈ 463 kW/m²
```

**Total heat flux (corrected):**
| Component | Value |
|-----------|-------|
| q_rad | 135 kW/m² (unchanged — T-dependent only) |
| q_conv | 463 kW/m² (was 318 at ṁ = 0.69) |
| **q_total** | **598 kW/m²** (was 453) |
| Total heat load (Q) | 598,000 × 0.0503 = **30.0 kW** (was 22.8) |

**Heat load as fraction of AB energy:**
ṁ_fuel × LHV = 0.0273 × 43e6 = 1174 kW → **2.6% lost to walls**, balance goes to exhaust enthalpy.

---

### 1c. Film Cooling Effectiveness

**Cooling supply (corrected to ṁ = 1.10 kg/s):**
- Cooling air source: ram air scoop, 2-3% of core flow = 0.022-0.033 kg/s (corrected; was 0.014-0.021)
- Supply temperature: T_c ≈ 423 K (150°C after ram recovery)
- Annulus pressure ≈ 2 bar

**Single-row film cooling correlation (30° injection, 1mm holes):**

| x/d | η = (T_g − T_aw)/(T_g − T_c) |
|-----|------|
| 10 (10mm) | 0.30-0.35 |
| 20 (20mm) | 0.20-0.25 |
| 50 (50mm) | 0.10-0.15 |

**Hole sizing:**

Per-hole mass flow (choked, Cd = 0.8) — unchanged (geometry/P0/T0-based):
```
ṁ_hole = Cd × A × P0 / √T0 × √(γ/R) × [(γ+1)/2]^[−(γ+1)/(2(γ−1))]
       = 0.8 × 7.85e-7 × 2e5 / √423 × 0.0699 × 0.579
       = 2.47 × 10⁻⁴ kg/s per 1mm hole
```

20 × 1mm holes → 0.0049 kg/s → **only 0.45% of corrected core flow (1.10 kg/s)** — insufficient.

**Required hole count (corrected):**
Target 2.5% bleed = 0.0275 kg/s → 0.0275 / 2.47e-4 = **111 holes**
(q_conv-scaling alternative, bleed ∝ Re^0.8 ≈ 1.45×: ~102 holes — final count confirmed on bench, 21 §4 Phase 1.3)

**Recommended distribution — 6 staggered rows (scaled from the 5-row plan):**

| Row | x (mm) | Holes | φ (mm) | Cumulative flow (kg/s) | η at start | η at end |
|-----|--------|-------|--------|----------------------|------------|----------|
| 1 | 0 | 30 | 1.0 | 0.0074 | 0.35 | 0.15 |
| 2 | 32 | 24 | 1.0 | 0.0133 | 0.35 | 0.15 |
| 3 | 64 | 20 | 1.0 | 0.0183 | 0.35 | 0.15 |
| 4 | 96 | 16 | 1.0 | 0.0222 | 0.35 | 0.15 |
| 5 | 128 | 12 | 1.0 | 0.0252 | 0.35 | 0.15 |
| 6 | 160 | 10 | 1.0 | 0.0277 | 0.35 | 0.20 |
| **Total** | | **112** | | **0.0277 (2.5%)** | | |

**Adiabatic wall temperature along liner:**
T_aw = T_g − η × (T_g − T_c) where T_c = 423 K, T_g = 1800 K

| x (mm) | η | T_aw (K) | T_aw (°C) |
|--------|-----|----------|-----------|
| 0-10 (row 1) | 0.35 | 1318 | 1045 |
| 10-20 | 0.25 | 1456 | 1183 |
| 20-40 | 0.15 | 1593 | 1320 |
| 40-50 (row 2) | 0.35 | 1318 | 1045 |
| 80-90 (row 3) | 0.35 | 1318 | 1045 |
| 120-130 (row 4) | 0.35 | 1318 | 1045 |
| 160-170 (row 5) | 0.35 | 1318 | 1045 |
| 180-200 | 0.15 | 1593 | 1320 |

**With 6 rows, T_aw peaks at ~1600K near the exit and at row overlaps. The 20-hole inlet-only configuration would leave most of the liner unprotected — ~105–115 holes (target 2.5% bleed) are needed, confirmed on bench (21 §4 Phase 1.3).**

---

### 1d. Wall Temperature and Structural Margin

**Wall temperature calculation (thermal circuit):**

```
Gas side:         q = h × (T_aw − T_wo) + εσ(T_g⁴ − T_wo⁴)
Through wall:     q = k/t × (T_wo − T_wi)
Coolant side:     q = h_c × (T_wi − T_cool)
```

Solving iteratively at the worst point (exit, x=180mm, T_aw=1593K; h = 579 W/m²K corrected):
- Assume T_wo ≈ 1150K → q_conv = 579 × (1593−1150) = 256 kW/m², q_rad = 0.25×5.67e-8×(1800⁴−1150⁴) = 126 kW/m², q_total = 382 kW/m²
- Through wall: ΔT = q × t/k = 382,000 × 0.001/18 = 21K → T_wi ≈ 1171K
- Back side cooling: verify h_c × (T_wi − 423) ≈ 382 kW/m² → h_c needed ≈ 382,000/748 = 511 W/m²K — achievable in annulus (h_ann 125 W/m²K is the *film* margin driver; see §1e mitigation)

**Near holes (x=10mm, T_aw=1318K):**
- T_wo ≈ 1000K → q_conv = 579 × (1318−1000) = 184 kW/m², q_rad = 0.25×5.67e-8×(1800⁴−1000⁴) = 135 kW/m², q_total = 319 kW/m²
- ΔT_wall = 319,000 × 0.001/18 = 18K

**Hoop stress (pressure load):**
```
σ_hoop = P × r / t
P ≈ 2 bar = 200,000 Pa (combustion rise)
r = 0.040 m, t = 0.001 m
σ_hoop = 200,000 × 0.040 / 0.001 = 8 MPa
```

**Thermal stress (temperature gradient through wall):**
```
σ_th = E × α × ΔT_wall / (1 − ν)
E = 150 GPa (Inconel 625 at 1000°C)
α = 14 × 10⁻⁶ /K
ν = 0.3

At worst point (exit): ΔT_wall ≈ 21-24K
σ_th = 150e9 × 14e-6 × 24 / 0.7 = 71 MPa

Near holes: ΔT_wall ≈ 18K
σ_th = 150e9 × 14e-6 × 18 / 0.7 = 54 MPa
```

**Margin check (corrected to q_total ≈ 598 kW/m²; ΔT_wall scales with q):**
| Stress type | Value | σ_yield (1000°C) | Margin |
|-------------|-------|-------------------|--------|
| Hoop | 8 MPa | 90 MPa | 10.3× |
| Thermal (worst, ΔT_wall ≈ 24 K) | 71 MPa | 90 MPa | 1.27× |
| Combined (hoop + thermal) | 79 MPa | 90 MPa | **1.14×** |

**Verdict (corrected):** With the corrected heat flux of ~600 kW/m² and 6-row film cooling, the wall temperature gradient through 1mm Inconel 625 produces ~71 MPa thermal stress. Combined with 8 MPa hoop stress, total is 79 MPa — within the 90 MPa yield at 1000°C, giving margin of 1.14×. **This is thinner than the 1.45× at the old 0.69 kg/s flow; the mitigation strategies below are now required, not optional (21 §9 item 5).**

**However, at 1 MW/m² (higher gas temperature, degraded cooling):**
```
ΔT_wall = 1e6 × 0.001/18 = 56 K
σ_th = 150e9 × 14e-6 × 56 / 0.7 = 385 MPa → FAR EXCEEDS 90 MPa
```

**Mitigation strategies (ranked by effectiveness):**

| Strategy | Effect | Risk |
|----------|--------|------|
| **1. Corrugated/expansion liner** | Allows thermal expansion without stress buildup — reduces σ_th near zero | Slightly harder to manufacture |
| **2. Accept yield — consumable liner** | Liner yields on first cycle, residual compressive stress on cooldown. Replace every 5-10 flights | Low cycle fatigue, liner may crack after ~20 cycles |
| **3. Thermal barrier coating (TBC)** | 0.2mm YSZ (k=2 W/mK) reduces ΔT_wall by ~40% | Coating spallation risk |
| **4. Increase film cooling rows** | 7 rows instead of 5, or larger holes | Higher bleed penalty |
| **5. Reduce T_AB** | Design for 1600K instead of 1800K: q drops ~35% | Thrust reduction ~15% |

**Recommendation:** Corrugated Inconel 625 liner (Option 1) + thin YSZ TBC (Option 3). This combination eliminates thermal stress concern entirely and provides margin for occasional overtemp.

---

### 1e. Structural Shell Temperature

**Outer shell:** 304 SS, 1.5mm wall, 90mm ID / 93mm OD
**Annulus:** 5mm gap between liner (82mm OD) and shell (90mm ID) → A_annulus = 0.00108 m²

**Cooling flow (corrected to ṁ = 1.10 kg/s):**
```
ṁ_cool = 0.023 × 1.10 = 0.0253 kg/s (after ~2.5% through film holes, remainder through annulus)
ρ_cool at 423K, 0.7 bar: ρ = 69,700 / (287 × 423) = 0.574 kg/m³
V_cool = 0.0253 / (0.574 × 0.00108) = 40.8 m/s
```

**Heat transfer through annulus (corrected):**
```
D_h = 0.090 − 0.082 = 0.008 m
Re = 0.574 × 40.8 × 0.008 / 2.5e-5 = 7,500 (turbulent)
Nu = 0.023 × Re^0.8 × Pr^0.4 = 0.023 × 7500^0.8 × 0.7^0.4 = 25
h_ann = 25 × 0.04 / 0.008 = 125 W/m²K
```

**Cooling air temperature rise (corrected LMTD iteration):**

Solving the energy balance iteratively (T_liner_outer ≈ 1100K, T_cool_in = 423K):

| Iteration | T_cool_out (K) | ΔT_lm (K) | Q_transfer (W) | Q_absorbed (W) |
|-----------|----------------|-----------|----------------|----------------|
| 1 | 650 | 567 | 125×0.065×567=4610 | 0.0253×1000×227=5743 |
| 2 | 610 | 527 | 4280 | 4730 |
| 3 | **610** | **527** | **4280** | **4730** |

**Exit cooling air temperature ≈ 610K (337°C)**

**Outer shell temperature:**
Conduction through 1.5mm 304SS (k=16 W/mK) with Q ≈ 4300W:
ΔT_shell = q × t/k where q ≈ 4300/(π×0.09×0.2) = 76,000 W/m²
ΔT_shell = 76,000 × 0.0015/16 = 7.1K

**Outer shell surface temperature ≈ 610K (337°C)** — exceeds 200°C limit for composite contact. Shell temperature is a **measured PASS criterion (< 200 °C)** in the bench program (21 §8).

**Mitigation:**
| Solution | Shell temp | Complexity |
|----------|-----------|------------|
| 5mm ceramic blanket (k=0.05) between shell & fuse | <100°C | Low |
| Increase annulus to 8mm | ~250°C | Medium (redesign shell) |
| Double cooling bleed to 5% | ~220°C | High (scoop size, drag) |
| Radiative shield (polished foil between shell & fuse) | ~150°C | Low |

**Recommendation:** Wrap shell with 5mm ceramic fiber blanket (e.g., Cotronics 3633, rated to 1260°C) and secure with stainless steel foil. This adds ~30g but keeps fuselage composite below 100°C.

---

## Part 2: Integration Design

### 2a. Mounting to P550-PRO

**Configuration:** Afterburner replaces stock C-D nozzle. Mounts via 4× M3 bolts on 45mm PCD at engine exhaust flange (x = 1.60 m). Cantilevered 350 mm aft.

**Loads:**
- Thrust (wet): 450 N (axial, compressive on bolts)
- Mass: 1.3 kg → 12.8 N static, with 5g vibration → 64 N
- Bending moment at flange: 1.3 × 0.35 × 9.81 × 5 = **22.3 N·m**

**Bolt analysis (4× M3, A2-70 stainless):**

| Check | Value | Capacity | Margin |
|-------|-------|----------|--------|
| Shear per bolt (thrust) | 112.5 N | 2113 N | 18.8× |
| Tension from moment | 248 N | 2113 N | 8.5× |
| Combined (shear + tension) | — | — | >5× |

**M3 bolts are adequate.** However, the load is cantilevered entirely on the engine exhaust flange (cast Inconel). The primary risk is fatigue of the engine flange, not the bolts.

**Recommendation:**
- Use M3 Inconel 718 bolts (not stainless) to match CTE of engine flange
- Apply anti-seize (Nickel-based, e.g., Never-Seez)
- Torque to 2.5 N·m with thread-locker (Loctite 272 high-temp)
- Add a lightweight triangulated strut (CF tube, 6mm OD × 0.5mm wall, ~15g) from afterburner shell to fuselage bulkhead BH8 as a safety backup — not structurally required but reduces engine flange fatigue

**Strut design:**
```
F_strut = M_bending / (strut_arm × sin(θ))
M = 22.3 N·m, arm = 0.15 m, θ ≈ 45°
F_strut = 22.3 / (0.15 × 0.707) = 210 N compression
6mm CF tube (0.5mm wall): σ = 210 / (π×6×0.5) = 22 MPa → Safety factor > 20×
```

---

### 2b. Fuselage Fit

**Cross-section at x = 1.75m (mid-afterburner):**

```
                    ┌──────────────────────────┐
                    │  Fuselage (200mm ID)     │
                    │  ┌────────────────────┐  │
                    │  │  Ceramic blanket   │  │  ← 5mm insulation
                    │  │ ┌──────────────┐   │  │
                    │  │ │ 304SS Shell  │   │  │  ← 90mm OD
                    │  │ │ ┌──────────┐ │   │  │
                    │  │ │ │  5mm gap │ │   │  │  ← cooling annulus
                    │  │ │ │ ┌──────┐ │ │   │  │
                    │  │ │ │ │Liner │ │ │   │  │  ← 80mm ID
                    │  │ │ │ │80mm  │ │ │   │  │
                    │  │ │ │ └──────┘ │ │   │  │
                    │  │ │ └──────────┘ │   │  │
                    │  │ └──────────────┘   │  │
                    │  └────────────────────┘  │
                    └──────────────────────────┘
  52.5mm annular space: ← utility routing zone →
```

**Utility channel packing (52.5mm annular space between shell and fuselage):**

| Item | OD (mm) | Qty | Route |
|------|---------|-----|-------|
| AB fuel line (Viton, 4mm ID × 7mm OD) | 7 | 1 | Bottom, secured every 50mm |
| Cooling air duct (silicone, from scoop) | 15 | 1 | Top, 180° from fuel |
| Igniter cable (coaxial, shielded) | 3 | 1 | Port side |
| Servo pushrod (iris nozzle, 2mm Ti in 4mm PTFE sheath) | 4 | 1 | Starboard |
| K-type thermocouple wires (glass braid, 1mm) | 2 | 3 | Port + starboard |
| UV flame sensor cable (coaxial) | 3 | 1 | Bottom, alongside fuel line |

All utilities secured with RTV-lined P-clips bonded to the outer shell.

---

### 2c. Cooling Air Supply

**Dual-mode cooling system:**

**Mode 1 — Ram air scoop (high-speed):**

At Mach 1, 10,000 ft (corrected to ṁ = 1.10 kg/s):
```
q = 0.5 × ρ × V² = 0.5 × 0.905 × 328² = 48,600 Pa
Cp_scoop = 0.8 (NACA submerged scoop)
Required ṁ_cool = 0.033 kg/s (3% bleed; corrected — was 0.021 at 0.69)

Scoop area:
  A = ṁ / (ρ × V × Cp_scoop)
    = 0.033 / (0.905 × 328 × 0.8)
    = 1.39 × 10⁻⁴ m²
  → Equivalent diameter ≈ 13.3 mm
```

Scoop location: Lower fuselage, x = 1.50m (ahead of afterburner, in unheated boundary layer). NACA submerged scoop, flush with fuselage contour, **13.3 mm equivalent dia** (was 10.6 mm; sized for corrected cooling bleed, 21 §3).

**Mode 2 — Ejector (low-speed/takeoff):**

At low speed, ram pressure is insufficient. The AB exhaust jet creates a low-pressure region at the nozzle exit, drawing cooling air through the annulus via ejector action:
```
ΔP_ejector ≈ ρ_exh × V_exh² × (A_nozzle / A_annulus)
At takeoff: V_exh ≈ 590 m/s, A_nozzle = 0.00238 m², A_annulus = 0.00108 m²
ΔP ≈ 0.196 × 590² × (0.00238/0.00108) = 150 Pa → sufficient for ~1% bleed
```

**Cooling duct schematic:**
```
Scoop (fuselage bottom)
  → 15mm silicone hose
    → Check valve (prevents backflow if ejector overpressures)
      → Tee: 70% to annulus, 30% to film cooling plenum
        → Annulus flow: enters forward annulus, cools shell back-side
        → Film flow: enters plenum chamber at liner inlet, through ~105–115 holes
          → Both exit at nozzle
```

---

### 2d. Weight Budget & Reduction

| Component | Estimated (g) | Revised (g) | Reduction method |
|-----------|--------------|-------------|------------------|
| Transition duct (Inconel) | 120 | **90** | Reduce wall to 0.8mm; 304SS flange, Inconel only in hot zone |
| Spray ring + injectors (Inconel) | 80 | **60** | DMLS-optimized manifold, fewer injectors (6 vs 8) |
| Flame holder (Inconel) | 100 | **70** | Lighter V-gutter design, 0.5mm sheet, dimpled for stiffness |
| Liner (Inconel) | 180 | **130** | Corrugated 0.5mm Inconel 625 (corrugation adds stiffness with less mass) |
| Outer shell (304SS) | 250 | **150** | 0.8mm wall instead of 1.5mm (annulus pressure is near-ambient) |
| Iris nozzle petals + sync ring | 150 | **120** | 3 petals instead of 4, Ti-6Al-4V instead of 304SS |
| Servo for iris | 50 | **50** | No change (KST X08H+, 12g, repurposed — see below) |
| AB fuel pump (Speck ZY-4S-12V) | 100 | **128** | **VOID: "eliminate pump / tap engine pump" reverted (18 §7 D8). Dedicated pump restored (15:46).** |
| Pump ESC (30A) | — | **15** | HobbyKing SS 30A pump drive (15:657) |
| Solenoid valve | 50 | **30** | Miniature solenoid (MGV series, 28g) |
| Plumbing + fittings | 80 | **50** | Reduce line length, use lightweight AN fittings |
| Ignition system | 60 | **40** | Surface-mount glow plug, no separate exciter |
| Control board + wiring | 80 | **40** | Integrate with ECU interface, shared wiring |
| **Total** | **1300** | **973** | **Pump restored (+143 g vs the 830 g pump-less build)** |

**Key changes:**
- Use KST X08H+ servo (12g, 1.5 kg·cm) for iris — sufficient for friction-free petal mechanism with sync ring
- **VOID — "tap engine fuel pump":** the engine pump maxes at 27.5 g/s (13:160) vs the corrected AB demand of **27.3 g/s at M1** with zero headroom, and the AB must meter independently. The dedicated **Speck ZY-4S-12V** (128 g, 15:46) supplies AB fuel at 4 bar / 44 g/s (1.61× margin; 21 §2). This is a P0 fix per 18 §7 D8 and restores the fuel-system weight in the 18 §3.4 mass table (see 21 §9 item 6).
- Reduce liner shell gauge from 1.5mm to 0.8mm (annulus is near-atmospheric pressure)
- Switch iris petals to Ti-6Al-4V (half the density of 304SS)

**Target weight: 973g** — under the 1.0 kg budget with 27 g margin. **NOTE:** this exceeds the 0.83 kg AB mass used in 18 §3.4; CG/mass reconciliation is a P0 cross-team item (21 §9 item 6, 18 §8).

---

### 2e. Impact on Aircraft CG

> **SUPERSEDED 2026-08-06:** this section is based on the pre-re-baseline MTOW 12.99 kg / CG 0.852 m / 5.25 kg ballast. **18 §3.4 is authoritative**: MTOW 13.60 kg, CG 0.975 m ±20 mm, 1.0 kg nose ballast, static margin 16% MAC (engine moved forward to station 1.20 m). With the Speck pump restored (§2d, +143 g → AB ≈ 0.97 kg), the AB mass is ~0.17 kg above the 0.83 kg used in 18 §3.4 — **CG/mass reconciliation is a P0 cross-team item** (21 §9 item 6); the corrected AF moment is within the ±20 mm CG budget with the §3.4 1.0 kg ballast before reconciliation. The historical numbers below are retained for traceability only.

**Baseline (from systems_layout.md):**
- Original MTOW: 12.99 kg (per airframe spec, slightly different from 13 kg used in systems_layout)
- Original CG: 1.127 m (aft of target 0.852 m)
- Original ballast needed: 5.25 kg at x=0.10m to correct CG

**Afterburner addition:**
- Mass: 1.3 kg (original budget) / 0.83 kg (revised)
- CG of AB: at x = 1.78 m (centroid of 1.60-1.95 m length)

**CG shift:**

For revised weight (0.83 kg):
```
ΔCG = M_AB × (x_AB − CG_original) / (MTOW + M_AB)
     = 0.83 × (1.78 − 1.127) / (12.99 + 0.83)
     = 0.83 × 0.653 / 13.82 = 0.039 m
New CG: 1.127 + 0.039 = 1.166 m
```

**Ballast required to bring CG back to 0.852 m:**

With revised AB (0.83 kg):
```
New total mass = 12.99 + 0.83 + m_bal
Target: (ΣM + 0.83 × 1.78 + m_bal × 0.10) / (13.82 + m_bal) = 0.852
(14.651 + 1.477 + 0.1 m_bal) / (13.82 + m_bal) = 0.852
16.128 + 0.1 m_bal = 11.775 + 0.852 m_bal
4.353 = 0.752 m_bal
m_bal = 5.79 kg
```

**Mass growth summary:**
| Configuration | MTOW | CG | Ballast | Nose ballast |
|--------------|------|-----|---------|-------------|
| Original (no AB) | 12.99 kg | 1.127 m | 5.25 kg | Tungsten slug |
| With AB (original 1.3 kg) | 14.29 kg | 1.186 m | 5.79 kg | — |
| With AB (revised 0.83 kg) | 13.82 kg | 1.166 m | 5.79 kg | — |
| AB + engine moved forward 0.2m | 13.82 kg | ~1.06 m | ~3.5 kg | — |

**The CG challenge is severe.** Adding an afterburner compounds the existing aft-CG problem. **Recommendations (in priority order):**

1. **Move engine forward** — Shift engine mount ring from x=1.50 to x=1.30m (as section 4.4 of systems_layout recommends). This reduces the AB's effective arm and adds engine mass forward of the original CG.

2. **Redistribute internal mass** — Move battery to nose (x=0.10m), add AB fuel in the forward tank (share with main engine fuel).

3. **Lightweight afterburner** — Use the corrected 973g design (with restored pump, §2d).

4. **Accept higher MTOW** — 13.8-14.3 kg is still within structural limits (wing loading increases from 137 to 150 kg/m²).

---

## Part 3: Test Program

### 3a. Bench Test Sequence

> **Corrected 2026-08-06:** flows corrected to ṁ = 1.10 kg/s and the matrix is expanded (Phases 0/5, instrumentation §3b, gate conversion, safety) in **21_afterburner_bench_program.md §4–8**. This table is the summary.

**Phase 1 — Cold flow (bench, no fuel):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 1.1 | Compressed air through AB (**1.10 kg/s equivalent** — was 0.69) | Measure ΔP across spray ring, flameholder, liner | 1 day |
| 1.2 | Vary flow from 0.2-1.2 kg/s | ΔP vs flow characteristic curve | 1 day |
| 1.3 | Measure annulus cooling flow distribution | **All ~105–115 holes** flowing evenly (±10%) (was 65) | 1 day |
| 1.4 | Iris nozzle calibration | Throat area vs servo position curve | 1 day |
| 1.5 | **Nozzle-matching check (NEW)** | Wet throat chokes; exit static pressure ≈ ambient (21 §9 item 2) | 1 day |

**Phase 2 — Fuel spray (no combustion):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 2.1 | Water spray test at ambient pressure | Visual: cone angle 30-60°, no dripping | 1 day |
| 2.2 | Jet A1 spray at **4-6 bar** (was 2-5) | SMD < 50 µm (Malvern or patternator); **24–27 g/s total** (21 §2) | 1 day |
| 2.3 | Fuel distribution across V-gutter | Uniform circumferential coverage | 1 day |
| 2.4 | Low-pressure spray at 0.7 bar | Verify atomization at altitude conditions | 1 day |

**Phase 3 — Ignition (no main engine flow):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 3.1 | Spark/glow plug test in still air | Reliable ignition within 1s at ambient P | 1 day |
| 3.2 | Low-pressure ignition at 0.7 atm | Ignition within 2s at 70 kPa | 1 day |
| 3.3 | Cross-fire test: igniter → V-gutter | Flame propagation < 0.5s | 1 day |
| 3.4 | Ignition with airflow **0.1–1.0 kg/s** (was 0.1-0.3) | Blowout margin; **ignition reliable at ≥1.0 kg/s** (1.10 target, 21 §4 Phase 3.5) | 1 day |

**Phase 4 — Integration with P550-PRO (engine test stand):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 4.1 | Dry run: engine 100% with AB installed | EGT stable, back-pressure < 5% rise | 1 day |
| 4.2 | Dry run: cycle iris dry/wet at various throttle | Smooth transition, verify servo position | 1 day |
| 4.3 | Wet run: 3s AB burst at 75% throttle | Thrust rise, **T5 < 750°C (datasheet limit, 13:17)** | 1 day |
| 4.4 | Wet run: 5s AB burst at 100% throttle | Record: thrust, EGT, wall temp, pressures; **T7 = 1800 K** | 1 day |
| 4.5 | Wet run: 10s AB burst | Verify cooling liner temp < 200°C outer shell | 1 day |
| 4.6 | Wet run: 20s max duration | Structural integrity check post-run | 2 days |
| 4.7 | Repeat 4.4-4.6 × 3 cycles | Repeatability, liner condition after each | 2 days |

### 3b. Instrumentation for Bench Test

| Sensor | Qty | Location | Range | Accuracy |
|--------|-----|----------|-------|----------|
| Load cell (S-type) | 1 | Engine thrust mount | 0-100 kg | ±0.1% |
| K-type thermocouple (1.5mm Inconel sheath) | 3 | AB inlet, mid-flame, exit | 0-1300°C | ±0.4% |
| R-type thermocouple (Pt/Pt-Rh) | 2 | AB exit plane (T7, 2 radii) | 0-1700°C | ±0.25% |
| **PT7 (AB inlet total pressure)** | 1 | AB inlet plane (before spray ring) | 0-5 bar abs | ±0.5% |
| Infrared pyrometer (2-color, 1-2.5 µm) | 2 | Liner wall, x=50mm and x=150mm | 500-2000°C | ±1% |
| Pressure transducer (0-5 bar abs) | 4 | Spray ring, flameholder, liner mid, exit | 0-5 bar | ±0.5% |
| Differential pressure (0-100 mbar) | 2 | Annulus inlet-to-exit | 0-100 mbar | ±1% |
| Turbine flow meter | 1 | AB fuel line (0-5 L/hr) | 0.5-5 L/hr | ±0.5% |
| High-speed camera (optional) | 1 | Through quartz window at liner mid | 1000 fps | — |

**Data acquisition (expanded in 21 §5):**
- 16-channel thermocouple DAQ (NI 9214 or similar, 24-bit)
- 8-channel analog input for pressure transducers
- **≥100 Hz logging for thrust, EGT (T5), T7, PT7, AB fuel flow during AB bursts (500 Hz for gate runs)** — 21 §5
- ECU datalink for engine parameters (RPM, EGT, fuel flow)

**Quartz window (optional but recommended for Phase 2-3):**
- 25mm diameter × 5mm thick fused silica
- Located at x=100mm (mid-flame), recessed from liner ID by 5mm to stay cool
- Nitrogen purge to prevent soot deposition

### 3c. Flight Test Limitations

| Parameter | Limit | Rationale |
|-----------|-------|-----------|
| Max AB duration | 20 s continuous | Liner temperature rise; fuel capacity |
| Min activation speed | M0.6 | Ram pressure for cooling air (below M0.6, ejector mode alone insufficient) |
| Min activation altitude | 5,000 ft | Ensure cooling flow density; prevent flameout at low Re |
| Max activation altitude | 15,000 ft | O₂ partial pressure too low above this (O₂ at 14% exhaust: 0.14 × P_amb) |
| Cool-down between runs | 5 min | Liner thermal soak-back; let wall temp drop below 200°C |
| Fuel purge after shutdown | 3 s of dry air | Prevent coking in spray ring (Jet A1 + residual heat) |
| EGT limit (engine exit) | 750°C | Datasheet limit (13:17); AB must not push T5 above this. AB-exit T7 target is 1800 K and is measured separately |

**State machine for AB control:**

```
   [IDLE] ──(AB arm command)──→ [ARMED]
                                   │
                     ┌─────────────┤
                     ▼             ▼
              (M>0.6 & h>5kft) (M or h too low)
                     │             │
                     ▼             ▼
              [ACTIVATION] ←── [ABORT]
                     │             ▲
              (fuel on,             │
               ignite 2s)   (failure to light)
                     │             │
                     ▼             │
              [SUSTAIN] ───────────┘
                     │       (flameout)
                     │
              (20s elapsed or
               manual shutoff)
                     │
                     ▼
              [PURGE] (3s dry air)
                     │
                     ▼
              [COOLDOWN] (5 min)
                     │
                     ▼
              [IDLE]
```

### 3d. Safety Checklist — First AB Flight

**Pre-flight (bench):**
- [ ] AB fuel system pressure tested to 10 bar (1.5× max operating)
- [ ] All fuel connections leak-checked with soapy water at 5 bar
- [ ] Ignition system bench-tested: glow plug glows within 3s at 6V, spark gap verified
- [ ] Iris nozzle full travel tested: 45mm ↔ 55mm throat, smooth, no binding
- [ ] Servo direction verified: close = dry position, open = wet position
- [ ] Failsafe: servo to dry position on signal loss
- [ ] AB fuel solenoid valve: closed with no power (fail-safe closed)
- [ ] Control system state machine bench-tested: simulate all transitions, record time in each state
- [ ] Telemetry: verify K-type thermocouple readings on ground station (ambient = within 5°C of local temp)
- [ ] Manual override switch: immediate AB shutoff (close fuel valve, open iris to dry, start purge)

**Engine test stand:**
- [ ] Dry run to 100% throttle (no AB): verify engine spools normally, EGT stable, no back-pressure issues
- [ ] Dry run with iris cycling: verify no thrust variation in dry position
- [ ] 3s AB burst at 75% throttle: verify ignition, thrust rise, EGT peak
- [ ] 5s AB burst at 100% throttle: record all parameters, verify telemetry works under vibration
- [ ] 10s AB burst: verify outer shell temperature < 200°C (thermocouple or pyrometer)
- [ ] Minimum 3 successful AB runs before aircraft installation

**Pre-flight (aircraft, day of flight):**
- [ ] AB fuel line connected, filter in line, no air bubbles
- [ ] AB fuel solenoid: cycle open/close, verify fuel flow at spray ring (remove igniter, look through port)
- [ ] Iris nozzle: full travel through servo travel, marks on pushrod for visual confirmation
- [ ] Engine ground run: idle → full throttle → idle (verify AB state machine in IDLE)
- [ ] Manual override switch: pilot confirms location, muscle memory check

**First AB flight:**
- [ ] **Min altitude for activation:** 8,000 ft AGL
- [ ] **Min speed for activation:** M0.7
- [ ] **Max AB duration on first flight:** 5 seconds
- [ ] **EGT limit:** if engine EGT (T5) exceeds 750°C during AB, shut down AB immediately (datasheet limit, 13:17)
- [ ] **Lighting:** pilot activates AB, expects visible flame extension + thrust increase within 2s
- [ ] **If no light within 2s:** close fuel, wait 3s, may re-attempt at lower throttle setting
- [ ] **If flameout during sustain:** close fuel, open iris to dry, wait 3s, verify EGT stable before re-attempt
- [ ] **After AB shutdown:** verify iris returns to dry position before next activation
- [ ] **Post-run:** minimum 5 minutes between AB runs (cool-down period)
- [ ] **Fuel management (corrected):** AB consumes ~27 g/s at M1 (T7=1800 K, ṁ=1.10). Per 5s AB burst ≈ 136 g ≈ 168 ml (AB only; 21 §2). With the 2.0 L tank (18 §3.4), max 2 bursts per flight with ~1 L margin per 18 §5.5.

**Post-flight inspection (first AB flight):**
- [ ] Liner visual inspection (boroscope through nozzle): check for cracks, discoloration, hole blockage
- [ ] Shell temperature indicator labels (TL-200, 200°C): verify outer shell stayed within limits
- [ ] Iris petals: check for warping, freedom of movement
- [ ] Spray ring: check for coking (disassemble, inspect injector faces)
- [ ] Fuel solenoid: operate on bench, verify no sticking
- [ ] All fasteners: re-torque M3 engine mounting bolts
- [ ] Thermocouple wires: check for damage at entry points

---

## Appendix A: Cooling Annulus Flow Circuit

```
Ram Air Scoop
  → Check valve
    → Tee
      → Path A (70%): Annulus inlet → flows 200mm aft between liner & shell
        → A1: ~105–115 film holes into liner (2.5% bleed, corrected)
        → A2: remainder exits at nozzle lip
      → Path B (30%): Plenum at liner inlet (mixing chamber)
        → Distributes to ~105–115 film holes via manifold
```

## Appendix B: Key Material Properties

| Material | T_use (°C) | ρ (kg/m³) | k (W/mK) | α (10⁻⁶/K) | σ_y (MPa) at temp |
|----------|-----------|-----------|----------|-------------|-------------------|
| Inconel 625 | 1000 | 8440 | 18 | 14 | 90 (1000°C) |
| 304 SS | 600 | 8000 | 16 | 17 | 150 (300°C) |
| Ti-6Al-4V | 400 | 4430 | 7 | 9 | 800 (20°C) |
| YSZ TBC | 1200 | 5600 | 2.0 | 10 | — |
| Ceramic fiber | 1260 | 128 | 0.05 | — | — |
