# Fuselage Mould — CNC Coordinates

## Overview

The fuselage uses a **split female mould** (LH and RH halves) bolted at a flange parting line. The mould is CNC-machined from RenShape 460 tooling board or MDF + tooling gelcoat.

> **Correction (2026-08-06, audit D3):** this file previously carried the 2.20 m / 200 mm-OD baseline data (spindle nose `R = 100·sin(πx/0.8)`, waist pinch centred at x = 1.00 m with the wrong 22 mm factor, and a 1.80–2.20 m boat tail to R = 17.5 mm). The mould coordinates are **re-derived below from the authoritative re-baselined body law** (18 §3.1, disposition D3). Regenerate any dependent DXF/STL/toolpath from §1.5 — do not reuse the old tables.

---

## 1. Fuselage Profile — Corrected Body Law

The mould cavity is defined by the fuselage outer radius R(x) at each station. The parting line runs horizontally through the aircraft centreline (top-bottom split). Origin = fuselage nose tip, +X aft.

### 1.0 Regeneration formula (authoritative)

```
R(x) [m], x in metres, stations measured from the nose tip:

  R(x) = 0.0925 · sin(π·x / 0.85)                             x ∈ [0.00, 0.85]  (nose ogive)
  R(x) = 0.086 · [1 − cos(π·(x − 0.85) / 0.20)] / 2           x ∈ [0.85, 1.05]  (pinch → waist R = 0.086 at x = 1.05)
  R(x) = 0.086 + 0.0065 · [1 − cos(π·(x − 1.05) / 0.34)] / 2  x ∈ [1.05, 1.39]  (recover → R = 0.0925 at x = 1.39)
  R(x) = 0.0925                                                x ∈ [1.39, 1.80]  (engine / afterburner bay, constant)
  R(x) = 0.0925 − (0.0925 − 0.055) / 0.80 · (x − 1.80)         x ∈ [1.80, 2.60]  (boat tail → AB nozzle fairing, R → 0.055)

  Notes:
  · Max body radius R = 0.0925 m (185 mm OD) at x = 0.425 m and from 1.39–1.80 m.
  · The ogive passes through R ≈ 0 at x = 0.85 m (nose forebody closes at the
    wing carry-through interface, stations 0.95–1.15 m per I-04).
  · Waist minimum R = 0.086 m (172 mm OD) at x = 1.05 m.
  · The 0.85–1.05 and 1.05–1.39 transitions are smooth cosine half-waves
    (zero slope at each end) so the mould surface has no tangent breaks.
  · Boat tail is linear from R = 0.0925 m @ 1.80 m to R = 0.055 m @ 2.60 m
    (opening into the afterburner / C-D nozzle fairing per 18 §2, D3).
```

### 1.1 Nose ogive (0 ≤ x ≤ 0.85 m)

`R(x) = 0.0925 · sin(π·x / 0.85)` m — maximum R = 92.5 mm at x = 0.425 m, R → 0 at x = 0.85 m. (Former nose table was a 100 mm × 0.80 m spindle — wrong amplitude, wrong length, wrong scale.)

### 1.2 Waist pinch & recovery (0.85 ≤ x ≤ 1.39 m)

Pinch to the waist minimum R = 86 mm at x = 1.05 m (172 mm OD), then recover to full R = 92.5 mm at x = 1.39 m. (Former waist was centred at x = 1.00 m with a 22 mm cosine factor on the old 200 mm body — off-station, wrong factor.)

### 1.3 Engine / afterburner bay (1.39 ≤ x ≤ 1.80 m)

Constant R = 92.5 mm (185 mm OD). Engine mount ring at x = 1.20 m per 18 §3.1.

### 1.4 Boat tail → AB nozzle fairing (1.80 ≤ x ≤ 2.60 m)

Linear taper R 92.5 → 55 mm over 0.80 m (half-angle = arctan(37.5/800) ≈ 2.7°). (The two former boat-tail tables — 200→35 mm over 0.40 m and the "35 mm nozzle" tailcone — are void; the tailcone is replaced by the AB duct + nozzle fairing per 18 §3.1.)

### 1.5 Master station / radius table (CNC mould stations)

Stations every 50 mm from 0 to 2600 mm, computed from the formula above.

| x (mm) | R (mm) | OD (mm) |
|--------|--------|---------|
| 0 | 0.00 | 0.00 |
| 50 | 17.00 | 33.99 |
| 100 | 33.41 | 66.83 |
| 150 | 48.69 | 97.39 |
| 200 | 62.32 | 124.63 |
| 250 | 73.82 | 147.63 |
| 300 | 82.80 | 165.61 |
| 350 | 88.97 | 177.94 |
| 400 | 92.11 | 184.21 |
| 450 | 92.11 | 184.21 |
| 500 | 88.97 | 177.94 |
| 550 | 82.80 | 165.61 |
| 600 | 73.82 | 147.63 |
| 650 | 62.32 | 124.63 |
| 700 | 48.69 | 97.39 |
| 750 | 33.41 | 66.83 |
| 800 | 17.00 | 33.99 |
| 850 | 0.00 | 0.00 |
| 900 | 12.59 | 25.19 |
| 950 | 43.00 | 86.00 |
| 1000 | 73.41 | 146.81 |
| 1050 | 86.00 | 172.00 |
| 1100 | 86.34 | 172.68 |
| 1150 | 87.29 | 174.58 |
| 1200 | 88.65 | 177.31 |
| 1250 | 90.14 | 180.28 |
| 1300 | 91.44 | 182.88 |
| 1350 | 92.28 | 184.56 |
| 1400 | 92.50 | 185.00 |
| 1450 | 92.50 | 185.00 |
| 1500 | 92.50 | 185.00 |
| 1550 | 92.50 | 185.00 |
| 1600 | 92.50 | 185.00 |
| 1650 | 92.50 | 185.00 |
| 1700 | 92.50 | 185.00 |
| 1750 | 92.50 | 185.00 |
| 1800 | 92.50 | 185.00 |
| 1850 | 90.16 | 180.31 |
| 1900 | 87.81 | 175.62 |
| 1950 | 85.47 | 170.94 |
| 2000 | 83.12 | 166.25 |
| 2050 | 80.78 | 161.56 |
| 2100 | 78.44 | 156.88 |
| 2150 | 76.09 | 152.19 |
| 2200 | 73.75 | 147.50 |
| 2250 | 71.41 | 142.81 |
| 2300 | 69.06 | 138.13 |
| 2350 | 66.72 | 133.44 |
| 2400 | 64.38 | 128.75 |
| 2450 | 62.03 | 124.06 |
| 2500 | 59.69 | 119.38 |
| 2550 | 57.34 | 114.69 |
| 2600 | 55.00 | 110.00 |

**Checkpoints:** R(425) = 92.5 mm (max ogive) · R(850) ≈ 0 (ogive closure) · R(1050) = 86.0 mm (waist min, 172 mm OD) · R(1390) = R(1800) = 92.5 mm (185 mm OD) · R(2600) = 55.0 mm.

### 1.6 Mould draft (D15)

CNC moulds are machined from these stations with **0.5–1° draft added** on the parting-line faces (or the tool is split fore/aft) — the former 2.2 m zero-draft female mould is not releasable. Draft angle per D15; add it to the tooling surface normal, not to the body law R(x) in §1.5.

---

## 2. Mould Cavity Dimensions

### 2.1 Parting Line

The mould splits at the horizontal centreline (y = 0). Each half is a female cavity that wraps 180° around the fuselage. (Unchanged.)

### 2.2 Mould Bounding Box (each half)

| Dimension | Value | Notes |
|-----------|-------|-------|
| Length (x) | 2650 mm | Nose to AB nozzle fairing (2600 mm) + 50 mm margin |
| Width (y) | 230 mm | Max OD 185 mm + 2 × 20 mm flange + margin |
| Height (z) | 115 mm | Radius 92.5 mm + wall/clearance |
| Flange width | 20 mm | At parting line |

### 2.3 Flange Detail

```
    CROSS-SECTION AT PARTING LINE (x = 1.0 m)

    Upper mould half
    ┌──────────────────────────────────────┐
    │         ╭──────────╮                 │
    │        ╱            ╲                │
    │       ╱   Cavity     ╲               │
    │      ╱   R = 73.4 mm  ╲              │
    │     ╱                   ╲            │
    │────╱─────────────────────╲────────────│  ← Parting line
    │    │    Flange (20mm)     │            │
    │    │    4 × M6 bolts      │            │
    │    └─────────────────────┘            │
    │         ╭──────────╮                 │
    │        ╱            ╲                │
    │       ╱   Cavity     ╲               │
    │      ╱   R = 73.4 mm  ╲              │
    │     ╱                   ╲            │
    │────╱─────────────────────╲────────────│
    └──────────────────────────────────────┘
    Lower mould half
```

(Cavity radius at x = 1.0 m is 73.4 mm per the §1.5 table.)

### 2.4 CNC Machining Sequence

1. **Rough:** 12 mm ball-nose end mill, 1.5 mm stepover
2. **Semi-finish:** 6 mm ball-nose, 0.8 mm stepover
3. **Finish:** 3 mm ball-nose, 0.4 mm stepover
4. **Polish:** 320 → 600 grit wet sand
5. **Seal:** Tooling gelcoat or epoxy sealer
6. **Release:** Frekote 770-NC

**Estimated CNC time:** 14–18 hours per half (3-axis mill)

---

## 3. Waist Region — Detailed Coordinates

The corrected waist spans the ogive closure through the wing carry-through and into the engine bay (x = 0.85 to 1.39 m). It is the most critical region for CNC machining.

### 3.1 Waist Profile (Radius, corrected)

```
Pinch:    R(x) = 86 × [1 − cos(π·(x − 850) / 200)] / 2       x ∈ [850, 1050]
Recovery: R(x) = 86 + 6.5 × [1 − cos(π·(x − 1050) / 340)] / 2  x ∈ [1050, 1390]
```

| x (mm) | R (mm) | OD (mm) | x (mm) | R (mm) | OD (mm) |
|--------|--------|---------|--------|--------|---------|
| 850 | 0.00 | 0.00 | 1000 | 73.41 | 146.81 |
| 860 | 0.53 | 1.06 | 1010 | 77.79 | 155.58 |
| 870 | 2.10 | 4.21 | 1020 | 81.31 | 162.63 |
| 880 | 4.69 | 9.37 | 1030 | 83.90 | 167.79 |
| 890 | 8.21 | 16.42 | 1040 | 85.47 | 170.94 |
| 900 | 12.59 | 25.19 | 1050 | 86.00 | 172.00 |
| 910 | 17.73 | 35.45 | 1060 | 86.01 | 172.03 |
| 920 | 23.48 | 46.96 | 1070 | 86.06 | 172.11 |
| 930 | 29.71 | 59.42 | 1080 | 86.12 | 172.25 |
| 940 | 36.27 | 72.55 | 1090 | 86.22 | 172.44 |
| 950 | 43.00 | 86.00 | 1100 | 86.34 | 172.68 |
| 960 | 49.73 | 99.45 | 1110 | 86.49 | 172.97 |
| 970 | 56.29 | 112.58 | 1120 | 86.66 | 173.31 |
| 980 | 62.52 | 125.04 | 1130 | 86.85 | 173.70 |
| 990 | 68.27 | 136.55 | 1140 | 87.06 | 174.12 |
| | | | 1150 | 87.29 | 174.58 |

---

## 4. Bulkhead Flat Patterns — CNC/Waterjet Cutting

> **⚠️ Legacy data:** the bulkhead OD values below are from the pre-re-baseline 2.20 m / 200 mm body. The BH schedule and ODs are owned by E1/E3 (structure) and must be re-derived from the **§1.5 master radius table** before cutting. The reference body-law radius at each shown station is listed; where the old station sits on the corrected body a new OD applies, and BH4 (x = 850 mm) is invalid — it lands on the ogive closure (R ≈ 0) and must be re-stationed inside the carry-through box (0.95–1.15 m, I-04) by the owning engineer.

| BH# | x (mm) | Legacy OD (mm) | Body-law R @ x (mm) | Corrected OD (mm) |
|-----|--------|----------------|---------------------|-------------------|
| BH1 | 100 | 78 | 33.41 | 66.8 |
| BH2 | 350 | 193 | 88.97 | 177.9 |
| BH3 | 600 | 200 | 73.82 | 147.6 |
| BH4 | 850 | 200→178 | 0.00 (ogive closure) | n/a — re-station |
| BH5 | 1100 | 194 | 86.34 | 172.7 |
| BH6 | 1400 | 200 | 92.50 | 185.0 |
| BH7 | 1600 | 200 | 92.50 | 185.0 |
| BH8 | 2050 | 97 | 80.78 | 161.6 |

### 4.1 BH1 — Nose Former (x = 100 mm)

| Feature | Value |
|---------|-------|
| OD | 66.8 mm (was 78 mm) |
| ID (centre hole) | 20 mm |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 0.8 mm |
| Cut method | CNC router or scissors |
| Shape | Annular ring |

### 4.2 BH2 — Avionics Bay (x = 350 mm)

| Feature | Value |
|---------|-------|
| OD | 177.9 mm (was 193 mm) |
| Centre hole | None (solid) |
| Wiring cutouts | 2 × 30×20 mm at 45° |
| M3 inserts | 4 × M3 at ±45°, 80 mm PCD |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.3 BH3 — Fuel Tank Fwd (x = 600 mm)

| Feature | Value |
|---------|-------|
| OD | 147.6 mm (was 200 mm) |
| AN-4 feed-through | 6.35 mm ID at 6 o'clock |
| Seal | 0.1 mm aluminium foil bonded to inner face |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.4 BH4 — Waist Ring / Wing LE (x = 850 mm)

| Feature | Value |
|---------|-------|
| OD forward | **re-station required** — x = 850 mm sits on the ogive closure (R ≈ 0), not the waist ring. Waist ring must sit inside the carry-through box (0.95–1.15 m, I-04). |
| M6 inserts | 4 × M6 at ±45°, 120 mm PCD |
| Material | T300 carbon [0/90/+45/−45] (6 ply) |
| Thickness | 1.2 mm |

### 4.5 BH5 — Wing Rear (x = 1100 mm)

| Feature | Value |
|---------|-------|
| OD | 172.7 mm (was 194 mm) |
| M6 inserts | 4 × M6 at ±45°, 120 mm PCD |
| Material | T300 carbon [0/90/+45/−45] (6 ply) |
| Thickness | 1.2 mm |

### 4.6 BH6 — Engine Mount Fwd (x = 1400 mm)

| Feature | Value |
|---------|-------|
| OD | 185.0 mm (was 200 mm) |
| Centre hole | 90 mm (engine pass-through) |
| Bracket pads | 4 × at ±45°, M5 tapped |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.7 BH7 — Engine Mount Aft (x = 1600 mm)

| Feature | Value |
|---------|-------|
| OD | 185.0 mm (was 200 mm) |
| Centre hole | 90 mm |
| Bracket pads | 4 × at ±45°, M5 tapped |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |

### 4.8 BH8 — Tailcone Former (x = 2050 mm)

| Feature | Value |
|---------|-------|
| OD | 161.6 mm (was 97 mm) |
| ID | 60 mm (thrust ring) |
| Material | T300 carbon [0/90]₂ (4 ply) |
| Thickness | 1.0 mm |
