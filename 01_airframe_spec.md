# Mach 1 RC Aircraft — Airframe Specification

**Project:** Path 2 — P550-PRO Level Flight Mach 1
**Date:** July 2026
**Status:** Design Complete

---

## 1. Mission Profile

1. Dolly launch to 70 m/s (252 km/h) on paved surface, 56m ground roll
2. Climb at full throttle to 10,000 ft (~25 s, 300g fuel)
3. Level off, accelerate M0.8 → M1.0 at 10,000 ft (11.4 s, 148g fuel)
4. Sustained supersonic flight M1.0+ for 5+ seconds (60g fuel)
5. Throttle back, decelerate subsonic
6. Deadstick approach, drogue chute deploy, belly skid landing (75 m/s)

## 2. General Dimensions

| Parameter | Value |
|-----------|-------|
| Overall length | 2.20 m |
| Fuselage max diameter | 200 mm |
| Fuselage effective diameter (drag ref) | 214 mm |
| Fineness ratio | 11:1 |
| Wing span | 0.90 m |
| Wing area (planform) | 0.095 m² |
| Wing root chord | 0.211 m |
| Wing loading | 129 kg/m² |
| Stabilator span | 0.24 m |
| Stabilator area | 0.0060 m² |
| Ventral fin area | 0.0089 m² |

## 3. Mass Properties

| Component | Mass (kg) |
|-----------|-----------|
| P550-PRO engine | 4.90 |
| C-D nozzle | 0.05 |
| Intake | 0.40 |
| Fuel (1.2L Jet A1) | 1.20 |
| Fuel system (bladder, lines, fittings) | 0.50 |
| Fuselage structure (skins + bulkheads + mount) | 2.95 |
| Wing structure (skins + spar + ribs) | 1.20 |
| Stabilator (both + hardware) | 0.10 |
| Stabilator servos (2× KST X20-12T) | 0.14 |
| Ventral fin | 0.10 |
| Avionics (Rx, FC, GPS, telemetry) | 0.60 |
| Battery (2S 5000mAh LiPo) | 0.30 |
| Belly skid + mounting | 0.15 |
| Drogue chute system | 0.15 |
| Dolly hardpoints (on aircraft) | 0.05 |
| Miscellaneous (fasteners, adhesives, wiring) | 0.30 |
| **MTOW** | **12.99 kg** |

## 4. Aerodynamics

| Parameter | Value |
|-----------|-------|
| Cd at M1.0 (after reductions) | 0.166 |
| Drag at M1/10kft | 292 N |
| Thrust at M1/10kft (C-D nozzle) | 300 N |
| T-D margin at M1 | +7.8 N |
| Acceleration at M1 | 0.74 m/s² |
| L/D at M1 (subsonic reference) | ~4.5 |

## 5. Performance Summary

| Regime | Speed | Altitude | Time | Fuel |
|--------|-------|----------|------|------|
| Launch | 0→70 m/s | SL | 56m roll | 0 |
| Climb | 70 m/s avg | SL→10kft | 25 s | 300 g |
| Transonic accel | M0.8→M1.0 | 10,000 ft | 11.4 s | 148 g |
| Supersonic sustain | M1.0+ | 10,000 ft | 5+ s | 60 g |
| Descent/landing | M1.0→0 | 10kft→SL | — | 0 |
| **Total** | | | | **508 g** |
| Fuel capacity | | | | 1,200 g |
| **Margin** | | | | **692 g (58%)** |

## 6. Control System

| Axis | Actuator | Deflection | Servo |
|------|----------|------------|-------|
| Pitch | Stabilator (collective) | ±15° | KST X20-12T (both) |
| Roll | Stabilator (differential) | ±10° | KST X20-12T (both) |
| Yaw | FBW + ventral fin | — | Active yaw damping |
| Drogue | Servo door release | 90° | Standard micro servo |

## 7. Critical Loads

| Load Case | Factor | Stress |
|-----------|--------|--------|
| 4g symmetric pull-up | Limit | 2.9 MPa fuse, 30 MPa spar |
| 9g ultimate | Ultimate | 68 MPa spar |
| Dolly launch (4.5g accel) | Limit | 15 MPa hardpoints |
| Landing (3g vertical) | Limit | 50 MPa skid bracket |

## 8. Design Margins

| Parameter | Required | Achieved | Margin |
|-----------|----------|----------|--------|
| T-D at M1 | >0 N | +7.8 N | 2.6% |
| MTOW | ≤25 kg | 12.99 kg | 92% |
| Fuel for mission | 508 g | 1,200 g | 58% |
| Supersonic sustain | 5 s | 9.3 s | 86% |
| Wing spar cap stress | <5500 MPa | 2208 MPa | 60% |
| Fuselage bending stress | <3500 MPa | 2.9 MPa | 99.9% |
