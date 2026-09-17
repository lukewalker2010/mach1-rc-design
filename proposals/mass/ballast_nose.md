# Ballast constraint study — no approved physical layout

**2026-09-16 · PROPOSED analysis only.** Source: `tools/mass_mission.py`,
`joint_ballast_analysis` and `ballast_mtow_proof`; baseline rows from 18 §3.4.

Additional nose ballast at station 0.10 m must be at least **0.679665 kg**
to meet empty CG <=0.995 m, but at most **0.315088 kg** to meet full CG
>=0.955 m. The intervals do not overlap. Existing 1 kg ballast is already
included in the mass table; these are additions, not replacement totals.

Changing ballast to 0.40 m does not fix this. Earlier claims of a feasible
0.40 m solution, improving gaps, or a small redistribution-plus-ballast
solution were arithmetically wrong and have been withdrawn.

For the baseline fuel centroid 0.45 m and capacity 1.62 kg, both endpoint
constraints require full mass >=**22.0725 kg** irrespective of dry layout.
At MTOW **25 kg**, an additional **11.40 kg** at centroid
**0.931368–0.941640 m** is mathematically feasible. For example the script
at x=0.94 m returns allowable additional mass **11.06–11.40 kg**; its lower
endpoint gives empty CG 0.995000 m and full CG 0.959197 m.

This is a counterexample to an unrestricted “no ballast can work” claim,
not a recommendation. No material, volume, attachment or simultaneous
duct/carry-through fit has been established. The heavy addition requires a
new coupled loads, recovery, propulsion and mass review. Unchanged-mass
redistribution cannot solve both endpoints even at the optimistic I-06 aft
fuel-centroid bound. See [31](../../31_mass_cg_resolution.md) for the proof,
uncertainties and unresolved interface decisions.
