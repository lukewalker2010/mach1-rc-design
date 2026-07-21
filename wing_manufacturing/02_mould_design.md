# Wing Mould Design — CNC Male Plug Specification

## 1. Mould Concept

The wing skins are laid up on a **male mould** (positive plug) that replicates the external wing surface. Two moulds are needed:
- **Inner panel mould** (root to 200 mm span)
- **Outer panel mould** (200 mm to 450 mm span)

The mould is a solid CNC-machined block that captures the biconvex airfoil shape across the delta planform.

---

## 2. Mould Geometry

### 2.1 Bounding Box

| Dimension | Value | Notes |
|-----------|-------|-------|
| Length (x, chordwise) | 220 mm | Root chord + 9 mm margin |
| Width (y, spanwise) | 460 mm | Half-span + 10 mm margin |
| Height (z, thickness) | 12 mm | Max wing thickness + margin |
| Block material | 6061-T6 aluminium | Or high-density tooling board (Renshape 5008) |

### 2.2 Surface Definition

The mould surface is defined by the biconvex airfoil swept across the delta planform.

**Upper surface equation:**

For any point (x, y) on the mould:
1. Determine local span station: y_station = y (measured from root)
2. Determine local chord at that station: c(y) = 211 × (1 − y/450)
3. Determine local max thickness: t(y) = 0.035 × c(y)
4. Determine normalised chordwise position: ξ = x / c(y)
5. If 0 ≤ ξ ≤ 1: z_upper = (t(y)/2) × sin(π × ξ)
6. If ξ < 0 or ξ > 1: z_upper = 0 (outside planform)

**Lower surface:** z_lower = −z_upper (symmetric biconvex)

### 2.3 Surface Resolution for CNC

| Parameter | Value |
|-----------|-------|
| X step (chordwise) | 0.5 mm |
| Y step (spanwise) | 1.0 mm |
| Total points per surface | ~19,800 |
| Surface finish target | Ra 0.8 μm (320-grit equivalent) |
| Tolerance | ±0.05 mm |

---

## 3. Mould Construction

### 3.1 Option A: Aluminium Plug (Recommended)

**Material:** 6061-T6 aluminium billet
**Size:** 220 × 460 × 12 mm (single piece)

**Machining sequence:**
1. Face top surface to flat, Ra 1.6 μm
2. Rough contour: 3-axis ball-nose end mill, 6 mm dia, 0.5 mm stepover
3. Semi-finish: 3 mm ball-nose, 0.3 mm stepover
4. Finish: 2 mm ball-nose, 0.15 mm stepover, Ra 0.8 μm
5. Polish: 600-grit wet, then polishing compound
6. Anodise: hard anodise (Type III) for durability, 25 μm
7. PTFE coat: dry film PTFE release coating

**Estimated CNC time:** 4–6 hours (3-axis mill)
**Surface prep:** 80 → 120 → 240 → 320 → 400 → 600 grit, then polish

### 3.2 Option B: Tooling Board Plug

**Material:** Renshape 5008 or polyurethane tooling board (Shore D 85)
**Size:** Same as aluminium

**Advantages:** Faster to machine, easier to hand-finish, lighter
**Disadvantages:** Less durable, can chip on sharp edges

**Machining sequence:** Same as aluminium, skip anodise step
**Surface prep:** Seal with epoxy sealer, then sand and polish

---

## 4. Mould Surface Details

### 4.1 Spar Channel

The spar rod passes through the mould at 30% chord:

| Feature | Value |
|---------|-------|
| Channel position | x = 0.30 × c(y) |
| Channel depth | 3.0 mm (half-rod depth into mould) |
| Channel width | 5.2 mm (slight clearance on 5.0 mm rod) |
| Channel profile | Semi-circular, radius 2.6 mm |
| Purpose | Locates spar during layup, ensures correct position |

### 4.2 Leading Edge Radius

The biconvex airfoil has a sharp LE at the mathematical surface. For mould durability:

| Parameter | Value |
|-----------|-------|
| LE radius (root) | 0.5 mm |
| LE radius (tip) | 0.2 mm |
| Blend length | 2 mm aft of LE |

### 4.3 Trailing Edge

The biconvex section comes to a sharp TE. For mould and part durability:

| Parameter | Value |
|-----------|-------|
| TE thickness | 0.3 mm minimum (mould) |
| TE angle | ~6° included (root) |
| TE treatment | Slight flat, 0.3 mm wide |

### 4.4 Ply Allowance

The mould represents the **outer skin surface**. Add material for:
- Peel ply: +0.1 mm (not machined into mould — applied during layup)
- Inner skin mould: separate plug, offset by 0.8 mm (inner panel thickness)

---

## 5. Inner vs Outer Panel Moulds

### 5.1 Inner Panel Mould (Root to 200 mm)

| Parameter | Value |
|-----------|-------|
| Span range | 0–200 mm |
| Chord range | 211–127 mm (linear taper) |
| Skin thickness | 0.8 mm (4-ply [0/±45/0]) |
| Mould offset | 0 mm (mould = outer surface) |

### 5.2 Outer Panel Mould (200–450 mm)

| Parameter | Value |
|-----------|-------|
| Span range | 200–450 mm |
| Chord range | 127–0 mm (linear taper) |
| Skin thickness | 0.6 mm (3-ply [0/±45]) |
| Mould offset | 0 mm (mould = outer surface) |

### 5.3 Ply Drop-Off Transition

At the 200 mm junction:
- Inner panel: [0/±45/0] (4 plies, 0.8 mm)
- Outer panel: [0/±45] (3 plies, 0.6 mm)
- Drop: inner 0° ply terminates at 195 mm
- Outer 0° ply starts at 205 mm
- 10 mm overlap zone filled with epoxy microballoon fairing
- Mould has a 0.2 mm step at 200 mm to accommodate thickness change

---

## 6. Mould Release System

### 6.1 Release Agent Schedule

| Step | Product | Application |
|------|---------|-------------|
| 1 | Partall #2 paste wax | 3 coats, buff between |
| 2 | Partall #10 PVA | 1 coat, spray, let dry |
| 3 | Frekote 770-NC | 2 coats, 15 min between |

### 6.2 Release Film

- **Peel ply:** Nylon peel ply, 80 g/m², applied over wet layup
- **Release film:** perforated FEP, applied over peel ply under vacuum bag

---

## 7. Vacuum Bagging Setup

### 7.1 Bag Stack (bottom to top)

1. Mould surface (male plug)
2. Peel ply (nylon, 80 g/m²)
3. Perforated FEP release film
4. Breather cloth (2 layers)
5. Vacuum bag (nylon, 0.05 mm)

### 7.2 Cure Schedule

| Parameter | Value |
|-----------|-------|
| Vacuum | −0.9 bar (−26.5 inHg) minimum |
| Cure temperature | 120 °C (prepreg) or RT (wet layup + heat lamp) |
| Cure time | 2 hours at 120 °C, or 24 hours at RT |
| Post-cure | 1 hour at 150 °C (optional, improves Tg) |
| Ramp rate | 2 °C/min max |

---

## 8. Mould Drawing (Cross-Section)

```
                        CROSS-SECTION AT ROOT (y = 0)
                        
                    ┌─── 220 mm ───┐
                    │               │
        ┌───────────┴───────────────┴───────────┐
        │            6061-T6 AL                  │ 12 mm
        │   ┌─────────────────────────────┐      │
        │   │    BICONVEX CONTOUR         │      │
        │   │    (machined into surface)  │      │
        │   │                             │      │
        │   │    x: 0 to 211 mm           │      │
        │   │    z: ±3.7 mm max           │      │
        │   │                             │      │
        │   │    Spar channel @ x=63.3    │      │
        │   │    (5.2 mm wide × 3.0 deep) │      │
        │   │         ┌───┐               │      │
        │   └─────────┤   ├───────────────┘      │
        │             │   │                      │
        └─────────────┴───┴──────────────────────┘
                      ▲
                      Spar channel (semi-circular)
```

```
                        TOP VIEW — Mould Layout
                        
        ┌──────────────────────────────────────────────┐
        │                                              │
        │     ╱╲                                       │
        │    ╱  ╲         OUTER PANEL                  │
        │   ╱    ╲        (200-450 mm)                 │
        │  ╱      ╲                                    │
        │ ╱   R3   ╲     R4      R5                    │
        │╱          ╲                                  │
        ├────────────╲─────────────────┐               │
        │  INNER      ╲   R2           │               │
        │  PANEL        ╲              │               │
        │ (0-200 mm)      ╲  R1        │               │
        │                   ╲          │               │
        │     R0              ╲        │               │
        │                      ╲       │               │
        └───────────────────────╲──────┘               │
                                ╲                      │
        │◄─── 211 mm (root) ────►│                     │
        │                        │                     │
        │◄──────── 460 mm (half-span) ────────────────►│
        
        ▲ Root (y=0)              Tip (y=450)
```

---

## 9. DXF/DXF Export Notes

To convert these profiles to DXF for CNC:

1. **Rib profiles:** Export each rib as a closed polyline (upper surface + LE + lower surface + TE)
2. **Mould surface:** Export as a mesh of triangles (STL) or as a series of cross-section polylines
3. **Spar channel:** Export as a circle (5.2 mm dia) at 30% chord station
4. **Coordinate system:** X = chordwise (0 at LE), Y = spanwise (0 at root), Z = thickness (0 at midplane)

### File Naming Convention

```
wing_rib_R0_outer.dxf    — Upper surface profile, rib R0
wing_rib_R0_inner.dxf    — Lower surface profile, rib R0
wing_rib_R0_foam.dxf     — Combined foam core outline, rib R0
...
wing_mould_upper.stl      — 3D mould surface, upper
wing_mould_lower.stl      — 3D mould surface, lower
wing_spar_channel.dxf     — Spar channel locations
```

---

## 10. Quality Acceptance Criteria

| Feature | Tolerance | Measurement Method |
|---------|-----------|-------------------|
| Airfoil profile | ±0.05 mm | CMM or profile gauge |
| Chord length | ±0.5 mm | Caliper |
| LE radius | ±0.1 mm | Radius gauge |
| TE thickness | 0.3 ±0.1 mm | Micrometer |
| Spar channel position | ±0.3 mm | Caliper |
| Surface finish | Ra ≤ 0.8 μm | Surface profilometer |
| Flatness (mould base) | 0.05 mm | Surface plate + dial indicator |
