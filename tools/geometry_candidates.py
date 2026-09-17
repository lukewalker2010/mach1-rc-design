"""R01–R03 analytic candidates, never released geometry (18 §§3.1–3.3).

SI except explicitly named mm inputs. Nose origin, +X aft, +Y right, +Z up.
Run python3 tools/geometry_candidates.py. No CAD environment is invoked.
"""
import math
from pathlib import Path

WING_B_M, WING_S_M2, WING_TAPER, WING_TC = 0.95, 0.14, 0.4, 0.04
WING_ROOT_CHORD_M = 2 * WING_S_M2 / (WING_B_M * (1 + WING_TAPER))
WING_TIP_CHORD_M = WING_TAPER * WING_ROOT_CHORD_M
WING_MAC_M = 2/3 * WING_ROOT_CHORD_M * (1+WING_TAPER+WING_TAPER**2)/(1+WING_TAPER)
FUSE_MAX_R_MM = FUSE_HALF_CHORD_AT_ROOT_MM = 92.5
WING_EXPOSED_HALF_SPAN_M = WING_B_M/2 - FUSE_MAX_R_MM/1000
STAB_ROOT_CHORD_MM, STAB_TIP_CHORD_MM = 90.0, 90*15/35
STAB_HALF_SPAN_MM, STAB_TC = 120.0, 0.06


def _range(value, lo, hi, name):
    if not math.isfinite(value) or not lo <= value <= hi:
        raise ValueError(f"{name} outside [{lo}, {hi}]")


def wing_chord_at_y(y_m):
    _range(y_m, 0, WING_B_M/2, "y_m")
    return WING_ROOT_CHORD_M + (WING_TIP_CHORD_M-WING_ROOT_CHORD_M)*y_m/(WING_B_M/2)


WING_EXPOSED_ROOT_CHORD_M = wing_chord_at_y(FUSE_MAX_R_MM/1000)


def wing_chord_at_exposed_y(y_exposed_mm):
    _range(y_exposed_mm, 0, WING_B_M*500-FUSE_MAX_R_MM, "exposed span")
    return wing_chord_at_y((y_exposed_mm+FUSE_MAX_R_MM)/1000)


def wing_le_station(y_m, root_le_m):
    """Absolute LE station; root LE is an unresolved owner-supplied input."""
    _range(y_m, -WING_B_M/2, WING_B_M/2, "y_m")
    _range(root_le_m, 0, 2.6, "root LE")
    return root_le_m + abs(y_m)*math.tan(math.radians(30))


def wing_area_full_trapezoidal():
    return WING_B_M*(WING_ROOT_CHORD_M+WING_TIP_CHORD_M)/2


def wing_area_exposed():
    """Constant y=92.5 mm cut surrogate, not the actual curved body intersection."""
    return WING_EXPOSED_HALF_SPAN_M*(WING_EXPOSED_ROOT_CHORD_M+WING_TIP_CHORD_M)


# Proposed knots: baseline max/waist; downstream stations and tail radius from
# fuselage_manufacturing/01 §1.5. Zero slopes and interpolation are a proposal.
FUSE_KNOTS = ((0., 0.), (.85, .0925), (1.05, .086),
              (1.39, .0925), (1.80, .0925), (2.60, .055))


def _fuse_segment(x_m):
    _range(x_m, 0, 2.6, "x_m")
    for (a, ra), (b, rb) in zip(FUSE_KNOTS, FUSE_KNOTS[1:]):
        if x_m <= b:
            return a, b, ra, rb, (x_m-a)/(b-a)


def fuse_radius(x_m):
    """C1 bounded cubic Hermite surrogate. Packaging failures remain explicit."""
    a, b, ra, rb, t = _fuse_segment(x_m)
    return ra + (rb-ra)*t*t*(3-2*t)


def fuse_radius_derivative(x_m):
    a, b, ra, rb, t = _fuse_segment(x_m)
    return (rb-ra)*6*t*(1-t)/(b-a)


def biconvex_half_thickness(chord_m, xc, t_c=WING_TC):
    """Returns the same length unit as chord_m; parabolic, not a circular arc."""
    _range(chord_m, 1e-12, math.inf, "chord")
    _range(xc, 0, 1, "x/c")
    _range(t_c, 1e-12, 1, "t/c")
    return 2*t_c*chord_m*xc*(1-xc)


def wing_spar_containment(y_exposed_mm, spar_width_mm=50.0):
    """50 mm cap at 30% chord, 0.5 mm skin, 1 mm cap: legacy fit screen.

    d_centroid = minimum outer depth - 2*skin - cap thickness. The two
    half-cap offsets sum to ONE cap thickness. 7 mm is a rejected proposal.
    """
    c = wing_chord_at_exposed_y(y_exposed_mm)*1000
    _range(spar_width_mm, 1e-12, c, "spar width")
    lo, hi = .3-spar_width_mm/(2*c), .3+spar_width_mm/(2*c)
    if lo < 0 or hi > 1:
        raise ValueError("spar footprint outside chord")
    depth = 2*min(biconvex_half_thickness(c, lo), biconvex_half_thickness(c, hi))
    sep = depth - 2*.5 - 1.
    return dict(chord_mm=c, t_max_mm=.04*c, spar_depth_mm=depth,
                available_separation_mm=sep, fits=sep >= 7,
                spar_le_xc=lo, spar_te_xc=hi)


def _hole_screen(c, tc, radius, offset):
    """Conservative full-width enclosing-rectangle screen, not a net-part check.

    Negative centre margin proves breakout. Otherwise box containment is
    sufficient but box failure is inconclusive. Offset is vertical, not normal.
    """
    h = biconvex_half_thickness(c, .3, tc)
    edge = min(biconvex_half_thickness(c, .3-radius/c, tc),
               biconvex_half_thickness(c, .3+radius/c, tc))
    margin = edge-offset-radius
    return dict(chord_mm=c, half_thickness_mm=h, hole_radius_mm=radius,
                centre_margin_mm=h-offset-radius, margin_mm=margin, fits=margin >= 0)


def wing_spar_hole_containment(y_exposed_mm):
    return _hole_screen(wing_chord_at_exposed_y(y_exposed_mm)*1000, .04, 3., .5)


def stab_chord_at_z(z_mm):
    """Legacy local span variable z; NOT aircraft +Z."""
    _range(z_mm, 0, STAB_HALF_SPAN_MM, "local span")
    return STAB_ROOT_CHORD_MM+(STAB_TIP_CHORD_MM-STAB_ROOT_CHORD_MM)*z_mm/120


def stab_spar_hole_containment(z_mm):
    """6% option, 2.5 mm spar at 30%: explicit candidate combination."""
    return _hole_screen(stab_chord_at_z(z_mm), .06, 1.25, 0.)


def engine_clearance_at_station(x_m, skin_mm=1.0, duct_wall_mm=3.0):
    """Local envelopes, not engine axial occupancy or assembly fit.

    Engine OD: 18 §3.1. Throat: I-02; wall is assumed. 1 mm skin is an
    illustrative engine-bay allowance (fuselage_manufacturing/02 §1).
    """
    _range(skin_mm, 0, FUSE_MAX_R_MM, "skin")
    _range(duct_wall_mm, 0, FUSE_MAX_R_MM, "duct wall")
    outer = fuse_radius(x_m)*1000
    inner = outer-skin_mm
    return dict(station_mm=x_m*1000, fuse_radius_mm=outer, inner_radius_mm=inner,
                fuse_clearance_mm=inner-87.5, duct_clearance_mm=inner-51.5-duct_wall_mm,
                engine_fits=inner >= 87.5, duct_fits=inner >= 51.5+duct_wall_mm)


def wing_carry_through_clearance(x_m, width_mm, height_mm, skin_mm=1.0):
    """Supply cross-section axes: I-04's 200x100 lacks a depth.

    200 mm is consistent with the 950–1150 station LENGTH, not an asserted
    transverse width. Centred rectangle corners, not independent axes, govern.
    """
    for value, name in ((width_mm, "width"), (height_mm, "height")):
        _range(value, 1e-12, math.inf, name)
    _range(skin_mm, 0, FUSE_MAX_R_MM, "skin")
    margin = fuse_radius(x_m)*1000-skin_mm-math.hypot(width_mm/2, height_mm/2)
    return dict(station_mm=x_m*1000, corner_clearance_mm=margin, fits=margin >= 0)


def export_wing_stations_csv(out_path):
    rows = ["rib,span_from_fuse_mm,y_from_centreline_mm,chord_mm,t_max_mm,le_offset_from_centreline_root_mm"]
    for i in range(6):
        s = WING_EXPOSED_HALF_SPAN_M*1000*i/5
        y = (s+FUSE_MAX_R_MM)/1000
        c = wing_chord_at_y(y)*1000
        rows.append(f"R{i},{s:.6f},{y*1000:.6f},{c:.6f},{.04*c:.6f},{wing_le_station(y,0)*1000:.6f}")
    Path(out_path).write_text("\n".join(rows)+"\n", encoding="utf-8")


def export_fuse_stations_csv(out_path):
    rows = ["x_mm,radius_mm,od_mm"]
    for x in sorted(set(range(0, 2601, 50)) | {1390}):
        r = fuse_radius(x/1000)*1000
        rows.append(f"{x},{r:.6f},{2*r:.6f}")
    Path(out_path).write_text("\n".join(rows)+"\n", encoding="utf-8")


def export_stab_stations_csv(out_path):
    rows = ["section,local_span_mm,chord_mm,t_max_mm,half_thickness_at_spar_mm"]
    for name, z in (("STA_ROOT",0), ("STA_MID",60), ("STA_TIP",120)):
        c = stab_chord_at_z(z)
        rows.append(f"{name},{z},{c:.6f},{.06*c:.6f},{biconvex_half_thickness(c,.3,.06):.6f}")
    Path(out_path).write_text("\n".join(rows)+"\n", encoding="utf-8")


def print_summary():
    print("PROPOSED analytic geometry; R01–R03 OPEN; no CAD qualification")
    print(f"Wing full/exposed area {wing_area_full_trapezoidal():.9f}/{wing_area_exposed():.9f} m²")
    print(f"Centreline/side/tip chord {WING_ROOT_CHORD_M*1000:.6f}/{WING_EXPOSED_ROOT_CHORD_M*1000:.6f}/{WING_TIP_CHORD_M*1000:.6f} mm; MAC {WING_MAC_M*1000:.6f} mm")
    for s in (0., 76.5, 153., 229.5, 306., 382.5):
        print(f"Wing exposed y={s} mm: {wing_spar_containment(s)}; hole {wing_spar_hole_containment(s)}")
    for x in (.05,.15,.3,.6,.85,1.05,1.2,1.39,1.8,2.6):
        print(f"Local envelope {engine_clearance_at_station(x)}")
    for z in (0,60,120):
        print(f"Stabilator local span {z} mm: {stab_spar_hole_containment(z)}")


if __name__ == "__main__":
    print_summary()
