# Fit-First Wing Box-Spar and Net-Rib Candidate

**Date:** 2026-11-10 · **Status:** PROPOSED for E1/E5 review; not released.
**Tool:** `tools/wing_box_spar.py` · **Tests:** `tests/test_wing_box_spar.py`
**Artifacts:** `proposals/structure/wing_box_spar/`

This addresses the specific R02/R03/R04 geometric failures without changing the
controlled planform: b = 0.95 m, S = 0.14 m², taper 0.4, LE sweep 30°,
t/c = 4%. It does not close strength, buckling, fatigue, bonded-joint or
flutter findings.

## 1. Why the old spar was replaced

The rejected 50 mm-wide cap at 30% chord sees only 4.980 mm outer depth at
its forward edge, leaving 2.980 mm cap-centroid separation before bond
allowance (20 §3). A 6 mm round hole also breaks out of the ribs. Shrinking
those holes would not create a viable load path.

The candidate moves the load-carrying box to **50% chord, the maximum-thickness
station**, and sizes chordwise cap width from the available depth instead of
prescribing depth from a desired cap stack.

## 2. Construction

- Upper and lower caps taper from **1.0 mm** at the centreline to **0.4 mm**
  at the tip.
- Two **1.0 mm** shear walls sit at the cap leading/trailing edges, forming a
  closed box with the caps. The box supplies a torsion cell; no torsion
  stiffness is calculated here.
- Ribs are **front and rear closed net segments outside the box**, bonded to
  its side walls and the skins. There is no spar through-hole to break out.
- Skin = 0.5 mm and bond = 0.2 mm per face are retained from doc 30.

## 3. Load and fit method

Chord-proportional lift at 9g is scaled so the centreline root moment is at
least the **150 N·m** interface reference. The same scale is applied to shear
and moment outboard. Cap width is iterated because the available cap-centroid
separation depends on the cap footprint:

```
d = min(depth at cap edges) − 2(skin + bond) − cap_thickness
A_each_cap = M / (d · sigma)
width = A_each_cap / cap_thickness
```

**sigma = 400 MPa is an input sensitivity, not a sourced laminate allowable.**
The resulting force couple is consistent by construction, but the material
must still be qualified for tension, compression, buckling and environment.

## 4. Candidate schedule

`python3 tools/wing_box_spar.py` reproduces:

| Station | Chord mm | Moment N·m | Cap t mm | Width mm | Separation mm | Box inner height mm | Web shear MPa |
|---|---:|---:|---:|---:|---:|---:|---:|
| C0 centreline | 210.53 | 150.00 | 1.00 | 76.30 | 4.92 | 3.92 | 94.10 |
| R0 body side | 185.89 | 90.89 | 0.88 | 58.15 | 4.43 | 3.54 | 76.73 |
| R1 | 165.58 | 54.86 | 0.79 | 43.92 | 3.97 | 3.18 | 63.16 |
| R2 | 145.26 | 29.01 | 0.69 | 30.31 | 3.47 | 2.78 | 49.91 |
| R3 | 124.95 | 12.08 | 0.59 | 17.51 | 2.91 | 2.31 | 36.46 |
| R4 | 104.53 | 2.79 | 0.50 | 6.20 | 2.27 | 1.77 | 21.40 |
| R5 tip | 84.21 | 0.00 | 0.40 | 2.00 | 1.57 | 1.17 | 0.00 |

All stations have positive separation, positive box height and cap footprints
inside the chord. Total cap volume is **52.68 cm³ for both wings**; no density
or mass claim is made without a material selection.

## 5. Net-part evidence

`stations.csv` records the schedule. Fourteen `rib_*_front/rear.dxf` files
contain one closed LWPOLYLINE each. The tests check:

- cap force/stress consistency at the root;
- positive fit at every station;
- every rib vertex lies inside the outer airfoil contour;
- no degenerate rib polygons and no spar holes;
- committed CSV/DXF artifacts reproduce the generator exactly.

## 6. Remaining work before release

1. Select an actual laminate and source tension/compression/shear allowables,
   then re-run cap widths with process, temperature and moisture knockdowns.
2. Size the two webs and closed cell for shear, torsion, local buckling and
   crippling; the listed web shear is only a sensitivity.
3. Detail cap/web/rib bonds, peel and joint fastener loads, tolerances and
   manufacturing sequence; closed-box cure access needs explicit review.
4. Reconcile the 6g/9g/150 N·m load contract and add gust, asymmetric, tail
   trim, launch/landing and joint cases.
5. Generate matched spar tooling and assembly STEP, then run interference and
   physical proof tests. A fitting candidate is not strength evidence.
