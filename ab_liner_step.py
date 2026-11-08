import cadquery as cq
import math

# Afterburner liner + outer shell.
# Fixes (2026-11): added the three circumferential spacer ribs that the
# fabrication note requires (previously the inner liner and shell exported
# as two unattached solids) and made the cooling-air inlet and film-cooling
# holes radial (they were axial, so they never pierced the wall).

liner_id = 80.0
liner_wall = 1.0
liner_len = 200.0
shell_id = 90.0
shell_wall = 1.5
cool_holes_n = 20
cool_hole_d = 1.0
cool_hole_row = 10.0
rib_thickness = 3.0
rib_stations = (50.0, 100.0, 150.0)

liner_od = liner_id + 2 * liner_wall
shell_od = shell_id + 2 * shell_wall

inner_liner = (
    cq.Workplane("XY")
    .circle(liner_od / 2)
    .circle(liner_id / 2)
    .extrude(liner_len)
)

# Radial film-cooling holes through the liner wall at the inlet row.
for i in range(cool_holes_n):
    angle = i * 360.0 / cool_holes_n
    hole = (
        cq.Workplane("YZ")
        .transformed(offset=(0, cool_hole_row, liner_id / 2 - 0.5))
        .circle(cool_hole_d / 2)
        .extrude(liner_wall + 1.0)
    )
    inner_liner = inner_liner.cut(hole.rotate((0, 0, 0), (0, 0, 1), angle))

outer_shell = (
    cq.Workplane("XY")
    .circle(shell_od / 2)
    .circle(shell_id / 2)
    .extrude(liner_len)
)

# Radial cooling-air inlet, overlapping the shell wall.
cool_inlet = (
    cq.Workplane("YZ")
    .transformed(offset=(0, 120, shell_od / 2 - 1.0))
    .circle(10.0 / 2)
    .circle(6.0 / 2)
    .extrude(15.0)
)

result = inner_liner.union(outer_shell).union(cool_inlet)

# Spacer ribs: weld to the shell in manufacture; modelled attached so the
# exported part is a single connected solid.
for z in rib_stations:
    rib = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, z))
        .circle(shell_id / 2 + 0.5)
        .circle(liner_od / 2 - 0.5)
        .extrude(rib_thickness)
    )
    result = result.union(rib)

cq.exporters.export(result, "ab_liner.step")
print("Exported ab_liner.step (single solid target)")
