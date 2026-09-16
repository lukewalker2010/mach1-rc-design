# Structural Analysis v2 — Corrected Equilibrium, Open Sizing

**Revised:** 2026-09-16 · **Owner:** E1 · **Status:** NOT CLOSED.
Supersedes 10's old-geometry calculations and this document's earlier 163 N·m
half-wing calculation and strength/thermal PASS claims. Requirements remain in
18 and INTERFACES; no member sizing or interface change is approved here.

## 1. Reproduce

```sh
python3 tools/structural_analysis.py
python3 tools/design_checks.py
```

Mass is read directly from 18 §3.4: 13.60 kg, moment 13.2574 kg·m. Full/half/empty
fuel CGs are 0.9748 / 1.0080 / 1.0458 m. Only the full-fuel point meets the
0.955–0.995 m band. A neutral-point assumption cannot override that requirement.

## 2. Half-wing loads

Preliminary **centreline** cantilever with chord-proportional symmetric lift:

```text
W = m g
V_root = n W / 2
y_centroid = (b/2) (1+2λ) / [3(1+λ)]
M_root = V_root y_centroid
```

Inputs b=0.95 m, λ=0.4 (18 §3.2), g=9.81 m/s². The result is **per half-wing**:

| Case | Root shear N | Root moment N·m |
|---|---:|---:|
| 4g limit | 266.83 | 54.32 |
| 6g ultimate | 400.25 | 81.48 |
| 9g comparison with INTERFACES §3 | 600.37 | 122.22 |

The former `n W y_centroid` doubled the bending load. The former shear expression
`n W (b/2−y_centroid)/(b/2)` was not half-wing equilibrium. These corrections do
not establish a complete load envelope or authorise reduced structure.

Define the actual fuselage-side joint separately and integrate the exposed lift
distribution about it. Add tail download, inertial relief, gusts, roll/asymmetric
loads, torsion, launch/recovery loads and local joint/fastener effects. Resolve
the 4g/6g versus 9g/~100 N·m contracts with the interface owners.

## 3. The proposed spar does not fit

The existing generator's parabolic section is
`depth(u)=0.04 c 4u(1−u)`, u=x/c. For its c=210 mm root at u=0.30:

- Outer depth = **7.056 mm**.
- With 0.5 mm skin allowance per face and 1.0 mm caps, available cap-centroid
  separation is at most **5.056 mm**, not 7 mm.
- For the proposed **50 mm wide** flat cap centred at 30% chord, the forward cap
  edge has only **4.980 mm** outer depth. The corresponding maximum constant
  centroid separation falls to **2.980 mm** before adhesive/tolerance allowances.

These numbers are from `tools/structural_analysis.py`, using 20's former cap
proposal and `gen_wing_ribs.py`'s section/offset. Skin/bond process is still
unreleased. The depth problem worsens along a constant-thickness spar toward
the tip. Existing round rib holes fail containment (25 R02).

Therefore the former 5-ply/7 mm stress and “2.6× margin” recommendation is
withdrawn. Establish a manufacturable tapered spar and actual laminate/material
allowables first, then check compression, buckling, web shear, bond transfer,
fatigue, damage tolerance and environmental knockdowns.

## 4. Remaining structural closure

| Subsystem | Missing evidence |
|---|---|
| Stabilator | Real hinge/bearing/spar geometry; hinge moments across Mach/q/incidence; per-servo linkage geometry, speed, torque and backlash under load; rotation and trim authority |
| Engine mount | Manufacturer interface and combined axial/lateral/moment loads; bolt-group tension/shear, bearing, pull-through, preload and bonded insert load path |
| Thermal interface | Conjugate/transient heat balance, material temperature limits and measured soak-back; blanket conductivity alone cannot predict composite temperature |
| Aeroelasticity | Mass/stiffness distributions, torsional rigidity, control freeplay, modal/ground vibration test, correlated flutter analysis and released speed/q limits |
| Physical proof | Fixture/load distribution representing the completed design, calibrated force/strain/deflection, inspection and article disposition |

The old thermal calculation prescribed both shell and composite temperatures and
then calculated `q=kΔT/t`; it did not prove the composite remains below its limit.
Likewise a generic bolt shear rating or servo stall torque is not an assembly
qualification. Track closure in 25 and retain measured evidence using 27.
