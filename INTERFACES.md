# INTERFACES.md — Subsystem Interface Control (Mach 1 RC)

**Authority:** `18_program_requirements.md` §4. Any change to a value below is a **P0 change** and requires a cross-team review (owning engineer + affected interface owners) before merge. One coordinate system everywhere: origin = nose tip, +X aft, +Z up. Units mm (CAD) / m, kg, N, K (analysis).

---

## 1. Interface inventory

| Ifc | Boundary | Mating owner → Owner | Key dimensions (must not change unilaterally) |
|---|---|---|---|
| I-01 | **Engine mount ring** → fuselage BH6 | Propulsion (E2) → Airframe (E1) | Ring at station **1200 mm**, P550 flange bolt circle 4× M3 / 45 mm PCD; thrust load path to BH6/BH7 nut-plates |
| I-02 | **Intake duct** nose → engine | Airframe (E1) → Propulsion (E2) | Throat Ø103 mm at 300–600 mm; lip Ø105 mm at 50–150 mm; duct FSA = engine inlet FSA ±5% |
| I-03 | **Afterburner mount** → engine exhaust flange | Propulsion (E2) → Propulsion (E2) | 4× M3 / 45 mm PCD at station ~1390 mm; AB total length 385 mm, Ø90 mm shell; wet thrust ≥450 N reaction into fuselage via strut to BH8 |
| I-04 | **Wing carry-through** → fuselage | Airframe (E1) → Airframe (E1) | Box 200×100 mm at stations 950–1150 mm; 4× M6 on 60 mm grid into insert plates |
| I-05 | **Stabilator hinge** → tailcone | Airframe (E1) → Airframe (E1) | Hinge axis at station ~2350 mm, both stabilators; 2× KST X20-12T, ±15° pitch / ±10° roll |
| I-06 | **Fuel tank** → fuselage + systems | Systems (E3) → Airframe (E1) | 2.0 L bladder at stations 350–600 mm; fuel dot + vent on top; AB tap line to rear |
| I-07 | **Avionics bay** → nose | Systems (E3) → Airframe (E1) | Stations 100–300 mm; TAT probe at 80 mm; pitot boom at 50 mm; sealed logger cavity |
| I-08 | **M&V data chain** | Systems (E3) owns | TAT + pitot-static + GPS ≥10 Hz + 2× sealed loggers @50 Hz; calibrated per 18 §5.1 |
| I-09 | **Dolly hardpoints** → belly | Launch/Recovery (E4) → Airframe (E1) | 4× latch points at stations 600/900 mm, 150 mm apart laterally; 4.5g launch load |
| I-10 | **Belly skid** → tailcone bottom | Launch/Recovery (E4) → Airframe (E1) | Stations 1900–2150 mm; UHMWPE strip, 5 mm; 3g landing load |
| I-11 | **Drogue door** → tailcone | Launch/Recovery (E4) → Airframe (E1) | Door at station 2500 mm; 0.6 m ribbon chute; deploy gate M ≤ 0.6 & h < 20 m |
| I-12 | **AB utilities** → annulus | Propulsion (E2) → Systems (E3) | Fuel line (Viton 4 mm ID), cooling air duct Ø15 mm, ignition coax, iris pushrod (Ti 2 mm in PTFE), 3× thermocouples — routed in 52.5 mm annulus per 17 §2b |

---

## 2. Thrust & mass flow contracts (propulsion, per 18 §2)

| Quantity | Value | Note |
|---|---|---|
| ṁ at M1/10 kft | 1.10 kg/s | corrected-flow model — NOT 0.69 |
| Net wet thrust @ M1 | 450–475 N | bench gate ≥ 450 N |
| Net dry thrust @ M1 | ~257 N | |
| AB fuel flow (1800 K) | ~27 g/s | dedicated Speck ZY-4S-12V pump |
| AB duration / cooldown | 20 s / 5 min | thermal limits |

## 3. Loads contracts (airframe, per 18 §3)

| Case | Limit | Ultimate |
|---|---|---|
| Symmetric pull-up | 4g | 6g |
| Launch (dolly 4.5g) | 4.5g | 6.75g |
| Landing vertical | 3g | 4.5g |
| Root bending (9g equiv.) | ~100 N·m | 150 N·m |

## 4. Change procedure

1. Propose in an issue/PR describing the ifc number, new value, and impact on each mating subsystem.
2. Affected owners must approve (comment). P0 if any `I-xx` value changes.
3. After approval: update `18_program_requirements.md`, this file, and any dependent CAD, then regenerate STEP/DXF and re-run the clash check.

## 5. Interface matrix (who must be notified)

Changes to | Notify | Reason
|---|---|---|
| I-01/I-03 | E1, E3 | mount loads, CG, utilities routing |
| I-04/I-05 | E2 | wing/engine proximity, stabilator flutter coupling |
| I-06 | E1, E4 | CG movement, dolly load transfer |
| I-09/I-10/I-11 | E1, E3 | structural + M&V gating |
| Thrust/mass-flow numbers | everyone | global program impact |
