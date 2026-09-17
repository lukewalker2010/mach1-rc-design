"""Declared-load power balance for 23 §5; not a completed electrical design.

Currents/durations from the existing 23 budget. Converter efficiencies below
are explicit planning assumptions pending hardware measurement.
The historical 7.4 V engine branch is incompatible with the primary P550-PRO
10–35 V specification found during review (33 §2); outputs are not sizing data.
"""
import math


def input_current(output_v, output_a, input_v, efficiency):
    if not all(math.isfinite(v) for v in (output_v, output_a, input_v, efficiency)):
        raise ValueError("power inputs must be finite")
    if output_v <= 0 or output_a < 0 or input_v <= 0 or not 0 < efficiency <= 1:
        raise ValueError("invalid voltage/current/efficiency")
    return output_v * output_a / (input_v * efficiency)


def estimate():
    battery_v = 7.4
    logic_input = input_current(5, 1.7, battery_v, 0.90)
    ab_input = input_current(12, 1.5 + 0.5, battery_v, 0.85)
    ab_peak = input_current(12, 1.8 + 0.5, battery_v, 0.85)
    flight_average = 0.5 + 1.5 + logic_input
    peak = 4 + 2 + logic_input + ab_peak
    return {"logic_input_a": logic_input, "ab_input_a": ab_input,
            "flight_average_a": flight_average, "declared_peak_a": peak,
            "charge_ah": (flight_average * 300 + ab_input * 40) / 3600}


if __name__ == "__main__":
    print("HISTORICAL SCENARIO: 7.4 V engine branch invalid for manufacturer 10–35 V specification; see 33 §2.")
    for key, value in estimate().items():
        print(f"{key}: {value:.4f}")
    print("Declared-load estimate only: iris/drogue loads, startup, low-voltage behaviour and fuel endurance remain open.")
