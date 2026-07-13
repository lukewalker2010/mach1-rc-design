# Mach 1 RC Plane — Full Engineering Analysis

**Prepared by:** Subagent — Supersonic Inlet & Flight Controls Specialist  
**Date:** 2026-07-12  
**Engine:** JetCat P550-PRO (~55 N thrust)  
**Configuration:** Chin/ventral scoop, flush lip, all-moving stabilator, ~1 m span, ~2 m length  
**Assumed geometry:** Aspect ratio 4 → S_wing ≈ 0.25 m², MAC ≈ 0.25 m  

---

## 1. Intake Analysis — Supersonic Inlet Physics

### Normal-Shock Total-Pressure Recovery

When a flush chin scoop encounters flow at M ≥ 1.0, a **detached bow shock** (approximated as a normal shock at the centerline) sits ahead of the inlet lip. Using standard normal-shock relations (γ = 1.4):

| Mach | M₂ (post-shock) | p₂/p₁ | p₀₂/p₀₁ | **Recovery** | **Loss** |
|:----:|:---------------:|:-----:|:--------:|:------------:|:--------:|
| 1.00 | 1.0000 | 1.000 | **1.000000** | 100.000 % | 0.000 % |
| 1.05 | 0.9531 | 1.120 | **0.999853** | 99.985 % | 0.015 % |
| 1.10 | 0.9118 | 1.245 | **0.998928** | 99.893 % | 0.107 % |
| 1.20 | 0.8422 | 1.513 | **0.992798** | 99.280 % | 0.720 % |
| 1.50 | 0.7011 | 2.458 | **0.929787** | 92.979 % | 7.021 % |

**Key takeaway:** The *pure normal-shock recovery* at M ≤ 1.1 is excellent (≥ 99.9 %). If the total-pressure loss were the only issue, the intake would be fine. **It is not the recovery that kills a flush scoop — it is the flow quality.**

### Why the Flush Scoop Fails Anyway

**Detached bow shock physics:** A flush/ventral scoop has no sharp lip for the shock to swallow. The shock stands off upstream. Flow that enters the scoop first passes through a *curved, detached bow shock* that creates:

1. **Massive spillage drag** — The captured streamtube area is much smaller than the physical inlet area; excess air spills around the lip, creating a high-drag flowfield.
2. **Severe flow distortion** — The shock is non-uniform across the inlet face; part of the flow has passed through a stronger (near-normal) portion of the shock, part through a weaker (oblique) portion. The resulting total-pressure *profile* at the compressor face is highly distorted.
3. **Boundary-layer ingestion** — The chin location on the fuselage means the inlet ingests the fuselage boundary layer, which at RC-scale Reynolds numbers is thick relative to the inlet height.
4. **Unstart / buzz** — The classic "inlet buzz" oscillation: the shock moves alternately swallowed and expelled at frequencies of 10–100 Hz, starving or over-pressuring the compressor in cycles.

---

## 2. Engine Tolerance — Can the P550-PRO Survive This?

### Compressor Type

The JetCat P550-PRO uses a **single-stage centrifugal compressor** (typical for hobby turbines: pressure ratio π_c ≈ 3–4:1, max RPM ~165,000). Centrifugal compressors are more forgiving of inlet distortion than axial compressors because:

- Single, robust flow path
- Less sensitive to inlet swirl/mal-distribution
- Wider surge margin at low corrected flow

However, they are NOT immune:

### Distortion Tolerance — Published & Extrapolated Data

**Full-scale centrifugal engines (e.g., PT6, Allison 250):**
- Tolerate DC(60) distortion descriptors up to ~0.15–0.20 (moderate)
- Surge margin erosion of 5–15 % for severe distortion patterns
- Survivable for steady-state operation if distortion is mild

**Hobby turbines:** No controlled published data exists, but from field experience:

- Many hobby turbines will flame out or surge with direct crosswind at idle (a weak form of inlet distortion)
- A buzz event at full power will almost certainly cause a flameout within 0.5–2 seconds
- The P550-PRO's ECU has no active surge-recovery logic beyond a fuel-cut restart

**Verdict on tolerance:** The P550-PRO will **not** tolerate sustained inlet buzz. Even if the distortion alone is borderline, the transient pressure pulses from buzz will push the compressor past surge margin and cause flameout or mechanical damage (turbine overtemperature from fuel-rich recovery spikes).

### Compressor Operating Point Shift

With a normal-shock pressure recovery of 99.9 % at M 1.05, the compressor inlet pressure is effectively ambient. However:

- The dynamic pressure **q = ½ρV²** = ~71 kPa at M 1.0 SL means the compressor sees *high inlet Mach numbers* (M_inlet ~ 0.5–0.7 depending on area contraction)
- This moves the operating point up the speed line toward choke
- The compressor map shows reduced surge margin at high corrected flow

**The real threat is not pressure recovery loss but inlet Mach number and distortion.**

---

## 3. Inlet Starting & Buzz — The Showstopper

A flush scoop at supersonic speed *cannot start* without:

- Variable geometry (movable ramp/spike)
- Boundary-layer bleed
- Or a very high contraction ratio (which creates its own problems)

**Starting criterion** (Kantrowitz-Donaldson): An inlet starts if the throat area A_throat / A_capture exceeds the isentropic area ratio for the upstream Mach number. For a flush scoop with no variable throat:
- A_th / A₀ is fixed at the subsonic design value
- At M ≥ 1.0, the ratio is too small → **inlet cannot start**
- The shock stays outside → **unstarted inlet**

**Buzz characteristics at RC scale:**
- Frequency scales with duct length: f ≈ a / (4L) — for a ~0.5 m duct, f ≈ 170 Hz
- At 170 Hz with a 165 krpm compressor, the compressor sees ~55 pressure cycles per revolution
- This causes rapid blade fatigue and almost certain surge

**Conclusion: The flush chin scoop WILL unstart/buzz at Mach 1+. It is not viable for sustained supersonic flight.**

---

## 4. Alternative Intake Geometries

### Option A: Pitot-Type Intake (Sharp-Lipped, Axisymmetric or Semi-Circular)

```
     _____________
    /       ______\    ← sharp lip (0.1–0.5 mm radius)
   /       |       \
  |  DUMP | ENGINE |
   \      |_______/
    \______________/
```

**Advantages:**
- A sharp-lipped pitot inlet CAN start — the normal shock attaches to the lip
- At M ≤ 1.2: recovery > 99 %
- Simplest buildable supersonic inlet
- Proven: F-100, MiG-19, many supersonic missiles
- **Easily fabricated at RC scale**: 3D-printed duct with knife-edge lip

**Disadvantages:**
- Must be centerline or side-mounted (not ventral chin unless duct is S-duct)
- Spillage drag at off-design Mach numbers
- ADD (additive drag) from excess spillage

**RC-scale feasibility:** HIGH. A pitot scoop with sharp lip (≈0.2 mm radius) can be glassed or 3D-printed. The normal shock recovery at M ≤ 1.1 is nearly isentropic. **This is the recommended intake geometry.**

### Option B: 2-D Wedge / Ramp Inlet

```
      _____________
     /            / ← compression ramp (~10°)
    /   OBLIQUE  /
   /   SHOCK    /
  /____________/ ← cowl lip
```

**Advantages:**
- Better recovery if multiple ramps used (external compression)
- Lower spillage drag at design Mach
- Works up to M ~ 1.6–2.0 with two ramps

**Disadvantages:**
- Complex geometry — ramp angle, cowl lip position, throat area all critical
- Shock-on-lip condition is Mach-specific; off-design performance suffers
- Very difficult to fabricate at RC scale with required precision
- Boundary-layer bleed likely needed

**RC-scale feasibility:** LOW. The precision required for shock attachment and cowl lip alignment is beyond practical RC fabrication.

### Option C: Centerbody Spike (e.g., Concorde-style)

- Excellent recovery but mechanically complex
- No variable-spike mechanism at RC scale
- **Not buildable** at RC scale without an actuated spike

### Recommendation

| Geometry | Feasibility at RC Scale | M 1.0–1.1 Recovery | Build Complexity |
|----------|:----------------------:|:-------------------:|:----------------:|
| Flush chin scoop | **HIGH (easy build)** | **UNSTART — FAILS** | Low |
| Sharp-lipped pitot | **HIGH** | > 99.8 % | Low–Medium |
| 2-D wedge ramp | **LOW** | > 99 % (if tuned) | High |
| Centerbody spike | **VERY LOW** | > 99 % (if tuned) | Very High |

**Verdict: Convert to a sharp-lipped pitot intake. Side-mount or chin-mount with a gentle S-duct if centerline mounting is impossible.**

### On the P550-PRO Inlet Diameter

The P550-PRO has a bellmouth inlet diameter of roughly 45–50 mm. A pitot scoop sized at ~1.3× the engine inlet area (to allow for boundary-layer bleed and spillage) would be about **55–60 mm diameter** — trivially easy to fabricate.

---

## 5. Transonic Pitch-Up — Stabilator Authority

### The Problem

As the wing accelerates through Mach 1, the aerodynamic center shifts:

- **Subsonic:** AC at ~0.25 × MAC (quarter-chord)
- **Supersonic:** AC at ~0.50 × MAC (mid-chord for thin wings)
- **Shift:** ∆x_ac/c ≈ +0.25 (25 % of MAC aft)

For a 0.25 m MAC, the shift is **6.25 cm aft**.

### Trim Requirement

The aircraft must generate an increment of tail-down force to balance the new nose-down moment. Using the tail volume coefficient method:

- **C_m_ac** (wing alone pitching moment) ≈ -0.02 to -0.05 for thin, moderately cambered sections
- With the AC shift, the additional nose-down moment from lift is:  
  ∆M = L_wing × ∆x_ac = W × 0.0625 m

For a 55 kg aircraft: ∆M = 55 × 9.81 × 0.0625 = **33.7 N·m**

The tail must provide downforce: L_tail = ∆M / L_h = 33.7 / 1.10 = **30.6 N** downforce

### Stabilator Effectiveness at Supersonic Speeds

The all-moving stabilator's lift-curve slope at Mach 1 (supersonic thin-airfoil theory):

- dCl/dα ≈ 4 / √(M² − 1) for a 2D airfoil
- At M = 1.1: dCl/dα ≈ 4 / √(0.21) = **8.73 rad⁻¹**
- Finite-span correction (Prandtl-Glauert): Cl_α ≈ (Cl_α)₂D × (AR) / (AR + 2 × √(M² − 1))

For a stabilator with AR_tail ≈ 2.5:  
Cl_α_tail ≈ 8.73 × 2.5 / (2.5 + 2 × 0.458) = **6.42 rad⁻¹**

Required deflection for 30.6 N:  
α_needed = L_tail / (q × S_tail × Cl_α_tail) = 30.6 / (70,930 × 0.0341 × 6.42)  
= 30.6 / 15,530 = **0.00197 rad = 0.11°**

**That's tiny** — comfortably within the stabilator's range.

But wait — there are critical nuances:

1. **Transonic nonlinearity:** At M ≈ 0.95–1.05, mixed subsonic/supersonic flow on the wing creates large, nonlinear pitching moment changes (the "tuck" or "pitch-up pitch-down" phenomenon). The simple AC-shift model breaks down — actual trim requirements can be 3–5× larger in the transonic bucket.

2. **Downwash changes:** The wing's downwash field changes drastically across Mach 1, changing the effective α at the tail. This can reduce or increase the required deflection.

3. **Shock-induced separation on the tail:** If the tail operates in the wing's wake or at a high α, shock-induced separation can reduce effectiveness.

**Verdict:** The stabilator *area* is adequate for a smooth supersonic transition, but **special care is needed in the transonic regime (M 0.95–1.05)** where trim requirements can spike. A stability augmentation system (gyro) is essential for this regime.

---

## 6. Stabilator Sizing & Hinge Moments

### Sizing Summary

| Parameter | Value |
|-----------|-------|
| Wing area S_wing | 0.250 m² |
| MAC | 0.250 m |
| Tail moment arm L_h | 1.10 m |
| Tail volume coefficient V_h (supersonic) | 0.60 |
| **Required stabilator area S_h** | **0.0341 m²** |
| Stabilator span (partial, ~40 % fuselage width) | ~0.30 m |
| Stabilator chord | ~0.08–0.12 m |
| Aspect ratio of stabilator | ~2.5–3.75 |

### Hinge Moments at M 1.0

| Parameter | Value |
|-----------|-------|
| Dynamic pressure q | 70,930 Pa |
| Stabilator area S_h | 0.0341 m² |
| Mean chord | 0.08 m |
| Hinge moment coefficient C_h (all-moving, 5° deflection) | 0.03 |
| **Hinge moment** | **5.80 N·m** |
| In oz·in | **822 oz·in** |
| In kg·cm | **59.2 kg·cm** |
| **With 1.5× safety factor** | **89 kg·cm** |

### Servo Capability

| Servo Class | Torque | Suitable? |
|-------------|:------:|:---------:|
| Standard micro (e.g., HS-55) | 1.1 kg·cm | ❌ NO |
| Standard (e.g., HS-645MG) | 5–8 kg·cm | ❌ NO |
| High-torque (e.g., Hitec D645) | 15–25 kg·cm | ⚠️ MARGINAL |
| Giant-scale (e.g., Hitec D955TW) | 35–60 kg·cm | ✅ ADEQUATE (> 59 kg·cm) |
| Brushless HV (e.g., Savox 2290SG) | 70+ kg·cm | ✅✅ RECOMMENDED (C_h margin) |

**If mass-balancing weights are added forward of the hinge line** (which is necessary — see Section 8), the effective hinge moment increases by the product of weight × arm. The servo must overcome both aerodynamic and inertial moments, pushing the requirement toward the brushless HV class.

**Recommendation:** Dual brushless HV servos (> 80 kg·cm each) in a push-pull configuration, with a short, stiff pushrod in a carbon-fiber tube housing. Metal gears, titanium output shaft.

---

## 7. Lateral-Directional Stability

### Configuration Risk

- **Ventral fin only** — no dorsal fin
- Fin is "small" per the spec
- No wing-mounted servos (no ailerons? or servos in fuselage?)

### Directional Stability Derivative C_nβ

At supersonic speeds, vertical tail effectiveness drops:

C_nβ_tail = k × (S_v / S) × (L_v / b) × (Cl_α_v / Cl_α_wing)

At M 1.1: Cl_α_v ≈ 4 / √(M²−1) reduced by fin AR.

For a small ventral fin:
- S_v ≈ 0.5 × S_h ≈ 0.017 m² (small ventral)
- L_v / b ≈ 1.0 (fuselage-length fin)
- Cl_α_v ≈ 3.0 rad⁻¹ (AR ~ 1, supersonic correction)

C_nβ_tail ≈ 0.017/0.25 × 1.0 × (3.0/6.28) ≈ **0.032**

**Target C_nβ** for a stable aircraft: > 0.05 (positive).  
**Estimated:** 0.032 — **INSUFFICIENT.**

The aircraft will have:

- **Poor yaw stiffness** — tends to diverge in yaw after disturbance
- **Dutch roll** — poorly damped oscillation (yaw + roll coupling)
- **Adverse roll-yaw coupling** — roll inputs produce large yaw excursions
- **Spiral instability** possible at low angles of attack

### Mitigation — Gyro/Stabilization

**Is a gyro necessary?** YES — absolutely essential.

- A 3-axis gyro (yaw + pitch + roll) with rate stabilization is **non-negotiable** at Mach 1+
- The gyro must have bandwidth > 50 Hz (RC gyros like Cortex Pro, iGyro, or Aura AFCS)
- Yaw-axis specifically needs high gain to supplement the inadequate C_nβ
- Without gyro stabilization: the aircraft will likely depart controlled flight on the first yaw disturbance at M > 0.9

**Recommendation:** Install a high-performance 3-axis rate gyro with heading-hold (AVCS) mode for yaw. This enables safe flight despite the inadequate fin.

---

## 8. Control Surface Flutter — Mass Balancing Requirement

### Flutter Physics at M 1.0

At q = 71 kPa and Mach 1, the flutter speed V_f for a control surface is:

V_f ∝ √(G / ρ)

where G is the structural stiffness and ρ is air density. The key parameters:

| Factor | Impact |
|--------|--------|
| Dynamic pressure | 71 kPa — comparable to a full-scale fighter at Mach 1 at sea level |
| RC structure | **Much lower stiffness** per unit mass than full-scale metal |
| Backlash | Even 0.5° of pushrod slop can couple bending-torsion modes |
| Mass balance | **Critical** — must keep CG of control surface ahead of hinge line |

### All-Moving Stabilator Flutter Risk

The all-moving stabilator is susceptible to **body freedom flutter** (BFF), where the tail's pitch mode couples with the fuselage's bending mode. At RC scale:

- Fuselage bending frequency: ~10–20 Hz
- Stabilator pitch frequency: ~30–80 Hz (depending on servo stiffness and linkage)
- If frequencies converge → **divergent flutter**

### Requirements for Safe Operation

| Item | Requirement |
|------|-------------|
| Mass balance (stabilator) | CG of stabilator **ahead** of hinge line by ≥ 5 % chord |
| Mass balance (ventral fin rudder) | CG of rudder ahead of hinge line by ≥ 5 % chord |
| Pushrod stiffness | ≥ 3 mm diameter carbon rod, minimal free length |
| Pushrod end play | ≤ 0.1 mm total (use ball links with no slop) |
| Servo arm play | ≤ 0.5° at the servo output |
| Structural frequency separation | Stabilator pitch freq / fuselage bending freq ≥ 1.5 |

**Mass balancing weight estimates** (per stabilator half):

- Stabilator moment about hinge: m × x (where x is distance from CG to hinge)
- Counterweight: m_cw × r_cw ≥ m × x
- Typical: add 5–15 g of lead or tungsten at the leading edge, 20–30 mm ahead of the hinge

**Verdict on hobby servos at M1:** Even with proper mass balancing, hobby-class pushrods and servo gears are operating at their limit. Metal-geared, high-voltage servos with titanium output shafts are **mandatory**. Standard plastic-gear or nylon-gear servos will fail from flutter within seconds.

---

## 9. Launch Analysis

### Stall Speed

| Wing Loading | Stall Speed (CL_max=1.1) |
|:------------:|:------------------------:|
| **190 kg/m²** | **52.6 m/s** (189 km/h, 118 mph) |
| **220 kg/m²** | **56.6 m/s** (204 km/h, 127 mph) |
| **250 kg/m²** | **60.3 m/s** (217 km/h, 135 mph) |

These are **extremely high** stall speeds — comparable to a full-scale light jet. Most RC turbine jets have wing loadings of 40–80 kg/m² and stall at 30–50 m/s.

### Rail / Ramp Launch Requirements (W/S = 220 kg/m², 1.2× V_stall)

| Rail Length | Required Acceleration | G-Force | Launch Time | Launch Speed |
|:-----------:|:--------------------:|:-------:|:-----------:|:------------:|
| 3 m | 769 m/s² | **78 g** | 0.09 s | 245 km/h |
| 5 m | 461 m/s² | **47 g** | 0.15 s | 245 km/h |
| 10 m | 231 m/s² | **24 g** | 0.29 s | 245 km/h |
| 15 m | 154 m/s² | **16 g** | 0.44 s | 245 km/h |
| 20 m | 115 m/s² | **12 g** | 0.59 s | 245 km/h |

### P550-PRO Thrust-Weight Check

| Wing Loading | Mass | T/W | L/D needed for level M1 flight |
|:------------:|:----:|:---:|:----------------------------:|
| 190 kg/m² | 47.5 kg | **0.118** | **8.5** |
| 220 kg/m² | 55.0 kg | **0.102** | **9.8** |
| 250 kg/m² | 62.5 kg | **0.090** | **11.1** |

**Critical finding:** An L/D of 8.5–11.1 is required for level supersonic flight. At RC scale and Mach 1 (high wave drag), a realistic L/D is **4–6** for a clean design. **This means the P550-PRO does NOT produce enough thrust for level supersonic flight with the stated wing loading.** The aircraft would need a T/W of at least 0.2–0.25 for sustained M > 1.0.

### Practical Launch Strategy

Given the power deficiency, the only feasible supersonic flight profile is:

1. **Catapult or rail launch:** 10+ m rail with bungee/pneumatic/pyrotechnic catapult delivering ≥ 24 g
2. **Dive acceleration:** Gain speed in a dive from altitude
3. **Transient supersonic:** Brief Mach 1+ in a shallow dive with full throttle
4. **Cannot sustain** level supersonic flight

---

## 10. Summary & Verdict

### Verdict Table

| Component / System | Feasibility | Risk Level | Mitigation |
|-------------------|:-----------:|:----------:|------------|
| **1. Flush chin scoop at M 1+** | ❌ **NOT FEASIBLE** | **CRITICAL** | Unstart/buzz inevitable; engine will flame out |
| **2. P550-PRO tolerance** | ⚠️ Marginal with sharp-lipped pitot | HIGH | Only acceptable with started inlet + gyro-stabilized flow |
| **3. Inlet starting** | ❌ Flush scoop fails | **CRITICAL** | Must convert to pitot geometry |
| **4. Alternative intake (pitot)** | ✅ **FEASIBLE** | LOW | Sharp-lipped pitot, 55–60 mm dia, 3D-printable |
| **5. Stabilator for transonic trim** | ✅ Adequate area | MODERATE | Transient pitch-up in M 0.95–1.05 needs gyro augmentation |
| **6. Servo torque for stabilator** | ✅ With HV brushless servos | MODERATE | Need ≥ 80 kg·cm, metal gears, titanium shafts |
| **7. Lateral-directional stability** | ❌ **Insufficient fin** | **HIGH** | Mandatory 3-axis gyro; consider adding dorsal fin |
| **8. Control surface flutter** | ⚠️ Manageable with mass balancing | HIGH | Mandatory mass balance weights; stiff linkages; metal-gear servos |
| **9. Launch feasibility** | ⚠️ **Marginal** | HIGH | Stall speed 190+ km/h; T/W < 0.12; only transient supersonic |
| **10. Thrust-to-weight mismatch** | ❌ **Design contradiction** | **CRITICAL** | W/S = 190–250 kg/m² + P550-PRO cannot level-sustain M 1; needs 2× thrust or half the mass |

### Overall Verdict

> **The flush scoop intake is the clear primary blocker — it will not start, will buzz, and will cause the engine to flame out at Mach 1+. This must be replaced with a sharp-lipped pitot intake.**

> **The secondary blocker is the thrust-to-weight ratio.** With the stated wing loading of 190–250 kg/m², the P550-PRO cannot sustain level supersonic flight. The aircraft has a T/W of only 0.09–0.12, requiring an L/D of 8.5–11 at Mach 1 — unachievable for an RC-scale aircraft. Supersonic flight is only possible as a brief transient in a dive.

> **The tertiary issue is directional stability.** The small ventral fin alone provides inadequate C_nβ. A 3-axis gyro is mandatory, and adding a dorsal fin is strongly advised.

> **The controls are feasible but at the limits of hobby hardware:** HV brushless servos (80+ kg·cm) with mass-balanced surfaces, stiff high-quality linkages, and a high-bandwidth gyro can work.

> **Recommendation:** Before proceeding, resolve:
> 1. **Intake:** Sharp-lipped pitot (not flush scoop)
> 2. **Thrust:** Either reduce wing loading to ~100 kg/m² (half the mass) or use a larger engine (e.g., JetCat P800 or twin P550s)
> 3. **Stability:** Add a dorsal fin and a 3-axis gyro
> 4. **Structure:** Mass-balance all control surfaces; use only metal-gear, high-torque servos

---

*End of analysis. All calculations use standard compressible flow relations (γ = 1.4) and published normal-shock tables.*
