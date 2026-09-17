# Manufacturing records and rig statics — R13/R16 implementation and review

**2026-09-16 · Coordinator baseline: `9db2fd0` · R13 OPEN · R16 OPEN.**
The partial worker implementation has been corrected and regression-reviewed.
Results below are calculations and record-integrity checks, not measured fixture
performance, authenticated approval, manufacturing release or hot-run clearance.

## Reproduce

From the repository root, Python standard library only:

```sh
python3 -m unittest discover -s tests -p 'test_rig_loads.py' -v
python3 -m unittest discover -s tests -p 'test_release_records.py' -v
python3 tools/rig_loads.py
python3 tools/release_records_check.py --json
```

Rig output is JSON; exit 0 means calculation completed. Records exit 0 means
`CONSISTENT_UNVERIFIED`, 1 means `INCOMPLETE`, 2 means `INVALID`. Current records
return **1**, deliberately. No output state certifies a part or rig.

Verification: **15 focused tests passed** (7 rig, 8 records). The integrated
suite result is recorded in 28 rather than duplicated here as workers change
their tests. Test counts are not technical approval of other implementations.
This task's review checked source, dimensional
consistency, free-body equilibrium, failure handling and evidence semantics;
external engineering acceptance remains outstanding.

## R13 — source, free bodies and actual calculated results

Sources and unit conversions are recorded in
[`proposals/rig/sources.md`](proposals/rig/sources.md). The specific vendor page
confirms **80/20 40-4040 Ix = Iy = 13.787 cm⁴ = 1.3787e-7 m⁴**. Its modulus
text is malformed; **E = 68.9 GPa is an explicit parameter**, pending supplier
confirmation. This candidate profile is not an as-built identification.

### Engine adapter connection

The documented series load path is engine → adapter/mount connection → carriage
→ cell → fixed bracket → frame → pad. A downstream load cell does not bypass
the engine bolts. The unchanged controlled pattern is **4×M3 / 45 mm PCD**;
actual I-01 versus I-03 hardware, bolt-axis orientation and bracket drawings
remain to be identified by E1/E2. No interface dimension is changed.

The illustrative planar model uses local `(x,y,z) = (global Y, global Z, global X)`
with origin at the bolt centroid. Global origin remains the aircraft nose,
+X aft, +Z up; this local mapping is not an installed drawing/placement.
Bolt angular orientation 45° is a parameter, not verified hardware geometry.
Applied normal force N, two shear components Vx/Vy and moments Mx/My/Tz are
distributed using equal stiffness and a rigid plate about the centroid:

```
Fi = N/n + a*xi + b*yi
[sum(x²) sum(xy); sum(xy) sum(y²)] [a;b] = [-My;Mx]
Vxi = Vx/n - Tz*yi/J ; Vyi = Vy/n + Tz*xi/J ; J = sum(x²+y²)
sum(Fi)=N; sum(yi*Fi)=Mx; -sum(xi*Fi)=My
sum(Vxi)=Vx; sum(Vyi)=Vy; sum(xi*Vyi-yi*Vxi)=Tz
```

`tools/rig_loads.py` reports all six recovered loads and residuals; tests include
an unsymmetric nonzero-product-of-inertia group and an independent square-group
hand solution. Torsional and direct shear are added as vectors, not magnitudes.

Concept engine/AB mass **5.87 kg**, 5g total vertical load **287.9235 N**;
carriage mass belongs in the frame case, not the engine free body. The 0.97 kg
AB concept mass conflicts with 18's 0.83 kg allocation (R05): these outputs retain
the explicitly identified 24 sensitivity input, not a revised mass baseline.
Full thrust **721 N** is included as a normal load under the assumed bolt-plane
orientation; actual geometry could instead place it in shear.

| CG arm along local z | Weight moment Mx | Signed axial force, upper / lower bolts | Shear per bolt |
|---|---:|---:|---:|
| 0 m sensitivity | 0 N·m | +180.250 / +180.250 N | 71.980875 N |
| 0.35 m sensitivity | 100.773225 N·m | +1763.748461 / −1403.248461 N | 71.980875 N |

There are two bolts in each upper/lower row. Maximum default force-equilibrium
residual is approximately **2.3e-13 N**. Negative axial values are signed
**contact compression terms**, not compressive bolt capacity. The full-contact
linear model does not solve separation, preload loss, plate bending or prying;
clipping negative values to zero is not a re-equilibrated tension-only solution.
Neither arm endpoint bounds unknown as-built geometry or all dynamic cases.

The coupled screening function requires explicit tension/shear areas and
allowables: `(Ft/(At*sigma))² + (Fs/(As*tau))²`. It honors the supplied `tau`.
This is a **parameterized elliptical interaction**, not a sourced, approved
fastener/joint design criterion. No default allowable or interaction PASS is
printed. The coarse-thread area helper is a geometric approximation for supported
M3/M4/M5/M6 diameters; nominal shank area is not automatically the threaded shear
area. Actual grade, thread plane, preload, temperature, fatigue, bearing,
pull-through/strip-out and manufacturer-approved combined-load method are open.

### Frame bending

Two rails, span 0.60 m; 5g on (5.87 + 2.0) kg gives **386.0235 N total**, equally
shared **193.01175 N per rail**. Central point-load Euler–Bernoulli idealizations:

| Support assumption | Deflection | Maximum bending stress | Maximum moment |
|---|---:|---:|---:|
| Simply supported (`PL³/48EI`) | 0.09143390 mm | 4.199864 MPa | 28.951763 N·m |
| Fixed-fixed (`PL³/192EI`) | 0.02285848 mm | 2.099932 MPa | 14.475881 N·m |

Each end reaction is **96.505875 N per rail**. Fixed ends require hogging
connection moment of 14.475881 N·m. These are support sensitivities, not a
guaranteed bracket stiffness range; a loose joint can be more flexible than
either model. There is no arbitrary “10–20% inertia knockdown.” Axial/lateral
frame loading, eccentric rail sharing, local slot and fastener effects, foot
fixity, buckling, fatigue, thermal loads and modes remain unqualified.

### Tension-only anchors and uplift

Separate **illustrative** inputs: thrust height h=0.35 m above pad, toe-to-opposite
anchor-row distance b=0.10 m, two anchors (one per row), centered downward load
W=0 N (no credit for unknown ballast). Global +X thrust at +Z height gives +Y
overturning, lifting the −X row and compressing the +X toe. For either thrust sign:

```
M = thrust*h
Trow = max(0, abs(M)/b - W/2)
Ctoe = W + Trow
uplift: Ctoe*b/2 + Trow*b/2 = abs(M)
no uplift: Trow=0, bearing resultant offset=abs(M)/W within b/2
```

Actual tool result: **M=252.35 N·m; active anchor tension=2523.5 N; inactive
anchor tension=0 N; bearing compression=2523.5 N; shear=360.5 N per anchor**.
Vertical residual is zero; moment residual is about 2.8e-14 N·m. Bearing is
compression-only, anchors tensile-only. Equal anchor shear assumes no friction
credit and equal shear stiffness. Load reversal, no-uplift and onset-of-uplift
cases are tested. The model rejects negative W (net vertical uplift is outside
this model), odd row populations and zero lever arms. No anchor grade, substrate,
embedment, edge distance, baseplate/prying capacity or ballast is inferred.

## R16 — real schema validation and current outputs

All **three existing CSV headers** match exactly; all are header-only:

| File | Rows | Result |
|---|---:|---|
| `records/part_release.csv` | 0 | INCOMPLETE |
| `records/build_traveller.csv` | 0 | INCOMPLETE |
| `records/test_results.csv` | 0 | INCOMPLETE |

The checker enforces exact schema/order, row width, required values, finite
positive mass and nonnegative global station, revision tokens, real nonfuture
dates/UTC timestamps, interface IDs and explicit result/disposition/phase enums.
CG checks are numeric sanity only, not whole-aircraft acceptance. Traveller
results may be descriptive or signed readings; numerical NaN/Inf is rejected.

It checks each evidence file exists, is a regular file and resolves within the
repository. Absolute paths, `..`, Windows path forms, symlink loops/escapes and
directory references are rejected. Evidence SHA-256 is recalculated; source,
configuration and analysis commits must resolve to actual Git commits. The part
artifact must match the source-commit blob; joined hardware must have the same
artifact hash at the test configuration commit. A real commit is provenance,
not proof that its author approved the content. CSV `analysis_command` is never
executed. Work on a stable evidence snapshot; this is not protection against a
concurrent malicious filesystem writer.

### Checker conventions (existing columns, no schema change)

- All evidence paths are repository-relative, including material certificates,
  acceptance-source documents and uncertainty records. `calibration_ids` uses
  semicolon-separated certificate-file paths as IDs; bare unresolved instrument
  labels cannot establish certificate existence. Certificate validity/range,
  calibration scope and authenticity still require review.
- `interface_ids`: semicolon-separated I-01… I-12 or explicit `NONE`.
  `hardware_serials`: semicolon-separated serial/lot values, each resolving to
  exactly one part row. Ambiguous serials across parts/revisions are rejected;
  do not guess which revision was tested. Parent assembly can be an external
  controlled assembly ID and is not falsely required to be another released row.
- Revision and process/instruction revision tokens use letters/digits, `_`, `.`,
  `-`, at most 64 characters. Operation instruction revision is not forced to
  equal the assembly process revision: subordinate instructions may differ.
- Part/build disposition enum: `RELEASED`, `CONDITIONAL`, `REJECTED`, `NOT RUN`,
  `INCOMPLETE`, `OPEN`, `PENDING`, `QUARANTINE`. Test result enum: `PASS`, `FAIL`,
  `NOT RUN`, `INCOMPLETE`, `CONDITIONAL`. Phases: G0–G7, COUPON, PROOF, BENCH,
  GROUND, FLIGHT, DEVELOPMENT. Unknown values are invalid, not normalized into
  acceptance. Rejected/conditional/quarantine operations require deviation IDs.
- All columns are required to contain values except an inapplicable
  `deviation_id`; `NONE` can explicitly record no next permitted test or no
  applicable interface. Incomplete/unperformed records are retained but cannot
  establish a consistent completed package merely by omitting evidence fields.
- Joins use `(part_number, revision, serial_or_lot)`, unique operation IDs per
  part and unique test IDs. A declared released part requires at least one
  released traveller and linked passing test. Failed/unperformed/open rows keep
  the package incomplete. This is minimum linkage, **not completeness of all
  required operations or acceptance characteristics**.

The current schemas cannot authenticate signatures, distinguish truthful from
fabricated/simulated data, prove instrument calibration fitness, link every
instruction to an approved process, or establish that every required physical
test occurred. Those are explicit unresolved review tasks, not inferred from
checksums. Even the synthetic test fixture with matching hashes and fake reviewer
names returns only **CONSISTENT_UNVERIFIED**. No synthetic fixture is installed
in `records/` or represented as measured hardware evidence.

## Review findings fixed and evidence still required

Implementation review fixed: thrust bypass, omitted dynamic moment, assumed CG
offset presented as conservative, extrusion yield reused for bolts, ignored
shear allowable, incorrect supplier weight conversion, unsupported joint-inertia
knockdown, compressive anchor “forces,” missing bolt equilibrium, header-only
schema bypass, missing-field bypass, NaN acceptance, unchecked hashes, unsafe
paths, date-format-only checking, unknown enums, missing Git provenance and
missing cross-record linkage. All former unqualified bolt/frame/anchor PASS/FAIL
claims have been removed from this worker's implementation.

Remaining evidence for **R13**, E1/E2 with E3/E5:

1. Released load-path/adapter/rail/bracket/footing drawings, actual bolt plane and
   CG/force-line offsets, load combinations, support/anchor geometry, certified
   extrusion and selected fastener/rod-end/cell/rail/substrate data.
2. Reviewed joint/contact/prying and coupled-load checks, anchor bearing/pullout/
   breakout/slip and overturning design, thermal/fatigue/modal assessment.
3. Approved cold proof plan derived from those completed checks: calibrated
   applied loads in each governing direction, defined limits on deflection,
   slip, residual deformation and inspection, and signed results. No numerical
   proof multiplier or loading instruction is invented here.
4. Engine-off tare with installed hoses/cables; traceable installed calibration
   in both loading directions over the intended range, hysteresis/creep/thermal
   drift and uncertainty records. Do not tare away real idle thrust. Measured
   fixture modes and verified acquisition timing/filters/abort remain required
   with E3 under R11/R12; static calculations do not validate instrumentation.

Remaining evidence for **R16**, E1–E5:

- Matched drawing/CAD/BOM revisions, datums/transforms/tolerances and inspection
  acceptance; material lots/certificates and reviewed substitution decisions.
- Selected supplier-qualified composite resin/fibre/bond/cure instructions,
  approved operation revisions, actual part-temperature/pressure histories,
  operator/inspector/deviation records and coupons/NDI/dimensional reports.
- Hot-section alloy/build orientation/stock or powder, heat treatment, coating,
  wall/hole inspection and thermal-cycle qualification records.
- Actual instrument certificates, raw test logs and uncertainties linked to
  serialised hardware, authenticated dated owner/interface review and release.

No physical manufacture, proof test, calibration or hot run occurred in this
task. Principal coordinator owns integration of this report into global trackers.
