# Systems & Measurement/Verification Design v2

**Revised:** 2026-09-16 · **Owner:** E3 · **Status:** development layout, NOT RELEASED.
I-06/I-07/I-08/I-12 stations and mating dimensions remain unchanged. This revision
corrects the earlier Mach processing, logger integrity, converter and power-budget
claims. See 25 R05/R09–R12/R15 and [26](26_measurement_validation.md).

## 1. M&V chain

| Instrument | Requirement / disposition |
|---|---|
| Pitot/static | Probe at I-07 station; actual probe/static-port calibration and pressure sensor order codes/ranges open. Former 3447 Pa qc range saturates long before M1. |
| Recovery/TAT probe | At I-07 station; identify part, temperature range, recovery/installation calibration and latency. |
| GNSS | ≥10 Hz Doppler-velocity data per I-08; verify receiver firmware/configuration, dynamics limits, rate and antenna installation. |
| Independent loggers | ≥50 Hz air-data acquisition per I-08; source timestamps, diagnostics and dropped-sample evidence. Verify sensor/power independence, not just two copies of one bus. |
| Altitude | Calibrated static-pressure/temperature and independent navigation comparison; agree uncertainty-aware no-altitude-loss method before flight. |

## 2. Computation and records

Use `tools/airdata.py` for subsonic isentropic and supersonic normal-shock pitot
inversion. Apply the calibrated recovery factor to probe temperature. TAT plus
static pressure alone cannot recover Mach and is not an independent cross-check
of a Mach value derived from the same chain.

`tools/flight_log_check.py` supplies an offline **Mach-duration screen**, including
uncertainty lower bounds and data-quality rejection. Input/CLI and limitations
are in 26. It does not implement flight control or certify the mission.

Each logger's raw file gets its **own** SHA-256, test ID, calibration/configuration
and seal-custody record. Independent samples are compared within calibrated clock
and measurement uncertainties; identical file hashes/sample counts are not the
criterion. Ordinary SD media are not write-once storage.

## 3. Calibration and integration deliverables

1. Qualified pressure range, zero/span/temperature error, leak and tubing lag,
   probe installation correction across the released envelope.
2. Probe temperature calibration, recovery/heat-soak/response assessment.
3. GNSS velocity and source-clock checks, paired logger acquisition/freshness
   verification under worst-case processor/telemetry traffic.
4. Power/ignition/servo/pump EMI and brownout tests; verify sensor diagnostic
   failures propagate to invalid samples, not plausible stale measurements.
5. Recorded configuration and calibrated uncertainty bounds for both reciprocal
   sorties; custody and post-test inspection records per 27.

## 4. Proposed power architecture — converter selection open

The direct **servo/ECU 2S rail concept is withdrawn for the engine branch**.
Cross-workstream primary-source review found that the P550-PRO datasheet V1.1
02/2023 specifies **10–35 VDC**, above even 8.4 V charged 2S. See 33 §2 and
`tools/hardware_budget.py`. Confirm the installed variant and startup/current
requirements before choosing its supply. The 2S servo, regulated 5 V logic and
separate CDI concepts require their own actual component/pin-to-pin review.
A regulator by itself does not provide galvanic isolation. Revise the resulting
power mass and CG together; no replacement supply is qualified here.

The dedicated AB pump/solenoid need a regulated **12 V rail**. The former
“Pololu D24V50F12 2.5 A boost” selection is **withdrawn**: the exact order code
has not been verified, and the verified D24 product family is step-down/buck,
not boost ([manufacturer example](https://www.pololu.com/product/2855)).
Choose and qualify a true boost/buck-boost using actual pump motor/driver data,
minimum pack voltage, solenoid load, startup/stall peaks and installed cooling.
Do not connect a motor to a generic ESC without establishing its motor type and
drive interface. BOM S20 is now a cost allowance with supplier/part TBD.

## 5. Corrected declared-load electrical budget

`tools/power_budget.py`, also used by `tools/bom_v2_check.py`, reproduces these
planning values from the earlier load table. They are **not measured ratings**.
The engine's assumed 7.4 V current row below is now a **rejected historical
scenario**, not a sizing basis for the manufacturer's 10–35 V supply (33 §2).

| Load | Assumed rail / current |
|---|---|
| Tail servos, pair | 7.4 V: 0.5 A average, 4 A declared peak |
| ECU/pump | 7.4 V: 1.5 A average, 2 A declared peak |
| Logic/receiver/telemetry/FPV/loggers/Pico/TAT total | 5 V: 1.7 A |
| AB pump | 12 V: 1.5 A operating, 1.8 A declared maximum |
| AB solenoid | 12 V: 0.5 A |

Use **power**, not current, when moving between rails:

```text
I_battery = V_load I_load / (V_battery efficiency)
```

Planning efficiencies: 5 V converter **0.90**, 12 V converter **0.85**; battery
**7.4 V**. These are assumptions to replace with measured maps. The 5 V load is
already inclusive of Pico/TAT/FPV; do not count them again.

- 5 V loads draw **1.276 A** from the assumed battery.
- AB operating increment is **3.816 A**.
- Declared flight average (excluding AB) = **3.276 A**.
- Hypothetical **300 s** electrical duty plus **40 s** AB increment = **0.315 Ah**.
- Declared simultaneous peak = **11.664 A**, including logic and the pump's
  stated maximum, before unbudgeted loads/transients.

**Open:** iris/drogue servo loads, startup/inrush, low-voltage and wiring drops,
usable battery capacity, thermal derating and real load profiles. The electrical
300 s example does not establish fuel endurance or a five-minute flight. Fuel
consumption must be integrated for start/taxi/climb/acceleration/dash/recovery
with unusable fuel and reserve, independently of this battery calculation.

## 6. Fuel integration

I-06 remains a 2.0 L bladder at stations 0.35–0.60 m. I-12's AB feed routing
remains controlled. Dedicated AB pump is required by 18 D8; no engine-pump tap
is justified. Confirm exact engine installation/return/vent instructions with
the manufacturer, actual bladder construction and fuel-compatible components.

The previous short-orifice vent model at **83 ml/s** gives **5.25 mm minimum ID**
for **25 Pa** loss. Its proposed 5 mm tube gives about **30 Pa**, before line and
check-valve losses, so it does not meet that chosen 25 Pa budget. Numbers are
from `tools/bom_v2_check.py`. Determine tank pressure limits, real line/check-valve
losses and collapse behaviour by the actual tank design; do not infer complete
vent qualification from the orifice model.

## 7. CG and stability

Read 18 §3.4 through `tools/design_checks.py`: full CG **0.974809 m**, empty
**1.045776 m**, excursion **+0.070967 m**. The ±20 mm contract fails at empty
and half fuel. No flight, including a dry-engine-only flight, bypasses fuel-burn
CG movement. Resolve the layout through owner review, then weigh the actual
article over its fuel range. Validate full-aircraft neutral point and trim
separately; 19's guessed tail correction did not close this finding.

## 8. Controls and abort qualification

18's pilot abort <0.5 s is a requirement. The earlier “hold 1 s after signal loss”
sequence and claims of independent abort through the same Pico do not demonstrate
it. Resolve maximum-area versus “dry” iris position using the engine/nozzle
matching design; the original documents prescribe conflicting abort positions.

Required evidence: actual schematic/firmware build, valve/pump/iris feedback,
power-on/reset states, independent fuel-cut path and timed fault injection for
MCU hangs, RC/power loss, sensor stale/open/short conditions and actuator faults.
Measure command-to-physical-fuel-cut latency; a software log line is not proof of
valve closure. The offline tools in 26 do not implement these controls.
