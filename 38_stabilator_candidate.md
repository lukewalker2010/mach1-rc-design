# Feasible Stabilator Section Candidate (R02 / I-05)

**Date:** 2026-11-10 · **Status:** PROPOSED for E1/E5 review; not released.
**Tool:** `tools/stabilator_candidate.py` · **Tests:** `tests/test_stabilator_candidate.py`
**Artifacts:** `proposals/structure/stabilator_candidate/`

This resolves the two geometric impossibilities in 18 §3.3 / 25 R02 without
changing the controlled 6% stabilator outline, chords or 30% hinge line.

## 1. Defects addressed

| Defect | Cause |
|---|---|
| `STA_TIP` spar-hole breakout | Constant 2.5 mm spar has radius 1.25 mm; tip half-thickness at 30% chord is only 0.972 mm |
| 8 mm hinge-bearing pockets impossible | Root section is 5.4 mm thick; an 8 mm bearing cannot fit inside the aerosurface |
| Bearing pockets interrupt the spar | Legacy rod was kinked around pockets inside a 1–5 mm section |

## 2. Candidate construction

- Keep the **biconvex 6% t/c**, root chord 90 mm, tip chord 38.571 mm,
  half-span 120 mm, hinge line at 30% chord.
- Taper a **Ti-6Al-4V spar from 2.5 mm at the root to 1.4 mm at the tip**
  (0.1 mm diametral hole clearance).
- Move the hinges to an **external clevis** on the fuselage side; the
  aerosurface carries only the spar hole, no bearing pockets.
- Use the **full-depth Ti-alloy laminate** from 18 §3.3 to carry surface
  loads. Laminate schedule, bond and allowables are not selected here.

Spar diameter: `d(z) = 2.5 − 1.1·z/120` mm.
Chord: `C(z) = 90 − 51.4286·z/120` mm.

## 3. Section fit (reproducible)

| Section | z mm | Chord mm | Max t mm | t at 30% mm | Spar mm | Hole mm | Edge margin mm |
|---|---:|---:|---:|---:|---:|---:|---:|
| STA_ROOT | 0 | 90.00 | 5.400 | 4.536 | 2.50 | 2.60 | 0.968 |
| STA_MID | 60 | 64.29 | 3.857 | 3.240 | 1.95 | 2.05 | 0.595 |
| STA_TIP | 120 | 38.57 | 2.314 | 1.944 | 1.40 | 1.50 | 0.222 |

Every station now has positive edge margin. The former failure boundary is
still visible in the test: the constant 2.5 mm radius 1.25 mm exceeds the
0.972 mm tip half-thickness. Tapered spar volume is 367.9 mm³ per side,
consistent with the existing ~2.4 g-per-side estimate.

## 4. Net-part evidence

`STA_ROOT/MID/TIP.dxf` each contain exactly two closed LWPOLYLINEs: outer
section and spar hole. There are **no bearing pockets**. Tests verify:

- exact baseline chords and 6% thickness law;
- positive margin at all three sections, including >0.2 mm at the tip;
- every spar-hole vertex lies inside the outer contour;
- committed CSV/DXF artifacts reproduce the generator.

## 5. Remaining work before release

1. External clevis/bracket and 4 mm pin loads, bearing selection, bolt path
   into the tailcone, freeplay and stiffness.
2. Ti-alloy laminate schedule, ply orientation, bonding, lightning/EMI and
   allowables with environmental knockdowns.
3. Hinge-moment and control-authority validation across the Mach/q envelope.
4. Flutter/aeroelastic model correlated to ground vibration; the 2.5→1.4 mm
   spar is a fit candidate, not a stiffness or flutter clearance.
5. Physical section proof, torques and inspection per 27. No release is implied.
