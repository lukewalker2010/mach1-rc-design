# Manufacturing Release & Test Records

**Date:** 2026-09-16 · **Status:** process/templates available; no parts released.
Use with [25](25_readiness_review.md). This defines the missing build records
needed to turn a design package into traceable hardware.

## 1. Release package for each part or assembly

Before supplying a file to a shop, the part's record must include:

| Field | Required content |
|---|---|
| Identity | Part number, revision, serial/lot, drawing title, parent assembly |
| Source | Repository commit, generator/environment version, artifact SHA-256 |
| Geometry | Drawing and authoritative STEP/DXF, units, aircraft/local datums and explicit transform, handedness |
| Fit | Interface IDs, nominal dimensions, tolerances/clearances, hole/insert/fastener details, mating part revisions |
| Material | Exact supplier/material/resin or alloy designation, certificate and lot; substitution disposition |
| Process | Approved machining/printing/heat treatment/coating or ply/bond/cure instruction revision |
| Inspection | Characteristic, datum, instrument, tolerance and acceptance authority; no unassigned critical tolerance |
| Evidence | Dimensional report, mass/station measurement, NDI/coupon/proof evidence as applicable |
| Release | Owner/affected interface review, disposition and dated signature |

Populate `records/part_release.csv` with one row per controlled part. Blank
templates are not a release. Names/part numbers below are local record IDs and
do not assign or change mating dimensions.

## 2. CAD and tooling checks

- Verify 25 R01–R04 before regenerating airframe tooling. A closed DXF entity
  does not guarantee a usable net part; check self-intersections, nested loops,
  minimum ligaments, hole/skin containment and consistent centreline geometry.
- For changed STEP files use the repository's pinned Python 3.12/CadQuery 2.8.0
  environment. Import each solid, check validity, dimensions, handedness and
  volume, and check transformed assembly interferences. Record the environment
  and results. Keep intended contact distinct from interference.
- Publish global aircraft coordinates (+X aft, +Z up) and every local-to-global
  transform. The existing AB generators use local Z as the axial direction;
  that is not a global aircraft placement without a documented rotation/offset.
- Separate net-part geometry from tool allowance, trim allowance, cutter kerf,
  coating and cure shrinkage. Record allowances on the drawing/process sheet.
- Prove mould extraction/access, parting/draft, cure access and fastener access.
  Review full installed engine envelope, cooling ducting and exhaust path, not
  only shell OD at one fuselage station.

## 3. Composite / bonded-part traveller

Copy `records/build_traveller.csv` for each serialised part. Record operator,
timestamp, instruction revision, measured result and inspector/disposition for:

1. Incoming resin/prepreg/core/fibre certificates, shelf life, storage and out-time.
2. Tool identity/revision, dimensional and surface inspection, release preparation.
3. Ply kit: material/lot, ply number, shape, orientation datum, drops/splices and
   actual sequence. The existing conflicting cure/layup recipes are not approved.
4. Inserts/core preparation, surface treatment, isolation of dissimilar metals,
   bondline control and adhesive lot/mix/open time.
5. Bag leak test and calibrated pressure/temperature sensor locations.
6. Actual cure time/part-temperature/pressure traces against the **selected
   material supplier's qualified process**. Furnace/autoclave setpoint alone is
   not part temperature. Record deviations rather than replacing trace data.
7. Demould/trim/drill, visual/dimensional inspection, void/delamination inspection
   method and acceptance standard, witness-coupon results as required.
8. Final mass, CG datum measurement, hardware torque/locking records and serial
   linkage to the parent assembly.

For hot-section parts replace the ply/cure operations with the approved alloy,
build orientation, powder/stock traceability, heat treatment, finish, coating,
wall/hole inspection and thermal-cycle qualification instructions. Those
parameters must come from the released hot-section design, not a generic recipe.

## 4. Test card and evidence

Use `records/test_card.md` for every coupon, structural, bench, ground or flight
test. Link raw data and calibration certificates from `records/test_results.csv`.
Record configuration/serials, preconditions, the actual test procedure, acceptance
limits with source, instrumentation and uncertainties, observed events, results,
disposition, post-test inspection and next permitted configuration/envelope.

Structural proof loads/fixtures must come from the **completed** load-path and
allowables work. The corrected centreline half-wing calculation is not a loading
instruction for a fuselage-side joint. Do not proof-test a flight article to
ultimate and then treat it as undamaged without an explicit design disposition.

## 5. Release sequence tied to 18 G0–G7

| Release | Evidence required | Current state |
|---|---|---|
| Development tooling / coupon | Approved material/process and representative coupon geometry | OPEN |
| Bench rig / cold test | Rig drawings/load checks, released wiring/channel map, calibration and verified independent abort | OPEN: 25 R07–R13 |
| Hot bench / G0 | Cold-flow/fuel/control preconditions, engine installation limits, cooling and calibrated acquisition; flight-thrust inference separately justified | OPEN |
| Aircraft manufacture | R01–R06 resolved, released matched drawings/CAD/BOM, qualified process and inspections | OPEN |
| Ground / G1–G2 | Conforming hardware, measured fuel-state CG, structural/control/modal/thermal and launch/recovery evidence | OPEN |
| Initial flight / G3 | Reviewed speed/q/load/CG limits, trim/control and flutter basis, range and recovery demonstration | OPEN |
| Transonic / G4–G5 | Correlated aeroelastic and thrust/drag models across the intended Mach/altitude envelope, calibrated M&V | OPEN |
| Reciprocal / G6–G7 | Prior sortie raw logs, post-flight inspection, turnaround and same-configuration record | OPEN |

Attach supporting evidence before recording PASS. Mark a failed or unperformed
test as FAIL or NOT RUN, and retain the raw result. Flight-envelope changes and
interface changes use the existing owner-review process.
