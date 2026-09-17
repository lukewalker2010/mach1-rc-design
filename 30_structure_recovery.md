# Structure, recovery and aeroelastic screening

**2026-09-16 · baseline `9db2fd0` · R04/R06/R14 OPEN.**
Analysis implementation reviewed; no strength, recovery or flutter clearance.
Sources: 18 §§3.2–3.4, §5.4; INTERFACES §3; legacy 08 parameters explicitly
identified below. Numerical tables are reproduced by `tools/loads_recovery.py`.

```sh
python3 tools/loads_recovery.py
python3 -m unittest tests.test_loads_recovery -v
```

## 1. Geometry and spanwise loads

Centreline trapezoid: b=0.95 m, S=0.14 m², taper=0.4; root/tip chords
210.526/84.211 mm, MAC **156.391 mm**, mean chord S/b=147.368 mm.
As in 29, y0=92.5 mm is a constant maximum-body-radius **surrogate cut**,
not a qualified I-04 joint or actual curved body intersection.

Total wing lift `Lw=n*m*g+Dtail`: positive tail download increases wing lift;
negative input is tail upload. Each full semispan carries Lw/2. Lift shapes
are uniform, triangular, or chord-proportional, each normalised over the
**full** semispan. Outboard shear and bending integrate only beyond the cut.
Inertial relief subtracts `n*g*mwing/2` per full semispan, distributed as
specified. Here mwing is total left+right mass in that idealised distribution;
the baseline 0.50 kg includes carry-through, so using it all as distributed
wing mass is a sensitivity, not measured relief.

`V(y)=integral(l dy)`, `M(y)=integral(l*(y′−y)dy′)`, `dM/dy=−V`.
Positive M denotes bending from upward load. Numerical force **and first
moment** integration is exact for the supported linear load shapes. For a
triangular distribution beyond y0 its centroid arm is `(b/2−y0)/3`.

Baseline full mass is read from 18 §3.4: 13.60 kg, g=9.81 m/s².

| Case | Centreline shear N / moment N·m | y0=92.5 mm shear N / moment N·m |
|---|---:|---:|
| 4g | 266.8 / 54.32 | 196.9 / 32.94 |
| 6g | 400.2 / 81.48 | 295.4 / 49.41 |
| 9g | 600.4 / 122.22 | 443.1 / 74.11 |
| 6g, 0.50 kg like-lift relief | — | 284.5 / 47.59 |
| 6g, illustrative 50 N tail download | — | 313.9 / 52.49 |

Relief subtracts 14.715 N at the **centreline**, but only the outboard fraction
at the side cut (about 10.86 N). Likewise the side-cut tail increment is the
outboard fraction of 25 N, about 18.45 N, not the full 25 N.

INTERFACES §3 separately lists 4g/6g pull-up and root bending ~100 N·m limit /
**150 N·m ultimate** (9g-equivalent wording). 9g recomputes to 122.22 N·m;
legacy 12.2 kg gives 109.64 N·m. Owners must reconcile the reference station,
load distribution and limit/ultimate meanings. This screen cannot replace the
150 N·m contract or select 81.48/122.22 N·m as the governing design load.
Gust, tail trim, asymmetric loads, launch/landing, torsion and joints remain open.

## 2. Cap fit and units

Legacy **210 mm chord** section checks reproduce 20 §3; this rounded reference
must not be confused with the smaller 185.928 mm exposed root in 29.
For flat finite-width caps at u=0.30, minimum depth occurs at a footprint edge.
`d_centroid=min(depth)−2*(skin+bond)−cap_thickness`.

| Width / skin / bond / cap thickness, mm | Outer depth mm | d mm |
|---|---:|---:|
| 50 / 0.5 / 0 / 1 | 4.980 | 2.980 |
| 50 / 0.5 / 0.2 / 1 | 4.980 | 2.580 |
| 35 / 0.5 / 0.2 / 1 | 5.703 | 3.303 |

All fail the previously proposed 7 mm spacing. Footprints crossing LE/TE are
rejected, not clipped. Required area of **each cap**, not both caps combined,
is `A=abs(M)*1000/(d*sigma)` with M in N·m, d in mm, sigma in MPa=N/mm².

| d mm, at M=81.48 N·m | A at 400 MPa | 600 MPa | 800 MPa |
|---|---:|---:|---:|
| 5.056 (centre-only, not finite-width fit) | 40.3 mm² | 26.9 | 20.1 |
| 2.980 | 68.4 | 45.6 | 34.2 |
| 2.580 | 79.0 | 52.6 | 39.5 |

These stresses are sensitivity inputs, **not sourced laminate allowables**.
If area changes cap thickness, separation must be recalculated; this table is
not a self-consistent spar sizing solution. Compression/tension allowables,
environment/process knockdowns, buckling, web shear, bonds, fatigue, fasteners
and proof loads remain required. Section torque uses nose-up-positive convention:
`t=lift_per_length*(x_SC/c−x_AC/c)*c+Cm*q*c²`; upward lift aft of SC is nose-down.
No torque result is claimed without aerodynamic centre, shear centre and Cm data.

## 3. Recovery screen

At sea-level density 1.225 kg/m³, S=0.14 m², `CL=2mg/(rho*V²*S)`:

| Speed | CL full 13.60 kg | CL empty 11.98 kg |
|---|---:|---:|
| 38 m/s approach | 1.077 | 0.949 |
| 30 m/s | 1.729 | 1.523 |
| 70 m/s launch | 0.318 | 0.280 |

At assumed CLmax=0.8, stall speeds are 44.10/41.39 m/s. No low-speed polar
is measured. The 30 m/s calculation is **1g, zero tail download**, not a flare
trim solution. Approach/launch CL ratio is 3.4; 30/70 m/s ratio is 5.4.

Legacy 08 inputs: wheel diameter 50 mm (§1.4), friction mu=0.4 (§2.2), chute
Cd=0.75 and area=0.283 m² (§3.3). These are assumptions, not qualifications.

* Wheel at 70 m/s: **26,738 RPM**; wheel/bearing ratings remain unverified.
* Aircraft KE at 30 m/s: **6,120 J full / 5,391 J empty**. A 0.60 kg dolly
  sensitivity gives combined 14.20 kg and **34,790 J** at 70 m/s.
* Friction-only stop at 30 m/s: **114.7 m**. At mu=0.8: 57.3 m.
* With steady chute drag from initial speed: **60.7 m full / 57.6 m empty**.
  Full mass exceeds the 60 m requirement even before deployment delay.
  The model assumes zero residual lift and constant skid normal load mg;
  measured friction, flare, terrain and opening dynamics are unresolved.
* Legacy ideal roll 54 m (08 §1.2; rounded there to 56 m) + 150 m gives an
  illustrative 204 m stopping distance. Stopping from 70 m/s then requires
  **12.01 m/s² (1.22g)**, versus 624 m at mu=0.4. Roll length at current
  mass/thrust and actual distance remaining at abort must be determined.

Steady chute drag at SL is 117/188/637 N at 30/38/70 m/s; at M0.6 SL it is
**5,420 N**. The 10 kft density sensitivity gives 3,718 N at M0.6 but is not
an allowed corner of a literal h<20 m gate. If height means AGL, terrain
elevation and density must be stated separately.
18 §5.4's 1 kN is a design opening-load reference, **not proof of a rated
hardpoint**. Legacy 100 kg weak link / 500 kg bridle correspond to nominal
981/4905 N force equivalents, not installed dynamic qualification.
An illustrative 800 N steady budget yields 78.4 m/s at SL; 1000 N yields
87.7 m/s. Neither is an approved deployment threshold. At lower density the
same steady load permits **higher** TAS. Measured opening transients, line
loads and a reviewed gate/load budget are needed; no opening multiplier is assumed.

## 4. Aeroelastic evidence required

Uniform cantilever formula `f1=(1.8751²/(2*pi))*sqrt(EI/(mbar*L⁴))` is only
a dimensional/modal sanity check. **Illustrative mass 0.50 kg per half** and
L=0.475 m give f1=13.2/24.2/41.9 Hz for EI=30/100/300 N·m²; 25 Hz requires
EI≈107 N·m². This half-wing mass is a sensitivity input, not the baseline's
0.50 kg total wing+carry-through. It is not a stiffness requirement.
At 25 Hz and actual MAC 0.156391 m, reduced frequency is 0.0340 at 360.8 m/s
and 0.3232 at 38 m/s. Small k alone does not justify quasi-steady transonic
flutter modelling, and ground modes cannot clear flutter.

Required owner-reviewed evidence: measured mass/CG/inertia; static bending and
torsional stiffness; complete-aircraft ground vibration modes and damping;
control stiffness, freeplay and actuator coupling; an uncertainty-bounded
unsteady aeroelastic model over the intended Mach/q/CG envelope, correlated
to those measurements; and approved flight-test limits/cards. Numerical modal
correlation tolerances, mode count, sensor count, damping criteria and flutter
margins must be chosen and justified by the responsible engineers. None are
invented here. Correlated prediction precedes envelope expansion; absence of
observed oscillation is not clearance (25 R14).

## 5. Exact review corrections

Fixed triangular centroid double-division at nonzero cuts, exact distributed
first moments, validation bypass with mixed relief, cap footprint clipping,
per-cap versus pair-area units, torque sign, and unsupported atmospheric domain.
Corrected side-cut relief/download interpretation, bond separation 2.580 mm,
CL ratios, altitude-gate interpretation and density/TAS direction. Removed
invented flutter factor and numerical acceptance policy, false full-suite /
commit claims and physical I-04 load/qualification claims.
Focused tests cover conservation at both cuts, load signs, cap force couples,
footprints, units and invalid inputs. Physical R04/R06/R14 deliverables remain open.
