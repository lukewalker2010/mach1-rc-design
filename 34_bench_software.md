# 34. Offline bench software contract

**2026-09-16 · Implemented offline screens; R12/R15 hardware qualification OPEN.**
Standard-library Python only. Source requirements and hardware limitations:
[25](25_readiness_review.md) R07/R11–R15,
[26](26_measurement_validation.md) §§3–4,
[33](33_instrumentation_power.md) §§3–4.
No streaming driver, controller, hardware acquisition or physical test is provided.

## Acquisition events and immutable archive segments

`tools/bench_schema.py` is shared by ingestion, post-processing and pair checking.
Input CSV columns (all required for an accepted event):

```csv
source_id,channel,sample_id,timestamp_s,value,unit,valid,source_type,run_id,test_id,logger_id,sensor_id,acquisition_path,config_hash,cal_hash,cal_sensor_id
```

- `sample_id`: nonnegative **new-conversion** sequence, consecutive per
  `(source_id, channel)`. `timestamp_s`: nonnegative finite source acquisition
  seconds, strictly increasing on that same key. Equal times across channels
  are valid. Repeated reads must not invent conversions or increment sequence.
- `value`: finite engineering value; `unit`: supported SI token (including N,
  K, Pa, V). Invalid/nonfinite measurements remain in the archive with rejection
  diagnostics. `valid=1` alone is insufficient to accept an event.
- `source_type`: exactly `BENCH`, `FLIGHT`, `CALIBRATION` or `SIMULATED`.
  Missing/unknown provenance is rejected, never defaulted to a physical source.
- Run/test/logger/config/source-type metadata must be constant across the file.
  Sensor/path/calibration/unit metadata must be constant per source/channel.
  `cal_sensor_id` must equal the actual `sensor_id`. `acquisition_path` identifies
  the physical sensor-to-converter/logging path, not an arbitrary filename.
- Config and calibration references are lowercase 64-hex SHA-256. These are
  references, **not authentication** of calibration, source type or hardware.

`daq_bench.ingest()` returns **every row** in `records` with `ingest_valid`, JSON
`ingest_errors`, `raw_record_json` and `record_hash`. Extra input metadata is
retained. No sorting, filtering, renumbering or provenance stamping occurs.
Input hashes, if present, are verified before archiving; a poisoned hash cannot
be laundered by re-ingestion. Extra CSV cells are preserved and flagged.

The hash covers **all output columns except `record_hash`**, including simulation
provenance, configuration, calibration, extra metadata and diagnostics. Canonical
encoding: string-valued object, sorted keys, compact JSON separators, unescaped
Unicode, UTF-8, SHA-256. Exact original file SHA-256 is reported separately;
retain that original file for byte-level custody (CSV whitespace is not preserved
by reserialization). Post/pair require the archive hash column on every event.

```sh
python3 tools/daq_bench.py RAW.csv -o NEW_ARCHIVE.csv
python3 tools/daq_bench.py - -o NEW_ARCHIVE.csv < RAW.csv
```

Optional `--source-id ID` and positive `--max-gap-s GAP` add rejection criteria;
the latter applies per source/channel. CLI and API use the same validation path.
Outputs use exclusive creation: existing paths, symlinks and same-input outputs
cannot be overwritten. Each invocation creates a new archive segment; there is
no in-place append/resume feature or claim that ordinary storage is write-once.
Exit **0 INGESTED**, **1 FLAGGED/EMPTY**, **2 input/configuration/I/O error**.
Malformed event rows are archived with exit 1; unreadable/malformed CSV structure
is an input error. The CLI prints a summary; the API returns the rows as well.

## Load-cell cycle analysis

`tools/cal_bench.py` accepts:

```csv
cycle,direction,known_N,measured_v,valid
```

`known_N` is N and `measured_v` is **V, not counts**. Optional `known_unit`/`unit`
must be N/V. At least two consecutive complete cycles, starting at 1, are
required, in acquisition order. Each cycle has ASC then DESC, each with at least
three strictly ordered, identical load levels; all cycles repeat those levels.
Invalid points, constant/nonmonotonic response, changed sensitivity sign,
unpaired levels and insufficient reviewed range are errors. A consistently
negative voltage sensitivity is valid and explicitly inverted.

Centred OLS fits `voltage = slope_V_per_N * force + intercept_V`; output supplies
the inverse and a centred conversion formula for numerical stability. Residuals,
per-cycle paired hysteresis, same-level/direction cycle repeatability range and
leave-one-cycle-out maximum prediction error are all in **N**. No voltage error
is divided by a force full scale. No residual is labelled expanded uncertainty.

```sh
python3 tools/cal_bench.py CAL_POINTS.csv -o NEW_ANALYSIS.json
python3 tools/cal_bench.py CAL_POINTS.csv -o NEW_LIMITED_ANALYSIS.json \
  --min-load-N "$CAL_MIN_N" --max-load-N "$CAL_MAX_N" \
  --max-residual-N "$RESIDUAL_LIMIT_N" \
  --max-hysteresis-N "$HYSTERESIS_LIMIT_N" \
  --max-repeatability-N "$REPEATABILITY_LIMIT_N" \
  --max-heldout-N "$HELDOUT_LIMIT_N"
```

All capitalised shell variables must be set from reviewed numerical criteria.
Omitted thresholds or range give **ANALYSIS_ONLY**; complete criteria give
**METRICS_WITHIN_LIMITS** or **FAIL**. Exit 0 for completed analysis/within-limits,
1 for failed metrics, 2 for input error. These statuses never certify calibration.
Load references, applied-load uncertainty, creep, zero drift, mounting/line
forces, environmental effects and calibration authenticity remain separate.

## Selected-channel static screen

```sh
python3 tools/post_bench.py NEW_ARCHIVE.csv -o NEW_SCREEN.json \
  --gate-start-s "$START_S" --gate-end-s "$END_S" \
  --min-thrust-N "$STATIC_THRESHOLD_N" \
  --thrust-uncertainty-N "$FORCE_ABSOLUTE_BOUND_N" \
  --max-temp-K "$SELECTED_TEMP_LIMIT_K" \
  --temp-uncertainty-K "$TEMP_ABSOLUTE_BOUND_K" \
  --temp-rate-hz "$SELECTED_TEMP_REQUIRED_HZ"
```

- Default required duration is **20 s**, not 19.99 s or `N/rate`. Omitted end
  means start+duration. Both selected channels must have samples at **both gate
  endpoints**; no extrapolation through missing endpoints. Alternate
  `--duration-s` requires a nonempty `--duration-review` reference.
- Default channels: `THRUST_N` in N, `TEMP_K` in K; override with
  `--thrust-channel`/`--temp-channel`. Each must retain one source throughout the
  gate. Per-channel sequence/validity and maximum time gaps are enforced.
- Thrust defaults to **500 Hz** per 26/33; `--thrust-rate-hz` cannot lower it.
  Temperature rate is explicitly supplied for the selected-channel scope.
  The `1e-9 s` comparison tolerance is floating-point tolerance, not jitter
  permission. A 19.998 s recording fails the default interval.
- Every sampled force minus the **positive absolute expanded bound** must meet
  the explicit positive thrust threshold. Time-weighted lower-endpoint force is
  also reported: sum of interval duration × minimum adjacent force, divided by
  total span, minus the bound. This is conservative against linear interpolation,
  not proof of unobserved intersample dynamics.
- Thermal screening uses **raw maximum + positive absolute bound**, never a
  smoothed mean. A single temperature sample cannot cover the interval.
- Optional paired `--thrust-min-N/--thrust-max-N` and
  `--temp-min-K/--temp-max-K` reject values at/outside explicitly calibrated
  clipping bounds. Without bounds the tool does not claim to detect sensor rails.
- Any whole-file schema/hash/metadata/sequence/invalid-event fault fails the
  screen, including faults outside the selected interval. Gate selection cannot
  hide corrupted records. Selected-channel time gaps also prevent success.
- Only consistently declared `BENCH` provenance is eligible for **SCREEN_PASS**.
  Otherwise numerically sufficient data is **NONPHYSICAL**, or **FAIL** if checks
  fail. Simulation/calibration/unknown/missing provenance cannot pass. Exit 0 only
  for SCREEN_PASS, 1 otherwise, 2 for malformed input/options.

**SCREEN_PASS is a selected-channel screen, not G0 qualification, the full G0
thermal suite, flight thrust, or release.** `physical_qualified` is always false.
No static-to-flight or 450 N conversion exists. A declared source and a hash cannot
establish that an instrument actually acquired the data.

## Concurrent-log consistency

```sh
python3 tools/log_pair_check.py ARCHIVE_A.csv ARCHIVE_B.csv -o NEW_PAIR.json \
  --calibration-record CALIBRATION_DOCUMENT.json \
  --clock-offset-s "$B_TO_A_OFFSET_S" \
  --clock-uncertainty-s "$CLOCK_ABSOLUTE_BOUND_S" \
  --alignment-tolerance-s "$ALIGNMENT_TOLERANCE_S" \
  --clock-calibration-ref "$CLOCK_CALIBRATION_REFERENCE"
```

Require **same constant run/test/config/source type**, **distinct logger, source,
sensor and acquisition-path IDs**, valid whole-log metadata, source/channel
timing/sequences and mandatory archive hashes. Identical files/records fail;
different hashes do not prove independence. SIMULATED/CALIBRATION logs fail the
physical provenance screen.

Repeat `--calibration-record` for multiple documents. Each JSON document must
contain a nonempty `sensor_ids` list; its exact byte hash must match `cal_hash`
on the corresponding sensor events. **One document can cover both sensors**.
This checks document/sensor linkage, not certificate validity or authenticity.
The cycle-analysis JSON alone is not a sensor calibration certificate.

Clock convention: `time_A = time_B + offset`. Positive absolute clock uncertainty
must bound residual clock/latency error over the entire run and be ≤ supplied
positive tolerance. Corrected common overlap across **all channels** is reduced
by twice the uncertainty and must remain positive. Start/end overlap is only
coverage, never clock calibration or a drift estimate. Missing clock arguments
or calibration documents give **UNRESOLVED**; partial/malformed clock arguments
are input errors. A complete consistent declaration gives
**CONSISTENCY_CANDIDATE**, never genuine independence or mission qualification.
`independence_proven` and `physical_qualified` are always false.
Exit 0 candidate, 1 failure/unresolved, 2 input error. All JSON outputs are
exclusive-create too; missing parent directories are reported as I/O errors.

## Verification and remaining hardware work

```sh
python3 -m unittest tests.test_bench_pipeline tests.test_log_pair_check tests.test_bench_cli -v
```

Synthetic API and subprocess CLI regressions exercise ingestion→post, calibration
and pair checks, including zero thrust, wrong units, equal multichannel times,
resets, invalid rows, missing endpoints, short duration, raw thermal spike plus
uncertainty, provenance hash poisoning, no-clobber and clean malformed-input
errors. Synthetic results are never physical qualification evidence.

R11/R12/R15 remain open: installed ADC pin/reference/common-mode/settling and
anti-alias qualification; weighted full-channel DRDY scheduling; real conversion
sequence/timestamp generation; independent logger power/sensors/custody and clock
calibration; control/abort fault injection. 33's MAX31856 subsequent-auto maximum
base period is **90 ms at 60 Hz rejection**, not 60 conversions/s; rereading a
register cannot satisfy temperature source-rate requirements. Probe bandwidth,
full G0 thermal coverage, engine-off installed tare, facility corrections,
calibration authenticity and flight matching require hardware and review.
