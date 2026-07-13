# Structural Feasibility Analysis: Mach 1 RC Supersonic Aircraft

**Prepared:** 12 July 2026  
**Configuration:** JetCat P550-PRO, MTOW ≤25 kg, biconvex wing, Mach 1 sustained at 10,000 ft  
**Role:** Structures/Aerospace Engineering Review

---

## 1. Dynamic Pressure and Aerodynamic Loads

### Atmospheric Conditions at 10,000 ft (3,048 m)

Using the U.S. Standard Atmosphere (1976):

| Parameter | Value | Units | Source |
|---|---|---|---|
| Altitude | 10,000 (3,048) | ft (m) | — |
| Temperature, *T* | −4.8 (268.35) | °C (K) | ISA lapse rate: 15°C − 6.5°C/km × 3.048 km |
| Pressure, *p* | 69,680 | Pa | Standard atmosphere table |
| Density, *ρ* | 0.9044 | kg/m³ | ρ = ρ₀(T/T₀)^(g₀/(RL)−1) |
| Dynamic viscosity, *μ* | 1.69 × 10⁻⁵ | Pa·s | Sutherland's formula |
| Speed of sound, *a* | √(γRT) = 328.4 | m/s | γ = 1.4, R = 287.058 J/(kg·K) |

> **Note:** The spec quotes "~340 m/s at 10,000 ft." At this altitude the true speed of sound is 328 m/s. 340 m/s is the sea-level value. This introduces a ~3.5% non-conservative error in dynamic pressure calculations if used for structural design.

### Dynamic Pressure

$$q = \frac{1}{2} \rho V^2 = \frac{1}{2} (0.9044)(328.4)^2 = 48,\!769 \text{ Pa} \approx \mathbf{48.8 \text{ kPa}}$$

In imperial: **1,019 psf** (lb/ft²) or **7.07 psi**.

**Comparison to familiar aircraft:**  
At Mach 1 / 10,000 ft, *q* = 48.8 kPa. An aircraft at sea level experiences the same *q* at:

$$V_{EAS} = \sqrt{\frac{2q}{\rho_0}} = \sqrt{\frac{2 \times 48,769}{1.225}} = 282 \text{ m/s} = \text{Mach 0.83 at sea level}$$

The structure sees loads equivalent to a 550 km/h dive at sea level — significant but manageable for a well-designed composite airframe.

### Aerodynamic Loads at 1g Level Flight

| Parameter | Value | Notes |
|---|---|---|
| Wing area, *S* | 0.11 m² | Midpoint of 0.10–0.12 m² spec |
| MTOW | 25 kg × 9.81 = 245.25 N | — |
| Required *C_L* for 1g | 245.25 / (48,769 × 0.11) = **0.0457** | Very low; wing loafs at Mach 1 |
| *C_{Lmax}* at Mach 1 (biconvex) | ~0.4–0.5 | Wave drag limits; thin section stalls early |
| Maximum lift at Mach 1 | 0.5 × 48,769 × 0.11 = **2,682 N** | — |
| Maximum attainable *n* at Mach 1 | 2,682 / 245.25 = **10.9g** | *Hard limit*: cannot pull >11g at this speed without stalling |
| Total wing lift at limit load (10g) | 10 × 245.25 = **2,452 N** | — |

**Key finding:** The *maximum* achievable load factor at Mach 1 is ~11g. The wing cannot generate more lift because the thin biconvex section has limited *C_{Lmax}* at supersonic speeds. This sets a natural ceiling on structural loads *provided* the aircraft avoids diving build-ups (already excluded by spec).

### Drag and Thrust Balance

For sustained level Mach 1 flight:

$$D = q S C_D$$

With biconvex wing at Mach ~1.05:
- Wave drag: $C_{d,wave} \approx \frac{4(t/c)^2}{\sqrt{M^2-1}} = \frac{4(0.0375)^2}{\sqrt{0.1025}} \approx 0.0176$
- Skin friction (turbulent, Re ≈ 1.93×10⁶): $C_{d,f} \approx 0.074/Re^{0.2} \approx 0.0163$
- Wing $C_D$ ≈ 0.034 → wing drag ≈ 48,769 × 0.11 × 0.034 = **182 N**
- Full-aircraft drag (×~2.5 with fuselage, tail, interference) ≈ **450–500 N**

**Thrust at altitude:** The P550-PRO is rated at 550 N sea-level. At 10,000 ft, thrust scales roughly with density ratio: 550 × (0.904/1.225) ≈ **406 N** — marginally below estimated drag. Sustained level Mach 1 flight may be **borderline or require descent/zoom**. This is a *propulsion* concern, not a structural one, but it means the aircraft may spend only brief periods at Mach 1.

---

## 2. Wing Spar Feasibility and Geometry Consistency

### The Geometry Contradiction

The spec contains a **fundamental inconsistency**:

> Root thickness envelope ~27–35 mm  
> Biconvex airfoil 3.5–4% t/c  
> Wing area 0.10–0.12 m², span ~0.9–1.1 m

**Let's check:** For a 4% biconvex section to have a physical thickness of 27 mm:

$$c_{root} = \frac{27\text{ mm}}{0.04} = 675\text{ mm} \quad\text{(for 27 mm root thickness)}$$
$$c_{root} = \frac{35\text{ mm}}{0.035} = 1,000\text{ mm} \quad\text{(for 35 mm root thickness)}$$

That requires a root chord of **675–1,000 mm** on a wing with only **0.9–1.1 m span**. This is geometrically impossible — the root chord cannot exceed the semi-span.

### What the Actual Geometry Is

Given *S* = 0.11 m², *b* = 1.0 m, tapered wing with λ = 0.4:

| Parameter | Value | Derivation |
|---|---|---|
| Mean chord (*c̄*) | 110 mm | *S*/*b* |
| Root chord (*cᵣ*) | **157 mm** | 2*S*/(*b*(1+λ)) = 0.22/(1.0×1.4) |
| Tip chord (*cₜ*) | **63 mm** | λ × *cᵣ* |
| Aspect ratio (*AR*) | **9.1** | *b²*/*S* = 1.0/0.11 |
| Max root thickness (3.75% t/c) | **5.9 mm** | 0.0375 × 157 |
| Max tip thickness (3.75% t/c) | **2.4 mm** | 0.0375 × 63 |

### Resolution of the Discrepancy

The "27–35 mm root thickness envelope" **cannot** refer to the wing airfoil thickness. It most likely refers to one of:

1. **Spar carry-through depth inside the fuselage:** With a 200 mm diameter fuselage, there is ~27–35 mm of vertical clearance for the main spar to pass through internal formers/bulkheads. The actual wing *airfoil* remains 5.9 mm thick; the spar thickens inside the fuselage only (where it's not constrained by the airfoil).

2. **Bulbous root fairing:** A structural fairing at the wing root that provides extra depth for the primary structure.

Regardless of interpretation, the **airfoil physical thickness available for a wing spar is ~6 mm at root**, tapering to ~2.5 mm at tip.

### Implications for Spar Design

A 6 mm spar depth at the root is **extremely shallow** for the bending loads:

At a 10g maneuver (limit load):
- Root bending moment per wing half:*M* = (nW/2) × (b/4) = (10 × 245.25/2) × (0.25) = **306 N·m**  
  *(using quarter-span centroid approximation for elliptical lift)*
- Spar cap force = *M* / *d* = 306 / 0.006 = **51,000 N**
- Required cap area (unidirectional carbon, σ_allowable ≈ 800 MPa):  
  *A* = 51,000 / 800×10⁶ = **63.8 mm²**
- At the root, caps would need to be roughly **6 mm × 11 mm each** (top and bottom) within a total depth of ~6 mm. This means the caps are nearly the full thickness, leaving almost no room for a shear web.
- At **12g ultimate** (1.5×): *M* = 368 N·m → cap force = 61,200 N → area = 76.5 mm² per cap.

**Verdict:** The spar is feasible but **extremely marginal**. The caps essentially fill most of the airfoil thickness, leaving minimal shear web. Requires:
- Ultra-high modulus carbon fibre (M55J or similar, E > 350 GPa)
- Thick-ply unidirectional tape
- Reliable bond between cap and web
- No room for lightning strike mesh or erosion protection within the airfoil envelope

---

## 3. Thermal Loads

### Stagnation Temperature

At Mach 1, 10,000 ft:

$$T_0 = T + \frac{V^2}{2C_p} = 268.35 + \frac{(328.4)^2}{2 \times 1005}$$

$$T_0 = 268.35 + 53.66 = 322.0 \text{ K} = \mathbf{48.9^\circ C}$$

**Recovery temperature:** Depends on boundary layer state:

| Location | Recovery factor (*r*) | *T_r* | Margin below Tg |
|---|---|---|---|
| Leading edge stagnation point | 1.00 | **48.9°C** | ~50–70°C below typical Tg |
| Turbulent boundary layer | Pr^{1/3} ≈ 0.892 | **43.0°C** | ~60–80°C below typical Tg |
| Laminar boundary layer | √Pr ≈ 0.843 | **40.4°C** | ~60–80°C below typical Tg |

### Effect on Epoxy Matrix

| Property | Value | Assessment |
|---|---|---|
| Standard epoxy *Tg* (dry) | 100–140°C | Safe: ~50°C is well below |
| High-temp epoxy *Tg* | 150–200°C | Overkill for flight surfaces |
| Strength at 50°C vs RT | ~90–95% retention | Negligible degradation |
| Creep at 50°C | Minimal below 0.6×*Tg* | Not a concern |

**Conclusion:** Aerodynamic heating at Mach 1 / 10,000 ft is **benign** for carbon-epoxy structure. The skin reaches ~40–50°C, well within the service temperature range of aerospace epoxies. **No special thermal protection required for flight surfaces.**

### Engine Bay — Different Story

The P550-PRO turbine presents a much more severe thermal environment:

| Zone | Estimated Temperature | Concern |
|---|---|---|
| Turbine case exterior | 100–200°C | Can exceed epoxy *Tg*; will soften structural bond |
| Exhaust duct / tailpipe | 300–600°C | Carbon-epoxy will pyrolize; metal required |
| Forward firewall area | 60–120°C | Marginal; high-temp epoxy or aluminum bulkhead needed |

**Recommendations:**
- Aluminum or titanium firewall/bulkhead immediately aft of engine mount
- High-temperature epoxy (e.g., Tg > 180°C) for all structure within 200 mm of engine
- Metal tailpipe / exhaust liner (stainless steel, 0.3–0.5 mm wall)
- Ceramic blanket insulation between engine case and carbon fuselage
- Active cooling air for ECU and fuel lines

---

## 4. Aeroelasticity and Flutter Assessment

### Flutter Parameter Estimation

For thin biconvex wings at Mach 1, flutter is a **critical** design driver.

### Estimated Modal Frequencies

Using the actual wing geometry (*S* = 0.11, *b* = 1.0 m):

| Parameter | Value | Derivation |
|---|---|---|
| Semi-span, *b/2* | 0.5 m | — |
| Spar depth, *d* | ~6 mm root, ~2.5 mm tip | From biconvex profile |
| Average chord, *c̄* | 0.11 m | *S*/*b* |
| Spar width (envelope) | ~30 mm root, ~15 mm tip | ~20% chord |
| Wing mass per half-span | 0.2–0.3 kg | Structure + covering |

**Torsional stiffness** (box spar approximation for a thin-walled closed section):

$$J \approx \frac{4A^2}{\oint ds/t}$$

At root section: *A* ≈ 0.022 × 0.006 = 1.32×10⁻⁴ m², ∮(*ds/t*) ≈ 2(0.022+0.006)/0.0003 = 187

$$J \approx 3.73 \times 10^{-10} \text{ m}^4$$

$$GJ \approx (5 \times 10^9)(3.73 \times 10^{-10}) = \mathbf{1.87 \text{ N·m}^2}$$

**Bending stiffness** (I-beam approximation):

$$I \approx \frac{0.03 \times 0.006^3}{12} \approx 5.4 \times 10^{-10} \text{ m}^4$$

$$EI \approx (135 \times 10^9)(5.4 \times 10^{-10}) = \mathbf{73 \text{ N·m}^2}$$

These are **exceptionally low** stiffness values reflecting the extreme thinness of the wing.

### Natural Frequencies (Cantilever, Root-Fixed)

| Mode | Frequency | Formula |
|---|---|---|
| First bending, *ω_h* | **~28 Hz** (176 rad/s) | (π/2L)² × √(EI/*m̄*) |
| First torsion, *ω_θ* | **~35 Hz** (220 rad/s) | (π/2L) × √(GJ/*I_p*) |
| Frequency ratio, *ω_θ / ω_h* | **1.25** | — |

### Flutter Risk Assessment

**Why this is concerning:**
- **Frequency ratio ≈ 1.25:** Classical bending-torsion flutter occurs when these modes couple. A ratio near 1.0 is the worst case — the modes coalesce easily. Safe designs typically target *ω_θ/ω_h* ≥ 2.0.
- **Transonic dip:** At Mach 0.9–1.1, there is a well-documented reduction in flutter speed (the "transonic dip"). For thin wings, the dip can reduce flutter speed by 20–30%.
- **Low structural damping:** Carbon-epoxy has low material damping (loss factor ≈ 0.5–1%), providing little flutter suppression.

**Expected flutter speed estimate** (simplified):

$$V_f \approx \frac{\omega_\theta b}{\sqrt{2}} \sqrt{\mu r_\theta^2 \left(1 - \frac{\omega_h^2}{\omega_\theta^2}\right)}$$

where *μ* = mass ratio, *b* = semi-chord, *r_θ* = radius of gyration.

Using approximate values for this wing:
- *μ* = *m̄*/(πρ*b²*) ≈ 0.4/(π × 0.904 × 0.055²) ≈ 0.4/(0.0086) ≈ 46.5
- *r_θ* ≈ 0.35 (dimensionless)
- With ratio 1.25: the term 1 − (ω_h/ω_θ)² = 1 − 0.64 = 0.36

$$V_f \approx \frac{220 \times 0.055}{\sqrt{2}} \sqrt{46.5 \times 0.35^2 \times 0.36} \approx 8.55 \sqrt{2.05} \approx 12.2 \text{ m/s}$$

This is a **very crude** 2D approximation and the result (12 m/s) is artificially low because the 2D strip theory over-penalizes the low aspect ratio 3D wing. But even applying a realistic correction factor of 5–10×, the flutter speed may be in the **120–250 m/s range**, which is still **below the Mach 1 operating speed of 328 m/s**.

### Mitigation Measures Required

1. **Closed carbon box spar** with ±45° shear webs occupying the full airfoil thickness
2. **Mass balancing** — no servo or mass aft of the elastic axis; servos mounted forward with push-pull rods
3. **Wing-tip mass balancers** if needed
4. **Stiffer skin** — consider 0°/90°/+45° layup with higher areal weight
5. **Active flutter suppression** via flight controller (accelerometer + gyro sensing, high-rate servo response)
6. **Flutter clearance flight testing** with telemetry accelerometers at multiple spanwise stations
7. **Do not operate near Mach 1 at low altitude** (higher *q* exacerbates flutter)

**Verdict:** Flutter is the **single greatest structural risk**. The thin wing produces very low torsional stiffness, frequencies are dangerously close, and operating speed is in the transonic dip region. Mitigation is possible but demands exceptional design rigor.

---

## 5. Weight Budget Analysis

### Component Weight Estimates

| Component | Estimate (kg) | Basis |
|---|---|---|
| **Engine system** | | |
| JetCat P550-PRO (bare) | 4.90 | Manufacturer spec |
| Mount, firewall, vibration isolators | 0.40 | Aluminum/carbon mount structure |
| ECU, wiring harness, sensors | 0.30 | ECU + cables |
| Starter/battery or pneumatic system | 0.25 | For turbine start |
| *Engine system subtotal* | *5.85* | |
| | | |
| **Fuel system** | | |
| Jet-A1 fuel (4.5 min @ full power) | 1.38 | 275 g/min × 5 min |
| Fuel tank (bladder or rigid) | 0.15 | Carbon/Kevlar wrap |
| Plumbing, valves, clunk, filler | 0.15 | |
| *Fuel system subtotal* | *1.68* | |
| | | |
| **Airframe structure** | | |
| Fuselage shell (200φ × 2.0m, 1.5 m², 3-ply carbon, ~500 g/m²) | 0.75 | Thin shell, locally reinforced |
| Bulkheads and formers (×6–8) | 0.40 | Plywood or carbon plate |
| Wing skins (2 × 0.12 m² × 2 sides, 300 g/m²) | 0.14 | Thin carbon skin |
| Wing spar (carbon, including root reinforcement) | 0.35 | Heavy unidirectional + shear web |
| Wing root joiner / carry-through | 0.15 | Carbon or aluminum billet |
| Tail surfaces (stabilator + fin + rudder) | 0.30 | Carbon sandwich |
| Control surface hinges and horns | 0.08 | |
| *Airframe subtotal* | *2.17* | |
| | | |
| **Avionics and control** | | |
| HV digital metal-gear servos ×6 (@70 g) | 0.42 | Aileron×2, elev×1, rudder×1, throttle, gear |
| Pushrods, clevises, bellcranks | 0.12 | Carbon tube pushrods |
| Receiver + antennas | 0.04 | 2.4 GHz redundant Rx |
| Flight controller + IMU + pitot/static | 0.08 | For stabilization and telemetry |
| GPS module | 0.01 | |
| Power distribution + wiring | 0.15 | |
| Rx battery (2S LiFe 2000 mAh) | 0.12 | |
| *Avionics subtotal* | *0.94* | |
| | | |
| **Landing gear** | | |
| Pneumatic retract units (mains ×2 + nose ×1) | 0.50 | Heavy-duty, scale |
| Wheels + tires (3×) | 0.25 | High-speed rated |
| Brakes | 0.08 | Disc brakes for rollout |
| Retract valve/servo or sequencer | 0.05 | |
| *Landing gear subtotal* | *0.88* | |
| | | |
| **Miscellaneous** | | |
| Paint, finish, decals | 0.25 | |
| Canopy / hatch | 0.10 | |
| Fasteners, adhesives, potting | 0.15 | |
| Ballast for CG | 0.20 | |
| Parachute / recovery system (drag chute) | 0.25 | Recommended for landing |
| *Miscellaneous subtotal* | *0.95* | |
| | | |
| **TOTAL (dry, no fuel)** | **12.42** | Sum of all above excluding fuel |
| **Fuel** | **1.38** | |
| **TOTAL AOW (with fuel)** | **13.80** | |
| **Margin to 25 kg MTOW** | **11.20 kg** | 44.8% margin |

### Analysis

The budget **easily closes within 25 kg** with 45% margin. This is surprising for a Mach 1 aircraft but reflects:

1. **Small scale:** The planform area is tiny (0.11 m²), limiting structural mass.
2. **25 kg is a very generous MTOW** for this size — it's the maximum allowed under most regulations without special permits.
3. The 25 kg limit gives **substantial room** for reinforcement, thicker skins, heavier spar caps, and flutter-mitigation mass.

**Sensitivity: Even doubling the airframe weight** (to 4.3 kg) and adding 2 kg of additional structure for flutter resistance still leaves MTOW at ~17 kg, well within 25 kg.

**Recommended additional weight allocations:**
- Heavier spar (thicker caps, more conservative design): +0.5 kg
- Heavier skins (for torsional stiffness, flutter): +0.4 kg
- Wing tip mass balancers: +0.2 kg
- Additional bulkheads for fuselage stiffness: +0.2 kg
- Extra fuel (for longer flight): +0.5 kg

**Updated MTOW with margin:** ~15–17 kg — still well within 25 kg.

**Conclusion:** Weight is **not a constraint**. The designer has 8–10 kg of unused weight budget that could be deployed for structural reinforcement, flutter suppression, and additional fuel.

---

## 6. Design Limit Load Factors

### Governing Factors

| Factor | Value | Basis |
|---|---|---|
| **Maximum achievable** at Mach 1 | **10.9g** | *q* × *S* × *C_{Lmax}* / *W* |
| **Limit load factor** | **10g** | Rounded down from max achievable; provides 1g margin for buffet onset |
| **Ultimate load factor** | **15g** | 1.5× safety factor (common for composite structures, per AC 20-107B) |
| **Landing load factor** | **3–4g** | Typical for RC aircraft; sink rate at touchdown |
| **Ground handling** | **2g** | Taxi, takeoff roll, crosswind |

### Load Cases for Structural Design

| Case | Load Factor | Distributed Load (N/m²) | Notes |
|---|---|---|---|
| 1. Level flight (1g) | 1.0 | 2,230 | Baseline |
| 2. Symmetric pull-up (lim) | 10.0 | 22,300 | Wing critical |
| 3. Symmetric pull-up (ult) | 15.0 | 33,450 | Ultimate design |
| 4. Push-over (negative) | −5.0 | −11,150 | Negative *C_L*, lower magnitude |
| 5. Rolling / asymmetric | 8.0 (one wing) | 17,840 | Differential load |
| 6. Landing impact | 3.0 vertical | — | Landing gear critical |

### What This Means for Structure

- Wing design load: **10g limit, 15g ultimate**
- At ultimate (15g), root bending moment = **460 N·m** per half-span
- Spar cap stress at ultimate (6 mm depth, 64 mm² cap): 460/0.006 = 76,667 N → σ = 76,667 / 64×10⁻⁶ = **1,198 MPa** — exceeds typical carbon-epoxy allowable (~800 MPa)
- **Conclusion: The spar requires either deeper section (not available without changing airfoil), higher modulus fibre (M55J at 3,500 MPa+ tensile), or larger cap area (wider spar, reducing space for shear web).**

### Recommended Design Speeds

| Condition | Speed | Notes |
|---|---|---|
| *V_D* (dive) | 360 m/s (Mach 1.1) | 10% above Mach 1 |
| *V_A* (maneuver) | 328 m/s (Mach 1.0) | Full control deflection at limit load |
| *V_C* (cruise) | 280 m/s (Mach 0.85) | Some margin below max |
| *V_F* (flaps) | 60 m/s | Subsonic approach — flaps deployment |
| *V_S1* (stall, clean) | 85 m/s (307 km/h) | Sea level, *C_{Lmax}* = 0.5 |
| *V_S0* (stall, flaps) | 68 m/s (245 km/h) | Sea level, *C_{Lmax}* = 0.8 |

> **Note on stall speed:** 85 m/s (307 km/h) stall speed at sea level is extraordinarily high for an RC model. Landing approach at 110–130 m/s (400–470 km/h) will be required. This demands a very long runway (500+ m), heavy-duty brakes, and possibly a drag chute.

---

## 7. Integrated Verdict: Structural Feasibility

### Summary of Findings

| Category | Rating | Rationale |
|---|---|---|
| **Dynamic pressure / loads** | ✅ SAFE | 48.8 kPa is manageable for composites; max ~11g at Mach 1 |
| **Wing geometry consistency** | ❌ **RESOLVED WITH CAVEAT** | Spec's "27–35 mm thickness" contradicts biconvex 3.5–4% airfoil at given S and b. True wing root thickness is ~6 mm. The 27–35 mm likely refers to spar carry-through depth in fuselage. Deeper is better for structure. |
| **Wing spar feasibility** | ⚠️ **MARGINAL** | 6 mm root depth forces extremely compact spar caps with minimal shear web. Works only with highest-grade carbon. |
| **Thermal loads (flight surfaces)** | ✅ SAFE | 40–50°C skin temp well below epoxy *Tg* |
| **Thermal loads (engine bay)** | ⚠️ **CONCERN** | Requires metal bulkheads, high-temp epoxy, ceramic insulation |
| **Flutter / aeroelasticity** | ❌ **HIGH RISK** | ω_θ/ω_h ≈ 1.25; transonic dip; very low torsional stiffness at 6 mm root. Flutter speed likely < Mach 1. **Critical design driver.** |
| **Weight budget** | ✅ GENEROUS | 12–17 kg estimated vs 25 kg MTOW. 30–50% margin available for reinforcement. |
| **G-loads** | ✅ REASONABLE | 10g limit / 15g ultimate is achievable. |
| **Stall speed / landing** | ⚠️ **OPERATIONAL CONCERN** | ~85 m/s stall speed requires very high landing speed; not a structural issue but a practical one. |

### Overall Feasibility Verdict

**STRUCTURALLY FEASIBLE WITH MAJOR CAVEATS**

The aircraft **can** be built within the specified constraints, but three issues demand extraordinary design attention:

1. **🟢 Weight is not the problem** — the 25 kg MTOW provides generous margin. The real challenges are structural, not mass-driven.

2. **🔴 Flutter is the existential threat.** The wing's 6 mm root depth provides very low torsional stiffness, the frequency ratio is in the danger zone (1.25), and operation at Mach 1 places the aircraft in the transonic dip where flutter margins shrink. This requires:
   - A closed carbon box spar layout
   - ±45° shear plies on spar webs
   - Possibly thicker skins (drag penalty)
   - Wing tip mass balances
   - Stringent flutter analysis using MSC.Nastran or similar
   - Flight flutter testing with accelerometer telemetry
   - A flight envelope with *V_NE* (never-exceed) at least 20% below predicted flutter speed

3. **🟡 The wing spar works only with best-in-class materials.** The root bending moment at 15g ultimate requires spar caps that occupy nearly the entire 6 mm depth. Candidate material: M55J ultra-high-modulus carbon (E = 540 GPa, σ_ult = 3,500 MPa) or IM10 intermediate-modulus (E = 303 GPa, σ_ult = 4,930 MPa).

### Recommended Near-Term Actions

- [ ] Perform detailed 3D FEM of wing (bending + torsion modes) to refine flutter speed
- [ ] Wind tunnel test at representative Reynolds numbers (Re ~ 10⁶) for *C_{Lmax}* data
- [ ] Build and ground-vibration-test a flutter-representative wing specimen
- [ ] Investigate thickened root section (transition from biconvex to a bulged root fairing) to increase spar depth where loads are highest
- [ ] Source M55J, IM10, or equivalent high-modulus carbon prepreg in unidirectional tape
- [ ] Design engine-bay thermal management (ceramic blanket, metal firewall, cooling ducts)
- [ ] Plan for drag chute or brake parachute to manage 400+ km/h landing speeds

---

*Report prepared from first principles. All calculations in SI units. Standard atmosphere per ISA 1976. Flutter analysis uses simplified 2D strip theory; detailed 3D aeroelastic analysis is required before committing to manufacture.*
