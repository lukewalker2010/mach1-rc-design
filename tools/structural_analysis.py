#!/usr/bin/env python3
"""Corrected preliminary half-wing equilibrium; see 20 and 25 for open limits.

Run: python3 tools/structural_analysis.py. No strength or flight-release claim.
"""
if __package__:
    from .design_checks import mass_rows, mass_state, semispan_load
else:
    from design_checks import mass_rows, mass_state, semispan_load


def main():
    rows = mass_rows()
    print("MASS / CG (read directly from 18 §3.4 component rows)")
    for fraction in (1, 0.5, 0):
        state = mass_state(rows, fraction)
        cg = state["cg_m"]
        print(f"  fuel {fraction:.0%}: mass {state['mass_kg']:.2f} kg, moment {state['moment_kg_m']:.4f} kg.m, "
              f"CG {cg:.4f} m; band {'PASS' if 0.955 <= cg <= 0.995 else 'FAIL'}")
    print("  Static margin UNVERIFIED: no validated full-aircraft neutral point.")
    mass = mass_state(rows)["mass_kg"]
    print("HALF-WING CENTRELINE LOADS (chord-proportional lift, no tail trim/inertial relief)")
    for n in (4, 6, 9):
        load = semispan_load(mass, n)
        print(f"  {n}g: shear {load['shear_n']:.1f} N, moment {load['moment_nm']:.2f} N.m")
    print("SPAR FIT (20 proposed 5 x 0.2 mm caps, 50 mm width, 7 mm centroid spacing)")
    chord, width, skin, cap = 210.0, 50.0, 0.5, 1.0
    # Conservative constant-depth cap: check both chordwise edges, not just 30%.
    edges = (0.3 - width / (2 * chord), 0.3 + width / (2 * chord))
    edge_depth = min(0.04 * chord * 4 * u * (1 - u) for u in edges)
    separation = edge_depth - 2 * skin - cap
    print(f"  centre depth {0.04 * chord * 4 * 0.3 * 0.7:.3f} mm; min cap-edge depth {edge_depth:.3f} mm")
    print(f"  available centroid separation <= {separation:.3f} mm: FAIL 7 mm proposal")
    print("  Strength UNVERIFIED: establish a fitting tapered spar, laminate allowables,")
    print("  web/cap buckling, bonded joints, combined loads and physical proof evidence.")
    print("THERMAL: k*dT/t is a heat flux at assumed temperatures, not a cold-face temperature solution.")


if __name__ == "__main__":
    main()
