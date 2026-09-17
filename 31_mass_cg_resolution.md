# R05 mass, CG and mission feasibility

**2026-09-16 · baseline `9db2fd0` · analysis reviewed, R05 OPEN.**
Sources: actual 18 §3.4 rows, 18 §1's 25 kg maximum, I-06 tank range,
0.975 ±**0.020 m** CG contract. Tool: `tools/mass_mission.py`.
No candidate station is approved or physically packaged.

```sh
python3 tools/mass_mission.py
python3 tools/mass_mission.py --json
python3 tools/mass_mission.py --mission proposals/mass/illustrative_mission.csv
python3 -m unittest tests.test_mass_mission -v
```

## 1. Baseline and exact constraint

| Fuel state | Mass kg | Moment kg·m | CG m |
|---|---:|---:|---:|
| Full | 13.600 | 13.2574 | 0.974809 |
| Half | 12.790 | 12.8929 | 1.008045 |
| Empty | 11.980 | 12.5284 | 1.045776 |

Empty CG is 50.776 mm aft of the upper bound. At fixed dry mass the admissible
dry moment is **11.4409–11.9201 kg·m**, requiring at least **0.6083 kg·m**
reduction to satisfy empty CG alone. That reduction alone does **not** close
both endpoints. CG is a monotone linear-fractional function of fuel mass at
a fixed fuel station, so endpoint compliance is sufficient for intermediate
states only under this fixed-station model; bladder slosh/moving fuel centroid
requires separate data.

With the current dry moment, full-state admissible fuel station is
0.283704–0.619506 m, containing I-06's 0.350–0.600 m range. This is only a
full-fuel result. Changing dry moment changes that interval. The tank station
range is an optimistic centroid bound, not a demonstration that a finite
2 L bladder can place its centroid at either boundary while fitting in the bay.

At baseline x_f=0.45 m, the exact aft-band boundary is **1.116147 kg fuel**
(fraction **0.688979**), allowing **0.503853 kg** burn before violation.
This is not an approved reserve or operational workaround.

## 2. Coupled mass/ballast proof, including MTOW=25 kg

For fuel mass m_f at x_f ahead of the CG band and full mass M,

`CG_full <= CG_MAX − m_f*(CG_MAX−x_f)/M`

because dry CG must be <=CG_MAX. Therefore necessarily
`M >= m_f*(CG_MAX−x_f)/(CG_MAX−CG_MIN)`.
The script's `ballast_mtow_proof` computes **22.0725 kg** for m_f=1.62 kg,
x_f=0.45 m. Even placing fuel centroid at I-06's aft boundary 0.60 m requires
**15.9975 kg**, above the 13.60 kg baseline. Thus redistribution at unchanged
dry mass/fuel cannot close the band anywhere in I-06. Simply moving the engine
or calling fuselage structure movable avionics does not solve the joint problem.

Additional nose ballast at x=0.10 m requires **b≥0.679665 kg** for empty CG,
but **b≤0.315088 kg** for full CG: infeasible. The full-state upper-CG
inequality supplies a lower bound, not a negative maximum-ballast prohibition.
The existing 1 kg nose ballast remains part of the input table.

**It is incorrect to claim all ballast locations are impossible below 25 kg.**
At 25 kg, additional b=11.40 kg can mathematically satisfy both endpoints
with a centroid in **0.931368–0.941640 m**, the interval returned by
`ballast_mtow_proof` from both endpoints.
This is a constructive moment balance, not a feasible aircraft layout.
The tests construct its midpoint and verify the full fuel sweep and MTOW.
Any such large addition requires material volume, attachment loads, simultaneous
duct/carry-through packaging, revised structure/recovery/propulsion and measured
mass/CG review. No ballast block, engine move or changed CG band is recommended.

For mass removal, the correct empty-aft constraint uses `(x_component−CG_MAX)`
per kg removed, not x_component alone, because the denominator changes too.
Removing forward ballast worsens aft CG. No unsupported mass-removal or
CG-neutral aft-movement claim is retained.

## 3. Independent uncertainty bounds

Illustrative tolerances: ±0.050 kg for each **non-fuel** component, ±0.005 m
for every station; fuel quantity at each sweep point treated as known.
These are sensitivity inputs, not measured uncertainty or approved tolerances.
Mass bounds are chosen independently by component position relative to trial
CG, and the zero of the extreme moment residual is solved. The old all-light /
all-heavy calculation was not a worst-case bound.

| State | Minimum CG m | Maximum CG m |
|---|---:|---:|
| Full | **0.947669** | **1.001465** |
| Empty | **1.016147** | **1.075612** |

Even full-fuel CG is not guaranteed in band under these assumptions.
Independent exhaustive-corner tests verify the solver on a small asymmetric
fixture. Fuel metering uncertainty, correlated errors and moving fuel centroid
must be supplied for a real uncertainty budget.

## 4. AB accounting

Replacing 0.83 kg with 0.97 kg at the same 1.48 m station gives full mass
13.74 kg / CG **0.979956 m**, empty mass 12.12 kg / CG **1.050792 m**;
empty shift is **+5.015785 mm**. This sensitivity adds 0.14 kg without asserting
that the mass belongs there. 17 §2e's supersession note mentions restored pump
mass; 18 §5.2's **$80 is price, not grams**. It does not establish pump mass
or inclusion in the 0.50 kg fuel-system row. Enumerate and weigh assembly,
pump, lines, brackets and utilities, assigning each once at its actual centroid.
See `proposals/mass/ab_mass_accounting.md`.

## 5. Mission CSV

Fields: phase, duration_s, engine_flow_g_s, ab_flow_g_s, initial_fuel_kg,
initial_cg_m. The parser validates finite nonnegative flows/time, tank capacity
from the supplied fuel row, phase fuel continuity, no overdraw, nonempty phases,
CSV shape and initial CG agreement with the mass table (0.00005 m allows
rounding to 0.1 mm; this is a serialization tolerance, not a CG acceptance band).
Engine and AB flow both consume the common fuel row; a separate tank needs a
different model. CG is calculated, not taken from the CSV as evidence.

`proposals/mass/illustrative_mission.csv` is synthetic parser/planning input.
Its 15/20 g/s rates are arbitrary examples, not validated engine/AB mission
flows; phase names do not establish Mach or thrust. It finishes with 0.070 kg
fuel and violates the CG band. No climb, dash, reciprocal mission, cooldown or
reserve capability is demonstrated.

## 6. Exact defects corrected / unresolved interfaces

Corrected independent CG extrema, ballast inequality direction and MTOW
feasibility, fixed-capacity assumptions for caller-supplied tables, ignored
initial-CG fields, malformed CSV/overflow handling and sweep validation.
Removed incorrect 25 mm tolerance, fabricated pump grams, false ballast
stations/gaps, incorrect mass-removal arithmetic, false full-state redistribution
closure and unsupported “CG-neutral” component moves. Replaced invented layout
recommendations with the endpoint proof and an explicitly un-packaged ballast
counterexample. No controlled stations or original mass rows were edited.

E1/E3 must select a coupled mass/fuel/layout solution and component boundaries;
I-01/I-04/I-06/I-07 and recovery/propulsion impacts require owner review.
Physical weigh-off and Mach-dependent neutral point/trim/control authority
remain independent requirements. The principal owns global documentation integration.
