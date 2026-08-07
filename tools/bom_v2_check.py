#! /tmp/opencode/cq312/bin/python
"""Mach 1 RC - BOM v2 arithmetic, CG excursion, and tank vent sizing.

Author: E3 (Systems/M&V). Committed per AGENTS.md sec 4.4 (analysis changes
must ship the script that produced the number).
All inputs trace to 18_program_requirements.md / 15 / 16 / 17 / 09.
"""
import math

# ---------------------------------------------------------------------------
# 1. BOM v2 (mirror of 22_bom_v2.md). (cat, item, qty, unit, supplier, single_src, fab)
#    Prices trace to 09_bom.md / 09_bom_with_links.md / 15:652 / 16:1119 /
#    17 / 18 sec 5.2. fab=True marks fabricated-not-purchased items.
# ---------------------------------------------------------------------------
BOM = [
    # --- Airframe ---
    ("Airframe", "Carbon fiber prepreg 3K twill 200 g/m^2 (skins)", 5, 45.0, "ACP Composites", False, False),
    ("Airframe", "Epoxy resin West System 105 + 206", 2, 60.0, "West System", False, False),
    ("Airframe", "Epoxy bonding 105 + 406 colloidal silica", 1, 40.0, "West System", False, False),
    ("Airframe", "Rohacell 71IG foam core 5 mm", 1, 80.0, "Aircraft Spruce", False, False),
    ("Airframe", "Rohacell 71IG 3 mm (box-spar shear-web core, 18 D1)", 1, 30.0, "Aircraft Spruce", False, False),
    ("Airframe", "T300 UD carbon tape (box-spar caps; supersedes DragonPlate rod per 18 D1)", 2, 15.0, "DragonPlate / Easy Composites", False, False),
    ("Airframe", "7075-T6 aluminum plate (engine mount ring, hardpoints)", 1, 50.0, "McMaster-Carr", False, False),
    ("Airframe", "6061-T6 aluminum sheet (brackets, small parts)", 1, 20.0, "McMaster-Carr", False, False),
    ("Airframe", "304 SS tube (tailpipe/exhaust stub)", 1, 10.0, "McMaster-Carr", False, False),
    ("Airframe", "Inconel 718 intake lip + diverter (DMLS)", 1, 350.0, "Xometry", True, True),
    ("Airframe", "CNC machined inserts (BH nut-plate doublers, mount-ring machining, rib pockets)", 1, 100.0, "Shop / local CNC", False, True),
    ("Airframe", "Fasteners assortment M2-M6 (nylon + stainless)", 1, 30.0, "Amazon", False, False),
    # --- Propulsion ---
    ("Propulsion", "JetCat P550-PRO (incl. ECU + internal gear pump)", 1, 4500.0, "JetCat / Chief RC", True, False),
    # --- Afterburner (structure = fabrication) ---
    ("Afterburner", "Transition duct (Inconel 625, 0.8 mm)", 1, 85.0, "Shop DMLS/form", True, True),
    ("Afterburner", "Spray ring assembly (Inconel 625 tube + 6 bosses)", 1, 60.0, "Shop DMLS", True, True),
    ("Afterburner", "Orifice discs 0.5 mm EDM (6)", 1, 90.0, "Wire EDM shop", False, True),
    ("Afterburner", "Flame holder (Inconel 625 V-gutter)", 1, 70.0, "Shop DMLS/form", True, True),
    ("Afterburner", "Liner (Inconel 625 corrugated, 65 film holes) - CONSUMABLE", 1, 120.0, "Shop DMLS", True, True),
    ("Afterburner", "Outer shell (304 SS, 0.8 mm)", 1, 40.0, "Shop", False, True),
    ("Afterburner", "Iris nozzle petals + sync ring (Ti-6Al-4V)", 1, 120.0, "Shop CNC", False, True),
    ("Afterburner", "Ceramic blanket 5 mm (Cotronics 3633)", 1, 35.0, "Cotronics", False, False),
    ("Afterburner", "Iris servo KST X08H+ (17:426)", 1, 28.0, "KST / dealers", False, False),
    ("Afterburner", "AB fuel pump Speck ZY-4S-12V (18 D8)", 1, 95.0, "Speck Pumpen / Anaheim", True, False),
    ("Afterburner", "Pump ESC 30 A (PWM drive)", 1, 15.0, "HobbyKing SS / ZTW", False, False),
    ("Afterburner", "Bosch EV14 fuel injector 0280158117", 1, 45.0, "Bosch distributor / eBay", False, False),
    ("Afterburner", "Injector driver MOSFET (IRF520)", 1, 5.0, "Mouser / eBay", False, False),
    ("Afterburner", "Injector check valves Beswick MCD-1008 (6)", 1, 150.0, "Beswick", False, False),
    ("Afterburner", "Main check valve McMaster 4723T78", 1, 13.0, "McMaster-Carr", False, False),
    ("Afterburner", "Fuel filter Dubro #601 (50 um) x2", 1, 10.0, "Dubro / AMain", False, False),
    ("Afterburner", "Brass barbed tee Dubro #567", 1, 4.0, "Dubro / AMain", False, False),
    ("Afterburner", "Viton 4 mm ID line (AB feed, rear run) 2 m", 1, 16.0, "McMaster 5119K75", False, False),
    ("Afterburner", "Barb fittings McMaster 5359K21 (6)", 1, 18.0, "McMaster-Carr", False, False),
    ("Afterburner", "Spark plug NGK CM-6 x2", 1, 16.0, "NGK dealer", False, False),
    ("Afterburner", "CDI module RCEXL G306", 1, 45.0, "RCEXL / RCGF", False, False),
    ("Afterburner", "HV wire NGK VD05G", 1, 10.0, "NGK dealer", False, False),
    ("Afterburner", "Spark plug cap NGK LB10EMH", 1, 6.0, "NGK dealer", False, False),
    ("Afterburner", "CDI filter cap WIMA MKP10 0.47 uF", 1, 3.0, "Mouser", False, False),
    ("Afterburner", "CDI pack 2S 500 mAh (isolated)", 1, 12.0, "HobbyKing", False, False),
    ("Afterburner", "Fuses 20 A + 3 A", 1, 7.0, "Amazon", False, False),
    ("Afterburner", "Misc wire / heatshrink (AB bay)", 1, 20.0, "Amazon", False, False),
    ("Afterburner", "Raspberry Pi Pico RP2040 (AB controller)", 1, 4.0, "RS / Amazon", False, False),
    ("Afterburner", "MAX6675 thermocouple amp x3 (I-12: 3x TC)", 1, 24.0, "Amazon", False, False),
    ("Afterburner", "K-type probe Inconel 1 mm x3", 1, 45.0, "Amazon / HYPER RC", False, False),
    ("Afterburner", "Flame detector Hamamatsu G5842 UV", 1, 35.0, "Hamamatsu / Mouser", False, False),
    ("Afterburner", "Pressure transducer Keller 4LPR-10 (0-10 bar)", 1, 50.0, "Keller", False, False),
    ("Afterburner", "Solenoid valve 12 V NC (AB fuel on/off)", 1, 20.0, "SMC / generic", False, False),
    ("Afterburner", "Solenoid MOSFET IRLZ44N + 1N4001 + 1k", 1, 3.0, "Mouser", False, False),
    ("Afterburner", "Optocoupler 4N25", 1, 1.0, "Mouser", False, False),
    ("Afterburner", "AB controller PCB / protoboard + enclosure + wire", 1, 30.0, "Amazon / shop", False, False),
    ("Afterburner", "AB utility routing (I-12): Ti 2 mm pushrod + PTFE sheath, 15 mm cooling duct, coax", 1, 40.0, "McMaster-Carr", False, False),
    # --- Systems / M&V ---
    ("Systems/M&V", "RC receiver Futaba R7018SB (18 ch FASSTest)", 1, 329.0, "Modelland / eBay", True, False),
    ("Systems/M&V", "Flight controller Cube Orange+", 1, 300.0, "CubePilot / ReadyMadeRC", False, False),
    ("Systems/M&V", "GPS u-blox M8P RTK (Here+) - NAV-PVT >=10 Hz", 1, 100.0, "CubePilot", False, False),
    ("Systems/M&V", "Telemetry RFD900x (air) - bundle 2 units ~$220", 1, 120.0, "ReadyMadeRC", False, False),
    ("Systems/M&V", "Pitot-static probe (Prandtl; REPLACES dead Eagle Tree link)", 1, 25.0, "HobbyKing / generic", False, False),
    ("Systems/M&V", "Airspeed sensor MS4525DO", 1, 35.0, "DigiKey / eBay", False, False),
    ("Systems/M&V", "TAT probe (Rosenount-style) at x=0.08 m (18 5.2)", 1, 40.0, "Aspen/OpenCanopy", False, False),
    ("Systems/M&V", "Sealed SD data loggers x2 (write-once, 50 Hz)", 1, 60.0, "OpenLog / byteflight", False, False),
    ("Systems/M&V", "FPV VTX 5.8 GHz + camera + ground goggles (18 5.2)", 1, 150.0, "GetFPV / RDQ", False, False),
    ("Systems/M&V", "Tungsten nose ballast 1.0 kg (18 5.2)", 1, 300.0, "McMaster / RMI", False, False),
    ("Systems/M&V", "Main battery 2S 5000 mAh 30 C", 1, 80.0, "Gens Ace / AMain", False, False),
    ("Systems/M&V", "Power distribution board", 1, 25.0, "CubePilot / custom", False, False),
    ("Systems/M&V", "Deans Ultra connectors (3 pairs)", 1, 12.0, "Amass / Amazon", False, False),
    ("Systems/M&V", "JR servo connectors (20)", 1, 30.0, "Amazon", False, False),
    ("Systems/M&V", "Wire 14 AWG silicone 3 m", 1, 15.0, "Amazon", False, False),
    ("Systems/M&V", "Wire 20 AWG silicone 5 m", 1, 15.0, "Amazon", False, False),
    ("Systems/M&V", "Wire 22 AWG silicone 10 m", 1, 25.0, "Amazon", False, False),
    ("Systems/M&V", "Braided nylon conduit 10 mm 3 m", 1, 12.0, "Amazon", False, False),
    ("Systems/M&V", "5 V BEC (Castle CC BEC 10 A)", 1, 30.0, "Castle Creations", False, False),
    ("Systems/M&V", "12 V boost (Pololu D24V50F12 2.5 A; supersedes U3V40A12 1.5 A - Speck needs 1.8 A)", 1, 20.0, "Pololu", False, False),
    ("Systems/M&V", "3.3 V regulator Pololu D24V10F3", 1, 10.0, "Pololu", False, False),
    # --- Fuel system (E3 owns per I-06; 18 D20) ---
    ("Systems/M&V", "Fuel bladder 2.0 L custom PU 2-ply (I-06 stations 0.35-0.60 m)", 1, 60.0, "Custom fabrication", True, True),
    ("Systems/M&V", "Viton tubing 4 mm ID x 7 mm OD (main engine feed) 3 m", 1, 45.0, "McMaster-Carr", False, False),
    ("Systems/M&V", "Viton vent line 5 mm ID (D20 - vent sized for 83 ml/s)", 1, 12.0, "McMaster-Carr", False, False),
    ("Systems/M&V", "Viton return line 4 mm ID (JetCat install practice) 1 m", 1, 8.0, "McMaster-Carr", False, False),
    ("Systems/M&V", "Fuel dot Dubro HD-175 (6 mm, top fill)", 1, 8.0, "Dubro / Tower", False, False),
    ("Systems/M&V", "One-way vent check valve (anti-siphon)", 1, 12.0, "Amazon", False, False),
    ("Systems/M&V", "Clunk pickup + felt filter (50-100 um)", 1, 6.0, "Dubro", False, False),
    ("Systems/M&V", "Brass fittings (barbs, tees, elbows)", 1, 15.0, "McMaster-Carr", False, False),
    # --- Launch / Recovery ---
    ("Launch/Recovery", "UHMWPE belly strip 50x200x5 mm x2", 1, 16.0, "McMaster-Carr", False, False),
    ("Launch/Recovery", "Ti-6Al-4V skid shoe 1x50x200 mm x2", 1, 30.0, "eBay / McMaster", False, False),
    ("Launch/Recovery", "Dolly wheel 50 mm PU x2", 1, 24.0, "Amazon", False, False),
    ("Launch/Recovery", "Dolly frame 2024-T6 T-slot 20x20 2 m", 1, 24.0, "McMaster-Carr", False, False),
    ("Launch/Recovery", "Dolly hardware (axles, bearings, E-clips)", 1, 15.0, "Amazon", False, False),
    ("Launch/Recovery", "Dolly release servo 5 g metal gear", 1, 12.0, "Amazon", False, False),
    ("Launch/Recovery", "Separation spring 50 N 30 mm", 1, 5.0, "McMaster-Carr", False, False),
    ("Launch/Recovery", "Dolly parachute 0.3 m", 1, 10.0, "Amazon", False, False),
    ("Launch/Recovery", "Dolly abort brakes + pull-pin cable (18 D12)", 1, 40.0, "Amazon / shop", False, False),
    ("Launch/Recovery", "Drogue main chute 0.6 m ribbon (custom net-part)", 1, 30.0, "Custom fab", True, True),
    ("Launch/Recovery", "Pilot chute 0.1 m spring-loaded", 1, 15.0, "Amazon", False, False),
    ("Launch/Recovery", "Bridle 500 kg Kevlar 3 m", 1, 10.0, "Amazon", False, False),
    ("Launch/Recovery", "Ball-bearing swivel", 1, 8.0, "Amazon", False, False),
    ("Launch/Recovery", "Drogue container G10 box (custom)", 1, 20.0, "Fabricate", False, True),
    ("Launch/Recovery", "Weak link / jettison 100 kg", 1, 12.0, "Amazon", False, False),
    ("Launch/Recovery", "Drogue door servo (micro, metal gear)", 1, 15.0, "Amazon", False, False),
    # --- Consumables ---
    ("Consumables", "Mold release Partall #2 1 L", 1, 25.0, "Fibre Glast", False, False),
    ("Consumables", "Peel ply 5 m", 1, 40.0, "Amazon", False, False),
    ("Consumables", "Breather cloth 5 m", 1, 30.0, "Amazon", False, False),
    ("Consumables", "Vacuum bag film 5 m", 1, 50.0, "Amazon", False, False),
    ("Consumables", "Bag sealant tape 2 rolls", 1, 12.0, "Amazon", False, False),
    ("Consumables", "CNC foam plug 200x200x1000", 1, 30.0, "McMaster-Carr", False, False),
    ("Consumables", "Sanding supplies 80-1000", 1, 25.0, "Amazon", False, False),
    ("Consumables", "Vacuum pump rental", 1, 50.0, "Local / shop", False, False),
    ("Consumables", "Tooling gelcoat grey 2 kg", 1, 60.0, "Fibre Glast", False, False),
    ("Consumables", "Fiberglass tooling 200 g/m^2 10 m^2", 1, 100.0, "Fibre Glast", False, False),
    ("Consumables", "Jet A1 fuel (build/test + 2 sorties)", 1, 30.0, "Local FBO", False, False),
    ("Consumables", "Fire extinguisher + PPE (flight-line safety)", 1, 50.0, "Amazon", False, False),
]

cats = {}
total = 0.0
n = 0
for cat, item, qty, unit, sup, ss, fab in BOM:
    t = qty * unit
    total += t
    n += 1
    cats[cat] = cats.get(cat, 0.0) + t

print("=" * 64)
print(f"BOM v2 line items : {n}")
for c in ["Airframe", "Propulsion", "Afterburner", "Systems/M&V", "Launch/Recovery", "Consumables"]:
    print(f"  {c:16s} : ${cats[c]:9,.2f}")
print(f"  {'TOTAL':16s} : ${total:9,.2f}")
print("=" * 64)

# 18 sec 5.2 add-on group check
group520 = 40 + 60 + 150 + 300 + 80 + 120
print(f"18 sec 5.2 group subtotal (TAT+loggers+FPV+ballast+pump+BEC/etc): ${group520:,.2f}")

# ---------------------------------------------------------------------------
# 2. CG excursion (18 sec 3.4 mass table) - full -> empty fuel
# ---------------------------------------------------------------------------
rows = [
    ("P550-PRO engine", 4.90, 1.20),
    ("Afterburner", 0.83, 1.48),
    ("Wing + carry-through", 0.50, 1.00),
    ("Stabilator + hardware", 0.10, 2.35),
    ("Ventral fin", 0.10, 2.30),
    ("Fuselage structure", 2.50, 1.30),
    ("Fuel (2.0 L Jet A1)", 1.62, 0.45),
    ("Fuel system", 0.50, 0.60),
    ("Avionics + battery + FPV + M&V", 0.90, 0.25),
    ("Landing/dolly hardpoints", 0.35, 0.80),
    ("Nose ballast (tungsten)", 1.00, 0.10),
    ("Miscellaneous", 0.30, 1.00),
]
M = sum(r[1] for r in rows)
mom = sum(r[1] * r[2] for r in rows)
m_fuel = rows[6][1]
x_fuel = rows[6][2]
cg_full = mom / M
M_empty = M - m_fuel
mom_empty = mom - m_fuel * x_fuel
cg_empty = mom_empty / M_empty
MAC = 0.156
NP = 1.00  # 18 sec 3.4: neutral point approx 1.00 m
sm_full = (NP - cg_full) / MAC
sm_empty = (NP - cg_empty) / MAC
np_req_empty = cg_empty + 0.12 * MAC

print("=" * 64)
print(f"MTOW full        : {M:6.2f} kg   moment {mom:6.3f} kg.m  CG {cg_full:.4f} m")
print(f"MTOW empty       : {M_empty:6.2f} kg   moment {mom_empty:6.3f} kg.m  CG {cg_empty:.4f} m")
print(f"Fuel-burn excursion (full->empty): +{cg_empty - cg_full:.4f} m  (aft)")
print(f"Static margin full  (NP=1.00) : {sm_full*100:6.1f} % MAC")
print(f"Static margin empty (NP=1.00) : {sm_empty*100:6.1f} % MAC   <- 18 claim '>=12% at empty' does NOT hold")
print(f"NP required for >=12% MAC at empty CG: {np_req_empty:.4f} m")
print("=" * 64)

# ---------------------------------------------------------------------------
# 3. Tank vent diameter for 83 ml/s makeup air
# ---------------------------------------------------------------------------
Q = 83e-6            # m3/s (fuel volume leaving tank = air volume entering)
rho = 1.225          # kg/m3 air (SL)
Cd = 0.6             # short-tube/entrance+exit loss coefficient
for dP in (25.0, 50.0, 100.0):
    A = Q / (Cd * math.sqrt(2 * dP / rho))
    d = math.sqrt(4 * A / math.pi) * 1000
    print(f"vent @ dP={dP:5.0f} Pa: d = {d:5.2f} mm  ->  recommend 5 mm ID")

# existing 2 mm vent pressure drop at 83 ml/s
for dmm in (2.0, 5.0):
    A = math.pi / 4 * (dmm / 1000) ** 2
    V = Q / A
    dP = 0.5 * rho * (V / Cd) ** 2
    print(f"vent ID {dmm:.1f} mm: V={V:6.1f} m/s  dP={dP:8.0f} Pa")

# ---------------------------------------------------------------------------
# 4. Current budget / battery sizing for a ~5 min sortie + 2x20s AB dashes
# ---------------------------------------------------------------------------
servo_cruise = 0.5
servo_peak = 4.0
ecu_avg = 1.5
ecu_peak = 2.0
rail5 = 1.7          # FC 0.4 + Rx 0.2 + RFD 0.3 + FPV 0.5 + loggers 0.2 + TAT 0.1
dash = 20.0          # s per AB dash, x2
pump_12 = 1.5        # A @ 12 V Speck operating point (6 bar / 34 g/s)
sol_12 = 0.5
boost_eff = 0.85
batt_V = 7.4
i_from_batt_dash = (pump_12 + sol_12) * 12.0 / batt_V / boost_eff   # A on 2S during AB
flight_avg = servo_cruise + ecu_avg + rail5 + 0.1  # + Pico/sensors
t_flight = 5.0 * 60.0
Ah = (flight_avg * t_flight + i_from_batt_dash * dash * 2) / 3600.0
peak = servo_peak + ecu_peak + i_from_batt_dash
cap = 5.0  # Ah
print("=" * 64)
print(f"Flight avg draw (2S)        : {flight_avg:.2f} A")
print(f"AB dash draw on 2S          : {i_from_batt_dash:.2f} A (2x20 s)")
print(f"Charge used / 5 min sortie  : {Ah:.3f} Ah  of {cap:.1f} Ah -> {Ah/cap*100:.1f}%")
print(f"Worst-case peak draw        : {peak:.1f} A (battery 150 A burst OK)")
print("=" * 64)
