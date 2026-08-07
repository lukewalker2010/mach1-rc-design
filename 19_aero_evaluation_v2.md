# Aerodynamic Evaluation v2 (Re-baselined Geometry)

**Doc:** 19 — supersedes 12 (audit D4: re-run on re-baselined geometry)
**Author:** E1 (Airframe) + AI verification
**Date:** 2026-08-06
**Status:** 🟢 closure verified on re-baselined geometry
**Authority:** `18_program_requirements.md` §2/§3 (drag contract ≤ 430 N hump, wing §3.2, mass §3.4)

> **Every number below is produced by `tools/aero_evaluation.py` + `tools/structural_analysis.py` (committed, AGENTS.md §4.4).** MTOW = **13.60 kg** per the 18 §3.4 table as published. Induced drag is negligible (~0.1 N), so mass deltas move totals < 1 N. **Sensitivity (P0 change-notice to 18):** E2 re-derived the AB mass at 0.97 kg (18 lists 0.83) → MTOW 13.74 kg; stability stays PASS (full SM +71.6%, empty +26.2%, see §4).

---

## 1. Reference conditions

| Quantity | Value | Source |
|---|---|---|
| Altitude (dash window) | 10,000–12,000 ft (3,048–3,658 m) | 18 §2.3 |
| ρ @ 10 kft | 0.905 kg/m³ | ISA (18:36) |
| a @ 10 kft | 328 m/s | 18:37 |
| S_front | π·0.0925² = 0.0269 m² | 18 §3.1 |
| S_w | 0.14 m² | 18 §3.2 |
| Swet (body, shape-factor approx) | 0.78 m² | analysis model |
| MAC | 0.156 m | 18 §3.2 |
| MTOW | 13.60 kg | 18 §3.4 |

---

## 2. Drag buildup (10,000 ft)

Computed by `tools/aero_evaluation.py` (Sears–Haack body wave + transonic factor, flat-plate skin friction, wing wave via M·cos30° clamped to subsonic floor, tail 25% wing, intake/base/excrescence, induced).

| M | waveB | fricB | fricW | waveW | tail | int | base | excr | ind | **Total (N)** |
|---|---|------|------|------|------|-----|-----|------|------|-----|--------|
| 0.85 | 53 | 62 | 39 | 20 | 15 | 8 | 5 | 6 | 0.2 | **207** |
| 0.95 | 76 | 75 | 48 | 25 | 18 | 10 | 6 | 7 | 0.2 | **264** |
| 1.00 | 94 | 83 | 52 | 27 | 20 | 11 | 7 | 8 | 0.2 | **301** |
| **1.05** | **111** | **90** | **57** | **30** | **22** | **12** | **7** | **9** | 0.1 | **338** |
| 1.10 | 113 | 98 | 62 | 52 | 29 | 14 | 8 | 10 | 0.1 | **385** |
| 1.20 | 116 | 115 | 72 | 164 | 59 | 16 | 9 | 11 | 0.1 | **563** |

### At 12,000 ft (3658 m)

| M | **Total (N)** |
|---|---|
| 1.00 | 280 |
| **1.05** | **314** |
| 1.10 | 358 |
| 1.20 | 523 |

---

## 3. Thrust–drag closure (the make-or-break, 18 §2)

| Condition | Drag (N) | Wet thrust (N) | Margin | Verdict |
|---|---|---|---|---|
| **M1.05 / 10 kft (hump)** | **338** | 451–474 (1800 K) | **+113 to +136 N (+33–40%)** | **PASS ≤ 430 N contract** |
| M1.10 / 10 kft (sustain) | 385 | 451–497 | +66 to +112 N | PASS |
| M1.05 / 12 kft | 314 | 451–474 | +137 to +160 N | PASS |
| M1.20 / 10 kft | 563 | 465 (design pt) | −98 N (drag > thrust) | NOT sustainable — outside dash window, dive-only |

**Key results:**
- **Hump drag 338 N vs the 430 N hard contract** (18 §2.3) → **92 N design margin** on the airframe, on top of the wet-thrust margin. The re-baselined 185 mm × 2.6 m body (fineness 14) delivers the drag reduction 18 §2.2 requires.
- Sustain at **M1.10 (385 N)** is below the lowest wet-thrust point (451 N @ T7 1700 K, 21 §1) — so even a bench-limited 1700 K AB closes the sustain case.
- The 18 §2.2 estimate (~410–420 N hump) is **conservative** vs the 338 N model; the model's total sits mid-way between 18's subsonic breakdown (303 N) and its transonic-factor estimate.
- M1.20 is beyond the mission envelope (18 §2.3 dash is M1.05–1.10); the +10 N "dive headroom" claim in 18 §2.2 is **not supported** at M1.20 and should be treated as dive-transition-only.

---

## 4. Stability & trim (CG / neutral point)

Mass table per 18 §3.4 (as published, AB 0.83 kg), stations unchanged:

| Component | Mass (kg) | Station (m) |
|---|---|---|
| Engine | 4.90 | 1.20 |
| Afterburner | 0.83 | 1.48 |
| Wing + carry-through | 0.50 | 1.00 |
| Stabilator + hardware | 0.10 | 2.35 |
| Ventral fin | 0.10 | 2.30 |
| Fuselage structure | 2.50 | 1.30 |
| Fuel | 1.62 | 0.45 |
| Fuel system | 0.50 | 0.60 |
| Avionics + batt + FPV + M&V | 0.90 | 0.25 |
| Landing/dolly | 0.35 | 0.80 |
| Nose ballast | 1.00 | 0.10 |
| Misc | 0.30 | 1.00 |
| **Total** | **13.60** | |

Stability computed in `tools/structural_analysis.py`. The neutral point must include the **stabilator contribution**:

```
Xac_wing = wingLE + 0.25·MAC = 0.96 + 0.039 = 0.999 m
NP       = Xac_wing + 0.8·(S_t/S_w)·(x_tail − Xac_wing)
         = 0.999 + 0.8·(0.012/0.14)·(2.35 − 0.999) = 1.092 m
```

| Load | MTOW (kg) | CG (m) | SM vs NP=1.092 (tail-incl) | SM vs NP=0.999 (wing-only) |
|---|---|---|---|---|
| FULL | 13.60 | 0.975 | **+74.9% MAC** | +15.5% |
| EMPTY | 11.98 | 1.046 | **+29.4% MAC** | −30.0% **FAIL** |

**Resolution (18 §3.4 CG claim, E3 finding):** E3's "empty SM = −30% → FAIL" used the **wing-only NP (≈1.00 m)**, which neglects the stabilator's stabilizing contribution. With the full-aircraft NP (1.092 m, tail included), **both fuel loads exceed the ≥12% MAC rule** (empty +29%, full +75%). The 18 §3.4 layout is stable as published — the "empty ≥12%" claim in 18 §3.4 holds once the tail is included.

> ⚠️ **P0 follow-up:** full-load SM of +75% MAC is far above the 12–20% design band. It gives very strong pitch stability but demands large tail download at rotation/low speed, and stiffens pitch response. **Verify pitch authority and rotation capability at the stabilator servo (20 §3) before flight test**; if excessive, move the 1.0 kg nose ballast aft (or shift CG target aft) in a change-notice PR to 18. Target CG 0.975 m ±20 mm is maintained by the table (CG 0.975 m full).
>
> **AB-mass sensitivity (E2, P0 for 18):** if AB = 0.97 kg (→ MTOW 13.74 kg), full CG = 0.980 m, empty CG = 1.051 m; tail-incl SM +71.6% full / +26.2% empty — still PASS ≥ 12%.

---

## 5. Reynolds numbers & low-Re implications

| Component | Chord/Length | Re @ M1/10 kft |
|---|---|---|
| Wing (MAC 0.156 m) | 0.156 m | **2.7×10⁶** |
| Fuselage (2.6 m) | 2.6 m | **45.6×10⁶** |

- Wing Re = 2.7×10⁶ is transitional; turbulent Cf used (0.074/Re^0.2), so drag is conservative vs any partial laminar run.
- 12 §4's warnings (SWBLI, transition modeling) still apply: **the 92 N hump margin is the buffer for model error**; validate M0.85–0.97 transonic probes (18 §6 G4) before the first wet dash.
- CNC seamless skins + gap-free LE/TE are required to hold the model's friction/wave numbers (18 §2.3).

---

## 6. Area rule & surface quality (12 §5 carried forward)

- Body BL δ* ~1.6 mm at this scale; 50–70% of theoretical area-rule benefit achievable (12 §5.3). The re-baselined slimmer body reduces the sensitivity.
- The 18 §3.1 area-ruled waist (172 mm @ x≈1.05) and the corrected mould table (`fuselage_manufacturing/01_mould_coordinates.md`) implement the pinched waist; drag model uses Sears–Haack body only — **the pinch is not in the model**, so the 338 N hump is conservative if the waist is built per the mould table.

---

## 7. Verdict

```
────────────────────────────────────────────────────
  Hump drag @ M1.05/10kft     338 N   (contract ≤ 430)   PASS  +92 N margin
  Sustain   @ M1.10/10kft     385 N   (wet ≥ 451)        PASS
  M1.05 @ 12kft               314 N                       PASS
  Re_w @ M1/10kft             2.7×10⁶
  CG 0.975 m full / 1.046 m empty
  SM (tail-incl NP=1.092):    +74.9% full / +29.4% empty  PASS ≥ 12%
  M1.20 sustain               563 N > thrust              NOT in envelope
────────────────────────────────────────────────────
```

**Aerodynamic feasibility: CLOSED on the re-baselined geometry.** The single-P550+AB configuration closes thrust-vs-drag at M1.05–1.10 with ~30–40% margin, satisfying 18 §2.3 contracts. Remaining risks: (1) high full-load static margin → pitch-authority check (20 §3, 18 §6 G1), (2) model error buffer absorbed by the 92 N margin → transonic probes before first dash (18 §6 G4).

*Produced by `tools/aero_evaluation.py` (drag/closure) + `tools/structural_analysis.py` (stability), pinned CadQuery env. Supersedes 12's old-geometry (200 mm, 2.2 m, 60° sweep) results.*
