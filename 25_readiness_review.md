# Manufacturing, Test & Flight Readiness Review

**Date:** 2026-09-16 · **Baseline reviewed:** `ec00a3b` plus this review's corrections.
**Disposition:** engineering development; aircraft tooling, hot-run rig and flight release remain open.

The repository contains useful concept work, but the earlier “closure verified”,
“build-ready” and “design complete” statements are not supported by the actual
geometry, instrumentation or test evidence. This review supersedes those status
claims. Mission requirements in [18](18_program_requirements.md) and mating
dimensions in [INTERFACES](INTERFACES.md) remain the coordination contract.
No mating dimension is changed here. Decisions affecting those interfaces require
the owning engineers' review under `INTERFACES.md` §4.

## 1. Reproduce the review

Python standard library only (Python 3.12+); from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 tools/design_checks.py
python3 tools/design_checks.py --strict
python3 tools/structural_analysis.py
```

`--strict` currently exits **1**, deliberately: physical design checks fail.
Exit **2** means missing/malformed input, not a completed review. Ordinary audit
mode exits **0** after generating the report, regardless of physical findings.
CI tests the analysis and uploads the screening report; a green CI badge does
**not** mean an aircraft passed manufacturing or flight qualification.

The audit reads the actual §3.4 component rows, rib CSV, DXF polylines and mould
station table. Its geometry checks are limited to those artifacts; it does not
validate STEP solids, tooling release, tolerances, strength or flutter. Existing
STEP files were not regenerated or import-validated in this review.

## 2. Findings and closure deliverables

Priority follows 18 §7: P0 before relevant build, P1 before flight. All rows below
are **OPEN** until the named deliverable is reviewed and linked to measured or
analytical evidence. A proposed test is not evidence that the test passed.

| ID | Priority / owner | Finding and source | Required closure deliverable |
|---|---|---|---|
| R01 | P0 E1/E5 | Mould §1.5 gives **R=0 at x=850 mm**. The forebody pinches completely shut; the adjoining cosine does not repair connectivity or tangent continuity. `FUSE-CONTINUITY`. | Reviewed continuous outer/inner mould lines, intake/engine/structure clearance sections, matched bulkheads, draft/parting and complete assembly STEP. Resolve nose-law ambiguity in 18 §3.1 before cutting tooling. |
| R02 | P0 E1/E5 | `HOLE-wing_rib_R1`…`R5` fail web containment; `HOLE-STA_TIP` fails even outer-contour containment. A round hole is also not a detailed box-spar interface. | Tapered spar/cap/web and rib-pocket design, bonded-joint details, minimum ligaments, tolerance stack; regenerate and validate all net parts. Do not merely shrink holes to make an audit pass. |
| R03 | P0 E1/E5 | CSV/generator put the 210 mm root at the **fuselage side**, whereas the span/area equation is for a centreline root. Including a constant hidden root gives **0.151305 m²**, not 0.14 m² (`WING-AREA`). Legacy rib Markdown uses a different airfoil again. | Decide centreline versus exposed-area convention, root LE station and sweep transform; derive all CAD/CSV/mould tables and aerodynamic references from that one definition. |
| R04 | P0 E1 | 20 assigned full-aircraft lift to a half-wing and used an unrelated shear formula. Correct centreline 6g loads are **81.48 N·m / 400.25 N**, not 163 N·m / 457 N. Proposed 7 mm cap-centroid spacing fails the section envelope. | Fit-first spar design, full load cases including tail trim, gusts, torsion, local buckling and joints, laminate allowables with manufacturing/environmental knockdowns; proof-test plan. Corrected calculations in `tools/structural_analysis.py`; see 20. |
| R05 | P0 E1/E3 | Full CG **0.974809 m**; empty **1.045776 m**, outside 0.955–0.995 m. Half-fuel CG is also outside. A guessed tail neutral point cannot waive the CG contract. | Reviewed mass/station layout and fuel-state sweep with uncertainties; measured weigh-off. Validate Mach-dependent neutral point, trim and control authority separately. Resolve AB 0.83 vs 0.97 kg accounting without double-counting pump/fuel-system mass. |
| R06 | P0 E1/E4 | At full mass, S=0.14 m², 30 m/s and sea-level density, required **CL=1.729** before tail download (`LANDING-LIFT`). Screening against assumed CLmax=0.8 fails; neither value is a measured lift polar. | Validated low-speed polar, approach/flare/rotation trim, and recovery concept meeting the speed requirement; energy and load-rated dolly brakes, wheels, skid and chute system. Resolve 38 m/s approach versus 70 m/s launch. |
| R07 | P0 E2/E3 | Static thrust × mass-flow ratio is not a validated flight thrust map. Nozzle velocity depends on pressure ratio, efficiency, mass flow and matching, not T7 alone. Fuel weighing cannot measure core airflow. | Engine/inlet/nozzle matching and calibrated air mass flow, pressure thrust and installation corrections; uncertainty-bounded thrust over Mach/altitude. Bench 700 N is a development target, not proof of ≥450 N in flight. |
| R08 | P0 E2/E5 | 21 calls for revised film cooling but CAD/BOM have older counts; hot-section wall stress and shell/composite temperatures remain predictions. `k·ΔT/t` with assumed endpoint temperatures does not solve the cold-face temperature. | Released liner/shell/nozzle assembly, cooling pressure/flow balance, material/process records, thermal transient and soak-back data. Check nozzle travel/clearances hot and cold and resolve iris abort direction. |
| R09 | P0 E3 | 23's 3447 Pa pitot range versus **62,237 Pa at M1**, **78,960 Pa at M1.1** / 69.7 kPa ambient. The subsonic pressure inversion is used beyond M1. | Range/accuracy/rate-qualified pressure chain and probe calibration; shock-aware processing now provided by `tools/airdata.py`. See 26. |
| R10 | P0 E3 | “D24V50F12 boost” is not substantiated by a manufacturer part page. Verified Pololu D24 devices are **buck** regulators, requiring input above output. 2S cannot supply regulated 12 V through a buck. Existing power budget mixes currents on different voltages. | Actual pump motor/driver datasheet, true boost or buck-boost choice, low-pack-voltage/startup/stall current and thermal qualification, pin-to-pin schematic and power isolation test. S20 remains a budget allowance. |
| R11 | P0 E2/E3 | 24 treats ADS1256 as eight differential channels; it has four pairs/eight single-ended inputs. Two raw bridges plus six single-ended signals exceed its pins without additional circuitry. 60 Hz rejection on MAX31856 is not 60 conversions/s. | Reviewed channel/pin allocation, gains/input limits, conversion-ready timing, settling and anti-alias filters; measured aggregate throughput with source timestamps. See 26. |
| R12 | P0 E2/E3 | 24 names `daq_bench.py`, `post_bench.py`, `cal_bench.py` as committed; they are absent. 16 contains design/code fragments rather than a qualified, reproducible controller build. | Implement and bench-verify actual acquisition and control hardware/software; fault injection for MCU hang/reset, power/RC loss, sensor faults, and independent abort latency. A Pico GPIO described as “independent” is not hardware independence. |
| R13 | P0 E2/E1 | 24 stand analysis uses solid-square inertia for slotted extrusion, simplified bolt load division and estimated cell stiffness; no combined-load/anchor/overturning closure. Running-engine tare removes real idle thrust. | Supplier section properties, load paths and bracket/anchor drawings, fastener checks and rig proof plan; engine-off tare and traceable installed calibration. |
| R14 | P1 E1/E3 | 19 calls an empirical drag estimate “closed”; no validated transonic model, uncertainty bounds or aeroelastic analysis. 12 kft thrust reused the 10 kft assumption. | CFD/tunnel/identified aerodynamic data with uncertainty; matched thrust-drag map, ground vibration and flutter prediction correlated to hardware before envelope expansion. “No observed oscillation” alone is not flutter clearance. |
| R15 | P1 E3 | Independent loggers should not have identical hashes. TAT+static pressure alone cannot recover Mach. Claimed no-altitude-loss rule conflicts with ad hoc tolerances. | Separate sealed raw-log hashes, clock/latency and uncertainty calibration, agreed altitude-loss evaluation and reciprocal-run protocol. New offline duration screen does not certify the mission. |
| R16 | P0 E1–E5 | Cure process, material system, datum/tolerances, inspection acceptance, hot-section build and suppliers are not a released manufacturing set. Cost omits unresolved replacements and qualification work. | Part/drawing/BOM release matrix, approved process instructions, completed build travellers and calibration/test records per 27. Update cost only against traceable quotes. |

## 3. What was upgraded in this revision

- Corrected half-wing equilibrium and CG reporting, removed unsupported strength,
  thermal and aerodynamic closure claims.
- Added artifact-aware design screening, shock-aware Mach/TAS analysis, and an
  offline uncertainty-aware sustained-Mach log screen with raw-file hashing.
- Added regression tests covering independent textbook shock/load cases, actual
  invalid CAD contours, fuel mass conservation, sensor rails, missing samples,
  sequence/clock faults and duration boundaries, plus CI.
- Corrected current-budget voltage conversion and flagged incompatible procurement
  choices without substituting unqualified parts.
- Added controlled manufacturing/test record templates and a staged closure path.

## 4. Order of work to reach the user's build/test/fly goal

1. **Geometry and mass design review:** resolve R01–R06 and the relevant P0
   interfaces together. Tooling is expensive to change after this point.
2. **Bench subsystem release:** close R07–R13; release rig drawings, calibration,
   acquisition and abort hardware before hot testing. Static development results
   must retain their actual inlet/exhaust conditions.
3. **Manufacturing release:** instantiate the 27 templates for each part; qualify
   the chosen composite and hot-section processes, then release serialised parts.
4. **Ground qualification:** weigh fuel states, structural proof, rig correlation,
   vibration/modal data, control travel/load checks, range/EMI and recovery tests.
5. **Flight envelope release:** establish quantitative speed/q/load/CG/thermal
   limits from the above evidence; define each test card and abort condition.
   Close the Mach-dependent thrust/drag and flutter gaps before transonic flight.
6. **Mission verification:** calibrated dual logs, independent uncertainty analysis,
   reviewed no-altitude-loss evidence, intact landing and reciprocal repeat.

No physical build, calibration, hot run, proof test or flight occurred during
this repository review. The new tools make discrepancies reproducible; the
remaining work requires actual engineering decisions and hardware evidence.
