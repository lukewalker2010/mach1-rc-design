// ab_assembly.scad — Complete afterburner assembly drawing
// All dimensions in mm. Shows all 6 components stacked with labels.
// Uses include to bring in individual component files.

// ===== PARAMETERS =====
$fn = 64;

// Component positions along Z axis (engine aft is z=0)
z_transition    = 0;    // Transition duct inlet
z_spray_ring    = 100;  // Spray ring (sandwiched)
z_flameholder   = 115;  // Flame holder
z_liner         = 150;  // Liner start
z_iris          = 350;  // Iris nozzle
total_len       = 385;  // Overall assembly length

// Reference dimensions for visualization
outer_shell_od  = 93;   // Shell outer diameter (for display)
p550_flange_z   = 0;

module label(text, pos, col) {
    color(col)
    translate(pos)
    rotate([0, 0, 0])
    linear_extrude(height=0.5)
        text(text, size=4, halign="center", valign="center");
}

// ===== COMPONENT IMPORTS (simplified representations) =====

module transition_duct() {
    color("LightSalmon") {
        // Conical body
        cylinder(h=100, d1=38, d2=83);
        // Inlet flange
        cylinder(h=3, d=50);
        // Outlet flange
        translate([0, 0, 100])
            cylinder(h=3, d=100);
    }
}

module spray_ring() {
    color("LightGreen") {
        // Manifold ring
        rotate_extrude()
            translate([37.5, 0, 0])
                circle(d=10);
        // Injectors
        for (i = [0:5]) {
            rotate([0, 0, i*60])
            translate([40, 0, 0])
            rotate([0, -15, 0])
                cylinder(d=2, h=12);
        }
    }
}

module flameholder() {
    color("LightBlue") {
        // Outer ring
        cylinder(h=30, d=80);
        // Inner cutout
        translate([0, 0, -0.01])
            cylinder(h=30.02, d=40);
        // V-gutter surface
        difference() {
            cylinder(h=30, d=80);
            cylinder(h=30, d=40);
            rotate_extrude()
                polygon(points=[
                    [20,0],[20,30],[30,15],[30,15],[40,30],[40,0]
                ]);
        }
        // Arms
        for (i = [0:5]) {
            rotate([0, 0, i*60])
            translate([20, -3, 0])
                cube([20, 6, 30]);
        }
    }
}

module liner() {
    color("Orange") {
        // Outer shell
        cylinder(h=200, d=93);
        // Inner liner
        color("Gold")
            translate([0, 0, 0])
                cylinder(h=200, d=82);
        // Cooling holes indicator
        for (i = [0:19]) {
            angle = i * 18;
            translate([41*cos(angle), 41*sin(angle), 10])
                cylinder(d=1, h=3);
        }
    }
}

module iris_nozzle() {
    color("Silver") {
        // Mounting ring
        cylinder(h=3, d=100);
        // Petals (simplified, closed position)
        for (i = [0:5]) {
            rotate([0, 0, i*60])
            translate([0, 0, 0])
            rotate([0, 3, 0])
                cube([30, 2, 30]);
        }
        // Sync ring
        translate([0, 0, 35])
            cylinder(h=5, d=95);
    }
}

module cooling_arrows() {
    // Cooling air path arrows
    color("Cyan") {
        // Entry arrow
        translate([50, 0, 120])
        rotate([0, -90, 0])
            union() {
                cylinder(d=8, h=20);
                translate([20, 0, 0])
                    cylinder(d1=8, d2=0, h=8);
            }
        
        // Annulus flow arrows
        for (z = [130, 180, 230, 280, 330]) {
            translate([39, 0, z])
            rotate([0, 0, 0])
                cube([3, 3, 6]);
        }
    }
}

module fuel_arrows() {
    // Fuel flow path arrows
    color("Red") {
        // Entry
        translate([45, 0, 105])
        rotate([0, -90, 0])
            union() {
                cylinder(d=4, h=15);
                translate([15, 0, 0])
                    cylinder(d1=4, d2=0, h=5);
            }
        
        // Injection arrows
        for (i = [0:5]) {
            rotate([0, 0, i*60])
            translate([35, 0, 108])
            rotate([0, -15, 0])
            union() {
                cylinder(d=1, h=8);
                translate([0, 0, 8])
                    cylinder(d1=1, d2=0, h=3);
            }
        }
    }
}

module section_labels() {
    offset_z = -12;
    label("1: Transition Duct", [0, 45, 50], "Black");
    label("2: Spray Ring", [0, 45, 108], "Black");
    label("3: Flame Holder", [0, 45, 130], "Black");
    label("4: Combustion Liner", [0, 45, 250], "Black");
    label("5: Iris Nozzle", [0, 45, 365], "Black");
    label("6: Outer Shell", [0, 55, 250], "Black");
    label("P550 Flange", [0, 45, -5], "Black");
}

module bolt_locations() {
    color("DarkGray") {
        // Inlet bolts (4x M3 on 45 PCD)
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([22.5, 0, -0.5])
                cylinder(d=3, h=4);
        }
        // Flange bolts (4x M4 on 95 PCD) at transition/flameholder interface
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([47.5, 0, 102])
                cylinder(d=4, h=10);
        }
        // Nozzle bolts (4x M4 on 95 PCD)
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([47.5, 0, 353])
                cylinder(d=4, h=4);
        }
    }
}

module dimension_lines() {
    color("DarkGray") {
        // Total length dimension
        translate([-60, 0, 0])
        union() {
            translate([0, 0, 0])
                cylinder(d=1, h=total_len);
            translate([-5, 0, 0])
                cube([10, 1, 1]);
            translate([-5, 0, total_len-1])
                cube([10, 1, 1]);
        }
        // Tick marks
        for (z = [0, 100, 115, 150, 350, 385]) {
            translate([-62, 0, z])
            rotate([0, 0, 0])
                linear_extrude(height=0.5)
                    text(str(z), size=3, halign="center");
        }
    }
}

// ===== MAIN ASSEMBLY =====

// Background engine outline
color("DimGray", 0.3)
    translate([0, 0, -100])
        cylinder(h=100, d=35);

// 1. Transition Duct (0-103 mm)
transition_duct();

// 2. Spray Ring (sandwiched at z=100)
translate([0, 0, z_transition + 100])
    spray_ring();

// 3. Flame Holder (115-145 mm)
translate([0, 0, z_transition + 115])
    flameholder();

// 4. Liner (150-350 mm)
translate([0, 0, z_transition + 150])
    liner();

// 5. Iris Nozzle (350-385 mm)
translate([0, 0, z_transition + 350])
    iris_nozzle();

// Annotation overlays
cooling_arrows();
fuel_arrows();
section_labels();
bolt_locations();
dimension_lines();

// Centroid axis
color("DarkGray", 0.5)
    cylinder(d=1, h=total_len + 20);
