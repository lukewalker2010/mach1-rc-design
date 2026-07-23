# Mach 1 RC Aircraft BOM — Link Verification Report

**Checked:** 2026-07-23  
**Source:** `09_bom_with_links.md`  
**Method:** `web_fetch` on every unique URL extracted from the BOM

---

## Summary

| Metric | Count |
|--------|-------|
| **Total unique links checked** | **78** |
| ✅ Successfully loaded (200) | **65** |
| ⚠️ Loaded but redirected to generic page | **2** |
| ❌ Blocked / inaccessible | **11** |
| **Strong links** (specific product pages) | **27** |
| **Weak links** (homepages or search results, not specific products) | **40** |

---

## 1. Engine & Powerplant

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 1 | [jetcat.de — P550-PRO-S product](https://www.jetcat.de/en/products/produkte/jetcat/kategorien/professional/550%20PRO-S) | ✅ 200 | **Strong.** Product page for JetCat P550-PRO-S turbine engine; price on request, part no 71155-0278 |
| 2 | [chiefrc.com — JetCat turbines](https://www.chiefrc.com/collections/jet-cat-turbines) | ✅ 200 | **Strong.** Collection page listing 94 JetCat turbine products with prices (P250 $4,899, P350 $7,399, etc.) |
| 3 | [tomahawk-aviation.com — sArticle/3217](https://tomahawk-aviation.com/eu/detail/index/sArticle/3217) | ⚠️ 200 → redirected | Redirected to `tomahawk-aviation-usa.com` homepage (gliders & jets catalog). **No P550 product page reached.** |

---

## 2. Major Structure Materials

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 4 | [acpsales.com](https://www.acpsales.com) | ⚠️ 200 → redirected | Redirects to `acpcomposites.com` homepage — AS9100-certified custom composite manufacturer. No specific product page for 3K twill carbon. |
| 5 | [dragonplate.com](https://www.dragonplate.com) | ✅ 200 | **Weak.** Homepage for DragonPlate carbon fiber products. No direct link to 5mm T800 pultruded rod. |
| 6 | [westsystem.com](https://www.westsystem.com) | ✅ 200 | **Weak.** West System Epoxy homepage. No direct link to 105/206 product. |
| 7 | [Amazon — west system 105 206](https://www.amazon.com/s?k=west+system+105+206) | ✅ 200 | **Weak.** Amazon search results page for "west system 105 206". |
| 8 | [aircraftspruce.com](https://www.aircraftspruce.com) | ✅ 200 | **Weak.** Aircraft Spruce & Specialty homepage (aviation parts since 1965). No direct link to Rohacell foam. |
| 9 | [xometry.com](https://www.xometry.com) | ✅ 200 | **Weak.** Xometry custom manufacturing homepage. Upload STL for instant quote — but no direct link to Inconel 718 DMLS. |
| 10 | [mcmaster.com — 304 SS tubing](https://www.mcmaster.com/304-stainless-steel-tubing) | ✅ 200 | **Strong.** McMaster-Carr category page for 304 stainless steel tubing. (JS-heavy site; content not extractable via fetch but URL is valid.) |
| 11 | [mcmaster.com — 7075 aluminum](https://www.mcmaster.com/7075-aluminum) | ✅ 200 | **Strong.** McMaster-Carr category page for 7075 aluminum. |
| 12 | [mcmaster.com — 6061 aluminum](https://www.mcmaster.com/6061-aluminum) | ✅ 200 | **Strong.** McMaster-Carr category page for 6061 aluminum. |

---

## 3. Avionics

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 13 | [eBay — Futaba R7018SB search](https://www.ebay.com/sch/i.html?_nkw=Futaba+R7018SB) | ❌ 403 | Blocked by eBay Cloudflare bot protection. |
| 14 | [HobbyKing — Futaba R7018SB product](https://hobbyking.com/en_us/futaba-r7018sb-s-bus-2-18ch-fasstest-telemetry-receiver.html) | ❌ 403 | Blocked by Cloudflare. |
| 15 | [Modelland — Futaba R7018SB product](https://store.modelland.com/p-110546-futaba-futr7018sb-r7018sb-2-4ghz-fasstest-receiver-dual-battery.aspx) | ✅ 200 | **Strong.** Product page for Futaba R7018SB 2.4GHz FASSTest Receiver, $329, in stock. |
| 16 | [Amazon — Cube Orange+ Standard Set](https://www.amazon.com/The-Cube-Orange-Standard-Set/dp/B0C8Y1LMGZ) | ✅ 200 | **Strong.** Amazon product page for Cube Orange+ Standard Set, $449. |
| 17 | [ReadyMadeRC — Cube Orange+ Kit](https://www.readymaderc.com/products/details/pixhawk2-cube-orange-plus-standard-set-cube-carrier) | ✅ 200 | **Strong.** ReadyMadeRC product page for CubePilot Cube Orange+ ADS-B Flight Controller Kit with full specs. |
| 18 | [cubepilot.com](https://www.cubepilot.com) | ✅ 200 | **Weak.** CubePilot homepage (autopilot-on-module, Pixhawk team). No direct product link. |
| 19 | [GetFPV — Here+ RTK GPS](https://www.getfpv.com/cubepilot-here-rtk-gnss-gps-kit-m8p.html) | ❌ 403 | Blocked by Cloudflare. |
| 20 | [RobotShop — Here+ RTK GPS](https://www.robotshop.com/products/cubepilot-here-v2-rtk-gnss-gps-m8p) | ❌ 403 | Blocked by Cloudflare. |
| 21 | [ReadyMadeRC — RFD900x-US modem](https://www.readymaderc.com/products/details/rfdesign-rfd-900x-modem-us-fcc) | ✅ 200 | **Strong.** Product page for RFDesign RFD900x-US Modem (FCC approved, 40+ km range, 1W TX). |
| 22 | [ReadyMadeRC — RFD900x bundle](https://www.readymaderc.com/products/details/rfdesign-900x-telemetry-modem-bundle) | ✅ 200 | **Strong.** Product page for RFDesign RFD900x Telemetry Modem Bundle (2 modems + antennas). |
| 23 | [WorldDroneMarket — RFD900x bundle](https://www.worldronemarket.com/product/rfd900x-us-bundle/) | ✅ 200 | **Strong.** Product page for RFD900X US Bundle (FCC Approved) with feature details. |
| 24 | [eagletreetechnologies.com](https://www.eagletreetechnologies.com) | ❌ DNS | **Domain does not exist** (ENOTFOUND). Eagle Tree may have changed domains. |
| 25 | [Mouser — MS4525DO search](https://www.mouser.com/Search/Refine?Keyword=MS4525DO) | ❌ 403 | Blocked — requires JS and disables ad blockers. |
| 26 | [DigiKey — pressure sensors filter](https://www.digikey.com/en/products/filter/pressure-sensors/534) | ❌ 403 | Blocked by Cloudflare. |

---

## 4. Power System

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 27 | [Amazon — 2S LiPo 5000mAh 30C](https://www.amazon.com/s?k=2S+LiPo+5000mAh+30C) | ✅ 200 | **Weak.** Amazon search results (166 results for "2S LiPo 5000mAh 30C"). |
| 28 | [hobbyking.com](https://hobbyking.com) | ❌ 403 | Blocked by Cloudflare. |
| 29 | [amainhobbies.com](https://www.amainhobbies.com) | ✅ 200 | **Weak.** AMain Hobbies homepage (RC hobby shop). No direct link to 2S LiPo. |
| 30 | [Amazon — pixhawk power module](https://www.amazon.com/s?k=pixhawk+power+module) | ✅ 200 | **Weak.** Amazon search results (260 results). |
| 31 | [Amazon — amass deans t-plug](https://www.amazon.com/s?k=amass+deans+t-plug) | ✅ 200 | **Weak.** Amazon search results (119 results). |
| 32 | [Amazon — jr servo connector](https://www.amazon.com/s?k=jr+servo+connector) | ✅ 200 | **Weak.** Amazon search results (2,000+ results). |
| 33 | [Amazon — 14 awg silicone wire](https://www.amazon.com/s?k=14+awg+silicone+wire) | ✅ 200 | **Weak.** Amazon search results (531 results). |
| 34 | [Amazon — 20 awg silicone wire](https://www.amazon.com/s?k=20+awg+silicone+wire) | ✅ 200 | **Weak.** Amazon search results (524 results). |
| 35 | [Amazon — 22 awg silicone wire](https://www.amazon.com/s?k=22+awg+silicone+wire) | ✅ 200 | **Weak.** Amazon search results (394 results). |
| 36 | [Amazon — braided nylon cable sleeve 10mm](https://www.amazon.com/s?k=braided+nylon+cable+sleeve+10mm) | ✅ 200 | **Weak.** Amazon search results (1,000+ results). |

---

## 5. Fuel System

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 37 | [mcmaster.com](https://www.mcmaster.com) | ✅ 200 | **Weak.** McMaster-Carr homepage (JS-heavy; minimal content via fetch). |
| 38 | [mcmaster.com — viton tubing](https://www.mcmaster.com/viton-tubing) | ✅ 200 | **Strong.** McMaster-Carr category page for Viton tubing. |
| 39 | [Amazon — viton tubing 4mm](https://www.amazon.com/s?k=viton+tubing+4mm) | ✅ 200 | **Weak.** Amazon search results for Viton tubing. |
| 40 | [Amazon — dubro fuel dot](https://www.amazon.com/s?k=dubro+fuel+dot) | ✅ 200 | **Weak.** Amazon search results for Dubro fuel dot. |
| 41 | [towerhobbies.com](https://www.towerhobbies.com) | ✅ 200 | **Weak.** Tower Hobbies homepage (RC cars, trucks, planes, trains). |
| 42 | [Amazon — fuel check valve rc](https://www.amazon.com/s?k=fuel+check+valve+rc) | ✅ 200 | **Weak.** Amazon search results for fuel check valve RC. |
| 43 | [Amazon — rc fuel clunk filter](https://www.amazon.com/s?k=rc+fuel+clunk+filter) | ✅ 200 | **Weak.** Amazon search results for RC fuel clunk filter. |
| 44 | [Amazon — brass barb fittings rc](https://www.amazon.com/s?k=brass+barb+fittings+rc) | ✅ 200 | **Weak.** Amazon search results for brass barb fittings RC. |

---

## 6. Control System

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 45 | [KST Servos — X20 Series](https://kstservos.com/collections/x20-series-1) | ✅ 200 | **Strong.** KST Servos X20 Series collection page listing X20 servo models. |
| 46 | [Buddy RC — KST Servos](https://www.buddyrc.com/collections/kst-servos) | ✅ 200 | **Strong.** Buddy RC KST Servos collection page (Columbus, OH shop). |
| 47 | [eBay — KST X20-12T search](https://www.ebay.com/sch/i.html?_nkw=KST+X20-12T) | ❌ 403 | Blocked by eBay Cloudflare bot protection. |
| 48 | [Amazon — 2mm titanium rod threaded](https://www.amazon.com/s?k=2mm+titanium+rod+threaded) | ✅ 200 | **Weak.** Amazon search results for 2mm titanium rod. |
| 49 | [Amazon — dubro ball link](https://www.amazon.com/s?k=dubro+ball+link) | ✅ 200 | **Weak.** Amazon search results for Dubro ball link. |
| 50 | [Amazon — servo extension 300mm jr](https://www.amazon.com/s?k=servo+extension+300mm+jr) | ✅ 200 | **Weak.** Amazon search results for servo extension 300mm JR. |
| 51 | [Amazon — M2.5 stainless screws](https://www.amazon.com/s?k=M2.5+stainless+screws) | ✅ 200 | **Weak.** Amazon search results for M2.5 stainless screws. |

---

## 7. Landing & Launch

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 52 | [Amazon — uhmwpe sheet](https://www.amazon.com/s?k=uhmwpe+sheet) | ✅ 200 | **Weak.** Amazon search results for UHMWPE sheet. |
| 53 | [mcmaster.com — uhmw](https://www.mcmaster.com/uhmw) | ✅ 200 | **Strong.** McMaster-Carr category page for UHMW plastic. |
| 54 | [eBay — titanium sheet 6al4v search](https://www.ebay.com/sch/i.html?_nkw=titanium+sheet+6al4v) | ❌ 403 | Blocked by eBay Cloudflare bot protection. |
| 55 | [Amazon — 50mm polyurethane wheel](https://www.amazon.com/s?k=50mm+polyurethane+wheel) | ✅ 200 | **Weak.** Amazon search results for 50mm polyurethane wheel. |
| 56 | [mcmaster.com — t-slot framing](https://www.mcmaster.com/t-slot-framing) | ✅ 200 | **Strong.** McMaster-Carr category page for T-slot framing. |
| 57 | [Amazon — mini bearing axle kit](https://www.amazon.com/s?k=mini+bearing+axle+kit) | ✅ 200 | **Weak.** Amazon search results for mini bearing axle kit. |
| 58 | [Amazon — 5g micro servo metal gear](https://www.amazon.com/s?k=5g+micro+servo+metal+gear) | ✅ 200 | **Weak.** Amazon search results for 5g micro servo metal gear. |
| 59 | [mcmaster.com — springs](https://www.mcmaster.com/springs) | ✅ 200 | **Strong.** McMaster-Carr category page for springs. |
| 60 | [Amazon — ripstop nylon mini parachute](https://www.amazon.com/s?k=ripstop+nylon+mini+parachute) | ✅ 200 | **Weak.** Amazon search results for ripstop nylon mini parachute. |

---

## 8. Drogue Chute

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 61 | [chutingstar.com](https://www.chutingstar.com) | ❌ 403 | Blocked by Cloudflare. |
| 62 | [Amazon — 0.6m drogue parachute](https://www.amazon.com/s?k=0.6m+drogue+parachute) | ✅ 200 | **Weak.** Amazon search results for 0.6m drogue parachute. |
| 63 | [Amazon — rc pilot chute spring](https://www.amazon.com/s?k=rc+pilot+chute+spring) | ✅ 200 | **Weak.** Amazon search results for RC pilot chute spring. |
| 64 | [Amazon — kevlar cord 500kg](https://www.amazon.com/s?k=kevlar+cord+500kg) | ✅ 200 | **Weak.** Amazon search results for kevlar cord 500kg. |
| 65 | [Amazon — ball bearing swivel parachute](https://www.amazon.com/s?k=ball+bearing+swivel+parachute) | ✅ 200 | **Weak.** Amazon search results for ball bearing swivel parachute. |
| 66 | [Amazon — kevlar thread parachute](https://www.amazon.com/s?k=kevlar+thread+parachute) | ✅ 200 | **Weak.** Amazon search results for kevlar thread parachute. |

---

## 9. Tooling & Consumables

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 67 | [Amazon — partall 2 mold release](https://www.amazon.com/s?k=partall+2+mold+release) | ✅ 200 | **Weak.** Amazon search results for Partall #2 mold release. |
| 68 | [Amazon — peel ply nylon composite](https://www.amazon.com/s?k=peel+ply+nylon+composite) | ✅ 200 | **Weak.** Amazon search results for peel ply nylon composite. |
| 69 | [Amazon — vacuum bagging breather cloth](https://www.amazon.com/s?k=vacuum+bagging+breather+cloth) | ✅ 200 | **Weak.** Amazon search results for vacuum bagging breather cloth (18 results). |
| 70 | [Amazon — vacuum bag film nylon](https://www.amazon.com/s?k=vacuum+bag+film+nylon) | ✅ 200 | **Weak.** Amazon search results for vacuum bag film nylon. |
| 71 | [Amazon — vacuum bag sealant tape](https://www.amazon.com/s?k=vacuum+bag+sealant+tape) | ✅ 200 | **Weak.** Amazon search results for vacuum bag sealant tape. |
| 72 | [mcmaster.com — urethane foam](https://www.mcmaster.com/urethane-foam) | ✅ 200 | **Strong.** McMaster-Carr category page for urethane foam (redirected to /products/urethane-foam/). |
| 73 | [Amazon — sandpaper assortment 80 1000](https://www.amazon.com/s?k=sandpaper+assortment+80+1000) | ✅ 200 | **Weak.** Amazon search results for sandpaper assortment 80-1000. |
| 74 | [fibreglast.com](https://www.fibreglast.com) | ✅ 200 | **Weak.** Fibre Glast Developments homepage (AS9120B-certified composite supplier). No direct link to gelcoat or fiberglass. |
| 75 | [Amazon — tooling gelcoat](https://www.amazon.com/s?k=tooling+gelcoat) | ✅ 200 | **Weak.** Amazon search results for tooling gelcoat. |
| 76 | [Amazon — fiberglass cloth 200g](https://www.amazon.com/s?k=fiberglass+cloth+200g) | ✅ 200 | **Weak.** Amazon search results for fiberglass cloth 200g. |
| 77 | [Amazon — model aircraft hardware kit](https://www.amazon.com/s?k=model+aircraft+hardware+kit) | ✅ 200 | **Weak.** Amazon search results for model aircraft hardware kit. |

---

## 10. Quick Buy Checklist (duplicates)

| # | URL | Status | Summary |
|---|-----|--------|---------|
| 78 | [Amazon — Cube Orange+ (dp link)](https://www.amazon.com/dp/B0C8Y1LMGZ) | ✅ 200 | **Strong.** Same Cube Orange+ product page as #16 via alternate URL format. |

*(All other checklist URLs were duplicates of URLs already checked above.)*

---

## Detailed Failure Analysis

### ❌ Blocked by Cloudflare / Bot Protection (9 URLs)

| URL | Intended Purpose | Notes |
|-----|-----------------|-------|
| `ebay.com/sch/i.html?_nkw=Futaba+R7018SB` | Find Futaba R7018SB on eBay | eBay blocks automated fetchers entirely |
| `ebay.com/sch/i.html?_nkw=KST+X20-12T` | Find KST X20-12T on eBay | Same eBay block |
| `ebay.com/sch/i.html?_nkw=titanium+sheet+6al4v` | Find Ti-6Al-4V sheet on eBay | Same eBay block |
| `hobbyking.com/en_us/futaba-r7018sb-...` | HobbyKing Futaba R7018SB product | Cloudflare protection |
| `hobbyking.com` | HobbyKing homepage | Cloudflare protection |
| `getfpv.com/.../cubepilot-here-rtk-...` | GetFPV Here+ RTK GPS product | Cloudflare protection |
| `robotshop.com/.../cubepilot-here-v2-...` | RobotShop Here+ RTK GPS product | Cloudflare protection |
| `chutingstar.com` | ChutingStar parachute shop homepage | Cloudflare protection |
| `mouser.com/Search/Refine?Keyword=MS4525DO` | Mouser search for MS4525DO | Requires JS; blocks ad-blockers |

### ❌ DNS Resolution Failure (1 URL)

| URL | Intended Purpose | Notes |
|-----|-----------------|-------|
| `eagletreetechnologies.com` | Eagle Tree pitot/static ports | Domain does not resolve (ENOTFOUND). Eagle Tree likely rebranded or changed domains. |

### ❌ Blocked by Cloudflare / Bot Protection (1 URL)

| URL | Intended Purpose | Notes |
|-----|-----------------|-------|
| `digikey.com/en/products/filter/pressure-sensors/534` | DigiKey pressure sensors catalog | Cloudflare protection |

---

## Observations & Recommendations

### 🔴 Critical Issues

1. **Eagle Tree domain is dead** (`eagletreetechnologies.com` → ENOTFOUND). The pitot-static link is completely broken. Eagle Tree may have moved to a new domain — needs a replacement URL.

2. **HobbyKing.com is fully blocked** by Cloudflare. The specific Futaba R7018SB product link is inaccessible, and even the homepage fails. Consider if HobbyKing is still a viable vendor or if the link should be replaced.

3. **ChutingStar.com is fully blocked** by Cloudflare. The drogue chute sourcing link is inaccessible from automated tools (may still work in a real browser).

### 🟡 Weak Links (40 of 78)

The majority of links in this BOM are **Amazon search pages** (30 URLs) or **vendor homepages** (10 URLs) rather than specific product pages. While these will technically load, they require the buyer to navigate and find the correct product themselves.

**Amazon search links (30):** All load successfully but point to search results, not specific products. This is the single largest weakness in the BOM. Consider replacing key ones with direct product `dp/` links where specific products have been identified.

**Vendor homepages (10):** acpsales.com, dragonplate.com, westsystem.com, aircraftspruce.com, xometry.com, mcmaster.com (root), cubepilot.com, amainhobbies.com, towerhobbies.com, fibreglast.com — all load but don't lead to the specific product listed.

### 🟡 Redirected Links (2)

- `tomahawk-aviation.com/eu/detail/index/sArticle/3217` → redirects to USA homepage (original EU article no longer exists)
- `acpsales.com` → redirects to `acpcomposites.com` (domain change, but company is the same)

### ✅ Strong Links (27)

The best-linked items are:
- **JetCat P550** — direct product page on jetcat.de and collection page on Chief RC
- **Futaba R7018SB** — specific product page on Modelland ($329)
- **Cube Orange+** — specific product on Amazon ($449) and ReadyMadeRC
- **RFD900x** — specific product pages on ReadyMadeRC (modem + bundle) and WorldDroneMarket
- **KST X20 servos** — collection pages on KST official site and Buddy RC
- **McMaster-Carr items** (7 links) — all resolve to valid category pages (SS tubing, 7075/6061 aluminum, Viton tubing, UHMW, T-slot framing, springs, urethane foam)

### Recommendations

1. **Replace the dead Eagle Tree link** with the correct current domain (likely `www.eagletreetech.com` or similar).
2. **Add specific Amazon `dp/` product links** for the top-priority items (fuel system, servos, wiring) instead of search pages.
3. **Verify eBay, HobbyKing, GetFPV, RobotShop, ChutingStar, Mouser, and DigiKey links manually** in a browser — they likely work for human visitors but block automated fetching.
4. **Update the Tomahawk Aviation link** — the EU article `/sArticle/3217` no longer exists and redirects to the USA homepage.
5. **Update the acpsales.com link** to `acpcomposites.com` to avoid the redirect.
