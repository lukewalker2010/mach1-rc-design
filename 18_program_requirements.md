# Mach 1 RC — Program Requirements & Engineering Re-Baseline (v2.0)

**Author:** Program engineering (AI-driven design verification, 2026-08-06)
**Supersedes:** Contradictory values in 01 / 04 / 05 / 06 / 07 / 10 / 11 / 12 / 13 / 14 / 15 / 17 where noted.
**Status:** ⚠️ DESIGN NOT YET MANUFACTURABLE AS DOCUMENTED — this document is the disposition.

> **One-line verdict:** The single-P550-PRO + **afterburner** configuration is the only airframe-shape that can physically close the thrust-vs-drag gap at Mach 1 within the 25 kg MTOW cap, and it closes *only* if the airframe meets the drag budget below. As written, the package's own analyses contradict each other (thrust 180–550 N, MTOW 12.2–13.8 kg, limit load 4g–10g, wing area 0.095–0.25 m²). This document fixes the baseline and sets hard design contracts.

---

## 1. Mission Rules (from the published Measurement & Verification Protocol)

| # | Rule | Engineering translation | Where verified |
|---|------|--------------------------|----------------|
| 01 | **Break the barrier — level.** TAS > local Mach 1, sustained ≥5 continuous seconds, M0.8→M1+ flown level or climbing, no altitude loss. Dives don't count. | Net thrust > drag at M ≥ 1.05 for ≥5 s in level/climb at dash altitude. | §2 (thrust/drag), §6 (flight test) |
| 02 | **Air-breathing power.** Turbojet/turbofan/ramjet/pulsejet or combinations. No rocket, no onboard oxidizer. | JetCat P550-PRO + afterburner (reheat = allowed turbojet augmentation). | §2, docs 13–17 |
| 03 | **Land intact.** Controlled landing on designated area; fly again without replacing major components. | Belly-skid + drogue envelope must not exceed structure/skid capability; landing ≤ 30 m/s. | §5.4, doc 08 (corrected) |
| 04 | **Do it again.** Same airframe, same day, reciprocal heading; refuel + minor repairs only. | Fuel ≥ 2 sorties; AB reliability ≥ 95% lighting; engine-bay thermal limits; ~60 min turnaround. | §5.5, §6 |
| C1 | **MTOW ≤ 25 kg** (incl. fuel). | Re-baselined MTOW 13.6 kg. | §3 |
| C2 | **Fixed-wing airplane** (aerodynamic lift). | Wing planform per §3.2. | §3 |
| C3 | **Remote human pilot, continuous command + abort authority.** | FPV + 2.4 GHz RC + 900 MHz telemetry; explicit abort chain. | §5.3 |
| C4 | **Verification:** calibrated pitot-static + total air temp, sealed data loggers, GPS telemetry, reciprocal runs. | Instrumentation per §5.2; missing items are added to BOM. | §5.2 |

---

## 2. Propulsion / Drag Closure (the make-or-break)

### 2.1 The single showstopper, resolved

Every prior analysis in the repo agrees on one fact: **dry single-engine thrust cannot break Mach 1 level.** The original +7.8 N margin (01:63) is an artifact of a sub-Mach drag model. The afterburner is the swing factor. Full closure calculation:

**Engine at Mach 1.0, 10,000 ft** (from 13 Method B, corrected-flow — the physically correct model):

| Quantity | Symbol | Value | Source |
|---|---|---|---|
| Altitude density | ρ | 0.905 kg/m³ | ISA |
| Speed of sound | a | 328 m/s | 13:65 |
| Ram total pressure | Pt | 131.9 kPa (1.893 × 69.7) | 13:84 |
| Ram total temp | Tt | 322 K (1.2 × 268.3) | 13:85 |
| Corrected mass flow (94.6% N_corr) | ṁ_corr | ~0.88 kg/s | 13:94 |
| **Physical mass flow** | **ṁ** | **1.08–1.15 kg/s** | 13:96 |
| Turbine-exit temp, dry, TIT-limited | T5, dry | ~1000 K | 13:120 |
| Dry jet velocity (TIT-limited) | Vj,dry | ~566 m/s | 13:123 |
| **Net thrust, dry** | Fn,dry | **~257 N** | 13:126 |

**Afterburner (wet):** T5 raised to 1800 K by reheat → Vj scales as √T:

```
Vj,wet  = 566 × √(1800/1000)          = 759 m/s
ṁ_wet   = 1.10 kg/s (core + AB fuel 27 g/s)
Gross   = ṁ × Vj + (Pe−Pa)Ae         ≈ 835 N
Ram     = ṁ × V∞ = 1.10 × 328        ≈ 361 N
Net     = Gross − Ram                 ≈ 450–475 N   (design point 465 N)
```

> **⚠️ Critical internal inconsistency fixed here:** docs 14 and 17 use ṁ = 0.69 kg/s at Mach 1 (simple ρ-scaling, 14:15, 17:22). Doc 13 Method B correctly computes 1.08–1.15 kg/s via corrected flow. **The 0.69 value is wrong** — it ignores ram total-pressure recovery (the whole point of the supersonic intake). With ṁ = 0.69 the afterburner yields only ~300 N and the program fails. **All AB thrust/thermal calcs must be re-run at ṁ = 1.10 kg/s.** AB fuel for 1800 K then becomes ~27 g/s (not 17.7 g/s).

### 2.2 Drag budget (the design contract the airframe must meet)

Re-baselined airframe: **185 mm max OD, 2.60 m long, fineness 14:1** (longer & slimmer than the 200 mm × 2.2 m baseline — cuts body wave drag ~25%).

```
q @ M1.1, 10 kft  = 0.5 × 0.905 × (1.1×328)² = 58,900 Pa
S_front           = π × 0.0925²               = 0.0269 m²

Body wave (Sears-Haack):  C_Dw = (9π²/2)(R/L)² = 44.4×(0.0925/2.6)² = 0.056  →  89 N
Body friction (Cf 0.0024, Swet 0.85 m²):                           → 120 N
Wing (S=0.14 m², Cf 0.003, both sides):                            →  49 N
Tail (25% wing)                                                     →  12 N
Intake                                                             →  15 N
Base                                                               →   8 N
Excrescences/seams/gaps                                            →  10 N
────────────────────────────────────────────────────────────────────────────
Subsonic total @ M1.1                                              → 303 N
× Transonic factor (≈1.35 past hump)                               → ≈410 N  (M1.1)
Hump estimate @ M1.03–1.05                                          → ≈420 N
```

**Closure:**

| Condition | Drag | Wet thrust | Margin |
|---|---|---|---|
| M1.05 (hump) | ~420 N | 465 N | **+45 N (+11%)** |
| M1.10 (sustain) | ~410 N | 465 N | **+55 N (+13%)** |
| M1.20 (dive headroom) | ~455 N | 465 N | +10 N (limit) |

### 2.3 Hard contracts (non-negotiable)

1. **Net wet thrust ≥ 450 N** at M1.0/10 kft — MUST be bench-verified (doc 17 §3a, Phase 4). If the AB delivers only 400 N, the program cannot sustain M1.05 and must stop.
2. **Drag budget: hump drag ≤ 430 N** ⇒ requires (a) 185 mm body, (b) 2.6 m length, (c) CNC seamless skins, (d) gap-free LE/TE. A 200 mm × 2.2 m airframe (as documented) raises hump drag to ~480 N and **does not close**.
3. **Dash window: 10,000–12,000 ft.** T–D margin is altitude-invariant to first order (thrust ∝ ρ, drag ∝ ρ), but colder air at altitude preserves turbine-inlet-temperature margin. AB O₂ support is adequate to 15 kft (17:566).
4. **Sustain at M ≈ 1.10**, not "touch M1.0." The rule requires ≥5 s *above* Mach 1; 01:105's 9.3 s was computed on the bogus +7.8 N model.

---

## 3. Airframe Re-Baseline (corrected geometry)

### 3.1 Fuselage

| Parameter | Baseline (01/05) | **Re-baseline** | Reason |
|---|---|---|---|
| Length | 2.20 m | **2.60 m** | fineness 14:1 cuts wave drag ~25% (Sears-Haack) |
| Max OD | 200 mm | **185 mm** | S_front 0.0314→0.0269 m² (−14% drag); engine 175 mm + mount fits |
| Engine mount station | 1.40–1.60 m | **1.20 m** | CG closure (§4), shorter intake duct |
| Tailcone | 35 mm OD @ 2.20 | opens into AB + C-D nozzle | the 49 mm nozzle cannot be inside a 35 mm neck (05:120 vs 02:48) — tailcone is replaced by the AB duct + nozzle fairing |
| Nose | ogive per 05:25 | **R(x)=0.0925·sin(πx/0.85)** | re-derive mould table from this equation (05 vs fuselage_manufacturing/01 mismatch, see §7) |
| Area-ruled waist | 178 mm @ x=1.00 | **~172 mm @ x=1.05** | re-pinch at wing/engine junction |

### 3.2 Wing (F-104-style thin, internally consistent planform)

The documented planform (S=0.095, b=0.9, Λ=14.6°, c_r=0.211) is **numerically impossible** (geometry gives c_r = 1.73 m). Re-baseline:

| Parameter | Value | 
|---|---|
| Span b | 0.95 m |
| Area S | 0.14 m² |
| Taper λ | 0.40 |
| Root chord c_r | 0.210 m (`2S/(b(1+λ))`) |
| Tip chord c_t | 0.084 m |
| LE sweep Λ | 30° (subsonic LE to M 1.15; F-104-proven thin-wing approach) |
| Airfoil | biconvex 4% t/c (root thickness 8.4 mm — fits a box spar) |
| MAC | 0.156 m |
| Wing loading @ 13.6 kg | 97 kg/m² |
| Re @ M1/10 kft | ~3×10⁶ |

**Structure (replaces the unbuildable 04 spar):** a single rod on the airfoil midplane is on the bending neutral axis and carries no load (04's own math: 862→8150→2208 MPa contradiction). Use a **box spar**:
- Upper/lower caps: 2 plies × 0.2 mm T300 UD at 6 mm separation near 30% chord
- Shear web: ±45° 0.5 mm + 3 mm Rohacell
- Root bending moment at 9g: ~100 N·m (recomputed at 13.6 kg) → cap stress ~700 MPa, ~2× margin vs T300
- Ribs: real core-offset DXFs (see §7) — every `wing_rib_R*.dxf` currently carries only the outer contour, no web/flange.

### 3.3 Stabilator (currently geometrically impossible)

The documented 2 mm spar + 8 mm hinge bearings inside a 1.225 mm-thick airfoil cannot exist (06:19-20, 204, 310, 347-375). Fix:
- Increase section to **6% t/c** (root chord 90 mm → 5.4 mm thick), OR
- Move the hinge to an **external clevis** and make the stabilator a full-depth titanium-alloy laminated control surface with a 2.5 mm Ti spar at max thickness.
- Regenerate STA_MID (currently 5% too thick; `STA_MID.dxf` is root scaled inconsistently in x/y).
- Reconcile the airfoil table vs DXF (06:146-160 vs STA_ROOT disagree 2.5×).

### 3.4 Mass budget (MTOW 13.6 kg, closes CG)

| Component | Mass (kg) | Station (m) | Moment (kg·m) |
|---|---|---|---|
| P550-PRO engine | 4.90 | 1.20 | 5.880 |
| Afterburner (17 revised) | 0.83 | 1.48 | 1.228 |
| Wing + carry-through | 0.50 | 1.00 | 0.500 |
| Stabilator + hardware | 0.10 | 2.35 | 0.235 |
| Ventral fin | 0.10 | 2.30 | 0.230 |
| Fuselage structure | 2.50 | 1.30 | 3.250 |
| Fuel (2.0 L Jet A1) | 1.62 | 0.45 | 0.729 |
| Fuel system | 0.50 | 0.60 | 0.300 |
| Avionics + battery + FPV + M&V | 0.90 | 0.25 | 0.225 |
| Landing/dolly hardpoints | 0.35 | 0.80 | 0.280 |
| Nose ballast (tungsten) | 1.00 | 0.10 | 0.100 |
| Miscellaneous | 0.30 | 1.00 | 0.300 |
| **Total** | **13.60** | | **13.257** |

**CG = 0.975 m.** With MAC 0.156 m and wing 30% MAC at x ≈ 1.0 m, neutral point ≈ 1.00 m → **static margin ≈ 16% MAC** — stable, no FBW dependence. Ballast reduced from 5.8–11.2 kg (07:223, 17:474) to **1.0 kg** via the engine-forward re-layout. (Verify: 13.257/13.60 = 0.975 ✓; fuel-burn excursion ~ +0.03 m aft, still ≥12% MAC at empty.)

---

## 4. Interface Control (who owns what boundary)

See `INTERFACES.md`. The five subsystem ownership boundaries:

| Subsystem | Engineer owner | Interfaces owned | Key mating dimensions |
|---|---|---|---|
| **A. Airframe** (wing/fuse/stab) | E1 | fuselage stations 0–2.60 m; wing carry-through 0.95–1.15 m; stabilator 2.30–2.45 m | Engine mount ring @ 1.20 m; AB duct fairing 1.39–1.80 m |
| **B. Propulsion + afterburner** | E2 | P550 mount @ 1.20 m; intake duct 0.30–1.20 m; AB 1.39–1.80 m | ṁ model (1.10 kg/s); wet thrust ≥ 450 N |
| **C. Systems** (fuel/avionics/M&V) | E3 | fuel tank 0.35–0.60 m; avionics bay 0.10–0.30 m | fuel flow ≥ 40 g/s AB; TAT + sealed loggers |
| **D. Launch & recovery** | E4 | dolly, skid, drogue | landing ≤ 30 m/s; dolly abort braking |
| **E. Manufacturing & QC** | E5 | all STEP/DXF/mould data; tooling; tolerances | CNC mould surfaces; DMLS Inconel prints |

---

## 5. Verification & Instrumentation (M&V protocol compliance)

### 5.1 Measurement chain (required by protocol)
- **Airspeed/Mach:** calibrated pitot-static (Eagle Tree + MS4525DO) **plus total air temperature (TAT) probe** — Mach from `M = √(5·((Pt/P)²/⁷ − 1))` with total-temp cross-check. **TAT is currently missing from the design** → add Rosenount-style TAT probe (Aspen/OpenCanopy or equivalent), calibrated on a bench vs known TAS.
- **Speed certification:** GPS at ≥10 Hz with Doppler-velocity logging (u-blox M8P `NAV-PVT`), dual-redundant loggers: Cube blackbox SD + independent sealed logger (e.g., two independent OpenLog/byteflight devices with write-once SD, sealed after each flight). Barometric + GPS cross-check; log at ≥50 Hz during the dash window.
- **Altitude-loss check (rule 01):** barometric altitude from the sealed logger at 50 Hz — must be monotonic non-decreasing through the M0.8→M1+ window.
- **Reciprocal runs:** two sorties, opposite headings (≤60 min apart), same day. Report both; the protocol uses the reciprocal pair.

### 5.2 Instruments to add to BOM (not in 09)
| Item | Est. cost |
|---|---|
| TAT probe + interface | $40 |
| 2× sealed SD data loggers | $60 |
| FPV VTX + camera + ground goggles | $150 |
| 1.0 kg tungsten nose ballast | $300 |
| Dedicated AB fuel pump (Speck ZY-4S — see §7) | $80 |
| Iris servo + drogue door servo + CDI pack + 10 A BEC/12 V boost | $120 |

### 5.3 Pilot & control
- **FPV mandatory** (13:191 — visual control impossible at Mach 1). Add FPV VTX 5.8 GHz.
- RC: 2.4 GHz FASSTest for command; 900 MHz RFD900x for telemetry/abort relay; **range verification >4 km** (not the current 100 m walk, 09:178).
- **Abort authority:** pilot command closes AB fuel valve + opens iris to dry + throttle to idle in <0.5 s (17:616); independent of the AB state machine.

### 5.4 Landing & recovery (rule 03)
- **Correct the landing-speed contradiction** (01:16 75 m/s vs 08:180 15 m/s vs 08:155 30 m/s). Design case: **approach 38 m/s, flare to ≤ 30 m/s**, drogue 0.6 m ribbon deploys subsonic ≤ M0.6 (gated on TAS, not just throttle+alt — fix 08:368), skid stop ≤ 60 m. Structure sized to 3g vertical at 30 m/s.
- Drogue hardpoint: add doubler/insert at BH8 (1 mm carbon cannot take the 1 kN opening load).

### 5.5 Same-day reuse (rule 04)
- Fuel: 2.0 L (1.62 kg) — two × 5 s AB dashes + climb/accel for both sorties ≈ 1.55 kg (17:643 corrected to ṁ 1.10 → ~370 ml per 5 s AB burst). Margin ~1 L after two sorties.
- Engine-bay thermal: add firewall + ceramic blanket per 10:159-174 (currently absent in 05 — see §7).
- AB liner: consumable per 17:237, inspect via boroscope between sorties; 5 min cooldown between AB runs (17:568).
- Turnaround checklist (build from 09:273 + AB post-flight inspection 17:645).

---

## 6. Flight Test Plan (envelope expansion to the record)

| Phase | What | Gate to pass before next |
|---|---|---|
| G0 | Bench: AB cold-flow, fuel spray, ignition, 20 s wet runs ×3 (17 §3a) | wet thrust ≥ 450 N; shell < 200 °C |
| G1 | Ground: full-power runs, AB cycling on test stand, CG/weigh-off at both fuel loads | CG 0.975 m ±20 mm both fuel loads |
| G2 | Dolly launch aborts: 30→50 m/s, braking + aborts verified | no excursion, all aborts stop < roll+150 m |
| G3 | Envelope: M0.5→0.8 dives/level at 8 kft; flutter checkpoints | stable, no oscillation |
| G4 | Transonic probes: M0.85, 0.92, 0.97 level at 10–12 kft (dry) | M0.97 level sustained ≥ 3 s |
| G5 | **First M1.0+ dash (wet), 5 s sustain** | TAT/Mach log confirms M > 1.0 for 5 s, no altitude loss |
| G6 | **Reciprocal second sortie, same day** | full protocol pass, only minor repairs |
| G7 | Sustained M1.05–1.10 × 2 sorties | record verified |

---

## 7. Audit Dispositions (every material finding from the 2026-08-06 audit)

Priority P0 = must fix before build, P1 = fix before flight, P2 = correct in docs.

| # | Finding (source) | Fix | Pri |
|---|---|---|---|
| D1 | Wing spar unbuildable: rod on neutral axis, rods > rib thicknesses, 3 contradictory locations (04:76-112, 03:168/219, 02:90) | Box spar per §3.2; rib holes ≥ spar; single assembly sequence defined | P0 |
| D2 | Stabilator impossible geometry (06:204/310/347-375) | 6% t/c or external-clevis Ti stabilator §3.3; regen STA_MID | P0 |
| D3 | Fuselage mould data ≠ design: nose ogive, waist pinch off-station, boat-tail table wrong (fuselage_manufacturing/01 vs 05) | Re-derive all mould tables from 05 + §3.1 equations; regenerate | P0 |
| D4 | Structural/aero analyses (10, 12) on different aircraft (S=0.11, b=1.0, Λ=60°) than build (S=0.14, b=0.95, Λ=30°) | Re-run 10 & 12 on the re-baselined geometry | P0 |
| D5 | T–D margin +7.8 N bogus (01:63) | Replace with §2 closure; wet-thrust is the gating metric | P0 |
| D6 | Mass/CG contradictions: MTOW 12.2–13.8, wing 0.2–1.2 kg, stab 55 g–0.3 kg, load factors 4g–15g | Use §3.4 mass/CG table as the single source of truth | P0 |
| D7 | CG unstable; 5.8–11.2 kg ballast (07:223, 17:474) | Engine-forward layout §3.4 → 1.0 kg ballast, SM 16% MAC | P0 |
| D8 | AB fuel pump contradiction: 17:436 taps engine pump (max 27.5 g/s, 13:160) — physically impossible for AB | **Dedicated Speck ZY-4S-12V** (15:93) supplies AB; 17's "eliminate pump" is void | P0 |
| D9 | ṁ = 0.69 kg/s in 14/17 vs 1.10 in 13 | Re-run all AB thermal/thrust at ṁ 1.10; AB fuel 27 g/s | P0 |
| D10 | No TAT, no sealed loggers, no FPV; BVR piloting unverified (M&V fail) | §5.2 items added; range test >4 km | P0 |
| D11 | Landing speed 15–75 m/s contradiction; drogue not achieving its design speed; supersonic deploy risk (08) | §5.4 envelope; TAS-gated deployment | P0 |
| D12 | Dolly abort: no braking/chute during launch roll (08:60) | Add dolly brakes + pull-pin cable abort | P0 |
| D13 | No engine-bay firewall/insulation though 10:159-174 requires it (05) | Metal firewall BH6 + ceramic blanket + metal tailpipe | P0 |
| D14 | Wing DXF/CSV/md mismatches (81 vs 21 points; missing core-offset webs/flanges; 01:21, 01:235-239) | Regenerate net-part DXFs | P1 |
| D15 | Mould draft: 2.2 m zero-draft female mould (05:599, 02:189) | Add 0.5–1° draft or split fore/aft | P1 |
| D16 | Cure-pressure contradiction: 6 bar autoclave (03:27) vs −0.9 bar vacuum (02:189) | Commit to one: 3 bar autoclave wing, or wet-layup with Vf knockdown | P1 |
| D17 | BH1 thickness 1.0 vs 0.8 mm; M5 tapped into 1 mm carbon vs nut-plates (05 vs manuf) | Nut-plates everywhere; reconcile thickness | P1 |
| D18 | Wing planform numerically impossible (S/b/Λ/c_r inconsistent) | §3.2 planform is authoritative | P1 |
| D19 | BOM missing: AB system, ballast, TAT/loggers/FPV, iris/drogue servos, CDI pack, BEC (09) | Add per §5.2 + 15:652 + 16:1119 | P1 |
| D20 | Fuel: tank 1.2/1.5/2.0 L contradiction; bladder vent undersized for AB flow | 2.0 L bladder, vent sized for 83 ml/s, fuel return line per JetCat install | P1 |
| D21 | Wing mass over-estimated 3× (04:320 double-counts planform) | Use §3.4 masses | P2 |
| D22 | Stabilator t(z) interpolation wrong (stabilator_manufacturing/01:62-67) | Fix formula; regen mould stations | P2 |
| D23 | 09 cost math errors ($174 vs $214 etc.) | Re-sum; program cost ~$9,500 | P2 |
| D24 | Dead/broken BOM links (Eagle Tree dead, Futaba R7018SB risk) | Re-verify purchases; list alternates | P2 |

---

## 8. Next actions (owners)

| Action | Owner | Deliverable |
|---|---|---|
| Re-run aero/structural (10, 12) on §3 geometry | E1 + AI | updated 10/12 |
| AB bench build + wet-thrust validation ≥450 N | E2 | test report |
| Re-generate mould/rib/DXF data from corrected equations | E5 | net-part DXF + mould STEP |
| Update BOM + add §5.2/§7 items | E3 | BOM v2 |
| Build & integrate per G0–G7 test plan | all | flight test log |

*This document, `INTERFACES.md`, and `AGENTS.md` form the coordination contract for the 5-engineer + AI team. All future changes must be reviewed against this baseline via PR.*
