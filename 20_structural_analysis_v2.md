# Structural Analysis v2 (Re-baselined Geometry)

**Doc:** 20 — supersedes 10 (audit D4: re-run on re-baselined geometry)
**Author:** E1 (Airframe) + AI verification
**Date:** 2026-08-06
**Status:** 🟡 margins closed with the recommended box-spar sizing; pitch-authority follow-up open
**Authority:** `18_program_requirements.md` §3 (geometry), §2.3 (thrust 465 N design), INTERFACES.md I-01 (engine mount)

> **Every number below is produced by `tools/structural_analysis.py` (committed, AGENTS.md §4.4).** Load cases use MTOW = 13.60 kg (18 §3.4 table as published). Limit 4g / ultimate 6g load factors per 10 §1 (Mach-1 C_Lmax ceiling ≈ 11g hard limit, so 6g ultimate is the sizing case).

---

## 1. Dynamic pressure & loads at M1/10 kft

| Quantity | Value | Source |
|---|---|---|
| q @ M1/10 kft | 0.5·0.905·328² = 48,776 Pa | 10:28 (geometry-independent) |
| Wing area S_w | 0.14 m² | 18 §3.2 |
| MTOW | 13.60 kg → 133.4 N | 18 §3.4 |
| C_L for 1g @ M1 | 133.4/(48,776·0.14) = **0.0195** | — |
| C_Lmax (biconvex 4%, M1) | ~0.4 | 10:46 |
| Max load factor @ M1 | 0.4·48,776·0.14/133.4 ≈ **20g** (C_L-limited) | 10:48 re-derived |

The Mach-1 lift ceiling is not the binding constraint (20g > 6g). **The 6g ultimate case governs spar sizing.**

---

## 2. Wing box spar

### 2.1 Loads (trapezoidal lift, λ=0.4)

```
Ycg (lift centroid from root) = (1+2λ)/(3(1+λ)) · b/2 = 0.4286 · 0.475 = 0.2036 m
M_root = n·W·Ycg    V_root = n·W·(0.475−Ycg)/0.475
```

| Case | n | M_root (N·m) | V_root (N) |
|---|---|---|---|
| LIMIT 4g | 4 | **108.6** | **305** |
| ULT 6g | 6 | **163.0** | **457** |

### 2.2 Sizing constraint — thin wing

Root chord 0.210 m, t/c 4% → root max thickness **8.4 mm** (18 §3.2). Spar is at 30% chord where the biconvex half-thickness is `(t/2)·4·0.3·0.7` = 1.47·4.2·0.21 ≈ — **in practice the available cap separation inside the skin envelope is ~7 mm**. This rules out the 10 mm separations in earlier sweeps; **sep = 7.0 mm is the build limit**.

### 2.3 Recommended sizing (closes margins ≥ 2.0)

| Member | Sizing | Stress @ 6g | Capability | **Margin** |
|---|---|---|---|---|
| Upper/lower caps | **5 plies × 0.2 mm T300 UD × 50 mm** (area 5·0.2·50 = 50 mm²) | σ = M/(sep·A) = 163.0/(0.007·50e-6) = **466 MPa** | T300 comp 1200 MPa | **2.6×** |
| Shear web | **1.0 mm ±45° CF, sep 7 mm** (per side) | τ = V/2/(0.007·0.001) = **33 MPa** | ±45° ~90 MPa | **2.8×** |

- **vs 18 §3.2 "2 plies, 6 mm sep":** 18's §3.2 sizing gave σ = 163.0/(0.006·2·0.2e-3·0.05) = 1358 MPa → **margin 0.88 → FAIL**. The §3.2 "~100 N·m @ 9g" was from a different load arm. **The 5-ply/7 mm box is the change vs 18 §3.2 — flag in the change-notice PR.**
- Web margin 2.8× vs 10 §2's old failing geometry — the box web carries shear efficiently; 1.0 mm ±45° is buildable in a 7 mm bay.
- Cap stress at 4g limit = 310 MPa (margin 3.9×) — no fatigue concern for the 2-sortie/day duty.

### 2.4 Parametric sweep (for sensitivity)

`e1_sweep` (run during verification): at sep 7.0 mm the minimum passing cap is **4 plies × 50 mm** (σ=582 MPa, m=2.06); **5 plies recommended** for handling/misc mass growth to 14.5 kg. Web 1.0 mm passes all cases (m ≥ 2.7). Widening the cap to 60 mm adds no margin benefit over adding a ply and wastes 30% chord depth.

---

## 3. Stabilator & pitch authority (18 §3.3, 06)

| Quantity | Value | Source |
|---|---|---|
| S_t | 0.012 m² | analysis assumption |
| x_tail | 2.35 m | 18 §4 |
| c_avg | 0.06 m | analysis assumption |
| Servo | KST X20-12T, 1.18 N·m | BOM v2 (22) |

**Hinge moment @ M1, 15°:** M_h = q·S_t·c_avg·0.02 = 48,776·0.012·0.06·0.02 = **0.70 N·m** → servo margin **1.7×**.

> ⚠️ **Follow-up (P0, ties to 19 §4):** with full-load SM of +75% MAC the tail must carry a **trim download** at rotation that can exceed the 15° hinge case. **Verify rotation-pitch authority at the dolly-drop speed (≈38 m/s, 18 §5.4) and add tail load to the 6g case before flight.** If the servo margin closes to < 1.3, move ballast aft (19 §4) — this is the same change-notice item.

---

## 4. Engine mount (I-01: 4× M3 on 45 mm PCD @ 1200 mm)

| Load | Value |
|---|---|
| Wet thrust (design) | 465 N → 116 N shear/bolt |
| 5g vibration (engine+AB 5.87 kg) | 72 N/bolt |
| M3 A2-70 single-shear capacity | ~2113 N (documented in 14) |
| **Margin** | **> 18× (thrust), > 29× (vib)** |

No change from 14 — mount is not a constraint.

---

## 5. Thermal (AB shell → composite, 17 §2a carried forward)

AB outer shell runs at **≈610 K** (17:287). Composite Tg limit 410 K. **5 mm ceramic blanket (Cotronics 3633, k=0.05):**

```
Required ΔT  = 610 − 410 = 200 K
Leak flux    = k·ΔT/t = 0.05·200/0.005 = 2,000 W/m² = 3% of shell flux (76,000 W/m²)
```

**PASS** — the blanket carries only ~3% of the shell's heat outward (rest is taken by the annulus cooling air, 17 §2a); composite stays < 410 K. This closes 18 D13 (firewall + blanket) for the AB interface; the engine-bay firewall remains per 10:159-174.

---

## 6. Load summary & verdict

```
────────────────────────────────────────────────────
  q @ M1/10kft           48.8 kPa
  C_L 1g @ M1             0.0195
  Load factor ceiling     20g (C_L-limited) — not binding
  ── Wing box (6g ult) ──
    M_root                163.0 N·m   V_root 457 N
    Cap (5×0.2mm×50mm)    466 MPa     margin 2.6×   ✓ ≥ 2.0
    Web (1.0mm ±45°)       33 MPa     margin 2.8×   ✓
  ── Stabilator ──
    Hinge @ M1 15°        0.70 N·m    servo 1.7×    ⚠ check rotation
  ── Engine mount (I-01) ──
    4× M3                 116 N/bolt  margin >18×   ✓
  ── Thermal (AB→composite) ──
    5mm blanket           610→410 K   leak 3%       ✓
────────────────────────────────────────────────────
```

**Structural feasibility: CLOSED** with the 5-ply/7 mm box spar (upgraded from 18 §3.2's failing 2-ply/6 mm). The two open follow-ups — **rotation pitch authority** (high SM) and the **18 §3.2 spar change-notice** — are P0 before flight but do not block the current CAD/DXF baseline.
*Produced by `tools/structural_analysis.py`, pinned CadQuery env. Supersedes 10's old-geometry (200 mm × 2.2 m, S=0.11, b=1.0, Λ=60°) results.*
