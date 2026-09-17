# Propulsion Matching & Thermal Candidate Review — R07/R08 OPEN

**2026-09-16 · E2 support · Parametric analysis, not physical qualification.**
Reproduce: `python3 tools/propulsion_matching.py` and
`python3 -m unittest tests.test_propulsion_matching -v`.
The **1.10 kg/s incoming-air baseline**, ≥450 N wet-flight contract and
controlled 45/55 mm throat dimensions remain requirements. This study exposes
assumption conflicts; it does not substitute a new baseline, engine map or BOM.

## 1. Nozzle model and limitations

`nozzle_flow()` is a perfect-gas **convergent-nozzle** screen. For a choked
exit, `ṁ=Pt Cd A /√Tt × √(γ/R) × ((γ+1)/2)^(-(γ+1)/(2(γ−1)))`.
Critical `Pt/Pa=((γ+1)/2)^(γ/(γ−1))` is **1.893** for γ=1.4 and **1.851**
for γ=1.33. At choking `Pe=Pt/critical`, `Te=2Tt/(γ+1)` and sonic ideal
velocity is `√(γRTe)`. Below that pressure ratio, `Pe=Pa` and the script
solves subsonic isentropic exit Mach/density/velocity. `Pt=Pa` gives zero
flow; reverse flow is rejected. Invalid/nonfinite temperatures, pressures,
areas, gas properties and coefficient ranges are rejected.

**Area convention:** `Cd A` is effective mass-flow area in **both** choked
and unchoked branches. Pressure thrust uses geometric exit area A:
`Fgross=ṁVe+(Pe−Pa)A`. This assumes uniform exit pressure over that area.
Cd and kinetic-energy efficiency η (velocity multiplier √η) are independent
empirical screen parameters, not a solved viscous flow field. A contracted jet
or nonuniform exit requires integration/calibration. The choked inversion gives
a required Pt only conditional on choking; verify `Pa≤Pt/critical` separately.
The two branches are regression-tested for continuity and consistent Cd use.

The actual iris/duct may not behave as a simple convergent nozzle. A divergent
section, shocks, separation, nonuniform temperatures, AB total-pressure loss,
cooling flow and installation drag require separate matching. Dry γ=1.4/R=287.05
and wet γ=1.33/R=298 are illustrative approximations; the latter implies
cp≈1201 J/kg/K, close to but not identically the heat screen's 1200.

## 2. Pressure demand and mass accounting

For baseline air 1.10 kg/s plus **assumed** core fuel 0.022 kg/s, and the
legacy AB planning value 0.0273 kg/s:

| Conditional state, Cd=1 | Nozzle flow kg/s | Required total pressure, bar absolute |
|---|---:|---:|
| 45 mm dry, 1000 K | 1.122 | 5.52 |
| 55 mm wet, 1700 K | 1.1493 | 5.12 |
| 55 mm wet, 1800 K | 1.1493 | 5.27 |
| 55 mm wet, 1900 K | 1.1493 | 5.41 |

At Pa=69.7 kPa, choking begins at only **1.32 bar dry / 1.29 bar wet**;
onset of choking does not establish required mass capacity. At Pt=2 bar and
1800 K the 55 mm model passes only **0.436 kg/s**. Compare the doc 17 2-bar
assumption cautiously: its station and static/total/absolute/gauge basis need
resolution before equating it to nozzle-inlet total pressure. Pt at the **AB
inlet** is not automatically nozzle-inlet Pt after heat addition/pressure loss.
Pt is also not the only missing input: flow map, Tt, losses, Cd and installed
exit conditions remain unknown. Smaller Cd raises required Pt.

`flight_net()` now requires `ṁair+ṁcorefuel+ṁABfuel=ṁnozzle`; mismatched
states raise an error rather than silently overriding nozzle mass flow.
`Fnet=Fgross−ṁair V∞`; onboard fuel has no incoming ram penalty. The pressure
sweep subtracts assumed fuel from nozzle flow to form **hypothetical** air
flow. Those rows do not replace the 1.10 kg/s baseline and are not matched
engine/AB operating points (Tt and fuel are independently prescribed).

At the old fixed velocity shortcut, including 0.0493 kg/s fuel adds 37.4 N
exit momentum. This is a bookkeeping sensitivity, not a new thrust prediction.
Interpreting 1.10 as total exhaust instead of air would violate the stated
baseline. The screen's ~511 N pressure term at Pt=5.27 bar illustrates why
neglecting pressure thrust can fail; it does not prove actual thrust. For a
fully expanded nozzle Pe=Pa even at high total-pressure ratio, so a small
pressure term does **not** necessarily imply low pressure ratio.

## 3. Heat addition: consistent approximation, not exact combustion physics

The prior round trip hid both omitted core fuel and a prescribed exhaust mass
that did not include the newly solved AB fuel. The corrected model defines
`m0=ṁair+ṁcorefuel` **upstream**, with fuel entering at zero sensible enthalpy
at reference temperature Tr=298.15 K:

`m0 cp(T5−Tr)+mf η LHV = (m0+mf) cp(T7−Tr)`

Thus `mf=m0 cp(T7−T5)/(η LHV−cp(T7−Tr))`. For m0=1.122, cp=1200,
T5=1000 K, T7=1800 K, LHV=43 MJ/kg and η=0.90, **mf=29.19 g/s**.
The inverse returns 1800 K on exactly the same mass/reference basis. The old
27.3 g/s is reproduced only by the simpler `1.10 cp ΔT/(η LHV)` approximation.
Neither value changes the interface fuel contract. The nozzle table above
deliberately retains the legacy fuel assumption; coupling this heat model
would increase wet exhaust flow to ~1.1512 kg/s and require recalculation.

Constant common cp, fixed composition and fuel reference enthalpy are explicit
approximations: real cp(T), oxygen availability, fuel sensible heat, vaporization,
dissociation, radiation and pressure loss need a reacting-flow/enthalpy model
and measurements. Algebraic round-trip agreement is not exact physical energy
closure. Targets exceeding the model's available fuel enthalpy are rejected.

## 4. Thermal equilibrium bounds

`liner_wall_balance()` enforces gas-side convection+radiation = wall conduction
= backside convection+radiation for **prescribed reservoirs**. It checks a
physical temperature bracket, positive conductivity/thickness, finite inputs
and emissivity in [0,1]. With hg=579, hc=125 W/m²/K, Tg=1800 K,
εg=0.25, εc=0.3, shell=610 K, k=18 W/m/K and t=1 mm:

- coolant at 423 K: hot/cold faces **1532/1520 K**, q≈226 kW/m²;
- coolant at 516 K: **1542/1530 K**, q≈218 kW/m².

These are conditional wall equilibria, not allowable Inconel temperatures or a
coupled coolant solution. Coolant heating/film effectiveness, wall properties,
area ratios, shell balance and radiation view factors are unvalidated.
The assumed coolant flow 0.0253 kg/s, cp=1000 and 423→610 K absorbs **4.73 kW**;
the legacy 382 kW/m² over π×0.08×0.20 m² is **19.20 kW**. It cannot all be
assigned to that coolant sensible-heat rise. Radiation can carry some load to
the shell, but then shell heat rejection must also close. This comparison alone
does not prove what fraction reaches coolant or what the actual wall reaches.

`shell_blanket_composite()` balances conduction from prescribed shell temperature
against external convection+radiation. At shell 610 K, ambient 268 K,
kblanket=0.05 W/m/K, thickness=5 mm:

| h_ext W/m²/K | surface K, ε=0.15 | surface K, ε=0.9 |
|---:|---:|---:|
| 5 | 471.0 | 413.8 |
| 10 | 427.1 | 391.9 |
| 15 | 398.0 | 375.0 |
| 25 | 362.8 | 351.1 |

For passive cooling the equilibrium lies between ambient and shell; with **no
external cooling it approaches 610 K**, regardless of blanket resistance.
The sampled h=25 cases fall below the **planning** 373.15 K comparator, while
the other sampled cases do not. These samples do not establish a universal
h threshold, material allowable, composite contact temperature or a flight
convection coefficient. The model omits composite/contact resistance and treats
the outer surface as one node; it is not a through-laminate solution. A prescribed
610 K shell already exceeds a 473.15 K shell comparator if that criterion applies
to this same surface. Resolve station/surface definitions before qualification.
Twenty-second transient heating and subsequent soak-back require thermal
capacity, initial conditions and measured histories; steady equilibrium alone
cannot approve duty/cooldown or guessed material limits.

## 5. Geometry, abort and closure evidence

Worker inventory flagged legacy 20-hole film cooling versus the 105–115-hole
proposal, an iris STEP at the dry position, and sync-ring thickness disagreement.
These remain **unverified inventory leads** pending E2/E5 inspection of generator,
STEP, motion envelope and hot/cold clearances. No geometry was regenerated.
Area ratio (55/45)²=1.494; comparing it directly to T7/T5=1.8 does not prove
matching failure: choked required area scales as `ṁ√Tt/Pt` for fixed gas/Cd.

Opening the iris after fuel cut may reduce backpressure at fixed flow, but the
engine rematches; neither reduced wall heating nor neutral dry thrust follows
automatically. Fail-open/closed selection needs the engine's allowable
backpressure, coupled transient, actuator/jam behavior and independent fuel-cut
latency. No temperature/travel range or fail direction is released here.

Required evidence: separately identified AB-inlet and nozzle-inlet total/static
pressure and temperature; calibrated air/core/AB/cooling flows; discharge and
exit pressure profiles; engine/inlet/nozzle map and uncertainty; wall/shell/
composite traces during wet run and soak-back; material/process allowables;
matched CAD and demonstrated abort/travel. Fuel weighing does not measure air.
R07/R08 and the ≥450 N installed-flight gate remain OPEN.

## Sources checked

- [JetCat primary P550-PRO datasheet](https://www.jetcat.de/jetcat/anleitungen/P550-PRO-Datasheet.pdf),
  V1.1 02/2023, p1, downloaded/read 2026-09-16: 28–550 N, 0.93 kg/s,
  SFC 0.144 kg/N/h, EGT 480–750 °C, 4900 g, 10–35 V supply; source says
  **ISA conditions**, not the draft's STP. It does **not** list compressor
  PR=3.8 or exhaust velocity=2129 km/h. Those claims were removed from the
  verified ledger. The 0.022 kg/s core fuel is only a nominal estimate
  consistent with 550×0.144/3600, not a measured M1 fuel map.
- [NASA thrust equation](https://www.grc.nasa.gov/WWW/k-12/airplane/turbth.html)
  is a conceptual reference; equations and limiting cases are implemented in
  the cited script. No nozzle/engine qualification is inferred from it.
- Repository authority: 18 §2, INTERFACES I-03/thrust contracts; 13–17 and 21
  supply legacy planning assumptions; 25 R07/R08 defines unresolved evidence.

Primary engine data supplies no turbine-exit/AB/nozzle total-pressure map or
installed flight thrust. This review is a candidate analysis handoff only.
