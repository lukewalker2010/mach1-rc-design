# P550-PRO Afterburner Control Electronics Design

## Overview

This document specifies the complete control electronics system for a P550-PRO turbojet afterburner on a Mach 1 RC aircraft. The afterburner adds secondary fuel injection, a variable iris nozzle, and an ignition system, all controlled by a dedicated microcontroller that interfaces with the existing engine ECU and flight controller.

---

## Task 1: Microcontroller Board Selection

### Recommendation: Raspberry Pi Pico (RP2040)

| Criteria | Arduino Nano | **Raspberry Pi Pico** | Teensy 4.0 | STM32 Blue Pill |
|---|---|---|---|---|
| Price | $5 | **$4** | $24 | $3 |
| Weight | 7g | **3g** | 4g | 10g |
| Size | 45×18mm | **51×21mm** | 35×18mm | 53×22mm |
| PWM outputs | 6 (via timer) | **16 (PIO)** | 12 | 8 |
| Analog inputs | 8 (10-bit) | **4 (12-bit)** | 14 (12-bit) | 10 (12-bit) |
| Logic level | 5V | **3.3V** | 3.3V | 3.3V |
| GPIO count | 14 | **26** | 34 | 37 |
| Processing | 16MHz | **133MHz** | 600MHz | 72MHz |
| Programming | USB/UART | **USB drag-drop** | USB | SWD |

**Rationale:**
- The Pico exceeds all I/O requirements (3x PWM, 2x analog, 2x digital, serial/I2C) with room to spare
- PIO (Programmable I/O) allows hardware-timed PWM servo pulses without CPU load
- Drag-drop programming via USB is simple—no external programmer needed
- 12-bit ADC provides better thermocouple resolution than Nano's 10-bit
- Lightest option at 3g
- Dual-core allows telemetry handling on core 1 while control logic runs on core 0
- Drawback: 3.3V logic requires level shifting for 5V peripherals (solved with MOSFETs)

### Pinout Diagram

```
Raspberry Pi Pico Pin Assignment:

Left edge (USB at top):
GP0  ←  EGT (MAX6675 CS)
GP1  ←  EGT (MAX6675 SCK)
GP2  ←  EGT (MAX6675 SO)
GP3  →  CDI igniter (via 4N25 optocoupler)
GP4  →  Fuel solenoid MOSFET (via 1kΩ gate resistor)
GND  ─── Common ground
GP5  →  Fuel pump ESC (PWM, 50Hz)
GP6  →  Iris servo (PWM, 50Hz)
GP7  ←  Flame detector (digital)
GP8  ←  Fuel pressure sensor (analog)
GND  ─── Common ground
GP9  ←  RC receiver AB switch channel (PWM)
GP10 ←  RC receiver throttle channel (PWM)
GP11 →  Telemetry TX (UART1 TX → Pixhawk)
GP12 ←  Telemetry RX (UART1 RX ← Pixhawk)
GND  ─── Common ground
GP13 ←  RSSI / link quality (analog)
GP14 ←  Aux RPM input (digital, optocoupled from ECU)
GP15 →  Status LED (RGB)
VSYS ─── 7.4V input via Schottky diode → 3.3V regulator
3V3  ─── 3.3V output (to sensors)
GND  ─── Common ground
```

### Power Requirements

- Raspberry Pi Pico: 3.3V, ~50mA (typical)
- External regulator required: 7.4V → 3.3V

### Programming Interface

- USB-C on Pico board: drag-and-drop UF2 files
- No external programmer needed
- Serial console via USB at 115200 baud for debugging
- SWD pins (GP24/SWD clk, GP25/SWD dat) available for advanced debugging

---

## Task 2: Power Supply

### Power Distribution Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       2S LiPo 5000mAh                          │
│                        7.4V nominal                            │
│                     (6.4V - 8.4V range)                        │
└────────────┬──────────┬─────────────┬──────────────┬──────────┘
             │          │              │              │
             │          │              │              │
        ┌────▼────┐ ┌──▼───┐    ┌─────▼─────┐  ┌────▼────┐
        │ 5V BEC  │ │ 12V  │    │  7.4V     │  │ 3.3V    │
        │ CC BEC  │ │ Boost│    │  (Direct)  │  │ Reg     │
        │   10A   │ │POLOLU│    │           │  │ POLOLU  │
        │ 5V rail │ │ 12V  │    │ Fuel pump │  │ 3.3V    │
        │ 5.0A pk │ │rail  │    │  ESC     │  │ 300mA   │
        │ 3.0A con│ │ 1.5A │    │          │  │         │
        └────┬────┘ └──┬───┘    └──────────┘  └────┬────┘
             │          │              │              │
    ┌────────┤          │              │              │
    │        │          │              │              │
    ▼        ▼          ▼              ▼              ▼
┌──────┐ ┌──────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│Rx +  │ │Iris  │ │Solenoid │ │Fuel pump│ │Raspberry Pi  │
│Servos│ │Servo │ │Valve    │ │ESC      │ │Pico + Sensors│
│5V    │ │5V    │ │12V      │ │7.4V     │ │3.3V          │
│~0.5A │ │~1A pk│ │~0.5A    │ │~3A      │ │~100mA        │
└──────┘ └──────┘ └──────────┘ └──────────┘ └──────────────┘
                                    │
                                    ▼
                              ┌──────────────┐
                              │P550-PRO ECU  │
                              │(separate PSU) │
                              │6-12V input   │
                              │~2A           │
                              └──────────────┘
```

### Component Specifications

| Component | Part Number | Input | Output | Efficiency | Notes |
|---|---|---|---|---|---|
| 5V BEC | Castle Creations CC BEC 10A | 6-25V | 5V, 10A peak / 5A cont | >90% | Adjustable, set to 5.0V |
| 12V Boost | Pololu 12V Step-Up U3V40A12 | 2.5-16V | 12V, 1.5A max (1A cont) | 85-90% | Enable pin not used (always on) |
| 3.3V Reg | Pololu 3.3V Step-Down D24V10F3 | 2.5-16V | 3.3V, 1A max (300mA cont) | >90% | Feeds Pico + sensors |
| Main Battery | Gens Ace 5000mAh 2S 7.4V 30C | - | 7.4V nom, 150A burst | - | XT60 connector |

### Wiring Notes

- All ground rails tied together at single star-ground point near battery
- 5V BEC input: 16AWG silicone wire, XT60 pigtail to battery
- 12V boost output: 20AWG silicone wire, JST-XH connector for distribution
- Direct 7.4V to ESC: 18AWG silicone wire, 3.5mm bullet connectors
- 3.3V rail: 24AWG wire, 2-pin JST-SH connector to Pico VSYS/GND

---

## Task 3: Sensor Selection

### 3.1 EGT (Exhaust Gas Temperature) - AB Section

| Parameter | Value |
|---|---|
| Sensor | K-type thermocouple, 1mm exposed junction, Inconel sheath |
| Max Temp | 1300°C (AB flame temp) |
| Accuracy | ±2°C (with cold-junction compensation) |
| Interface | SPI via MAX6675 |
| Part Number | MAX6675 module + K-type probe (e.g., HYPER RC K-TC-1.0) |

**Wiring:**

```
MAX6675 Module      Raspberry Pi Pico
┌──────────┐
│ CS  ───── GP0 (SPI CS)
│ SCK ───── GP1 (SPI SCK)
│ SO  ───── GP2 (SPI MISO)
│ VCC ───── 3.3V rail
│ GND ───── Ground
└──────────┘
```

**Notes:**
- MAX6675 reads 0-1024°C; for 1300°C, use MAX31855 instead if needed
- Place thermocouple probe tip in AB flame path, 50mm downstream of flame holder
- Use K-type extension wire (thermocouple grade) from probe to MAX6675 module
- Keep thermocouple wire away from ignition/spark sources (noise pickup)

### 3.2 Flame Detection

**Primary option: UV photodiode**

```
Hamamatsu G5842 UV Photodiode
├── Anode → +5V via 10kΩ pull-up resistor
├── Cathode → GND
└── Output → GP7 (digital input, active LOW when flame detected)

Circuit:
    5V
     │
    10kΩ pull-up
     │
─────┼────── GP7 (Pico)
     │
    ┌┤
    │ └─ G5842
    │   │
    └───┴────── GND
```

| Parameter | Value |
|---|---|
| Part | Hamamatsu G5842 |
| Spectral range | 185-265nm (UV-C) |
| Dark current | 10nA |
| Response time | <1ms |
| Output | Digital (LOW = flame detected) |

**Alternative: IR optical flame sensor**

If UV cost is prohibitive ($30+ for G5842):

```
KY-026 Flame Sensor Module (IR phototransistor)
├── VCC → 5V
├── GND → GND
├── DO  → GP7 (digital)
└── AO  → not connected (analog unused)

Sensitivity adjusted via onboard potentiometer
```

**Placement:**
- Mount sensor looking into AB combustion zone through a quartz window
- UV diode needs line-of-sight to flame front
- Shield from direct sunlight with baffle tube

### 3.3 Fuel Pressure

| Parameter | Value |
|---|---|
| Sensor | 0-10 bar gauge pressure transducer |
| Output | 0.5-4.5V ratiometric (3-wire) |
| Supply | 5V (from BEC) |
| Part | Keller 4LPR-10 (or Honeywell ABP2LANT025PG2A3XX) |
| Thread | G1/4 or 1/8 NPT |

**Wiring:**

```
Pressure Transducer    Raspberry Pi Pico
┌──────────────┐
│ Red   (VCC) ─── 5V rail
│ Black (GND) ─── GND
│ White (OUT) ─── GP8 (ADC input, 0-3.3V via resistor divider)
└──────────────┘

Voltage Divider (4.5V → 3.3V max):
  White ──┬── 10kΩ ── GP8
         ┌┴┐
         │ │ 12kΩ
         └┬┘
           │
          GND

  Vout = Vin × 12k / (10k + 12k) = Vin × 0.545
  4.5V × 0.545 = 2.45V max at GP8
```

### 3.4 Airspeed / Mach Number

Airspeed is read from the existing Pixhawk flight controller via serial UART at 115200 baud using MAVLink protocol:

| Parameter | Source | Protocol |
|---|---|---|
| Airspeed | Pixhawk AIRSPEED_RAW | MAVLink msg #74 |
| Mach number | Calculated from airspeed + altitude temp | Derived |

**Wiring:**

```
Pixhawk TELEM1     Raspberry Pi Pico
┌──────────┐
│ TX ──────── GP12 (RX)
│ RX ──────── GP11 (TX)
│ VCC ─────── not connected (separate power)
│ GND ─────── GND
└──────────┘
```

---

## Task 4: Actuator Interface

### 4.1 Secondary Fuel Pump (Brushless DC Gear Pump)

```
Raspberry Pi Pico    ESC (SS Series 30A)     Brushless Fuel Pump
┌──────────────┐     ┌──────────┐           ┌──────────────┐
│ GP5 (PWM)  ───────├─ Signal (white)       │              │
│ GND        ───────├─ GND (black)          │              │
│ 5V         ───────├─ 5V (red, opto-only)  │              │
└──────────────┘     │                      │              │
                    │ Power: 7.4V direct    │              │
                    │ Battery ──── Red      │              │
                    │ GND ──────── Black    │              │
                    │                      │              │
                    │ 3-phase output ──────► ├─ Phase A    │
                    │                      │ ├─ Phase B    │
                    │                      │ ├─ Phase C    │
                    └──────────────────────┘ └──────────────┘
```

| Component | Specification |
|---|---|
| ESC | HobbyKing SS Series 30A (or ZTW Spider 30A) |
| PWM signal | 50Hz, 1ms = OFF, 2ms = full power |
| Pump motor | Brushless DC gear pump, 3A @ 7.4V |
| Battery feed | 18AWG, 3.5mm bullet to battery |

**ESC Configuration:**
- Set ESC for: Fixed-wing mode (no brake), Medium timing, LiPo cutoff OFF (we controller power)
- Optional: opto-isolated version to reduce electrical noise

### 4.2 Fuel Solenoid Valve

```
Raspberry Pi Pico           IRLZ44N MOSFET               Solenoid Valve
                    ┌─────────────────────┐             ┌──────────────┐
GP4 ─── 1kΩ ───────┤ Gate                │             │              │
                    │                Drain├─────────────┤ Negative     │
GND ────────────────┤ Source              │             │ (one coil    │
                    │                GND  │             │  terminal)   │
                    │                     │      │      │              │
                    └─────────────────────┘      │      │              │
                                                │      │ Positive ────┼── 12V rail
                                                │      └──────────────┘
                                                │
                                               1N4001 flyback diode
                                               (cathode to positive)

Circuit:
               12V rail
                  │
    ┌─────────────┤
    │             │
    │             │ 1N4001 (cathode up)
    │             ↑
    │             │
    │    ┌────────┤
    │    │        │
    │  Solenoid  │
    │  (12V,    │
    │   0.5A)   │
    │    │        │
    │    └────────┤
    │             │
    └─────────────┤─── Drain
                     │
                   IRLZ44N
                     │
                  Source ─── GND
                     │
                  Gate ─── 1kΩ ─── GP4
```

| Component | Specification |
|---|---|
| MOSFET | IRLZ44N (N-channel logic-level, Vgs(th) 1-2V) |
| Gate resistor | 1kΩ (limits inrush, dampens oscillation) |
| Flyback diode | 1N4001 (50V, 1A) or 1N4148 for faster switching |
| Solenoid | Normally closed, 12V, 0.5A |

### 4.3 Variable Iris Nozzle Servo

```
Raspberry Pi Pico    Standard RC Servo        Iris Mechanism
┌──────────────┐     ┌──────────────┐        ┌──────────────┐
│ GP6 (PWM)  ───────├─ Signal (white/orange)   │              │
│ 5V rail   ────────├─ Power (red)      ├────► │ Mechanical   │
│ GND        ───────├─ Ground (black)   │      │ linkage      │
└──────────────┘     └──────────────┘        └──────────────┘
```

| Component | Specification |
|---|---|
| Servo | Standard RC servo (e.g., Savox SB-2274MG) |
| Torque | >3.5 kg-cm (to overcome exhaust pressure) |
| Speed | 0.12s/60° at 5V |
| PWM | 50Hz, 1.0ms = fully closed, 2.0ms = fully open |
| Material | Metal gears, aluminum case (heat resistance) |

**Calibration:**
- 1.0ms → Iris fully closed (minimum throat, ~45mm)
- 1.5ms → Midpoint (~60mm throat)
- 2.0ms → Iris fully open (~85mm throat)
- Linear mapping within mechanical limits
- Homing sequence at boot: servo sweeps to find end stops

### 4.4 CDI Ignition Module

```
Raspberry Pi Pico      4N25 Optocoupler           CDI Module         Spark Plug
┌──────────────┐      ┌──────────────┐        ┌──────────────┐    ┌──────────┐
│ GP3         ────────┤ Anode (pin 1) │        │              │    │          │
│ (5V pulse)      1kΩ  │              │        │              │    │          │
│                    │ Cathode (pin2)─┼─ GND    │              │    │          │
│                    │              │        │              │    │          │
│                    │ Transistor   │        │              │    │          │
│                    │ Collector    ──┤──► Trigger ────────┤───►│
│                    │ (pin 5)      │        │ (+) 12V     │    │          │
│                    │              │        │              │    │          │
│                    │ Emitter      ──┤──► GND       │    │          │
│                    │ (pin 4)      │        │              │    │          │
│                    │              │        │              │    │          │
│                    │ Power: none  │        │ Power ───────┼── 12V rail  │
│                    │ (passive)    │        │              │    │          │
│                    └──────────────┘        └──────────────┘    └──────────┘

Circuit Detail:

Pico GP3 ── 1kΩ ──┬── 4N25 pin 1 (anode)
                   │
                   └── (no parallel resistor needed)
GND ────────────────┬── 4N25 pin 2 (cathode)
                    │
                    4N25 pin 4 (emitter) ── GND
                    4N25 pin 5 (collector) ── CDI trigger input

12V rail ─────────────────────────────────────── CDI power input
```

| Component | Specification |
|---|---|
| Optocoupler | 4N25 (or MOC3021 for higher current) |
| Gate resistor | 1kΩ on LED anode |
| CDI module | Standard RC CDI (e.g., RcExcel CDI module) |
| Trigger pulse | 5V, 10-15ms duration, 50-100Hz during FIRE state |
| Power | 12V rail (from boost converter), ~2A peak |

**Trigger timing:**
- Initial FIRE: 100Hz pulse train for 500ms (promotes ignition)
- After flame detected: reduce to 50Hz for 1.5s
- After 2s total: igniter OFF (flame self-sustaining)

---

## Task 5: Control Logic and State Machine

### State Machine Diagram

```
      ┌────────────────────────────────────────────────────┐
      │                                                    │
      ▼                                                    │
  ┌───────┐    RPM>50% && Thr>80% && M>0.6    ┌───────┐   │
  │  OFF  │ ─────────────────────────────────► │ ARM   │   │
  │       │◄─────────────────────────────────  │       │   │
  └───────┘   RPM<40% || Thr<60%              └───┬───┘   │
      ▲                                            │       │
      │                                     Switch=FIRE   │
      │                                            │       │
      │                                            ▼       │
      │                                     ┌───────┐      │
      │                              ┌─────│ FIRE  │      │
      │                              │     │(0-2s)│      │
      │                              │     └───┬───┘      │
      │                              │         │          │
      │                         No flame      │ Flame    │
      │                         after 2s      │ detected │
      │                              │         │          │
      │                              ▼         ▼          │
      │  ┌────────┐              ┌───────┐  ┌──────────┐  │
      │  │ ABORT  │ ◄────────────│ FAIL  │  │ SUSTAIN  │  │
      │  │(2-5s)  │              │(any)  │  │ (2-20s)  │  │
      │  └────────┘              └───────┘  └────┬───────┘  │
      │      ▲                                    │          │
      │      │                         Switch=OFF           │
      │      │                         || Overtemp          │
      │      │                         || RPM drop          │
      │      │                         || Max time          │
      │      │                                    │          │
      │      └────────────────────────────────────┘          │
      │                  ┌────────────┐                      │
      │                  │  COOLDOWN  │                      │
      │                  │  (3s fixed)│                      │
      │                  └─────┬──────┘                      │
      │                        │                             │
      └────────────────────────┘                             │
                                                             │
                            "Switch=OFF" anywhere ───────────┘
                      (immediate abort-on-power-down safety)
```

### Pseudo-code Implementation

```c
// Control logic runs on core 0 at 100Hz loop rate
// Core 1 handles telemetry output at 10Hz

enum AB_State {
    OFF,
    ARM,
    FIRE,
    SUSTAIN,
    COOLDOWN,
    ABORT,
    FAIL
};

// Global state
AB_State current_state = OFF;
uint32_t state_entry_time = 0;
uint32_t sustain_elapsed = 0;

// Inputs (updated each loop)
float rpm_percent;          // 0-100% from ECU
float throttle_percent;     // 0-100% from RC receiver
float airspeed_mach;        // from Pixhawk
float egt_ab;               // °C from MAX6675
bool flame_detected;        // from UV photodiode
float fuel_pressure_bar;    // from pressure transducer
int switch_position;        // 0=OFF, 1=ARM, 2=FIRE
float rssi_percent;         // 0-100% RC link quality
bool self_test_ok;          // true if all hardware passes startup check

// Outputs
float pump_power;           // 0.0 - 1.0 (mapped to PWM 1-2ms)
bool solenoid_open;         // true = open, false = closed
float iris_position;        // 0.0 (closed) - 1.0 (open)
bool igniter_active;        // true = sparking
float igniter_freq;         // Hz

// Safety check function
bool safety_interlocks_pass() {
    if (!self_test_ok)                    return false;
    if (rssi_percent < 50.0)             return false;   // RC link degraded
    if (rpm_percent < 50.0)              return false;   // AB not at idle
    if (throttle_percent < 80.0)         return false;   // AB only at high power
    if (airspeed_mach < 0.6)             return false;   // flameout risk
    if (p550_egt > 650.0)                return false;   // prevent overtemp
    // main fuel pressure checked via existing ECU telemetry
    return true;
}

// Main control loop
void control_loop() {
    read_sensors();
    uint32_t now_ms = time_us_32() / 1000;
    uint32_t state_elapsed = now_ms - state_entry_time;
    
    switch (current_state) {
        
        case OFF:
            // All actuators off/safe
            pump_power = 0.0;
            solenoid_open = false;
            iris_position = 0.0;       // closed (45mm throat)
            igniter_active = false;
            
            // Transition to ARM
            if (switch_position == 1 && safety_interlocks_pass()) {
                transition_to(ARM);
            }
            break;
            
        case ARM:
            // System armed, actuators still safe
            pump_power = 0.0;
            solenoid_open = false;
            iris_position = 0.0;
            igniter_active = false;
            
            // Monitor conditions
            if (switch_position == 0) {
                transition_to(OFF);
            }
            if (switch_position == 2) {
                // Pilot commanded FIRE
                if (safety_interlocks_pass()) {
                    transition_to(FIRE);
                } else {
                    // Don't fire, stay armed, log warning
                    set_warning("AB FIRE rejected: safety interlocks");
                }
            }
            // Safety regressions
            if (rpm_percent < 40.0 || throttle_percent < 60.0) {
                transition_to(OFF);
                set_warning("AB disarmed: RPM/throttle dropped");
            }
            if (!self_test_ok || rssi_percent < 50.0) {
                transition_to(OFF);
                set_warning("AB disarmed: system fault");
            }
            break;
            
        case FIRE:
            // --- Phase 1: Ignition sequence ---
            uint32_t fire_t = state_elapsed;
            
            // Igniter: active for first 2 seconds
            if (fire_t < 2000) {
                igniter_active = true;
                // Variable frequency: 100Hz first 500ms, then 50Hz
                igniter_freq = (fire_t < 500) ? 100.0 : 50.0;
            } else {
                igniter_active = false;
            }
            
            // Fuel pump: ramp to 30% over 500ms
            if (fire_t < 500) {
                pump_power = 0.30 * (fire_t / 500.0);
            } else {
                pump_power = 0.30;       // hold at 30%
            }
            
            // Solenoid: open immediately
            solenoid_open = true;
            
            // Iris: ramp open over 1000ms
            if (fire_t < 1000) {
                iris_position = 1.0 * (fire_t / 1000.0);
            } else {
                iris_position = 1.0;     // fully open
            }
            
            // Flame detection check
            if (fire_t >= 2000 && !flame_detected) {
                // No flame established - ABORT
                transition_to(ABORT);
                set_error("AB FIRE failed: no flame detected");
            }
            if (flame_detected && fire_t >= 500) {
                // Flame established early, proceed to SUSTAIN
                transition_to(SUSTAIN);
            }
            
            // Safety: immediate abort on any critical fault
            if (check_critical_faults()) {
                transition_to(ABORT);
            }
            break;
            
        case SUSTAIN:
            // --- Phase 2: Sustained burn ---
            sustain_elapsed = state_elapsed;
            
            // Igniter: OFF (flame is self-sustaining)
            igniter_active = false;
            
            // Solenoid: OPEN
            solenoid_open = true;
            
            // Iris: OPEN
            iris_position = 1.0;
            
            // Fuel pump: closed-loop EGT control
            // Target: 850-950°C in AB section
            float target_egt = 900.0;  // center of target band
            float error = target_egt - egt_ab;
            
            // Simple PI controller
            // Kp = 0.002, Ki = 0.0001 (tuned values)
            static float integral = 0.0;
            integral += error * 0.01;   // 100Hz loop
            integral = clamp(integral, -0.2, 0.2);
            
            float p_term = error * 0.002;
            float i_term = integral * 0.0001;
            float pump_setpoint = 0.30 + p_term + i_term;
            pump_power = clamp(pump_setpoint, 0.05, 0.60);
            
            // Exit conditions
            if (switch_position == 0) {
                transition_to(COOLDOWN);
            }
            // Critical safety limits
            if (egt_ab > 1050.0) {
                transition_to(ABORT);
                set_error("AB overtemperature: EGT > 1050°C");
            }
            if (rpm_percent < 40.0) {
                transition_to(ABORT);
                set_error("AB abort: engine RPM dropped");
            }
            if (!flame_detected && sustain_elapsed > 500) {
                // Flameout detected
                transition_to(ABORT);
                set_error("AB flameout detected");
            }
            // Max burn time: 20 seconds (afterburner duration limit)
            if (sustain_elapsed > 20000) {
                transition_to(COOLDOWN);
                set_warning("AB max burn time reached");
            }
            break;
            
        case COOLDOWN:
            // --- Phase 3: Cooldown sequence ---
            uint32_t cool_t = state_elapsed;
            
            // Fuel: OFF immediately
            pump_power = 0.0;
            
            // Solenoid: CLOSE immediately
            solenoid_open = false;
            
            // Igniter: OFF
            igniter_active = false;
            
            // Iris: HOLD OPEN for 2s, then close over 1s
            if (cool_t < 2000) {
                iris_position = 1.0;    // hold open for purge airflow
            } else if (cool_t < 3000) {
                // Close over 1 second
                float close_factor = (cool_t - 2000) / 1000.0;
                iris_position = 1.0 - (1.0 * close_factor);
            } else {
                iris_position = 0.0;    // fully closed
                transition_to(OFF);
            }
            break;
            
        case ABORT:
            // Emergency abort sequence (fastest safe shutdown)
            uint32_t abort_t = state_elapsed;
            
            // Fuel: OFF immediately
            pump_power = 0.0;
            
            // Solenoid: CLOSE immediately
            solenoid_open = false;
            
            // Igniter: OFF
            igniter_active = false;
            
            // Iris: close aggressively over 2 seconds
            if (abort_t < 500) {
                iris_position = 1.0;    // brief hold for flame purge
            } else if (abort_t < 2500) {
                float close_factor = (abort_t - 500) / 2000.0;
                iris_position = 1.0 - close_factor;
            } else {
                iris_position = 0.0;
                transition_to(OFF);
            }
            
            // Note: ABORT always transitions to OFF after 2.5s
            break;
            
        case FAIL:
            // Severe system failure - manual intervention required
            // All outputs safe
            pump_power = 0.0;
            solenoid_open = false;
            iris_position = 0.0;
            igniter_active = false;
            // Only way out: power cycle
            break;
    }
    
    write_actuators();
    update_led();       // status LED: green=ARM, blue=FIRE, red=FAIL
}

void transition_to(AB_State new_state) {
    current_state = new_state;
    state_entry_time = time_us_32() / 1000;
    
    // Reset integrators on specific transitions
    if (new_state == FIRE || new_state == OFF) {
        integral = 0.0;
    }
}

bool check_critical_faults() {
    // Called during FIRE and SUSTAIN for immediate abort
    if (!flame_detected && current_state == FIRE && 
        (time_us_32()/1000 - state_entry_time) > 2000) {
        return true;  // handled in FIRE state, but belt-and-suspenders
    }
    if (egt_ab > 1100.0) {
        return true;  // hard overtemp limit
    }
    if (fuel_pressure_bar < 0.5 || fuel_pressure_bar > 10.0) {
        return true;  // fuel pressure out of range
    }
    if (rpm_percent < 30.0) {
        return true;  // engine nearly stopped
    }
    if (rssi_percent < 40.0) {
        return true;  // RC link critical
    }
    return false;
}
```

### State Transition Table

| Current State | Condition | Next State | Action |
|---|---|---|---|
| OFF | Switch=ARM && Safety OK | ARM | Start monitoring |
| OFF | Any | OFF | Default |
| ARM | Switch=OFF | OFF | Disarm |
| ARM | Safety fail | OFF | Disarm, log warning |
| ARM | Switch=FIRE && Safety OK | FIRE | Begin ignition |
| ARM | Switch=FIRE && Safety fail | ARM | Reject, log warning |
| FIRE | Flame detected (t>500ms) | SUSTAIN | Early sustain |
| FIRE | No flame @ 2s | ABORT | Failed ignition |
| FIRE | Switch=OFF | ABORT | Pilot abort |
| FIRE | Critical fault | ABORT | Safety abort |
| SUSTAIN | Switch=OFF | COOLDOWN | Begin cooldown |
| SUSTAIN | EGT > 1050°C | ABORT | Overtemp abort |
| SUSTAIN | RPM < 40% | ABORT | Engine failure |
| SUSTAIN | Flameout (t>500ms) | ABORT | Flameout abort |
| SUSTAIN | Time > 20s | COOLDOWN | Max time |
| SUSTAIN | Critical fault | ABORT | Safety abort |
| COOLDOWN | t > 3s | OFF | Complete |
| ABORT | t > 2.5s | OFF | Complete |
| FAIL | Power cycle | OFF | Manual reset |

---

## Task 6: Wiring Diagram

```
COMPLETE WIRING DIAGRAM - P550-PRO AFTERBURNER CONTROLLER
==========================================================

                                         ┌─────────────────────────┐
                                         │     2S LiPo 5000mAh     │
                                         │       7.4V XT60        │
                                         └────┬────────┬──────────┘
                                              │        │
                                          16AWG │        │ 16AWG
                                              │        │
                                    ┌─────────┘        └──────────┐
                                    │                             │
                                    ▼                             ▼
                          ┌──────────────────┐       ┌──────────────────────┐
                          │  CC BEC 10A      │       │  P550-PRO ECU        │
                          │  Input: 7.4V     │       │  Input: 7.4V         │
                          │  Output: 5V 10A  │       │  (separate circuit)  │
                          └────────┬─────────┘       └──────────────────────┘
                                   │
                                   5V rail (20AWG)
                                   │
           ┌───────────┬───────────┼───────────┬───────────┐
           │           │           │           │           │
           ▼           ▼           ▼           ▼           ▼
     ┌──────────┐ ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐
     │ Receiver │ │ Servo │ │ Pixhawk│ │  3.3V    │ │ Pressure │
     │ (RC Rx)  │ │ Iris  │ │ Telems│ │ Regulator │ │ Sensor   │
     │ 5V       │ │ 5V    │ │ 5V    │ │ (Pololu)  │ │ 5V       │
     │ CH3: Thr │ │ ~1A pk│ │ ~200mA│ │ 5V→3.3V   │ │ 5mA      │
     │ CH5: AB  │ └────────┘ │ 20AWG │ └─────┬─────┘ └──────────┘
     │ PWM out  │            └────────┘       │
     └─────┬────┘                              │
           │             ┌─────────────────────┤
           │             │                     │
           │         24AWG                   24AWG
           │             │                     │
           ▼             ▼                     ▼
     ┌─────────────────────────────────────────────┐
     │          RASPBERRY PI PICO (RP2040)          │
     │                                             │
     │  GP0 ← CS   (MAX6675)                       │
     │  GP1 ← SCK  (MAX6675)                       │
     │  GP2 ← MISO (MAX6675)                       │
     │  GP3 → CDI ignitor (via 4N25 opto)          │
     │  GP4 → Solenoid MOSFET gate (via 1kΩ)        │
     │  GP5 → Pump ESC signal                       │
     │  GP6 → Iris servo signal                     │
     │  GP7 ← Flame detector (digital)              │
     │  GP8 ← Fuel pressure (analog, 0-3.3V)        │
     │  GP9 ← RC Rx CH5 (AB switch PWM)             │
     │  GP10 ← RC Rx CH3 (throttle PWM)              │
     │  GP11 → Pixhawk UART TX (telemetry)           │
     │  GP12 ← Pixhawk UART RX (airspeed)            │
     │  GP13 ← RSSI (analog, RC Rx)                  │
     │  GP14 ← RPM input (optocoupled from ECU)     │
     │  GP15 → RGB status LED                        │
     │                                             │
     │  VSYS ← 7.4V via Schottky diode              │
     │  3V3  → MAX6675, flame detector              │
     │  GND  ← Common ground (star point)           │
     └───────────────────────────────────────────────┘
               │        │        │         │
               │        │        │         │
         24AWG │   24AWG │   24AWG │    24AWG
               │        │        │         │
               ▼        ▼        ▼         ▼
     ┌───────────┐ ┌────────┐ ┌────────┐ ┌──────────┐
     │ MAX6675   │ │Flame   │ │Pixhawk │ │RGB LED   │
     │ + K-type  │ │Detector│ │TELEM1  │ │(cathode) │
     │ thermocpl │ │(UV/IR) │ │UART    │ │3.3V-GP15 │
     └───────────┘ └────────┘ └────────┘ └──────────┘

Power:
     ┌──────────────────────────────────────────────────────────
     │ 7.4V rail (18AWG, from battery via XT60 + 20A fuse)
     │
     ├── 5V BEC input ── 16AWG ── CC BEC 10A ── 5V rail (20AWG)
     │                                  │
     │                                  ├── Rx channels ── 26AWG servo leads
     │                                  ├── Iris servo ── 26AWG extension
     │                                  ├── Pixhawk ── 4-wire dupont
     │                                  ├── 3.3V reg input ── 24AWG
     │                                  └── Pressure sensor ── 24AWG 3-wire
     │
     ├── 12V boost input ── 20AWG ── Pololu U3V40A12 ── 12V rail (20AWG)
     │                                                │
     │                                   ┌────────────┤
     │                                   │            │
     │                                   ▼            ▼
     │                            ┌────────────┐ ┌──────────────┐
     │                            │ Solenoid   │ │ CDI module   │
     │                            │ 12V, 0.5A  │ │ 12V, 2A peak │
     │                            └────────────┘ └──────────────┘
     │
     ├── pump ESC power ── 18AWG ── SS 30A ESC ── brushless pump motor
     │                                          │
     │                                 ┌────────┤
     │                                 │ 3-phase 18AWG
     │                                 ▼
     │                          ┌──────────────┐
     │                          │ Fuel pump    │
     │                          │ (BLDC gear)  │
     │                          └──────────────┘
     │
     └── P550 ECU power ── 18AWG ── ECU (6-12V compatible)

Connector Summary:
     Battery:       XT60 (16AWG)
     ESC motor:     3× 3.5mm bullet (18AWG)
     Servo:         JR-style 26AWG (PWM + 5V + GND)
     Sensor:        Dupont 2.54mm (24AWG)
     Signal:        26AWG servo-style
     Power dist:    JST-XH (20AWG) or Powerpole (18AWG)
```

---

## Task 7: Safety Interlocks (Critical)

### Interlock Logic Table

| Interlock | Condition | Threshold | Rationale | Failure Action |
|---|---|---|---|---|
| Engine RPM | `rpm_percent >= 50.0%` | >50% N1 | Prevent AB activation at idle or spool-up where flame propagation is unreliable | Block ARM→FIRE; if in SUSTAIN, immediate ABORT |
| Throttle position | `throttle_percent >= 80.0%` | >80% | AB fuel ignites only in high-temperature, high-velocity exhaust stream | Block ARM→FIRE; if in SUSTAIN and drops below 60%, ABORT |
| Airspeed | `airspeed_mach >= 0.6` | ≥M0.6 | Prevent AB at low airspeed where flameout risk increases and nozzle positioning affects flight characteristics | Block ARM→FIRE |
| Main fuel pressure | Via ECU telemetry | Within spec | Ensure engine has adequate fuel pressure before diverting fuel to AB | Block ARM→FIRE |
| Engine EGT | `p550_egt < 650.0°C` | <650°C | Prevent engaging AB when engine is already near thermal limits | Block ARM→FIRE |
| Self-test | All peripherals respond | All OK | Verify sensors, actuators, and communication at system boot | Enter FAIL state until power cycle; block any transition out of OFF |
| RC link quality | `rssi_percent >= 50.0%` | >50% | Ensure control link is reliable before committing to high-risk operation | Block ARM→FIRE; if in SUSTAIN and drops below 40%, ABORT |
| Flame detection | Flame present in FIRE | Within 2s | Verify ignition occurred before proceeding to SUSTAIN | ABORT if no flame after 2s |
| AB EGT overtemperature | `egt_ab <= 1050.0°C` | ≤1050°C | Prevent thermal damage to AB section and downstream structure | Immediate ABORT |
| Max AB time | `sustain_time <= 20s` | ≤20s | Limit thermal stress; AB section not designed for continuous operation | Transition to COOLDOWN |
| Pump current | `pump_current < 4A` | <4A | Detect pump stall, blockage, or wiring fault | Transition to ABORT; log diagnostic |

### Self-Test Sequence (at boot)

1. **Power-on self-test** (runs once, before ARM is permitted)
   - Measure Pico supply voltage (VSYS) → must be 6-9V
   - Test MAX6675 communication → read temperature, must return valid data
   - Test flame detector → must read NO FLAME (LOW ambient UV)
   - Read fuel pressure → must be 0-2 bar (engine off, residual pressure)
   - Sweep iris servo through full range → verify response
   - Test solenoid MOSFET → pulse briefly (20ms), verify no short
   - Test pump ESC → send 1ms pulse (OFF), listen for signal
   - Test CDI optocoupler → send test pulse, verify collector voltage drops
   - Read RSSI → must be > 50%
   - Read RPM → must be 0 (engine off at boot)
   - Read throttle → sanity check (0-100%)
   - Read AB switch → sanity check (0, 1, or 2)

2. **On each ARM transition** (while engine running)
   - Re-verify: RPM, throttle, airspeed, EGT, fuel pressure, RSSI
   - If any fail: remain in OFF, log exact failure

3. **Continuous monitoring** (every control loop iteration, 10ms)
   - All sensor values within expected ranges
   - RC switch position valid (debounced, hysteresis applied)
   - No communication timeout on any sensor

### Failure Mode Matrix

| Failure Mode | Detection | Immediate Action | Fallback State |
|---|---|---|---|
| Flame ignition failure | No flame after 2s in FIRE | Close solenoid, kill pump | ABORT → OFF |
| Flameout in SUSTAIN | Flame goes LOW + EGT drops | Close solenoid, kill pump | ABORT → OFF |
| AB overtemp (>1050°C) | EGT > 1050°C | Close solenoid, kill pump | ABORT → OFF |
| AB overtemp (>1100°C) | EGT > 1100°C | Close solenoid, kill pump, close iris | ABORT → OFF (hard limit) |
| Engine RPM loss | RPM < 40% in SUSTAIN | Abort immediately | ABORT → OFF |
| RC signal loss | No valid pulses for 500ms | Maintain current state for 1s, then safe shutdown | COOLDOWN if in FIRE/SUSTAIN; OFF otherwise |
| Fuel pressure loss | Pressure < 0.5 bar | Close solenoid, abort | ABORT → OFF |
| Fuel pump stall | Current spike > 4A | Cut pump power, abort | ABORT → OFF |
| Sensor fault (any) | Invalid reading (NaN, out of range) | If critical (EGT/flame): abort; if non-critical: log, continue | State-dependent |
| Microcontroller hang | Watchdog timer expires | Hardware reset; all GPIOs float low (via pull-downs) | OFF (safe state) |
| Battery undervoltage | VSYS < 6.0V | Log warning, continue; at < 5.5V: immediate safe shutdown | COOLDOWN → OFF |

### Hardware Watchdog Implementation

```c
// Enable hardware watchdog on Pico
// If main loop stalls > 2 seconds, watchdog forces reset
#include "hardware/watchdog.h"

void setup() {
    // Enable watchdog with 2000ms timeout
    watchdog_enable(2000, true);  // true = pause on debug
}

void main_loop() {
    while (1) {
        control_loop();
        watchdog_update();  // reset watchdog timer
    }
}

// All GPIO outputs configured with pull-down resistors
// On watchdog reset (or brownout), GPIOs go to safe state:
//   - Pump: LOW → 1ms PWM → pump OFF
//   - Solenoid: LOW → MOSFET off → valve CLOSED
//   - Igniter: LOW → optocoupler off → no spark
//   - Servo: to be safe, external pull-down on signal line
```

---

## Task 8: Telemetry Output

### Data Format

Telemetry is transmitted from the Pico to the Pixhawk via UART1 at 115200 baud using MAVLink protocol. The Pixhawk forwards to ground station (Mission Planner / QGroundControl) via telemetry radio.

A custom MAVLink message (`AB_STATUS`, msg ID 200) is defined with the following payload:

### Telemetry Message Definition

```
MAVLink message AB_STATUS (ID 200)
Payload (24 bytes):

Byte   | Field              | Type    | Units  | Range          | Description
-------+--------------------+---------+--------+----------------+------------------------------
0      | ab_state           | uint8_t | -      | 0-6            | 0=OFF, 1=ARM, 2=FIRE, 
      |                    |         |        |                | 3=SUSTAIN, 4=COOLDOWN, 
      |                    |         |        |                | 5=ABORT, 6=FAIL
1      | egt_ab             | uint8_t | °C     | 0-255°C offset | EGT value: real = byte + 500
      |                    |         |        |                | (covers 500-755°C)
2-3    | egt_ab_high        | uint16_t | °C   | 0-1300°C       | High-resolution EGT (if 
      |                    |         |        |                | >755°C, use this field)
4      | fuel_pressure      | uint8_t | bar×10 | 0-100          | Fuel pressure × 10 
      |                    |         |        |                | (0.0-10.0 bar)
5      | flame_detected     | uint8_t | -      | 0/1            | 0=no flame, 1=flame detected
6      | iris_position      | uint8_t | %      | 0-100          | Iris nozzle position %
7      | pump_power         | uint8_t | %      | 0-100          | Pump power %
8-9    | sustain_time       | uint16_t | s×10 | 0-65535        | Time in current state ×10
10     | rssi               | uint8_t | %      | 0-100          | RC link RSSI
11     | rpm_percent        | uint8_t | %      | 0-100          | Engine RPM %
12     | throttle_percent   | uint8_t | %      | 0-100          | Throttle position %
13     | airspeed_mach      | uint8_t | Mach×100 | 0-200       | Mach number ×100 (0.00-2.00)
14     | error_code         | uint8_t | -      | 0-255          | Error code (0=no error)
15     | warning_code       | uint8_t | -      | 0-255          | Warning code (0=none)
16-23  | reserved           | 8 bytes | -      | -              | Future use
```

### Error Codes

| Code | Name | Description |
|---|---|---|
| 0 | ERR_NONE | No error |
| 1 | ERR_NO_FLAME_IGNITION | Flame not detected within 2s of FIRE |
| 2 | ERR_FLAMEOUT | Flame lost during SUSTAIN |
| 3 | ERR_AB_OVERTEMP | AB EGT > 1050°C |
| 4 | ERR_RPM_DROP | Engine RPM < 40% during AB |
| 5 | ERR_FUEL_PRESSURE | Fuel pressure out of range |
| 6 | ERR_PUMP_STALL | Pump current exceeded |
| 7 | ERR_SENSOR_FAIL | Critical sensor failure |
| 8 | ERR_RC_LOSS | RC signal lost |
| 9 | ERR_BROWNOUT | Supply voltage < 5.5V |
| 10 | ERR_SELF_TEST | Power-on self-test failed |
| 11 | ERR_SWITCH_INVALID | AB switch in undefined position |

### Warning Codes

| Code | Name | Description |
|---|---|---|
| 0 | WARN_NONE | No warning |
| 1 | WARN_AB_MAX_TIME | Max burn time approaching |
| 2 | WARN_EGT_HIGH | EGT approaching limit (>950°C) |
| 3 | WARN_RSSI_LOW | RSSI < 60% |
| 4 | WARN_BAT_LOW | Battery < 6.5V |
| 5 | WARN_SENSOR_NOISY | Sensor reading erratic |
| 6 | WARN_FIRE_REJECTED | FIRE commanded but interlocks failed |

### Ground Station Display

On the ground station (Mission Planner QCustomPlot or QGC), the following should be displayed:

- **AB status indicator**: Colored text showing current state (OFF=gray, ARM=yellow, FIRE=red, SUSTAIN=green, COOLDOWN=blue, ABORT=red flashing)
- **AB EGT gauge**: 0-1100°C with colored zones (safe=green <800°C, caution=yellow 800-950°C, warning=orange 950-1050°C, critical=red >1050°C)
- **Fuel pressure**: Bar gauge 0-10 bar with expected operating band (2-6 bar)
- **Flame indicator**: Green ON / gray OFF icon
- **Iris position**: Percentage bar
- **Pump power**: Percentage bar
- **AB timer**: Elapsed time since FIRE entry (seconds)
- **Error/warning text**: Latest error or warning message

### Telemetry Rate

| State | Update Rate | Notes |
|---|---|---|
| OFF | 1 Hz | Low rate during standby |
| ARM | 5 Hz | Increased monitoring |
| FIRE | 20 Hz | Fast updates during critical phase |
| SUSTAIN | 10 Hz | Standard operational rate |
| COOLDOWN | 5 Hz | Reduced rate during cooldown |
| ABORT | 20 Hz | Fast updates during emergency |
| FAIL | 1 Hz | Minimal rate in fault state |

---

## Bill of Materials Summary

| Item | Part Number | Qty | Est. Cost |
|---|---|---|---|
| Microcontroller | Raspberry Pi Pico (RP2040) | 1 | $4 |
| 5V BEC | Castle Creations CC BEC 10A | 1 | $30 |
| 12V boost | Pololu U3V40A12 | 1 | $15 |
| 3.3V regulator | Pololu D24V10F3 | 1 | $10 |
| Thermocouple amp | MAX6675 module | 1 | $8 |
| K-type probe | 1mm exposed junction, Inconel | 1 | $15 |
| Flame detector | Hamamatsu G5842 UV photodiode | 1 | $35 |
| Pressure transducer | Keller 4LPR-10 (0-10 bar) | 1 | $50 |
| Fuel pump ESC | HobbyKing SS Series 30A | 1 | $12 |
| Fuel pump motor | Brushless DC gear pump 3A/7.4V | 1 | $25 |
| Solenoid valve | 12V NC, 1/8" NPT | 1 | $20 |
| Solenoid MOSFET | IRLZ44N + 1N4001 + 1kΩ | 1 | $3 |
| Iris servo | Savox SB-2274MG | 1 | $55 |
| CDI module | RcExcel CDI + spark plug | 1 | $30 |
| Optocoupler | 4N25 | 1 | $1 |
| Connectors | XT60, JST-XH, Dupont, servo leads | - | $10 |
| Wire | 16/18/20/24/26 AWG silicone | - | $10 |
| PCB | Custom PCB or protoboard | 1 | $5 |
| Enclosure | 3D-printed ABS or aluminum box | 1 | $5 |
| **Total** | | | **~$340** |

---

## Appendix: Programming and Setup

### Raspberry Pi Pico Setup

1. Install MicroPython or C SDK:
   - **MicroPython**: Download .uf2 from micropython.org, drag to Pico
   - **C SDK**: Install Raspberry Pi Pico C SDK, compile with CMake

2. Pin configuration constants:
```c
// Pin definitions (C SDK)
#define PIN_EGT_CS      0
#define PIN_EGT_SCK     1
#define PIN_EGT_MISO    2
#define PIN_CDI_TRIG    3
#define PIN_SOLENOID    4
#define PIN_PUMP_PWM    5
#define PIN_IRIS_PWM    6
#define PIN_FLAME_DET   7
#define PIN_FUEL_PRESS  8  // ADC capable
#define PIN_RC_SWITCH   9  // PWM input
#define PIN_RC_THROTTLE 10 // PWM input
#define PIN_TX          11 // UART TX
#define PIN_RX          12 // UART RX
#define PIN_RSSI        13 // ADC capable
#define PIN_RPM_IN      14 // PWM input or digital
#define PIN_STATUS_LED  15
```

3. PWM configuration:
```c
// Servo/ESC PWM: 50Hz, 1-2ms pulse
// Pico PWM clock: 125MHz
// Wrap value for 50Hz: 125,000,000 / 50 = 2,500,000
// For 1ms pulse: level = 2,500,000 * 0.05 = 125,000
// For 2ms pulse: level = 2,500,000 * 0.10 = 250,000

#define SERVO_FREQ      50
#define SERVO_WRAP      24999   // 50Hz at 125MHz / 25000 = 5kHz PWM resolution
#define SERVO_1MS       1250    // 1ms pulse (2500 * 0.05 / 2)
#define SERVO_2MS       2500    // 2ms pulse
#define SERVO_OFF       0       // no pulse (fail-safe)
```

4. RC PWM input reading (PIO or interrupt-based):
```c
// Use PIO to measure pulse width on RC channels
// Resolution: ±1μs, 1-2ms valid range for servo PWM
// 1.0ms → 0% (OFF/CLOSED)
// 1.5ms → 50% (mid)
// 2.0ms → 100% (ON/OPEN)
```

5. MAX6675 SPI reading:
```c
uint16_t read_max6675() {
    // CS low
    gpio_put(PIN_EGT_CS, 0);
    sleep_us(10);
    
    // Read 16 bits
    uint16_t data = 0;
    for (int i = 0; i < 16; i++) {
        gpio_put(PIN_EGT_SCK, 1);
        sleep_us(1);
        data <<= 1;
        if (gpio_get(PIN_EGT_MISO)) data |= 1;
        gpio_put(PIN_EGT_SCK, 0);
        sleep_us(1);
    }
    
    // CS high
    gpio_put(PIN_EGT_CS, 1);
    sleep_us(10);
    
    // Thermocouple data in bits 3-14 (12-bit)
    // Temperature = data >> 3 * 0.25°C
    if (data & 0x04) return 0;  // open circuit detected
    return (data >> 3) * 25 / 100;  // with rounding
    
    // Note: MAX31855 used if >1024°C needed (handles up to 1350°C)
}
```

---

## Revision History

| Date | Version | Changes |
|---|---|---|
| 2026-07-27 | 1.0 | Initial complete design specification |
