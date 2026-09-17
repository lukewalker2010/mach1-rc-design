# Open-Item Closure Workstreams

**Started:** 2026-09-16 · **Input revision:** `9db2fd0`.
**Requested scope:** address every R01–R16 item with delegated implementation and
principal-agent consistency review. Findings and full closure criteria remain
in [25](25_readiness_review.md).

## Status semantics

- **ASSIGNED:** a worker owns implementation; no result accepted yet.
- **IMPLEMENTED / REVIEWED:** a specific calculation, software or document gap
  is addressed and its checks reviewed. This does not release physical hardware.
- **PROPOSED:** a candidate design requires the stated interface/design decision.
- **AWAITING EVIDENCE:** a specific physical measurement, supplier qualification
  or engineering approval remains necessary.
- **CLOSED:** the entire original finding's deliverables and evidence are complete.

An item cannot be closed by inventing material properties, changing acceptance
limits, marking simulated samples as measurements or assuming an approval.
Controlled interfaces stay fixed until the existing owner-review process is met.

## Assignment and file ownership

The initial implementation workers use provider-listed zero-price models. MiMo
V2.5 Free and Big Pickle both passed availability probes with reported cost zero.
Nemotron 3 Ultra Free timed out at the availability probe and was not assigned
production work. Primary review is performed in the coordinating session.

| Stream | Findings | Initial model | Exclusive deliverables | State |
|---|---|---|---|---|
| A — Geometry | R01/R02/R03 | `opencode/mimo-v2.5-free` | [29](29_geometry_resolution.md), `tools/geometry_candidates.py`, candidate geometry and focused tests | IMPLEMENTED / REVIEWED; candidate fit still fails |
| B — Loads/recovery | R04/R06/R14 | `opencode/big-pickle` | [30](30_structure_recovery.md), `tools/loads_recovery.py`, focused tests | IMPLEMENTED / REVIEWED; physical evidence open |
| C — Mass/mission | R05 | `opencode/mimo-v2.5-free` | [31](31_mass_cg_resolution.md), `tools/mass_mission.py`, candidate layouts and focused tests | IMPLEMENTED / REVIEWED; coupled layout decision open |
| D — Propulsion/thermal | R07/R08 | `opencode/big-pickle` | [32](32_propulsion_thermal.md), `tools/propulsion_matching.py`, focused tests | IMPLEMENTED / REVIEWED; matching/hardware open |
| E — Hardware | R09/R10/R11 | `opencode/big-pickle` | [33](33_instrumentation_power.md), `tools/hardware_budget.py`, sourced candidate parts and tests | IMPLEMENTED / REVIEWED; qualification open |
| F — Bench/data software | R12/R15 | `opencode/mimo-v2.5-free` | [34](34_bench_software.md), offline bench ingestion/calibration/post-processing and paired-log tools/tests | IMPLEMENTED / REVIEWED; hardware/protocol open |
| G — Rig/manufacture | R13/R16 | `opencode/mimo-v2.5-free` | [35](35_manufacturing_rig.md), rig load and release-record checkers/tests | IMPLEMENTED / REVIEWED; real evidence incomplete |

Workers may not edit each other's paths, master requirements, controlled
interfaces or global status/index files. Candidate geometry lives under
`proposals/` and is not a released toolpath. No worker may commit, push or spawn
additional workers. The coordinator owns integration and final disposition.

## Cross-workstream consistency review

1. **Geometry → loads:** total span versus exposed span, centreline root versus
   body-side root, exact area/MAC and sweep/reference transforms must agree.
2. **Mass → recovery/loads:** use the actual 18 §3.4 rows; distinguish full/empty
   states, added tail loads, fuel consumption and duplicated subsystem mass.
3. **Propulsion → hardware:** distinguish air/core/AB fuel flow and pressure
   stations; engine/nozzle/pump specs must be traceable to actual parts.
4. **Hardware → DAQ:** physical channels, SI units, gains, input limits, conversion
   timestamps, valid flags and achievable rates must agree with software schemas.
5. **Software → evidence:** simulated sources, missing calibration, stale samples,
   incomplete records and unknown approval cannot become a physical PASS.
6. **Manufacture → configuration:** every candidate/released artifact must identify
   revision, source, coordinate convention, process and verification scope.

## Integration results and precise remaining work

Seven free workers produced the first implementation. Three reached the bounded
runtime with partial work; targeted reviewers completed it. Four technical-review
tasks corrected defects, followed by principal cross-workstream review. Worker
event streams reported total inference cost **0**; that excludes primary/reviewer
costs, which were not exposed by the task result. Actual model/session provenance
and cost limitations are in [reviews/agent_provenance.json](reviews/agent_provenance.json).

| Finding | Completed subitem | What prevents full closure |
|---|---|---|
| R01 | Tested continuous body-law candidate and local envelope checks (29) | Candidate still fails intake/packaging; approved body/installed layout and validated STEP needed |
| R02 | Correct finite-width cap and hole containment, explicit stabilator failure (29/30) | Fitting load-bearing spar/hinge/joint design, tolerances and regenerated net parts |
| R03 | Exact centreline root/tip/MAC/exposed-area convention derived and cross-tested (29/30) | Root LE/global mating definition and approved propagation into baseline CAD/moulds |
| R04 | Distributed shear/moment, tail/inertial relief, cap fit and force-couple units corrected (30) | Governing 150 N·m versus g-load contract review, fitting spar, laminate/buckling/joint allowables and proof |
| R05 | Fuel-state/independent uncertainty sweeps, coupled ballast proof and mission accounting (31) | Actual feasible tank/mass/CG layout, packaging, weigh-off and independent neutral-point/trim evidence |
| R06 | Lift requirement, wheel RPM, brake/skid energy and chute load quantified (30) | Measured polar/control authority and qualified recovery/abort hardware and deployment gate |
| R07 | Choked/unchoked capacity, pressure thrust and air/fuel bookkeeping implemented (32) | Engine/inlet/nozzle flow-pressure map and installed uncertainty-bounded measurements |
| R08 | Conditional heat-addition and balanced wall/blanket equilibria implemented (32) | Matched hot-section CAD, material/cooling/transient/soak-back and fail-direction evidence |
| R09 | Pressure-envelope/range screen and explicit source confidence for candidates (33) | Exact options/static sensor source, calibration, tubing/static-port/overpressure qualification |
| R10 | Correct voltage/current screens; rejected direct-2S P550 supply; boost isolation behavior identified (33) | Actual engine current/startup/variant, real AB pump/driver and qualified power architecture |
| R11 | Correct ADC scale/common-mode/pin split/settling and TC conversion-time calculations (33) | Board schematic, weighted DRDY schedule and measured noise/bandwidth/EMI/source timing |
| R12 | Actual offline event archive, force-domain calibration and static screening CLI (34) | Real acquisition/actuator drivers, independent hardware cutoff and timed fault injection |
| R13 | Bolt six-component equilibrium, sourced extrusion inertia, support/anchor statics (35) | Released fixture geometry, joint/anchor capacities, installed calibration and physical proof |
| R14 | Consistent geometry/modal dimensional checks and defined evidence requirements (30) | Correlated aeroelastic/CFD/tunnel/GVT data and reviewed envelope; no flutter margin invented |
| R15 | Metadata-inclusive hashes, same-run/config pair semantics and calibrated-clock consistency tool (34) | Physical independence/custody, calibrated clocks/sensors, altitude-loss and reciprocal-run protocol |
| R16 | Real-schema evidence-path/hash/Git-provenance/record-join validation (35) | Qualified materials/processes, complete authentic travellers/inspection/test evidence and owner acceptance |

**No entire R01–R16 finding is marked CLOSED.** The completed subitems are usable
software/analysis deliverables, not physical qualification or automatic approval.

### Important review corrections

- Removed wrong sweep/taper and half-thickness math, discontinuous candidate
  coefficients, centroid/force-couple errors and arbitrary flutter clearance.
- Replaced correlated all-heavy/all-light CG bounds with independent extrema;
  disproved the initial claim that *all* ballast solutions below 25 kg fail.
- Corrected nozzle mass/enthalpy consistency, ADC **±2 VREF/PGA** scaling,
  common-mode constraints and settled mux throughput; retained source conflicts.
- Repaired software that could previously accept simulated/zero-thrust data,
  mix volts/newtons in calibration, drop invalid records, or reject correctly
  matching test/config IDs. CLI regressions now exercise those failures.
- Added a cross-workstream discovery: the primary P550-PRO datasheet specifies
  **10–35 V**, so the former direct-2S engine supply is invalid (33 §2).

### Decisions to resolve before baseline redesign

1. **Coupled tank/mass/layout:** at 13.60 kg the fixed I-06 centroid range cannot
   meet both CG endpoints merely by redistributing dry masses (31 proof).
   At x_f=0.45 m the necessary mass bound is 22.0725 kg; at the optimistic
   x_f=0.60 m it is 15.9975 kg. The 25 kg ballast counterexample is not a
   packaging or performance solution. Select a physically feasible layout and
   review affected tank/engine/wing/avionics interfaces together.
2. **Body/intake/spar integration:** continuity is fixed in the candidate law,
   but intake and finite-width structure still do not fit. Approve an integrated
   shape/load path rather than modifying individual holes to pass a check.
3. **Propulsion/power source facts:** obtain exact engine variant/installation
   limits and actual AB pump data before deciding nozzle matching, engine supply
   or motor driver. Candidate calculations are not supplier approval.

### Verification

Run `python3 -m unittest discover -s tests -v`, plus the analysis CLIs listed in
00. Cross-workstream regressions check geometry/loads/mass consistency and the
manufacturer engine voltage range. `design_checks.py --strict` still returns 1
for original physical design failures; `release_records_check.py --json` returns
1 for empty records. CI distinguishes those expected incomplete screens from
malformed-input/tool failures. Integrated test count/result is recorded after
the final verification run below.
