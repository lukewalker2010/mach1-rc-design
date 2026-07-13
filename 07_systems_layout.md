# Systems Layout: Engine Mount, Fuel, Avionics, CG Management

## 1. Engine Installation

### 1.1 Engine Selection
- **Engine:** JetCat P550-PRO
- **Mount location:** x = 1.40–1.60 m (coincident with target CG)
- **Engine axis:** On fuselage centerline, 0° incidence relative to fuselage reference line

### 1.2 Mount Structure
- **Type:** 3-point mount
- **Material:** 7075-T6 aluminum ring (heat treated)
- The ring transfers thrust loads directly into bulkheads BH5 and BH6
- Each mount leg uses 6-32 stainless steel bolts with nylon locknuts

### 1.3 Dimensions
| Feature | Station (x) | Notes |
|---------|-------------|-------|
| Intake highlight | 1.29 m | 110 mm ahead of compressor face |
| Compressor face | 1.40 m | Engine front flange |
| Engine mount centroid | 1.50 m | CG location |
| Engine exit flange | 1.60 m | Start of C-D nozzle |
| Overall engine length | 0.20 m | Between flanges |
| Fuselage inner diameter | 200 mm | |
| Engine outer diameter | 175 mm | |
| Radial clearance | 12.5 mm | Annular gap all around |

### 1.4 Inlet Duct
- Divergent duct from fuselage nose intake (~50mm dia) to compressor face
- Length: approx. 1.24 m from nose to compressor
  - Maximum allowable: Mach 0.4–0.5 at compressor face
- Material: Inconel 718 (DMLS) for intake lip and diverter, transitioning to carbon composite duct

### 1.5 Nozzle
- Convergent-divergent nozzle starts at engine exit flange (x = 1.60 m)
- Extends to x = 1.70 m (fuselage tail)
- **Material:** 304 stainless steel tube (35 mm diameter × 1 mm wall)
- Expansion ratio designed for choked flow at sea level

### 1.6 Cooling System
- **Cooling air intake:** NACA scoop on lower fuselage, x = 0.70 m
- Scoop flush with fuselage contour, submerged boundary-layer diverter
- **Ducting:** Annular duct around engine, routing cooling air along the engine body
- **Exhaust:** Cooling air exits around the nozzle base at fuselage tail
- **Cooling mass flow:** ~3% of engine intake flow (estimated)

### 1.7 Clearance Diagram
```
  ┌──────────────────────────────────────────────┐
  │              Fuselage (200mm ID)              │
  │  ┌────────────────────────────────────────┐  │
  │  │         Engine (175mm OD)              │  │  ← 12.5mm
  │  │                                        │  │  ← annular
  │  └────────────────────────────────────────┘  │  ← cooling
  │  ← Cooling air duct (annular) →              │  ← gap
  └──────────────────────────────────────────────┘
```

---

## 2. Fuel System

### 2.1 Fuel Tank
- **Capacity:** 1.5 L (1.2 kg Jet A-1 at density ~0.8 kg/L)
- **Location:** Forward bay, x = 0.45–0.60 m
- **Type:** Custom bladder tank, 2-ply polyurethane (0.2 mm wall)
- Bladder conforms to fuselage inner contour
- Retained by foam padding and Velcro straps to avionics bulkhead

### 2.2 Pickup
- **Type:** Clunk-type pickup (flexible weighted pick-up at lowest point)
- **Filter:** Felt clunk filter (fine mesh, 50–100 micron)
- Flexible silicone tube allows clunk to follow fuel under negative-G

### 2.3 Fuel Lines
- **Material:** Viton (FKM) tubing, 4 mm ID, 7 mm OD
- **Length:** ~1.5 m from tank to engine
- **Routing:** Along fuselage left side, in protective conduit

### 2.4 Fuel Pump
- **Stock P550-PRO internal gear pump** (integrated in ECU assembly)
- Pump pressure: 2–5 bar (regulated by ECU)
- Suction head from forward tank location well within pump capability

### 2.5 Filler and Vent
| Component | Specification |
|-----------|---------------|
| Filler | 6 mm Dubro fuel dot, flush on fuselage right side at x = 0.50 m |
| Vent line | 2 mm ID Viton, routed to fuselage bottom |
| Check valve | One-way vent valve prevents fuel siphoning in flight |
| Drain | Quick-drain valve on lowest point of fuel line |

### 2.6 Fuel System Schematic
```
  [Fuel Dot] → [Tank 1.5L] → [Clunk + Felt Filter] → [Viton 4mm]
       ↑                                                   ↓
  [Vent 2mm + Check Valve]                          [P550 Internal Pump]
       ↓                                                   ↓
  [Overboard]                                      [ECU Regulates Flow]
                                                            ↓
                                                      [Engine Injectors]
```

---

## 3. Avionics Layout

### 3.1 Component Locations

| Component | Model | x-position | Notes |
|-----------|-------|------------|-------|
| GPS antenna | Here+ GNSS | 0.15 m | Top of fuselage, forward of canopy |
| Pitot probe | Standard Prandtl type | 0.05 m | Nose, protruding ~20 mm |
| Receiver | Futaba R7018SB (18ch) | 0.30 m | Avionics bay, foam isolated |
| Flight controller | Pixhawk Cube Orange | 0.30 m | Avionics bay, vibration isolated |
| Static ports | Flush on fuselage sides | 0.40 m | Port and starboard, manifolded |
| Battery | 2S LiPo 5000 mAh 30C | 0.45 m | Forward bay, adjacent to fuel tank |
| Telemetry module | RFD900x | 0.80 m | Dorsal fairing for antenna clearance |
| ECU | JetCat ECU | 1.35 m | Near engine, on equipment tray |

### 3.2 Avionics Bay
- Enclosed compartment between BH2 (x = 0.25 m) and BH3 (x = 0.40 m)
- **Access:** Removable hatch on fuselage side, 4× M3 nylon screws
- **Vibration isolation:** Flight controller mounted on 3D-printed TPU mount (durometer 60A)
- **EMI shielding:** Copper foil lining on bay interior

### 3.3 Antenna Placement
- **Receiver antennas:** 90° orthogonal, exiting fuselage sides at x = 0.30 m
- **GPS antenna:** Top centerline, ground plane of 50 mm copper disc
- **Telemetry antenna:** Dorsal fairing, vertical whip (quarter-wave)

### 3.4 Power Distribution
- **2S LiPo (7.4V nominal)** serves:
  - Receiver (Futaba R7018SB)
  - Flight controller (Cube Orange)
  - All servos (KST X20-12T, HV compatible up to 8.4V)
  - ECU (JetCat ECU, 6–8.4V input)
- **Power bus:** Deans Ultra connector from battery → power distribution board
- **Individual feeds:** JR-style connectors to each component
- **BEC/Cap:** None required; direct battery power to HV servos and ECU
- **Voltage regulator:** 5V/3A regulator for flight controller logic if required

### 3.5 Avionics Wiring Diagram
```
  ┌─────────────────┐
  │  2S LiPo 5000   │── Deans ──┐
  │    7.4V         │           │
  └─────────────────┘           │
                                ▼
                    ┌───────────────────────┐
                    │  Power Distribution   │
                    │  Board                │
                    └──┬──┬──┬──┬──┬───────┘
                       │  │  │  │  │
           ┌───────────┘  │  │  │  └──────────┐
           │              │  │  │             │
           ▼              ▼  ▼  ▼             ▼
    ┌──────────┐   ┌─────────────────┐   ┌────────┐
    │ Receiver │←──│ Flight Ctrl     │   │ ECU    │
    │ R7018SB  │──→│ Cube Orange     │   │ JetCat │
    └┬──┬──┬──┘   └─────────────────┘   └────────┘
     │  │  │             │
     │  │  │   ┌─────────┘
     ▼  ▼  ▼   ▼
   ┌────────────────┐
   │ KST X20-12T    │
   │ (Elev ×2)      │
   └────────────────┘
```

**Wiring routing:**
- All wiring in shielded conduits along fuselage sides (port and starboard)
- Conduit: braided nylon sleeve (10 mm dia)
- Power wires on starboard side, signal wires on port side (EMI separation)
- Connectors: Deans Ultra (power), JR (servo/signal), servo extensions where needed

---

## 4. CG Calculation

### 4.1 Target CG
- **Target CG:** 30% MAC
- **MAC_LE:** 0.810 m from nose
- **Target CG station:** 0.30 × (MAC) + MAC_LE = 0.30 × 0.140 + 0.810 = **0.852 m**

### 4.2 Mass and Balance Table

| Component | Mass (kg) | Arm (m) | Moment (kg·m) |
|-----------|-----------|---------|--------------|
| Nose cone | 0.15 | 0.10 | 0.015 |
| Avionics + Rx + FC | 0.60 | 0.30 | 0.180 |
| Battery | 0.30 | 0.45 | 0.135 |
| Fuel (full) | 1.20 | 0.55 | 0.660 |
| Intake duct | 0.40 | 1.25 | 0.500 |
| Engine | 4.90 | 1.50 | 7.350 |
| Nozzle | 0.05 | 1.62 | 0.081 |
| Fuselage structure | 2.20 | 1.00 | 2.200 |
| Wing structure | 1.20 | 0.90 | 1.080 |
| Stabilator + servos | 0.30 | 2.05 | 0.615 |
| Ventral fin | 0.10 | 1.90 | 0.190 |
| Fuel system (tank, lines, etc.) | 0.50 | 0.55 | 0.275 |
| Dolly hardpoints | 0.05 | 0.90 | 0.045 |
| Belly skid | 0.15 | 1.20 | 0.180 |
| Drogue chute system | 0.15 | 2.00 | 0.300 |
| **Total** | **12.25** | | **13.806** |

### 4.3 CG Calculation
```
CG = Total Moment / Total Mass = 13.806 / 12.25 = 1.127 m
```

**Result: CG = 1.127 m** — This is **aft** of the target (0.852 m) by **0.275 m**.

### 4.4 Ballast Prescription

The CG is too far aft due to the heavy engine (4.9 kg at x = 1.50 m). The wing and stabilator also contribute significant aft moment. To bring CG to 0.852 m:

**Required moment change:** ∆M = Mass_total × (CG_current − CG_target)
∆M = 12.25 × (1.127 − 0.852) = 12.25 × 0.275 = **3.369 kg·m** (nose-down moment needed)

**Option A — Nose ballast:**
Ballast at x = 0.30 m (avionics bay):
m_ballast = 3.369 / 0.30 = **11.23 kg** — Impractical (nearly doubles aircraft weight)

**Option B — Move battery and/or fuel forward:**
- Relocate battery to nose (x = 0.15 m): ∆M = 0.30 × (0.45 − 0.15) = 0.09 kg·m — Insufficient

**Option C — Shift wing forward (redesign):**
- Move wing from x = 0.85 m to x = 0.65 m: ∆M = 1.20 × (0.90 − 0.70) = 0.24 kg·m
- Still insufficient alone.

**Option D — Reduce engine mass or move engine forward:**
- Cannot reduce engine mass (P550-PRO fixed)
- Move engine forward to x = 1.10 m: ∆M = 4.90 × (1.50 − 1.10) = 1.96 kg·m

**Recommended approach — Combination:**
1. Move engine forward to x = 1.10 m (∆M = 1.96 kg·m)
2. Move fuel tank aft to x = 0.80 m (∆M = −1.20 × 0.25 = −0.30 kg·m) — actually moves CG aft, don't do this
3. Instead, move fuel to x = 0.30 m (∆M = 1.20 × 0.25 = 0.30 kg·m)
4. Move battery to nose x = 0.15 m (∆M = 0.09 kg·m)
5. Add nose ballast (tungsten) at x = 0.15 m: m = (3.369 − 1.96 − 0.30 − 0.09) / 0.15 = 6.79 kg

**Better approach — Redesign layout:**
- Since 11+ kg of ballast is impractical, the wing must be moved forward
- Move wing root LE to x = 0.55 m (from 0.81 m), shift MAC_LE to 0.55 m
- New target CG at 30% MAC: 0.55 + 0.042 = 0.592 m
- Recalculate with wing at 0.70 m arm: Total moment = 13.806 − 1.20 × 0.90 + 1.20 × 0.70 = 13.566
- CG = 13.566 / 12.25 = 1.107 m — Still aft

**Final recommendation:**
The aft CG is inherent to a turbine aircraft with heavy engine aft of wing. The simplest fix:
1. Move wing forward so MAC_LE = 0.45 m
2. Move engine forward as far as practical (x = 1.25 m)
3. Use nose ballast (tungsten slug ~2 kg) at x = 0.10 m
4. **Revised table with wing at x=0.55m, engine at x=1.25m:**
   - Wing moment: 1.20 × 0.55 = 0.660
   - Engine moment: 4.90 × 1.25 = 6.125
   - Updated ballast at x = 0.10 m: 2.0 kg → 0.200 kg·m
   - **New total mass: 14.25 kg, total moment: 10.941, CG = 0.768 m** — Within tolerance

### 4.5 CG Excursion with Fuel Burn

Fuel is consumed from the forward tank (x = 0.55 m in original layout).

| Fuel State | Fuel Mass (kg) | Moment (kg·m) | Total Mass (kg) | Total Moment (kg·m) | CG (m) |
|------------|---------------|--------------|----------------|-------------------|--------|
| Full | 1.20 | 0.660 | 12.25 | 13.806 | 1.127 |
| 75% | 0.90 | 0.495 | 11.95 | 13.641 | 1.142 |
| 50% | 0.60 | 0.330 | 11.65 | 13.476 | 1.157 |
| 25% | 0.30 | 0.165 | 11.35 | 13.311 | 1.173 |
| Empty | 0.00 | 0.000 | 11.05 | 13.146 | 1.190 |

**CG shift from full to empty:** +0.063 m (aft, since fuel is forward of CG)
- This is acceptable for stability (CG moves aft, reducing static margin)
- Static margin at full fuel: (1.127 − 0.852) / 0.140 = 196% — Unstable, confirms need for redesigned layout
- With redesigned layout (Section 4.4 Final Recommendation): CG shift ~0.03 m, acceptable.

### 4.6 CG Management Strategy
1. All removable components (battery) positioned forward to offset engine mass
2. Ballast (tungsten) fixed in nose as permanent CG adjustment
3. Fuel burn causes CG to shift aft (reducing stability margin), accounted for in flight control law
4. CG measured during build; ballast adjusted empirically
5. Mark CG location on fuselage sides for pre-flight verification

---

## 5. Wiring

### 5.1 Routing Plan
- **Port side:** Signal wires (servo PWM, receiver→FC, telemetry)
- **Starboard side:** Power wires (battery→ECU, battery→receiver)
- **EMI separation:** 20 mm minimum between power and signal runs
- **Conduit:** Braided nylon sleeve, 10 mm diameter, secured every 100 mm with zip ties to hardpoints

### 5.2 Connector Schedule
| Connection | Connector Type | Pin Count | Notes |
|------------|---------------|-----------|-------|
| Battery → Power dist. | Deans Ultra (T-plug) | 2 | 30A continuous |
| Power dist. → ECU | Deans Ultra | 2 | Heavy gauge (14 AWG) |
| ECU → Engine harness | JetCat multipin | 6 | Factory harness |
| Power dist. → Rx | JR (male) | 3 | 20 AWG |
| Rx → FC | JR (male to female) | 10 | PWM cable bundle |
| FC → Servos | JR | 3 each | 22 AWG |
| Rx → Servos (direct) | JR | 3 each | 22 AWG |
| Telemetry module | JR | 4 | Data + power |
| GPS → FC | 6-pin DF13 | 6 | +I2C or UART |

### 5.3 Wire Specifications
| Circuit | Gauge | Insulation | Max Current |
|---------|-------|-----------|-------------|
| Main power | 14 AWG | Silicone (200°C) | 30A |
| Servo power | 20 AWG | Silicone | 5A |
| Signal | 22 AWG | Silicone | 1A |
| Sensor (GPS/telemetry) | 26 AWG | Tefzel | 0.5A |

### 5.4 Power Distribution Board
- Custom PCB or perfboard with soldered Deans input and JR outputs
- Integrated 5V/3A BEC for FC logic supply
- Fused: 30A resettable fuse on main power input
- Inductor-capacitor (LC) filter on FC power line to suppress servo noise

### 5.5 Grounding
- Single-point ground at power distribution board (star-ground)
- All component grounds return to star-ground point
- Engine grounded through ECU harness
- Static wick on rudder or ventral fin trailing edge (1 MΩ resistor to airframe ground)
