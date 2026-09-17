#!/usr/bin/env python3
"""R13 parametric statics screening; never a rig strength qualification.

SI units. See 35_manufacturing_rig.md and proposals/rig/sources.md for provenance,
coordinate transforms, free bodies and limits. No fastener allowable is defaulted.
"""

import json
import math
from dataclasses import dataclass


EXTRUSION = {
    "profile": "80/20 40-4040 (candidate, not procured)",
    "source_url": "https://8020.net/40-4040.html",
    "retrieved": "2026-09-16",
    "I_cm4": 13.787,
    "I_m4": 13.787 * 1e-8,
    "weight_lb_in": 0.1321,
    "weight_kg_m": 0.1321 * 0.45359237 / 0.0254,
    "E_Pa": 68.9e9,
    "E_basis": "explicit screening parameter; vendor prints malformed 68.947.6 N / Sq mm",
}


def number(value, name, *, positive=False, nonnegative=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if positive and value <= 0 or nonnegative and value < 0:
        raise ValueError(f"{name} outside permitted range")
    return value


@dataclass(frozen=True)
class BoltCoord:
    label: str
    x: float
    y: float


def bolt_circle_coords(pcd_m, n, start_angle_deg=45.0):
    number(pcd_m, "pcd_m", positive=True)
    number(start_angle_deg, "start_angle_deg")
    if type(n) is not int or n < 3:
        raise ValueError("at least three bolts required for biaxial distribution")
    return [BoltCoord(f"B{i+1}", pcd_m / 2 * math.cos(math.radians(start_angle_deg + i*360/n)),
                      pcd_m / 2 * math.sin(math.radians(start_angle_deg + i*360/n)))
            for i in range(n)]


def bolt_group_loads(coords, axial_N=0.0, shear_x_N=0.0, shear_y_N=0.0,
                     moment_x_Nm=0.0, moment_y_Nm=0.0, torsion_Nm=0.0):
    """Equal-stiffness rigid group, loads about its centroid, local normal +z.

    Signed axial forces represent bolt tension AND contact compression, not
    compression-capable bolts. This linear full-contact model ceases to represent
    an opening/prying joint; tension=max(0, axial) alone does not solve that joint.
    In-plane torsion is vectorially added to direct shear at each bolt.
    """
    loads = (axial_N, shear_x_N, shear_y_N, moment_x_Nm, moment_y_Nm, torsion_Nm)
    for value in loads:
        number(value, "load")
    if len(coords) < 3 or len({b.label for b in coords}) != len(coords):
        raise ValueError("need >=3 uniquely labelled bolts")
    for b in coords:
        number(b.x, "bolt x")
        number(b.y, "bolt y")
    n = len(coords)
    cx, cy = sum(b.x for b in coords)/n, sum(b.y for b in coords)/n
    xy = [(b.x-cx, b.y-cy) for b in coords]
    xx = sum(x*x for x, y in xy)
    yy = sum(y*y for x, y in xy)
    cross = sum(x*y for x, y in xy)
    det = xx*yy-cross*cross
    if xx+yy == 0 or det <= 1e-12*(xx+yy)**2:
        raise ValueError("degenerate/ill-conditioned bolt group")
    a = (-moment_y_Nm*yy - moment_x_Nm*cross)/det
    b = (moment_x_Nm*xx + moment_y_Nm*cross)/det
    forces = []
    for bolt, (x, y) in zip(coords, xy):
        axial = axial_N/n+a*x+b*y
        sx = shear_x_N/n-torsion_Nm*y/(xx+yy)
        sy = shear_y_N/n+torsion_Nm*x/(xx+yy)
        forces.append({"label": bolt.label, "x_m": x, "y_m": y,
                       "axial_signed_N": axial, "tension_screen_N": max(0.0, axial),
                       "shear_x_N": sx, "shear_y_N": sy, "shear_N": math.hypot(sx, sy)})
    recovered = [sum(f["axial_signed_N"] for f in forces),
                 sum(f["shear_x_N"] for f in forces), sum(f["shear_y_N"] for f in forces),
                 sum(f["y_m"]*f["axial_signed_N"] for f in forces),
                 -sum(f["x_m"]*f["axial_signed_N"] for f in forces),
                 sum(f["x_m"]*f["shear_y_N"]-f["y_m"]*f["shear_x_N"] for f in forces)]
    return {"bolts": forces, "applied_N_Nm": list(loads), "recovered_N_Nm": recovered,
            "equilibrium_residual_N_Nm": [r-v for r, v in zip(recovered, loads)],
            "strength_status": "UNQUALIFIED", "model": "rigid full-contact elastic group"}


def bolt_group_axial_moment(coords, M_Nm):
    result = bolt_group_loads(coords, moment_x_Nm=M_Nm)
    return ([f["axial_signed_N"] for f in result["bolts"]],
            sum(f["y_m"]**2 for f in result["bolts"]))


def bolt_shear_area(dia_m):
    """Nominal shank area only; not valid for an unspecified threaded shear plane."""
    return math.pi/4 * number(dia_m, "diameter", positive=True)**2


def bolt_tensile_stress_area(dia_m):
    """Metric coarse-thread geometric approximation pi/4*(d-0.9382*p)^2.

    Not a material capacity; unsupported diameters are rejected.
    """
    number(dia_m, "diameter", positive=True)
    pitch = {0.003: 0.0005, 0.004: 0.0007, 0.005: 0.0008, 0.006: 0.001}.get(dia_m)
    if pitch is None:
        raise ValueError("unsupported coarse-thread diameter")
    return math.pi/4*(dia_m-0.9382*pitch)**2


def combined_interaction(F_tension_N, F_shear_N, A_t, A_s, sigma_y_Pa, tau_y_Pa):
    """User-parameter elliptical interaction, NOT an approved fastener criterion.

    R=(Ft/(At*sigma))^2+(Fs/(As*tau))^2. Separate tensile and shear allowables
    must be supplied from the selected fastener/joint design basis. No inference
    from extrusion yield, and no override of the supplied shear allowable.
    """
    for value in (F_tension_N, F_shear_N):
        number(value, "force magnitude", nonnegative=True)
    for value in (A_t, A_s, sigma_y_Pa, tau_y_Pa):
        number(value, "area/allowable", positive=True)
    return (F_tension_N/(A_t*sigma_y_Pa))**2 + (F_shear_N/(A_s*tau_y_Pa))**2


def beam_analysis(span_m, P_N, E_Pa, I_m4, depth_m, support="simply_supported"):
    """Euler-Bernoulli prismatic beam, central transverse point load.

    Simple supports: delta=PL^3/(48EI), Mmax=PL/4.
    Fixed ends: delta=PL^3/(192EI), |M|max=PL/8 (hogging at ends).
    Neither boundary condition qualifies bracket/slot/anchor stiffness.
    """
    for value in (span_m, E_Pa, I_m4, depth_m):
        number(value, "beam dimension/property", positive=True)
    number(P_N, "load", nonnegative=True)
    if support not in {"simply_supported", "fixed_fixed"}:
        raise ValueError("unknown support model")
    fixed = support == "fixed_fixed"
    moment = P_N*span_m/(8 if fixed else 4)
    return {"support": support, "load_N": P_N, "reaction_each_N": P_N/2,
            "end_moment_magnitude_Nm": moment if fixed else 0.0,
            "max_moment_Nm": moment,
            "deflection_m": P_N*span_m**3/((192 if fixed else 48)*E_Pa*I_m4),
            "max_stress_Pa": moment*depth_m/(2*I_m4), "strength_status": "UNQUALIFIED"}


def beam_central_point_deflection(span_m, P_N, E_Pa, I_m4):
    return beam_analysis(span_m, P_N, E_Pa, I_m4, 0.04, "fixed_fixed")["deflection_m"]


def beam_central_point_stress(span_m, P_N, d_m, I_m4):
    return beam_analysis(span_m, P_N, 1.0, I_m4, d_m, "fixed_fixed")["max_stress_Pa"]


def overturning_analysis(thrust_N, arm_m, anchor_bolts=2, anchor_spacing_m=0.10,
                          downward_load_N=0.0):
    """Rigid footing, two anchor rows at +/-b/2, centered downward load W.

    Global thrust is along +X and height along +Z; overturning is about +Y.
    Positive thrust lifts the -X anchor row, bearing at the +X toe.
    arm_m is thrust HEIGHT above bearing plane, never an axial stand length.
    b is distance from compression toe to opposite anchor row. Tension-only
    anchors; bearing carries compression. No friction credit: equal shear in
    all anchors. No prying, preload, lateral moment or net vertical uplift model.
    W=0 default deliberately gives no credit for unknown ballast.
    """
    number(thrust_N, "thrust")
    number(arm_m, "height", nonnegative=True)
    number(anchor_spacing_m, "toe-to-anchor lever", positive=True)
    number(downward_load_N, "downward load", nonnegative=True)
    if type(anchor_bolts) is not int or anchor_bolts < 2 or anchor_bolts % 2:
        raise ValueError("equal anchor rows require positive even bolt count >=2")
    moment = thrust_N*arm_m
    b, w = anchor_spacing_m, downward_load_N
    tension = max(0.0, abs(moment)/b-w/2)
    compression = w+tension
    # Signed contact offset measured toward the active compression toe.
    contact_offset = abs(moment)/w if tension == 0 and w else b/2
    resisting_moment = compression*contact_offset+tension*b/2
    return {"thrust_N": thrust_N, "height_m": arm_m, "moment_Nm": moment,
            "downward_load_N": w, "uplift": tension > 0,
            "tension_row": "-X" if moment >= 0 else "+X",
            "anchor_row_total_tension_N": tension,
            "anchor_tension_each_active_N": tension/(anchor_bolts/2),
            "anchor_tension_each_inactive_N": 0.0,
            "bearing_compression_N": compression, "contact_offset_m": contact_offset,
            "shear_each_N": abs(thrust_N)/anchor_bolts,
            "vertical_residual_N": compression-tension-w,
            "moment_residual_Nm": resisting_moment-abs(moment),
            "strength_status": "UNQUALIFIED"}


def full_analysis():
    # Concept sensitivity inputs: 24 lines 30,37,45,57-60,88. Not an as-built model.
    engine_ab_mass = 4.90+0.97  # 24 concept; 18 instead assigns 0.83 kg AB (R05).
    vertical = engine_ab_mass*5*9.81
    rail_load = (engine_ab_mass+2.0)*5*9.81/2
    bolts = bolt_circle_coords(0.045, 4)  # unchanged controlled pattern
    return {
        "status": "SCREENING_ONLY_UNQUALIFIED", "extrusion": EXTRUSION,
        "inputs": {"thrust_N": 721.0, "engine_ab_mass_kg": engine_ab_mass,
                   "engine_vertical_5g_N": vertical, "rail_load_each_N": rail_load,
                   "cg_arm_sensitivity_m": [0.0, 0.35], "anchor_height_assumed_m": 0.35,
                   "toe_anchor_spacing_assumed_m": 0.10},
        "engine_mount_arm_sweep": [
            {"cg_arm_m": arm, **bolt_group_loads(bolts, axial_N=721.0, shear_y_N=-vertical,
                                               moment_x_Nm=vertical*arm)}
            for arm in (0.0, 0.35)],
        "beam_support_sweep": [beam_analysis(0.60, rail_load, EXTRUSION["E_Pa"],
                                             EXTRUSION["I_m4"], 0.04, support)
                               for support in ("simply_supported", "fixed_fixed")],
        "anchor_example": overturning_analysis(721.0, 0.35),
        "allowables": None,
        "limitations": ["Unknown actual CG arms, mount plane, preload/contact and prying",
                        "No supplier fastener, bracket, slot, rod-end or substrate capacities",
                        "No measured rig stiffness, modes, proof or installed calibration",
                        "Equal rail sharing and rigid support assumptions need drawings/test"],
    }


def main():
    print(json.dumps(full_analysis(), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
