# Afterburner: Thermal Analysis, Integration Design & Test Program

**Date:** 2026-07-27
**Engine:** JetCat P550-PRO with afterburner
**Condition:** Mach 1 @ 10,000 ft (3,048 m)

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
- Mass flow ṁ_exh = 0.69 kg/s (at Mach 1, 10kft)
- O₂ mole fraction in exhaust: 14% → mass fraction = 0.14 × 32/28.97 = 0.155
- ṁ_O₂ = 0.69 × 0.155 = **0.107 kg/s**

**Energy balance:**

```
ṁ_fuel × LHV × η_comb = ṁ_exh × cp × ΔT

Solve for fuel flow to reach T_AB = 1800K:
  T_turbine_exit (EGT at full power, Mach 1) ≈ 700°C = 973 K
  ΔT = 1800 - 973 = 827 K
  cp = 1200 J/kgK (combustion products)
  LHV = 43 MJ/kg (Jet A1)
  η = 0.90 (V-gutter flameholder)

ṁ_fuel = 0.69 × 1200 × 827 / (43e6 × 0.90) = 0.0177 kg/s = 17.7 g/s
```

**O₂ balance check:**
- O₂ consumed = 0.0177 × 3.40 = 0.060 kg/s
- O₂ available = 0.107 kg/s
- **56% of available O₂ consumed** — mixture is fuel-lean (φ_O₂ = 0.56)

**Result:**
| Parameter | Value |
|-----------|-------|
| T_turbine_exit | 973 K (700°C) |
| ΔT_AB | 827 K |
| T_AB (design) | **1800 K (1527°C)** |
| AB fuel flow | **17.7 g/s** |
| Equiv. ratio (O₂-based) | 0.56 |

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

**Convective heat flux:**

```
Reynolds number:
  Re = 4 × ṁ / (π × D × μ)
     = 4 × 0.69 / (π × 0.08 × 4e-5)
     = 2.76 / 1.005e-5 = 274,500
```

Gnielinski correlation for turbulent pipe flow:
```
f = (0.79 × ln(Re) − 1.64)⁻²
  = (0.79 × 12.52 − 1.64)⁻²
  = (8.25)⁻² = 0.0147

Pr ≈ 0.7 (combustion products)

Nu = (f/8)(Re−1000)Pr / (1 + 12.7(f/8)^0.5 (Pr^(2/3)−1))
f/8 = 0.00184
Nu = 0.00184 × 273,500 × 0.7 / (1 + 12.7 × 0.0429 × (−0.213))
   = 351.4 / 0.884 = 398

h = Nu × k / D = 398 × 0.08 / 0.08 = 398 W/m²K

q_conv = h × (T_g − T_w) = 398 × (1800 − 1000) = 318,400 W/m² ≈ 318 kW/m²
```

**Total heat flux:**
| Component | Value |
|-----------|-------|
| q_rad | 135 kW/m² |
| q_conv | 318 kW/m² |
| **q_total** | **453 kW/m²** |
| Total heat load (Q) | 453,000 × 0.0503 = **22.8 kW** |

**Heat load as fraction of AB energy:**
ṁ_fuel × LHV = 0.0177 × 43e6 = 761 kW → **3% lost to walls**, balance goes to exhaust enthalpy.

---

### 1c. Film Cooling Effectiveness

**Cooling supply:**
- Cooling air source: ram air scoop, 2-3% of core flow = 0.014-0.021 kg/s
- Supply temperature: T_c ≈ 423 K (150°C after ram recovery)
- Annulus pressure ≈ 2 bar

**Single-row film cooling correlation (30° injection, 1mm holes):**

| x/d | η = (T_g − T_aw)/(T_g − T_c) |
|-----|------|
| 10 (10mm) | 0.30-0.35 |
| 20 (20mm) | 0.20-0.25 |
| 50 (50mm) | 0.10-0.15 |

**Hole sizing:**

Per-hole mass flow (choked, Cd = 0.8):
```
ṁ_hole = Cd × A × P0 / √T0 × √(γ/R) × [(γ+1)/2]^[−(γ+1)/(2(γ−1))]
       = 0.8 × 7.85e-7 × 2e5 / √423 × 0.0699 × 0.579
       = 2.47 × 10⁻⁴ kg/s per 1mm hole
```

20 × 1mm holes → 0.0049 kg/s → **only 0.7% of core flow** — insufficient.

**Required hole count:**
Target 2.5% bleed = 0.017 kg/s → 0.017 / 2.47e-4 = **69 holes**

**Recommended distribution — 5 staggered rows:**

| Row | x (mm) | Holes | φ (mm) | Cumulative flow (kg/s) | η at start | η at end |
|-----|--------|-------|--------|----------------------|------------|----------|
| 1 | 0 | 20 | 1.0 | 0.0049 | 0.35 | 0.15 |
| 2 | 40 | 15 | 1.0 | 0.0086 | 0.35 | 0.15 |
| 3 | 80 | 12 | 1.0 | 0.0116 | 0.35 | 0.15 |
| 4 | 120 | 10 | 1.0 | 0.0141 | 0.35 | 0.15 |
| 5 | 160 | 8 | 1.0 | 0.0160 | 0.35 | 0.20 |
| **Total** | | **65** | | **0.0160 (2.3%)** | | |

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

**With 5 rows, T_aw peaks at ~1600K near the exit and at row overlaps. The 20-hole inlet-only configuration would leave most of the liner unprotected — 65 holes are needed.**

---

### 1d. Wall Temperature and Structural Margin

**Wall temperature calculation (thermal circuit):**

```
Gas side:         q = h × (T_aw − T_wo) + εσ(T_g⁴ − T_wo⁴)
Through wall:     q = k/t × (T_wo − T_wi)
Coolant side:     q = h_c × (T_wi − T_cool)
```

Solving iteratively at the worst point (exit, x=180mm, T_aw=1593K):
- Assume T_wo ≈ 1100K → q_conv = 398 × (1593−1100) = 196 kW/m², q_rad = 0.25×5.67e-8×(1800⁴−1100⁴) = 128 kW/m², q_total = 324 kW/m²
- Through wall: ΔT = q × t/k = 324,000 × 0.001/18 = 18K → T_wi ≈ 1118K
- Back side cooling: verify h_c × (T_wi − 423) ≈ 324 kW/m² → h_c needed ≈ 324,000/695 = 466 W/m²K — achievable in annulus

**Near holes (x=10mm, T_aw=1318K):**
- T_wo ≈ 950K → q_conv = 398 × (1318−950) = 146 kW/m², q_rad = 0.25×5.67e-8×(1800⁴−950⁴) = 138 kW/m², q_total = 284 kW/m²
- ΔT_wall = 284,000 × 0.001/18 = 16K

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

At worst point (exit): ΔT_wall ≈ 18K
σ_th = 150e9 × 14e-6 × 18 / 0.7 = 54 MPa

Near holes: ΔT_wall ≈ 16K
σ_th = 150e9 × 14e-6 × 16 / 0.7 = 48 MPa
```

**Margin check:**
| Stress type | Value | σ_yield (1000°C) | Margin |
|-------------|-------|-------------------|--------|
| Hoop | 8 MPa | 90 MPa | 10.3× |
| Thermal (worst) | 54 MPa | 90 MPa | 1.67× |
| Combined (hoop + thermal) | 62 MPa | 90 MPa | **1.45×** |

**Verdict:** With the calculated heat flux of ~450 kW/m² and 5-row film cooling, the wall temperature gradient through 1mm Inconel 625 produces ~50-55 MPa thermal stress. Combined with 8 MPa hoop stress, total is 62 MPa — within the 90 MPa yield at 1000°C, giving margin of 1.45×.

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

**Cooling flow:**
```
ṁ_cool = 0.023 × 0.69 = 0.016 kg/s (after ~2.3% through film holes, remainder through annulus)
ρ_cool at 423K, 0.7 bar: ρ = 69,700 / (287 × 423) = 0.574 kg/m³
V_cool = 0.016 / (0.574 × 0.00108) = 25.8 m/s
```

**Heat transfer through annulus:**
```
D_h = 0.090 − 0.082 = 0.008 m
Re = 0.574 × 25.8 × 0.008 / 2.5e-5 = 4,740 (turbulent)
Nu = 0.023 × Re^0.8 × Pr^0.4 = 0.023 × 4740^0.8 × 0.7^0.4 = 20.9
h_ann = 20.9 × 0.04 / 0.008 = 104 W/m²K
```

**Cooling air temperature rise:**

Solving the energy balance iteratively (T_liner_outer ≈ 1100K, T_cool_in = 423K):

| Iteration | T_cool_out (K) | ΔT_lm (K) | Q_transfer (W) | Q_absorbed (W) |
|-----------|----------------|-----------|----------------|----------------|
| 1 | 600 | 567 | 104×0.065×567=3840 | 0.016×1100×177=3115 |
| 2 | 550 | 517 | 3490 | 2235 |
| 3 | **580** | **547** | **3690** | **2763** |

**Exit cooling air temperature ≈ 580K (307°C)**

**Outer shell temperature:**
Conduction through 1.5mm 304SS (k=16 W/mK) with Q ≈ 3690W:
ΔT_shell = q × t/k where q ≈ 3690/(π×0.09×0.2) = 65,300 W/m²
ΔT_shell = 65,300 × 0.0015/16 = 6.1K

**Outer shell surface temperature ≈ 580K (307°C)** — exceeds 200°C limit for composite contact.

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

At Mach 1, 10,000 ft:
```
q = 0.5 × ρ × V² = 0.5 × 0.905 × 328² = 48,600 Pa
Cp_scoop = 0.8 (NACA submerged scoop)
Required ṁ_cool = 0.021 kg/s (3% bleed)

Scoop area:
  A = ṁ / (ρ × V × Cp_scoop)
    = 0.021 / (0.905 × 328 × 0.8)
    = 8.8 × 10⁻⁵ m²
  → Equivalent diameter ≈ 10.6 mm
```

Scoop location: Lower fuselage, x = 1.50m (ahead of afterburner, in unheated boundary layer). NACA submerged scoop, flush with fuselage contour, 12mm wide × 8mm deep × 40mm long.

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
        → Film flow: enters plenum chamber at liner inlet, through 65 holes
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
| Fuel pump | 100 | **0** | **Eliminate** — use engine's fuel pump with a tap for AB fuel |
| Solenoid valve | 50 | **30** | Miniature solenoid (MGV series, 28g) |
| Plumbing + fittings | 80 | **50** | Reduce line length, use lightweight AN fittings |
| Ignition system | 60 | **40** | Surface-mount glow plug, no separate exciter |
| Control board + wiring | 80 | **40** | Integrate with ECU interface, shared wiring |
| **Total** | **1300** | **830** | **36% reduction** |

**Key changes:**
- Use KST X08H+ servo (12g, 1.5 kg·cm) for iris — sufficient for friction-free petal mechanism with sync ring
- Tap engine fuel pump (already 2-5 bar) for AB fuel; add only a solenoid valve + metering orifice
- Reduce liner shell gauge from 1.5mm to 0.8mm (annulus is near-atmospheric pressure)
- Switch iris petals to Ti-6Al-4V (half the density of 304SS)

**Target weight: 830g** — under the 1.0 kg budget with margin.

---

### 2e. Impact on Aircraft CG

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

3. **Lightweight afterburner** — Use the revised 830g design.

4. **Accept higher MTOW** — 13.8-14.3 kg is still within structural limits (wing loading increases from 137 to 150 kg/m²).

---

## Part 3: Test Program

### 3a. Bench Test Sequence

**Phase 1 — Cold flow (bench, no fuel):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 1.1 | Compressed air through AB (0.69 kg/s equivalent) | Measure ΔP across spray ring, flameholder, liner | 1 day |
| 1.2 | Vary flow from 0.2-1.0 kg/s | ΔP vs flow characteristic curve | 1 day |
| 1.3 | Measure annulus cooling flow distribution | All 65 holes flowing evenly (±10%) | 1 day |
| 1.4 | Iris nozzle calibration | Throat area vs servo position curve | 1 day |

**Phase 2 — Fuel spray (no combustion):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 2.1 | Water spray test at ambient pressure | Visual: cone angle 30-60°, no dripping | 1 day |
| 2.2 | Jet A1 spray at 2-5 bar | SMD < 50 µm (Malvern or patternator) | 1 day |
| 2.3 | Fuel distribution across V-gutter | Uniform circumferential coverage | 1 day |
| 2.4 | Low-pressure spray at 0.7 bar | Verify atomization at altitude conditions | 1 day |

**Phase 3 — Ignition (no main engine flow):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 3.1 | Spark/glow plug test in still air | Reliable ignition within 1s at ambient P | 1 day |
| 3.2 | Low-pressure ignition at 0.7 atm | Ignition within 2s at 70 kPa | 1 day |
| 3.3 | Cross-fire test: igniter → V-gutter | Flame propagation < 0.5s | 1 day |
| 3.4 | Ignition with airflow at 0.1-0.3 kg/s | Blowout margin (max airflow for ignition) | 1 day |

**Phase 4 — Integration with P550-PRO (engine test stand):**
| Step | Test | Criteria | Duration |
|------|------|----------|----------|
| 4.1 | Dry run: engine 100% with AB installed | EGT stable, back-pressure < 5% rise | 1 day |
| 4.2 | Dry run: cycle iris dry/wet at various throttle | Smooth transition, verify servo position | 1 day |
| 4.3 | Wet run: 3s AB burst at 75% throttle | Thrust rise, EGT < 950°C (turbine exit) | 1 day |
| 4.4 | Wet run: 5s AB burst at 100% throttle | Record: thrust, EGT, wall temp, pressures | 1 day |
| 4.5 | Wet run: 10s AB burst | Verify cooling liner temp < 200°C outer shell | 1 day |
| 4.6 | Wet run: 20s max duration | Structural integrity check post-run | 2 days |
| 4.7 | Repeat 4.4-4.6 × 3 cycles | Repeatability, liner condition after each | 2 days |

### 3b. Instrumentation for Bench Test

| Sensor | Qty | Location | Range | Accuracy |
|--------|-----|----------|-------|----------|
| Load cell (S-type) | 1 | Engine thrust mount | 0-100 kg | ±0.1% |
| K-type thermocouple (1.5mm Inconel sheath) | 3 | AB inlet, mid-flame, exit | 0-1300°C | ±0.4% |
| R-type thermocouple (Pt/Pt-Rh) | 1 | Peak flame zone (centerline) | 0-1600°C | ±0.25% |
| Infrared pyrometer (2-color, 1-2.5 µm) | 2 | Liner wall, x=50mm and x=150mm | 500-2000°C | ±1% |
| Pressure transducer (0-5 bar abs) | 4 | Spray ring, flameholder, liner mid, exit | 0-5 bar | ±0.5% |
| Differential pressure (0-100 mbar) | 2 | Annulus inlet-to-exit | 0-100 mbar | ±1% |
| Turbine flow meter | 1 | AB fuel line (0-5 L/hr) | 0.5-5 L/hr | ±0.5% |
| High-speed camera (optional) | 1 | Through quartz window at liner mid | 1000 fps | — |

**Data acquisition:**
- 16-channel thermocouple DAQ (NI 9214 or similar, 24-bit)
- 8-channel analog input for pressure transducers
- 100 Hz logging rate minimum (200 Hz recommended for transients)
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
| EGT limit (engine exit) | 850°C | Do not exceed engine EGT limit; back-pressure rise must be monitored |

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
- [ ] **EGT limit:** if engine EGT exceeds 850°C during AB, shut down AB immediately
- [ ] **Lighting:** pilot activates AB, expects visible flame extension + thrust increase within 2s
- [ ] **If no light within 2s:** close fuel, wait 3s, may re-attempt at lower throttle setting
- [ ] **If flameout during sustain:** close fuel, open iris to dry, wait 3s, verify EGT stable before re-attempt
- [ ] **After AB shutdown:** verify iris returns to dry position before next activation
- [ ] **Post-run:** minimum 5 minutes between AB runs (cool-down period)
- [ ] **Fuel management:** AB consumes ~18 g/s (~80 ml/s). With 1.2L total capacity, each 5s AB burst consumes ~400 ml. Max 2 bursts per flight.

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
        → A1: 65 film holes into liner (2.3% bleed)
        → A2: remainder exits at nozzle lip
      → Path B (30%): Plenum at liner inlet (mixing chamber)
        → Distributes to 65 film holes via manifold
```

## Appendix B: Key Material Properties

| Material | T_use (°C) | ρ (kg/m³) | k (W/mK) | α (10⁻⁶/K) | σ_y (MPa) at temp |
|----------|-----------|-----------|----------|-------------|-------------------|
| Inconel 625 | 1000 | 8440 | 18 | 14 | 90 (1000°C) |
| 304 SS | 600 | 8000 | 16 | 17 | 150 (300°C) |
| Ti-6Al-4V | 400 | 4430 | 7 | 9 | 800 (20°C) |
| YSZ TBC | 1200 | 5600 | 2.0 | 10 | — |
| Ceramic fiber | 1260 | 128 | 0.05 | — | — |
