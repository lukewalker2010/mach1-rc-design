# Pressure chain candidate — R09 OPEN

[33 §1](../../33_instrumentation_power.md) is the evidence/uncertainty ledger.
Envelope screen: max qc 142.615 kPa, SL/M1.2; not a flight release.

- `4525DO-DS3BJ050DP`: exact TE page confirms 50 psi differential and 300 psi
  proof. Exact interface/address, supply, transfer function and TEB need
  ordering-table confirmation; no procurement quote.
- `4525DO-DS5AI001DP`: TE description says 1 psi, but page attributes conflict.
  Range/proof/options unverified. Full-flight exposure can be 20.7 psi even
  when its low-range samples are ignored; resolve physical overrange protection.
- `MS5803-02BA`: family candidate only; exact primary specifications/order code
  and pressure noise/rate unverified. A raw 24-bit ADC is not pressure resolution.

Proposed high/low differential qc + absolute static architecture awaits bus
address/voltage checks, proof/common-port/reverse pressure checks, calibrated
usable ranges, temperature/installation errors, tube lag and source-clock
freshness. No part selection or interface/BOM change is released.
