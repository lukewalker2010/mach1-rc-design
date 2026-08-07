# Mach 1 RC — Bill of Materials v2 (authoritative for the build)

**Author:** E3 (Systems/M&V), 2026-08-06
**Supersedes:** `09_bom.md` and `09_bom_with_links.md` for build procurement.
**Dispositions closed:** 18 §7 D19 (BOM missing AB + M&V items), D20 (fuel vent), D23 (09 cost math errors), D24 (dead links).
**Total:** **$9,662** — re-summed line-by-line (see §7). Within ~2% of the 18 §5.2 / 00_index target **~$9,500**; the delta is the fully itemised AB build-out from 15:652 and 16:1119 vs the rough §5.2 estimate.

> Legend: **★** = single-source / critical-path item. **[FAB]** = fabricated in-house or via a machine shop, not bought off-the-shelf. All prices USD, traceable to `09_bom.md`, `09_bom_with_links.md`, `15_afterburner_fuel_ignition.md` (App. C, line 652), `16_afterburner_electronics.md` (line 1119), `17_afterburner_thermal_integration.md` (2d), and `18_program_requirements.md` §5.2. Sum verified by `tools/bom_v2_check.py`.

---

## 1. Summary

| Subsystem | Total |
|---|---|
| Airframe | $1,085 |
| Propulsion | $4,500 |
| Afterburner | $1,390 |
| Systems / M&V (incl. fuel system) | $1,899 |
| Launch / Recovery | $286 |
| Consumables | $502 |
| **TOTAL** | **$9,662** |

---

## 2. Airframe — $1,085

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| A1 | Carbon prepreg 3K twill | 200 g/m², skins + fuselage | 5 m² | $45/m² | $225 | ACP Composites (acpcomposites.com) | | | domain moved from acpsales.com (link report #36) |
| A2 | Epoxy resin | West System 105 + 206 | 2 L | $60/L | $120 | West System | | | |
| A3 | Epoxy bonding | West System 105 + 406 silica | 0.5 L | $40 | $40 | West System | | | |
| A4 | Foam core | Rohacell 71IG, 5 mm | 1 m² | $80/m² | $80 | Aircraft Spruce | | | |
| A5 | Foam core (box-spar web) | Rohacell 71IG, 3 mm | 0.5 m² | $60/m² | $30 | Aircraft Spruce | | | new for 18 §3.2 box spar |
| A6 | T300 UD carbon tape | box-spar caps, ~6 mm separation | 2 m | $15/m | $30 | DragonPlate / Easy Composites | | | **supersedes DragonPlate pultruded rod** — rod is on the bending neutral axis (18 D1) |
| A7 | 7075-T6 plate | engine mount ring, hardpoints | 0.2 m² | $50 | $50 | McMaster-Carr | | | |
| A8 | 6061-T6 sheet | brackets, small parts | 0.3 m² | $20 | $20 | McMaster-Carr | | | |
| A9 | 304 SS tube | tailpipe/exhaust stub | 50 mm | $10 | $10 | McMaster-Carr | | | |
| A10 | **Inconel 718 intake** (lip + diverter) | DMLS, 105 mm lip / 103 mm throat (I-02) | 1 | $350 | $350 | Xometry | ★ | [FAB] | long lead; alternates Protolabs / Shapeways / 3D Systems |
| A11 | CNC machined inserts | BH nut-plate doublers, mount-ring machining, rib pockets | 1 lot | $100 | $100 | Shop / local CNC | | [FAB] | |
| A12 | Fasteners assortment | M2–M6 nylon + stainless | 1 lot | $30 | $30 | Amazon | | | |

## 3. Propulsion — $4,500

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| P1 | **JetCat P550-PRO** (incl. ECU + internal gear pump) | single engine, program-critical | 1 | $4,500 | $4,500 | JetCat (jetcat.de) / Chief RC / JetCat USA | ★ | | price on request, $4,500–5,500; **order first (long lead)** |

## 4. Afterburner — $1,390

Structural hot-section parts are **[FAB]** Inconel 625 / Ti-6Al-4V / 304 SS per the 14–17 package and 18 §3.4 (0.83 kg AB mass). Geometry per the `.step` files (`ab_*.step`).

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| AB1 | Transition duct | Inconel 625, 0.8 mm wall (17:420, 90 g) | 1 | $85 | $85 | Shop DMLS | ★ | [FAB] | |
| AB2 | Spray ring assembly | Inconel 625 tube + 6 bosses (15:660) | 1 | $60 | $60 | Shop DMLS | ★ | [FAB] | |
| AB3 | Orifice discs | 0.5 mm EDM hole, Inconel (15:663) | 6 | $15 | $90 | Wire EDM shop | | [FAB] | |
| AB4 | Flame holder | Inconel 625 V-gutter (17:422) | 1 | $70 | $70 | Shop DMLS | ★ | [FAB] | |
| AB5 | **Liner** | Inconel 625 corrugated, 65 film-cooling holes (17 §2) | 1 | $120 | $120 | Shop DMLS | ★ | [FAB] | **consumable**, replace ~5–10 flights (17:237, 18 §5.5) |
| AB6 | Outer shell | 304 SS, 0.8 mm, Ø90/93 (17:248, 424) | 1 | $40 | $40 | Shop | | [FAB] | |
| AB7 | Iris nozzle | Ti-6Al-4V petals + sync ring (17:425) | 1 | $120 | $120 | Shop CNC | | [FAB] | |
| AB8 | Ceramic blanket | 5 mm, Cotronics 3633, 1260 °C rated (17:293) | 1 | $35 | $35 | Cotronics | | | keeps composite <100 °C |
| AB9 | Iris servo | KST X08H+, 12 g (17:426) | 1 | $28 | $28 | KST / dealers | | | |
| AB10 | **AB fuel pump** | **Speck ZY-4S-12V** (18 D8; 15:656) | 1 | $95 | $95 | Speck Pumpen / Anaheim | ★ | | dedicated; engine-pump tap is impossible (18 §2.1). 18 §5.2 estimated $80 |
| AB11 | Pump ESC | 30 A (SS / ZTW), PWM drive (15:657) | 1 | $15 | $15 | HobbyKing / ZTW | | | |
| AB12 | Fuel injector | Bosch EV14 0280158117 (15:658) | 1 | $45 | $45 | Bosch dist. / eBay | | | |
| AB13 | Injector driver | IRF520 MOSFET + diode (15:659) | 1 | $5 | $5 | Mouser / eBay | | | |
| AB14 | Injector check valves | Beswick MCD-1008 ×6 (15:661) | 6 | $25 | $150 | Beswick | | | anti-drain / anti-coking |
| AB15 | Main check valve | McMaster 4723T78, 0.5 bar (15:262) | 1 | $13 | $13 | McMaster-Carr | | | |
| AB16 | Fuel filter | Dubro #601, 50 µm ×2 | 2 | $5 | $10 | Dubro / AMain | | | |
| AB17 | Tee fitting | Dubro #567 | 1 | $4 | $4 | Dubro / AMain | | | |
| AB18 | Viton 4 mm ID line | AB feed, rear run (I-12) | 2 m | $8/m | $16 | McMaster 5119K75 | | | |
| AB19 | Barb fittings | McMaster 5359K21 ×6 | 6 | $3 | $18 | McMaster-Carr | | | |
| AB20 | Spark plug | NGK CM-6 (1 + 1 spare) | 2 | $8 | $16 | NGK dealer | | | |
| AB21 | CDI module | RCEXL G306, 15–25 kV (15:334) | 1 | $45 | $45 | RCEXL / RCGF | | | |
| AB22 | HV wire | NGK VD05G | 1 | $10 | $10 | NGK dealer | | | |
| AB23 | Spark plug cap | NGK LB10EMH | 1 | $6 | $6 | NGK dealer | | | |
| AB24 | CDI filter cap | WIMA MKP10 0.47 µF | 1 | $3 | $3 | Mouser | | | |
| AB25 | **CDI pack** | 2S 500 mAh LiPo, isolated (15:672) | 1 | $12 | $12 | HobbyKing | | | isolated per 23 §4 |
| AB26 | Fuses | 20 A + 3 A | 2 | — | $7 | Amazon | | | |
| AB27 | Misc wire / heatshrink | AB bay | 1 lot | $20 | $20 | Amazon | | | |
| AB28 | AB controller | Raspberry Pi Pico RP2040 (16:1111) | 1 | $4 | $4 | RS / Amazon | | | |
| AB29 | Thermocouple amps | MAX6675 ×3 (I-12: 3× TC) | 3 | $8 | $24 | Amazon | | | |
| AB30 | K-type probes | 1 mm exposed, Inconel sheath ×3 | 3 | $15 | $45 | HYPER RC / Amazon | | | |
| AB31 | Flame detector | Hamamatsu G5842 UV (16:1117) | 1 | $35 | $35 | Hamamatsu / Mouser | | | |
| AB32 | Pressure transducer | Keller 4LPR-10, 0–10 bar (16:1118) | 1 | $50 | $50 | Keller | | | |
| AB33 | Solenoid valve | 12 V NC, 1/8" NPT (16:1121) | 1 | $20 | $20 | SMC / generic | | | AB fuel on/off |
| AB34 | Solenoid MOSFET | IRLZ44N + 1N4001 + 1 kΩ (16:1122) | 1 | $3 | $3 | Mouser | | | |
| AB35 | Optocoupler | 4N25 (16:1125) | 1 | $1 | $1 | Mouser | | | |
| AB36 | Controller board | protoboard/PCB + enclosure + wire (16:1126–29) | 1 | $30 | $30 | Amazon / shop | | [FAB] | |
| AB37 | AB utility routing | I-12: Ti 2 mm pushrod + PTFE, Ø15 mm cooling duct, ignition coax | 1 | $40 | $40 | McMaster-Carr | | [FAB] | 52.5 mm annulus per 17 §2b |

## 5. Systems / M&V (incl. fuel system) — $1,899

### 5.1 Avionics & instrumentation

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| S1 | RC receiver | Futaba R7018SB, 18 ch FASSTest (07 §3.1) | 1 | $329 | $329 | Modelland / eBay | ★ | | **supply risk** — often sold out (link report #13-15). Alternates: R7008SB / R7108SB |
| S2 | Flight controller | Cube Orange+ (Pixhawk) | 1 | $300 | $300 | CubePilot / ReadyMadeRC | | | |
| S3 | GPS | Here+ RTK GNSS, u-blox M8P, **NAV-PVT ≥10 Hz** (18 §5.1) | 1 | $100 | $100 | CubePilot | | | |
| S4 | Telemetry | RFD900x (900 MHz) air unit | 1 | $120 | $120 | ReadyMadeRC | | | buy bundle (2 units) ~$220 for air + ground |
| S5 | Pitot-static probe | Prandtl-type at x = 0.05 m (I-07) | 1 | $25 | $25 | HobbyKing / generic | | | **replaces dead Eagle Tree link** (link report #24: domain DNS-failed) |
| S6 | Airspeed sensor | MS4525DO differential | 1 | $35 | $35 | DigiKey / eBay | | | Mouser/DigiKey block bots; order via product page |
| S7 | **TAT probe** | Rosenount-style total-air-temp at x = 0.08 m (I-07) | 1 | $40 | $40 | Aspen/OpenCanopy equiv. | | | 18 §5.2 add-on |
| S8 | Sealed SD loggers | 2× independent, write-once, ≥50 Hz (18 §5.1) | 2 | $30 | $60 | OpenLog / byteflight | | | 18 §5.2 add-on |
| S9 | **FPV** | 5.8 GHz VTX + camera + ground goggles (18 §5.2) | 1 set | $150 | $150 | GetFPV / RDQ | | | mandatory (18 §5.3) |
| S10 | **Tungsten ballast** | 1.0 kg nose, x = 0.10 m (18 §3.4/§5.2) | 1 | $300 | $300 | McMaster / RMI | | | |

### 5.2 Power

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| S11 | Main battery | 2S 5000 mAh 30 C (07/16) | 1 | $80 | $80 | Gens Ace / AMain | | | sized per 23 §5 |
| S12 | Power distribution board | Pixhawk power module | 1 | $25 | $25 | CubePilot | | | |
| S13 | Deans Ultra connectors | 3 pairs | 3 | $4 | $12 | Amass / Amazon | | | |
| S14 | JR connectors | male+female | 20 | $1.50 | $30 | Amazon | | | |
| S15 | Wire 14 AWG silicone | red/black | 3 m | $5/m | $15 | Amazon | | | |
| S16 | Wire 20 AWG silicone | assorted | 5 m | $3/m | $15 | Amazon | | | |
| S17 | Wire 22 AWG silicone | signal | 10 m | $2.50/m | $25 | Amazon | | | |
| S18 | Conduit braided nylon | 10 mm | 3 m | $4/m | $12 | Amazon | | | |
| S19 | **5 V BEC** | Castle CC BEC 10 A (16:1112) | 1 | $30 | $30 | Castle Creations | | | 18 §5.2 group |
| S20 | **12 V boost** | Pololu D24V50F12 **2.5 A** — **supersedes 16's U3V40A12 (1.5 A)**: Speck pump needs 1.8 A @ 12 V | 1 | $20 | $20 | Pololu | | | 18 §5.2 group; sizing justified in 23 §4–5 |
| S21 | 3.3 V regulator | Pololu D24V10F3 (16:1114) | 1 | $10 | $10 | Pololu | | | |

### 5.3 Fuel system (E3 owns, I-06 / 18 D20)

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| S22 | **Fuel bladder** | **2.0 L** custom 2-ply PU, stations 0.35–0.60 m (I-06, 18 §3.4) | 1 | $60 | $60 | Custom fabrication | ★ | [FAB] | no off-the-shelf conformal bladder; 18 D20 resolves 1.2/1.5/2.0 L → 2.0 L |
| S23 | Viton feed line | 4 mm ID × 7 mm OD, engine feed | 3 m | $15/m | $45 | McMaster | | | |
| S24 | **Vent line** | **5 mm ID** Viton, top of bladder | 1 m | $12 | $12 | McMaster | | | D20 — 2 mm was undersized; diameter calc in 23 §6 (5.25 mm needed @25 Pa) |
| S25 | Return line | Viton 4 mm ID, JetCat install practice | 1 m | $8 | $8 | McMaster | | | 18 D20 |
| S26 | Fuel dot | Dubro HD-175, 6 mm, top fill | 1 | $8 | $8 | Dubro / Tower | | | I-06 |
| S27 | Vent check valve | one-way, anti-siphon | 1 | $12 | $12 | Amazon | | | |
| S28 | Clunk pickup + filter | felt, 50–100 µm | 1 | $6 | $6 | Dubro | | | |
| S29 | Brass fittings | barbs, tees, elbows | 1 lot | $15 | $15 | McMaster | | | |

## 6. Launch / Recovery — $286

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| L1 | UHMWPE belly strip | 50×200×5 mm | 2 | $8 | $16 | McMaster-Carr | | | I-10 |
| L2 | Ti skid shoe | Ti-6Al-4V 1×50×200 mm | 2 | $15 | $30 | eBay / McMaster | | | |
| L3 | Dolly wheels | 50 mm PU × 20 mm | 2 | $12 | $24 | Amazon | | | |
| L4 | Dolly frame | 2024-T6 T-slot 20×20 mm | 2 m | $12/m | $24 | McMaster-Carr | | | |
| L5 | Dolly hardware | axles, bearings, E-clips | 1 lot | $15 | $15 | Amazon | | | |
| L6 | Dolly release servo | 5 g metal gear | 1 | $12 | $12 | Amazon | | | |
| L7 | Separation spring | 50 N, 30 mm stroke | 1 | $5 | $5 | McMaster-Carr | | | |
| L8 | Dolly parachute | 0.3 m ripstop | 1 | $10 | $10 | Amazon | | | |
| L9 | **Dolly abort brakes + pull-pin cable** | 18 D12 (no braking during roll today) | 1 set | $40 | $40 | Amazon / shop | | [FAB] | |
| L10 | **Drogue main chute** | 0.6 m hemispherical ribbon, net-part spec (I-11) | 1 | $30 | $30 | Custom fabrication | ★ | [FAB] | TAS-gated deploy ≤ M0.6 (18 §5.4); ChutingStar link blocked |
| L11 | Pilot chute | 0.1 m spring-loaded | 1 | $15 | $15 | Amazon | | | |
| L12 | Bridle line | 500 kg Kevlar, 3 m | 1 | $10 | $10 | Amazon | | | |
| L13 | Swivel | ball-bearing | 1 | $8 | $8 | Amazon | | | |
| L14 | Drogue container | G10 box, custom | 1 | $20 | $20 | Fabricate | | [FAB] | BH8 doubler/insert for 1 kN opening load (18 §5.4) |
| L15 | Weak link / jettison | 100 kg Kevlar + hook | 1 | $12 | $12 | Amazon | | | |
| L16 | Drogue door servo | micro metal gear | 1 | $15 | $15 | Amazon | | | 18 §5.2 group |

## 7. Consumables — $502

| # | Item | Spec | Qty | Unit | Total | Supplier | ★ | FAB | Notes |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Mold release | Partall #2, 1 L | 1 | $25 | $25 | Fibre Glast | | | |
| C2 | Peel ply | nylon, 1 m wide | 5 m | $8/m | $40 | Amazon | | | |
| C3 | Breather cloth | polyester, 1 m wide | 5 m | $6/m | $30 | Amazon | | | |
| C4 | Vacuum bag film | nylon, 1 m wide | 5 m | $10/m | $50 | Amazon | | | |
| C5 | Bag sealant tape | QT-2 butyl | 2 rolls | $6 | $12 | Amazon | | | |
| C6 | CNC foam plug | PU 200×200×1000 | 1 | $30 | $30 | McMaster-Carr | | | |
| C7 | Sanding supplies | 80–1000 grit | 1 lot | $25 | $25 | Amazon | | | |
| C8 | Vacuum pump | rental / shop | 1 | $50 | $50 | Local | | | |
| C9 | Tooling gelcoat | grey, 2 kg | 2 | $30/kg | $60 | Fibre Glast | | | |
| C10 | Fiberglass (tooling) | 200 g/m², splash mould | 10 m² | $10/m² | $100 | Fibre Glast | | | |
| C11 | Jet A1 fuel | build/test + 2 sorties (~10 L) | 10 L | $3/L | $30 | Local FBO | | | |
| C12 | Fire extinguisher + PPE | flight-line safety | 1 set | $50 | $50 | Amazon | | | per 09 §3 |

---

## 8. Single-source critical-path items (★) & alternates

| Item | Cost | Why critical | Alternate if it fails |
|---|---|---|---|
| **JetCat P550-PRO + ECU + pump** | $4,500 | only engine that closes T–D; program is built around it (18 §2) | none program-equivalent; buy from JetCat USA / Chief RC (2nd dealer). **Order first.** |
| **KST X20-12T** ×2 | $240 | stabilator flutter margin / 12 kg·cm @ 8.4 V (I-05) | no drop-in equivalent; Buddy RC is 2nd dealer of the *same* part, not an alternate. Stock-outs common → order early |
| **Speck ZY-4S-12V** | $95 | AB fuel ≥ 450 N wet (18 D8); engine-pump tap impossible | HobbyKing gear pump rejected in 15 (marginal, 2.5 L/min); Speck is the decision |
| **Xometry Inconel DMLS** (intake + AB parts) | ~$490 | intake lip/diverter + hot-section geometry | Protolabs / Shapeways / 3D Systems (same STL/STEP); long lead |
| **Custom bladder 2.0 L** | $60 | I-06 envelope, no off-the-shelf | none — must be made; JetCat OEM tank is 1.2 L (too small) |
| **Custom drogue 0.6 m** | $30 | TAS-gated landing spec (18 §5.4) | generic 0.6 m chutes exist (ChutingStar link blocked to bots) but not to net-part spec |
| **Futaba R7018SB** | $329 | FASSTest + 18 ch + S.Bus2 | R7008SB / R7108SB (fewer channels, same protocol) |
| **AB liner** (consumable) | $120 | must survive ~5–10 AB flights then be replaced (17:237) | vendor-laser-cut Inconel; stock one spare |

## 9. Link status (from `bom_link_check_report.md`, 2026-07-23)

| Item | Status | Action in v2 |
|---|---|---|
| Eagle Tree pitot-static | ❌ DNS dead (`eagletreetechnologies.com` ENOTFOUND, report #24) | replaced with generic Prandtl probe (S5) — dead link eliminated |
| HobbyKing (Futaba, LiPo) | ❌ Cloudflare-blocked to bots (report #14, #28) | alternate vendors listed (Modelland for Rx) |
| ChutingStar (drogue) | ❌ blocked (report #61) | drogue is custom fabrication (L10) |
| Mouser / DigiKey | ❌ blocked to bots (report #25-26) | order via product page / eBay |
| eBay search links | ❌ 403 to bots | fine in a human browser |
| acpsales.com | ⚠️ redirects → acpcomposites.com | use new domain |
| Cube Orange+ Amazon price | ⚠️ $449 on Amazon vs $300 BOM | BOM keeps $300 (CubePilot/ReadyMadeRC list); confirm at order |
| RFD900x | ✅ strong (ReadyMadeRC bundle) | bundle ~$220 includes ground modem |

## 10. Corrections to 09 (18 §7 D23)

- **Power section:** 09 §1.9 stated $174; the 09 lines actually sum to **$214** (2S $80 + PDB $25 + Deans $12 + JR $30 + 14AWG $15 + 20AWG $15 + 22AWG $25 + conduit $12). **Off by $40.** v2 carries the correct $214 (S11–S18) and adds the missing BEC/boost/regulator (+$60).
- **Tooling/consumables:** 09 §1.9 stated $462; lines sum to **$452**. v2 re-sums as $502 including fuel + safety items.
- **09 total "~$7,662"** → v2 corrected, re-summed, and re-based: **$9,662** (adding the missing AB system $1,390, M&V add-ons $750 group, fuel-system v2, dolly abort brakes).
- 09 carried the AB pump/solenoid/iris/CDI/BEC items nowhere (D19); v2 places them per 15:652 and 16:1119 with unit prices from those tables.

*Every line above is re-summed by `tools/bom_v2_check.py` (107 lines, total $9,662).*
