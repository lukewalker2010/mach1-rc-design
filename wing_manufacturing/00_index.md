# Wing Manufacturing Package — Index

**Date:** 2026-07-21
**Purpose:** Close the manufacturing gap between design spec and build-ready data

## Files

| # | File | Contents |
|---|------|----------|
| 01 | `01_rib_profiles.md` | Complete biconvex airfoil coordinates for all 6 ribs (20 stations each), CNC cutting notes |
| 02 | `02_mould_design.md` | Mould geometry, material, CNC machining sequence, vacuum bag setup, release system |
| 03 | `03_layup_schedule.md` | Ply-by-ply layup instructions, cutting dimensions, cure cycle, bond schedule, QA criteria |

## What This Adds

The original design spec (`04_wing_structure.md`) defined the wing structurally but lacked:
- Exact rib profile coordinates for CNC cutting
- Mould dimensions and machining instructions
- Ply cutting patterns and orientation diagrams
- Detailed layup sequence and cure parameters
- Ply drop-off transition detail

This package fills those gaps and makes the wing **as build-ready as the C-D nozzle**.

## Build Time Estimate

| Task | Hours |
|------|-------|
| Generate CNC code from rib coordinates | 1-2 |
| Machine aluminium mould | 4-6 |
| Surface prep + polish mould | 2-3 |
| Cut prepreg plies | 1-2 |
| Layup + vacuum bag | 2-3 |
| Cure (passive, not active labour) | 4 |
| Demould + trim | 1-2 |
| Rib fabrication (×12) | 3-4 |
| Assembly (spar, ribs, skins) | 4-6 |
| **Total** | **22-32 hours** |

## Quick Reference

- Biconvex formula: y(x) = ±(t/2) × sin(πx/c)
- t/c = 3.5%
- Spar position: 30% chord
- Spar diameter: 5.0 mm
- Rib count: 12 (6 per half)
- Inner skin: [0/±45/0], 0.8 mm, 4 plies
- Outer skin: [0/±45], 0.6 mm, 3 plies
- Total wing weight: 568 g target
