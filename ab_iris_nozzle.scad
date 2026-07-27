// ab_iris_nozzle.scad — 6-petal variable iris nozzle with sync ring actuation
// All dimensions in mm.

// ===== PARAMETERS =====
n_petals     = 6;      // Number of petals
throat_dry   = 45.0;   // Throat diameter, dry (closed)
throat_wet   = 55.0;   // Throat diameter, wet (open)
petal_len    = 30.0;   // Petal axial length
petal_t      = 1.5;    // Petal thickness (Inconel 625)
pivot_pin_d  = 3.0;    // Pivot pin diameter (Inconel rod)
bushing_d    = 5.0;    // Ceramic bushing OD
mount_ring_od = 100.0; // Mounting ring outer diameter
mount_ring_id = 84.0;  // Mounting ring inner diameter (fits over 80mm shell)
flg_t        = 3.0;    // Flange thickness
pcd          = 95.0;   // Nozzle mounting bolt PCD
bolt_dia     = 4.3;    // M4 clearance
n_bolts      = 4;

sync_ring_od = 95.0;   // Sync ring outer diameter
sync_ring_id = 80.0;   // Sync ring inner diameter
sync_ring_t  = 5.0;    // Sync ring thickness (304 SS)
slot_width   = 3.5;    // Slot width for petal follower pins
slot_len     = 12.0;   // Slot radial length

servo_arm_len = 30.0;  // Pushrod length from servo to sync ring
pushrod_d     = 3.0;   // Pushrod diameter

$fn = 64;

// Petal geometry
// Each petal covers 360/n_petals + overlap angle
overlap_angle   = 10;   // Degrees of circumferential overlap
petal_span      = 360/n_petals + overlap_angle;

// Pivot radius (where petal pivots on mount ring)
pivot_r = mount_ring_od / 2 - 4.0;

// Closed throat radius
closed_r = throat_dry / 2;
open_r   = throat_wet / 2;

module single_petal(throat_r) {
    // Petal profile: trapezoidal in (r,z) plane
    // Pivot at [pivot_r, 0], throat edge determined by throat_r
    // Petal extends from z=0 to z=petal_len
    // Inner edge contour: linear from throat inlet to outlet
    
    // At z=0 (pivot plane): inner edge radius = throat_r
    // At z=petal_len (exit): inner edge radius = throat_r + petal_len * tan(6deg)
    exit_r = throat_r + petal_len * 0.105; // ~6 deg half-angle
    
    d = petal_span;
    difference() {
        // Petal body - a wedge cut from an annular sector
        intersection() {
            // Outer radius sector
            rotate([0, 0, -petal_span/2])
            linear_extrude(height=petal_len, scale=exit_r/throat_r)
                sector(2 * throat_r + 8, petal_span);
            // Inner wedge
            rotate([0, 0, -petal_span/2])
            linear_extrude(height=petal_len, scale=exit_r/throat_r)
                sector(2 * throat_r, petal_span);
        }
    }
}

module sector(radius, angle) {
    // 2D pie sector at origin
    intersection() {
        circle(r=radius);
        polygon(points=[
            [0,0],
            [radius * cos(-angle/2), radius * sin(-angle/2)],
            [radius * cos(angle/2), radius * sin(angle/2)]
        ]);
    }
}

module petal_assembly(position) {
    // position: "closed" or "open"
    throat_r = position == "closed" ? closed_r : open_r;
    
    for (i = [0 : n_petals - 1]) {
        angle = i * 360 / n_petals;
        rotate([0, 0, angle])
        translate([0, 0, 0])
        union() {
            // Petal body
            color("gold")
                single_petal(throat_r);
            
            // Pivot pin hole indicator
            translate([pivot_r, 0, 0])
                cylinder(d=pivot_pin_d, h=petal_len + 2);
            
            // Follower pin (engages sync ring slot)
            translate([pivot_r - 2, 0, petal_len])
                cylinder(d=2.5, h=6.0);
        }
    }
}

module sync_ring() {
    difference() {
        // Ring body
        cylinder(d=sync_ring_od, h=sync_ring_t);
        translate([0, 0, -0.01])
            cylinder(d=sync_ring_id, h=sync_ring_t + 0.02);
        
        // Slots for follower pins
        for (i = [0 : n_petals - 1]) {
            angle = i * 360 / n_petals;
            rotate([0, 0, angle])
            translate([pivot_r - 2 - slot_len/2, 0, -0.01])
            rotate([0, 0, -90])
                square([slot_width, slot_len]);
        }
        
        // Servo arm connection point
        slot_center = pivot_r - 2;
        rotate([0, 0, 0])
        translate([slot_center, 0, -0.01])
            circle(d=3.0);
    }
}

module servo_actuator() {
    // Simplified servo mounted to outer ring
    rotate([0, 0, 0])
    translate([pivot_r - 2, -12, sync_ring_t])
    union() {
        color("red") {
            cylinder(d=8.0, h=servo_arm_len);
            translate([0, 0, servo_arm_len])
                cylinder(d=3.0, h=5.0);
        }
    }
}

module mounting_ring() {
    difference() {
        cylinder(d=mount_ring_od, h=flg_t);
        translate([0, 0, -0.01])
            cylinder(d=mount_ring_id, h=flg_t + 0.02);
        for (i = [0 : n_bolts - 1]) {
            angle = i * 360 / n_bolts;
            translate([pcd/2 * cos(angle), pcd/2 * sin(angle), -0.01])
                cylinder(d=bolt_dia, h=flg_t + 0.02);
        }
        // Pivot pin holes
        for (i = [0 : n_petals - 1]) {
            angle = i * 360 / n_petals;
            rotate([0, 0, angle])
            translate([pivot_r, 0, -0.01])
                cylinder(d=pivot_pin_d + 0.2, h=flg_t + 0.02);
        }
    }
}

module limit_stops() {
    // Two limit stops on the sync ring path
    for (s = [-1, 1]) {
        translate([sync_ring_od/2 + 2, s * 8, sync_ring_t/2])
            cylinder(d=4.0, h=sync_ring_t);
    }
}

// ===== ASSEMBLY =====
// Change this to "open" to see the wet-configuration throat
show_position = "closed";

// Mounting ring (attached to aft end of liner outer shell)
mounting_ring();

// Petals
translate([0, 0, flg_t])
    petal_assembly(show_position);

// Sync ring
translate([0, 0, flg_t + petal_len + 1])
    sync_ring();

// Servo
translate([0, 0, flg_t + petal_len + 1])
    servo_actuator();

// Limit stops
translate([0, 0, flg_t + petal_len + 1])
    limit_stops();
