import cadquery as cq
import math

liner_id = 80.0
liner_wall = 1.0
liner_len = 200.0
shell_id = 90.0
shell_wall = 1.5
cool_holes_n = 20
cool_hole_d = 1.0
cool_hole_row = 10.0
cool_hole_angle = 30

liner_od = liner_id + 2 * liner_wall
shell_od = shell_id + 2 * shell_wall

inner_liner = (
    cq.Workplane("XY")
    .circle(liner_od / 2)
    .circle(liner_id / 2)
    .extrude(liner_len)
)

for i in range(cool_holes_n):
    angle = i * 360.0 / cool_holes_n
    rad = math.radians(angle)
    x = liner_od / 2 * math.cos(rad)
    y = liner_od / 2 * math.sin(rad)
    
    hole_axis = (
        cq.Workplane("XY")
        .transformed(offset=(x, y, cool_hole_row))
        .circle(cool_hole_d / 2)
        .extrude(liner_wall * 4)
    )
    
    inner_liner = inner_liner.cut(hole_axis)

outer_shell = (
    cq.Workplane("XY")
    .circle(shell_od / 2)
    .circle(shell_id / 2)
    .extrude(liner_len)
)

cool_inlet = (
    cq.Workplane("XY")
    .transformed(offset=(shell_od / 2, 0, 120))
    .circle(10.0 / 2)
    .circle(6.0 / 2)
    .extrude(15.0)
)

result = inner_liner.union(outer_shell).union(cool_inlet)

cq.exporters.export(result, "ab_liner.step")
print("Exported ab_liner.step")
