import cadquery as cq
import math

# Afterburner V-gutter flame holder.
# Reconstructed (2026-11) as a valid single solid: the previous bow-tie
# revolve profile was self-intersecting and produced a zero-volume sliver
# plus a detached glow-plug boss. Envelope and features per 14 §Component 3:
# OD 80, ID 40, flange 100/80 x 3, 4x M4 on 95 PCD, 6 radial arms,
# M10 glow-plug boss. The V-gutter is a 1.5 mm chevron ring with apex at
# mid-radius, joined to the flange by the six arms.

outer_od = 80.0
inner_id = 40.0
flg_od = 100.0
flg_t = 3.0
apex_z = 18.0          # apex height above flange face
wall = 1.5             # chevron wall thickness
n_arms = 6
arm_width = 6.0
arm_h = 6.0
glowplug_d = 10.0
glow_boss_od = 14.0
pcd = 95.0
bolt_dia = 4.3
n_bolts = 4

outer_r = outer_od / 2
inner_r = inner_id / 2
apex_r = (inner_r + outer_r) / 2

# --- Mounting flange (z = 0 .. flg_t) ---
flange = cq.Workplane("XY").circle(flg_od / 2).circle(outer_r).extrude(flg_t)
for i in range(n_bolts):
    a = i * 360.0 / n_bolts
    bx = pcd / 2 * math.cos(math.radians(a))
    by = pcd / 2 * math.sin(math.radians(a))
    flange = (
        flange.faces("<Z").workplane()
        .transformed(offset=(bx, by, 0))
        .circle(bolt_dia / 2)
        .cutThruAll()
    )

# --- V-gutter chevron ring (solid V minus an inner V = constant shell) ---
# Two simple triangles avoid the self-intersection of the old bow-tie profile.
v_outer_tri = [(outer_r, flg_t), (apex_r, flg_t + apex_z), (inner_r, flg_t)]
v_inner_tri = [
    (outer_r - wall, flg_t),
    (apex_r, flg_t + apex_z - wall),
    (inner_r + wall, flg_t),
]
v_outer = (
    cq.Workplane("XZ").polyline(v_outer_tri).close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
v_inner = (
    cq.Workplane("XZ").polyline(v_inner_tri).close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)
v_ring = v_outer.cut(v_inner)

body = flange.union(v_ring)

# --- Outer and inner housing walls, continuing the section to 35 mm ---
section_len = 35.0
outer_wall = (
    cq.Workplane("XY").circle(outer_r).circle(outer_r - wall)
    .extrude(section_len - flg_t).translate((0, 0, flg_t))
)
inner_wall = (
    cq.Workplane("XY").circle(inner_r + wall).circle(inner_r)
    .extrude(section_len - flg_t).translate((0, 0, flg_t))
)
body = body.union(outer_wall).union(inner_wall)

# --- Six radial stabiliser arms (overlap flange and V base) ---
arm_cx = (inner_r + flg_od / 2) / 2
for i in range(n_arms):
    a = i * 360.0 / n_arms
    arm = (
        cq.Workplane("XY")
        .transformed(offset=(arm_cx, 0, 0), rotate=(0, 0, a))
        .rect(flg_od / 2 - inner_r, arm_width)
        .extrude(arm_h)
    )
    body = body.union(arm)

# --- Glow-plug boss, radial through the chevron at z = 10 ---
boss_z = 10.0
boss_x0 = 24.0
boss = (
    cq.Workplane("YZ")
    .transformed(offset=(0, boss_z, boss_x0))
    .circle(glow_boss_od / 2)
    .extrude(outer_r - boss_x0 + 2.0)
)
hole = (
    cq.Workplane("YZ")
    .transformed(offset=(0, boss_z, boss_x0 - 1))
    .circle(glowplug_d / 2)
    .extrude(outer_r - boss_x0 + 4.0)
)
body = body.union(boss.cut(hole))

cq.exporters.export(body, "ab_flameholder.step")
print("Exported ab_flameholder.step (single solid target)")
