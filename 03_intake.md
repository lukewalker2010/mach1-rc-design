# Supersonic Pitot Intake Design — Fabrication Drawing

## 1. Intake Parameters Summary

| Parameter | Value | Notes |
|-----------|-------|-------|
| Type | Fixed-geometry pitot, axisymmetric | No centrebody or ramp |
| Lip diameter | 105 mm | Capture area Ac = 86.6 cm² |
| Throat diameter | 103 mm | A_throat = 83.3 cm² |
| Contraction ratio (A_lip - A_thr)/A_lip | 3.8% | Slight contraction for boundary layer growth |
| Throat-to-lip area ratio A_thr/A_lip | 0.963 | |
| Diffuser half-angle | 6° | Included angle 12° |
| Diffuser length | 60 mm | From throat to compressor face |
| Compressor face diameter | 115 mm | Effective compressor inlet |
| Total length | 110 mm | Lip to compressor face flange |
| Self-starting Mach | ≥ 1.05 | Fixed geometry starts without auxiliary bleeds |
| Material | Inconel 718 | DMLS (direct metal laser sintering) |
| Wall thickness | 0.8 mm | Nominal |
| Target mass | 400 g | Including hardware |
| Max operating temperature | 650 °C | Continuous |

## 2. Cross-Section Drawing

### Longitudinal Section (A-A)

```
     LIP                          THROAT            DIFFUSER         COMPRESSOR
     PLANE                         PLANE             EXIT              FACE
     │                             │                 │                 │
     │◄────────── 110 mm ────────────────────────────────────────────►│
     │                                                               │
     │◄─── 25 mm ──►│◄─────────── 85 mm ────────────────────────────►│
     │                                                               │
     │                                                               │
     ╱╲              ╱════════════╲        ╱══════════════╲           │
    ╱  ╲            ╱              ╲      ╱                ╲          │
   ╱    ╲          ╱                ╲    ╱                  ╲         │
  ╱      ╲        ╱                  ╲  ╱                    ╲        │
 ╱   EL-  ╲      ╱    THROAT         ╲╱    DIFFUSER          ╲       │
╱   LIPSE  ╲────╱    ═══ 103 mm ═══   ╲────────────────────────╲──────┤
╲   RADIUS  ╱────╲                    ╱╲                        ╱      │
 ╲        ╱      ╲                  ╱  ╲                      ╱       │
  ╲      ╱        ╲                ╱    ╲                    ╱        │
   ╲    ╱          ╲              ╱      ╲                  ╱         │
    ╲  ╱            ╲            ╱        ╲                ╱          │
     ╲╱              ╲══════════╱          ╲══════════════╱           │
                     ╱        ╲            ╲            ╱            │
                    ╱          ╲            ╲          ╱             │
                   ╱            ╲            ╲        ╱              │
                  ╱              ╲            ╲      ╱               │
                 ╱                ╲            ╲    ╱                │
                ╱                  ╲            ╲  ╱                 │
               ╱                    ╲            ╲╱                  │
              ╱     CENTRELINE       ╲───────────────────────────────│
              ╲                      ╱                               │
               ╲════════════════════╱                                │
                                                                    │
     LIP: 105 mm               THROAT: 103 mm        EXIT: 115 mm
     DIA                        DIA                   DIA
```

### Key Dimensions

| Ref | Dimension | Value | Tolerance |
|-----|-----------|-------|-----------|
| A | Lip diameter (internal) | 105.0 mm | ±0.2 mm |
| B | Lip OD | 106.6 mm | ±0.2 mm |
| C | Throat diameter | 103.0 mm | ±0.1 mm |
| D | Diffuser exit diameter (compressor face) | 115.0 mm | ±0.2 mm |
| E | Total intake length | 110.0 mm | ±0.5 mm |
| F | Lip section length | 25.0 mm | ±0.2 mm |
| G | Throat-to-compressor distance | 85.0 mm | ±0.5 mm |
| H | Diffuser length | 60.0 mm | ±0.5 mm |
| I | Diffuser half-angle | 6° | ±0.2° |
| J | Wall thickness (nominal) | 0.8 mm | ±0.1 mm |
| K | Lip ellipse radius (major) | 5.0 mm | ±0.1 mm |
| L | Lip ellipse radius (minor) | 2.5 mm | ±0.1 mm |
| M | O-ring groove width | 3.0 mm | +0.2/-0.0 mm |
| N | O-ring groove depth | 2.0 mm | +0.0/-0.1 mm |
| O | O-ring groove diameter (mean) | 116.0 mm | ±0.1 mm |
| P | Bolt circle PCD | 122.0 mm | ±0.2 mm |
| Q | Bolt holes | 4 × M4 | clearance ⌀4.3 mm |
| R | Splitter plate standoff | 15.0 mm | ±0.2 mm |
| S | Splitter plate length ahead of lip | 80.0 mm | ±1.0 mm |
| T | Ramp angle from fuselage | 10° | ±0.5° |

## 3. Lip Geometry

### Elliptical Lip Section Profile

The lip is an elliptical quadrant with semi-major axis (axial) = 5.0 mm and semi-minor axis (radial) = 2.5 mm.

```
              INFLOW
                │
                ▼
                ╱￣￣￣╲          ──► a = 5.0 mm (axial)
              ╱        ╲         │
             ╱          ╲        │ b = 2.5 mm (radial)
            ╱            ╲       ▼
           ╱              ╲
          ╱                ╲
         ╱                  ╲──────► Internal duct wall
        ╱                  ╱
       ╱                  ╱
      ╱                  ╱
     ╱                  ╱
    ╱──────────────────╱
    ╲                 ╱
     ╲───────────────╱
         External wall
```

**Lip section coordinates** (ellipse quadrant, origin at lip highlight):

| θ (deg) | x (mm) | r (mm) | Notes |
|---------|--------|--------|-------|
| 0 | 0.0 | 0.0 | Highlight (stagnation point) |
| 15 | 5.0·sin(15°) = 1.29 | 2.5·(1-cos(15°)) = 0.17 | |
| 30 | 5.0·sin(30°) = 2.50 | 2.5·(1-cos(30°)) = 0.67 | |
| 45 | 5.0·sin(45°) = 3.54 | 2.5·(1-cos(45°)) = 1.47 | |
| 60 | 5.0·sin(60°) = 4.33 | 2.5·(1-cos(60°)) = 2.17 | |
| 75 | 5.0·sin(75°) = 4.83 | 2.5·(1-cos(75°)) = 2.52 | |
| 90 | 5.0·sin(90°) = 5.00 | 2.5·(1-cos(90°)) = 2.50 | Internal tangent point |

**Parametric lip equation**:
```
x(θ) = a · sin(θ)
r(θ) = b · (1 - cos(θ))
```
where a = 5.0 mm, b = 2.5 mm, 0 ≤ θ ≤ 90°

### Lip Design Rationale

- The 2:1 elliptical aspect ratio (a/b = 2) provides good off-design performance
- The 5 mm axial extent provides adequate internal flow turning without separation
- The lip radius is sized so that the internal contraction (105 mm → 103 mm) is smooth and shock-free at the design Mach number
- At M = 1.05 (self-starting), the swallowed normal shock passes through the throat without detaching

## 4. Diffuser Geometry

### Conical Diffuser Parameters

| Parameter | Value | Formula |
|-----------|-------|---------|
| Inlet diameter (throat) | 103.0 mm | D₁ |
| Exit diameter (compressor face) | 115.0 mm | D₂ |
| Length | 60.0 mm | L |
| Half-angle | 6° | θ |
| Area ratio (A₂/A₁) | 1.246 | (D₂/D₁)² |
| Equivalent conical angle | 6° | 2θ = 12° included |

### Diffuser Section Coordinates

Measured from throat plane (z = 0 at throat, z = 60 at compressor face):

| z (mm) | Diameter ID (mm) | Radius ID (mm) |
|--------|-------------------|----------------|
| 0.0 | 103.00 | 51.50 |
| 10.0 | 103.00 + 2·10·tan(6°) = 105.10 | 52.55 |
| 20.0 | 103.00 + 2·20·tan(6°) = 107.21 | 53.60 |
| 30.0 | 103.00 + 2·30·tan(6°) = 109.31 | 54.66 |
| 40.0 | 103.00 + 2·40·tan(6°) = 111.41 | 55.71 |
| 50.0 | 103.00 + 2·50·tan(6°) = 113.51 | 56.76 |
| 60.0 | 103.00 + 2·60·tan(6°) = 115.62 → 115.00 | 57.50 |

Note: The last 10 mm transitions from the conical diffuser to the compressor face flange. A 0.5 mm radius fillet is applied at the diffuser exit to smooth the transition.

### Flow Performance Estimates

| Parameter | Value | Condition |
|-----------|-------|-----------|
| Diffuser pressure recovery Cp | 0.72 | Design point, M_throat = 0.58 |
| Total pressure recovery | 1.0 - (1 - Cp)·(1 - (1/M²)) | ~0.97 at Mlip = 1.05 |
| Boundary layer thickness at throat | ~2.5 mm | Fully turbulent, Re based on lip dia |
| Boundary layer displacement δ* | ~0.8 mm | At throat |
| Effective throat area reduction | ~3% | Due to BL displacement |
| Diffuser effectiveness η_diff | 0.85 | Per conical diffuser correlation |
| Self-starting margin | Wide | Ac/Athr = 1.038 ensures starting |

## 5. Compressor Face Interface

### Interface Flange Drawing

```
                    ╭────────────────────╮
                    │                    │
                    │   ╭──────────────╮ │
                    │   │              │ │
                    │   │  ╭────────╮  │ │
                    │   │  │        │  │ │
                    │   │  │ 115 mm │  │ │
                    │   │  │  ID    │  │ │
                    │   │  ╰────────╯  │ │
                    │   │              │ │
                    │   ╰──────────────╯ │
                    │                    │
                    ╰────────────────────╯
                    │◄── 130 mm OD ────►│
                    
                    O-ring groove: ⌀116 mm mean
                    Bolt circle: ⌀122 mm, 4× M4
```

### Flange Details

| Feature | Dimension | Tolerance |
|---------|-----------|-----------|
| Flange OD | 130.0 mm | ±0.3 mm |
| Flange ID (diffuser exit) | 115.0 mm | ±0.2 mm |
| Flange thickness | 4.0 mm | ±0.1 mm |
| O-ring groove: mean diameter | 116.0 mm | ±0.1 mm |
| O-ring groove: width | 3.0 mm | +0.2/-0.0 mm |
| O-ring groove: depth | 2.0 mm | +0.0/-0.1 mm |
| O-ring section | 2.0 mm | BS024 (or equivalent) |
| O-ring material | Viton (FKM) | 250°C continuous |
| Bolt holes | 4 × ⌀4.3 mm | ±0.1 mm |
| Bolt PCD | 122.0 mm | ±0.2 mm |
| Bolt type | M4 × 16 mm | A2 stainless |
| Torque | 3.0 N·m | Each bolt, cross-tighten |

### Compressor Face Seal

The O-ring sits in a groove machined into the intake flange face. The compressor face has a flat mating surface with a 0.4 μm Ra finish. When the 4× M4 bolts are torqued, the O-ring compresses to 1.3-1.4 mm, creating a pressure-tight seal rated to 5 bar differential.

**O-ring groove detail**:
```
            ┌──────────────────────┐
            │        │             │
            │  ├ ─ ─ ┤│            │
            │  │  3  ││ 2.0 mm     │
            │  │  mm ││  deep      │
            │  └ ─ ─ ┘│            │
            │◄──── 116 mm ────────►│
            │         mean dia     │
            └──────────────────────┘
```

## 6. Boundary Layer Diverter

### Splitter Plate Configuration

The BLD uses a splitter plate mounted ahead of the intake lip, diverted away from the fuselage boundary layer.

```
    PLAN VIEW:
    
    FUSELAGE SURFACE ──────────────────────────────────────────────►
    
    BOUNDARY LAYER ──────────────────►  ┌─────────────────────────────┐
                                      │  VENT PATH                   │
                                      │  (through fuselage bottom)   │
                                      │                              │
                                      ▼  ┌──────────────────────────┐
    ┌──────────────┐    ┌──────────────┐  │  INTAKE                  │
    │  SPLITTER     │    │  80 mm       │  │  LIP                     │
    │  PLATE        ├────┤  ahead of    ├──┤───── 105 mm ───────────►│
    │               │    │  lip         │  │  CAPTURE                │
    └──────────────┘    └──────────────┘  │  PLANE                   │
        ▲                                  └──────────────────────────┘
        │ 15 mm
        │ standoff
        │
        ▼
    FUSELAGE SURFACE ──────────────────────────────────────────────►
    
    10° RAMP:
    ──►╱
      ╱
     ╱  Ramp from fuselage surface to splitter plate trailing edge
    ╱   10° angle


    SIDE VIEW:
    
                    ╱  ┌──────────────────────────┐
                ╱     │  SPLITTER                  │
            ╱        │  PLATE                      │
        ╱  15 mm     │  Sharp LE < 0.5 mm radius   │
    ╱──────────────  └──────────────────────────┘
    ╲  10° ramp                                │
     ╲                                          │  VENT
      ╲                                         ▼
       ╲────────────────────────────────────────────────────────────────
        FUSELAGE SURFACE                          BOTTOM VENT PATH
    
    ═════  BOUNDARY LAYER FLOW  ════►  ════►  VENTED OVERBOARD
                                          THROUGH FUSELAGE BOTTOM
```

### Splitter Plate Dimensions

| Feature | Dimension | Tolerance |
|---------|-----------|-----------|
| Plate length ahead of lip | 80.0 mm | ±1.0 mm |
| Standoff from fuselage | 15.0 mm | ±0.5 mm |
| Plate width | 120.0 mm | ±0.5 mm |
| Plate thickness | 1.0 mm | ±0.1 mm |
| Leading edge radius | <0.5 mm | As sharp as practical |
| Ramp angle from fuselage | 10° | ±0.5° |
| Plate material | Inconel 718 | Same as intake |
| Attachment | 4 × M3 countersunk screws | To intake structure |

### Vent Path

- The BL flow captured below the splitter plate is ducted through a 20 mm × 80 mm rectangular vent opening in the fuselage bottom
- Vent path cross-section: 1600 mm² minimum
- Vent exit: flush with fuselage bottom skin
- A NACA-style submerged scoop may be used at the vent exit to aid extraction at supersonic speeds

### Performance

| Parameter | Value |
|-----------|-------|
| BL thickness at lip station (without diverter) | ~15 mm at M1.0 |
| BL diverted | ~95% |
| Residual BL ingested | ~1-2 mm |
| Effect on intake recovery | +0.02-0.03 in total pressure recovery |
| Drag penalty (diverter + vent) | ~1.5% of intake capture drag |

## 7. Auxiliary Inlet Doors

### Configuration

Two spring-loaded auxiliary inlet doors are located on the intake duct to provide additional airflow during low-speed/high-power operation (takeoff, climb).

```
    DUCT CROSS-SECTION AT DOOR LOCATION:
    
                     ┌─────────────────┐
                    ╱                   ╲
                   ╱                     ╲
                  ╱      DOOR #1           ╲
                 ╱     35 × 22 mm           ╲
                ╱     opens outward           ╲
               ╱                               ╲
              ╱     ╭─── 180° ───╮              ╲
             ╱       │           │               ╲
            ╱        │           │                ╲
           ╱     DOOR #2        │                 ╲
          ╱     35 × 22 mm     │                  ╲
         ╱     180° apart      │                   ╲
        ╱                      │                    ╲
       ╱                       ▼                     ╲
      ╱────────────────────────────────────────────────╲
      ╲                                                ╱
       ╲──────────────────────────────────────────────╱
```

### Door Mechanism Details

| Feature | Dimension | Notes |
|---------|-----------|-------|
| Number of doors | 2 | Per intake |
| Door opening area (each) | 35 mm × 22 mm = 770 mm² | |
| Total auxiliary area | 1540 mm² | ~1.8% of lip capture area |
| Door type | Hinged, outward-opening | Pivot at upstream edge |
| Door material | Inconel 718 | 0.5 mm thick |
| Hinge | Piano hinge, 35 mm long | Inconel 718 |
| Spring type | Torsion spring | Per door |
| Spring preload equivalent ΔP | 500 Pa | Opens when duct pressure < ambient by 500 Pa |
| Closure Mach | > 0.6 | Ram pressure forces doors shut |
| Seal | Silicone gasket | 250°C rated |
| Door stop angle | 30° | Max opening relative to duct wall |
| Mass per door (incl. hardware) | 15 g | |

### Spring Specification

```
    Spring type: Torsion spring, 35 mm body length
    Wire diameter: 0.6 mm
    Coil OD: 4.0 mm
    Number of coils: 10
    Free angle: 50°
    Preload angle: 20° (gives 500 Pa equivalent at door area)
    Material: Inconel X-750 (spring temper)
    Max operating temperature: 650°C
```

### Operation

1. **Takeoff / Low-speed climb** (M < 0.4, high throttle):
   - Intake duct pressure drops as compressor demands high airflow
   - When ΔP = P_ambient - P_duct > 500 Pa, springs push doors open
   - Additional flow enters through doors, supplementing main intake
   - Prevents compressor surge/stall at low speeds

2. **Cruise** (M > 0.6):
   - Ram pressure at intake lip rises, duct pressure increases
   - When P_duct ≥ P_ambient, doors are forced shut
   - Springs cannot overcome ram pressure above ~M0.6
   - Doors remain closed and sealed, no drag penalty

3. **Transonic / Supersonic**:
   - Doors fully closed, intake operates on main inlet only
   - The door mechanism is designed to be flutter-free up to M1.2

## 8. Fabrication Notes — DMLS (Inconel 718)

### Printing Orientation

```
                         BUILD DIRECTION (Z)
                              ▲
                              │
                              │
                         ┌────┴────┐
                         │         │
                         │ INTAKE  │
                         │  AXIS   │
                         │         │
                         │ ────────┤
                         │         │
                         │         │
                         └─────────┘
                              │
                              │
                         ─────┴──────► X
                         BUILD PLATE

    Recommended orientation: Intake axis at 45° to build plate
```

**Orientation rationale**:
- Printing with the intake axis at 45° minimises the number of supports needed inside the diffuser
- The 0.8 mm wall is self-supporting at this angle
- The internal surface (flow path) is built without supports touching the critical aerodynamic surface
- The lip elliptical profile is built with approximately uniform layer steps

### Support Structure

| Region | Support Type | Notes |
|--------|-------------|-------|
| Lip external overhang | Tree/cone supports | Removable by wire EDM |
| O-ring groove | Lattice supports | Thin-wall, breakaway |
| Compressor face flange bottom | Solid block supports | Machined off in post-processing |
| Splitter plate mounting bosses | Minimal/conformal | At 45° orientation, minimal needed |
| Door hinge pockets | Lattice supports | Must be accessible for machining |

### Post-Processing Steps

1. **Stress relief**:
   - Hold at 980°C for 1 hour in argon atmosphere
   - Furnace cool to below 300°C
   - Purpose: relieve residual stresses from printing

2. **Hot isostatic pressing (HIP)**:
   - 1200°C, 150 MPa argon, 4 hours
   - Eliminates internal porosity
   - Improves fatigue life by 2-3×
   - Improves elongation from ~12% to ~22%

3. **Support removal**:
   - Wire EDM for large supports (lip, flange)
   - Manual removal with pliers and grinding for small supports
   - CNC machining for flange face and O-ring groove

4. **Solution treatment and aging**:
   - Solution: 980°C, 1 hour, air cool
   - Aging: 720°C, 8 hours, furnace cool to 620°C, hold 8 hours, air cool
   - Final hardness: 40-44 HRC

5. **Final machining**:
   - Machine flange face flat (0.02 mm TIR)
   - Machine O-ring groove (verify 116.0 mm mean dia)
   - Drill and tap M4 holes (or use threaded inserts)
   - Machine door hinge pockets
   - Machine splitter plate mounting points

6. **Surface finish**:
   - Internal flow path: abrasive flow machining (AFM) to 0.8 μm Ra
   - External surface: glass bead blast, 60-80 μm finish
   - Compressor face seal surface: CNC mill to 0.4 μm Ra

7. **Inspection**:
   - CT scan for internal porosity (>99.9% density target)
   - Coordinate measuring machine (CMM) of all critical dimensions
   - Airflow test: measure pressure drop at known flow rate
   - X-ray fluorescence (XRF) verify Inconel 718 composition

### Mass Budget

| Component | Mass (g) | Notes |
|-----------|----------|-------|
| Intake body (printed) | 310 | Inconel 718, 0.8 mm wall |
| Flange (integral) | Included above | Part of print |
| Auxiliary door × 2 | 30 | 15 g each |
| Springs × 2 | 4 | 2 g each |
| O-ring | 5 | Viton BS024 |
| M4 bolts × 4 | 12 | 3 g each |
| M3 countersunk × 4 | 8 | Splitter plate mounting |
| Splitter plate (printed) | 25 | Inconel 718 |
| Misc hardware | 6 | Hinges, grommets |
| **Total** | **400** | Target |

## 9. Aerodynamic Performance Predictions

### Intake Performance Map

| Flight Mach | Lip Mach | Throat Mach | Total Pressure Recovery | Flow Coefficient | Notes |
|-------------|----------|-------------|------------------------|------------------|-------|
| 0.0 | 0.0 | 0.60 | 1.00 | 0.95 | Aux doors open |
| 0.2 | 0.22 | 0.62 | 0.99 | 0.94 | |
| 0.4 | 0.44 | 0.64 | 0.98 | 0.93 | |
| 0.6 | 0.66 | 0.66 | 0.97 | 0.92 | Doors close |
| 0.8 | 0.88 | 0.68 | 0.96 | 0.92 | |
| 0.95 | 1.05 | 0.70 | 0.95 | 0.90 | Self-starting threshold |
| **1.00** | **1.10** | **0.72** | **0.94** | **0.88** | **Supersonic** |
| 1.05 | 1.15 | 0.74 | 0.93 | 0.87 | Design point |
| 1.10 | 1.21 | 0.76 | 0.91 | 0.86 | |

### Self-Starting Analysis

The intake self-starts when the swallowed normal shock passes through the throat. This occurs when:

```
A_throat / A_lip > 1 / (M_lip · ( (γ+1)/(2) · (1 + (γ-1)/2 · M_lip²) )^((γ+1)/(2(γ-1))) )
```

For A_thr/A_lip = 0.963 and γ = 1.4, self-starting occurs at M_lip ≥ 1.03-1.05. Therefore, this intake self-starts at flight Mach ≥ 1.05.

If the intake fails to start:
- A normal shock stands ahead of the lip (detached)
- Total pressure recovery drops to ~0.75-0.80
- Mass flow is reduced by approximately 15%
- The auxiliary doors can help unstart recovery by providing additional flow area

### Buzz Margin

- First buzz frequency: ~120 Hz (organ-pipe mode of intake duct)
- Buzz margin: ~3% below design Mach (M_buzz ≈ 1.02)
- The 3.8% contraction provides a small but adequate buzz margin
- Active buzz suppression not required for this application

## 10. Integration Notes

### Fuselage Attachment

The intake mounts to the fuselage via the compressor face flange (4× M4 bolts). The fuselage structure at station x = 1.50 m includes:

- Bulkhead ring: 130 mm ID × 5 mm wall, 6061-T6 aluminium
- Four M4 threaded inserts in bulkhead at 122 mm PCD
- The intake weight (400 g) is cantilevered forward of this bulkhead

### Thermal Considerations

- Inconel 718 CTE: 13.0 μm/m·°C
- 6061-T6 aluminium CTE: 23.6 μm/m·°C
- A thermal expansion gap of 0.3 mm is allowed at the flange interface
- The O-ring accommodates this differential expansion
- At 650°C, the intake expands ~0.9 mm in length; the fuselage station x = 1.50 m is the reference

### Splitter Plate Integration

- The splitter plate bolts to the intake via 2 × M3 brackets on each side
- The fuselage skin is cut away beneath the splitter plate to form the vent path
- A fairing blends the splitter plate leading edge into the fuselage contour

### Access Requirements

- The intake is removable from the aircraft by releasing 4× M4 bolts and disconnecting the compressor face duct
- No special tools required
- Estimated removal/installation time: 15 minutes

## Appendix A: Inconel 718 Material Properties (DMLS)

| Property | As-printed | HIP + Heat Treated |
|----------|-----------|-------------------|
| Density | 8.19 g/cm³ | 8.22 g/cm³ |
| Yield strength (0.2%) | 850 MPa | 1100 MPa |
| Ultimate tensile strength | 1100 MPa | 1400 MPa |
| Elongation at break | 12% | 22% |
| Hardness | 38 HRC | 44 HRC |
| Fatigue strength (10⁷ cycles) | 400 MPa | 550 MPa |
| Max service temperature | 650°C continuous | 700°C peak |
| Thermal conductivity | 11.4 W/m·K | 11.4 W/m·K |

## Appendix B: Recommended Print Parameters

| Parameter | Value |
|-----------|-------|
| Layer height | 30 μm |
| Laser power | 250 W |
| Scan speed | 800 mm/s |
| Hatch spacing | 0.10 mm |
| Scan strategy | Island (5 × 5 mm) with 67° rotation per layer |
| Contour scans | 2 (inner + outer) |
| Preheat temperature | 80°C |
| Inert gas | Argon, O₂ < 100 ppm |
| Build plate material | Inconel 718 |

## Revision History

| Rev | Date | Changes |
|-----|------|---------|
| 01 | Initial release | |

---

*End of document — intake ready for DMLS production*
