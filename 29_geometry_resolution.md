# R01–R03 geometry resolution study

**2026-09-16 · input baseline `9db2fd0` · PROPOSED / findings OPEN.**
Source: `tools/geometry_candidates.py`; tests: `tests/test_geometry_candidates.py`.
This is an analytic candidate study. No STEP regeneration, pinned CadQuery
execution, assembly interference check, tooling qualification or physical fit
test occurred. Baseline CAD and controlled dimensions retain their authority.

```sh
python3 tools/geometry_candidates.py
python3 -m unittest tests.test_geometry_candidates -v
```

## R03: one explicitly stated planform interpretation

Use 18 §3.2's b=0.95 m, S=0.14 m², taper=0.4, LE sweep=30° and t/c=4%.
The trapezoidal area includes the hidden centreline root. Coordinates are nose
origin, +X aft, +Y right, +Z up; spanwise sections use positive local semispan.

| Script-derived quantity | Value |
|---|---:|
| Centreline root chord | 210.526316 mm |
| Tip chord | 84.210526 mm |
| MAC = integral(c² dy)/integral(c dy) | 156.390977 mm |
| Chord at y=92.5 mm | 185.927978 mm |
| Exposed semispan at constant y=92.5 mm cut | 382.5 mm |
| Full trapezoidal area | 0.140000000 m² |
| Exposed area at that cut | 0.103327978 m² |

Sweep translates a section in X; it does not subtract twice the sweep offset
from its chord. `x_LE(y)=x_LE,centre+abs(y)*tan(30°)`. Root LE station is an
explicit caller input, not inferred from I-04. The 92.5 mm cut uses **maximum**
body radius: actual curved wing/body intersection depends on local body radius,
wing vertical position and root station and is unresolved. Thus this convention
supports the load screens in 30; it does not approve the original rib stations.

## R01: continuous candidate, with demonstrated packaging failures

Candidate outer-radius knots (x m, R m) are `(0,0), (.85,.0925),
(1.05,.086), (1.39,.0925), (1.80,.0925), (2.60,.055)`.
Max radius and waist trace to 18 §3.1; downstream knots/tail radius trace to
`fuselage_manufacturing/01_mould_coordinates.md` §1.5. Between knots use
`R=Ra+(Rb-Ra)*(3t²−2t³)`, `t=(x−a)/(b−a)`.
Zero endpoint slopes are a **new proposal**. This gives C1 continuity and
bounded, nonnegative radii; it does not demonstrate suitable aerodynamics,
curvature continuity, a manufacturable nose tip or an acceptable intake layout.

Local envelope screen uses illustrative 1 mm radial skin and 3 mm duct wall:

| Station | Outer R | 103 mm throat + wall clearance | 175 mm engine clearance |
|---|---:|---:|---:|
| 300 mm | 26.433951 mm | −29.066049 mm | not an engine location |
| 600 mm | 73.201710 mm | +17.701710 mm | not an engine location |
| 1050 mm | 86.000000 mm | +30.500000 mm | −2.500000 mm if occupied |
| 1200 mm | 88.679117 mm | +33.179117 mm | +0.179117 mm |
| 1390–1800 mm | 92.500000 mm | +37.000000 mm | +4.000000 mm if occupied |

The throat already fails at 300 mm; the 105 mm lip in I-02's 50–150 mm
region also cannot fit this axisymmetric nose (R at 150 mm is 7.625178 mm).
Even positive engine radial clearance omits mount, tolerances, plumbing,
firewall and thermal growth. An axial engine envelope is still required.
The inner-radius subtraction is only a local envelope allowance; where it is
negative near the tip it signals failure of that allowance, not an inner solid.

I-04's “200×100 mm” lacks a complete axis/depth definition. Its 200 mm is
consistent with axial length 950–1150 mm, so treating it automatically as a
transverse width was unjustified. The screen now requires explicit transverse
width/height and uses corner radius `hypot(w/2,h/2)`. It cannot certify I-04.
Tank/bladder, duct, avionics and ballast must be packaged simultaneously, not
cleared independently against an empty outer cylinder.

## R02: finite-width section fit remains open

Parabolic biconvex half-thickness is `h=2(t/c)c u(1−u)`. The 50 mm cap screen
at 30% chord subtracts 0.5 mm skin on each face and **one** 1 mm cap thickness
from minimum outer depth to obtain cap-centroid separation. At the exposed
root this gives depth **4.109337 mm**, separation **2.109337 mm**; at the tip
separation is **−1.958026 mm**. The rejected 7 mm separation fails every rib.
Negative separation means the assumed cap/skin combination cannot fit.

The 6 mm wing hole with 0.5 mm vertical web allowance fails even the centre
thickness test at every candidate rib (root margin −0.376410 mm). Full-width
enclosing-rectangle checks are conservative sufficient containment tests, not
actual normal-offset DXF or tolerance/ligament qualification.

The stabilator study explicitly combines the 6% section option with a 2.5 mm
spar at 30% chord; 18 §3.3 presents alternatives, not an approved combination.
Legacy local spans 0/60/120 mm give chords 90/64.285714/38.571429 mm.
Root half-thickness at the spar is **2.268 mm**, not 4.536 mm. Tip
half-thickness is **0.972 mm**, below the 1.25 mm hole radius. Even placing
that hole at maximum thickness leaves only 1.157143 mm half-depth at the tip.
Tapered spar/cap/web design, bearings/external clevis, pockets, bonded joints,
ligaments, tolerances and matched net parts remain E1/E5 deliverables.

## Exact review corrections / remaining decisions

Corrected fabricated cubic coefficients and junction jumps; sweep/taper mix-up;
full/exposed area claims; factor-of-two half-thickness and cap-offset errors;
false hole/root-fit tests; unsubstantiated I-04 cross-section interpretation;
outer-radius-only packaging claims; misleading duplicate CSV chord headings.
Tests now independently integrate area/MAC, check two-sided C0/C1 continuity
and numerical derivatives, reproduce packaging failures, and validate domains
and exported station values. Candidate export functions remain opt-in.

E1/E5 must approve body law, wing reference station and detailed fit design;
E2 owns engine/intake occupancy; E3 owns simultaneous tank/avionics packaging.
The principal handles global index/tracker integration. No finding is closed.
