// ab_spray_ring.scad — Annular spray ring fuel injector manifold
// All dimensions in mm.

// ===== PARAMETERS =====
ring_id     = 70.0;   // Manifold ring inner diameter
ring_od     = 80.0;   // Manifold ring outer diameter
ring_wall   = 2.0;    // Manifold tube wall thickness (Inconel 625)
n_injectors = 6;      // Number of injectors
inj_angle   = 15;     // Injector downstream angle from radial (degrees)
orifice_d   = 0.5;    // Injector orifice diameter
inj_tube_od = 2.0;    // Injector tube outer diameter (check valve housing)
inj_tube_len = 12.0;  // Injector tube protrusion length
fuel_tube_od = 4.0;   // Fuel supply tube outer diameter
fuel_tube_id = 2.5;   // Fuel supply tube inner diameter

$fn = 64;

module manifold_ring() {
    tube_center_r = (ring_id + ring_od) / 4;
    tube_d = (ring_od - ring_id) / 2;
    difference() {
        rotate_extrude()
            translate([tube_center_r, 0, 0])
                circle(d=tube_d);
        rotate_extrude()
            translate([tube_center_r, 0, 0])
                circle(d=tube_d - 2*ring_wall);
    }
}

module injector_port(angle) {
    rotate([0, 0, angle])
    translate([ring_od/2, 0, 0])
    rotate([0, -inj_angle, 0])
    union() {
        cylinder(d=inj_tube_od, h=inj_tube_len);
        translate([0, 0, -0.01])
            cylinder(d=orifice_d, h=inj_tube_len + 0.02);
    }
}

module fuel_supply_entry() {
    rotate([0, 90, 0])
    difference() {
        cylinder(d=fuel_tube_od, h=25.0);
        cylinder(d=fuel_tube_id, h=25.0);
    }
}

manifold_ring();

for (i = [0 : n_injectors - 1]) {
    injector_port(i * 360 / n_injectors);
}

translate([ring_od/2, 0, 0])
    fuel_supply_entry();
