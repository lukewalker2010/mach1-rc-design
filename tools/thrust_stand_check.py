"""Thrust stand sanity checks: load cell, rails, frame, engine mount bolts, rod-ends, resonance, DAQ rate.

Numbers referenced in 24_thrust_stand.md. Authority inputs: 21 §5-6 (sensor table, gate
F_s >= 700 N, design 721 N), 17 §2a (M3 bolt capacity on 45 mm PCD), 18 §3.1 (engine mount ring).

Run: /tmp/opencode/cq312/bin/python tools/thrust_stand_check.py
"""
import math

print("=== LOAD CELL (T-1) ===")
F_gate = 700.0          # N static wet gate (21 §6)
F_design = 721.0        # N design point (21 §6)
cell_cap = 100.0 * 9.81  # 100 kg S-type -> 981 N
print(f"  gate {F_gate:.0f} N, design {F_design:.0f} N, cell 100 kg = {cell_cap:.0f} N")
print(f"  margin gate = {cell_cap/F_gate:.2f}x   margin design = {cell_cap/F_design:.2f}x")

print("\n=== LINEAR RAILS (2x SBR12, 4 blocks) ===")
m_engine = 4.9 + 0.97     # P550-PRO + AB (18 §3.1/3.4, 17 §2d)
m_carriage = 2.0          # plate + engine adapter estimate
m_total = m_engine + m_carriage
F_rail = m_total * 9.81 * 5    # 5g dynamic (17 §2a vibration case)
print(f"  static {m_total:.1f} kg, 5g dynamic {F_rail:.0f} N")
print(f"  per rail {F_rail/2:.0f} N (~{F_rail/2/9.81:.1f} kg) - SBR12 static rating >> 50 kg/block: OK")

print("\n=== FRAME (40x40 T-slot, 600 mm span) ===")
E = 70e9
I = 40e-3 * 40e-3**3 / 12
L = 0.6
w = 400.0                      # worst-case mid-span load, N
d = w * L**3 / (48 * E * I) * 1e3
print(f"  mid deflection {d:.3f} mm under {w:.0f} N -> {'OK' if d < 1 else 'CHECK'} (<1 mm)")

print("\n=== ENGINE MOUNT BOLTS (4x M3 A2-70, 45 mm PCD) ===")
n = 4
F_bolt = F_gate / n
cap_shear = 2113.0             # M3 A2-70 shear capacity, N (17 §2a)
print(f"  shear per bolt at gate {F_bolt:.0f} N vs {cap_shear:.0f} N cap = {cap_shear/F_bolt:.1f}x")
M = m_engine * 9.81 * 0.35     # engine+AB bending at flange, 0.35 m cantilever (17 §2a)
r = 45e-3 / 2
F_tens = M / (n * r)
print(f"  bending {M:.1f} Nm -> tension per bolt {F_tens:.0f} N = {cap_shear/F_tens:.1f}x")

print("\n=== ROD-ENDS (M6, load-cell axial path) ===")
F_rod = F_gate * 1.25          # 25% margin requirement
cap_rod = 1500.0               # conservative M6 clevis rating (typically 1.5-3 kN)
print(f"  axial {F_rod:.0f} N req vs {cap_rod:.0f} N rating = {cap_rod/F_rod:.1f}x")

print("\n=== STRUCTURAL RESONANCE (engine + carriage on rails, cell in line) ===")
k_cell = 1.0e7                 # S-type 100 kg axial stiffness ~10 MN/m (est)
f = 1 / (2 * math.pi) * math.sqrt(k_cell / m_total)
print(f"  f_n = {f:.0f} Hz (100 kg cell, {m_total:.1f} kg) - above 100 Hz control band")
print(f"  note: engine spool resonance / stand modes must be confirmed in Phase 0.2 tap test")

print("\n=== DAQ RATE BUDGET (ADS1256 24-bit, 30 kSPS chip) ===")
n_ch = 8                        # thrust + gravimetric + flow + 5x pressure analog if used
rate = 500.0
print(f"  {n_ch} ch x {rate:.0f} Hz = {n_ch*rate:.0f} SPS << 30,000 SPS: OK")
print(f"  F_s logged at 500 Hz on its own diff channel (21 §5 Phase 5 requirement)")

print("\n=== THERMOCOUPLE RATE (MAX31856, 24-bit, 60 Hz reject) ===")
t_conv = 0.0166                 # 16.6 ms with 60 Hz rejection
print(f"  {1/t_conv:.0f} Hz/channel -> T5/T7 log at ~60 Hz each on 6 channels (21 §5 needs >=100 Hz)")
print(f"  NOTE: 100 Hz spec on TCs is above physical probe response (R-type tau ~1-2 s);")
print(f"  flagged as deviation request in 24 §10; NI 9214 class is the compliant alternative")
