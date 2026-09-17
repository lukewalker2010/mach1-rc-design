"""Thrust-stand concept screening, not structural or DAQ qualification.

Run: python3 tools/thrust_stand_check.py. See 25 R07/R11/R13 and 26 §4.
"""
import math


def main():
    capacity = 100 * 9.81  # 24 proposed nominal load-cell range, not overload proof
    print(f"LOAD CELL nominal range {capacity:.0f} N; 700 N development target ratio {capacity / 700:.2f}")
    print("  Range headroom is not structural qualification or flight-thrust verification.")
    solid_i = 0.04**4 / 12
    solid_deflection = 400 * 0.6**3 / (48 * 70e9 * solid_i)
    print(f"FRAME solid-square idealisation: {solid_deflection * 1000:.3f} mm deflection")
    print("  This underestimates slotted-extrusion deflection. Use supplier inertia and actual supports.")
    print("BOLTS/ANCHORS: combined tension/shear, prying, bearing and overturning UNVERIFIED.")
    estimate = math.sqrt(1e7 / (4.9 + 0.97 + 2)) / (2 * math.pi)
    print(f"MODE with assumed 10 MN/m stiffness: {estimate:.0f} Hz, not a measured mode.")
    print("  Requires measured dynamics and anti-alias filtering at every acquisition rate.")
    required_pins = 2 * 2 + 5 + 1  # thrust/tank bridges + pressure + flow (24 §4)
    print(f"ADS1256 INPUTS: direct wiring needs {required_pins} analog pins; 8 available: FAIL")
    print("  Four differential pairs OR eight single-ended inputs, not eight differential pairs.")
    print("  Settling, common-mode limits, gain switching and actual source timing need qualification.")
    print("MAX31856: 60 Hz is line-rejection frequency, not conversion rate. Verify datasheet mode/DRDY.")
    print("DAQ SOFTWARE: offline ingestion/calibration/post-processing now implemented (34); hardware drivers remain open.")


if __name__ == "__main__":
    main()
