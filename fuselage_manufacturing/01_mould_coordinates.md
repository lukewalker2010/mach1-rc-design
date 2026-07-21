# Fuselage Mould — CNC Coordinates

## Overview

The fuselage uses a **split female mould** (LH and RH halves) bolted at a flange parting line. The mould is CNC-machined from RenShape 460 tooling board or MDF + tooling gelcoat.

---

## 1. Fuselage Profile — Upper/Lower Outline

The mould cavity is defined by the fuselage outer diameter at each station. The parting line runs horizontally through the aircraft centreline (top-bottom split).

### 1.1 Nose Section (Ogive, 0 ≤ x ≤ 0.40 m)

Formula: `R(x) = 100 × sin(π × x / 0.800)` mm

| x (mm) | R_upper (mm) | R_lower (mm) | Diameter (mm) |
|--------|-------------|-------------|---------------|
| 0 | 0.000 | 0.000 | 0.0 |
| 20 | 7.65 | 7.65 | 15.3 |
| 40 | 15.00 | 15.00 | 30.0 |
| 60 | 21.82 | 21.82 | 43.6 |
| 80 | 27.86 | 27.86 | 55.7 |
| 100 | 32.99 | 32.99 | 66.0 |
| 120 | 37.10 | 37.10 | 74.2 |
| 140 | 40.10 | 40.10 | 80.2 |
| 160 | 41.96 | 41.96 | 83.9 |
| 180 | 42.66 | 42.66 | 85.3 |
| 200 | 42.23 | 42.23 | 84.5 |
| 250 | 38.84 | 38.84 | 77.7 |
| 300 | 30.88 | 30.88 | 61.8 |
| 350 | 17.68 | 17.68 | 35.4 |
| 400 | 0.000 | 0.000 | 0.0 |

### 1.2 Parallel Section (0.40 ≤ x ≤ 1.80 m)

R = 100 mm constant (200 mm diameter), except waist region.

| x (mm) | R (mm) | Notes |
|--------|--------|-------|
| 400 | 100.0 | Start parallel |
| 500 | 100.0 | BH1 at 100mm |
| 600 | 100.0 | BH3 at 600mm |
| 700 | 100.0 | |
| 800 | 100.0 | Waist start |
| 850 | 100.0 | BH4 waist ring |
| 875 | 99.3 | |
| 900 | 97.3 | |
| 925 | 94.5 | |
| 950 | 91.8 | |
| 975 | 89.8 | |
| 1000 | 89.0 | Waist min |
| 1025 | 89.8 | |
| 1050 | 91.8 | |
| 1075 | 94.5 | |
| 1100 | 97.3 | BH5 |
| 1125 | 99.3 | |
| 1150 | 100.0 | Waist end |
| 1200 | 100.0 | |
| 1400 | 100.0 | BH6 engine fwd |
| 1600 | 100.0 | BH7 engine aft |
| 1800 | 100.0 | Boat tail start |

### 1.3 Boat Tail (1.80 ≤ x ≤ 2.20 m)

Formula: `R(x) = 100 − (x − 1800) × tan(11.6°)` mm

| x (mm) | R (mm) | Diameter (mm) |
|--------|--------|---------------|
| 1800 | 100.0 | 200.0 |
| 1850 | 93.1 | 186.2 |
| 1900 | 86.2 | 172.4 |
| 1950 | 79.3 | 158.6 |
| 2000 | 72.4 | 144.8 |
| 2050 | 65.5 | 131.0 |
| 2100 | 58.6 | 117.2 |
| 2150 | 51.7 | 103.4 |
| 2200 | 44.8 | 89.6 |

Wait — the spec says exhaust nozzle OD is 35 mm at x = 2.20 m. Let me recalculate.

From spec: R(2.20) = 17.5 mm. So the boat tail goes from R=100 at x=1.80 to R=17.5 at x=2.20.

`R(x) = 100 − (x − 1800) × (100 − 17.5) / 400 = 100 − (x − 1800) × 0.20625`

| x (mm) | R (mm) | Diameter (mm) |
|--------|--------|---------------|
| 1800 | 100.0 | 200.0 |
| 1850 | 89.7 | 179.4 |
| 1900 | 79.4 | 158.8 |
| 1950 | 69.1 | 138.2 |
| 2000 | 58.8 | 117.6 |
| 2050 | 48.5 | 97.0 |
| 2100 | 38.2 | 76.4 |
| 2150 | 27.9 | 55.8 |
| 2200 | 17.5 | 35.0 |

---

## 2. Mould Cavity Dimensions

### 2.1 Parting Line

The mould splits at the horizontal centreline (y = 0). Each half is a female cavity that wraps 180° around the fuselage.

### 2.2 Mould Bounding Box (each half)

| Dimension | Value | Notes |
|-----------|-------|-------|
| Length (x) | 2300 mm | Nose to exhaust, +50mm margin |
| Width (y) | 250 mm | Radius 100 + flange + margin |
| Height (z) | 130 mm | Radius 100 + clearance |
| Flange width | 20 mm | At parting line |

### 2.3 Flange Detail

```
    CROSS-SECTION AT PARTING LINE (x = 1.0 m)
    
    Upper mould half
    ┌──────────────────────────────────────┐
    │         ╭──────────╮                 │
    │        ╱            ╲                │
    │       ╱   Cavity     ╲               │
    │      ╱    R = 89 mm   ╲              │
    │     ╱                   ╲             │
    │────╱─────────────────────╲────────────│  ← Parting line
    │    │    Flange (20mm)     │            │
    │    │    4 × M6 bolts      │            │
    │    └─────────────────────┘            │
    │         ╭──────────╮                 │
    │        ╱            ╲                │
    │       ╱   Cavity     ╲               │
    │      ╱    R = 89 mm   ╲              │
    │     ╱                   ╲             │
    │────╱─────────────────────╲────────────│
    └──────────────────────────────────────┘
    Lower mould half
```

### 2.4 CNC Machining Sequence

1. **Rough:** 12 mm ball-nose end mill, 1.5 mm stepover
2. **Semi-finish:** 6 mm ball-nose, 0.8 mm stepover
3. **Finish:** 3 mm ball-nose, 0.4 mm stepover
4. **Polish:** 320 → 600 grit wet sand
5. **Seal:** Tooling gelcoat or epoxy sealer
6. **Release:** Frekote 770-NC

**Estimated CNC time:** 12-16 hours per half (3-axis mill)

---

## 3. Waist Region — Detailed Coordinates

The area-ruled waist (x = 0.85 to 1.15 m) is the most critical section for CNC machining.

### 3.1 Waist Profile (Diameter)

Formula: `D(x) = 200 − 22 × 0.5 × [1 − cos(2π × (x − 850) / 300)]` mm

| x (mm) | Factor | D (mm) | R (mm) |
|--------|--------|--------|--------|
| 850 | 0.000 | 200.0 | 100.0 |
| 860 | 0.020 | 199.6 | 99.8 |
| 870 | 0.079 | 198.3 | 99.1 |
| 880 | 0.172 | 196.2 | 98.1 |
| 890 | 0.300 | 193.4 | 96.7 |
| 900 | 0.450 | 190.1 | 95.1 |
| 910 | 0.613 | 186.5 | 93.3 |
| 920 | 0.772 | 183.0 | 91.5 |
| 930 | 0.901 | 180.2 | 90.1 |
| 940 | 0.981 | 178.4 | 89.2 |
| 950 | 1.000 | 178.0 | 89.0 |
| 960 | 0.981 | 178.4 | 89.2 |
| 970 | 0.901 | 180.2 | 90.1 |
| 980 | 0.772 | 183.0 | 91.5 |
| 990 | 0.613 | 186.5 | 93.3 |
| 1000 | 0.450 | 190.1 | 95.1 |
| 1010 | 0.300 | 193.4 | 96.7 |
| 1020 | 0.172 | 196.2 | 98.1 |
| 1030 | 0.079 | 198.3 | 99.1 |
| 1040 | 0.020 | 199.6 | 99.8 |
| 1050 | 0.000 | 200.0 | 100.0 |

---

## 4. Bulkhead Flat Patterns — CNC/Waterjet Cutting

### 4.1 BH1 — Nose Former (x = 100 mm)

| Feature | Value |
|---------|-------|
| OD | 78 mm |
| ID (centre hole) | 20 mm |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 0.8 mm |
| Cut method | CNC router or scissors |
| Shape | Annular ring |

### 4.2 BH2 — Avionics Bay (x = 350 mm)

| Feature | Value |
|---------|-------|
| OD | 193 mm |
| Centre hole | None (solid) |
| Wiring cutouts | 2 × 30×20 mm at 45° |
| M3 inserts | 4 × M3 at ±45°, 80 mm PCD |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.3 BH3 — Fuel Tank Fwd (x = 600 mm)

| Feature | Value |
|---------|-------|
| OD | 200 mm |
| AN-4 feed-through | 6.35 mm ID at 6 o'clock |
| Seal | 0.1 mm aluminium foil bonded to inner face |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.4 BH4 — Waist Ring / Wing LE (x = 850 mm)

| Feature | Value |
|---------|-------|
| OD forward | 200 mm |
| OD aft | 178 mm |
| Taper | Linear over 1.2 mm thickness |
| M6 inserts | 4 × M6 at ±45°, 120 mm PCD |
| Doubler pad | 2 mm local at bolt locations |
| Material | T300 carbon [0/90/+45/−45] (6 ply) |
| Thickness | 1.2 mm |

### 4.5 BH5 — Wing Rear (x = 1100 mm)

| Feature | Value |
|---------|-------|
| OD forward | 194 mm |
| OD aft | 194 mm (constant) |
| M6 inserts | 4 × M6 at ±45°, 120 mm PCD |
| Material | T300 carbon [0/90/+45/−45] (6 ply) |
| Thickness | 1.2 mm |

### 4.6 BH6 — Engine Mount Fwd (x = 1400 mm)

| Feature | Value |
|---------|-------|
| OD | 200 mm |
| Centre hole | 90 mm (engine pass-through) |
| Bracket pads | 4 × at ±45°, M5 tapped |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.7 BH7 — Engine Mount Aft (x = 1600 mm)

| Feature | Value |
|---------|-------|
| OD | 200 mm |
| Centre hole | 90 mm |
| Bracket pads | 4 × at ±45°, M5 tapped |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.8 BH8 — Tailcone Former (x = 2050 mm)

| Feature | Value |
|---------|-------|
| OD | 97 mm |
| ID | 60 mm (thrust ring) |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |
