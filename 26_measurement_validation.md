# Measurement Implementation & Validation

**Date:** 2026-09-16 · **Status:** offline analysis implemented; hardware qualification open.
Supersedes the calculation, logging-integrity and DAQ assumptions identified in
25 R09/R11/R15. It does not change I-07/I-08 probe stations or sample requirements.

## 1. Air data

Use `tools/airdata.py`. All pressure values are **Pa**, temperatures **K** and TAS
**m/s**. Input impact pressure is `qc = p_pitot - p_static`, not dynamic pressure
`q = ρV²/2`. At subsonic speed pitot pressure is upstream stagnation pressure.
Above M1 the probe measures stagnation pressure **after a normal shock**.

The implementation uses γ=1.4 and R=287.05 J/(kg·K), subsonic isentropic inversion,
and supersonic normal-shock static rise followed by downstream stagnation. A
bracketed inversion selects the continuous sonic boundary. Reference equations:
[NASA Glenn normal shocks](https://www.grc.nasa.gov/www/k-12/airplane/normal.html)
and [isentropic flow](https://www.grc.nasa.gov/www/k-12/airplane/isentrop.html).
The M≤3 numerical limit is **not** a permitted aircraft speed.

```text
T_probe = T_static (1 + r (γ−1)/2 M²)
TAS = M sqrt(γ R T_static)
```

`r` is the calibrated recovery factor. Without independent static temperature or
another independent speed observation, TAT does not independently validate Mach.
TAT and static pressure alone do not determine Mach. Account for probe position,
shock/installation error, tubing lag, solar/engine heating and time alignment.

### Range selection

`tools/design_checks.py` gives qc=62.237 kPa at M1 and 78.960 kPa at M1.1 for
p=69.7 kPa. The 23-specified 3.447 kPa range is unsuitable; “MS4525DO” alone is
a sensor family, not a range/order code. Select static and impact sensor ranges
against the **entire released pressure/Mach envelope**, including ground tests,
transients and proof pressure. Record usable calibrated bounds, not just an
advertised full-scale value. No replacement sensor is qualified by this revision.

Calibration records must identify instrument serial, certificate/reference,
uncertainty (including temperature/installation), pressure points and residuals,
zero drift, leak/lag tests and acquisition configuration. A low-speed calibration
does not validate transonic static-port error. Bench pressure sweeps must span
the selected sensor's actual working range.

## 2. Offline log screening (implemented)

`tools/flight_log_check.py` reads:

```csv
sample_id,t_s,static_pa,impact_pa,probe_temp_k,valid
```

- `sample_id`: nonnegative acquisition sequence, incrementing for each new
  synchronised air-data sample. It must not increment for repeated logger values.
- `t_s`: monotonic source acquisition time in seconds. Source time, arrival time,
  clock offsets and per-channel ages should also be retained in the raw archive.
- Pressures are calibrated engineering values; temperature is recovery-probe K.
- `valid`: exactly `1` or `0`, including sensor diagnostic and freshness results.
  Invalid samples may have blank measurement values and break the window.

Invocation (replace **all** capitalised tokens with actual paths/calibration
values; no illustrative calibration is accepted as real evidence):

```sh
python3 tools/flight_log_check.py FLIGHT.csv \
  --static-uncertainty-pa STATIC_BOUND \
  --impact-uncertainty-pa IMPACT_BOUND \
  --static-min-pa STATIC_MIN --static-max-pa STATIC_MAX \
  --impact-max-pa IMPACT_MAX --recovery-factor RECOVERY
```

The tool rejects pressure clipping, invalid/nonfinite values, out-of-domain
pressure ratios, repeated/backward timestamps and repeated/backward sequence
numbers. Missing sequence numbers, sample intervals above 0.02 s (18 I-08's
50 Hz requirement) or invalid samples break a continuous window. The small
1e-9 s numerical tolerance is not an allowance for acquisition jitter.

Conservative lower bound:

```text
M_low = M(qc − absolute_qc_error, p_static + absolute_static_error)
```

The uncertainty inputs must be **positive absolute bounds**, not unexpanded
standard deviations. Correlation/coverage and installation effects belong in
the calibration assessment. For negative lower qc bound, zero is used only for
the lower-bound calculation; a negative measured qc is invalid.

Only intervals whose every sample has `M_low > 1` count. Duration is last minus
first timestamp, so 250 samples at 50 Hz span 4.98 s, not 5 s. Exit codes:
**0 CANDIDATE**, **1 INSUFFICIENT**, **2 input/configuration error**. JSON contains
window endpoints, rejected-sample reasons, calibration arguments and SHA-256 of
the exact input file. Tests generate synthetic data; no synthetic flight logs
are presented as measurements.

**CANDIDATE is only an air-data duration result.** It does not check the
M0.8-to-M1 altitude history, reciprocal headings, structural limits, landing,
logger independence or calibration authenticity. Those remain in the review
record. Do not interpolate through missing data to claim a record.

## 3. Independent records

Hash each logger's **own** file separately and retain the hashes, file sizes,
test ID, logger serial/firmware/calibration IDs and seal custody. Compare clocks,
physical signals, missing sequences and uncertainties after acquisition. Two
independent logs will ordinarily have **different** hashes and sample counts;
identical hashes are a file-copy check, not redundancy verification. An ordinary
SD card is rewritable: a mechanical seal and an archived hash provide custody
evidence, not hardware write-once storage.

Agree the altitude-loss estimator, uncertainty and clock alignment **before**
flight. A noisy barometer cannot prove strict point-by-point monotonic altitude;
an unexplained “3 m noise” or “5 m drop” exception does not satisfy 18's rule.

## 4. Bench DAQ corrections

| Existing assumption in 24 | Correct disposition |
|---|---|
| ADS1256 has eight differential channels | [TI ADS1256](https://www.ti.com/product/ADS1256) specifies **four differential / eight single-ended** inputs. Two raw bridges use four pins; five pressure plus one flow signal need six more single-ended pins. The proposed direct wiring needs ten inputs. Add qualified signal conditioning/multiplexing or converters and publish a pin map. |
| Sum of requested SPS below headline 30 kSPS proves rate | Multiplexer and PGA settling, filter latency, input common mode, source impedance, SPI scheduling and timing matter. Measure conversion-ready sample throughput and dropped conversions under all-channel load. |
| MAX31856 60 Hz rejection = 16.6 ms conversion | [Analog Devices MAX31856](https://www.analog.com/en/products/max31856.html) identifies **line-frequency filtering**. Use the datasheet conversion-time table for the actual averaging/filter mode and verify DRDY; do not count repeated register reads. No 60/100 Hz compliance claim or alternative DAQ is qualified here. |
| A 179 Hz resonance cannot alias | At 100 Hz sampling that frequency can alias; 500 Hz only raises Nyquist to 250 Hz. Measured bandwidth and analog anti-alias filtering are required. Estimated stiffness is not a modal test. |
| Gravimetric fuel flow measures engine gas mass flow | Fuel and air are separate measurements. A fuel tank measures fuel consumption. Core airflow requires a calibrated air-flow method and its own uncertainty. |

**Thrust tare:** establish zero with the engine **off**, with production hoses,
cables and fixtures installed. Characterise drift/friction/line forces using
known axial loads. Do not zero out running idle thrust; it is real force. Correct
facility/inlet momentum, nozzle pressure thrust and installation effects under
a documented force balance. A static 700 N result alone cannot establish the
450 N at-M1 flight requirement.

The promised hardware drivers and bench calibration/post-processing programs in
24 are not implemented. The new offline flight screen is not a replacement for
those programs. Raw T5/T7 sampling rates must be demonstrated independently of
the CSV write rate and independently of physical probe response time.
