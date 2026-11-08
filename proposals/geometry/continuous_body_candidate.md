# Continuous Fuselage Body-Law Candidate (R01 decision input)

**Date:** 2026-11-08 · **Status:** PROPOSED, not a released mould.
**Tool:** `tools/fuselage_profile.py` · **Table:** `proposals/geometry/fuselage_stations_v3.csv`
**Tests:** `tests/test_fuselage_profile.py`

## 1. Defect being addressed

The released mould table (`fuselage_manufacturing/01_mould_coordinates.md`)
uses, for the forebody,

```
R(x) = 0.0925 · sin(π·x / 0.85)
```

This sine completes a half period at x = 0.85 m, so **R = 0 there** — the
fuselage pinches completely shut (25 R01, `FUSE-CONTINUITY`). The adjoining
cosine cannot repair a zero-radius station. This is a law problem, not a
table-rounding problem.

## 2. Candidate law

Same knots as 29 §R01, joined by smoothstep (zero slope at every knot):

| x (m) | R (m) | Meaning |
|---:|---:|---|
| 0.00 | 0.0000 | nose tip |
| 0.85 | 0.0925 | maximum radius (185 mm OD) |
| 1.05 | 0.0860 | area-ruled waist (172 mm OD) |
| 1.39 | 0.0925 | engine/AB bay |
| 1.80 | 0.0925 | bay end |
| 2.60 | 0.0550 | AB nozzle fairing |

Between knots: `R = Ra + (Rb−Ra)(3t² − 2t³)`, `t = (x−a)/(b−a)`.

Generated result (53 stations, 50 mm pitch):

| Metric | Value |
|---|---:|
| Maximum radius | 92.5 mm |
| Minimum interior radius | 0.92 mm at x = 50 mm |
| Nose / tail radius | 0.0 / 55.0 mm |
| Knot slopes | ≈ 0 (C1) |
| Interior pinch | none |

`proposals/geometry/fuselage_stations_v3.csv` carries `x_mm, R_mm, OD_mm`.

## 3. What this does not fix

- The **intake still does not fit**: at x = 300 mm the outer radius is 26.4 mm,
  far below the 103 mm throat plus wall (29 §R01). A sharp nose that grows to
  92.5 mm at 0.85 m leaves no room for the documented pitot intake.
- No aerodynamic optimisation, curvature-continuity proof, nose-tip
  manufacturability or boundary-layer study is included.
- The 1.05 m waist and 1.39–1.80 m bay are inherited from 18/29; the engine
  mount, tank and avionics packaging are not re-checked here.

## 4. Disposition

This candidate shows that the **pinch is removable with a one-line law change**,
which is the first R01 sub-item. It does not close R01: E1/E2 must choose a body
law jointly with an intake/engine layout that fits it, then regenerate the
controlled mould table and matched bulkheads. The released table is unchanged.

Run `python3 tools/fuselage_profile.py --write` to regenerate the CSV.
