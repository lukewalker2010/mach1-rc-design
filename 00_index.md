# Mach 1 RC Aircraft — Design Package Index

**Project:** single P550-PRO + afterburner, level Mach 1 mission.
**Reviewed:** 2026-09-16.
**Status:** engineering development — **not released for aircraft manufacture,
hot testing or flight**. [Read the readiness review first](25_readiness_review.md).

The review found invalid mould/rib geometry, an out-of-band fuel-empty CG,
unclosed structure/recovery and incompatible measurement/DAQ assumptions.
Earlier “build-ready” and “closure verified” statements are superseded by 25.
Passing software checks do not constitute aircraft qualification.

## Start here

| Document | Purpose |
|---|---|
| [18 — Program requirements](18_program_requirements.md) | Mission/geometry/mass contracts; September errata identify unverified claims |
| [25 — Readiness review](25_readiness_review.md) | Reproducible findings, owners, closure deliverables and order of work |
| [26 — Measurement validation](26_measurement_validation.md) | Implemented Mach/TAS and log screening, calibration and DAQ corrections |
| [27 — Manufacturing release](27_manufacturing_release.md) | Part release, traveller, inspection and test evidence process |
| [28 — Closure tracker](28_closure_tracker.md) | All R01–R16 workstreams, reviewed results, model provenance and remaining decisions |
| [INTERFACES](INTERFACES.md) | Controlled mating dimensions and cross-team change procedure |
| [AGENTS](AGENTS.md) | Repository instructions and subsystem status |

## Current analyses and development packages

| Document | Current use / limitation |
|---|---|
| [19 — Aero evaluation v2](19_aero_evaluation_v2.md) | Preliminary empirical drag estimate; no demonstrated aero/flight closure |
| [20 — Structural analysis v2](20_structural_analysis_v2.md) | Corrected half-wing equilibrium, spar fit failure, open strength/flutter work |
| [21 — Afterburner bench program](21_afterburner_bench_program.md) | Development test matrix; static-to-flight conversion unvalidated |
| [22 — BOM v2](22_bom_v2.md) | Historical $9,662 aircraft allowance; flagged parts are not purchase-qualified |
| [23 — Systems/M&V](23_systems_mv.md) | Layout concept with measurement/power errata and open CG/failsafe work |
| [24 — Thrust stand](24_thrust_stand.md) | Concept rig; revised statics in 35, DAQ hardware in 33 and implemented offline software in 34 |
| [29 — Geometry resolution](29_geometry_resolution.md) | Exact centreline planform, continuous body candidate, finite-width containment and remaining packaging failures |
| [30 — Structure/recovery](30_structure_recovery.md) | Distributed loads, cap fit, braking/chute energy and aeroelastic evidence |
| [31 — Mass/CG resolution](31_mass_cg_resolution.md) | Fuel/uncertainty sweeps, coupled ballast feasibility proof and mission fuel accounting |
| [32 — Propulsion/thermal](32_propulsion_thermal.md) | Choked-flow/pressure-thrust/energy bookkeeping and conditional thermal equilibria |
| [33 — Instrumentation/power](33_instrumentation_power.md) | Manufacturer-source checks, candidate ranges, P550 supply conflict, ADC pin/scale/timing |
| [34 — Bench software](34_bench_software.md) | Implemented event ingestion, force-domain calibration, static screening and concurrent-log checking |
| [35 — Rig/manufacturing](35_manufacturing_rig.md) | Bolt/beam/anchor equilibrium and evidence-record integrity validation |

## Geometry and manufacture

| Package | Status |
|---|---|
| [Wing](wing_manufacturing/00_index.md) | R1–R5 spar-hole containment fails; CSV root/area convention conflicts; legacy layup and mould data |
| [Fuselage](fuselage_manufacturing/00_index.md) | Mould pinches to zero radius at station 850 mm; matched assembly/tooling unresolved |
| [Stabilator](stabilator_manufacturing/01_manufacturing.md) | Tip spar-hole breakout; hinge/bearing packaging unresolved |
| AB `*_step.py`, `*.step`, `*.scad` | Existing concept CAD; revised cooling, complete installed assembly and coordinate transforms require closure |
| [Records](records/) | Blank part-release, build-traveller and test-result templates; no qualification results recorded |
| [Proposals](proposals/) | Analytic design alternatives and source ledgers; no released replacement CAD/toolpaths |

## Run the engineering tools

Python standard library only, Python 3.12+ (CAD regeneration has separate pinned
requirements in AGENTS §5):

```sh
python3 -m unittest discover -s tests -v
python3 tools/design_checks.py
python3 tools/structural_analysis.py
python3 tools/aero_evaluation.py
python3 tools/bom_v2_check.py
python3 tools/geometry_candidates.py
python3 tools/loads_recovery.py
python3 tools/mass_mission.py
python3 tools/propulsion_matching.py
python3 tools/hardware_budget.py
python3 tools/rig_loads.py
```

`python3 tools/design_checks.py --strict` currently exits **1** because design
failures remain. `--json` produces a machine-readable screening report. CI runs
regressions and archives that report. For calibrated flight-data screening see
26; bench pipeline CLI/schema are in 34. `python3 tools/release_records_check.py
--json` exits **1** for the current header-only records. No acquired flight or
hot-run evidence is included in this review.

## Legacy concept documents (01–17)

Retained for design history. Use only where consistent with 18 and the subsequent
review; these are **not standalone fabrication or flight instructions**.

| # | Document | Subject |
|---|---|---|
| 01 | [Airframe spec](01_airframe_spec.md) | Original geometry/mass/performance |
| 02 | [C-D nozzle](02_cd_nozzle.md) | Nozzle concept and fabrication notes |
| 03 | [Intake](03_intake.md) | Intake/diverter concept |
| 04 | [Wing structure](04_wing_structure.md) | Original spar/rib/skin design |
| 05 | [Fuselage](05_fuselage.md) | Original mould/bulkhead layout |
| 06 | [Stabilator](06_stabilator.md) | Taileron/hinge concept |
| 07 | [Systems layout](07_systems_layout.md) | Original fuel/avionics/wiring |
| 08 | [Launch/recovery](08_launch_recovery.md) | Dolly/skid/drogue concepts |
| 09 | [BOM](09_bom.md), [supplier links](09_bom_with_links.md) | Historical costs/sources |
| 10 | [Structural analysis](10_structural_analysis.md) | Superseded geometry analysis |
| 11 | [Inlet analysis](11_inlet_analysis.md) | Preliminary inlet/FADEC assumptions |
| 12 | [Aero evaluation](12_aero_evaluation.md) | Superseded geometry drag/stability |
| 13 | [Propulsion analysis](13_propulsion_analysis.md) | Unvalidated engine performance models |
| 14 | [AB mechanical](14_afterburner_mechanical.md) | Hot-section concept CAD |
| 15 | [AB fuel/ignition](15_afterburner_fuel_ignition.md) | Pump/injector/ignition concepts |
| 16 | [AB electronics](16_afterburner_electronics.md) | Controller design/code fragments; no qualified firmware build |
| 17 | [AB thermal integration](17_afterburner_thermal_integration.md) | Preliminary heat/cooling/integration model |

Manufacturing time, total project cost and flight performance require a new
estimate after the open design decisions and actual supplier/process selection.
