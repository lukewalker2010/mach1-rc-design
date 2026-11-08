# Mass/CG Closure Candidates (R05 decision input)

**Date:** 2026-11-08 · **Status:** PROPOSED, not an approved layout.
**Tool:** `tools/cg_candidates.py` · **Tests:** `tests/test_cg_candidates.py`
**Baseline:** 18 §3.4 rows; CG contract 0.975 ± 0.020 m (0.955–0.995 m).

This note answers the R05 question left open in 31 §2: *what single change
makes the existing mass table close both fuel states?* It does not change any
controlled station. The candidates below require owner review of the fuel-bay
(I-06) and/or engine-mount interfaces.

## 1. The binding constraint

| State | Mass (kg) | CG (m) |
|---|---:|---:|
| Full | 13.600 | 0.974809 |
| Empty | 11.980 | 1.045776 |

Empty CG is 50.8 mm aft of the limit. Fixing it needs **0.6083 kg·m** of
forward dry moment. Nose ballast alone is infeasible at the controlled fuel
station: it needs ≥0.6797 kg for empty but ≤0.3151 kg for full (31 §2).

The missing degree of freedom is the **fuel centroid**. With dry CG pinned at
the aft limit, the full-fuel constraint gives

```
M >= m_f (CG_MAX − x_f) / (CG_MAX − CG_MIN)
x_f >= CG_MAX − M (CG_MAX − CG_MIN) / m_f = 0.6592 m   at M = 13.60 kg
```

So a tank centroid of **0.66 m** (vs I-06's 0.35–0.60 m) is the threshold that
lets the 13.60 kg aircraft close both endpoints.

## 2. Candidates (tool output)

| Candidate | Change | Full CG | Empty CG | MTOW | Verdict |
|---|---|---:|---:|---:|---|
| **A** | fuel @ 0.66 m + 1.68 kg nose ballast | 0.9570 | 0.9950 | 14.28 kg | closes at the limit |
| **B** | fuel @ 0.66 m + engine mount @ 1.076 m | 0.9551 | 0.9950 | 13.60 kg | closes at the limit |
| **A-margin** | fuel @ 0.81 m + 1.82 kg ballast | 0.9650 | 0.9850 | 14.42 kg | 20 mm inside band |

All three are under the 25 kg limit. A and B sit exactly on the acceptance
boundary, so they are **not** robust to the ±10 mm-level uncertainty in 31 §3;
A-margin is the only one with usable margin, and it needs a fuel centroid near
0.81 m.

## 3. What each candidate costs

- **A / A-margin** keep the 1.20 m engine mount but add 0.68–0.82 kg of nose
  ballast (total ~1.7–1.8 kg tungsten) and require the fuel bay to extend aft
  to 0.66–0.81 m. The added ballast is inert mass and increases landing energy.
- **B** keeps MTOW at 13.60 kg but moves the engine mount to 1.076 m, which
  conflicts with the wing carry-through (0.95–1.15 m) and shortens the intake
  duct. It has zero CG margin.

No candidate resolves packaging: a 2 L bladder centroid at 0.66–0.81 m must
physically fit around the carry-through, and ballast needs a mounted volume and
attachment loads. Those are E1/E3 deliverables.

## 4. Recommendation for the decision review

1. Treat **fuel-station range** as the primary variable: without x_f ≥ 0.66 m,
   no combination of nose ballast, engine move or avionics relocation closes
   the band at ≤25 kg with this dry mass.
2. If the fuel bay cannot move aft, the dry mass must fall or the CG band must
   be renegotiated — not waived.
3. Any selected candidate still needs a measured weigh-off, a Mach-dependent
   neutral-point/trim check and independent uncertainty data (31 §3).

Run `python3 tools/cg_candidates.py` to reproduce the table.
