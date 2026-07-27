import cadquery as cq
import math

inlet_id = 35.0
outlet_id = 80.0
body_len = 94.0
wall_t = 1.5

inlet_flg_od = 50.0
inlet_flg_t = 3.0
inlet_pcd = 45.0
inlet_bolt = 3.2
inlet_nhole = 4

outlet_flg_od = 100.0
outlet_flg_t = 3.0
outlet_pcd = 95.0
outlet_bolt = 4.3
outlet_nhole = 4

result = cq.Workplane("XY")

inlet_flg = cq.Workplane("XY").circle(inlet_flg_od / 2).circle(inlet_id / 2).extrude(inlet_flg_t)
for i in range(inlet_nhole):
    a = i * 360.0 / inlet_nhole
    x = inlet_pcd / 2 * math.cos(math.radians(a))
    y = inlet_pcd / 2 * math.sin(math.radians(a))
    inlet_flg = inlet_flg.faces("<Z").workplane().transformed(offset=(x, y, 0)).circle(inlet_bolt / 2).cutThruAll()
result = inlet_flg

body_outer = (
    cq.Workplane("XY").circle((inlet_id + 2 * wall_t) / 2)
    .workplane(offset=body_len).circle((outlet_id + 2 * wall_t) / 2).loft()
)
body_inner = (
    cq.Workplane("XY").circle(inlet_id / 2)
    .workplane(offset=body_len + 0.01).circle(outlet_id / 2).loft()
)
body = body_outer.cut(body_inner).translate((0, 0, inlet_flg_t))
result = result.union(body)

outlet_flg = (
    cq.Workplane("XY").transformed(offset=(0, 0, inlet_flg_t + body_len))
    .circle(outlet_flg_od / 2).circle(outlet_id / 2).extrude(outlet_flg_t)
)
for i in range(outlet_nhole):
    a = i * 360.0 / outlet_nhole
    x = outlet_pcd / 2 * math.cos(math.radians(a))
    y = outlet_pcd / 2 * math.sin(math.radians(a))
    outlet_flg = outlet_flg.faces("<Z").workplane().transformed(offset=(x, y, 0)).circle(outlet_bolt / 2).cutThruAll()
result = result.union(outlet_flg)

cq.exporters.export(result, "ab_transition.step")
print("Exported ab_transition.step — z=0 to 100")
