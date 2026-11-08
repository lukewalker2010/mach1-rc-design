# Afterburner CAD Repair and STEP Validation

**Date:** 2026-11-08 · **Scope:** afterburner concept CAD only.
**Status:** geometry defects repaired and import-validated; this is **not** a
design release. Coolant balance, hot clearances, petal motion and material
approvals remain open (see 21, 32 and 25 R08).

## 1. Defects found by STEP import inspection

The committed STEP files loaded but were not valid single solids. Importing
them with OpenCascade showed:

| File | Before | Defect |
|---|---|---|
| `ab_flameholder.step` | 3 solids | Self-intersecting bow-tie V-gutter profile left a zero-volume sliver; glow-plug boss detached |
| `ab_liner.step` | 2 solids | Inner liner and outer shell unconnected (spacer ribs missing from CAD); cooling inlet and film holes were axial, not through the wall |
| `ab_iris_nozzle.step` | 10 solids | 12 mm slots cut through a 7.5 mm-wide sync ring, severing it into six arcs; petals generated at 2x throat radius (r 45–57), outside the 100 mm ring; pivot pins sat on the axis |
| `ab_spray_ring.step` | 1 solid | No mounting flange, so the 4x bolt holes cut empty space; injectors pointed outward; body reached z = −2 mm |
| `ab_assembly.step` | 14 solids | A compound of touching/unconnected solids, not a fused assembly |

## 2. Repairs in the authoritative generators

- **`ab_flameholder_step.py`** — V-gutter rebuilt as an outer V solid minus an
  inner V solid (two simple triangles) instead of the self-intersecting
  polygon. Added outer/inner housing walls to the full 35 mm section, kept the
  six radial arms and the radial M10 glow-plug boss.
- **`ab_iris_nozzle_step.py`** — Petals now span throat radius (22.5 mm) to the
  100 mm ring OD; pivot pins are at r = 46 mm and pass through the mounting
  ring; sync-ring slots are 5 x 2.4 mm (ring stays continuous); limit stops
  overlap the ring.
- **`ab_liner_step.py`** — Added the three circumferential spacer ribs required
  by the fabrication note (welded to the shell in manufacture; modelled
  attached for a connected export); cooling-air inlet and film-cooling holes
  are now radial through-holes.
- **`ab_spray_ring_step.py`** — Added the 100/79 x 3 mm sandwich flange with
  4x M4 on 95 mm PCD, turned injectors inward into the flow, and removed the
  negative-Z overhang.
- **`ab_assembly_step.py`** — Places each part from its own generator at the
  AGENTS §2 station stack (0–100, 100–115, 115–150, 150–350, 350–385 mm) and
  adds a 2 mm weld/joint ring at the flame-holder-to-liner interface so the
  export is one connected solid.

## 3. Verification

```
$ python3 tools/step_validate.py
PASS ab_transition.step     solids=1 zero=0 z=0.0..100.0
PASS ab_spray_ring.step     solids=1 zero=0 z=0.0..15.0
PASS ab_flameholder.step    solids=1 zero=0 z=0.0..35.0
PASS ab_liner.step          solids=1 zero=0 z=0.0..200.0
PASS ab_iris_nozzle.step    solids=1 zero=0 z=0.0..35.0
PASS ab_assembly.step       solids=1 zero=0 z=0.0..385.0
```

`tests/test_step_geometry.py` runs the same gate in the regression suite (it
skips when OCP is not installed, so the standard-library CI is unaffected).

## 4. Remaining discrepancies (not resolved here)

- Sync-ring thickness is modelled **2 mm** so the iris fits the 35 mm section;
  doc 14 specifies 5 mm. One of the two documents must change before release.
- Film-cooling holes remain the legacy **20-hole** row; 21/32 discuss a
  105–115-hole revision. The thermal case must be re-run before either is cut.
- The iris is modelled at the **dry** position only. Travel, overlap, hot/cold
  clearance and fail direction are unverified (25 R08).
- The assembly joint ring is a CAD connection artifact, not a released part.
- No material, process, tolerance or physical evidence is implied by a clean
  STEP import. See 25/27.
