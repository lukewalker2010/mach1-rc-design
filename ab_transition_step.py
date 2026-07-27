import cadquery as cq
import math

inlet_id = 35.0
outlet_id = 80.0
length = 94.0
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

inlet_flange = cq.Workplane("XY").circle(inlet_flg_od / 2).circle(inlet_id / 2).extrude(inlet_flg_t)
for i in range(inlet_nhole):
    angle = i * 360.0 / inlet_nhole
    x = inlet_pcd / 2 * math.cos(math.radians(angle))
    y = inlet_pcd / 2 * math.sin(math.radians(angle))
    inlet_flange = inlet_flange.faces("<Z").workplane().transformed(offset=(x, y, 0)).circle(inlet_bolt / 2).cutThruAll()
result = inlet_flange

body = cq.Workplane("XY").transformed(offset=(0, 0, inlet_flg_t))
body = body.circle((inlet_id + 2 * wall_t) / 2).workplane(offset=length).circle((outlet_id + 2 * wall_t) / 2).loft()
inner = cq.Workplane("XY").transformed(offset=(0, 0, inlet_flg_t - 0.01))
inner = inner.circle(inlet_id / 2).workplane(offset=length + 0.02).circle(outlet_id / 2).loft()
body = body.cut(inner)
result = result.union(body)

outlet_flange = cq.Workplane("XY").transformed(offset=(0, 0, inlet_flg_t + length))
outlet_flange = outlet_flange.circle(outlet_flg_od / 2).circle(outlet_id / 2).extrude(outlet_flg_t)
for i in range(outlet_nhole):
    angle = i * 360.0 / outlet_nhole
    x = outlet_pcd / 2 * math.cos(math.radians(angle))
    y = outlet_pcd / 2 * math.sin(math.radians(angle))
    outlet_flange = outlet_flange.faces("<Z").workplane().transformed(offset=(x, y, 0)).circle(outlet_bolt / 2).cutThruAll()
result = result.union(outlet_flange)

cq.exporters.export(result, "ab_transition.step")
print("Exported ab_transition.step")
