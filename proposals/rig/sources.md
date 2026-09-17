# R13 source ledger — candidate analysis, 2026-09-16

Primary source inspected directly: <https://8020.net/40-4040.html>, product
details for **40-4040**, not 40-4040-Lite or a generic solid 40 mm square.
This is a transcription of selected fields, not a supplier certificate or a
downloaded, authenticated vendor document. Exact bought profile remains to be selected.

| Vendor field | Text observed | Treatment in `tools/rig_loads.py` |
|---|---|---|
| Grade | 6063-T6 | Identification only; no fastener allowable inferred |
| Moment of Inertia - IX / IY | 13.787 cm⁴ each | `13.787 × 10^-8 = 1.3787e-7 m⁴` |
| Modulus of Elasticity | `68.947.6 N / Sq mm` | Malformed vendor text; **68.9 GPa is an explicit screening parameter**, not a verified transcription |
| Yield Strength | 172.37 N / Sq mm | Not used to qualify profile, connections or fasteners |
| Weight lbs | 0.1321 per inch | `0.1321 × 0.45359237 / 0.0254 = 2.359037483 kg/m` |
| Surface Area | 8.742 Sq cm | Vendor label retained here only; not interpreted as section area |

Conversions use exact definitions 1 cm = 0.01 m, 1 inch = 0.0254 m,
1 pound = 0.45359237 kg. Connection flexibility is a boundary/joint problem;
the previous arbitrary “80–90% effective inertia” reduction has no basis and
is removed. Beam end restraint is shown as two separate idealizations.

Repository source anchors (baseline supplied by coordinator: `9db2fd0`):

- `24_thrust_stand.md:30,37,45,57–60`: 721 N concept target, 5g, 4.90 +
  0.97 kg engine/AB, 2 kg carriage, two 0.60 m rails, 4×M3/45 mm PCD.
- `24_thrust_stand.md:68`: thrust goes **through** the engine adapter connection
  and carriage before the load cell. A downstream cell is not a bolt bypass.
- `24_thrust_stand.md:88`: historical 0.35 m arm is unverified; used only as a
  CG-arm sensitivity endpoint. Anchor height 0.35 m and toe-to-anchor distance
  0.10 m are separate **illustrative inputs**, not dimensions derived from it.
- `INTERFACES.md:11,13`: I-01 and I-03 controlled 4×M3 / 45 mm patterns;
  drawing review must determine which actual hardware connection the stand uses.
- `25_readiness_review.md:56,59`: R13 and R16 remain open.
- `27_manufacturing_release.md:9–21,45–80,96–98`: required provenance,
  manufacturing operations and physical evidence; templates are not a release.

No fastener grade/allowable, certified joint interaction law, substrate capacity,
proof load, process recipe or as-built fixture measurement is supplied here.
