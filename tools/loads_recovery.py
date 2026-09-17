#!/usr/bin/env python3
"""R04/R06/R14 spanwise loads, recovery energy and aeroelastic screening.

    Numerical screening tables in 30_structure_recovery.md use this script.
Python standard library only; run:

    python3 tools/loads_recovery.py
    python3 -m unittest tests.test_loads_recovery

Deliberate scope limits (screening, never a release claim):
  * no composite allowable is selected - cap area is reported /sigma so the
    owning engineer applies sourced laminate allowables with knockdowns;
  * no CLmax is measured - stall/required-CL are functions of an input CLmax;
  * no chute opening-shock factor is invented (08:267 used 1.2-1.5 without a
    source); only steady-state drag is computed;
  * torsion is returned only when the section input data (AC/SC positions,
    Cm), which do not exist for the current 4% biconvex, are supplied;
  * no flutter clearance - R14 is an acceptance matrix and dimensional
    sanity of candidate stiffness/mass, not a correlated flutter analysis.
"""
import math
import sys
from pathlib import Path

G = 9.81
RHO_SL = 1.225  # kg/m3, ISA sea level


def _finite(name, value, minimum=0.0, inclusive=False):
    if not math.isfinite(value) or (value < minimum if inclusive else value <= minimum):
        raise ValueError(f"{name} must be finite and {'>=' if inclusive else '>'} {minimum}")


def _linspace(a, b, n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("num must be >= 2")
    h = (b - a) / (n - 1)
    return [a + i * h for i in range(n)]


_LOAD_SCHEMES = ("uniform", "triangular", "chord")


# --------------------------------------------------------------------------
# R04: planform, spanwise loads, cap fit screening
# --------------------------------------------------------------------------
def wing_planform(span=0.95, area=0.14, taper=0.4, root_cut_m=None):
    """Centreline trapezoid derived from b, S, lambda (18 sect.3.2).

    The 'root cut at the fuselage side' defines where the cantilever wing
    structure begins: y0 = 0.185/2 m (185 mm max fuselage OD, 18 sect.3.1).
    During the 2026-09-16 readiness review this convention was left open (R03).
    """
    _finite("span", span); _finite("area", area); _finite("taper", taper, inclusive=True)
    if not 0 <= taper <= 1:
        raise ValueError("taper must be in [0, 1]")
    c_root = 2 * area / (span * (1 + taper))
    c_tip = taper * c_root
    if root_cut_m is None:
        root_cut_m = 0.185 / 2
    half = span / 2
    if not 0 <= root_cut_m < half:
        raise ValueError(f"root cut {root_cut_m} m must be in [0, {half})")
    mac = (2 / 3) * c_root * (1 + taper + taper ** 2) / (1 + taper)
    return {"c_root_m": c_root, "c_tip_m": c_tip, "mac_m": mac,
            "avg_chord_m": area / span, "semi_m": half, "root_cut_m": root_cut_m}


def chord_at(y, planform):
    """Linear-rule chord (m) at span station y (inboard origin, aft +x up +z)."""
    c0, ct, half = planform["c_root_m"], planform["c_tip_m"], planform["semi_m"]
    if not 0 <= y <= half:
        raise ValueError("station outside half-span")
    return c0 + (ct - c0) * y / half


def _shape_g(y, planform, scheme):
    """Half-span shape function, integral over [0, half] = 1."""
    c_r, ct, half = planform["c_root_m"], planform["c_tip_m"], planform["semi_m"]
    if scheme == "uniform":
        return 1.0 / half
    if scheme == "triangular":
        return 2.0 / half * (1 - y / half)
    if scheme == "chord":
        return 2.0 * chord_at(y, planform) / planform["avg_chord_m"] / span_of(planform)
    raise ValueError(f"unknown load scheme {scheme!r}; use {_LOAD_SCHEMES}")


def span_of(planform):
    return 2 * planform["semi_m"]


def _shape_check(planform, scheme, num=20001):
    y = _linspace(0, planform["semi_m"], num)
    g = [_shape_g(yi, planform, scheme) for yi in y]
    total = sum((g[i] + g[i + 1]) / 2 * (y[i + 1] - y[i]) for i in range(num - 1))
    if not math.isclose(total, 1.0, rel_tol=1e-6):
        raise RuntimeError(f"{scheme} shape not normalised: {total}")


def analytic_semispan(mass_kg, n, planform, scheme, y0=0.0, tail_download_n=0.0, wing_mass_kg=0.0):
    """Closed-form root shear/moment for the analytic schemes (like-lift relief).

    Drop load factor, W = n*m*g. Required wing lift = n*m*g + tail_download_n
    (tail_download_n > 0 = stabiliser download, which the wing must carry; the
    symmetric tail load splits into the two wing-root joints). Symmetric wing
    inertial relief = n*g*m_w/2 per half-wing, distributed like the lift scheme.
    """
    _finite("mass_kg", mass_kg)
    _finite("n", n)
    _finite("wing_mass_kg", wing_mass_kg, inclusive=True)
    if wing_mass_kg > mass_kg:
        raise ValueError("wing mass exceeds aircraft mass")
    if not math.isfinite(tail_download_n):
        raise ValueError("tail_download_n must be finite")
    half = planform["semi_m"]
    c_r = planform["c_root_m"]
    taper = planform["c_tip_m"] / c_r
    if not 0 <= y0 < half:
        raise ValueError("y0 outside half-span")
    lift_half = (n * mass_kg * G + tail_download_n) / 2.0
    relief_half = n * G * wing_mass_kg / 2.0

    if scheme == "chord":
        slope = c_r * (1 - taper) / half
        area_out = c_r * (half - y0) - slope * (half ** 2 - y0 ** 2) / 2
        frac = area_out / (planform["avg_chord_m"] * span_of(planform) / 2)
        num = (c_r * (half ** 2 - y0 ** 2) / 2 - slope * (half ** 3 - y0 ** 3) / 3
               - c_r * y0 * (half - y0) + slope * y0 * (half ** 2 - y0 ** 2) / 2)
        arm = num / area_out
    elif scheme == "uniform":
        frac = (half - y0) / half
        arm = (half - y0) / 2
    elif scheme == "triangular":
        # g(y) = (2/L)(1 - y/L), area on [y0, L] = (L-y0)^2/L^2
        frac = (half - y0) ** 2 / half ** 2
        arm = (half - y0) / 3
    else:
        raise ValueError(f"unknown load scheme {scheme!r}; use {_LOAD_SCHEMES}")
    net = (lift_half - relief_half) * frac
    return {"shear_n": net, "moment_nm": net * arm, "arm_m": arm,
            "fraction_outboard": frac, "lift_half_n": lift_half, "relief_half_n": relief_half}


def beam_loads(mass_kg, n, planform, scheme="chord", tail_download_n=0.0,
               wing_mass_kg=0.0, relief_scheme=None, num=1201):
    """Numeric spanwise shear/moment for a cantilever from the root cut to tip.

    Sign convention: lift up (+) and inertial relief down (-). V(y) > 0 carries
    the outboard load inboard; M(y) = sum of outboard force x arm about y
    (positive root bending from up-lift). dM/dy = -V. A dense grid plus the
    analytic closed-form test prove force and first-moment conservation.
    """
    # Validate even when a different relief distribution bypasses the final check.
    analytic_semispan(mass_kg, n, planform, scheme, planform["root_cut_m"],
                      tail_download_n, wing_mass_kg)
    _shape_check(planform, scheme)
    if relief_scheme is None or relief_scheme == scheme:
        relief_scheme = scheme
    _shape_check(planform, relief_scheme)
    y0 = planform["root_cut_m"]
    y = _linspace(y0, planform["semi_m"], num)
    lift_half = (n * mass_kg * G + tail_download_n) / 2.0
    relief_half = n * G * wing_mass_kg / 2.0
    l = [lift_half * _shape_g(yi, planform, scheme) - relief_half * _shape_g(yi, planform, relief_scheme)
         for yi in y]
    shear, moment = [0.0] * num, [0.0] * num
    f_sum = m_sum = 0.0
    for j in range(num - 2, -1, -1):
        dyj = y[j + 1] - y[j]
        fseg = (l[j] + l[j + 1]) / 2 * dyj
        f_sum += fseg
        # Exact first moment of the linearly interpolated distributed load.
        m_sum += y[j]*fseg + dyj**2*(l[j]/6 + l[j+1]/3)
        shear[j] = f_sum
        moment[j] = m_sum - y[j] * f_sum
    if relief_scheme == scheme:
        expected = analytic_semispan(mass_kg, n, planform, scheme, y0,
                                     tail_download_n, wing_mass_kg)
        resid_s = shear[0] - expected["shear_n"]
    else:
        expected, resid_s = None, float("nan")
    return {"y": y, "shear": shear, "moment": moment,
            "root_shear_n": shear[0], "root_moment_nm": moment[0],
            "root_moment_analytic_nm": expected["moment_nm"] if expected else float("nan"),
            "shear_residual_vs_analytic": resid_s, "expected": expected}


def section_depth_mm(u, chord_mm, t_ratio=0.04):
    """Parabolic biconvex thickness law used by the rib generator (20 sect.3;
    depth(u) = t_ratio * c * 4u(1-u); max thickness at u=0.5)."""
    if not 0 <= u <= 1:
        raise ValueError("u must be in [0, 1]")
    _finite("chord_mm", chord_mm); _finite("t_ratio", t_ratio)
    return t_ratio * chord_mm * 4 * u * (1 - u)


def cap_centroid_separation_mm(u_center, cap_width_mm, chord_mm, t_ratio=0.04,
                               skin_mm=0.5, bond_mm=0.0, cap_thick_mm=1.0):
    """Maximum available upper/lower cap-centroid separation across the finite
    cap band, allowing one skin offset per face plus a bond/adhesive allowance.
    Uses the minimal section depth across the cap's chordwise footprint
    (conservative because the cap is flat across a finite width)."""
    for name, v in (("u_center", u_center), ("cap_width_mm", cap_width_mm), ("chord_mm", chord_mm),
                    ("skin_mm", skin_mm), ("bond_mm", bond_mm), ("cap_thick_mm", cap_thick_mm)):
        _finite(name, v, inclusive=True)
    _finite("chord_mm", chord_mm)
    _finite("cap_width_mm", cap_width_mm)
    if not 0 <= u_center <= 1 or cap_width_mm > chord_mm:
        raise ValueError("cap must lie within the chord")
    u_lo = u_center - cap_width_mm / 2 / chord_mm
    u_hi = u_center + cap_width_mm / 2 / chord_mm
    if u_lo < 0 or u_hi > 1:
        raise ValueError("cap footprint outside chord")
    d_outer = min(section_depth_mm(u_lo, chord_mm, t_ratio),
                  section_depth_mm(u_hi, chord_mm, t_ratio))
    sep = d_outer - 2 * (skin_mm + bond_mm) - cap_thick_mm
    return {"outer_depth_mm": d_outer, "centre_depth_mm": section_depth_mm(u_center, chord_mm, t_ratio),
            "u_lo": u_lo, "u_hi": u_hi, "separation_mm": sep}


def required_cap_area_mm2(moment_nm, separation_mm, allowable_mpa):
    """Required area of EACH cap A = |M|/(d * sigma) in mm^2.

    sigma is an INPUT: no laminate allowable is selected here (matrix-dominated
    compression with manufacture/environmental knockdowns is owned by E1 from
    sourced data). Units: M[N.mm] / (d[mm] * sigma[N/mm^2])."""
    if not math.isfinite(moment_nm):
        raise ValueError("moment must be finite")
    _finite("separation_mm", separation_mm)
    _finite("allowable_mpa", allowable_mpa)
    if separation_mm <= 0:
        raise ValueError("separation must be > 0 mm")
    return abs(moment_nm) * 1e3 / (separation_mm * allowable_mpa)


def load_case_discrepancy(mass_kg=13.6, legacy_mass_kg=12.2, span=0.95, taper=0.4, area=0.14):
    """4g/6g envelope vs the legacy 9g root-bending contract (18 sect.3.2,
    INTERFACES sect.3: 'Root bending (9g equiv.) ~100 N.m')."""
    pf = wing_planform(span, area, taper, root_cut_m=0.0)
    rows = []
    for n in (4, 6, 9):
        rows.append((n, analytic_semispan(mass_kg, n, pf, "chord")))
    legacy9 = analytic_semispan(legacy_mass_kg, 9, pf, "chord")
    rows.append(("9g legacy %g kg" % legacy_mass_kg, legacy9))
    return rows


# --------------------------------------------------------------------------
# R06: recovery - required CL, stall, wheels/energy, chute
# --------------------------------------------------------------------------
def isa_density(alt_m):
    """ISA troposphere density; only valid < 11 km. 18 sect.2.1 annotates
    rho 1.225 (SL) and 0.905 (10 kft)."""
    _finite("alt_m", alt_m, inclusive=True)
    if alt_m >= 11000:
        raise ValueError("troposphere model requires altitude < 11000 m")
    T = 288.15 - 0.0065 * alt_m
    p = 101325.0 * (1 - 0.0065 * alt_m / 288.15) ** 5.2561
    return p / (287.05 * T)


def required_cl(mass_kg, speed_m_s, rho=RHO_SL, area=0.14):
    for name, v in (("mass_kg", mass_kg), ("speed", speed_m_s), ("rho", rho), ("area", area)):
        _finite(name, v)
    return 2 * mass_kg * G / (rho * speed_m_s ** 2 * area)


def stall_speed(mass_kg, clmax, rho=RHO_SL, area=0.14):
    """1-g level-flight stall speed for an input CLmax (no polar is measured)."""
    for name, v in (("mass_kg", mass_kg), ("clmax", clmax), ("rho", rho), ("area", area)):
        _finite(name, v)
    return math.sqrt(2 * mass_kg * G / (rho * clmax * area))


def wheel_rev_per_s(ground_speed_m_s, wheel_dia_m):
    _finite("speed", ground_speed_m_s, inclusive=True)
    _finite("wheel_dia_m", wheel_dia_m)
    return ground_speed_m_s / (math.pi * wheel_dia_m)


def kinetic_energy(mass_kg, speed_m_s):
    _finite("mass_kg", mass_kg, inclusive=True); _finite("speed_m_s", speed_m_s, inclusive=True)
    return 0.5 * mass_kg * speed_m_s ** 2


def stop_distance(speed_m_s, decel_m_s2=0.4 * G):
    """Constant-deceleration stop distance s = V^2/(2a)."""
    _finite("decel_m_s2", decel_m_s2)
    _finite("speed", speed_m_s, inclusive=True)
    return speed_m_s ** 2 / (2 * decel_m_s2)


def skid_stop_with_drogue(mass_kg, speed0_m_s, mu, rho=RHO_SL, cd=0.75, s=0.283,
                          g=G, chute_on=True):
    """Skid stop distance with rolling/friction drag plus steady chute drag.

    Closed form of m V dV/dx = -(mu m g + 0.5 rho V^2 cd s):
        V(x)^2 = (V0^2 + 2 mu g/beta) exp(-beta x) - 2 mu g/beta,
    solved for V=0. beta = rho cd s / m. No opening-shock transient is added.
    """
    for name, v in (("mass_kg", mass_kg), ("mu", mu), ("rho", rho), ("cd", cd), ("s", s), ("g", g)):
        _finite(name, v)
    _finite("speed", speed0_m_s, inclusive=True)
    if not 0 <= mu:
        raise ValueError("mu must be >= 0")
    if not chute_on:
        return speed0_m_s ** 2 / (2 * mu * g)
    beta = rho * cd * s / mass_kg
    G0 = 2 * mu * g / beta
    if speed0_m_s ** 2 <= 0:
        return 0.0
    return math.log1p(speed0_m_s ** 2 / G0) / beta


def chute_steady_drag(speed_m_s, rho=RHO_SL, cd=0.75, s=0.283):
    """Steady-state chute drag D = 0.5 rho V^2 cd S. NO opening-shock factor;
    real opening transients must be measured (drop test), not multiplied in."""
    _finite("speed_m_s", speed_m_s); _finite("rho", rho); _finite("cd", cd); _finite("s", s)
    return 0.5 * rho * speed_m_s ** 2 * cd * s


def chute_gate_speed(load_n, rho=RHO_SL, cd=0.75, s=0.283):
    """Speed at which steady-state chute drag equals the input load budget."""
    for name, v in (("load_n", load_n), ("rho", rho), ("cd", cd), ("s", s)):
        _finite(name, v)
    return math.sqrt(2 * load_n / (rho * cd * s))


# --------------------------------------------------------------------------
# R14: aeroelastic acceptance inputs - dimensional sanity, not clearance
# --------------------------------------------------------------------------
def cantilever_bending_freq(mass_kg, semi_m, EI):
    """Rayleigh/exact uniform-cantilever first bending mode
    f = (1.8751^2/2pi) sqrt(EI / (mbar L^4)), mbar = mass per half-span.
    Screening sanity for the mass/stiffness model that must be GVT-matched."""
    for name, v in (("mass_kg", mass_kg), ("semi_m", semi_m), ("EI", EI)):
        _finite(name, v)
    mbar = mass_kg / semi_m
    return 1.8751 ** 2 / (2 * math.pi) * math.sqrt(EI / (mbar * semi_m ** 4))


def bending_ei_for_freq(freq_hz, mass_kg, semi_m):
    for name, v in (("freq_hz", freq_hz), ("mass_kg", mass_kg), ("semi_m", semi_m)):
        _finite(name, v)
    mbar = mass_kg / semi_m
    return (freq_hz * 2 * math.pi / 1.8751 ** 2) ** 2 * mbar * semi_m ** 4


def reduced_frequency(freq_hz, chord_m, speed_m_s):
    """k = omega*c/(2V). Small k alone establishes no flutter approximation."""
    _finite("freq_hz", freq_hz); _finite("chord_m", chord_m); _finite("speed_m_s", speed_m_s)
    return math.pi * freq_hz * chord_m / speed_m_s


def torque_per_span(lift_per_len, q, chord_m, x_ac_c, x_sc_c, cm):
    """Section torque about the (candidate) shear centre.
    Nose-up positive: t(y) = lift_per_len*(x_sc - x_ac) + cm*q*c^2.
    With +X aft, lift aft of the shear centre is nose-down. All inputs (AC/SC
    fractions, Cm) are UNKNOWN for the 4% biconvex and must be measured or
    taken from a suitable 2-D source before a torsion number is published."""
    for value in (lift_per_len, x_ac_c, x_sc_c, cm):
        if not math.isfinite(value):
            raise ValueError("section inputs must be finite")
    _finite("q", q, inclusive=True); _finite("chord", chord_m)
    return lift_per_len * (x_sc_c - x_ac_c) * chord_m + cm * q * chord_m ** 2


# --------------------------------------------------------------------------
# Script output (drives 30_structure_recovery.md)
# --------------------------------------------------------------------------
def main():
    try:
        from design_checks import mass_rows, mass_state
    except ImportError:
        from .design_checks import mass_rows, mass_state

    rows = mass_rows()
    full = mass_state(rows)
    empty = mass_state(rows, 0.0)

    print("=" * 78)
    print("Mach-1 RC review: R04 (spanwise loads / spar fit / load contract),")
    print("R06 (recovery), R14 (aeroelastic acceptance). Screening, not release.")
    print("=" * 78)

    pf = wing_planform()                       # b .95, S .14, taper .4
    print("\nR04 PLANFORM (centreline trapezoid, 18 sect.3.2)")
    print(f"  c_root={pf['c_root_m']*1e3:.1f} mm  c_tip={pf['c_tip_m']*1e3:.1f} mm  "
          f"MAC={pf['mac_m']*1e3:.1f} mm  avg chord={pf['avg_chord_m']*1e3:.1f} mm")
    print(f"  fuselage-side root cut y0={pf['root_cut_m']*1e3:.1f} mm (185 mm fuselage OD)")
    for u, frac in ((0.180952, "50 mm cap fwd edge"), (0.30, "cap centre"), (0.419048, "50 mm cap aft edge")):
        print(f"  biconvex depth at u={u:.3f} ({frac}): {section_depth_mm(u, 210.0):.3f} mm")

    print("\nR04 HALF-WING CENTRELINE LOADS (closed form, y0 = 0, no relief/tail)")
    for n, load in ((4, analytic_semispan(full["mass_kg"], 4, pf, "chord")),
                    (6, analytic_semispan(full["mass_kg"], 6, pf, "chord")),
                    (9, analytic_semispan(full["mass_kg"], 9, pf, "chord"))):
        print(f"  {n}g: shear {load['shear_n']:7.1f} N  moment {load['moment_nm']:6.2f} N.m"
              f"  (arm {load['arm_m']*1e3:.1f} mm)")

    print("\nR04 FUSELAGE-SIDE CUT (y0 = 92.5 mm, numeric beam, chord-proportional)")
    for n in (4, 6, 9):
        b = beam_loads(full["mass_kg"], n, pf, wing_mass_kg=0.0)
        a = analytic_semispan(full["mass_kg"], n, pf, "chord", y0=pf["root_cut_m"])
        print(f"  {n}g: shear {b['root_shear_n']:7.1f} N  moment {b['root_moment_nm']:6.2f} N.m"
              f"  (analytic {a['shear_n']:.1f}/{a['moment_nm']:.2f},"
              f" dM resid {b['root_moment_nm']-a['moment_nm']:+.1e})")
    print("  with symmetric wing inertial relief (m_w 0.50 kg, like-lift, halves each n*g*m/2):")
    b = beam_loads(full["mass_kg"], 6, pf, wing_mass_kg=0.50)
    a = analytic_semispan(full["mass_kg"], 6, pf, "chord", y0=pf["root_cut_m"], wing_mass_kg=0.50)
    print(f"  6g -0.5 kg relief: shear {b['root_shear_n']:7.1f} N"
          f" moment {b['root_moment_nm']:6.2f} N.m (analytic at same cut {a['shear_n']:.1f}/{a['moment_nm']:.2f})")
    for n in (6,):
        b = beam_loads(full["mass_kg"], n, pf, tail_download_n=50.0)
        a = analytic_semispan(full["mass_kg"], n, pf, "chord", y0=pf["root_cut_m"], tail_download_n=50.0)
        print(f"  {n}g +50 N tail download: shear {b['root_shear_n']:7.1f} N"
              f" moment {b['root_moment_nm']:6.2f} N.m (analytic at same cut {a['shear_n']:.1f}/{a['moment_nm']:.2f})")

    print("\nR04 4g/6g vs 9g CONTRACT DISCREPANCY")
    for n, load in load_case_discrepancy():
        print(f"  {n:>18}: centreline moment {load['moment_nm']:7.2f} N.m")
    m9 = [r for r in load_case_discrepancy() if isinstance(r[0], int) and r[0] == 9][0][1]
    m6 = [r for r in load_case_discrepancy() if r[0] == 6][0][1]
    print(f"  9g/13.6 kg = {m9['moment_nm']:.1f} N.m: {100*(m9['moment_nm']/100-1):+.0f}% vs the"
          f" '~100 N.m' 9g reference and {100*(m9['moment_nm']/m6['moment_nm']-1):+.0f}% above the 6g"
           f" ultimate {m6['moment_nm']:.1f} N.m (screening loads, not replacement contracts)")
    print("  -> INTERFACES sect.3 mixes a 4g/6g envelope with a legacy 9g root-bending")
    print("     contract including 150 N.m ultimate; owners must reconcile the load basis.")

    print("\nR04 SPAR CAP FIT (parabolic biconvex, root chord 210 mm)")
    for w, bond in ((50.0, 0.0), (50.0, 0.2), (35.0, 0.2)):
        s = cap_centroid_separation_mm(0.30, w, 210.0, bond_mm=bond)
        print(f"  cap {w:.0f} mm, bond {bond:.1f} mm: outer depth {s['outer_depth_mm']:.3f} mm,"
              f" available separation {s['separation_mm']:.3f} mm"
              f" ({'PASS' if s['separation_mm'] >= 7 else 'FAIL'} vs 7 mm proposal)")
    print("  required EACH-cap area A = M/(d*sigma): (sigma INPUT, no allowable selected)")
    for sigma in (400, 600, 800):
        for d in (5.056, 2.980, 2.580):
            print(f"    sigma {sigma:>3d} MPa, sep {d:5.3f} mm, M 81.48 N.m:"
                  f" A = {required_cap_area_mm2(81.48, d, sigma):5.1f} mm^2")
    print("  local buckling, web shear, bond lap and joint checks are absent: fit and")
    print("  cap-area screening only; release needs sourced allowables + proof test.")

    print("\nR06 RECOVERY (CL/stall as input-CLmax functions)")
    print(f"  masses: full {full['mass_kg']:.2f} kg, empty {empty['mass_kg']:.2f} kg (18 sect.3.4)")
    for mass, name in ((full["mass_kg"], "FULL"), (empty["mass_kg"], "EMPTY")):
        for v in (38.0, 30.0, 70.0):
            print(f"  {name:>5} CL_req @ {v:4.1f} m/s = {required_cl(mass, v):5.3f}")
    print("  stall speed vs assumed CLmax (screening; no polar measured):")
    for clmax in (0.8, 1.2, 1.6, 1.73):
        print(f"    CLmax {clmax:4.2f}: full {stall_speed(full['mass_kg'], clmax):5.2f} m/s,"
              f" empty {stall_speed(empty['mass_kg'], clmax):5.2f} m/s")
    print("  -> to flare to <=30 m/s level flight needs CLmax >= ~1.73 at full mass;")
    print("     the 38 m/s approach needs CL~1.08 while the 70 m/s dolly launch needs")
    print("     only ~0.32. Approach/launch CL ratio is ~3.4; flare/launch is ~5.4.")
    print("\nR06 WHEELS / ENERGY (legacy 08 sizes and friction, re-run on current mass)")
    print(f"  dolly wheel D=50 mm @70 m/s: {wheel_rev_per_s(70, 0.050)*60:,.0f} RPM")
    for mass, name, v in ((13.6, "aircraft full", 30), (11.98, "aircraft empty", 30),
                          (14.2, "aircraft+dolly (13.6+0.6)", 70)):
        print(f"  KE {name} @{v:>3d} m/s = {kinetic_energy(mass, v):8,.0f} J")
    print(f"  skid stop @30 m/s (mu 0.4, mass-independent): {stop_distance(30, 0.4*G):.1f} m"
          f" (requirement <=60 m)")
    print("  with 0.6 m drogue steady drag: full "
          f"{skid_stop_with_drogue(13.6, 30, 0.4):.1f} m, "
          f"empty {skid_stop_with_drogue(11.98, 30, 0.4):.1f} m")
    for mu in (0.6, 0.8):
        print(f"  skid-only @mu {mu:.1f}: full {skid_stop_with_drogue(13.6, 30, mu, chute_on=False):.1f} m")
    a_req = 70 ** 2 / (2 * (54 + 150))
    print(f"  dolly abort within roll+150 m (54+150): needs braking decel "
          f">= {a_req:.2f} m/s^2 = {a_req/G:.2f}g (friction-only mu 0.4 gives"
          f" {stop_distance(70):.0f} m; no roll/chute credit)")

    print("\nR06 CHUTE STEADY DRAG vs DEPLOY (NO opening-shock factor; 08:267 1.2-1.5 is unsourced)")
    cases = [("30 m/s SL", 30.0, RHO_SL), ("38 m/s SL", 38.0, RHO_SL), ("70 m/s SL", 70.0, RHO_SL),
             ("M0.6/10 kft", 0.6 * 328.0, isa_density(3048.0)), ("M0.6/SL", 0.6 * 340.3, RHO_SL)]
    for label, v, rho in cases:
        print(f"  {label:>14}: steady drag {chute_steady_drag(v, rho):7,.0f} N")
    print(f"  hardpoint design load ~1 kN (18 sect.5.4), weak link 100 kg = {100*G:.0f} N,"
          f" bridle 500 kg = {500*G:.0f} N")
    for budget in (600, 800, 1000):
        print(f"  deploy-speed for steady drag <= {budget} N (SL):"
              f" {chute_gate_speed(budget):5.1f} m/s")
    print("  -> Near SL, M0.6 is 204 m/s and ~5.4 kN steady drag. The 10 kft")
    print("     case is a density sensitivity, not an allowed h<20 m gate corner.")
    print("  -> Load-based gating needs an approved transient load budget; 800 N is")
    print("     only a sensitivity input, not a selected deploy limit.")

    print("\nR14 AEROELASTIC / MODEL-INPUT ACCEPTANCE (dimensional sanity, no clearance)")
    for ei, f in ((30.0, cantilever_bending_freq(0.5, 0.475, 30.0)),
                  (100.0, cantilever_bending_freq(0.5, 0.475, 100.0)),
                  (300.0, cantilever_bending_freq(0.5, 0.475, 300.0))):
        print(f"  candidate EI {ei:6.1f} N.m^2 -> first bending f1 ~= {f:5.1f} Hz"
              f" (uniform model, m=0.5 kg half 0.475 m)")
    print(f"  EI for f1 = 25 Hz: {bending_ei_for_freq(25, 0.5, 0.475):.0f} N.m^2")
    for v in (360.8, 38.0):
        print(f"  reduced frequency k(25 Hz, MAC {pf['mac_m']:.6f} m, V={v:5.1f} m/s) = "
               f"{reduced_frequency(25, pf['mac_m'], v):.4f}")
    print("  -> Small k does not establish quasi-steady flutter validity; static drag and")
    print("     'no observed oscillation' cannot clear flutter; need GVT-correlated")
    print("     unsteady analysis - evidence requirements in 30 sect.4.")

    print("\nStatus: IMPLEMENTED. All numeric values above are produced by this script.")


if __name__ == "__main__":
    main()
