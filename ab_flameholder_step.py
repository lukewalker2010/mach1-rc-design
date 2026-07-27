import cadquery as cq
import math

outer_od = 80.0
inner_id = 40.0
radial_h = 15.0
section_len = 32.0
wall_t = 1.5
n_arms = 6
arm_width = 6.0
glowplug_d = 10.0
flg_od = 100.0
flg_t = 3.0
pcd = 95.0
bolt_dia = 4.3
n_bolts = 4

inner_r = inner_id / 2
outer_r = outer_od / 2
apex_z = section_len / 2

body = cq.Workplane("XY").circle(outer_r).circle(inner_r).extrude(section_len)

v = cq.Workplane("XZ").polyline([
    (inner_r, 0), (inner_r + radial_h, apex_z),
    (outer_r - radial_h, apex_z), (outer_r, 0)
]).close().revolve(360, (0, 0, 0), (0, 0, 1))
body = body.cut(v)

for i in range(n_arms):
    a = i * 360.0 / n_arms
    cx = (inner_r + outer_r) / 2 * math.cos(math.radians(a))
    cy = (inner_r + outer_r) / 2 * math.sin(math.radians(a))
    arm = (
        cq.Workplane("XY").transformed(offset=(cx, cy, 0), rotate=(0, 0, a))
        .rect((outer_r - inner_r), arm_width).extrude(section_len)
    )
    body = body.union(arm)

glow_x = (inner_r + outer_r) / 2
glow = (
    cq.Workplane("YZ").center(0, section_len / 2)
    .circle(7.0).circle(glowplug_d / 2).extrude(8.0)
    .translate((glow_x, 0, 0))
)
body = body.union(glow)

flange = cq.Workplane("XY").circle(flg_od / 2).circle(outer_r).extrude(flg_t)
for i in range(n_bolts):
    a = i * 360.0 / n_bolts
    bx = pcd / 2 * math.cos(math.radians(a))
    by = pcd / 2 * math.sin(math.radians(a))
    flange = flange.faces("<Z").workplane().transformed(offset=(bx, by, 0)).circle(bolt_dia / 2).cutThruAll()

result = flange.union(body.translate((0, 0, flg_t)))

cq.exporters.export(result, "ab_flameholder.step")
print("Exported ab_flameholder.step — z=0 to 35 (flg 3 + body 32)")
