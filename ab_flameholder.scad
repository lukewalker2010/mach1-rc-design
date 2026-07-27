// ab_flameholder.scad — Annular V-gutter flame holder with stabilizer arms
// All dimensions in mm.

// ===== PARAMETERS =====
outer_od    = 80.0;   // Outer V-gutter outer diameter
inner_id    = 40.0;   // Inner V-gutter inner diameter
v_angle     = 45;     // V-gutter half-angle (degrees); included = 90
radial_h    = 15.0;   // Radial height of V-gutter vane
section_len = 30.0;   // Axial length
wall_t      = 1.5;    // Material thickness (Inconel 625)
n_arms      = 6;      // Number of radial stabilizer arms
arm_width   = 6.0;    // Width of each radial arm
glowplug_d  = 10.0;   // Glow plug threaded hole (M10x1.0)

// Flanges (match transition outlet)
flg_od      = 100.0;  // Flange OD
flg_t       = 3.0;    // Flange thickness
pcd         = 95.0;   // Bolt PCD
bolt_dia    = 4.3;    // M4 clearance hole
n_bolts     = 4;      // Number of bolts

$fn = 64;

module v_gutter_profile() {
    // V-gutter: V opening upstream. Cross-section in (r,z) plane.
    apex_r  = (inner_id/2 + outer_od/2) / 2;
    apex_z  = section_len / 2;
    poly_points = [
        [inner_id/2, 0],
        [inner_id/2 + radial_h, apex_z],
        [inner_id/2 + radial_h, apex_z],
        [outer_od/2 - radial_h, apex_z],
        [outer_od/2 - radial_h, apex_z],
        [outer_od/2, 0]
    ];
    polygon(poly_points);
}

module v_gutter_ring() {
    rotate_extrude()
        v_gutter_profile();
}

module mounting_flange() {
    difference() {
        cylinder(d=flg_od, h=flg_t);
        translate([0, 0, -0.01])
            cylinder(d=outer_od, h=flg_t + 0.02);
        for (i = [0 : n_bolts - 1]) {
            angle = i * 360 / n_bolts;
            translate([pcd/2 * cos(angle), pcd/2 * sin(angle), -0.01])
                cylinder(d=bolt_dia, h=flg_t + 0.02);
        }
    }
}

module radial_arms() {
    for (i = [0 : n_arms - 1]) {
        rotate([0, 0, i * 360 / n_arms])
        translate([inner_id/2, -arm_width/2, 0])
        linear_extrude(height=section_len)
            square([(outer_od - inner_id)/2, arm_width]);
    }
}

module glow_plug_mount() {
    // Mounted in the wake of radial arm 0
    rotate([0, 0, 0])
    translate([(inner_id + outer_od)/4, 0, section_len/2])
    rotate([0, 90, 0])
    union() {
        cylinder(d=14.0, h=8.0);
        translate([0, 0, -0.01])
            cylinder(d=glowplug_d, h=8.02);
    }
}

mounting_flange();

translate([0, 0, flg_t])
union() {
    difference() {
        cylinder(h=section_len, d=outer_od);
        cylinder(h=section_len, d=inner_id);
        v_gutter_ring();
    }
    radial_arms();
}

translate([0, 0, flg_t])
    glow_plug_mount();
