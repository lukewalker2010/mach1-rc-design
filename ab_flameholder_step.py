import cadquery as cq
import math

outer_od = 80.0
inner_id = 40.0
v_angle = 45
radial_h = 15.0
section_len = 30.0
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

body = (
    cq.Workplane("XY")
    .circle(outer_r)
    .circle(inner_r)
    .extrude(section_len)
)

v_profile = (
    cq.Workplane("XZ")
    .polyline([
        (inner_r, 0),
        (inner_r + radial_h, apex_z),
        (outer_r - radial_h, apex_z),
        (outer_r, 0),
    ])
    .close()
)

v_solid = v_profile.revolve(360, (0, 0, 0), (0, 0, 1))

body = body.cut(v_solid)

for i in range(n_arms):
    angle = i * 360.0 / n_arms
    arm = (
        cq.Workplane("XY")
        .transformed(offset=(inner_r, -arm_width / 2, 0))
        .rect((outer_r - inner_r), arm_width)
        .extrude(section_len)
    )
    body = body.union(arm)

glow_x = (inner_r + outer_r) / 2
glow_boss = (
    cq.Workplane("XY")
    .transformed(offset=(glow_x, 0, section_len / 2))
    .circle(7.0)
    .extrude(8.0)
    .faces("<Z")
    .circle(glowplug_d / 2)
    .cutThruAll()
)
body = body.union(glow_boss)

flange = (
    cq.Workplane("XY")
    .circle(flg_od / 2)
    .circle(outer_r)
    .extrude(flg_t)
)
for i in range(n_bolts):
    angle = i * 360.0 / n_bolts
    bx = pcd / 2 * math.cos(math.radians(angle))
    by = pcd / 2 * math.sin(math.radians(angle))
    flange = flange.faces("<Z").workplane().transformed(offset=(bx, by, 0)).circle(bolt_dia / 2).cutThruAll()

result = flange.union(body.translate((0, 0, flg_t)))

cq.exporters.export(result, "ab_flameholder.step")
print("Exported ab_flameholder.step")
