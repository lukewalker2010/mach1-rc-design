# 12 V rail candidate — R10 OPEN; pump BLOCKED

[33 §2](../../33_instrumentation_power.md) contains source evidence and budget.
Pololu U3V50F12 #2568 is a verified 12 V boost candidate ($29.95 list,
2026-09-16). Its 5 A switch/typical input-current figure is not a continuous
output rating. At assumed 6 V/85%, valve-only input is 1.18 A; pump operating
plus valve is 4.71 A; placeholder pump maximum plus valve is **5.41 A**.
Every corner remains unqualified; pump currents are unverified placeholders.

**ENABLE passes input power through when disabled** and is pulled up to VIN.
It is neither valve isolation nor a directly approved MCU interface. Independent
load switching/driver, flyback, release latency and coordinated protection are
TBD; no fuse rating or direct GPIO net is released.

Speck ZY-4S-12V has no verified exact primary datasheet in this review. Obtain
its identity, fuel/flow/pressure capability, motor/driver and startup/stall data
before selecting the pump rail. Actual valve data, converter thermal/output
maps, low-pack startup, EMI and independent-abort tests also remain open.
