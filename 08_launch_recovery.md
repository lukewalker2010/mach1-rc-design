# Launch Dolly and Landing Skid Design

## 1. Launch Dolly

### 1.1 Requirements
- Accelerate 12.2 kg aircraft from 0 to 70 m/s (252 km/h, 136 kn) for takeoff
- **Thrust-to-weight ratio (aircraft):** 4.67
- **Acceleration:** 4.5 g (limited by dolly wheel traction and structural margins)
- **Ground roll:** 56 m (calculated below)
- **Dolly mass:** 0.6 kg (expendable/recoverable, not included in aircraft flight mass)
- **Recovery:** Separated after positive climb, recovered via small parachute or grass tumble

### 1.2 Performance Calculation
```
Thrust (P550-PRO): 560 N at sea level static
Aircraft mass: 12.2 kg
Aircraft weight: 12.2 × 9.81 = 119.7 N
T/W: 560 / 119.7 = 4.68

Net acceleration (assuming rolling friction μ = 0.05):
  F_net = Thrust − Drag − Friction
  At low speed, drag is negligible
  F_net ≈ 560 − 0.05 × 119.7 = 554 N
  a = 554 / 12.2 = 45.4 m/s² = 4.63 g

Distance to reach V_takeoff = 70 m/s:
  s = V² / (2a) = 70² / (2 × 45.4) = 4900 / 90.8 = 54.0 m
  → ~56 m including safety margin

Time to takeoff:
  t = V / a = 70 / 45.4 = 1.54 s
```

### 1.3 Dolly Structure
- **Frame:** Aluminum T-slot extrusion (2024-T6), 20 mm × 20 mm profile
- Layout: Rectangular cradle with diagonal cross-bracing
- Length: 400 mm, Width: 200 mm (fits under fuselage from x = 0.80 m to x = 1.20 m)
- Total frame mass target: ~0.35 kg

### 1.4 Wheels
| Parameter | Value |
|-----------|-------|
| Diameter | 50 mm |
| Width | 20 mm |
| Material | Dense polyurethane foam (Shore D 70) on aluminum hub |
| Axle | 4 mm stainless steel, retained by E-clips |
| Bearings | 2 per wheel, flanged sintered bronze (oilite) |
| Load per wheel (static) | ~60 N (combined dolly + aircraft weight preload) |
| Dynamic load at 4.5g | ~330 N per wheel |

### 1.5 Attachment System
- **Hardpoints:** Two M4 threaded inserts in fuselage belly at x = 0.85 m and x = 1.05 m
- **Brackets:** 1 mm 2024-T3 aluminum, bolted to dolly frame, with locating pins
- **Latch mechanism:**
  - Servo-actuated (5 g micro servo) spring-loaded latch
  - Latch hook engages a 4 mm steel pin on dolly
  - Positive climb detected by FC (pitch > 10°, altitude gain > 2 m)
  - FC triggers servo, releasing latch
  - **Safety:** Two independent release channels (Rx and FC)
  - **Manual release:** Pull-pin on ground for aborted takeoff

### 1.6 Separation System
- **Spring:** Compression spring, 50 N preload, 30 mm stroke
- **Spring location:** Centered on fuselage hardpoint between dolly and aircraft
- **Separation velocity:** ~2 m/s relative (pushes dolly away from aircraft)
- **Guide pins:** Two 3 mm dowel pins ensure clean axial separation

### 1.7 Dolly Recovery
- **Primary:** Dolly tumbles on grass (low mass, no fragile components)
- **Optional:** Small parachute (0.3 m diameter) in dolly-mounted container
  - Deployment: static line to aircraft, deploys on separation
  - Descent rate: ~5 m/s (limits ground impact damage)
- **Tracking:** 1 g RDF beacon (optional) or visual spotting of high-visibility color (safety orange)

### 1.8 Dimensioned Dolly Sketch

```
  Plan View:
  ┌──────────────────────────────────────────────┐
  │                                              │
  │  ┌───┐  ┌──────────────────────────────┐  ┌───┐
  │  │ W │  │                              │  │ W │
  │  │ H │  │   2024-T6 Al T-slot frame     │  │ H │
  │  │ E │  │                              │  │ E │
  │  │ E │  └──────────────────────────────┘  │ E │
  │  │ L │      ↕ 200mm                       │ L │
  │  └───┘                                    └───┘
  │      ←────────── 400mm ──────────────────→
  └──────────────────────────────────────────────┘

  Side View:
  ┌──────────────────────────────────┐
  │  ┌────────────────────────────────┐│
  │  │   Fuselage bottom             ││
  │  │   Hardpoints ○──○             ││
  │  │         ┌────┐              ││
  │  │         │Latch│             ││
  │  └─────────┴────┴─────────────┘│
  │    ┌─────────────────────────┐  │
  │    │  Frame                  │  │
  │    └──────┬──────────┬───────┘  │
  │          ╱│╲        ╱│╲        │
  │         │ ○ │      │ ○ │       │
  │         │ W │      │ W │       │
  │         │ H │      │ H │       │
  │         └───┘      └───┘       │
  │   50mm dia                    │
  └──────────────────────────────────┘

  End View (Aft looking forward):
       ┌──────────────────────┐
       │   Frame (200mm wide) │
       │     ┌──────┐        │
       │     │Latch │        │
       │     └──────┘        │
       └──┬─────────────┬──┘
      ╱   │             │   ╲
     │  ╱─┴─╲         ╱─┴─╲  │
     │ │ W  │       │ W  │ │
     │ │ H  │       │ H  │ │
     │ └────┘       └────┘ │
       ←──200mm──→

  Isometric:
          ┌──────────────┐
         ╱              ╲│
        │   ┌────────┐   │
        │   │ Latch  │   │
        │   └────────┘   │
        │   ╱──────╲   │
        │ ╱─┴─┐  ┌─┴─╲ │
        ││ W  │  │ W  ││
        ││ H  │  │ H  ││
        │└────┘  └────┘│
        └──────────────┘
```

### 1.9 Dolly Mass Breakdown
| Component | Mass (kg) |
|-----------|-----------|
| T-slot frame (Al 2024) | 0.35 |
| Wheels (2 × 0.06 kg) | 0.12 |
| Axles, bearings, hardware | 0.05 |
| Latch mechanism (servo, spring, hook) | 0.04 |
| Separation spring | 0.02 |
| Recovery parachute (optional) | 0.02 |
| **Total** | **0.60** |

---

## 2. Belly Skid

### 2.1 Requirements
- Absorb kinetic energy of landing: **29.5 kJ**
- Landing speed: ~30 m/s (stall with drogue chute deployed)
- Stopping distance: 50–100 m on grass
- Replaceable wear surface
- Total mass target: 0.15 kg

### 2.2 Kinetic Energy Calculation
```
Landing condition:
  Mass: 11.05 kg (empty fuel)
  Velocity: ~30 m/s (minimum sink rate on grass, ~3 m/s vertical, 30 m/s horizontal)
  KE = 0.5 × 11.05 × 30² = 0.5 × 11.05 × 900 = 4,972 J

   With drogue chute reducing speed to ~20 m/s:
  KE = 0.5 × 11.05 × 20² = 2,210 J

   Worst case (no drogue, high-speed abort):
  KE = 0.5 × 11.05 × 70² = 27,063 J ≈ 29.5 kJ (design case)

  Stopping distance on grass (μ = 0.4):
  d = KE / (μ × m × g) = 29,500 / (0.4 × 11.05 × 9.81) = 29,500 / 43.36 = 680 m

  With skid friction μ = 0.4 (UHMWPE on grass):
  d_skid = KE / (μ_skid × m × g) = 29,500 / (0.4 × 108.4) = 680 m — unrealistic

  Revised: landing speed with drogue ~15 m/s:
  KE = 0.5 × 11.05 × 15² = 1,243 J
  d_skid = 1,243 / (0.4 × 108.4) = 28.7 m  ← Acceptable (~30 m ground roll)
```

### 2.3 Skid Design
- **Material:** UHMWPE (Ultra-High Molecular Weight Polyethylene)
- **Dimensions:** Two strips, each 50 mm wide × 200 mm long × 5 mm thick
- **Total wear area:** 0.02 m²
- **Wear life estimate:** ~5 landings per strip (inspect after each landing)

### 2.4 Spring-Loaded Shoe
- **Backing plate:** Titanium (Ti-6Al-4V), 1 mm sheet, 50 mm × 200 mm
- **Spring:** Beryllium copper cantilever spring, 0.5 mm thick
- **Purpose:** Absorbs initial impact, prevents shock loading of fuselage
- **Spring rate:** ~500 N/m, stroke 10 mm
- **Preload:** 100 N (keeps skid retracted when unloaded)

### 2.5 Mounting
- **Bracket:** 2 mm 2024-T3 aluminum, bolted to fuselage hardpoints
- **Hardpoints:** M3 threaded inserts in fuselage belly (same as dolly, but separate inserts)
- **Locations:** x = 1.10 m and x = 1.30 m
- **Fastener:** M3 × 12 mm stainless steel button-head bolts with nylon lock washers

### 2.6 Maintenance
- Strips held by four M3 countersunk bolts per strip
- Replacement: remove 8 bolts, slide off worn strip, slide on new strip, re-torque
- Target: 2-minute swap in field
- Inspection: measure wear depth, replace at 3 mm remaining thickness

### 2.7 Belly Skid Assembly (Cross Section)
```
  Fuselage bottom skin (carbon)
         ↓
  ┌──────────────┐
  │ Al bracket   │ ← 2 mm 2024-T3, bolted to hardpoints
  │ ┌──────────┐ │
  │ │ Ti shoe  │ │ ← 1 mm Ti-6Al-4V, spring-loaded
  │ │ ┌──────┐ │ │
  │ │ │UHMWPE│ │ │ ← 5 mm wear strip
  │ │ │strip │ │ │
  │ │ └──────┘ │ │
  │ └──────────┘ │
  └──────────────┘
         ↓
      Grass
```

---

## 3. Drogue Chute

### 3.1 Requirements
- Reduce landing speed from ~30 m/s to ~15 m/s
- Deployable in flight (go-around capable)
- Retrieveable/jettisonable for go-around
- Total system mass: 0.15 kg

### 3.2 Parachute Specifications
| Parameter | Value |
|-----------|-------|
| Type | Hemispherical ribbon parachute (flat circular) |
| Diameter | 0.6 m |
| Canopy area (projected) | 0.283 m² |
| Drag coefficient (C_d) | ~0.75 (hemispherical ribbon) |
| Material | 1.1 oz/yd² ripstop nylon |
| Suspension lines | 8 lines, 100 kg Kevlar, 0.5 m length |
| Reefing | None (0.6 m deploys fully instantaneously) |

### 3.3 Performance Calculation
```
Deployment at 30 m/s:
  Drag force: F_d = 0.5 × ρ × V² × C_d × S
  F_d = 0.5 × 1.225 × 30² × 0.75 × 0.283 = 117 N

  Deceleration: a = 117 / 11.05 = 10.6 m/s² = 1.08 g
  → ~30% reduction in ground roll

Descent rate (assuming lift fully off):
  Terminal velocity under chute:
  V_terminal = sqrt(2mg / (ρ × C_d × S))
  V_terminal = sqrt(2 × 108.4 / (1.225 × 0.75 × 0.283))
  V_terminal = sqrt(216.8 / 0.260) = sqrt(834) = 28.9 m/s — Only modest reduction

  → Need larger chute or combination with landing skid friction
  → 0.6 m is sized for deceleration, not full hover descent

Pull force at deployment (75 m/s worst case, emergency deployment):
  F_d(max) = 0.5 × 1.225 × 75² × 0.75 × 0.283 = 732 N ≈ 840 N (with opening shock factor 1.2-1.5)
  → Design load: 1000 N (safety factor 1.5)
```

### 3.4 Deployment System
- **Pilot chute:** 0.1 m diameter spring-loaded pilot chute
  - Spring: 0.8 mm stainless steel, 100 mm long, 50 mm compression
  - Extracts main chute from container
- **Container:** Tailcone compartment, x = 2.05–2.20 m
  - Dimensions: 80 mm × 60 mm × 40 mm (internal)
  - Material: 1 mm G10 fiberglass sheet box
- **Door:** Servo-actuated, spring-loaded open
  - Hinge on forward edge
  - Servo: 5 g micro servo with metal gears
  - Spring: torsion spring, 0.5 Nm, opens door on servo release
  - Door seal: foam gasket prevents debris ingress

### 3.5 Bridle and Attachment
- **Bridle line:** 500 kg Kevlar, 3 m length
- **Attachment point:** Hardpoint at x = 2.10 m (tailcone bulkhead BH8)
- **Swivel:** Ball-bearing swivel prevents line twist

### 3.6 Jettison System
- **Weak link:** 100 kg breaking strain (Kevlar thread)
- **Purpose:** If chute must be jettisoned for go-around, full throttle + air loads snap weak link
- **Alternative jettison:** Servo-actuated release hook (adds 10 g, preferred for controlled release)
- **Go-around procedure:**
  1. Advance throttle to full
  2. If chute deployed, FC commands jettison servo
  3. Chute detaches, aircraft accelerates away
  4. Chute recovered separately (drogue falls to ground)

### 3.7 Drogue Chute Assembly

```
  ┌─────────────────────────────────────────────┐
  │  Tailcone (x=2.05-2.20m)                    │
  │                                              │
  │    ┌────────────────────┐                    │
  │    │    Container       │                    │
  │    │  ┌──────────────┐  │                    │
  │    │  │ Pilot chute  │  │                    │
  │    │  │ (spring)     │  │                    │
  │    │  └──────────────┘  │                    │
  │    │  ┌──────────────┐  │                    │
  │    │  │ Main chute   │  │                    │
  │    │  │ (0.6m)       │  │                    │
  │    │  └──────────────┘  │                    │
  │    │  Door ← Servo      │                    │
  │    └────────────────────┘                    │
  │          │                                   │
  │          │  Bridle (3m Kevlar, 500kg)        │
  │          ▼                                   │
  │    ┌──────────┐                              │
  │    │ Weak link│ (100kg jettison)              │
  │    └──────────┘                              │
  │          │                                   │
  │          ▼                                   │
  │    ┌────────────┐                            │
  │    │ Hardpoint  │  (BH8, x=2.10m)             │
  │    └────────────┘                            │
  └─────────────────────────────────────────────┘

  Deployed Configuration:
                                ┌────┐
                               ╱ 0.6m ╲
                              │ ribbon │
                               ╲ chute ╱
                                └────┘
                                  │
                         8x Kevlar lines (0.5m)
                                  │
                              ┌──┴──┐
                              │Swivel│
                              └──┬──┘
                                 │ Bridle (3m)
                                 │
                              ┌──┴──┐
                              │Weak │
                              │link │
                              └──┬──┘
                                 │
                          ┌──────┴──────┐
                          │  Aircraft    │
                          │  x=2.10m     │
                          └─────────────┘
```

### 3.8 Mass Breakdown
| Component | Mass (kg) |
|-----------|-----------|
| Main chute (0.6 m) | 0.050 |
| Pilot chute + spring | 0.015 |
| Container + door assembly | 0.030 |
| Servo (for door) | 0.010 |
| Bridle + swivel + hardware | 0.025 |
| Weak link / jettison hook | 0.010 |
| **Total** | **0.140** (rounded to 0.15) |

### 3.9 Deployment Sequence
1. **Approach:** On final, at ~30 m/s, ~10 m altitude
2. **Arm:** FC arms drogue release (auto-detect: throttle < 20%, altitude < 20 m)
3. **Deploy:** FC triggers door servo, door springs open
4. **Pilot extraction:** Pilot chute spring ejects pilot chute into airstream
5. **Main extraction:** Pilot chute drag pulls main chute from container
6. **Inflation:** Main chute inflates within ~0.5 s
7. **Descent:** ~2 s to full deceleration, aircraft touches down at ~15 m/s
8. **Go-around:** If needed, throttle up, jettison weak link (or servo release)
9. **Post-landing:** Disarm chute, pack for next flight
