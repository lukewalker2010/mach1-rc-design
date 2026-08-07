#!/usr/bin/env python3
"""
ab_bench_analysis.py — Corrected afterburner bench-model numbers at the
re-baselined mass flow.

Source authority:
  - mdot at M1/10kft = 1.10 kg/s  (18_program_requirements.md sec 2.1, 13 Method B)
  - Vj_dry = 566 m/s, T5 dry = 1000 K  (18 sec 2.1; 13:120,123)
  - Vinf = 328 m/s  (13:65, speed of sound at 10kft ISA)
  - LHV Jet A1 = 43 MJ/kg, cp = 1200 J/kgK, eta_comb = 0.90  (17 sec 1a)
  - Liner D = 80 mm, L = 200 mm, mu = 4e-5 Pa.s, Pr = 0.7, k = 0.08 W/mK  (17 sec 1b)
  - Static SL mass flow (wet) = 0.95 kg/s (0.93 core per datasheet 13:15/67
    + 0.023 kg/s AB fuel at T7=1800K)

Every printed number is reproduced in 21_afterburner_bench_program.md.
"""

import math

MDOT_M1 = 1.10      # kg/s, corrected-flow model at M1/10kft (18 sec 2.1)
MDOT_SL = 0.95      # kg/s, static sea-level wet (0.93 core + 0.023 AB)
VINF = 328.0        # m/s, 10kft speed of sound (13:65)
VJ_DRY = 566.0      # m/s, dry jet velocity TIT-limited (18 sec 2.1, 13:123)
T5 = 1000.0         # K, dry turbine-exit temp TIT-limited (18 sec 2.1, 13:120)
CP = 1200.0         # J/kgK combustion products (17 sec 1a)
LHV = 43.0e6        # J/kg Jet A1 (17 sec 1a)
ETA = 0.90          # V-gutter flameholder comb. eff. (17 sec 1a)

print("=" * 74)
print("SEC 1: CORRECTED WET THRUST MODEL AT MDOT = 1.10 kg/s (M1 / 10 kft)")
print("  Vj(T7) = Vj_dry*sqrt(T7/1000) = 566*sqrt(T7/1000)")
print("  gross  = mdot*Vj        ram = mdot*Vinf = 1.10*328")
print("  net    = gross - ram    boost vs dry net 257 N (18 sec 2.1)")
print("=" * 74)
hdr = f"{'T7 K':>6} {'Vj m/s':>8} {'gross N':>9} {'ram N':>7} {'net N':>7} {'boost':>6}"
print(hdr)
for T7 in (1700.0, 1800.0, 1900.0):
    Vj = VJ_DRY * math.sqrt(T7 / 1000.0)
    gross = MDOT_M1 * Vj
    ram = MDOT_M1 * VINF
    net = gross - ram
    print(f"{T7:6.0f} {Vj:8.1f} {gross:9.1f} {ram:7.1f} {net:7.1f} {net/257.0:5.0%}")

print()
print("=" * 74)
print("SEC 2: CORRECTED AB FUEL FLOW (energy balance) at T7 = 1800 K")
print("  mdot_fuel = mdot*cp*(T7-T5)/(LHV*eta)")
print("  T5 = 1000 K (18 sec 2.1), not the 973 K used in 17 sec 1a")
print("=" * 74)
T7 = 1800.0
mdot_fuel = MDOT_M1 * CP * (T7 - T5) / (LHV * ETA)
m_O2_avail = MDOT_M1 * 0.155          # 14% O2 mole frac -> mass frac 0.155 (17 sec 1a)
m_O2_cons = mdot_fuel * 3.40          # stoich 3.40 kg O2/kg fuel (17 sec 1a)
phi = m_O2_cons / m_O2_avail
print(f"  AB fuel flow      = {mdot_fuel*1000:6.1f} g/s  ({mdot_fuel:5.3f} kg/s)")
print(f"  O2 available      = {m_O2_avail:5.3f} kg/s   (1.10 * 0.155)")
print(f"  O2 consumed       = {m_O2_cons:5.3f} kg/s   (fuel * 3.40)")
print(f"  fraction consumed = {phi:5.1%}  (equivalence ratio, O2-based)")
mdot_fuel_sl = MDOT_SL * CP * (T7 - T5) / (LHV * ETA)
print(f"  static-SL AB fuel = {mdot_fuel_sl*1000:6.1f} g/s  (bench, mdot 0.95 kg/s)")
g_5 = mdot_fuel * 5.0 * 1000.0
g_20 = mdot_fuel * 20.0 * 1000.0
print(f"  per 5 s burst     = {g_5:5.0f} g  = {g_5/0.81:4.0f} ml  (Jet A1 0.81 kg/L)")
print(f"  per 20 s burst    = {g_20:5.0f} g  = {g_20/0.81:4.0f} ml")

print()
print("=" * 74)
print("SEC 3: STATIC -> M1 GATE CONVERSION (ram-drag-free thrust stand)")
print("  net_M1 = F_s * (mdot_M1/mdot_SL) - mdot_M1*Vinf  >= 450 N")
print("  F_s >= (450 + mdot_M1*Vinf) * mdot_SL/mdot_M1")
print("=" * 74)
ram_M1 = MDOT_M1 * VINF
k = MDOT_M1 / MDOT_SL
F_s_gate = (450.0 + ram_M1) * (MDOT_SL / MDOT_M1)
Vj1800 = VJ_DRY * math.sqrt(T7 / 1000.0)
F_s_design = MDOT_SL * Vj1800
net_design_M1 = F_s_design * k - ram_M1
print(f"  ram at M1         = {ram_M1:6.1f} N")
print(f"  mass-flow ratio k = {k:.4f}  (mdot_M1/mdot_SL)")
print(f"  STATIC GATE F_s   = {F_s_gate:6.1f} N  -> net_M1 = 450 N")
print(f"  design F_s        = {F_s_design:6.1f} N  (0.95*{Vj1800:.1f})  -> net_M1 = {net_design_M1:.0f} N")
print(f"  naive '450+ram'   = {450.0+ram_M1:6.1f} N  (conservative, ignores mdot ratio)")

print()
print("=" * 74)
print("SEC 4: CORRECTED THERMAL NUMBERS (mass-flow-dependent)")
print("  Liner Re   = 4*mdot/(pi*D*mu),  D=0.08 m, mu=4e-5 Pa.s")
print("  Gnielinski: f=(0.79*ln Re -1.64)^-2 ; Nu=... ; h=Nu*k/D, k=0.08")
print("  q_rad unchanged (T-dependent only).  q_conv=h*(Tg-Tw), Tg=1800, Tw=1000")
print("  Q = q_total * A,  A=pi*0.08*0.20 = 0.0503 m^2")
print("=" * 74)
D = 0.08
L = 0.20
mu = 4.0e-5
Pr = 0.7
k_gas = 0.08
A = math.pi * D * L
Re = 4.0 * MDOT_M1 / (math.pi * D * mu)
f = (0.79 * math.log(Re) - 1.64) ** -2
Nu = (f / 8.0) * (Re - 1000.0) * Pr / (1.0 + 12.7 * math.sqrt(f / 8.0) * (Pr ** (2.0 / 3.0) - 1.0))
h = Nu * k_gas / D
q_rad = 0.25 * 5.67e-8 * (1800.0 ** 4 - 1000.0 ** 4)
q_conv = h * (1800.0 - 1000.0)
q_tot = q_rad + q_conv
Q = q_tot * A
P_AB = mdot_fuel * LHV
print(f"  Re liner        = {Re:8.0f}")
print(f"  f               = {f:.4f}    Nu = {Nu:.0f}    h = {h:.0f} W/m2K")
print(f"  q_conv          = {q_conv/1000.0:6.1f} kW/m2   (was 318 at mdot 0.69)")
print(f"  q_rad           = {q_rad/1000.0:6.1f} kW/m2   (unchanged)")
print(f"  q_total         = {q_tot/1000.0:6.1f} kW/m2   (was 453)")
print(f"  Q total         = {Q/1000.0:6.1f} kW   (was 22.8)")
print(f"  Q / AB power    = {Q/P_AB:6.1%}   (AB power = {P_AB/1000.0:.0f} kW)")

print()
print("  Cooling bleed (film): 2.5% of core ->")
m_cool_film = 0.025 * MDOT_M1
m_hole = 2.47e-4                       # per 1mm hole, choked (17 sec 1c)
n_holes = m_cool_film / m_hole
print(f"    m_cool_film = {m_cool_film:.4f} kg/s   holes @2.47e-4 = {n_holes:.0f}  (was 65)")
print(f"    q_conv-scaled (Re^0.8 = {Re**0.8/(274500**0.8):.2f}) -> {0.0173*(Re**0.8/(274500**0.8)):.4f} kg/s -> {0.0173*(Re**0.8/(274500**0.8))/m_hole:.0f} holes")

print()
print("  Annulus (shell cooling): 2.3% of core, D_h = 8 mm, A_ann = 0.00108 m2")
m_cool_ann = 0.023 * MDOT_M1
rho_cool = 0.574                        # 423 K, 0.7 bar (17 sec 1e)
V_ann = m_cool_ann / (rho_cool * 0.00108)
Dh = 0.008
Re_ann = rho_cool * V_ann * Dh / 2.5e-5
Nu_ann = 0.023 * Re_ann ** 0.8 * 0.7 ** 0.4
h_ann = Nu_ann * 0.04 / Dh
print(f"    m_cool_ann  = {m_cool_ann:.4f} kg/s   V = {V_ann:.1f} m/s")
print(f"    Re_ann      = {Re_ann:.0f}   Nu_ann = {Nu_ann:.0f}   h_ann = {h_ann:.0f} W/m2K")

# annulus exit temp by LMTD iteration (17 sec 1e method, corrected inputs)
m_cool = m_cool_ann
h_a = h_ann
A_shell = 0.065          # annulus-side shell area (17 sec 1e used 0.065 m2)
cp_a = 1000.0
T_in = 423.0
T_liner_o = 1100.0
T_out = 600.0
for i in range(50):
    dT1 = T_liner_o - T_in
    dT2 = T_liner_o - T_out
    dTlm = (dT1 - dT2) / math.log(dT1 / dT2)
    Q = h_a * A_shell * dTlm
    Qabs = m_cool * cp_a * (T_out - T_in)
    err = Q - Qabs
    if abs(err) < 1.0:
        break
    T_out += 0.5 * err / (m_cool * cp_a)
print(f"    Q through shell ~ {Q:.0f} W -> T_cool_out ~ {T_out:.0f} K ({T_out-273:.0f} C)")

print()
print("  Ram scoop (17 sec 2c re-derived): mdot_cool = 3% of core")
rho = 0.905
Cp_scoop = 0.8
m_scoop = 0.03 * MDOT_M1
A_scoop = m_scoop / (rho * VINF * Cp_scoop)
d_scoop = math.sqrt(4.0 * A_scoop / math.pi) * 1000.0
print(f"    m_scoop = {m_scoop:.3f} kg/s  A = {A_scoop*1e6:.2f} e-6 m2  d_eq = {d_scoop:.1f} mm")

print()
print("=" * 74)
print("SANITY: fuel-flow cross-check vs 15 pump curve (Speck ZY-4S-12V)")
print("  req 27.3 g/s at M1; pump 4 bar -> 44 g/s, 6 bar -> 34 g/s (15:90-91)")
print("=" * 74)
print(f"  margin at 6 bar: {34.0/27.3:.2f}x   at 4 bar: {44.0/27.3:.2f}x")
