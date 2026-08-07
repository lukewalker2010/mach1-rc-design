#!/usr/bin/env python3
"""Aero re-run for re-baselined Mach-1 RC (18 §3). Drag buildup + stability.
Run: /tmp/opencode/cq312/bin/python aero_v2.py  (or python3)
"""
import math

G = 1.4
R = 287.0
# Reference geometry (18 §3)
S_front = math.pi * 0.0925 ** 2      # 0.0269 m2
BODY_L = 2.6
BODY_R = 0.0925
S_w = 0.14                            # wing planform area
SWET_BODY = 0.78                      # m2, shape-factor approx
MTOW = 13.60
W = MTOW * 9.81

def atmos(alt_m):
    # ISA troposphere
    T = 288.15 - 0.0065 * alt_m
    p = 101325.0 * (1 - 0.0065 * alt_m / 288.15) ** 5.2561
    rho = p / (R * T)
    return T, p, rho

def drag(M, alt_m):
    T, p, rho = atmos(alt_m)
    a = math.sqrt(G * R * T)
    V = M * a
    q = 0.5 * rho * V * V
    mu = 1.458e-6 * T ** 1.5 / (T + 110.4)
    # Body
    cd_wave = (9 * math.pi ** 2 / 2) * (BODY_R / BODY_L) ** 2   # Sears-Haack
    Re_b = rho * V * BODY_L / mu
    Cf_b = 0.074 / Re_b ** 0.2
    # Wing
    Re_w = rho * V * (0.156) / mu          # MAC 0.156
    Cf_w = 0.074 / Re_w ** 0.2
    # Wing wave drag (wing-area ref), subsonic LE at M_n<1 (Lambda=30 deg)
    Mn = M * math.cos(math.radians(30))
    cd_wing_wave = max(0.004, 0.012 * (Mn - 0.9) / 0.1)     # rise near M_n~1, clamped >= subsonic floor
    # transonic factor on body wave + wing wave
    def ft(M):
        if M <= 0.9: return 1.0
        if M < 1.04: return 1.0 + 0.38 * (M - 0.9) / 0.14     # rise
        if M < 1.25: return 1.38 - 0.38 * (M - 1.04) / 0.21   # decay
        return 1.0
    D_wave_body = cd_wave * ft(M) * q * S_front
    D_fric_body = Cf_b * q * SWET_BODY
    D_fric_wing = Cf_w * q * 2 * S_w
    D_wave_wing = cd_wing_wave * q * S_w
    D_tail = 0.25 * (D_fric_wing + D_wave_wing)
    D_intake = 0.0085 * q * S_front
    D_base = 0.005 * q * S_front
    D_excr = 0.006 * q * S_front
    # induced at CL
    CL = W / (q * S_w)
    AR = 0.95 ** 2 / S_w
    D_ind = CL ** 2 / (math.pi * AR * 0.85) * q * S_w
    D = D_wave_body + D_fric_body + D_fric_wing + D_wave_wing + D_tail + D_intake + D_base + D_excr + D_ind
    return dict(M=M, alt=alt_m, q=q, Cd_body_wave=cd_wave, ft=ft(M), D_wave_body=D_wave_body,
                D_fric_body=D_fric_body, D_fric_wing=D_fric_wing, D_wave_wing=D_wave_wing,
                D_tail=D_tail, D_intake=D_intake, D_base=D_base, D_excr=D_excr, D_ind=D_ind, D_total=D,
                CL=CL, Re_w=Re_w, Re_b=Re_b)

print(f"{'M':>5} {'alt':>6} {'q':>7} {'waveB':>7} {'fricB':>7} {'fricW':>7} {'waveW':>7} {'tail':>6} "
      f"{'int':>6} {'base':>6} {'excr':>6} {'ind':>6} {'TOTAL':>7}")
for alt in [3048, 3658]:
    for M in [0.85, 0.95, 1.00, 1.05, 1.10, 1.20]:
        d = drag(M, alt)
        print(f"{M:5.2f} {alt:6.0f} {d['q']:7.0f} {d['D_wave_body']:7.1f} {d['D_fric_body']:7.1f} "
              f"{d['D_fric_wing']:7.1f} {d['D_wave_wing']:7.1f} {d['D_tail']:6.1f} {d['D_intake']:6.1f} "
              f"{d['D_base']:6.1f} {d['D_excr']:6.1f} {d['D_ind']:6.1f} {d['D_total']:7.1f}")
print()
d = drag(1.05, 3048)
print(f"M1.05/10kft hump drag = {d['D_total']:.0f} N  (contract <=430)  -> {'PASS' if d['D_total']<=430 else 'FAIL'}")
d = drag(1.10, 3048)
print(f"M1.10/10kft sustain drag = {d['D_total']:.0f} N  (wet thrust 451-497) -> {'PASS' if d['D_total']<=451 else 'CHECK'}")
d = drag(1.05, 3658)
print(f"M1.05/12kft hump drag = {d['D_total']:.0f} N")
print(f"Re_w @M1/10kft = {drag(1.0,3048)['Re_w']/1e6:.2f}e6 ; Re_b = {drag(1.0,3048)['Re_b']/1e6:.1f}e6")
