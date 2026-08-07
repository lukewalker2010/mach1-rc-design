# Mach 1 RC — Systems & Measurement/Verification Design (v2)

**Author:** E3 (Systems/M&V), 2026-08-06
**Reconciles:** `07_systems_layout.md` (power §3.4, wiring §5), `15_afterburner_fuel_ignition.md` (power App. B), `16_afterburner_electronics.md` (power Task 2, safety Task 7) into **one** plan. Where the three conflict, the decision below states which document wins and why.
**Interface compliance:** I-06, I-07, I-08, I-12 values are unchanged. Numbers computed in `tools/bom_v2_check.py` and cited below.

---

## 1. M&V instrument chain (protocol rule C4 / 18 §5.1)

| Instrument | Spec | Mount / Interface | Source |
|---|---|---|---|
| **TAT probe** | Rosenount-style total-air-temp element (RTD or T/C), ±0.5 K, de-ice-tolerant immersion type | **x = 0.08 m** nose (I-07), shielded from solar radiation, aspirated or flush-immersion; sample stagnation stream off the pitot cone | 18 §5.1, I-07 |
| **Pitot-static** | Prandtl probe at **x = 0.05 m** (I-07); static ports flush on fuselage sides at x = 0.40 m, port+starboard manifolded (07 §3.1) | MS4525DO differential ±1 kPa, 0–±3447 Pa range, I²C | replaces **dead Eagle Tree link** (bom_link_check_report #24); new probe in BOM v2 S5 |
| **GPS** | u-blox M8P, **NAV-PVT ≥ 10 Hz**, Doppler-velocity (speed from PVT `vN/vE/vD`), HDOP < 1.0, ≥10 sats | Here+ antenna dorsal at x = 0.15 m (07 §3.1) | 18 §5.1 |
| **Sealed loggers ×2 (independent)** | Write-once SD; log ≥ **50 Hz** during the dash window; Cube blackbox SD = logger #1, sealed OpenLog/byteflight = logger #2 | logger cavity in avionics bay (I-07); both record baro, Pt/P, TAT, GPS, 1 Hz AB status | 18 §5.1 |
| **Barometric altitude** | from sealed logger #2 (≥50 Hz) — the **level-flight rule** evidence | avionics bay static port | 18 §5.1 |

**Sealing procedure (each flight, per 18 §5.1):** power up → sync both loggers to GPS time → verify both log the same test-ID → SD card latched, write-enabled, **mechanical seal** over the slot (tape + cover) → ground roll boot stamp → do not open until after landing → compare file hashes of both logs post-flight; a single-image (identical sample count, matching timestamps) cross-check is the certification record.

## 2. Mach computation & the "no altitude loss" evidence

**Mach from pitot-static** (18 §5.1 formula):

```
M = √( 5·((Pt/P)^(2/7) − 1) )        (γ = 1.4, (γ−1)/γ = 2/7)
```

- Pt/P from the MS4525DO (differential qc) + baro static P.
- **TAT cross-check:** `T = TAT / (1 + 0.2·M²)`, `a = √(1.4·287·T)`, `TAS = M·a`.
  At M1.0/10 kft: T = 268.3 K, a = 328 m/s, predicted TAT = 268.3·1.2 = **322 K** (13:65, 13:85). If `TAT_measured − TAT(M_pitot)` exceeds ±2 K for >1 s in the window, flag the sample and re-derive M from TAT + static P (consistency gate before the record is accepted).
- **Sustained window (rule 01):** log at ≥50 Hz over M0.8 → M1+; the M > 1.0 condition must hold ≥5 continuous seconds.
- **No-altitude-loss evidence (rule 01):** barometric altitude from sealed logger #2 must be **monotonic non-decreasing** across the M0.8→M1+ window (allowing ≤ +3 m sensor noise/overshoot, no negative step). A negative step > 5 m or a dive signature (baro-alt drop + TAS rise while climbing) invalidates the run.

## 3. Calibration plan (18 §5.1 "calibrated …")

1. **Pitot-static bench:** MS4525DO zero (both ports equal) and span (3-point against a water-column / calibrated manometer); probe alignment vs flow in a small wind tunnel or instrumented moving-vehicle run to 100 m/s; report the K-factor that matches the qc → TAS at ISA.
2. **TAT bench:** element resistance/temperature curve verified 250–330 K; then dynamic check — place the probe in the same moving-vehicle run as the pitot and confirm `TAT_meas = T_amb(1+0.2M²)` to ±0.5 K at M ≈ 0.1–0.3; the fitted recovery factor is stored in the logger configuration.
3. **GPS:** survey a 1 km baseline with the launch cart/dolly; drive at 20, 40, 60 m/s and confirm M8P PVT speed vs wheel speed ±0.1 m/s; confirm ≥10 Hz output persists with HDOP < 1.0.
4. **Logger pair:** same test-ID stamping, file-hash match, and sample-count identity checked on the bench before every flight day.
5. **Reciprocal runs (rule 04):** two sorties, opposite headings, ≤60 min apart, same day; the protocol uses the pair (18 §5.1/§6 G5–G6). Both logs + ECU + AB telemetry archived per sortie.

---

## 4. ONE power architecture (resolves the 07/15/16 conflict)

**Decision:** **2S 5000 mAh main pack.** Direct **7.4 V** rail → KST X20-12T servos + JetCat ECU. **5 V CC BEC 10 A** → FC, receiver, telemetry, loggers, FPV, TAT, Pico. **Pololu D24V50F12 (12 V, 2.5 A)** boost → Speck ZY-4S-12V pump ESC + AB solenoid. **Dedicated isolated 2S 500 mAh** pack → CDI.

| Conflict | 07 | 15 | 16 | **v2 winner** | Why |
|---|---|---|---|---|---|
| Main pack | 2S 5000 | 3S 2200 | 2S 5000 | **2S 5000 mAh (07/16)** | KST X20-12T and JetCat ECU are **≤8.4 V** parts; 3S forces a large BEC on the servo bus and extra mass. 15's 3S was a shortcut for 12 V and is rejected |
| Servo/ECU feed | direct 2S, no BEC | 5 V BEC → ECU | direct 7.4 V | **direct 7.4 V (07/16)** | ECU accepts 6–8.4 V; higher V = better pump head. 15's "5 V BEC → ECU" rejected |
| 5 V logic rail | none | — | CC BEC 10 A | **5 V BEC (16)** | FC (5 V), Rx, RFD900x, loggers, FPV, TAT are 5 V parts; BEC also isolates Rx from servo-bus noise. 07's "no BEC" rejected |
| 12 V AB rail | — | 3S direct 12 V | Pololu U3V40A12 (1.5 A) | **Pololu D24V50F12 2.5 A (16 concept, corrected)** | Speck ZY-4S-12V needs **1.5 A @ op / 1.8 A max** (15:93) — U3V40A12's 1.5 A max is undersized. New unit in BOM v2 S20 |
| CDI power | — | dedicated 2S 500 mAh | 12 V rail | **dedicated 2S pack (15)** | RCEXL G306 input is **3.0–8.4 V** (15:334); 12 V exceeds spec **and** couples ignition noise into flight electronics. Isolation is required for M&V data integrity |
| AB pump drive | — | ZY-4S via ESC | BLDC 7.4 V pump | **Speck ZY-4S-12V via 30 A ESC on 12 V rail (18 D8 + 15)** | 18 D8 voids the engine-pump tap; 16's 7.4 V BLDC pump is not the ZY-4S |

## 5. Current budget & battery sizing (23 §4)

| Load | Rail | Current | Source |
|---|---|---|---|
| KST X20-12T ×2 (stall) | 7.4 V | 2 A each → 4 A peak / 0.5 A cruise | servo spec, HV 12 kg·cm |
| JetCat ECU + internal pump | 7.4 V | 2 A peak / 1.5 A | 07 §3.4 |
| Speck ZY-4S-12V pump | 12 V | 1.5 A op (6 bar/34 g/s) / 1.8 A max | 15:93 |
| AB solenoid valve | 12 V | 0.5 A | 16:352 |
| CDI RCEXL G306 | 2S pack | 0.5 A firing | 15:337 |
| FPV VTX + camera | 5 V | 0.5 A | spec |
| RFD900x | 5 V | 0.3 A | spec |
| Cube Orange+ | 5 V | 0.4 A | spec |
| Rx R7018SB | 5 V | 0.2 A | spec |
| Sealed loggers ×2 | 5 V | 0.2 A | spec |
| TAT + Pico + sensors | 5 V / 3.3 V | 0.1 A | spec |
| **5 V rail total** | | **1.7 A** | < CC BEC 3 A continuous |

**Sortie budget (5 min flight + 2 × 20 s AB dashes):**
- Flight average on the 2S: 3.8 A (servo 0.5 + ECU 1.5 + 5 V rail ~1.1 after BEC losses + Pico/sensors 0.1 + FPV/TAT ~0.6). **0.32 Ah** over 5 min.
- AB dash: pump 1.5 A @ 12 V = 18 W → ~2.9 A on the 2S; + solenoid ~1 A → **3.8 A for 2×20 s = 0.04 Ah**.
- **Total ≈ 0.36 Ah of 5.0 Ah (7.2%)** — 2S 5000 mAh has ~14× margin; worst-case peak draw 9.8 A vs 150 A burst. Pack size is driven by the 18 §3.4 CG table (0.30 kg class), not energy. CDI pack 500 mAh comfortably covers 2 dashes.
- 12 V boost loads: 1.5 + 0.5 = 2.0 A < 2.5 A D24V50F12 rating ✓.

---

## 6. Fuel system v2 (18 §7 D20; I-06 unchanged)

**Layout (I-06):** 2.0 L bladder at stations **0.35–0.60 m**, fuel dot + vent on top, AB tap to rear; dedicated AB feed per **I-12** (Viton 4 mm ID, rear run in the 52.5 mm annulus).

**Vent sizing — makeup air for 83 ml/s** (combined engine 22 g/s + AB max 45 g/s ≈ 67 g/s ≈ **83 ml/s**; 15 App. A). Air enters the bladder at the fuel volume flow:

```
ΔP = ½ρ(V/Cd)² ,  V = Q/A ,  A = π/4·d²      (ρ = 1.225 kg/m³, Cd = 0.6 short tube)
```

| Pressure-drop budget | Required vent ID |
|---|---|
| 100 Pa | 3.71 mm |
| 50 Pa | 4.42 mm |
| **25 Pa (chosen, low-ΔP = no bladder collapse / no vapor lock)** | **5.25 mm** |

- **Result: 5 mm ID vent line** (BOM v2 S24). At 5 mm ID the flow is 4.2 m/s with only **30 Pa** drop.
- The old **2 mm ID** vent (07 §2.5) at 83 ml/s runs at **26 m/s, ~1.2 kPa** — it would pull the bladder to partial vacuum (collapse risk, vapor-lock risk, and cannot keep up on back-to-back AB dashes). Confirms D20.
- Vent route: top of bladder → check valve (anti-siphon) → overboard at the bottom of the fuselage; keep the vent clear of the intake flow (no ram suction on the tank).

**Feed & return:**
- **Main engine feed:** clunk + felt filter (50–100 µm) at the lowest point → Viton 4 mm ID → Dubro #601 filter → P550 internal pump (ECU-regulated, 2–5 bar). **Return line** (Viton 4 mm ID) back to the bladder per JetCat install practice — keeps the fuel cool, self-bleeds the line, and eliminates air locks on priming. 18 D20 explicitly requires it.
- **AB feed (dedicated):** separate pickup/tee at the tank → Dubro #601 → **Speck ZY-4S-12V at the rear** (near the AB, short suction head) → main check valve (McMaster 4723T78) → EV14 injector → 6× Beswick check valves → spray ring. Powered by the 12 V rail (23 §4).
- **Anti-vapor-lock notes:** Jet A1 vapor pressure is low (~0.2 kPa @ 20 °C) but keep (a) the 5 mm vent at low ΔP, (b) suction heads short and flooded (pump below tank outlet, clunk at the bottom), (c) lines ≥ 20 mm bend radius (15 §5), (d) a vented bladder so no negative pressure builds during the 83 ml/s peak draw, and (e) heat-shield the AB feed where it crosses the engine bay (heat-shrink secondary containment, 15 §5).
- **Fill/dot:** 6 mm Dubro HD-175 top fill at the tank; drain at the lowest line point (07 §2.5). **Filter:** felt clunk + 50 µm inline on both main and AB branches (15 §5).

## 7. CG check (18 §3.4 mass table)

Computed in `tools/bom_v2_check.py` from the 18 §3.4 table (MTOW 13.60 kg, Σmoment 13.257 kg·m):

| Fuel state | Mass (kg) | Moment (kg·m) | CG (m) | Static margin @ NP = 1.00 m (MAC 0.156 m) |
|---|---|---|---|---|
| **Full (2.0 L)** | 13.60 | 13.257 | **0.975 m ✓** | **+16.1 % MAC ✓** (matches 18: "≈16 %") |
| **Empty** | 11.98 | 12.528 | **1.046 m** | **−29.3 % MAC ✗** |
| Excursion (full→empty) | | | **+0.071 m aft** | |

**Finding — must be flagged:** 18 §3.4 states "fuel-burn excursion ~ +0.03 m aft, still ≥12 % MAC at empty". The mass table's **own numbers give +0.071 m**, and with the declared NP ≈ 1.00 m the empty-aircraft static margin is **−29 % MAC (unstable)**. The two ends of the CG band **cannot both** be met by the current layout: fuel at 0.45 m (I-06, fixed) is 0.52 m forward of CG, so burning it drives CG aft by ~4.5 % MAC per… **0.071 m / 0.156 m = 45 % MAC total**.

**Required for ≥12 % MAC at empty:** NP ≥ **1.065 m** (CG_empty + 0.12·MAC). The tail-volume estimate (stabilator at 2.35 m, S_h ≈ 0.006 m²) places NP ≈ 1.046 m — i.e. exactly marginal. **Actions (no interface changes; P0-flagged):**
1. **G1 gate (18 §6):** weigh-off at **both** fuel loads must verify CG 0.975 ±20 mm. If it doesn't, stop.
2. **Verify NP ≥ 1.065 m** from the re-run 10/12 on the re-baselined geometry (18 §7 D4). If short, the remedy is a cross-team **P0 interface proposal** (e.g., stabilator area/arm, or an aft-fuselage trim mass) — NOT a unilateral change to I-06.
3. Reserve nose-ballast strategy: adding ~7 kg nose ballast would re-close the empty end but pushes the full CG below the ±20 mm band — **not** the first choice; treat as fallback only.
4. In the meantime the **flight-test envelope (G2→G4) is flown dry** so the empty condition is approached gradually; first wet dash (G5) requires both-load weigh-off sign-off.

## 8. Wiring / routing summary & abort authority

**Routing (07 §5, kept):** power wires starboard, signal wires port, ≥20 mm separation, braided nylon conduit 10 mm, single-point star ground at the PDB, 14 AWG power / 20 AWG servo / 22 AWG signal / 26 AWG sensor.

| Link | Frequency / path | Notes |
|---|---|---|
| RC command | 2.4 GHz FASSTest, R7018SB | antennas 90° orthogonal (07 §3.3) |
| Telemetry | 900 MHz RFD900x, dorsal whip | MAVLink; AB_STATUS (ID 200) forwarded (16 Task 8) |
| FPV | 5.8 GHz VTX + camera | mandatory visual (18 §5.3) |
| AB control | Pico reads Rx **CH5 (AB arm/fire)** + **CH3 (throttle)**; drives pump ESC, solenoid, CDI, iris (16 Task 5) | MAVLink UART to Cube |
| M&V | sealed loggers (50 Hz) + GPS 10 Hz + TAT + pitot | independent of the control chain |

**Abort authority chain (18 §5.3):** pilot command → Rx CH5 → Pico **hard abort input (wired, independent of the state machine)** → in **<0.5 s**: close AB solenoid, pump → 0, **iris open to dry**, throttle → idle (17:616). Also the AB controller aborts on: EGT > 1050 °C (1100 °C hard), flameout > 500 ms, pump current > 4 A, fuel pressure out of 0.5–10 bar, RPM < 40 %, RSSI < 40 % (16 Task 7).

**Failsafe (16 Task 7):** RC signal loss > 500 ms → hold current state 1 s → safe shutdown: AB off (solenoid closed, pump 0), iris to dry/open, engine throttle to idle; watchdog reset on the Pico forces GPIOs low (pump off, valve closed, no spark).

## 9. Top-5 program risks (18 audit) & mitigations now in place

| # | Risk | Mitigation now in place |
|---|---|---|
| 1 | **Wet thrust < 450 N** (18 §2/§7 D5, D9) — program can't sustain M1 | Bench gate **G0**: 20 s wet runs ×3, wet ≥450 N; dedicated **Speck ZY-4S-12V** (D8) + 12 V boost sized 2.5 A; AB fuel 27 g/s @ 1800 K; EGT closed-loop (16) |
| 2 | **CG excursion at empty fuel** — **new finding** (23 §7): empty CG 1.046 m, needs NP ≥ 1.065 m | Flagged P0; NP verification on re-run 10/12 (D4); **G1 weigh-off at both fuel loads** is a hard gate; dry envelope flown before first wet dash |
| 3 | **M&V certification data integrity** (D10) — record could be rejected | TAT + pitot-static + **≥10 Hz M8P Doppler** + **2× independent sealed 50 Hz loggers** + baro monotonicity evidence; reciprocal runs; file-hash cross-check |
| 4 | **Drogue / landing envelope** (D11): 15–75 m/s contradiction, supersonic deploy risk | TAS-gated deploy ≤ M0.6, 0.6 m ribbon, approach 38 m/s → flare ≤30 m/s, skid ≤60 m, BH8 doubler/insert for 1 kN opening load (18 §5.4) |
| 5 | **Single-source critical-path supply** (D24): JetCat P550, KST X20-12T, Speck ZY-4S, Xometry Inconel, custom bladder/drogue, R7018SB | BOM v2 §8 order-first list with alternates; dead Eagle Tree link replaced; long-lead items flagged ★ and ordered before build |

---

## 10. Numbers owned — sources

| Number | Value | Source / formula |
|---|---|---|
| BOM v2 total | $9,662 (107 lines) | `tools/bom_v2_check.py` |
| Vent diameter | **5 mm ID** (2 mm was 1.2 kPa, 26 m/s) | ΔP = ½ρ(V/Cd)², Q = 83 ml/s |
| CG full / empty | 0.975 / 1.046 m | 18 §3.4 table |
| Fuel-burn excursion | +0.071 m aft | 18 §3.4 table |
| Static margin full / empty | +16.1 % / −29.3 % MAC @ NP 1.00 m | MAC 0.156 m (18 §3.2) |
| NP needed for ≥12 % MAC empty | ≥ 1.065 m | CG_empty + 0.12·MAC |
| Mach formula | M = √(5·((Pt/P)^(2/7)−1)) | 18 §5.1 |
| TAT @ M1/10 kft | 322 K | 13:85 |
| Sortie energy | 0.36 Ah / 5 Ah (7.2 %) | 23 §5 |
| 12 V peak | 2.0 A (pump 1.5 + solenoid 0.5) | 15:93, 16:352 |
