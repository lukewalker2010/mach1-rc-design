// ab_liner.scad — Afterburner liner with outer shell and film cooling holes
// All dimensions in mm.

// ===== PARAMETERS =====
liner_id      = 80.0;  // Inner liner ID (combustion chamber)
liner_wall    = 1.0;   // Inner liner wall (Inconel 625)
liner_len     = 200.0; // Liner total length
shell_id      = 90.0;  // Outer shell ID
shell_wall    = 1.5;   // Outer shell wall (304 SS)
annular_gap   = 5.0;   // Gap = (shell_id - liner_od) / 2
cool_holes_n  = 20;    // Number of film cooling holes
cool_hole_d   = 1.0;   // Cooling hole diameter
cool_hole_row = 10.0;  // Distance from inlet for cooling holes
cool_hole_angle = 30;  // Hole angle from radial (downstream)

$fn = 64;

liner_od = liner_id + 2 * liner_wall;
shell_od = shell_id + 2 * shell_wall;

module inner_liner() {
    difference() {
        cylinder(h=liner_len, d=liner_od);
        translate([0, 0, -0.01])
            cylinder(h=liner_len + 0.02, d=liner_id);
        // Film cooling holes at inlet end
        for (i = [0 : cool_holes_n - 1]) {
            angle = i * 360 / cool_holes_n;
            x = liner_od/2 * cos(angle);
            y = liner_od/2 * sin(angle);
            translate([x, y, cool_hole_row])
            rotate([0, cool_hole_angle, angle + 90])
                cylinder(d=cool_hole_d, h=liner_wall * 4, center=true);
        }
    }
}

module outer_shell() {
    difference() {
        cylinder(h=liner_len, d=shell_od);
        translate([0, 0, -0.01])
            cylinder(h=liner_len + 0.02, d=shell_id);
    }
}

module cooling_air_inlet() {
    // 10mm tube, threaded for NPT, positioned at x=120mm from start
    translate([shell_od/2, 0, 120])
    rotate([0, -90, 0])
    difference() {
        cylinder(d=10.0, h=15.0);
        cylinder(d=6.0, h=15.0);
    }
}

module assembly() {
    color("gold")
        inner_liner();
    color("silver")
        outer_shell();
    color("blue")
        cooling_air_inlet();
}

assembly();

// Transparent view helper - comment out for STL export
// %translate([0, 0, -0.5]) cylinder(h=liner_len+1, d=shell_od+2);
