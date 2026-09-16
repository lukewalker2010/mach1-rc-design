# Aerodynamic Evaluation v2 — Preliminary Model

**Revised:** 2026-09-16 · **Owner:** E1 · **Status:** aerodynamic closure UNVERIFIED.
**Authority:** 18 §2/§3 contracts. This replaces the prior “closure verified”
interpretation, not the mission requirements. See 25 R03/R05/R06/R14.

## 1. Reproduce and interpret

```sh
python3 tools/aero_evaluation.py
python3 tools/structural_analysis.py
```

The empirical drag script uses a 185 mm × 2.60 m body, 0.14 m² wing, 30° sweep,
0.156 m MAC and 13.60 kg mass (18), a shape-factor **assumption** of 0.78 m²
body wetted area, flat-plate turbulent skin friction, a Sears–Haack-inspired
body term, hand-selected transonic factors, a clamped wing-wave model and
intake/base/excrescence allowances. These are not measured drag coefficients.

The shape is not a validated Sears–Haack body; the actual mould pinches to zero
radius. The area-rule pinch is absent from the model. Its omission does not prove
conservatism. Interference, inlet recovery/spillage, propulsion installation,
shock/boundary-layer interaction, trim drag and the actual manufactured geometry
need explicit treatment. The rib generator also uses a different root/area
convention (25 R03).

## 2. Model outputs (rounded, reproduced by the script)

| Mach | Drag at 3048 m, N | Drag at 3658 m, N |
|---|---:|---:|
| 1.00 | 301 | 280 |
| 1.05 | 338 | 314 |
| 1.10 | 385 | 358 |
| 1.20 | 563 | 523 |

The M1.05 estimate is below the **430 N contract**, but no uncertainty bound
justifies calling the difference a physical margin. The chosen sample M1.05
does not establish where the real transonic drag maximum lies. A constant
450–475 N thrust band must not be reused across Mach and altitude without a
matched engine/inlet/nozzle model and supporting test data.

The original static-bench conversion in 21 is conditional on unverified exhaust
velocity/mass-flow assumptions; it cannot establish flight thrust. Therefore
this model does **not** demonstrate sustained level Mach 1, nor any M1.20
“dive headroom”. M1.20 is outside the requested dash window, not a flight clearance.

## 3. Stability and trim

`tools/structural_analysis.py` reads the actual component rows in 18 §3.4:

| Fuel fraction | Mass kg | CG m | CG band 0.955–0.995 m |
|---|---:|---:|---|
| Full | 13.60 | 0.9748 | PASS arithmetic only |
| Half | 12.79 | 1.0080 | FAIL |
| Empty | 11.98 | 1.0458 | FAIL |

The old tail correction `NP = x_ac + 0.8(S_t/S_w)(x_tail−x_ac)` assumes an
unvalidated effective tail lift slope/downwash and a wing aerodynamic-centre
location. It is not a full-aircraft neutral-point solution. Aerodynamic-centre
position, sweep/MAC reference, tail area, lift-curve slopes, downwash, fuselage
contribution and Mach dependence must be established on matched geometry.

Even if that approximate NP were correct, it would **not** repair the independent
empty-fuel CG-band failure. High static margin alone is not proof of acceptable
trim, rotation or actuator authority. Keep these as separate acceptance items.

## 4. Low-speed and aeroelastic closure

At the required 30 m/s landing speed, full-mass required CL is **1.729** at
sea-level density (script `LANDING-LIFT`), before trim download. No validated
low-speed lift/drag polar demonstrates this. Resolve takeoff/approach/flare and
recovery geometry with the CG/control design before setting flight-test speeds.

Release requires geometry-consistent aerodynamic analysis with error bounds,
correlated measurements, control/trim load cases, and modal/flutter evidence.
G3/G4 flight observations supplement that work; absence of visible oscillation
does not establish flutter clearance. Neither conservative skin-friction
assumptions nor a green analysis script can substitute for those results.
