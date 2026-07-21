# Wing Skin Layup Schedule — Detailed Manufacturing Instructions

## 1. Overview

The wing skins are carbon-epoxy prepreg, vacuum-bagged and cured on the male mould. Two distinct layup zones:

| Zone | Span | Thickness | Layup | Plies |
|------|------|-----------|-------|-------|
| Inner panel | 0–200 mm | 0.8 mm | [0/±45/0] | 4 |
| Outer panel | 200–450 mm | 0.6 mm | [0/±45] | 3 |

Each wing half requires one inner skin and one outer skin. Total: 4 skins per wing (2 inner + 2 outer).

---

## 2. Material Specification

### 2.1 Prepreg

| Property | Value |
|----------|-------|
| Material | Toray T300/2510 or T700/2510 carbon-epoxy prepreg |
| Areal weight | 150 g/m² per ply |
| Resin content | 35 ± 3% |
| Nominal cured ply thickness | 0.20 mm |
| Cure temperature | 120 °C (250 °F) |
| Cure pressure | 6 bar (85 psi) min, vacuum bag |
| Out-life | 21 days at 21 °C / 50% RH |
| Freeze life | 6 months at −18 °C |

### 2.2 Alternative: Wet Layup

If prepreg is unavailable:

| Property | Value |
|----------|-------|
| Fabric | T300 or T700 plain weave, 200 g/m² |
| Resin | West System 105/206 or MGS L285/H287 |
| Layup | Wet layup with squeegee, vacuum bag |
| Cure | RT 24h, then 60 °C post-cure 4h |
| Ply thickness | 0.22–0.25 mm (wet, varies with consolidation) |

**Note:** Wet layup adds ~10% weight and reduces fibre volume fraction to ~50% vs 60% for prepreg.

---

## 3. Inner Panel Layup [0/±45/0] — 4 Plies

### 3.1 Ply Schedule

| Ply | Orientation | Material | Width (root) | Width (200mm) | Length | Notes |
|-----|-------------|----------|-------------|--------------|--------|-------|
| 1 (bottom) | 0° | T300 UD tape | 211 mm | 127 mm | 200 mm | Spanwise, first ply on mould |
| 2 | +45° | T300 UD tape | 298 mm | 179 mm | 282 mm | Diagonal, trimmed |
| 3 | −45° | T300 UD tape | 298 mm | 179 mm | 282 mm | Diagonal, trimmed |
| 4 (top) | 0° | T300 UD tape | 211 mm | 127 mm | 200 mm | Spanwise, outermost ply |

### 3.2 Ply Cutting Dimensions

**Ply 1 — 0° (bottom):**
- Shape: Trapezoid matching inner panel planform
- Root edge: 211 mm (full root chord)
- 200 mm station edge: 127 mm
- LE edge: straight line from (0,0) to (0,200)
- TE edge: straight line from (211,0) to (127,200)
- Add 10 mm trim allowance on all edges
- Cut from roll: 221 mm wide × 210 mm long

**Ply 2 — +45°:**
- Shape: Same trapezoid rotated 45°
- Cut diagonal strip: width = 211/cos(45°) = 298 mm
- Length = 200/cos(45°) = 282 mm
- Position: centre on planform, trim excess

**Ply 3 — −45°:**
- Same as Ply 2, mirrored

**Ply 4 — 0° (top):**
- Same as Ply 1

### 3.3 Fibre Orientation Diagram

```
          PLANFORM VIEW — Inner Panel (0-200 mm span)
          
    LE edge                            TE edge
    │                                     │
    │  Ply 1 (0°)  ═══════════════════►  │  Spanwise fibres
    │  Ply 2 (+45) ╲ ╲ ╲ ╲ ╲ ╲ ╲ ╲ ╲   │  +45° to span
    │  Ply 3 (−45) ╱ ╱ ╱ ╱ ╱ ╱ ╱ ╱ ╱   │  −45° to span
    │  Ply 4 (0°)  ═══════════════════►  │  Spanwise fibres
    │                                     │
    ▼ Root                           200mm ▼
```

---

## 4. Outer Panel Layup [0/±45] — 3 Plies

### 4.1 Ply Schedule

| Ply | Orientation | Material | Width (200mm) | Width (tip) | Length | Notes |
|-----|-------------|----------|--------------|------------|--------|-------|
| 1 (bottom) | 0° | T300 UD tape | 127 mm | 0 mm | 250 mm | Spanwise |
| 2 | +45° | T300 UD tape | 179 mm | 0 mm | 353 mm | Diagonal |
| 3 (top) | −45° | T300 UD tape | 179 mm | 0 mm | 353 mm | Diagonal |

### 4.2 Ply Cutting Dimensions

**Ply 1 — 0° (bottom):**
- Triangle (delta planform)
- Root edge (200 mm station): 127 mm
- Tip: point
- LE edge: straight line
- TE edge: straight line
- Add 10 mm trim allowance
- Cut from roll: 137 mm wide × 260 mm long

**Ply 2 — +45°:**
- Cut diagonal strip: 179 mm wide × 353 mm long
- Position on planform, trim excess

**Ply 3 — −45°:**
- Same as Ply 2, mirrored

---

## 5. Layup Procedure — Step by Step

### 5.1 Preparation

1. **Mould prep:** Clean mould with acetone, apply release agent schedule (wax ×3, PVA ×1, Frekote ×2)
2. **Material prep:** Remove prepreg from freezer, allow to equilibrate to room temperature for 1 hour (keep in sealed bag until ready)
3. **Cut plies:** Cut all plies per dimensions above, label each ply
4. **Mark mould:** Scribe spar line at 30% chord, mark span stations with fine-tip marker

### 5.2 Layup Sequence

**For each skin (inner or outer):**

**Step 1 — Peel ply**
- Drape peel ply over mould surface
- Smooth from centre outward, remove wrinkles
- Trim to planform + 15 mm

**Step 2 — Ply 1 (0°, bottom)**
- Remove backing paper from prepreg
- Position on mould, align LE edge with mould LE
- Smooth from centre outward with plastic squeegee
- Press firmly along spar line to ensure contact
- No air bubbles — work from centre to edges

**Step 3 — Ply 2 (+45°)**
- Position at +45° to span axis
- Overlap onto Ply 1 by full width
- Smooth from centre outward
- Ensure fibre alignment is consistent

**Step 4 — Ply 3 (−45°)**
- Position at −45° to span axis
- Smooth from centre outward

**Step 5 — Ply 4 (0°, top) — inner panel only**
- Position on top of Ply 3
- Smooth from centre outward
- Final surface ply — ensure no wrinkles

**Step 6 — Spar rod placement**
- Lay 5.0 mm T800 carbon rod in spar channel at 30% chord
- Rod extends full span (0–450 mm for each wing half)
- Rod potted in structural epoxy at root (Hysol EA 9394)

**Step 7 — Release film + breather**
- Apply perforated FEP release film over layup
- Apply 2 layers of breather cloth
- Ensure breather extends to vacuum connection point

**Step 8 — Vacuum bag**
- Seal vacuum bag with sealant tape
- Connect vacuum fitting
- Pull vacuum to −0.9 bar minimum
- Check for leaks (hold vacuum for 5 minutes)

### 5.3 Cure

| Step | Temperature | Time | Notes |
|------|------------|------|-------|
| Ramp | RT → 120 °C | 60 min | 2 °C/min max |
| Hold | 120 °C | 120 min | Full vacuum maintained |
| Cool | 120 °C → RT | 90 min | ≤3 °C/min |
| Post-cure (optional) | RT → 150 °C → RT | 60 min hold | Improves Tg by ~15 °C |

### 5.4 Demould

1. Release vacuum
2. Remove bag, breather, release film
3. Carefully peel skin from mould (use plastic wedge at LE)
4. Inspect surface — should be smooth, Ra ≤ 1.6 μm
5. Trim to final planform dimensions:
   - Inner panel: 211 × 200 mm (root × span)
   - Outer panel: 127 × 250 mm (200mm station × span)

---

## 6. Spar Integration

### 6.1 Spar Rod Specification

| Property | Value |
|----------|-------|
| Material | Toray T800 pultruded carbon rod |
| Diameter | 5.00 mm ±0.05 mm |
| Length | 920 mm (460 mm per half, full span) |
| Tensile modulus | 294 GPa |
| Tensile strength | 5,520 MPa |
| Density | 1.60 g/cm³ |
| Mass per metre | 31.4 g/m |

### 6.2 Spar Routing Through Ribs

- Each rib has a 5.5 mm hole at 30% chord
- Spar slides through all 6 ribs (R0–R5)
- At root (R0), spar is potted in aluminium ferrule:
  - Ferrule: 8 mm OD × 6 mm ID × 20 mm long
  - Pot with Hysol EA 9394 structural epoxy
  - Ferrule bolts to carry-through box via M6 bolts

### 6.3 Spar-to-Skin Bond

- Spar sits in mould channel during layup
- 0° plies (Ply 1 and Ply 4) bond directly to spar surface
- Ensure spar is centred in channel (±0.2 mm)

---

## 7. Rib Installation

### 7.1 Rib Preparation

1. Cut foam cores from ROHACELL 71 HF using CNC hot-wire
2. Lay up 0.5 mm carbon web on each face (2 plies of 0.25 mm UD carbon)
3. Cure at RT with vacuum bag (12 hours minimum)
4. Drill spar hole: 5.5 mm at 30% chord
5. Trim web flanges to 3 mm

### 7.2 Rib-to-Skin Bond

1. Apply Araldite 420 A/B epoxy paste to rib web flanges (3 mm wide)
2. Position rib on inner skin at correct span station
3. Press firmly, ensure contact along full flange
4. Allow to cure 24 hours at RT before handling
5. Repeat for all 6 ribs per half

### 7.3 Assembly Sequence

```
Step 1: Bond all 6 ribs to inner skin
            │
Step 2: Slide spar through rib holes
            │
Step 3: Pot spar in root ferrule
            │
Step 4: Bond outer skin on top of ribs
            │
Step 5: Bond leading edge closeout strip (if needed)
            │
Step 6: Attach wing to fuselage carry-through
            │
Step 7: Torque M6 bolts to 12 N·m
```

---

## 8. Ply Drop-Off Detail (200 mm Junction)

### 8.1 Transition Zone

```
    INNER PANEL              OUTER PANEL
    [0/±45/0]                [0/±45]
    
    0° ───────────────────► 0°  (terminates at 195mm)
    +45° ╲ ╲ ╲ ╲ ╲ ╲ ╲ ╲ ╲ +45° ╲ ╲ ╲ ╲ ╲ ╲ ╲ (continuous)
    −45° ╱ ╱ ╱ ╱ ╱ ╱ ╱ ╱ ╱ −45° ╱ ╱ ╱ ╱ ╱ ╱ ╱ (continuous)
    0° ────────────────────  (absent — 3-ply outer)
    
    │◄──── 5mm overlap ────►│
    │         zone          │
    195mm   200mm   205mm
```

### 8.2 Transition Procedure

1. Inner panel: terminate inner 0° ply (Ply 1) at 195 mm station
2. Outer panel: start outer 0° ply (Ply 1) at 205 mm station
3. ±45° plies are continuous across the junction
4. Fill 0.2 mm step with epoxy microballoon fairing compound
5. Sand flush after cure

---

## 9. Leading Edge Closeout

### 9.1 Option A: Folded Skin

- Inner and outer skins meet at LE
- 3 mm overlap, bonded with Hysol EA 9394
- Sand to biconvex profile after cure

### 9.2 Option B: Separate LE Strip

- 10 mm wide carbon strip, 2 plies [0/90]
- Bonded over LE joint, faired to profile
- Provides abrasion resistance

---

## 10. Weight Verification

### 10.1 Target Weights

| Component | Target (g) | Tolerance |
|-----------|-----------|-----------|
| Inner skin (each) | 112 g | ±10 g |
| Outer skin (each) | 73 g | ±8 g |
| Total skins (4) | 370 g | ±30 g |
| Ribs (12 total) | 38 g | ±5 g |
| Spar rod | 28 g | ±2 g |
| Carry-through | 85 g | ±10 g |
| Fasteners + bond | 47 g | ±5 g |
| **Total wing** | **568 g** | **±52 g** |

### 10.2 Post-Cure Inspection

1. Weigh each component, compare to target
2. Check for voids with ultrasonic C-scan (if available)
3. Verify spar position: 30% chord ±1 mm
4. Check skin thickness: 0.8 mm (inner) or 0.6 mm (outer) ±0.1 mm
5. Verify planform dimensions against drawing

---

## 11. Bond Schedule

| Joint | Adhesive | Prep | Clamp | Cure |
|-------|----------|------|-------|------|
| Rib-to-skin | Araldite 420 A/B | Peel ply on skin | Spring clamp | 24h RT |
| Spar-to-rib | Hysol EA 9394 | Scuff spar with 120-grit | Tape hold | 24h RT |
| Spar-to-ferrule | Hysol EA 9394 | Scuff spar + ferrule | Press fit | 24h RT |
| Inner-to-outer skin (LE) | Hysol EA 9394 | Scuff bonding surfaces | Tape clamp | 24h RT |
| Wing-to-fuselage | Araldite 420 + M6 bolts | Scuff bond surfaces | Bolt torque 12 N·m | 24h RT |

---

## 12. Cure Cycle Summary

### For Prepreg (Recommended)

```
Temperature (°C)
    │
150 ┤                     ┌─────────┐  (optional post-cure)
    │                    ╱│         │╲
120 ┤───────────────────╱──│─────────│─╲──────────
    │                  ╱   │  2 hr   │  ╲
    │                ╱     │         │    ╲
 RT ┤──────────────╱       │         │      ╲──────
    │   60 min   │         │         │  90 min
    └──────────────────────────────────────────────► Time
         ramp     hold               cool
```

### For Wet Layup (Alternative)

```
Temperature (°C)
    │
 60 ┤                     ┌─────────┐
    │                    ╱│  4 hr   │╲
    │                  ╱  │         │  ╲
 RT ┤────────────────╱────│─────────│────╲──────
    │  RT 24 hr           │         │     RT
    └──────────────────────────────────────────────► Time
              initial         post-cure
              cure
```

---

*End of layup schedule. All coordinates in millimetres. Material specifications per manufacturer data sheets.*
