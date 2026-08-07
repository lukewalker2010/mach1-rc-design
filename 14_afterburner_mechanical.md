# Afterburner for JetCat P550-PRO — Mechanical Design

> **CORRECTED 2026-08-06 per 18 §2 and 21: mass flow at M1/10kft is 1.10 kg/s (not 0.69); see 21_afterburner_bench_program.md.** Mechanical dimensions, materials and the component stack are **unchanged**. Only mass-flow-dependent numbers (thrust claim, fuel flow, cooling flow) below are corrected. Interface I-03 dimensions unchanged.

## Design Overview

| Parameter | Value | Notes |
|-----------|-------|-------|
| Thrust boost | +75–95% wet (451–497 N net) | At M1/10kft, ṁ=1.10 kg/s, T7=1700–1900 K (21 §1); dry 257 N baseline (18 §2.1) |
| Fuel | Jet A1 | Same as main engine |
| Max AB duration | 20 s | Thermal limit of Inconel liner |
| Total weight | ≤ 1.0 kg | Target (est. 0.85 kg; see 17 §2d corrected — 0.97 kg with restored pump) |
| Fuselage dia | ≤ 200 mm | Fits existing airframe |
| Engine mount | 4× M3 on 45 mm PCD | Direct to P550-PRO exhaust flange |
| EGT range | 550–680 °C (partial power); ~1000 K (727 °C) at M1 full dry | Pre-AB gas temperature; 18 §2.1 |
| O₂ in exhaust | ~14 % | Supports sustained combustion |
| Mass flow | 0.93 kg/s (static SL), 1.10 kg/s (M1/10kft) | corrected-flow model (18 §2.1) — NOT 0.69 |

## Component Stack (Engine Aft → Forward)

```
 ┌───────────┬───────────┬──────────┬───────────┬───────────┐
 │ Transition │ Spray Ring │ Flame    │ Combustion │ Variable  │
 │ Duct       │ / Fuel Inj │ Holder   │ Liner      │ Iris Noz  │
 │ (100 mm)   │ (15 mm)    │ (35 mm)  │ (200 mm)   │ (35 mm)   │
 └───────────┴───────────┴──────────┴───────────┴───────────┘
 │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
 0 mm         100 mm     115 mm     150 mm        350 mm      385 mm
```

### Assembly Overview

```
         Cooling Air Inlet                  Film Cooling Holes
              ↓                                    ↓
  ┌─────┐ ┌─────┐ ┌──────┐ ┌──────────────────┐ ┌──────┐
  │     │ │     │ │      │ │                  │ │      │
  │ 1.  │ │ 2.  │ │ 3.   │ │ 4. Liner         │ │ 5.   │
  │ Trans│ │Spray│ │Flame │ │ (Inconel inside  │ │Iris  │
  │ Duct │ │Ring │ │Holder│ │  304SS shell)    │ │Nozzle│
  │ 35→80│ │ 6x  │ │V-gut │ │                  │ │Var.  │
  │      │ │inj. │ │45°   │ │                  │ │Area  │
  └──────┘ └─────┘ └──────┘ └──────────────────┘ └──────┘
   ↑         ↑                          ↑
  P550     Fuel In                     Hot Gas
  Flange   (Jet A1)                    Exit
```

## Material Selection

| Component | Material | Rationale |
|-----------|----------|-----------|
| Transition duct | Inconel 625 | 680°C EGT direct exposure |
| Spray ring | Inconel 625 | Flame zone, fuel wetting |
| Flame holder | Inconel 625 | Direct flame contact, 45° V-gutter |
| Inner liner | Inconel 625 | 1500-1800°C core, film cooled |
| Outer shell | 304 SS | <400°C (cooling annulus), structural |
| Iris petals | Inconel 625 | Hot gas path, variable geometry |
| Sync ring | 304 SS | Cool zone, structural only |
| Pivot bushings | Ceramic (ZrO₂) | High temp, low friction |
| Fasteners | Inconel 718 | At flanges (M3/M4 bolts) |

## Sizing Calculations

### Throat Area Requirements

- Dry throat: 45 mm dia → Area = π/4 × 45² = 1590 mm²
- Wet throat: 55 mm dia → Area = π/4 × 55² = 2376 mm²
- Area ratio: 2376/1590 = 1.49 (49% increase)

At M1/10kft (1.10 kg/s, ~1000 K pre-AB per 18 §2.1):
- AB raises exhaust temp to T7 = 1800 K (design)
- Volume increase ~ 1800/1000 ≈ 1.80×
- **Nozzle-matching flag:** the 1.49× throat area increase (45→55 mm) was sized on the old 1.56× model; the corrected ratio (1.80×) must be re-verified on the bench (21 §4 Phase 1.5). Interface I-03 dimensions unchanged.

### Cooling Air Flow

- Annulus area: π/4 × (90² - 82²) = π/4 × (8100 - 6724) = 1080 mm²
- At ~5% bleed from compressor: 0.05 × 1.10 = 0.055 kg/s (corrected to ṁ = 1.10 kg/s, 18 §2.1)
- Velocity in annulus: 0.055 / (1.2 × 1080e-6) ≈ 42 m/s
- Film cooling: **105–115 × 1 mm holes** (corrected from 20; bleed 2.5% = 0.0275 kg/s → ~111 holes at 2.47e-4 kg/s choked per hole, 21 §3). The 20-hole row is insufficient at corrected flow.

### Weight Budget

| Component | Est. Mass (g) |
|-----------|--------------|
| Transition duct (Inconel) | 85 |
| Spray ring (Inconel) | 45 |
| Flame holder (Inconel) | 95 |
| Liner + shell (Inconel+304SS) | 280 |
| Iris nozzle (Inconel+304SS) | 120 |
| Fasteners + fittings | 50 |
| Servo + pushrod | 35 |
| Fuel tube + fittings | 15 |
| Glow plug | 25 |
| **Total** | **750** |

Budget ≤ 1000 g. Margin: 250 g.

---

## Component 1: Transition Duct

Expands 35 mm ID (P550 exhaust) → 80 mm ID (AB section) over 100 mm.

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Inlet ID | 35.0 mm | Matches P550 turbine exit |
| Outlet ID | 80.0 mm | AB section diameter |
| Length | 100.0 mm | Conical section |
| Wall thickness | 1.5 mm | Inconel 625 |
| Inlet flange OD | 50.0 mm | 4× M3 holes on 45 mm PCD |
| Outlet flange OD | 100.0 mm | 4× M4 holes on 95 mm PCD |
| Inlet flange thick | 3.0 mm | |
| Outlet flange thick | 3.0 mm | |
| Material | Inconel 625 | |

### OpenSCAD: `ab_transition.scad`

```openscad
// ab_transition.scad — Transition Duct: P550-PRO (35mm) → AB section (80mm)
// All dimensions in mm. Render with: openscad -o ab_transition.stl ab_transition.scad

inlet_id     = 35.0;   // Inlet ID matching P550 exhaust
outlet_id    = 80.0;   // Outlet ID matching AB section
length       = 100.0;  // Duct axial length
wall_t       = 1.5;    // Wall thickness (Inconel 625)

inlet_flg_od = 50.0;   // Inlet flange outer diameter
inlet_flg_t  = 3.0;    // Inlet flange thickness
inlet_pcd    = 45.0;   // Inlet bolt PCD
inlet_bolt   = 3.2;    // M3 clearance hole (3.0mm + 0.2mm)
inlet_nhole  = 4;      // Number of inlet bolts

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
```

### Fabrication Notes

1. **CNC lathe or spin forming**: The conical body should be spun from 1.5 mm Inconel 625 sheet. If spin forming is unavailable, fabricate from rolled and welded sheet, then TIG weld.
2. **Flanges**: Waterjet or laser cut from 3 mm Inconel 625 plate. Drill M3/M4 clearance holes after cutting.
3. **Welding**: TIG weld flanges to cone body with Inconel 625 filler rod. Pre- and post-weld anneal recommended.
4. **Inspection**: Check concentricity; cone must be coaxial with flanges within 0.1 mm.

---

## Component 2: Spray Ring / Fuel Injection

Annular manifold with 6× injectors angled 15° downstream.

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Ring ID | 70.0 mm | Inner diameter of manifold tube |
| Ring OD | 80.0 mm | Outer diameter of manifold tube |
| Wall thickness | 2.0 mm | Inconel tube |
| Injector count | 6 | Equally spaced |
| Injector angle | 15° | Downstream from radial |
| Orifice dia | 0.5 mm | Each injector |
| Fuel supply tube OD | 4.0 mm | Single entry from fuselage side |
| Mounting | Sandwiched | Between transition and flame holder |

### OpenSCAD: `ab_spray_ring.scad`

```openscad
// ab_spray_ring.scad — Annular spray ring fuel injector manifold
// All dimensions in mm.

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
```

### Fabrication Notes

1. **Ring**: Bend 6 mm OD × 2 mm wall Inconel tube into a torus. Weld the seam.
2. **Injectors**: Braze six 2 mm OD Inconel tubes into the ring at 60° spacing. Drill 0.5 mm orifices.
3. **Angle**: The 15° downstream angle ensures fuel enters the high-velocity core rather than wetting the walls.
4. **Check valve**: Commercially available miniature spring-loaded check valves (e.g., The Lee Co.) press-fit into injector tubes. Prevents fuel drip during AB off-transient.
5. **Mounting**: The spray ring is sandwiched between the transition duct outlet flange and the flame holder section inlet flange. Gaskets on both sides.

---

## Component 3: Flame Holder Section

Annular V-gutter with 6 radial stabilizer arms.

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Outer V-gutter OD | 80.0 mm | |
| Inner V-gutter ID | 40.0 mm | Annular flow path |
| V-gutter angle | 45° | Half-angle; 90° included |
| Radial height | 15.0 mm | Vane depth |
| Section length | 30.0 mm | Axial extent |
| Radial arms | 6 | Connect inner/outer V-gutters |
| Arms width | 6.0 mm | |
| Wall thickness | 1.5 mm | Inconel 625 |
| Glow plug thread | 10.0 mm | M10 × 1.0 threaded hole |
| Mounting | 4× M4 on 95 mm PCD | Matches transition duct outlet |

### OpenSCAD: `ab_flameholder.scad`

```openscad
// ab_flameholder.scad — Annular V-gutter flame holder with stabilizer arms
// All dimensions in mm.

outer_od    = 80.0;   // Outer V-gutter outer diameter
inner_id    = 40.0;   // Inner V-gutter inner diameter
v_angle     = 45;     // V-gutter half-angle (degrees); included = 90
radial_h    = 15.0;   // Radial height of V-gutter vane
section_len = 30.0;   // Axial length
wall_t      = 1.5;    // Material thickness (Inconel 625)
n_arms      = 6;      // Number of radial stabilizer arms
arm_width   = 6.0;    // Width of each radial arm
glowplug_d  = 10.0;   // Glow plug threaded hole (M10x1.0)

flg_od      = 100.0;  // Flange OD
flg_t       = 3.0;    // Flange thickness
pcd         = 95.0;   // Bolt PCD
bolt_dia    = 4.3;    // M4 clearance hole
n_bolts     = 4;      // Number of bolts

$fn = 64;

module v_gutter_profile() {
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
```

### Fabrication Notes

1. **V-gutter rings**: CNC lathe or waterjet from 1.5 mm Inconel sheet, then form into V shape using a press brake or roller. Weld seams.
2. **Radial arms**: TIG weld six 6 mm × 30 mm Inconel strips between inner and outer V-rings.
3. **Glow plug boss**: Weld a 14 mm OD × 8 mm Inconel boss to one radial arm. Drill and tap M10×1.0. Use a ceramic glow plug (e.g., RC model type).
4. **Flanges**: Weld at upstream face only (downstream is the V-gutter wake).

---

## Component 4: Afterburner Liner

Concentric inner liner + outer shell with film cooling.

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Liner ID | 80.0 mm | Inner combustion chamber |
| Liner wall | 1.0 mm | Inconel 625 |
| Liner length | 200.0 mm | 150 mm combustion + 50 mm transition |
| Shell ID | 90.0 mm | |
| Shell wall | 1.5 mm | 304 stainless steel |
| Annular gap | 5.0 mm | Cooling air passage |
| Cooling holes | 20 × 1.0 mm | At inlet end, circumferential |
| Total length | 200.0 mm | |

### OpenSCAD: `ab_liner.scad`

```openscad
// ab_liner.scad — Afterburner liner with outer shell and film cooling holes
// All dimensions in mm.

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
```

### Fabrication Notes

1. **Liner**: Roll 1.0 mm Inconel 625 sheet to 80 mm ID tube, TIG weld longitudinal seam.
2. **Shell**: Roll 1.5 mm 304 SS sheet to 90 mm ID tube, TIG weld seam.
3. **Spacers**: 3× circumferential spacer ribs (5 mm tall, 3 mm wide) at 50 mm intervals keep the liner centered in the shell. Weld to shell only (liner floats axially for thermal expansion).
4. **Cooling holes**: Laser drill or EDM 20 holes, 1.0 mm dia, at 30° angle, 10 mm from inlet.
5. **Cooling air inlet**: Weld 10 mm OD 304 SS tube into shell at mid-length (120 mm from inlet). Tap for 1/8" NPT.

---

## Component 5: Variable Iris Nozzle

6 overlapping petals actuated by a single servo via a rotating sync ring.

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Petal count | 6 | Equally spaced |
| Throat (closed) | 45 mm dia | Dry operation |
| Throat (open) | 55 mm dia | Wet operation (+49% area) |
| Petal length | 30.0 mm | Axial |
| Petal thickness | 1.5 mm | Inconel 625 |
| Overlap angle | 10° | Per side, for sealing |
| Pivot pin | 3.0 mm | Inconel rod |
| Bushing | 5.0 mm OD | Zirconia ceramic |
| Sync ring OD/ID | 95/80 mm | 304 SS |
| Sync ring thick | 5.0 mm | |
| Slot length | 12.0 mm | For follower pin travel |
| Servo pushrod | 30.0 mm | |

### OpenSCAD: `ab_iris_nozzle.scad`

```openscad
// ab_iris_nozzle.scad — 6-petal variable iris nozzle with sync ring actuation
// All dimensions in mm.

n_petals     = 6;      // Number of petals
throat_dry   = 45.0;   // Throat diameter, dry (closed)
throat_wet   = 55.0;   // Throat diameter, wet (open)
petal_len    = 30.0;   // Petal axial length
petal_t      = 1.5;    // Petal thickness (Inconel 625)
pivot_pin_d  = 3.0;    // Pivot pin diameter (Inconel rod)
bushing_d    = 5.0;    // Ceramic bushing OD
mount_ring_od = 100.0; // Mounting ring outer diameter
mount_ring_id = 84.0;  // Mounting ring inner diameter
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

overlap_angle   = 10;   // Degrees of circumferential overlap
petal_span      = 360/n_petals + overlap_angle;
pivot_r = mount_ring_od / 2 - 4.0;
closed_r = throat_dry / 2;
open_r   = throat_wet / 2;

module sector(radius, angle) {
    intersection() {
        circle(r=radius);
        polygon(points=[
            [0, 0],
            [radius * cos(-angle/2), radius * sin(-angle/2)],
            [radius * cos(angle/2), radius * sin(angle/2)]
        ]);
    }
}

module single_petal(throat_r) {
    exit_r = throat_r + petal_len * 0.105;
    intersection() {
        rotate([0, 0, -petal_span/2])
        linear_extrude(height=petal_len, scale=exit_r/throat_r)
            sector(2 * throat_r + 12, petal_span);
        rotate([0, 0, -petal_span/2 + 1])
        linear_extrude(height=petal_len, scale=exit_r/throat_r)
            sector(2 * throat_r, petal_span);
    }
}

module petal_assembly(position) {
    throat_r = position == "closed" ? closed_r : open_r;
    for (i = [0 : n_petals - 1]) {
        angle = i * 360 / n_petals;
        rotate([0, 0, angle])
        union() {
            color("gold")
                single_petal(throat_r);
            translate([pivot_r, 0, 0])
                cylinder(d=pivot_pin_d, h=petal_len + 2);
            translate([pivot_r - 2, 0, petal_len])
                cylinder(d=2.5, h=6.0);
        }
    }
}

module sync_ring() {
    difference() {
        cylinder(d=sync_ring_od, h=sync_ring_t);
        translate([0, 0, -0.01])
            cylinder(d=sync_ring_id, h=sync_ring_t + 0.02);
        for (i = [0 : n_petals - 1]) {
            angle = i * 360 / n_petals;
            rotate([0, 0, angle])
            translate([pivot_r - 2 - slot_len/2, 0, -0.01])
                square([slot_width, slot_len]);
        }
        rotate([0, 0, 0])
        translate([pivot_r - 2, 0, -0.01])
            circle(d=3.0);
    }
}

module servo_actuator() {
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
        for (i = [0 : n_petals - 1]) {
            angle = i * 360 / n_petals;
            rotate([0, 0, angle])
            translate([pivot_r, 0, -0.01])
                cylinder(d=pivot_pin_d + 0.2, h=flg_t + 0.02);
        }
    }
}

module limit_stops() {
    for (s = [-1, 1]) {
        translate([sync_ring_od/2 + 2, s * 8, sync_ring_t/2])
            cylinder(d=4.0, h=sync_ring_t);
    }
}

show_position = "closed";

mounting_ring();

translate([0, 0, flg_t])
    petal_assembly(show_position);

translate([0, 0, flg_t + petal_len + 1])
    sync_ring();

translate([0, 0, flg_t + petal_len + 1])
    servo_actuator();

translate([0, 0, flg_t + petal_len + 1])
    limit_stops();
```

### Iris Mechanism Detail

```
                     Sync Ring (rotates)
                   ┌───────────────────┐
                   │  ╱  ╲  ╱  ╲  ╱  ╲│
                   │ ╱    ╲    ╲    ╲ │
                   │╱ slot ╲    ╲    ╲│
                   │        ╲    ╲    │
                   │ follower pin    │
                   │   ↓  ↓  ↓      │
                   │ Petal Pivot (fixed)
          ┌────────┴───────────────────┴────────┐
          │                                      │
          │         Petals (6)                    │
          │     ┌───┐ ┌───┐ ┌───┐               │
          │     │   │ │   │ │   │               │
          │     └───┘ └───┘ └───┘               │
          │        Throat (variable)              │
          └──────────────────────────────────────┘
```

**Actuation**: A standard RC servo (e.g., Hitec HS-645MG) rotates the sync ring via a pushrod. The sync ring's slots engage follower pins on each petal, rotating all petals simultaneously around their pivot pins. Limit stops (two mechanical stops on the sync ring travel) prevent over-rotation.

### Fabrication Notes

1. **Petals**: Waterjet or laser cut from 1.5 mm Inconel 625 sheet. Each petal is a trapezoidal sector.
2. **Pivot pins**: 3 mm Inconel rod, silver-soldered into the mounting ring. Ceramic (ZrO₂) bushings pressed into petal pivot holes.
3. **Follower pins**: 2.5 mm Inconel pins welded to the back (cool side) of each petal, at the pivot radius minus ~2 mm lever arm.
4. **Sync ring**: Waterjet or laser cut from 5 mm 304 SS plate. CNC mill the slots.
5. **Assembly sequence**: Mounting ring → pivot pins → petals (with ceramic bushings) → follower pins → sync ring (slots over follower pins) → servo/pushrod → mechanical limit stops.

---

## Component 6: Outer Shell Assembly

The outer shell is the structural backbone. It encloses all components and is the primary load path from the P550 engine mount to the nozzle.

### Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Shell ID | 90.0 mm | |
| Shell OD | 95.0 mm | |
| Wall thick | 1.5 mm | 304 SS |
| Total length | 350.0 mm | From P550 flange to nozzle exit |

### Sections (from engine aft)

| Section | Z Range (mm) | Description |
|---------|-------------|-------------|
| a) Mounting flange | 0–10 mm | 4× M3 on 45 mm PCD, matches P550 |
| b) Transition | 10–100 mm | Expands from 35 to 80 mm (the same geometry as Component 1 but as the outer shell) |
| c) Spray ring section | 100–115 mm | Contains fuel manifold |
| d) Flame holder section | 115–150 mm | Contains V-gutter |
| e) Combustion liner section | 150–350 mm | 80 mm ID liner within 90 mm shell |
| f) Nozzle mounting | 350–385 mm | 4× M4 on 95 mm PCD at exit plane |

*Note: The outer shell is actually the same physical part as the transition duct body + the outer shell of the liner section + the spray ring/flame holder housings, all welded into one continuous assembly. The "sections" above indicate internal stations.*

### Cooling Air Inlet

- 10 mm OD tube, threaded for 1/8" NPT
- Position: 120 mm from P550 flange (at the start of the combustion liner section)
- Through the shell wall into the 5 mm annular gap

### Fabrication

The outer shell is built as a welded assembly:
1. **Forward section** (z=0–115 mm): Same as transition duct (Component 1), fabricated from 1.5 mm Inconel 625.
2. **Middle section** (z=115–150 mm): Short cylindrical housing containing the flame holder. Also Inconel 625.
3. **Aft section** (z=150–385 mm): 304 SS tube, 90 mm ID × 1.5 mm wall.
4. **Weld joint**: Inconel-to-304 SS transition weld at z=150 mm using Inconel 625 filler (compatible with both).
5. **Cooling air inlet**: 304 SS tube TIG welded into the 304 SS shell section.

---

## Assembly Drawing: `ab_assembly.scad`

```openscad
// ab_assembly.scad — Complete afterburner assembly drawing
// Shows all 6 components stacked with labels, bolt locations,
// cooling air path, and fuel flow path.

$fn = 64;

z_transition    = 0;
z_spray_ring    = 100;
z_flameholder   = 115;
z_liner         = 150;
z_iris          = 350;
total_len       = 385;

module label(text, pos, col) {
    color(col)
    translate(pos)
    linear_extrude(height=0.5)
        text(text, size=4, halign="center", valign="center");
}

module transition_duct() {
    color("LightSalmon") {
        cylinder(h=100, d1=38, d2=83);
        cylinder(h=3, d=50);
        translate([0, 0, 100])
            cylinder(h=3, d=100);
    }
}

module spray_ring() {
    color("LightGreen") {
        rotate_extrude()
            translate([37.5, 0, 0])
                circle(d=10);
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
        cylinder(h=30, d=80);
        translate([0, 0, -0.01])
            cylinder(h=30.02, d=40);
        difference() {
            cylinder(h=30, d=80);
            cylinder(h=30, d=40);
            rotate_extrude()
                polygon(points=[
                    [20,0],[20,30],[30,15],[30,15],[40,30],[40,0]
                ]);
        }
        for (i = [0:5]) {
            rotate([0, 0, i*60])
            translate([20, -3, 0])
                cube([20, 6, 30]);
        }
    }
}

module liner() {
    color("Orange") {
        cylinder(h=200, d=93);
        color("Gold")
            translate([0, 0, 0])
                cylinder(h=200, d=82);
        for (i = [0:19]) {
            angle = i * 18;
            translate([41*cos(angle), 41*sin(angle), 10])
                cylinder(d=1, h=3);
        }
    }
}

module iris_nozzle() {
    color("Silver") {
        cylinder(h=3, d=100);
        for (i = [0:5]) {
            rotate([0, 0, i*60])
            translate([0, 0, 0])
            rotate([0, 3, 0])
                cube([30, 2, 30]);
        }
        translate([0, 0, 35])
            cylinder(h=5, d=95);
    }
}

module cooling_arrows() {
    color("Cyan") {
        translate([50, 0, 120])
        rotate([0, -90, 0])
            union() {
                cylinder(d=8, h=20);
                translate([20, 0, 0])
                    cylinder(d1=8, d2=0, h=8);
            }
        for (z = [130, 180, 230, 280, 330]) {
            translate([39, 0, z])
                cube([3, 3, 6]);
        }
    }
}

module fuel_arrows() {
    color("Red") {
        translate([45, 0, 105])
        rotate([0, -90, 0])
            union() {
                cylinder(d=4, h=15);
                translate([15, 0, 0])
                    cylinder(d1=4, d2=0, h=5);
            }
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
    label("1: Transition Duct", [0, 48, 50], "Black");
    label("2: Spray Ring", [0, 48, 108], "Black");
    label("3: Flame Holder", [0, 48, 130], "Black");
    label("4: Combustion Liner", [0, 48, 250], "Black");
    label("5: Iris Nozzle", [0, 48, 365], "Black");
    label("P550 Flange", [0, 48, -5], "Black");
}

module bolt_locations() {
    color("DarkGray") {
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([22.5, 0, -0.5])
                cylinder(d=3, h=4);
        }
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([47.5, 0, 102])
                cylinder(d=4, h=10);
        }
        for (i = [0:3]) {
            rotate([0, 0, i*90])
            translate([47.5, 0, 353])
                cylinder(d=4, h=4);
        }
    }
}

module dimension_lines() {
    color("DarkGray") {
        translate([-60, 0, 0])
        union() {
            cylinder(d=1, h=total_len);
            translate([-5, 0, 0])
                cube([10, 1, 1]);
            translate([-5, 0, total_len-1])
                cube([10, 1, 1]);
        }
        for (z = [0, 100, 115, 150, 350, 385]) {
            translate([-62, 0, z])
                linear_extrude(height=0.5)
                    text(str(z), size=3, halign="center");
        }
    }
}

color("DimGray", 0.3)
    translate([0, 0, -100])
        cylinder(h=100, d=35);

transition_duct();

translate([0, 0, z_transition + 100])
    spray_ring();

translate([0, 0, z_transition + 115])
    flameholder();

translate([0, 0, z_transition + 150])
    liner();

translate([0, 0, z_transition + 350])
    iris_nozzle();

cooling_arrows();
fuel_arrows();
section_labels();
bolt_locations();
dimension_lines();

color("DarkGray", 0.5)
    cylinder(d=1, h=total_len + 20);
```

---

## Bill of Materials

| Item | Qty | Material | Source |
|------|-----|----------|--------|
| Transition duct cone | 1 | Inconel 625, 1.5 mm sheet | Spin form or roll + weld |
| Transition flanges | 2 | Inconel 625, 3 mm plate | Waterjet/laser cut |
| Spray ring tube | 1 | Inconel 625, 6 mm OD × 2 mm wall | Bent and welded |
| Injector tubes | 6 | Inconel 625, 2 mm OD | Brazed into ring |
| Check valves | 6 | Stainless steel | The Lee Co. or equivalent |
| V-gutter inner ring | 1 | Inconel 625, 1.5 mm sheet | Formed and welded |
| V-gutter outer ring | 1 | Inconel 625, 1.5 mm sheet | Formed and welded |
| Radial arms | 6 | Inconel 625, 1.5 mm strip | TIG welded |
| Glow plug | 1 | Ceramic + Inconel | RC model glow plug (M10) |
| Inner liner tube | 1 | Inconel 625, 1.0 mm sheet | Rolled + welded |
| Outer shell tube | 1 | 304 SS, 1.5 mm sheet | Rolled + welded |
| Cooling air inlet | 1 | 304 SS, 10 mm tube | TIG welded |
| Spacer ribs | 3 | 304 SS, 3 mm strip | TIG welded |
| Iris petals | 6 | Inconel 625, 1.5 mm sheet | Waterjet/laser cut |
| Pivot pins | 6 | Inconel 718, 3 mm rod | Machined |
| Ceramic bushings | 6 | ZrO₂ (zirconia) | Precision ceramic |
| Sync ring | 1 | 304 SS, 5 mm plate | Waterjet + CNC mill |
| Follower pins | 6 | Inconel 718, 2.5 mm rod | TIG welded to petals |
| Servo | 1 | Standard RC | Hitec HS-645MG or equiv. |
| Servo pushrod | 1 | 304 SS, 3 mm rod | Threaded ends |
| Limit stops | 2 | 304 SS | Machined |
| M3×12 bolts | 4 | Inconel 718 | P550 flange mount |
| M4×16 bolts | 8 | Inconel 718 | Section flanges |
| M4×12 bolts | 4 | Inconel 718 | Nozzle mount |
| Washers | 16 | Inconel 718 | All flanges |

---

## Manufacturing Sequence

### Step 1: Fabricate Outer Shell (Monocoque)
1. Roll and weld the 304 SS aft section (z=150–385 mm): 90 mm ID, 200 mm long.
2. Spin form or roll-weld the Inconel forward section (z=0–150 mm): conical transition from 35 mm to 90 mm ID.
3. Weld the Inconel and 304 SS sections together at z=150 mm using Inconel 625 filler.
4. Weld the cooling air inlet (10 mm tube) into the 304 SS section at z=120 mm. Tap for 1/8" NPT.
5. Weld the P550 mounting flange at z=0. Drill 4× M3 clearance holes on 45 mm PCD.
6. Weld the nozzle mounting ring (100 mm OD × 3 mm) at z=350 mm. Drill 4× M4 holes on 95 mm PCD.

### Step 2: Fabricate Inner Subassemblies
1. **Spray ring**: Bend Inconel tube into torus, braze injectors, install check valves.
2. **Flame holder**: Form V-gutter rings, weld radial arms and glow plug boss.
3. **Liner**: Roll Inconel sheet, weld seam, laser-drill cooling holes. Install spacer ribs.

### Step 3: Assemble Internals
1. Insert spray ring between forward shell section and flame holder section. Use thin Inconel gaskets.
2. Insert flame holder assembly at z=115 mm. Bolt through shell using M4 bolts through all three layers (transition flange + spray ring + flame holder flange).
3. Insert liner into 304 SS shell section. The spacer ribs center the liner; the liner floats axially.
4. Wire the glow plug through a 10 mm hole in the shell at the flame holder station.

### Step 4: Fabricate and Attach Nozzle
1. Cut 6 petals from 1.5 mm Inconel sheet.
2. Press ceramic bushings into petal pivot holes.
3. Weld pivot pins into mounting ring.
4. Assemble petals onto pivot pins.
5. Weld follower pins to petals.
6. Install sync ring over follower pins.
7. Attach servo and pushrod. Set limit stops.

### Step 5: Final Assembly
1. Bolt iris nozzle assembly to aft flange.
2. Connect fuel line to spray ring (Swagelok or equivalent fitting).
3. Connect cooling air line (1/8" NPT to fuselage scoop).
4. Static bench test: check fuel distribution, actuate nozzle, verify glow plug ignition.

---

## Thermal Management

### Cooling Air Path
```
Compressor bleed (5%) → fuselage scoop → shell inlet (z=120 mm)
    → 5 mm annular gap (between liner OD and shell ID)
    → flows aft through annulus
    → exits through 105–115 × 1 mm film cooling holes at liner inlet
    → forms protective film on liner ID wall
    → additional cooling exits at liner aft end into nozzle
```

The 5 mm gap ensures:
- Outer shell stays below 400°C (304 SS limit)
- Inner liner film is replenished along the combustion zone
- Pressure drop across cooling holes is sufficient for uniform distribution

### Thermal Expansion

| Component | ΔT (°C) | CTE (μm/m·K) | Expansion over 200 mm |
|-----------|---------|---------------|----------------------|
| Inner liner (Inconel) | 1200 | 12.8 | 3.07 mm axial |
| Outer shell (304 SS) | 400 | 17.3 | 1.38 mm axial |
| **Differential** | | | **1.69 mm** |

The floating liner mounting + bellows section at the aft end accommodates this differential.

---

## Performance Estimates

### Thrust Boost Calculation

- Dry net thrust (M1/10kft): 257 N (18 §2.1, 13:126) — not 300 N
- AB temperature rise: 1000 K → 1800 K (T7 = T7_AB, design)
- Thrust ratio ≈ √(T7/T5) ≈ √(1800/1000) ≈ 1.34
- Net wet thrust (ṁ = 1.10 kg/s, 18 §2.1): gross 835 N − ram 361 N = **474 N** (design)
- Total boost over dry 257 N: **+85%** (1700 K → +75%, 1900 K → +94%; 21 §1)
- At static conditions (ṁ = 0.95 kg/s): F_s ≈ 721 N at 1800 K

### Fuel Flow

AB fuel flow: **~24 g/s static-SL, 27.3 g/s at M1/10kft** (energy balance, LHV 43 MJ/kg, cp 1200, η 0.90; T5 = 1000 K; 21 §2)
- At 20 s max duration: **546 g ≈ 674 mL (AB only)** consumed
- 6 × 0.5 mm orifices at 4 bar: ~28 g/s total (√ΔP scale of the 3-bar 20 g/s point) — meets the 27.3 g/s requirement with margin
- Pump: dedicated Speck ZY-4S-12V (15), 4 bar / 44 g/s — 1.61× margin

### Specific Fuel Consumption

- Dry SFC (datasheet, SL): ~0.144 kg/(N·h) (13:16)
- Dry SFC at M1/10kft (257 N, engine ~22 g/s): ~0.31 kg/(N·h)
- Wet SFC (M1, 1800 K): (22 + 27 g/s) ÷ 474 N ≈ **0.38 kg/(N·h)**
- Penalty acceptable for 20 s bursts

---

## Safety and Limitations

1. **Max AB duration**: 20 seconds. Beyond this, liner temperatures exceed safe limits and structural integrity degrades.
2. **Cooling air mandatory**: The afterburner must never be operated without cooling air flow. A pressure switch in the cooling air line should interlock the AB fuel valve.
3. **Glow plug**: Must be energized 2 seconds before fuel is admitted. A flame detector (UV sensor or thermocouple) should confirm ignition.
4. **Fuel shutoff**: If AB flameout is detected, fuel must shut off within 0.5 seconds to prevent unburned fuel accumulation and detonation.
5. **Iris nozzle**: The nozzle must fail-safe to the open (wet) position on power loss. Use a spring-return servo or a counterweight.
6. **Material**: Never substitute stainless steel for Inconel in hot sections (above the flame holder). Only the outer shell (protected by the cooling annulus) may be 304 SS.

---

## File Index

| File | Description |
|------|-------------|
| `ab_transition.scad` | Component 1: Transition duct (35→80 mm) |
| `ab_spray_ring.scad` | Component 2: Fuel injection manifold |
| `ab_flameholder.scad` | Component 3: Annular V-gutter flame holder |
| `ab_liner.scad` | Component 4: Combustion liner + cooling shell |
| `ab_iris_nozzle.scad` | Component 5: Variable iris nozzle |
| `ab_assembly.scad` | Assembly drawing (all 6 components) |

All files render with: `openscad -o <output>.stl <filename>.scad`

---

*Design prepared for Mach 1 project. This document contains the complete mechanical design, dimensioned drawings, and OpenSCAD manufacturing code for a JetCat P550-PRO afterburner.*
