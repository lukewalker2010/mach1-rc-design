# Stabilator Manufacturing Package

## 1. Overview

The stabilator is an all-moving tail surface with differential (taileron) control. Each half is a solid carbon laminate — too thin for foam-core sandwich construction.

| Parameter | Value |
|-----------|-------|
| Total span | 240 mm (120 mm per side) |
| Root chord | 90 mm |
| Tip chord | 38.6 mm |
| Taper ratio | 0.429 (C_tip/C_root, preserved from design) |
| Airfoil | Biconvex 6% |
| Max thickness (root) | 5.4 mm (6% of 90 mm) |
| Material | T300 carbon-epoxy prepreg [0/±45/0] |
| Laminate thickness | 0.4 mm (4 plies × 0.1 mm) |
| Spar | 2.5 mm Ti-6Al-4V rod at 30% chord |
| Target mass | 55 g (both sides + hardware + servos) |

---

## 2. Biconvex Airfoil Coordinates

### 2.1 Root Section (C = 90 mm, t = 5.400 mm)

Formula: `y(x) = (t/2) × (4 × x/C × (1 − x/C))`

**Max thickness at x/C = 0.50** (corrected — the biconvex parabola peaks at mid-chord, not at 0.30). 21 stations (5% steps), consistent with `STA_ROOT.dxf`.

| x/C | x (mm) | y_upper (mm) | y_lower (mm) |
|-----|--------|-------------|-------------|
| 0.00 | 0.000 | 0.000 | 0.000 |
| 0.05 | 4.500 | 0.513 | −0.513 |
| 0.10 | 9.000 | 0.972 | −0.972 |
| 0.15 | 13.500 | 1.377 | −1.377 |
| 0.20 | 18.000 | 1.728 | −1.728 |
| 0.25 | 22.500 | 2.025 | −2.025 |
| 0.30 | 27.000 | 2.268 | −2.268 |
| 0.35 | 31.500 | 2.457 | −2.457 |
| 0.40 | 36.000 | 2.592 | −2.592 |
| 0.45 | 40.500 | 2.673 | −2.673 |
| 0.50 | 45.000 | 2.700 | −2.700 |
| 0.55 | 49.500 | 2.673 | −2.673 |
| 0.60 | 54.000 | 2.592 | −2.592 |
| 0.65 | 58.500 | 2.457 | −2.457 |
| 0.70 | 63.000 | 2.268 | −2.268 |
| 0.75 | 67.500 | 2.025 | −2.025 |
| 0.80 | 72.000 | 1.728 | −1.728 |
| 0.85 | 76.500 | 1.377 | −1.377 |
| 0.90 | 81.000 | 0.972 | −0.972 |
| 0.95 | 85.500 | 0.513 | −0.513 |
| 1.00 | 90.000 | 0.000 | 0.000 |

### 2.2 Tip Section (C = 38.6 mm, t = 2.314 mm)

Scaled by factor 38.571/90 = 0.4286 from root (taper ratio 0.429). 21 stations, consistent with `STA_TIP.dxf`.

| x/C | x (mm) | y_upper (mm) | y_lower (mm) |
|-----|--------|-------------|-------------|
| 0.00 | 0.000 | 0.000 | 0.000 |
| 0.05 | 1.929 | 0.220 | −0.220 |
| 0.10 | 3.857 | 0.417 | −0.417 |
| 0.15 | 5.786 | 0.590 | −0.590 |
| 0.20 | 7.714 | 0.741 | −0.741 |
| 0.25 | 9.643 | 0.868 | −0.868 |
| 0.30 | 11.571 | 0.972 | −0.972 |
| 0.35 | 13.500 | 1.053 | −1.053 |
| 0.40 | 15.429 | 1.111 | −1.111 |
| 0.45 | 17.357 | 1.146 | −1.146 |
| 0.50 | 19.286 | 1.157 | −1.157 |
| 0.55 | 21.214 | 1.146 | −1.146 |
| 0.60 | 23.143 | 1.111 | −1.111 |
| 0.65 | 25.071 | 1.053 | −1.053 |
| 0.70 | 27.000 | 0.972 | −0.972 |
| 0.75 | 28.929 | 0.868 | −0.868 |
| 0.80 | 30.857 | 0.741 | −0.741 |
| 0.85 | 32.786 | 0.590 | −0.590 |
| 0.90 | 34.714 | 0.417 | −0.417 |
| 0.95 | 36.643 | 0.220 | −0.220 |
| 1.00 | 38.571 | 0.000 | 0.000 |

### 2.3 Intermediate Sections

At any span station z (0 ≤ z ≤ 120 mm):

```
C(z) = 90 − (90 − 38.571) × z/120 = 90 − 0.428571z  mm
t(z) = 0.06 × C(z) = 5.400 − 0.025714z  mm        (t/c constant = 6%)
```

> **Corrected (D22):** the former `t(z) = 1.225 × (1 − 0.4762 × z/120)` did not reproduce the tip — it gave t(120) = 0.642 mm against a 0.525 mm tip. The corrected interpolation scales thickness with chord (constant 6% t/c), so t(120) = 0.06 × 38.571 = 2.314 mm, exactly the tip section. Mid-station (`STA_MID`, z = 60 mm) is generated from this formula with consistent x/y scaling.

| z (mm) | C (mm) | t (mm) | t/2 (mm) |
|--------|--------|--------|---------|
| 0 (root) | 90.0 | 5.400 | 2.700 |
| 20 | 81.4 | 4.886 | 2.443 |
| 40 | 72.9 | 4.371 | 2.186 |
| 60 | 64.3 | 3.857 | 1.929 |
| 80 | 55.7 | 3.343 | 1.671 |
| 100 | 47.1 | 2.829 | 1.414 |
| 120 (tip) | 38.6 | 2.314 | 1.157 |

---

## 3. Mould Design

### 3.1 Mould Type

**CNC-machined aluminium male + female mould halves**, matching the stabilator planform and airfoil.

### 3.2 Mould Dimensions

| Dimension | Value |
|-----------|-------|
| Length (chordwise) | 100 mm (90 mm root + 10 mm margin) |
| Width (spanwise) | 130 mm (120 mm + 10 mm margin) |
| Height (each half) | 8 mm |
| Material | 6061-T6 aluminium |
| Surface finish | 0.2 μm Ra |

### 3.3 Mould Features

- Spar rod locating groove: 2.5 mm wide × 1.25 mm deep at 30% chord (Ti 2.5 mm spar)
- Bearing pocket inserts: ∅8.2 mm × 3.2 mm deep at z = 30 mm and z = 72 mm
- Parting line: midplane (y = 0)

### 3.4 CNC Machining Sequence

1. Face block to 45 × 130 × 8 mm
2. Rough contour: 3 mm ball-nose, 0.3 mm stepover
3. Finish contour: 1.5 mm ball-nose, 0.15 mm stepover
4. Machine spar groove
5. Machine bearing pockets
6. Polish to 0.2 μm Ra
7. Hard anodise (Type III, 25 μm)
8. PTFE dry-film coat

**Estimated CNC time:** 2–3 hours per half

---

## 4. Layup Procedure

### 4.1 Material Prep

- Cut 4 plies per side from T300 prepreg (0.1 mm cured thickness)
- Ply shape: trapezoid matching planform + 10 mm trim allowance
- Spar rod: 2.5 mm × 110 mm Ti-6Al-4V rod, scarf-bevel last 15 mm

### 4.2 Layup Sequence (per side)

1. Apply release agent to both mould halves
2. Lay Ply 1 (0°) in female mould
3. Lay Ply 2 (+45°)
4. Lay Ply 3 (−45°)
5. Lay Ply 4 (0°)
6. Place spar rod in groove at 30% chord
7. Embed bearing inserts in pockets (pre-coated with Hysol 9460)
8. Close male mould on top
9. Vacuum bag: −0.9 bar minimum
10. Cure: 135 °C, 6 bar pressure, 90 minutes (autoclave)
11. Cool to 60 °C at −3 °C/min, vent pressure

### 4.3 Post-Cure

1. Remove from mould
2. Trim to net profile (diamond waterjet or carbide router)
3. LE radius: 0.3 mm (profile sander)
4. TE taper: 0.1 mm ± 0.05 mm
5. Seal edges with thin CA glue
6. Optional: post-cure at 175 °C for 2 hours (if Tg needs boost)

---

## 5. Bearing Installation

### 5.1 Bearing Specification

| Feature | Value |
|---------|-------|
| Type | Deep groove ball bearing, 2RS (rubber sealed) |
| Size | 4 mm ID × 8 mm OD × 3 mm width |
| Material | 440C stainless steel |
| Qty | 4 (2 per side) |

### 5.2 Installation Procedure

1. Clean bearing pockets with isopropyl alcohol
2. Apply Hysol 9460 to pocket walls
3. Press bearings into pockets (interference fit)
4. Verify bore alignment: insert 4 mm pin, check free rotation
5. Cure 24 hours at RT

---

## 6. Control Horn Installation

### 6.1 Horn Fabrication

- Material: G10/FR4, 1.5 mm thick
- Cut to shape: 10 × 15 mm L-bracket
- Drill 2 × M2 mounting holes (through stabilator root)
- Drill 1 × M2 ball link hole (10 mm above hinge line)

### 6.2 Installation

1. Drill 2 × M2 holes through stabilator root at 30% chord
2. Bolt horn to root with M2 × 10 mm bolts + backing plate
3. Apply nylon lock nuts
4. Attach ball link with M2 bolt + nylon lock nut

---

## 7. Assembly Sequence

```
Step 1: Lay up + cure stabilator halves (LH, RH)
    │
Step 2: Trim to net profile
    │
Step 3: Bond bearings into pockets
    │
Step 4: Fabricate + bolt control horns
    │
Step 5: Fabricate fuselage brackets (CNC 7075-T6)
    │
Step 6: Install brackets on fuselage
    │
Step 7: Slide stabilators into brackets
    │
Step 8: Insert hinge pins (4 mm × 15 mm steel)
    │
Step 9: Secure pins with E-clips
    │
Step 10: Fabricate pushrod assemblies
    │
Step 11: Connect pushrods (servo → control horn)
    │
Step 12: Install servos on mounting plate
    │
Step 13: Set servo centre, verify ±25° deflection
```

---

## 8. Weight Budget

| Component | Qty | Unit (g) | Total (g) |
|-----------|-----|---------|-----------|
| Stabilator laminate (per side) | 2 | 2.5 | 5.0 |
| Ti spar (2.5 mm, per side) | 2 | 2.4 | 4.8 |
| Epoxy fill | 2 | 0.5 | 1.0 |
| Bearings (4×8×3) | 4 | 1.0 | 4.0 |
| Control horn (G10) | 2 | 0.8 | 1.6 |
| Horn hardware | 2 | 0.4 | 0.8 |
| KST X20-12T servos | 2 | 10.5 | 21.0 |
| Servo mounting plate | 1 | 5.0 | 5.0 |
| Rubber grommets | 4 | 0.2 | 0.8 |
| Servo screws | 8 | 0.1 | 0.8 |
| Pushrod assemblies | 2 | 0.95 | 1.9 |
| Fuselage brackets | 4 | 1.2 | 4.8 |
| Hinge pins (steel) | 4 | 1.5 | 6.0 |
| E-clips | 4 | 0.03 | 0.12 |
| Bracket screws | 8 | 0.15 | 1.2 |
| **Total** | | | **58.8 g** |

> Note: spar row updated for the 2.5 mm Ti-6Al-4V spar (density 4.43 g/cm³, ~2.4 g each); remaining rows are unchanged estimates.

---

## 9. Quality Acceptance

| Feature | Tolerance | Method |
|---------|-----------|--------|
| Planform dimensions | ±0.5 mm | Caliper |
| Airfoil profile | ±0.05 mm | Profile gauge |
| LE radius | ±0.1 mm | Radius gauge |
| TE thickness | 0.1 ±0.05 mm | Micrometer |
| Bearing bore alignment | ≤0.1 mm TIR | Pin gauge + dial indicator |
| Hinge friction | ≤0.05 N·m | Torque wrench |
| Deflection range | ±25° without binding | Visual |
| Surface finish | Ra ≤ 0.8 μm | Profilometer |
