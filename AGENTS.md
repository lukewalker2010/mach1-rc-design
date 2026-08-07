# AGENTS.md — Mach 1 RC: Master Instructions for AI Agents

This file is the **single source of truth for how AI tools work on this repository**. Every engineer's AI (code agents, CAD assistants, analysis models) MUST follow it. Update it when the team agrees on a new convention — do not fork it per-tool.

---

## 0. Ground rules

1. **Humans approve, AI proposes.** All writes go through PR/review. AI **may commit and push to `main` directly** — approved change to this rule, effective 2026-08-07 (team decision). For destructive/irreversible changes (history rewrite, secret removal, P0 interface edits) still pause and confirm first.
2. **The baseline is law.** `18_program_requirements.md` is the authoritative program spec (geometry, CG, thrust/drag contracts, mass table). If another doc contradicts it, the other doc is wrong — fix it, don't duplicate it.
3. **Never break an interface without a cross-team review.** Changing a mating dimension in `INTERFACES.md` is a P0 change.
4. **One coordinate system, everywhere.** Fuselage-station origin at the nose tip, +X aft, +Z up. All part CAD carries station/axis in its filename or header.
5. **Units: SI (m, kg, s, N, K), mm for CAD, deg for angles.** No mixed units. Temperature in K for analysis, °C only in lab/test write-ups.
6. **Numbers are owned, not invented.** Every published number must trace to a doc line or a committed analysis script. If you change an assumption, re-derive downstream numbers and say what changed.

---

## 1. Repository layout & naming

```
*.md                 design & analysis docs, numbered 00-18
*_step.py            CadQuery STEP generators (authoritative CAD)
*.step               generated solids (regenerate via *_step.py, don't hand-edit)
*.scad               OpenSCAD reference models (secondary to STEP)
*_manufacturing/     per-subsystem build packages (moulds, layups, DXFs)
```

- CAD files: `<part>_step.py` → `<part>.step`. Regenerate with the pinned CadQuery env (see §5).
- Docs: `NN_topic.md`, monotonic numbering, never renumber.
- DXF/CSV: `wing_manufacturing/`, `stabilator_manufacturing/` — net-part geometry only, one entity type per file.

---

## 2. Geometry conventions (critical)

| Item | Value |
|---|---|
| Origin | fuselage nose tip = (0,0,0); +X aft, +Z up |
| Fuselage | 185 mm max OD, 2.60 m long (baseline per 18 §3.1) |
| Wing | b 0.95 m, S 0.14 m², λ 0.4, Λ_LE 30°, t/c 4% (18 §3.2) |
| Wing carry-through | stations 0.95–1.15 m |
| Engine mount ring | station 1.20 m (18 §3.1) |
| Afterburner | stations 1.39–1.80 m (z-stack in `ab_assembly_step.py`) |
| Stabilator | station 2.30–2.45 m |
| Target CG | 0.975 m ±20 mm (all fuel loads) |
| Static margin | ≥ 12% MAC |

## 3. Propulsion facts (do not re-derive differently)

- Engine: JetCat P550-PRO. ṁ at M1/10 kft = **1.10 kg/s** (corrected-flow model, 13 Method B). **NOT 0.69** (see 18 §2.1 — that value breaks the program).
- Net dry thrust @ M1/10 kft ≈ **257 N**; wet (AB, 1800 K) ≈ **465 N** (450–475 N band).
- Design contracts: wet ≥ 450 N, hump drag ≤ 430 N, dash at 10–12 kft.
- AB fuel: dedicated Speck ZY-4S-12V pump (tapping the engine pump is impossible).

## 4. Quality gates (every AI contribution must pass)

1. **CAD change** → regenerate `.step`, then import-check with the pinned CadQuery env: part must load, bounding box must match design intent, assembly must have zero interferences (`/tmp/opencode/step_validate` equivalent or `importStep` + pairwise `.intersect().Volume()`).
2. **Doc change** → numbers must cite their source line or script; update `00_index.md` and any dependent docs.
3. **BOM change** → update cost, note single-source items, verify link not dead.
4. **Analysis change** → commit the script (`tools/` dir) that produced it, not just the number.

## 5. Environment

- CadQuery env (pinned): `python@3.12` + `cadquery==2.8.0`. Do NOT use system Python 3.14 (OCP not available).
- OpenSCAD: render `.scad` before relying on it; STEP files are authoritative for manufacture.
- DXF: generated from the corrected rib/mould equations in `18 §7` dispositions.

## 6. Status board (update after each session)

| Subsystem | Owner | Status | Next action |
|---|---|---|---|
| A. Airframe | E1 | 🔴 re-baseline done, CAD pending | re-run 10/12; regen moulds & ribs |
| B. Propulsion/AB | E2 | 🟡 design done, CAD verified | AB bench build → wet thrust ≥450 N |
| C. Systems/M&V | E3 | 🟡 gaps identified | add TAT/loggers/FPV; BOM v2 |
| D. Launch/Recovery | E4 | 🟡 | dolly abort brakes; TAS-gated drogue |
| E. Manufacturing/QC | E5 | 🔴 | regen net-part DXFs; reconcile mould tables |

Legend: 🔴 needs work · 🟡 in progress · 🟢 complete/verified
