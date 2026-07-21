# Stabilator Manufacturing Package

## 1. Overview

The stabilator is an all-moving tail surface with differential (taileron) control. Each half is a solid carbon laminate — too thin for foam-core sandwich construction.

| Parameter | Value |
|-----------|-------|
| Total span | 240 mm (120 mm per side) |
| Root chord | 35 mm |
| Tip chord | 15 mm |
| Airfoil | Biconvex 3.5% |
| Material | T300 carbon-epoxy prepreg [0/±45/0] |
| Laminate thickness | 0.4 mm (4 plies × 0.1 mm) |
| Spar | 2 mm carbon rod at 30% chord |
| Target mass | 55 g (both sides + hardware + servos) |

---

## 2. Biconvex Airfoil Coordinates

### 2.1 Root Section (C = 35 mm, t = 1.225 mm)

Formula: `y(x) = (t/2) × (4 × x/C × (1 − x/C))`

| x/C | x (mm) | y_upper (mm) | y_lower (mm) |
|-----|--------|-------------|-------------|
| 0.00 | 0.000 | 0.000 | 0.000 |
| 0.05 | 1.750 | 0.291 | −0.291 |
| 0.10 | 3.500 | 0.551 | −0.551 |
| 0.20 | 7.000 | 0.980 | −0.980 |
| 0.30 | 10.500 | 1.225 | −1.225 |
| 0.40 | 14.000 | 1.225 | −1.225 |
| 0.50 | 17.500 | 1.225 | −1.225 |
| 0.60 | 21.000 | 1.176 | −1.176 |
| 0.70 | 24.500 | 1.029 | −1.029 |
| 0.80 | 28.000 | 0.784 | −0.784 |
| 0.90 | 31.500 | 0.441 | −0.441 |
| 0.95 | 33.250 | 0.232 | −0.232 |
| 1.00 | 35.000 | 0.000 | 0.000 |

### 2.2 Tip Section (C = 15 mm, t = 0.525 mm)

Scaled by factor 15/35 = 0.4286 from root.

| x/C | x (mm) | y_upper (mm) | y_lower (mm) |
|-----|--------|-------------|-------------|
| 0.00 | 0.000 | 0.000 | 0.000 |
| 0.10 | 1.500 | 0.236 | −0.236 |
| 0.20 | 3.000 | 0.420 | −0.420 |
| 0.30 | 4.500 | 0.525 | −0.525 |
| 0.40 | 6.000 | 0.525 | −0.525 |
| 0.50 | 7.500 | 0.525 | −0.525 |
| 0.60 | 9.000 | 0.504 | −0.504 |
| 0.70 | 10.500 | 0.441 | −0.441 |
| 0.80 | 12.000 | 0.336 | −0.336 |
| 0.90 | 13.500 | 0.189 | −0.189 |
| 1.00 | 15.000 | 0.000 | 0.000 |

### 2.3 Intermediate Sections

At any span station z (0 ≤ z ≤ 120 mm):

```
C(z) = 35 − (35 − 15) × z/120 = 35 − 0.1667z  mm
t(z) = 1.225 × (1 − 0.4762 × z/120)  mm
```

| z (mm) | C (mm) | t (mm) | t/2 (mm) |
|--------|--------|--------|---------|
| 0 (root) | 35.0 | 1.225 | 0.613 |
| 20 | 31.7 | 1.123 | 0.561 |
| 40 | 28.3 | 1.021 | 0.510 |
| 60 | 25.0 | 0.919 | 0.460 |
| 80 | 21.7 | 0.817 | 0.408 |
| 100 | 18.3 | 0.715 | 0.357 |
| 120 (tip) | 15.0 | 0.525 | 0.263 |

---

## 3. Mould Design

### 3.1 Mould Type

**CNC-machined aluminium male + female mould halves**, matching the stabilator planform and airfoil.

### 3.2 Mould Dimensions

| Dimension | Value |
|-----------|-------|
| Length (chordwise) | 45 mm (35 mm root + 10 mm margin) |
| Width (spanwise) | 130 mm (120 mm + 10 mm margin) |
| Height (each half) | 8 mm |
| Material | 6061-T6 aluminium |
| Surface finish | 0.2 μm Ra |

### 3.3 Mould Features

- Spar rod locating groove: 2.0 mm wide × 1.0 mm deep at 30% chord
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
- Spar rod: 2 mm × 110 mm pultruded carbon, scarf-bevel last 15 mm

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
| Spar rod (per side) | 2 | 0.55 | 1.1 |
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
| **Total** | | | **55.1 g** |

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
