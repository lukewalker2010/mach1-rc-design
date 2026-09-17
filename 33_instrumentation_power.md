# Instrumentation, Power & DAQ Candidate Review — R09/R10/R11

**2026-09-16 · E3/E2 · Candidate analysis; all three readiness items OPEN.**
Reproduce: `python3 tools/hardware_budget.py` and
`python3 -m unittest tests.test_hardware_budget -v`.
Requirements and BOM remain under the principal's integration authority.
Arithmetic and datasheet checks are not installed-hardware qualification.

## 1. Pressure chain

`qc_at()` uses ISA troposphere pressure and the shock-aware forward pitot
relation in `tools/airdata.py`. The assumed range-selection envelope is
sea level–3657.6 m, Mach 0–1.2; maximum qc is **142,615 Pa** at SL/M1.2.
This is a range study, not a flight envelope. The baseline 3447 Pa range fails.

| Candidate | Evidence checked | Remaining uncertainty |
|---|---|---|
| `4525DO-DS3BJ050DP` | Exact TE page confirms 50 psi differential, 14-bit output, ±0.25% span accuracy, **300 psi proof** (not the draft's 150 psi) | Page says I²C or SPI generically; exact J address/interface, supply, transfer endpoints and total error band require ordering-table/vendor confirmation |
| `4525DO-DS5AI001DP` | Exact TE page exists; description says 1 psi I²C differential | Same page inconsistently lists MS4515DO and 300 psi pressure. Treat 1 psi range/options/proof as **unverified** pending written clarification |
| `MS5803-02BA` family | Candidate only; primary page unavailable during expert review | Exact order code, range, accuracy, OSR/rate, pressure conversion and noise **unverified**; no accepted equivalent or purchase selection |

The 50 psi assumed span is 344,738 Pa, 2.42× the envelope maximum;
±0.25% span is ±862 Pa. That accuracy entry is **not** a total installed error
budget. MS4525DO family transfer types A/B use portions of the 14-bit code
space (nominal 10–90% / 5–95%). The script's provisional 13107/14745 usable
code intervals give ~0.526/23.38 Pa per count, respectively; these are conditional
on exact option confirmation, not measured resolution. Static-sensor raw 24-bit
codes are nonlinear compensated inputs, so dividing a pressure span by 2²⁴
does **not** establish pressure resolution. The script labels its static
30–110 kPa, ±250 Pa screening assumptions unverified.

Candidate structure: high/low differential qc plus absolute static, each with
freshness/validity/source timestamps. A shared I²C bus is conditional on verified
addresses, levels and independence requirements. A 1 psi sensor connected to
the full pitot differential can be exposed to **142.6 kPa (~20.7 psi)** even
when software ignores it: proof pressure, both-port common pressure, reverse
pressure, overrange recovery and any physical isolation must be resolved.
Calibration must establish usable bounds, temperature drift, tubing lag,
installation error and Mach uncertainty. No pressure-sensor price is verified.

## 2. Power and pump blocker

### P550 supply conflict found during cross-workstream review

The directly retrieved [JetCat P550-PRO datasheet](https://www.jetcat.de/jetcat/anleitungen/P550-PRO-Datasheet.pdf),
V1.1 02/2023 p1, specifies **10–35 VDC** and lists integrated ECU/pump/solenoids.
The direct 2S concept in 23 (even **8.4 V** fully charged) is below that range.
`tools/hardware_budget.py` now checks this explicitly. Confirm the exact installed
engine variant and current/startup requirements, then redesign the engine supply
and revise mass/CG, wiring and the battery budget together. Do not simply attach
the engine to the unqualified AB boost rail; its current capability is unknown.
This is part of R10, and invalidates the engine branch of the historical power
budget independently of the AB converter problem below.

**Speck ZY-4S-12V remains unverified and blocks pump/driver/converter selection.**
Prior searches supplied no exact primary datasheet. This is not proof that the
part does not exist. Require exact manufacturer order code, fuel compatibility,
flow-versus-pressure curve, motor/driver type, startup/stall and thermal data.
The 1.5/1.8 A at 12 V values are load-table placeholders, not measured limits.

Pololu's exact **U3V50F12 #2568** page confirms fixed 12 V boost, input
2.9 V to VOUT, a 5 A switch/typical maximum input current, and **$29.95**
quantity-one list price as retrieved 2026-09-16 (not a landed procurement quote).
It specifies reverse-voltage, over-current, thermal and undervoltage protection;
the draft's overvoltage-protection assertion was unsupported and removed.

At assumed 6 V pack, η=0.85, `Iin=12 Iout/(6η)`:

| Assumed load | Input current | Disposition |
|---|---:|---|
| Solenoid 0.5 A | 1.18 A | UNQUALIFIED |
| Pump operating 1.5 A | 3.53 A | UNQUALIFIED; pump blocker |
| Pump max 1.8 A | 4.24 A | UNQUALIFIED; pump blocker |
| Pump operating + valve | 4.71 A | UNQUALIFIED; pump blocker |
| Pump max + valve | **5.41 A** | Exceeds typical input-current screen |

Input current below 5 A is only a necessary screen: switch ripple/peak,
continuous output capability, efficiency, low-pack startup, wiring and installed
heat rejection still need evidence. Neither nominal duty nor intermittent AB
operation qualifies a converter. The 6 V floor is an assumption, not an approved
pack cutoff. Even solenoid-only sizing awaits actual valve data and testing.

**ENABLE is not load isolation:** Pololu explicitly says input passes to output
when disabled. ENABLE is also pulled up to VIN through 100 kΩ; direct MCU GPIO
connection requires level/interface review. The candidate net is pack → rated
protection (TBD) → boost → independently controlled valve power switch/driver
(TBD) → normally closed valve. Independent fuel cut must act on the load path;
no MCU command or regulator ENABLE alone proves independent abort. Flyback,
release latency, fuse coordination, grounding and brownout testing remain open.

## 3. ADS1256: corrected scale, pins and settling

TI **SBAS288K**, p3, specifies:

- Differential full scale **±2 VREF/PGA**, full span **4 VREF/PGA**.
- VREFP−VREFN **0.5–2.6 V**, nominal 2.5 V. The draft's 5 V reference is invalid.
- Analog operating pin range (AIN0–7 **and AINCOM**): buffer off,
  AGND−0.1 to AVDD+0.1 V; buffer on, AGND to **AVDD−2 V**.
  These are operating limits, distinct from absolute maximum ratings.
- PGA values 1, 2, 4, 8, 16, 32, 64; input loading changes with PGA/buffer.
  Each physical input pin must meet its limit; differential range alone does
  not establish a valid common mode. Reference pins also have buffer-dependent
  restrictions (p3), and source/filter settling must be checked.

At VREF=2.5 V, PGA=1, **0–5 V fits the differential range without a 2:1
divider** with buffer off and nominal 5 V AVDD, subject to headroom/tolerance
and source impedance. Buffer on limits pins to 3 V at AVDD=5 V, requiring
appropriate conditioning. At PGA=8 the differential window is ±0.625 V.
A ±10 mV bridge centered at 2.5 V fits both buffered pin and differential
limits. Ratio-metric sensing requires a suitable scaled 2.5 V reference derived
from excitation, not wiring 5 V directly to VREF.

Two differential bridges plus six SE signals consume 10 of eight signal pins,
so a single board is impossible. Candidate split:

| Board | Pins | Requested outputs | Screening status |
|---|---|---:|---|
| A: thrust + gravimetric bridges | SIG+/− → AIN0/1 and AIN2/3 | 500+10=510 SPS | Pin-feasible |
| B: four pressures + PT7 + analog flow | AIN0..5; AINCOM → analog reference return | 4×100+500+100=**1000 SPS** | Pin-feasible |

Bridge EXC− goes to excitation return, **not AIN0** (the draft shorted a signal
to excitation return). EXC+ goes to the rated excitation supply. Exact bridge,
pressure and flow order codes/output types remain unverified; this map is
conditional on analog outputs and a reviewed board schematic. DRDY, chip-select,
reference and protection wiring require a complete pin allocation.

**1500 SPS is not an ADS1256 setting at 7.68 MHz.** TI Tables 13/14 distinguish
continuous data rate from settled mux throughput: 1000 SPS setting gives
1.18 ms settling / **837 mux samples/s**; 2000 gives 0.68 ms / **1438 samples/s**;
30000 gives only **4374 mux samples/s**. The tool applies its explicit 0.95
planning scheduling allowance to **mux throughput**, not the nominal rate.
These table figures require the documented WREG→SYNC→WAKEUP sequence and
fSCLK=fCLKIN/4. A candidate 2000 SPS setting passes aggregate arithmetic for
1000 SPS output, but equal six-channel scanning would not meet the 500 SPS
PT7 demand: implement and verify a weighted schedule/max-gap bound. Analog
settling, shared SPI traffic, calibration pauses and per-channel noise/bandwidth
remain open. No throughput qualification is implied.

## 4. MAX31856 timing

Manufacturer datasheet **19-7534 Rev 0 (2/15)**, p4 and Configuration 1:

| Conversion | 60 Hz rejection | 50 Hz rejection |
|---|---:|---:|
| One-shot / first auto, typical–maximum | 143–155 ms | 169–185 ms |
| Auto conversions 2..n, typical–maximum | 82–90 ms | 98–110 ms |
| Additional averaging, first/one-shot | (n−1)×33.33 ms | (n−1)×40 ms |
| Additional averaging, subsequent auto | (n−1)×16.67 ms | (n−1)×20 ms |

Averaging n is 1, 2, 4, 8 or 16. Datasheet averaging increments are **typical**;
adding them to the maximum base does not create a guaranteed worst-case bound.
`max31856_period()` labels that planning model. It distinguishes first/one-shot
from subsequent auto. Table 4 fault-test settings depend on **input resistance
and RC time constant**, not mains rejection: with CJ enabled, maximum extra
test times are 15 ms (<5 kΩ), 37 ms (5–40 kΩ, RC<2 ms), or 125 ms
(5–40 kΩ, RC>2 ms). Auto testing occurs once per 16 conversions; the tool's
optional addition represents a **test-containing interval**, not every interval
or the long-run average. CJ-disabled timings differ and are outside this model.

At n=1 without fault insertion, maximum base periods imply ~6.45 Hz one-shot
or ~11.11 Hz subsequent auto. Six parallel converters can deliver ~66.7 scalar
readings/s in aggregate, but only **~11.11 complete six-channel sets/s**, never
a 60 Hz set. Source-clock DRDY edges and freshness gate samples; repeated reads
do not create conversions. Probe thermal bandwidth is a separate requirement.

## 5. Source ledger and remaining gaps

Checked 2026-09-16:

- [TI ADS1256 primary PDF](https://www.ti.com/lit/ds/symlink/ads1256.pdf):
  SBAS288K, p3, Tables 13–15; downloaded and text-read directly.
- [MAX31856 manufacturer PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31856.pdf):
  primary host timed out; **manufacturer-authored Rev 0 PDF read via
  [mirror](https://datasheet.sic-components.com/MAX31856.pdf)**, p4/Table 4/
  Configuration 1. Primary-host retrieval remains a provenance gap.
- [Pololu exact product](https://www.pololu.com/product/2568): specifications,
  price and ENABLE pass-through checked directly.
- TE exact pages [50 psi](https://www.te.com/en/product-4525DO-DS3BJ050DP.html)
  and [1 psi](https://www.te.com/en/product-4525DO-DS5AI001DP.html): indexed
  primary-page text inspected; conflicts/options retained as open above.
- [MS5803 family page](https://www.te.com/en/product-CAT-BLPS0010.html):
  HTTP 403; draft accuracy/resolution/order claims not credited.

R09/R10/R11 require exact procurement data, calibration and installed tests:
pressure/probe uncertainty; real pump/valve and independent cut-off; startup,
stall, low-pack, thermal and EMI/brownout; ADC reference/common-mode/settling;
full-channel DRDY timing, max sample gaps and dropped conversions. No hardware
qualification, BOM change or release is claimed.
