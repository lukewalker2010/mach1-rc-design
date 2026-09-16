# DXF disposition — 2026-09-16

**These files are not released net parts.** The committed hole contours break
outside the wing web at R1–R5 and outside the stabilator tip outer surface.
The generator's exposed-root convention also disagrees with the wing area
baseline. The contours have been retained so the failures remain reproducible.

From the repository root run `python3 tools/design_checks.py`. This reads the
actual DXFs and checks hole vertices against the envelope; it is not a full CAD
validation. See `25_readiness_review.md` R02–R04 and `27_manufacturing_release.md`
for required redesign, review, regenerated artifact and inspection evidence.

Do not generate cutter paths from these files until a reviewed replacement
release identifies part revisions, datums, units, tolerances and mating parts.
