// ab_transition.scad — Transition Duct: P550-PRO (35mm) → AB section (80mm)
// All dimensions in mm. Render with: openscad -o ab_transition.stl ab_transition.scad

// ===== PARAMETERS =====
inlet_id     = 35.0;   // Inlet ID matching P550 exhaust
outlet_id    = 80.0;   // Outlet ID matching AB section
length       = 100.0;  // Duct axial length
wall_t       = 1.5;    // Wall thickness (Inconel 625)

// Inlet flange
inlet_flg_od = 50.0;   // Inlet flange outer diameter
inlet_flg_t  = 3.0;    // Inlet flange thickness
inlet_pcd    = 45.0;   // Inlet bolt PCD
inlet_bolt   = 3.2;    // M3 clearance hole (3.0mm + 0.2mm)
inlet_nhole  = 4;      // Number of inlet bolts

// Outlet flange
outlet_flg_od = 100.0;  // Outlet flange outer diameter
outlet_flg_t  = 3.0;    // Outlet flange thickness
outlet_pcd    = 95.0;   // Outlet bolt PCD
outlet_bolt   = 4.3;    // M4 clearance hole (4.0mm + 0.3mm)
outlet_nhole  = 4;      // Number of outlet bolts

$fn = 64;

module flange(od, id, thick, pcd, bolt_dia, n_holes) {
    difference() {
        cylinder(d=od, h=thick);
        translate([0, 0, -0.01])
            cylinder(d=id, h=thick + 0.02);
        for (i = [0 : n_holes - 1]) {
            angle = i * 360 / n_holes;
            translate([pcd/2 * cos(angle), pcd/2 * sin(angle), -0.01])
                cylinder(d=bolt_dia, h=thick + 0.02);
        }
    }
}

module transition_body() {
    difference() {
        translate([0, 0, inlet_flg_t])
            cylinder(h=length, d1=inlet_id + 2*wall_t,
                     d2=outlet_id + 2*wall_t);
        translate([0, 0, inlet_flg_t - 0.01])
            cylinder(h=length + 0.02, d1=inlet_id, d2=outlet_id);
    }
}

flange(inlet_flg_od, inlet_id, inlet_flg_t,
       inlet_pcd, inlet_bolt, inlet_nhole);

transition_body();

translate([0, 0, inlet_flg_t + length])
    flange(outlet_flg_od, outlet_id, outlet_flg_t,
           outlet_pcd, outlet_bolt, outlet_nhole);
