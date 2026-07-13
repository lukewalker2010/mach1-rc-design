# Mach 1 RC Plane — Aerodynamic Evaluation

**Evaluation date:** 2026-07-12  
**Role:** Aerodynamicist / design review  
**Configuration:** Area-ruled fuselage (Sears-Haack nose/tail), 60° swept biconvex wing, fineness ratio 10:1, 200mm dia. fuselage.

---

## 1. Sears-Haack Minimum Cd & Realistic Total

### Theoretical minimum (body only, wave drag)

Using linearized supersonic slender-body theory (Sears-Haack):

```
C_D_wave = (9π/2) · A_max / L² = (9π²/2) · (R_max/L)²

A_max = 0.03142 m²  (π × 0.1²)
L     = 2.0 m       (10:1 fineness)

C_D_wave = 0.1110   (based on frontal area)
```

**This is the absolute minimum possible wave drag** for a body of revolution with this fineness ratio and volume. Linearized theory gives Mach-independence for slender bodies; this value applies at M ≥ 1.05+.

### Complete drag buildup (frontal-area reference)

| Component | Cd (frontal ref) | Notes |
|---|---|---|
| Body — Sears-Haack wave | 0.1110 | Theoretical min |
| Body — skin friction | 0.0701 | Cf≈0.0024, Swet≈0.917 m² |
| Wing — wave (swept, subsonic LE) | 0.0074 | 3.8% t/c, 60° sweep, cos²Λ relief |
| Wing — skin friction | 0.0275 | Cf≈0.0039, Re_c=2.4×10⁶ |
| Tail (wave + friction) | 0.0101 | ~25% wing + friction |
| Intakes | 0.0100 | Typical supersonic intake |
| Excrescences/gaps | 0.0080 | RC scale proportionally worse |
| Base drag | 0.0050 | Conservative |
| Induced (CL=0.1) | 0.0014 | AR=9.1, e=0.85 |
| **TOTAL** | **0.2506** | |
| **Design target** | **0.1860** | |
| **Margin** | **−35%** | |

**The Cd target of 0.186 is not achievable based on first-principles drag buildup.** The bare body (wave + friction) already reaches Cd ≈ 0.181. The discrepancy arises because the spec appears to include only wave drag and underestimates skin friction, which is a dominant term at this scale.

### Equivalent wing-area-based Cd

- Computed: **Cd₀ = 0.0716** (wing-area ref, S=0.11m²)
- Target: **Cd₀ = 0.0531**
- F-104 Starfighter: Cd₀ ≈ 0.017 (much larger Re, thinner wings)
- Small supersonic missile: Cd₀ ≈ 0.03–0.08

The computed value sits at the high end of the missile range — plausible for a small supersonic vehicle.

---

## 2. Transonic Drag Rise

Conditions: 10,000 ft, ρ=0.905 kg/m³, a=328 m/s

| Mach | Cd (frontal ref) | Drag force | × Subsonic | Notes |
|---|---|---|---|---|
| 0.85 | 0.159 | 176 N (40 lbf) | 1.0× | Subsonic cruise |
| 0.95 | 0.160 | 221 N (50 lbf) | 1.0× | Drag rise begins |
| 1.00 | 0.202 | 309 N (70 lbf) | 1.3× | Transonic |
| **1.05** | **0.308** | **521 N (117 lbf)** | **1.9×** | **PEAK** |
| 1.10 | 0.289 | 536 N (120 lbf) | 1.8× | Decreasing |
| 1.20 | 0.251 | 553 N (124 lbf) | 1.6× | Fully supersonic |
| 1.50 | 0.221 | 762 N (171 lbf) | 1.4× | High Mach |

### Thrust requirement

The transonic drag hump peaks at **~520–550 N** sustained. Available RC propulsion:

| Powerplant | Max thrust | Feasible? |
|---|---|---|
| P-20 turbine | ~20 N | No |
| Large 127mm EDF (15S) | ~50 N | No |
| P-60 turbine | ~60 N | No |
| P-200 turbine (largest common) | ~200 N | No |
| **Required** | **~550 N** | — |

**The thrust required to transit Mach 1 in level flight exceeds any existing RC turbine by a factor of 2.5–3×.** Even at sea level (higher q), the drag is higher, not lower. This is the single biggest showstopper.

At lower altitudes the thrust requirement increases (higher dynamic pressure); at higher altitudes the engine thrust also drops. There is no altitude sweet spot that resolves this.

---

## 3. Biconvex Airfoil Structural Feasibility

### Geometry reconciliation

Given S=0.11 m², b=1.0 m:
- Streamwise mean chord = 110 mm
- Geometric chord (⊥ to LE, Λ=60°): c_geom = 110 / cos(60°) = **220 mm**
- Root geometric chord (×1.2 taper): **264 mm**
- Root max thickness @ 3.75% t/c: **9.9 mm**
- Tip max thickness: **6.2 mm**

**The spec claims "root thickness envelope 27–35 mm".** This is inconsistent with 3.5–4% t/c. For 27 mm thickness at 3.75% t/c, the chord would need to be **720 mm** — roughly 7× what the area/span give. Possible explanations:
1. "Thickness envelope" includes fuselage carry-through structure (not just airfoil)
2. The t/c or area/span numbers are wrong
3. It refers to the maximum thickness of fuselage + wing combined at the root

### Carbon spar feasibility

- Available spar depth (50% of max thickness): **4.9 mm**
- 3 mm carbon tube: ✓ fits
- 5 mm carbon rod: ✗ too large
- 8 mm spar: ✗

At Mach 1 loads (max weight ~27.5 kg, root bending moment ~34 N·m), a 4.9 mm deep unidirectional carbon spar sees ~826 MPa — **above typical carbon fiber strength (600 MPa)**. A multi-spar or thicker-section root design is required.

---

## 4. Reynolds Numbers

| Component | Chord/Length | Re at Mach 1, 10kft | Full-scale equivalent |
|---|---|---|---|
| Wing | 110 mm | **2.4×10⁶** | ~1.5×10⁷ (16%) |
| Fuselage | 2.0 m | **4.3×10⁷** | ~1–2×10⁸ (22–43%) |

### Implications

1. **Wing Re = 2.4×10⁶** → transitional regime (natural transition at ~21% chord). Mixed laminar/turbulent BL.
2. Turbulent Cf (0.0039) is **4.6× laminar Cf (0.0009)**. Laminar flow would help enormously, but surface imperfections at RC scale make natural laminar flow unlikely.
3. Shock/boundary layer interaction (SWBLI) is more severe at low Re — separation bubbles at shock foot, hysteresis, and off-design performance degradation are expected.
4. Linearized theory and high-Re CFD **overpredict performance** at this scale. Transition modeling and wind tunnel validation are essential.

---

## 5. Area Rule at RC Scale

### Boundary layer effects

- Physical BL thickness at fuselage midpoint: **12.6 mm** (12.6% of body radius)
- Displacement thickness δ*: **1.6 mm** (1.6% of radius)
- Full-scale comparison (Concorde): δ/R ≈ 1–2%

The BL is a significant fraction of the body radius at RC scale. The effective aerodynamic shape differs measurably from the geometric CAD model. **Area-rule optimization based on geometric cross-sections will overestimate drag reduction.**

### Surface quality

- RC panel gaps: 0.5–2.0 mm → 0.5–2.0% of R
- Full-scale aircraft gaps: ~0.01–0.1% of R
- RC imperfections are **10–50× larger proportionally** than full-scale

**Estimated: 50–70% of theoretical area-rule benefit is achievable** at RC scale with CNC-machined molds and seamless construction. Standard build techniques (glass/carbon wet layup with panel gaps) will achieve substantially less.

---

## 6. 60° Sweep + Biconvex Wave Drag

### Sweep effectiveness

| Mach | M_n = M·cos60° | LE type | Cd_swept/Cd_unswept |
|---|---|---|---|
| 0.95 | 0.475 | Subsonic | N/A (no wave drag) |
| 1.00 | 0.500 | Subsonic | N/A |
| 1.05 | 0.525 | Subsonic | 0.19× |
| 1.10 | 0.550 | Subsonic | 0.19× |
| 1.20 | 0.600 | Subsonic | 0.19× |
| 1.50 | 0.750 | Subsonic | 0.19× |

- **Subsonic leading edge is maintained up to M ≈ 1.7** (M_n=0.85 for 60° sweep)
- Wave drag reduction from sweep: **~5.3×** (cos²Λ = 0.25, plus β benefits)
- 60° is generous for this Mach range — could be relaxed slightly for structural benefit

### 2D biconvex section wave drag

- Unswept: Cd_wave ≈ 0.011 (wing-area ref at M=1.2)
- Swept 60°: Cd_wave ≈ 0.002 (wing-area ref)
- Wing wave drag contribution to total (frontal-area ref): ~0.007

**The wing wave drag is well-managed by the sweep. This is the best element of the design.**

---

## 7. Overall Verdict

```
─────────────────────────────────────────────────────
                    FINAL ASSESSMENT
─────────────────────────────────────────────────────

  Sears-Haack body (wave only):      0.1110
  Realistic total Cd (frontal ref):  0.2506
  Design target:                     0.1860
  Margin:                            −34.8%

  Equivalent Cd (wing-area ref):     0.0716
  Target (wing-area ref):            0.0531

  Drag @ M=1.2, 10kft:            553 N (124 lbf)
  Peak transonic drag:             ~550 N (120 lbf)
  Largest RC turbine available:    ~200 N

  Root envelope consistency:       INCONSISTENT
  Spar depth at root:              4.9 mm
  Wing Re:                         2.4×10⁶
─────────────────────────────────────────────────────
```

### The Cd target of 0.186 is NOT FEASIBLE as specified.

**Critical blockers (in order of severity):**

1. **🔴 THRUST (showstopper):** ~550 N required through transonic. Largest common RC turbine produces ~200 N. No current propulsion system can do this. This is not a marginal shortfall — it's a factor of 2.5–3×.

2. **🔴 AIRFOIL INCONSISTENCY:** The stated 27–35 mm root thickness envelope does not reconcile with 3.5–4% t/c at the implied chord. The actual max thickness is ~10 mm. Something in the spec is wrong or misinterpreted.

3. **🟡 LOW-RE SUPERSONIC:** Wing Re = 2.4×10⁶ differs fundamentally from full-scale supersonic. SWBLI, transition, and separation behavior are different. Standard drag prediction methods overestimate performance.

4. **🟡 AREA RULE BENEFIT REDUCED:** BL thickness (12.6% of body radius) and proportionally large surface imperfections (~50× full-scale) reduce the theoretical drag benefit of area ruling. Estimate: 50–70% of theoretical benefit achievable.

5. **🟢 SWEEP:** 60° sweep provides subsonic LE through M ≈ 1.7. Wave drag reduction from sweep is ~5×. Sound design choice.

### Recommendations

| Priority | Action |
|---|---|
| **Must** | Triple-check the Cd reference area convention. If Cd=0.186 is referenced to wing area, it becomes ~0.053 — which is ambitious but not impossible. |
| **Must** | Resolve the 27–35 mm root thickness vs 3.5–4% t/c discrepancy. |
| **Must** | Re-think propulsion. Level-flight Mach 1 is not feasible with current RC turbines at this scale. Options: (a) dive-assist / zoom climb, (b) dual turbines, (c) rocket boost, (d) reduce scale/lower drag, (e) limit to Mach ~0.92–0.95 transonic. |
| **Should** | Increase target Cd to ~0.25 (frontal ref) or equivalently ~0.072 (wing ref) for a realistic design target. |
| **Should** | Plan for CNC-machined molds with seamless surfaces if area ruling is to provide any benefit. |
| **Should** | Perform CFD with low-Re transition modeling (γ–Rẽθt or SST with transition). Do not rely on fully turbulent RANS or Euler methods. |

---

*Report prepared using Sears-Haack slender-body theory, linearized supersonic airfoil theory, Korn-equation transonic drag model, flat-plate skin friction (Prandtl-Schlichting), and empirical sweep theory.*
