# Propulsion Analysis: Mach 1 RC Plane with JetCat P550-PRO

**Date:** 2026-07-12
**Engine:** JetCat P550-PRO Turbojet
**Condition:** Mach 1 @ 10,000 ft (3,048 m)

---

## 1. VERIFIED DATASHEET SPECS (JetCat P550-PRO Datasheet v1.1, 02/2023)

| Parameter | Value |
|-----------|-------|
| Thrust range | 28 – 550 N |
| RPM range | 26,000 – 83,000 |
| Mass flow | **0.93 kg/s** |
| SFC | 0.144 kg/N·h |
| EGT | 480 – 750 °C |
| Power output (shaft equivalent) | 163 kW |
| Fuel consumption | 300 – 1,650 ml/min |
| Weight | 4,900 g |
| Diameter | 175 mm |
| Fuel | Jet A1 + 3–5% turbine oil |
| Features | Barometric pressure sensor, ECU with altitude modes |

---

## 2. ALTITUDE DERATING — 74% CLAIM

**Design claim:** 550 N → 405 N at 10,000 ft (74% retention).

### Analysis

At 10,000 ft ISA:
- ρ₀ = 1.225 kg/m³ (sea level)
- ρ₁₀ₖ = 0.905 kg/m³
- **Density ratio = 0.905/1.225 = 0.739 → 74%**

The claim exactly matches the density ratio. This is the *simplest possible* altitude derating model — scale thrust by air density. In reality:

**Favorable factors:**
- The P550-PRO includes a barometric pressure sensor and an "Industrial operation mode 1" for high altitude (confirmed in the manual). The ECU can adjust fuel metering.
- The engine weight (4.9 kg) and power (163 kW) give a power-to-weight ~33 kW/kg, suggesting it's a modern, well-designed unit.

**Unfavorable factors:**
- Small-scale centrifugal compressors suffer from Reynolds number effects at altitude (lower Re → lower efficiency).
- The tiny blade passages mean viscous losses become proportionally larger at lower density.
- RC hobbyists on RCUniverse report that model turbines lose thrust faster than the density ratio alone would predict — one commenter stated "less than 10% at 20k ft."

**Verdict: 74% is aggressive but not impossible as an upper bound.** A more realistic derating factoring in Re effects and compressor off-design is probably 65–70%. However, for the sake of assessing whether the design is mathematically *plausible*, we'll accept 405 N as the optimistic static thrust at 10,000 ft.

---

## 3. RAM DRAG CALCULATION — ~280-285N CLAIM

**Design claim:** Net thrust ~280-285 N at Mach 1, 10,000 ft (30% ram drag loss).

### Assumptions & Known Values

| Parameter | Value |
|-----------|-------|
| Altitude | 10,000 ft (3,048 m) |
| Temperature (ISA) | 268.3 K (−4.85 °C) |
| Pressure | 69.7 kPa |
| Density | 0.905 kg/m³ |
| Speed of sound | a = √(γRT) = √(1.4 × 287 × 268.3) = **328 m/s** |
| Mach 1 velocity | **328 m/s** |
| Sea level mass flow | **0.93 kg/s** (datasheet) |
| Sea level static thrust | 550 N |
| Implied jet velocity (SL static) | Vj = 550/0.93 = **591 m/s** |

### Calculation Method A: Simple scaling (no ram recovery)

Mass flow at 10,000 ft = 0.93 × (ρ₁₀ₖ/ρ₀) = 0.93 × 0.739 = **0.687 kg/s**

Ram drag = ṁ × V∞ = 0.687 × 328 = **225 N**

Net thrust = Static_alt − Ram_drag = 405 − 225 = **180 N**

**This gives only 180 N — far below the 280–285 N claim. The simple method fails.**

### Calculation Method B: With ram total pressure recovery (correct approach)

At Mach 1, the inlet total pressure is significantly higher than static:
- Pt/P∞ = (1 + (γ−1)/2 × M²)^(γ/(γ−1)) = 1.2^3.5 = **1.893**
- Tt/T∞ = 1 + (γ−1)/2 × M² = **1.2**

Engine mass flow is determined by corrected mass flow (compressor pumping characteristic):

ṁ = ṁ_corr × (Pt/101325) / √(Tt/288.15)

At sea level: ṁ_corr = 0.93 kg/s

At Mach 1, 10,000 ft, assuming corrected mass flow holds at ~95% of max (lower corrected speed):
- ṁ_corr ≈ 0.88 kg/s (corrected speed drops ~5.5% at max RPM due to higher Tt)
- ṁ = 0.88 × (131,944/101,325) / √(322/288.15)
- ṁ = 0.88 × 1.302 / 1.057 = **1.084 kg/s**

Gross thrust = ṁ × Vj = 1.084 × 591 = **641 N**

Ram drag = ṁ × V∞ = 1.084 × 328 = **356 N**

Net thrust = 641 − 356 = **285 N** ✅

**This exactly matches the 280–285 N claim!** The calculation is *mathematically consistent* if:
1. Corrected mass flow is ~95% of sea level max (~0.88 kg/s)
2. Jet velocity remains near 591 m/s
3. Nozzle is choked and fully expanded

### BUT — The Turbine Temperature Problem

Here's where the simple thrust equation misses the real issue:

At Mach 1, 10,000 ft, compressor inlet total temperature = 322 K (vs. 288 K at sea level). For a compressor with PR ≈ 3.5 and ηc ≈ 0.75:

| Condition | Tt2 (compressor exit) | Combustor ΔT (to TIT=1100K) | Fuel/air ratio |
|-----------|----------------------|------------------------------|----------------|
| SL static (288K) | 458 K | 642 K | ~0.021 |
| Mach 1, 10kft (322K) | 512 K | **588 K** | ~0.019 |

The combustor temperature rise drops by ~8.4%. Less fuel means lower turbine inlet temperature for a given fuel flow, OR the engine must throttle back to stay within TIT limits. This directly reduces jet velocity.

**Revised estimate with temperature correction:**
Vj_reduced = 591 × √(588/642) ≈ 566 m/s

Gross thrust = 1.084 × 566 = **613 N**
Net = 613 − 356 = **257 N**

This suggests ~257 N is a more realistic upper bound accounting for compressor temperature rise effects. Still in the ballpark, but lower than claimed.

### Ram Drag Percentage

Net: 257 N, Gross: 613 N
Ram drag fraction = (613 − 257)/613 = **58% of gross thrust**, not 30%.

The design's "30% ram drag loss" phrasing is ambiguous. It likely means "30% loss relative to static thrust at altitude":
- (405 − 285)/405 = 30% ✅

This is a semantic clarification: they're losing 30% of the *already derated* static thrust, not 30% of gross thrust.

---

## 4. SFC CROSS-CHECK — FUEL CONSUMPTION

SFC = 0.144 kg/N·h

At Mach 1 (280 N net):
- Fuel flow = 0.144 × 280 = **40.3 kg/hr = 11.2 g/s**

**5-second supersonic dash:**
- Fuel consumed = 0.0112 × 5 = **0.056 kg = 56 grams**
- Volume (Jet A1, ρ ≈ 0.81 kg/L) = 69 ml

**Fuel capacity context:**
- Engine weight: 4.9 kg
- Remaining mass after engine: ~17 kg (includes airframe + fuel)
- If fuel is ~3 L (2.43 kg), that's ~43 × 5-second dashes
- If fuel is ~5 L (4.05 kg), that's ~72 × 5-second dashes

**At full throttle (datasheet max):**
- 1,650 ml/min = 27.5 ml/s = 22.3 g/s
- In 5 seconds: 138 ml, 111 g

**Verdict:** Fuel consumption numbers are internally consistent and realistic. The SFC of 0.144 kg/N·h is standard for this class of engine. Fuel supply is ample for burst operations.

---

## 5. EXISTING SUPERSONIC RC ATTEMPTS — LITERATURE REVIEW

### Current Speed Record
- **Niels Herbrich (Germany, 2017):** 465.5 mph (749 km/h, Mach 0.70 at altitude)
- **Guinness World Record** — has stood for nearly a decade
- Gap from record to Mach 1: ~35% speed increase required

### Active Projects

| Project | Configuration | Target | Status |
|---------|--------------|--------|--------|
| **Project BreaCH** | Dual P550-PRO + afterburners, 44 kg, delta wing | Mach 1.1 @ 1,500 m | In development, 24-month program |
| **Tomas Salvo "Reaper"** | 250 N turbojet, 5 kg delta wing | 500 mph claimed | Announced July 2026, unverified |
| **Inman Aerospace** | 3D-printed airframe | Supersonic goal | Currently at 285 mph, developing |
| **Boom Supersonic Prize** | $100K prize purse | First RC > Mach 1 | Announced July 2, 2026 |

### Key Lessons from Community

From Physics Forums and RC community discussions:

1. **Propulsion is the hardest part** — RC jet turbines lack supersonic inlets/nozzles. A custom supersonic inlet (with proper shock positioning) and variable-area nozzle are needed for sustained supersonic flight (cjl, Physics Forums).

2. **No documented supersonic RC flight exists** — "Not once" (Project BreaCH).

3. **Visual control impossible** — At Mach 1, the aircraft covers 328 m/s. It would be out of sight in seconds. FPV or autonomous control mandatory.

4. **Regulatory hurdles** — FAA Part 107 restrictions, supersonic flight prohibits over land.

5. **Transonic drag rise** — Wave drag increases sharply approaching Mach 1; requires area-ruled fuselage and thin wings.

**Project BreaCH is the most relevant comparison for this design analysis.** They target Mach 1.1 with *dual* P550-PRO engines + afterburners, producing 1,100 N total, and a 44 kg gross mass. That's 25 N/kg thrust-to-weight. A single P550-PRO design with ~280 N and ~22 kg would have ~12.7 N/kg — only half the T/W of Project BreaCH.

---

## 6. ENGINE LIMITATIONS AT MACH 1

### 6.1 Turbine Inlet Temperature Limits

- Datasheet EGT: 480–750 °C (753–1,023 K)
- Turbine inlet temperature (TIT) is typically 100–150 °C above EGT: ~850–900 °C (1,123–1,173 K)
- Inconel 718 used in small turbine wheels can handle ~980 °C continuous
- As shown above, the compressor exit temperature at Mach 1 is ~54 K higher than static, reducing the allowable temperature rise in the combustor

**Risk:** The ECU will detect rising EGT and reduce fuel flow, limiting thrust. This is the primary limiter on Mach 1 performance.

### 6.2 Compressor Surge Risk

The centrifugal compressor's operating point is defined by corrected speed and corrected mass flow. At Mach 1:

- The compressor face sees elevated total pressure (1.89×) and temperature (1.2×)
- This shifts the operating point on the compressor map toward higher pressure ratio
- **Risk of surge if the operating line crosses the surge line**
- The engine's ECU barometric sensor may provide some protection, but supersonic operation is far outside the design envelope

### 6.3 Inlet Issues

**The P550-PRO has a pitot (straight) inlet, not a supersonic inlet.** At Mach 1+:
- A normal shock forms ahead of the inlet
- At Mach 1: normal shock is very weak, total pressure recovery ≈ 1.0
- At Mach 1.1: normal shock recovery drops to ~0.99 (negligible loss still)
- At Mach 1.4: recovery drops to ~0.96
- At Mach 2.0: recovery drops to ~0.72 → major problem

**For Mach 1 only:** pitot inlet is borderline acceptable. The normal shock sits right at the lip. At exactly Mach 1, the recovery is excellent. Slight overspeed would create detached shock losses.

### 6.4 Structural Limits

- Max RPM: 83,000
- At Mach 1, the higher inlet temperature means the physical RPM must INCREASE to maintain the same corrected speed, or the thrust drops
- The engine is already at its redline at sea level; there's no headroom
- If the engine can't increase RPM, corrected speed drops, corrected mass flow drops, and thrust falls off

### 6.5 Thermal Management

- Mach 1 at 10,000 ft: stagnation temperature on the airframe = 322 K = 49 °C
- This is mild — no significant aerothermal heating at Mach 1
- But internal engine temperatures are already at their limits

---

## 7. COMPREHENSIVE VERDICT

### What Works (Green)
- ✅ **SFC and fuel consumption** are internally consistent and realistic
- ✅ **Fuel volume** is adequate for short-duration supersonic dashes
- ✅ **Density-based altitude derating** to 405 N is plausible as an upper bound
- ✅ **The mass flow × ram recovery math** shows 285 N is mathematically reachable

### What's Marginal (Yellow)
- ⚠️ **Turbine temperature limits** reduce the achievable thrust ~10% below the claim (~257 N vs 280–285 N)
- ⚠️ **The "30% ram drag loss" claim is misleading** — it's 30% of the derated static thrust, not 30% of gross thrust. Ram drag is actually ~58% of gross thrust at Mach 1
- ⚠️ **Compressor exit temperature** erodes margin to TIT limit; real thrust likely ~250–260 N
- ⚠️ **Pitot inlet at Mach 1** is borderline — acceptable for Mach 1 but any overspeed creates losses
- ⚠️ **Corrected speed drop** (~5.5%) reduces compressor pumping capacity; the engine must overspeed or lose thrust

### What's Problematic (Red)
- ❌ **No hobby turbojet has ever been successfully operated at Mach 1** — this is entirely outside the design envelope
- ❌ **The engine has no supersonic inlet** — pitot inlets work at Mach 1 but this is the absolute upper limit
- ❌ **Surge risk is unknown** — the compressor map for this specific engine is proprietary; operation at Mach 1 could stall the compressor
- ❌ **The ECU is not programmed for supersonic flight** — the barometric sensor can't compensate for ram recovery effects
- ❌ **T/W ratio ~12.7 N/kg** — half that of Project BreaCH (which uses dual engines). For reference, the F-16 has ~8 N/kg T/W at full fuel, but supersonic-capable fighters need high T/W to overcome transonic drag

### The Transonic Drag Problem

Even if the propulsion works, the airframe must overcome wave drag. The transonic drag rise typically doubles or triples total drag from Mach 0.85 to Mach 1.05. For a delta wing RC plane at Mach 1:

- Zero-lift wave drag coefficient: Cd_wave ≈ 0.02–0.05 (depends on fineness ratio, area ruling)
- With 280 N thrust, the aircraft must have total drag ≤ 280 N
- At Mach 1, 10,000 ft: dynamic pressure q = 0.5 × 0.905 × 328² = 48,800 Pa
- Drag = Cd × q × S_ref ≤ 280 N
- S_ref ≤ 280 / (0.03 × 48,800) ≤ 0.19 m² for Cd = 0.03
- This is a very slender aircraft — plausible for a small delta, but tight

### Final Verdict

> **The propulsion math is internally consistent as a theoretical upper-bound calculation, but contains significant optimistic assumptions that would likely fail in practice:**

> 1. **Thrust estimate (280–285 N) is mathematically achievable** if one assumes ideal ram recovery and no turbine temperature constraints. However, when compressor temperature rise is accounted for, real thrust drops to ~250–260 N — about right for a Mach 0.92–0.95 dash but insufficient to reliably break Mach 1.

> 2. **The core unresolved risk is the compressor surge/turbine temperature problem.** Operating a centrifugal compressor at Mach 1 flight conditions is far outside the engine's validated envelope. The ECU will likely cut fuel before reaching the required thrust.

> 3. **The existing RC speed record is 465.5 mph (Mach ~0.70).** A single P550-PRO design claiming Mach 1 represents a ~40% speed increase beyond any previous achievement. Project BreaCH — arguably the most credible supersonic RC effort to date — uses dual P550-PROs *with afterburners* for 1,100 N total thrust toward the same goal.

> **Bottom line: Plausible on paper, improbable in practice.** A single P550-PRO is likely insufficient for sustained Mach 1 flight. At best, the aircraft might achieve Mach 0.92–0.95 in a dive — tantalizingly close but not supersonic. Breaking the sound barrier with this configuration would require: (1) an afterburner, (2) a second engine, OR (3) a significantly lighter airframe with lower wave drag. The propulsion assumptions are the weakest link in the design chain.
