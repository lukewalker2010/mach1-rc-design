# 05 — Fuselage Structure Design

## 1. Fuselage Mold Line

### 1.1 Overall Dimensions

| Parameter          | Value      | Notes                         |
|--------------------|------------|-------------------------------|
| Total length       | 2.200 m    | Nose tip to exhaust plane     |
| Max diameter       | 200 mm     | Parallel section              |
| Max radius         | 100 mm     | From x = 0.40 m to 1.60 m     |
| Nose section       | 0–0.40 m   | Ogive                         |
| Parallel section   | 0.40–1.60 m| Constant 200 mm OD (waist excluded) |
| Waist pinch        | 0.85–1.15 m| Diameter 200→178→200 mm       |
| Boat tail start    | 1.80 m     |                               |
| Boat tail half-angle | 4.0°     |                               |
| Exhaust nozzle OD  | 35 mm      | At x = 2.20 m                 |
| Fineness ratio     | 11.0       | L / D_max                     |

### 1.2 Nose Geometry (Ogive, 0 ≤ x ≤ 0.40 m)

Nose radius as a function of station:

```
  R(x) = 0.100 × sin(π × x / 0.800)    [metres]

  At x = 0.00 m:  R = 0.000 m   (tip)
  At x = 0.20 m:  R = 0.071 m   (mid-nose)
  At x = 0.40 m:  R = 0.100 m   (full radius, tangent to body)
```

### 1.3 Boat Tail Geometry (1.80 ≤ x ≤ 2.20 m)

Linear taper from 200 mm OD (R = 100 mm) at x = 1.80 m to 35 mm OD (R = 17.5 mm) at x = 2.20 m.

```
  Half-angle θ = 4.0°
  Δx = 0.40 m
  ΔR = 100.0 − 17.5 = 82.5 mm
  tan(θ) = 82.5 / 400 = 0.206 → θ = arctan(0.206) ≈ 11.6°
```

**NOTE:** 4° is achievable only if the taper starts earlier. To reconcile with 4° half-angle:
- Taper length needed: ΔR / tan(4°) = 82.5 mm / 0.0699 = **1 180 mm**
- Revised boat tail: start at x = 1.02 m, continue to x = 2.20 m
- However, this conflicts with wing and engine bay. **Design compromise:** Use boat tail from x = 1.80 m with **11.6° half-angle** (not 4°) for a practical layout, or accept that the 4° figure refers to the angle at the extreme aft section only.

**Adopted boat tail:** 11.6° half-angle, 1.80–2.20 m. A conical frustum.

```
  R(x) = 0.100 − (x − 1.80) × tan(11.6°)   for x ∈ [1.80, 2.20]
  R(1.80) = 100.0 mm
  R(2.00) = 58.8 mm
  R(2.20) = 17.5 mm
```

### 1.4 Area-Ruled Waist

Between x = 0.85 m and x = 1.15 m (wing root region), the fuselage is pinched to satisfy area rule (transonic drag reduction):

```
  Waist profile (cosine pinch):

    D_waist(x) = D_nominal − ΔD × 0.5 × [1 − cos(2π × (x − 0.85) / 0.30)]

  Where:
    D_nominal = 200 mm
    ΔD        = 22 mm  (pinch depth)
    x ∈ [0.85, 1.15] m
```

| x [m] | Factor  | D_waist [mm] |
|-------|---------|--------------|
| 0.850 | 0.000   | 200.0        |
| 0.875 | 0.067   | 199.3        |
| 0.900 | 0.250   | 194.5        |
| 0.925 | 0.500   | 189.0        |
| 0.950 | 0.750   | 183.5        |
| 0.975 | 0.933   | 179.5        |
| 1.000 | 1.000   | 178.0        |
| 1.025 | 0.933   | 179.5        |
| 1.050 | 0.750   | 183.5        |
| 1.075 | 0.500   | 189.0        |
| 1.100 | 0.250   | 194.5        |
| 1.125 | 0.067   | 199.3        |
| 1.150 | 0.000   | 200.0        |

### 1.5 Fuselage Diameter Table

| Station x [m] | Section      | Diameter [mm] | Radius [mm] | Notes                     |
|---------------|--------------|---------------|-------------|---------------------------|
| 0.00          | Nose tip     | 0             | 0           | Ogive tip                 |
| 0.10          | Nose         | 78            | 39          | BH1 location              |
| 0.20          | Nose         | 141           | 71          | Mid-nose                  |
| 0.30          | Nose         | 182           | 91          | Avionics bay start        |
| 0.35          | Nose         | 193           | 97          | BH2                       |
| 0.40          | Nose→parallel| 200           | 100         | Full radius               |
| 0.50          | Parallel     | 200           | 100         |                           |
| 0.60          | Parallel     | 200           | 100         | BH3 (fuel tank fwd)       |
| 0.70          | Parallel     | 200           | 100         |                           |
| 0.80          | Parallel     | 200           | 100         |                           |
| 0.85          | Waist start  | 200.0         | 100.0       | BH4                       |
| 0.90          | Waist        | 194.5         | 97.3        |                           |
| 0.95          | Waist        | 183.5         | 91.8        |                           |
| 1.00          | Waist min    | 178.0         | 89.0        | Wing root centre          |
| 1.05          | Waist        | 183.5         | 91.8        |                           |
| 1.10          | Waist        | 194.5         | 97.3        | BH5 (wing rear spar)      |
| 1.15          | Waist end    | 200.0         | 100.0       |                           |
| 1.20          | Parallel     | 200           | 100         | Engine bay start          |
| 1.30          | Parallel     | 200           | 100         |                           |
| 1.40          | Parallel     | 200           | 100         | BH6 (engine mount fwd)    |
| 1.50          | Parallel     | 200           | 100         |                           |
| 1.60          | Parallel     | 200           | 100         | BH7 (engine mount aft)    |
| 1.70          | Parallel     | 200           | 100         |                           |
| 1.80          | Boat tail    | 200.0         | 100.0       | Conical taper start       |
| 1.90          | Boat tail    | 161.2         | 80.6        |                           |
| 2.00          | Boat tail    | 117.6         | 58.8        |                           |
| 2.05          | Boat tail    | 96.6          | 48.3        | BH8 (tailcone former)     |
| 2.10          | Boat tail    | 76.0          | 38.0        |                           |
| 2.20          | Nozzle plane | 35.0          | 17.5        | Exhaust exit              |

### 1.6 Fuselage Profile (ASCII)

```
   R [mm]
  100 ┤╭──────────────────────────────────────────╮╱╲
      │╱                                          │  ╲
   80 ┤│                                          │   ╲
      ││                                          │    ╲
   60 ┤│                                          │     ╲
      ││                                          │      ╲
   40 ┤│                                          │       ╲
      ││                                          │        ╲
   20 ┤│                                          │         ╲
      ││                                          │          ╲
    0 ┼╰──────────────────────────────────────────╯───────────╲
     0    0.2   0.4   0.6   0.8   1.0   1.2   1.4   1.6   1.8   2.0   2.2
                       x [m]
  Key:
    ╭─╮  Nose ogive       (0.00–0.40 m)
    ──   Parallel body    (0.40–1.80 m, with waist pinch 0.85–1.15 m)
    ╲    Boat tail        (1.80–2.20 m)
```

---

## 2. Bulkhead Locations and Design

### 2.1 Bulkhead Schedule

| BH# | x [m] | Diameter [mm] | Thickness [mm] | Function                              |
|-----|-------|---------------|----------------|---------------------------------------|
| BH1 | 0.10  | 78            | 1.0            | Nose cone former, tip attachment      |
| BH2 | 0.35  | 193           | 1.0            | Avionics bay rear bulkhead            |
| BH3 | 0.60  | 200           | 1.0            | Fuel tank forward bulkhead            |
| BH4 | 0.85  | 200→178       | 1.2            | Waist ring, wing LE attachment        |
| BH5 | 1.10  | 194→178       | 1.2            | Wing rear spar attachment             |
| BH6 | 1.40  | 200           | 1.0            | Engine mount forward                  |
| BH7 | 1.60  | 200           | 1.0            | Engine mount aft                      |
| BH8 | 2.05  | 97            | 1.0            | Tailcone former, 60 mm ID thrust ring |

### 2.2 Bulkhead Design Details

**BH1 (x = 0.10 m) — Nose Former**
```
  ┌────────────┐
  │  ○ 78 mm   │  Annular ring
  │    OD      │  1 mm carbon laminate
  │            │  Centre hole: 20 mm (antenna or pitot feed)
  └────────────┘
  Draped with 0°/90° woven carbon, bonded to nose skin.
```

**BH2 (x = 0.35 m) — Avionics Bay Rear**
```
  ┌────────────┐
  │ ○ 193 mm   │  Full ring with equipment tray tabs
  │   OD       │  Four M3 tapped inserts at ±45°, 80 mm PCD
  │ ◇───◇     │
  │ ╲     ╲    │  Cutouts: 30×20 mm for wiring looms
  │  ╲   ╲     │  1 mm carbon
  └────────────┘
```

**BH3 (x = 0.60 m) — Fuel Tank Forward**
```
  ┌────────────┐
  │ ○ 200 mm   │  Sealed bulkhead (fuel barrier)
  │   OD       │  1 mm carbon + 0.1 mm aluminium foil vapour barrier
  │            │  AN-4 feed-through: 6.35 mm ID for fuel line
  │ ───AN4───  │  Bonded with fuel-resistant epoxy
  └────────────┘
```

**BH4 (x = 0.85 m) — Waist Ring / Wing LE Attachment**
```
  ┌────────────┐
  │ ○ 200 mm   │  Tapered ring: 200 mm at forward face,
  │   OD       │  178 mm at aft face (waist transition)
  │ ▼ 178mm   │  1.2 mm carbon (thicker for wing loads)
  │            │  Four M6 steel inserts for wing carry-through bolts
  │ ──M6──    │  Torque-box doubler: 2 mm local pad-up
  └────────────┘
```

**BH5 (x = 1.10 m) — Wing Rear Spar Attachment**
```
  ┌────────────┐
  │ ○ 194 mm   │  Tapered: 194→178→194 mm
  │   OD       │  1.2 mm carbon
  │            │  Four M6 steel inserts (wing aft bolts)
  │ ──M6──    │  Wing carry-through rear wall
  └────────────┘
```

**BH6 (x = 1.40 m) — Engine Mount Forward**
```
  ┌────────────┐
  │ ○ 200 mm   │  1 mm carbon
  │   OD       │  4 × aluminium brackets at ±45° (engine mount legs)
  │ ▲  ▲      │  7075-T6 brackets, bolted to bulkhead
  │ │  │       │  Centre hole: 90 mm (engine case pass-through)
  └────────────┘
```

**BH7 (x = 1.60 m) — Engine Mount Aft**
```
  ┌────────────┐
  │ ○ 200 mm   │  1 mm carbon
  │   OD       │  4 × aluminium brackets at ±45° (rear legs)
  │ ▲  ▲      │  7075-T6
  │ │  │       │  Centre hole: 90 mm
  └────────────┘
```

**BH8 (x = 2.05 m) — Tailcone Former**
```
  ┌────────────┐
  │ ○  97 mm   │  1 mm carbon
  │   OD       │  Inner hole: 60 mm ID (thrust ring)
  │ ○  60 mm   │  Exhaust nozzle support
  └────────────┘
```

### 2.3 Bulkhead Material & Layup (all bulkheads)

| BH#  | Material  | Layup                   | Notes                 |
|------|-----------|-------------------------|-----------------------|
| BH1  | Carbon    | [0/90]₂ (4 ply)         | Thin, lightly loaded  |
| BH2  | Carbon    | [0/90]₂ (4 ply)         | + local fabric at tabs|
| BH3  | Carbon    | [0/90]₂ (4 ply)         | Fuel seal             |
| BH4  | Carbon    | [0/90/+45/-45] (6 ply)  | 1.2 mm, wing loads    |
| BH5  | Carbon    | [0/90/+45/-45] (6 ply)  | 1.2 mm, wing loads    |
| BH6  | Carbon    | [0/90]₂ (4 ply)         | Engine mount          |
| BH7  | Carbon    | [0/90]₂ (4 ply)         | Engine mount          |
| BH8  | Carbon    | [0/90]₂ (4 ply)         | Tail cone support     |

---

## 3. Engine Mount

### 3.1 Configuration

```
         VIEW LOOKING FORWARD (x = 1.40 m → aft)

                       BH6
                 ┌──────────────┐
                /                \
               /      ▲           \
              /      / \           \
             /      /   \           \
            /      /     \           \
           /      /       \           \
          /     L1         L2          \
         /    (7075-T6)   (7075-T6)     \
        /     /               \          \
       /    /                   \         \
      /   /  ◄── Engine case ──► \        \
     /  /                           \       \
    / /                               \      \
   //                                   \     \
  //                                     \    \
  ╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲│╱╲
   Engine mount ring (7075-T6, 3-point)
```

### 3.2 Engine Mount Ring

- **Material:** 7075-T6 aluminium
- **Geometry:** Annular ring, 90 mm ID × 200 mm OD × 6 mm thick
- **Attachment:** 3-point to engine case via M5 bolts on 80 mm PCD
- **Mass:** ~90 g

| Point | Angle   | Fastener | Notes              |
|-------|---------|----------|--------------------|
| P1    | 0° (top)| M5 × 12 | Thrust link        |
| P2    | 120°    | M5 × 12 | Lateral restraint  |
| P3    | 240°    | M5 × 12 | Lateral restraint  |

### 3.3 Mount Legs

- **Quantity:** 4 legs per side (2 forward to BH6, 2 aft to BH7)
- **Material:** 7075-T6 aluminium, 6 mm × 20 mm rectangular bar
- **Angles:** ±45° from horizontal (to resist vertical, lateral, and thrust loads)
- **Length:** ~120 mm (forward), ~150 mm (aft)

```
          BH6 (x=1.40 m)          BH7 (x=1.60 m)
               │                       │
               ├── L1 (+45°) ─────────►│
               │                       │
    Ring ──────┤                       ├────── Ring
               │                       │
               ├── L2 (−45°) ─────────►│
               │                       │
               ├── L3 (+45°) ─────────►│
               │                       │
               ├── L4 (−45°) ─────────►│
               │                       │
               ▲ 200 mm gap            ▲
```

### 3.4 Thrust Load Path

```
  Engine thrust (T ≈ 300 N)
       │
       ▼
  Engine case → 3-point ring → 4 legs (shear)
       │                              │
       ▼                              ▼
  Ring-to-leg bolts (M5)        Leg-to-BH bolts (M5)
       │                              │
       ▼                              ▼
  BH6 / BH7 bulkheads (shear in diaphragm)
       │
       ▼
  Fuselage skin (shear flow → axial)
       │
       ▼
  Reaction at wing root / tail
```

### 3.5 Bolt Schedule

| Joint               | Fastener | Qty | Torque [N·m] | Notes            |
|---------------------|----------|-----|--------------|------------------|
| Ring to engine case | M5 × 12  | 3   | 6            | Loctite 242      |
| Leg to ring         | M5 × 16  | 8   | 6            | 2 per leg end    |
| Leg to BH6          | M5 × 16  | 8   | 6            | Nut plate on BH  |
| Leg to BH7          | M5 × 16  | 8   | 6            | Nut plate on BH  |

---

## 4. Skin Schedule

### 4.1 Thickness Zones

| Zone  | x range [m] | Thickness [mm] | Material        | Layup                | Notes                               |
|-------|-------------|----------------|-----------------|----------------------|-------------------------------------|
| Nose  | 0.00–0.30   | 0.8            | Carbon-epoxy    | [0/90/±45] (4 ply)   | Erosion resistance, hard tip        |
| Fwd   | 0.30–0.80   | 0.6            | Carbon-epoxy    | [0/±45] (3 ply)      | General forebody                    |
| Waist | 0.80–1.00   | 1.2            | Carbon-epoxy    | [0/90/±45/0/90] (6 ply)| + bonded doubler 0.6 mm            |
| Wing  | 1.00–1.40   | 0.8            | Carbon-epoxy    | [0/90/±45] (4 ply)   | Wing carry-through region           |
| Eng   | 1.20–1.80   | 1.0            | Carbon-epoxy    | [0/90/±45/0] (5 ply) | Heat & vibration, overlaps wing     |
| Aft   | 1.40–2.00   | 0.6            | Carbon-epoxy    | [0/±45] (3 ply)      | (overlaps engine zone aft of 1.80)  |
| Tail  | 2.00–2.20   | 0.6            | Carbon-epoxy    | [0/±45] (3 ply)      | Tail cone, conical layup            |

### 4.2 Layup Details

| Ply schedule | Thick    | Stacking sequence                        |
|--------------|----------|------------------------------------------|
| [0/90/±45]  | 0.8 mm   | 0°, 90°, +45°, −45°                      |
| [0/±45]     | 0.6 mm   | 0°, +45°, −45°                           |
| [0/90/±45/0/90] | 1.2 mm | 0°, 90°, +45°, −45°, 0°, 90°           |
| [0/90/±45/0] | 1.0 mm  | 0°, 90°, +45°, −45°, 0°                 |

Each ply: 0.20 mm cured prepreg (T300/Epoxy).

### 4.3 Waist Doubler

Location: x = 0.80–1.00 m

- Base skin: 0.6 mm [0/±45]
- **Bonded doubler:** 0.6 mm [0/90] bonded on inner surface with Araldite 420
- Total: 1.2 mm
- Doubler extends 50 mm past waist pinch on each side
- Edge taper: 10:1 scarf to base skin over 6 mm

```
  Section at waist (x = 1.0 m):

    Outer surface ───────────────────────
                   0.6 mm base skin [0/±45]
    Bond line ───────────────────────────
                   0.6 mm doubler [0/90]
    Inner surface ───────────────────────
```

### 4.4 Skin-to-Bulkhead Interface

Each bulkhead is bonded to the skin with an epoxy fillet:

```
            BH ring
          ╱──────╲
    Skin ┤        ├  Skin
         │        │
         │ ┌──────┤
         │ │Epoxy │
         │ │fillet│
         │ └──────┤
         │        │
          ╲──────╱
```

Fillet radius: 3 mm, Hysol EA 9394. Shear area: ~30 mm width × π × D.

---

## 5. Access Hatches

### 5.1 Hatch Locations

| Hatch | x range [m] | Size [mm]  | Location | Purpose                    |
|-------|-------------|------------|----------|----------------------------|
| H1    | 0.30–0.60   | 120 × 200  | Top      | Avionics + fuel access     |
| H2    | 1.30–1.80   | 150 × 450  | Bottom   | Engine access              |

### 5.2 Hatch Details

**H1 — Top Avionics/Fuel Hatch (0.30–0.60 m)**

```
             Top view

      ┌───────────────────────────────────┐
      │                                   │
      │   ┌───────────────────────────┐   │  Fuselage skin
      │   │ ╔═══════════════════════╗ │   │
      │   │ ║    HATCH  H1         ║ │   │
      │   │ ║  120 × 200 mm       ║ │   │
      │   │ ║  (cutout)           ║ │   │
      │   │ ╚═══════════════════════╝ │   │
      │   └───────────────────────────┘   │
      │                                   │
      └───────────────────────────────────┘
      ▲               ▲                   ▲
     x=0.30          x=0.60             x=0.80
```

- **Construction:** 0.8 mm carbon-epoxy [0/90/±45], same as nose skin
- **Edge:** 5 mm wide flange, recessed 1 mm for flush fit
- **Seal:** Closed-cell silicone foam, 3 mm × 4 mm, compression 50 %
- **Latching:** 4 × neodymium magnets (N42, 10 mm dia × 3 mm), potted into hatch rim; steel keeper plates bonded to fuselage frame
- **Retention:** Safety wire tether (fail-safe)

**H2 — Bottom Engine Hatch (1.30–1.80 m)**

```
             Bottom view

      ┌───────────────────────────────────────────┐
      │                                           │
      │   ┌───────────────────────────────────┐   │
      │   │ ╔═══════════════════════════════╗ │   │
      │   │ ║    HATCH  H2                 ║ │   │
      │   │ ║  150 × 450 mm               ║ │   │
      │   │ ║  (cutout)                   ║ │   │
      │   │ ╚═══════════════════════════════╝ │   │
      │   └───────────────────────────────────┘   │
      │                                           │
      └───────────────────────────────────────────┘
      ▲                                           ▲
     x=1.30                                      x=1.80
```

- **Construction:** 1.0 mm carbon-epoxy [0/90/±45/0] for heat resistance
- **Edge:** 8 mm flange, recessed 1.5 mm
- **Seal:** Silicone sponge with high-temp rating (250 °C continuous)
- **Latching:** 6 × neodymium magnets (N42, 15 mm dia × 4 mm), plus 2 × quarter-turn Dzus fasteners for positive lock under vibration
- **Heat shield:** 0.3 mm stainless steel foil bonded to inner face (engine-facing side)

### 5.3 Magnetic Latch System Details

```
  Cross-section through hatch edge:

    Fuselage skin (1.0 mm carbon)
      ┌──────────────────────────────┐
      │  ┌────────────────────────┐  │
      │  │  Foam seal (compressed)│  │
      │  │  ┌──────────────────┐  │  │
      │  │  │ Magnetic latch    │  │  │
      │  │  │ ┌────┐  ┌────┐  │  │  │
      │  │  │ │Mag │  │Steel│  │  │  │
      │  │  │ │N42 │  │kpr  │  │  │  │
      │  │  │ └────┘  └────┘  │  │  │
      │  │  └──────────────────┘  │  │
      │  └────────────────────────┘  │
      └──────────────────────────────┘
    Hatch panel

  Magnet pull-off force (N42, 10 × 3 mm): ~8 N each
  Total retention force H1: 4 × 8 = 32 N (≈ 3.3 kg)
  Total retention force H2: 6 × 15 = 90 N (≈ 9.2 kg) + Dzus
```

---

## 6. Weight Estimate

### 6.1 Fuselage Skins

| Zone      | x range [m] | Length [m] | Avg Ø [mm] | Area [m²] | Thick [mm] | Vol [cm³] | Density | Mass [g] |
|-----------|-------------|-----------|------------|-----------|------------|-----------|---------|----------|
| Nose (ogive)| 0.00–0.40 | 0.40      | integrate  | 0.088     | 0.8        | 70        | 1.55    | 109      |
| Fwd       | 0.30–0.80  | 0.50      | 196        | 0.308     | 0.6        | 185       | 1.55    | 287      |
| Waist     | 0.80–1.00  | 0.20      | 189        | 0.119     | 1.2        | 143       | 1.55    | 222      |
| Wing      | 1.00–1.40  | 0.40      | 200        | 0.251     | 0.8        | 201       | 1.55    | 312      |
| Engine    | 1.20–1.80  | 0.60      | 200        | 0.377     | 1.0        | 377       | 1.55    | 584      |
| Aft       | 1.40–2.00  | 0.60      | 165(average)|0.311    | 0.6        | 187       | 1.55    | 290      |
| Tail cone | 2.00–2.20  | 0.20      | 66(average)| 0.041     | 0.6        | 25        | 1.55    | 39       |
| **Total** |            |           |            |           |            |           |         | **~1 843 g** |

Notes: Overlaps between zones counted once. Waist area uses mean diameter ≈ 189 mm. Engine and wing zones overlap intentionally — min thickness controls; counted conservatively.

### 6.2 Bulkheads

| BH#  | Diameter [mm] | Thick [mm] | Area (annular) [cm²] | Vol [cm³] | Density | Mass [g] |
|------|--------------|------------|---------------------|-----------|---------|----------|
| BH1  | 78           | 1.0        | (π/4)(78²)          | 4.8       | 1.55    | 7        |
| BH2  | 193          | 1.0        | 29.3                | 29.3      | 1.55    | 45       |
| BH3  | 200          | 1.0        | 31.4                | 31.4      | 1.55    | 49       |
| BH4  | 200→178      | 1.2        | 35.0                | 42.0      | 1.55    | 65       |
| BH5  | 194→178      | 1.2        | 33.0                | 39.6      | 1.55    | 61       |
| BH6  | 200          | 1.0        | 31.4                | 31.4      | 1.55    | 49       |
| BH7  | 200          | 1.0        | 31.4                | 31.4      | 1.55    | 49       |
| BH8  | 97           | 1.0        | 7.4                 | 7.4       | 1.55    | 11       |
| **Total** |        |            |                     |           |         | **~336 g**|

### 6.3 Engine Mount

| Component               | Material  | Mass [g] |
|-------------------------|-----------|----------|
| Mount ring              | 7075-T6   | 90       |
| Legs (8 × 120 mm)       | 7075-T6   | 160      |
| Bolts, nuts, washers    | Steel     | 35       |
| **Total**               |           | **285 g**|

### 6.4 Hatches

| Item         | Material       | Count | Unit mass [g] | Mass [g] |
|--------------|----------------|-------|---------------|----------|
| H1 panel     | Carbon 0.8 mm  | 1     | 58            | 58       |
| H2 panel     | Carbon 1.0 mm  | 1     | 155           | 155      |
| H2 heat shield| SS foil 0.3 mm| 1     | 32            | 32       |
| Magnets H1   | N42            | 4     | 2             | 8        |
| Magnets H2   | N42            | 6     | 5             | 30       |
| Dzus+keepers | Steel          | 2     | 8             | 16       |
| Foam seals   | Silicone       | ~0.4 m| 1.5 g/m       | 1        |
| **Total**    |                |       |               | **~300 g**|

### 6.5 Adhesives & Misc

| Item                  | Mass [g] |
|-----------------------|----------|
| Epoxy fillets (bonds) | 80       |
| Wire harness, tubing  | 50       |
| Paint/primer          | 60       |
| **Total**             | **~190 g**|

### 6.6 Fuselage Mass Summary

| Component     | Mass [g] | % of fuselage |
|---------------|----------|---------------|
| Skins         | 1 843    | 62 %          |
| Bulkheads     | 336      | 11 %          |
| Engine mount  | 285      | 10 %          |
| Hatches       | 300      | 10 %          |
| Adhesives/misc| 190      | 6 %           |
| **Total**     | **~2 954 g** | 100 %      |

### 6.7 Total Airframe Mass (Wings + Fuselage)

| Component | Mass [kg] |
|-----------|-----------|
| Wings     | 0.568     |
| Fuselage  | 2.954     |
| **Total** | **3.522 kg** |

Excluding propulsion, avionics, fuel, payload, and landing gear.

---

## 7. Manufacturing Notes

1. **Mold:** CNC-machined split female mold from RenShape 460 or MDF + tooling gelcoat. Two halves (LH/RH) bolted at flange.
2. **Layup sequence:** (a) Gelcoat. (b) Skin plies, vacuum bag, cure at 120 °C/1 bar. (c) Post-cure 2 h at 150 °C. (d) Bond bulkheads with Araldite 420. (e) Bond doubler at waist. (f) Machine cutouts for hatches.
3. **Waist geometry:** Mold must be machined with the pinch contour. Use 5-axis CNC or hand-profiled plug.
4. **Bulkheads:** Cut from prepreg flat sheets on waterjet or CNC router. Cure flat in press. Bond in place using a centring jig.
5. **Engine mount:** Mill ring and legs from 7075-T6 plate. Anodise after machining (Type II, clear).
6. **Hatches:** Lay up in a separate flat mould. Machine recess after cure. Bond magnets with epoxy into pre-drilled pockets.
7. **CofG reference:** Fuselage CofG is estimated at x ≈ 1.05 m (waist region) based on skin distribution. Add ballast in nose if needed to achieve target CG.
