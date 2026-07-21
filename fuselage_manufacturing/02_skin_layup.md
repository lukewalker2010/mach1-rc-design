# Fuselage Skin Layup Schedule

## 1. Zone Overview

| Zone | x range (mm) | Thickness | Layup | Plies | Notes |
|------|-------------|-----------|-------|-------|-------|
| Nose | 0–300 | 0.8 mm | [0/90/±45] | 4 | Erosion resistance |
| Fwd | 300–800 | 0.6 mm | [0/±45] | 3 | General forebody |
| Waist | 800–1000 | 1.2 mm | [0/90/±45/0/90] | 6 | + bonded doubler |
| Wing | 1000–1400 | 0.8 mm | [0/90/±45] | 4 | Carry-through region |
| Engine | 1200–1800 | 1.0 mm | [0/90/±45/0] | 5 | Heat & vibration |
| Aft | 1400–2000 | 0.6 mm | [0/±45] | 3 | Boat tail start |
| Tail | 2000–2200 | 0.6 mm | [0/±45] | 3 | Conical layup |

---

## 2. Ply Details (per zone)

### 2.1 Nose Zone — [0/90/±45] (0.8 mm, 4 ply)

| Ply | Orientation | Thickness | Function |
|-----|-------------|-----------|----------|
| 1 | 0° | 0.20 mm | Axial bending |
| 2 | 90° | 0.20 mm | Circumferential hoop |
| 3 | +45° | 0.20 mm | Torsion/shear |
| 4 | −45° | 0.20 mm | Torsion/shear |

### 2.2 Fwd Zone — [0/±45] (0.6 mm, 3 ply)

| Ply | Orientation | Thickness | Function |
|-----|-------------|-----------|----------|
| 1 | 0° | 0.20 mm | Axial |
| 2 | +45° | 0.20 mm | Shear |
| 3 | −45° | 0.20 mm | Shear |

### 2.3 Waist Zone — [0/90/±45/0/90] (1.2 mm, 6 ply)

| Ply | Orientation | Thickness | Function |
|-----|-------------|-----------|----------|
| 1 | 0° | 0.20 mm | Axial |
| 2 | 90° | 0.20 mm | Hoop |
| 3 | +45° | 0.20 mm | Shear |
| 4 | −45° | 0.20 mm | Shear |
| 5 | 0° | 0.20 mm | Axial |
| 6 | 90° | 0.20 mm | Hoop |

Plus 0.6 mm bonded doubler [0/90] on inner surface (2 plies).

### 2.4 Engine Zone — [0/90/±45/0] (1.0 mm, 5 ply)

| Ply | Orientation | Thickness | Function |
|-----|-------------|-----------|----------|
| 1 | 0° | 0.20 mm | Axial |
| 2 | 90° | 0.20 mm | Hoop |
| 3 | +45° | 0.20 mm | Shear |
| 4 | −45° | 0.20 mm | Shear |
| 5 | 0° | 0.20 mm | Axial |

---

## 3. Layup Procedure — Split Female Mould

### 3.1 Mould Preparation

1. Clean both mould halves with acetone
2. Apply release schedule: Partall #2 wax ×3, PVA ×1, Frekote 770-NC ×2
3. Apply gelcoat if required (tooling gelcoat, spray, 0.3 mm)

### 3.2 Layup Sequence

**Step 1 — Lower half layup**
1. Apply plies to lower mould cavity, working from LE (nose) to TE (exhaust)
2. Each zone transitions: stagger ply termination by 20 mm minimum
3. Smooth from centre outward with plastic squeegee
4. Vacuum bag lower half, cure at RT (tack cure, 2 hours)

**Step 2 — Bulkhead installation**
1. Bond bulkheads BH1–BH8 into lower half using Araldite 420
2. Use centring jig to ensure alignment
3. Allow 4-hour tack cure

**Step 3 — Upper half layup**
1. Repeat ply layup in upper mould half
2. Do NOT cure upper half — leave as wet layup

**Step 4 — Join mould halves**
1. Apply Hysol EA 9394 to parting line flange
2. Mate upper and lower halves
3. Clamp at flange with M6 bolts (12 per side, 20 mm pitch)
4. Pull vacuum on entire assembly
5. Cure at 120 °C for 2 hours (if prepreg) or RT 24 hours (wet layup)

**Step 5 — Demould**
1. Remove flange bolts
2. Separate mould halves carefully
3. Remove fuselage shell
4. Trim flange flash with diamond wheel

### 3.3 Waist Doubler Application

After demoulding:
1. Lay 0.6 mm [0/90] doubler on inner surface, x = 750–1050 mm
2. Bond with Araldite 420
3. Scarf taper edges: 10:1 over 6 mm
4. Vacuum bag and cure 12 hours RT

---

## 4. Skin-to-Bulkhead Bonding

### 4.1 Fillet Detail

```
         BH ring
       ╱──────╲
 Skin ┤        ├ Skin
      │ ┌──────┤
      │ │Epoxy │
      │ │fillet│
      │ └──────┤
       ╲──────╱
```

- Fillet material: Hysol EA 9394
- Fillet radius: 3 mm
- Bond width: 30 mm on each side of bulkhead
- Shear area per bulkhead: π × D × 30 mm

### 4.2 Bond Sequence

1. Install bulkheads in order BH1 → BH8
2. Apply fillet to each side of each bulkhead
3. Allow 24-hour cure before handling
4. Inspect fillets for voids (visual + tap test)

---

## 5. Hatch Cutouts

### 5.1 H1 — Avionics Hatch (x = 300–600 mm, top)

- Cut after cure using diamond router
- Cutout: 120 × 200 mm
- Flange: 5 mm wide, recessed 1 mm
- Install magnet pockets: 4 × ∅10 mm × 3 mm deep
- Bond magnets with epoxy

### 5.2 H2 — Engine Hatch (x = 1300–1800 mm, bottom)

- Cut after cure
- Cutout: 150 × 450 mm
- Flange: 8 mm wide, recessed 1.5 mm
- Install magnet pockets: 6 × ∅15 mm × 4 mm deep
- Install Dzus fastener receptacles: 2 locations
- Bond 0.3 mm SS foil heat shield to inner face

---

## 6. Engine Mount Installation

### 6.1 Mount Ring

- Material: 7075-T6 aluminium, 6 mm plate
- CNC mill: 90 mm ID × 200 mm OD annular ring
- Drill 3 × M5 bolt holes at 80 mm PCD (0°, 120°, 240°)
- Anodise Type II after machining

### 6.2 Mount Legs

- Material: 7075-T6 aluminium, 6 × 20 mm bar
- Cut 8 legs: 4 forward (120 mm) + 4 aft (150 mm)
- Drill M5 holes at each end
- Anodise after machining

### 6.3 Assembly

1. Bolt ring to engine case (3 × M5, 6 N·m)
2. Attach legs to ring (8 × M5, 6 N·m)
3. Position engine assembly in fuselage
4. Mark leg positions on BH6 and BH7
5. Drill and tap M5 holes in bulkhead pads
6. Bolt legs to bulkheads (16 × M5, 6 N·m)
7. Apply Loctite 242 to all bolts

---

## 7. Hinge Bracket Installation (Stabilator)

### 7.1 Bracket Fabrication

- Material: 7075-T6 aluminium, 3 mm plate
- CNC mill 4 brackets (2 per side, inboard + outboard)
- Dimensions: 10 × 12 mm, with 4 mm bore (reamed H7)
- Drill 2 × M2.5 mounting holes per bracket

### 7.2 Installation

1. Bond aluminium hardpoint blocks to fuselage at x = 2050 mm
2. Bolt brackets to hardpoints (2 × M2.5 per bracket)
3. Align bore axes — must be coaxial within 0.1 mm
4. Final ream bores after installation

---

## 8. Weight Verification

| Component | Target (g) | Tolerance |
|-----------|-----------|-----------|
| Fuselage skins (complete) | 1843 | ±150 g |
| Bulkheads (8 total) | 336 | ±30 g |
| Engine mount | 285 | ±20 g |
| Hatches + hardware | 300 | ±25 g |
| Adhesives + misc | 190 | ±20 g |
| **Total fuselage** | **2954** | **±245 g** |

### Post-Cure Inspection

1. Weigh all components
2. Check skin thickness at 10 random points (±0.1 mm)
3. Verify bulkhead positions (±2 mm from nominal)
4. Check waist profile against mould coordinates (±0.5 mm)
5. Tap-test all bonded joints (no hollow sounds)
6. Verify hatch fit (flush, gap ≤0.5 mm)
