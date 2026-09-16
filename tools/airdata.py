"""Offline perfect-gas air data; NASA Glenn normal-shock/isentropic relations.

Pitot pressure above M=1 is stagnation pressure AFTER the probe's normal shock.
These equations do not correct installation error or qualify a real probe.
Units: Pa, K, m/s. See 26_measurement_validation.md for validity and calibration.
"""
import math

GAMMA = 1.4
R_AIR = 287.05
MAX_MACH = 3.0  # numerical domain, NOT an aircraft operating envelope


def finite(name, value, minimum=0.0, inclusive=False):
    if not math.isfinite(value) or (value < minimum if inclusive else value <= minimum):
        raise ValueError(f"{name} must be finite and {'>=' if inclusive else '>'} {minimum}")


def pitot_ratio(mach):
    """Return measured pitot/static ratio (Rayleigh pitot for supersonic flow)."""
    finite("Mach", mach, inclusive=True)
    if mach > MAX_MACH:
        raise ValueError(f"Mach exceeds model domain {MAX_MACH}")
    if mach <= 1.0:
        return (1.0 + (GAMMA - 1.0) / 2.0 * mach**2) ** (GAMMA / (GAMMA - 1.0))
    # Normal-shock static jump followed by subsonic isentropic stagnation.
    m2_sq = ((GAMMA - 1) * mach**2 + 2) / (2 * GAMMA * mach**2 - (GAMMA - 1))
    p2_p1 = (2 * GAMMA * mach**2 - (GAMMA - 1)) / (GAMMA + 1)
    return p2_p1 * (1 + (GAMMA - 1) / 2 * m2_sq) ** (GAMMA / (GAMMA - 1))


def mach_from_pressures(static_pa, impact_pa):
    """Invert qc = p_pitot - p_static. Reject negative qc; do not clip bad data."""
    finite("static pressure", static_pa)
    finite("impact pressure", impact_pa, inclusive=True)
    ratio = 1 + impact_pa / static_pa
    if ratio > pitot_ratio(MAX_MACH):
        raise ValueError("pressure ratio exceeds model domain")
    if ratio <= pitot_ratio(1.0):
        return math.sqrt(2 / (GAMMA - 1) * (ratio ** ((GAMMA - 1) / GAMMA) - 1))
    lo, hi = 1.0, MAX_MACH
    for _ in range(60):
        mid = (lo + hi) / 2
        if pitot_ratio(mid) < ratio:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def airdata(static_pa, impact_pa, probe_temp_k, recovery_factor):
    """Recovery-corrected static T and TAS; recovery factor must be calibrated."""
    finite("probe temperature", probe_temp_k)
    finite("recovery factor", recovery_factor)
    if recovery_factor > 1:
        raise ValueError("recovery factor must be <= 1")
    mach = mach_from_pressures(static_pa, impact_pa)
    static_k = probe_temp_k / (1 + recovery_factor * (GAMMA - 1) / 2 * mach**2)
    return {"mach": mach, "static_temp_k": static_k,
            "tas_m_s": mach * math.sqrt(GAMMA * R_AIR * static_k)}
