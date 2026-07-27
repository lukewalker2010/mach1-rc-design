# Mach 1 RC Aircraft — Design Package Index

**Project:** Path 2 — P550-PRO + C-D Nozzle + Cd 0.166
**Status:** Design complete + Afterburner Package
**Date:** July 2026
**Documents:** 14 files + 6 OpenSCAD drawings, 200,000+ bytes

---

## Design Documents

| # | File | Contents | Pages ~ |
|---|------|----------|---------|
| 00 | `00_index.md` | This index | 1 |
| 01 | `01_airframe_spec.md` | Complete airframe spec, dimensions, masses, performance | 3 |
| 02 | **`02_cd_nozzle.md`** | C-D nozzle fabrication drawing, lathe steps, contour table, test procedure | 8 |
| 03 | **`03_intake.md`** | Supersonic pitot intake, diverter, auxiliary doors, DMLS print spec | 14 |
| 04 | **`04_wing_structure.md`** | Wing planform, spar, 12 ribs, skin schedule, carry-through joint | 8 |
| 05 | **`05_fuselage.md`** | Fuselage mold lines, area-ruled waist table, 8 bulkheads, engine mount | 14 |
| 06 | **`06_stabilator.md`** | All-moving stabilator, hinge system, servo integration, tailerons | 18 |
| 07 | **`07_systems_layout.md`** | Engine mount, fuel system, avionics layout, CG calc, wiring | 8 |
| 08 | **`08_launch_recovery.md`** | Launch dolly, belly skid, drogue chute design, drawings | 8 |
| 09 | **`09_bom.md`** | Bill of materials (~$7,000), 150-hr build sequence, flight checklist | 8 |

## Engineering Analyses

| # | File | Contents | Pages ~ |
|---|------|----------|---------|
| 10 | **`10_structural_analysis.md`** | Full structural feasibility: spar design, flutter risk, thermal loads, weight budget, load factors | 10 |
| 11 | **`11_inlet_analysis.md`** | Supersonic inlet analysis: spillage drag, boundary layer diverter, auxiliary doors, FADEC integration | 10 |
| 12 | **`12_aero_evaluation.md`** | Aerodynamic evaluation: drag breakdown, trim, stability margins, transonic wave drag | 6 |
| 13 | **`13_propulsion_analysis.md`** | Propulsion analysis: thrust at altitude, specific impulse, C-D nozzle gains, fuel consumption | 5 |

## Afterburner Package (Path 2b)

| # | File | Contents | Pages ~ |
|---|------|----------|---------|
| 14 | **`14_afterburner_mechanical.md`** | Transition duct, spray ring, flame holder, liner, iris nozzle — 6 OpenSCAD parts + 5 CadQuery → STEP scripts | 10 |
| 15 | **`15_afterburner_fuel_ignition.md`** | Speck ZY-4S-12V pump, Bosch EV14 injector, NGK CM-6 + RCEXL CDI, plumbing | 6 |
| 16 | **`16_afterburner_electronics.md`** | RP2040 (Pi Pico), MAX6675 EGT, Hamamatsu G5842 UV sensor, 7-state machine, MAVLink | 8 |
| 17 | **`17_afterburner_thermal_integration.md`** | 1800K flame, 453 kW/m² flux, 65 film cooling holes, YSZ TBC, 830g, 4-phase test | 8 |

---

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Engine | JetCat P550-PRO (stock, 4.9 kg) |
| Nozzle | C-D, 35mm throat → 47mm exit, 10° half-angle, +11% thrust |
| Intake | Pitot, 105mm lip, 103mm throat, 15mm BL diverter |
| MTOW | 12.2 kg |
| Length | 2.2 m, fineness 11:1 |
| Wing | Delta, 0.9m span, 0.095 m², biconvex 3.5% |
| Cd at M1 | 0.166 |
| Thrust at M1 | 300 N |
| T-D margin | +7.8 N |
| Launch | Dolly, 56m to 70 m/s |
| Landing | Belly skid + 0.6m drogue chute |
| Build time | ~150 hours |
| Est. cost | ~$7,000 |

---

## Build Phases

| Phase | Hours | Description |
|-------|-------|-------------|
| 1. Tooling | 40 | CNC plugs, molds |
| 2. Structure | 60 | Layup, bond, assemble |
| 3. Systems | 30 | Plumbing, wiring, avionics |
| 4. Test | 20 | Ground run, taxi, envelope expansion |
| **Total** | **150** | |

---

## Key Suppliers

| Item | Source |
|------|--------|
| JetCat P550-PRO | jetcat.de / jetcatusa.com |
| Carbon prepreg | ACP Composites (acpsales.com) |
| Carbon rod | DragonPlate (dragonplate.com) |
| Inconel DMLS | Xometry (xometry.com) |
| Servos (KST X20-12T) | KST / hobby dealers |
| Flight controller | Holybro (Cube Orange+) |
| Foam core (Rohacell) | Aircraft Spruce / CST |
