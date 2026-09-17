# AB mass accounting — unresolved component boundary

**2026-09-16 · review proposal, no measured mass evidence.**
18 §3.4 specifies 0.83 kg at 1.48 m. The supersession note in 17 §2e
describes restoring the pump and an approximately 0.97 kg AB; 25 R05
requires reconciliation with the separately budgeted fuel system.

`tools/mass_mission.py::ab_sensitivity` replaces only the AB row while keeping
its station fixed:

| Assumed AB mass | Full CG m | Empty CG m |
|---|---:|---:|
| 0.83 kg | 0.974809 | 1.045776 |
| 0.97 kg | 0.979956 | 1.050792 |

The empty shift is +5.015785 mm. Neither closes empty CG. The full shift is
+5.147508 mm. The 0.14 kg sensitivity is not a measured pump mass or a
justification for placing the pump at the hot assembly's centroid.

18 §5.2's **$80 is cost, not 80 g**. The contents of “Fuel system” (0.50 kg)
and “Miscellaneous” (0.30 kg) are not itemised well enough to prove overlap.
Do not assert double-counting until the actual component inventory is known.

E2/E3 should enumerate and separately weigh AB metalwork/nozzle, pump,
lines, valves, brackets, wiring and controls; assign each exactly once with
its installed centroid. Review the resulting mass table and interface effects
before updating controlled requirements. This proposal makes no such update.
