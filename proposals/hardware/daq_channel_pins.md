# DAQ candidate — R11 OPEN

Expert-reviewed specification and candidate wiring are in
[33 §§3–4](../../33_instrumentation_power.md).

- Board A: bridge signals to AIN0/1 and AIN2/3, excitation returns separate.
- Board B: six analog signals to AIN0..5, AINCOM to analog return; 1000 SPS
  aggregate demand. Exact transducer output types/order codes unverified.
- ADS1256 scale is ±2 VREF/PGA; VREF is 0.5–2.6 V, not 5 V.
  Buffer-off/on pin ranges, common mode, source loading and reference
  conditioning must all be checked. A 0–5 V signal does not inherently require
  a 2:1 divider at VREF=2.5/PGA=1, but buffered inputs cannot reach 5 V.
- 2000 SPS nominal → 1438 settled mux samples/s under TI Table 14 conditions.
  Aggregate arithmetic is not a measured weighted schedule or bandwidth proof.
- MAX31856 six-channel sets arrive at ~11 Hz with the stated 90 ms base period,
  not 60 Hz. First conversion, averaging and fault checks add latency.

Full GPIO/DRDY/CS allocation, source timestamps, analog filtering, installed
throughput, reference noise and common-mode validation remain open.
