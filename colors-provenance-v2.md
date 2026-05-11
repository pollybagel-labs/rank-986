# 986 Boxster colors — provenance log (v2)

**Last updated:** 2026-05-10

This is v2, written after the Porsche AG factory paint reference (Printed in Germany, 2002, section 3.3.9) became available. v1 (`colors-provenance.md`) is preserved as the pre-authority snapshot — the multi-source triangulation that got us here, and the working state of the project before 2026-05-10.

---

## What changed in v2

A canonical authority source is now in play. The methodology shifts from "no authority, triangulate everything" to "authority confirmed, validate against it." Practically:

- 37 colors are now factory-confirmed by Porsche AG.
- Every prior ⚠️ "single-source" rating gets re-scored — most promoted to ✅.
- Two demoted-on-2026-05-01 colors (Fayence Yellow, Blue Turquoise) come back.
- Three year ranges and one name decision get corrected against the factory.
- Several vendor errors (ATU's pre-2001 listings, M5W aliasing, 987-era cross-pollination) are now formally rejected.

The triangulation methodology isn't dead. It still does real work — catching name translations, market-specific variants, and edge cases the factory doesn't address. But the hierarchy now has a clean apex.

---

## Source hierarchy (four tiers)

| Tier | Source | Role | Trust |
|---|---|---|---|
| **1. Factory** | Porsche AG paint reference, section 3.3.9 (Printed in Germany, 2002) | Canonical for codes, German names, model-year availability | ✅✅ Authoritative |
| **2. Editorial** | Stuttcars, 986porsche.com, PCA Unicorn Colors | English names, narrative context, special editions | ✅ Strong when consistent |
| **3. Vendor** | PaintScratch, AutomotiveTouchup | Real-world product cross-check | ⚠️ Contaminated with 987-era cross-pollination in some year listings |
| **4. Enthusiast / dealer** | 986 Forum gallery, 1998 Autopedia dealer sheet, owner records | Real-world owner confirmation, market-specific naming | ⚪ Anecdotal but useful for edge cases |

When sources conflict, factory wins. When the factory is silent (e.g. soft-top colors, interior trim, market-specific availability), the lower tiers are the only data.

---

## Headline corrections (factory overrides prior v1 decisions)

### 1. Year-range corrections

| Color | v1 range | Factory says | Reason for v1 error |
|---|---|---|---|
| Speed Yellow | 1997–2004 | **1999–2004** | 986porsche.com's start year was wrong |
| Orient Red Metallic | 2001–2003 | **2002–2004** | 986porsche.com's range was off by a year on both ends |
| Iris Blue Pearl | 1997–2000 (ATU-expanded) | **1999–2000** | ATU 1997/1998/1999 listings were wrong |
| Ocean Blue Metallic | 1997–2004 (ATU-expanded) | **1997–2000** | ATU 2001–2004 listings were wrong |

### 2. Name reversion

**Carmon Red Metallic** → **Carmona Red Metallic** (MY04 only).
Factory German is "carmonarot" — Carmona is an Andalusian town, fitting the Porsche place-name pattern (Biarritz, Carrara, Wimbledon, Vesuvio). The vendor "Carmon" version that PaintScratch and ATU used was a transcription error. v1 followed vendor consensus; v2 reverts to Carmona per factory + Stuttcars + 986porsche.com.

### 3. Re-promotions (single-source colors v1 had on the bubble)

All of these were ⚠️ in v1; factory promotes them to ✅:
- Fayence Yellow (1C1, MY04) — was removed from the live ranking on 2026-05-01. Re-added.
- Blue Turquoise (3AS/3AR, MY97–98) — was removed from the live ranking on 2026-05-01. Re-added.
- Mirage Pearl (paladio-met., 555/554, MY98–00)
- Vesuvio Metallic (40X/40W, MY98–00)
- Snow White (3AU/3AT, MY97–99)
- Pastel Yellow (12M/12L, MY97–99)
- Arena Red Pearl (84S/84R, MY97–00)
- Libel Turquoise / Ocean Jade Metallic (25K/25H, MY97–99) — kept market English name "Ocean Jade" per PCA + dealer sheet, but factory German "libelltürkis" now confirmed
- Black Metallic 744/746 (MY97–01) — confirmed as distinct color from Basalt Black C9Z (MY02–04)

### 4. Rejected vendor claims

- **ATU's "earlier than 2001" listings** for Cobalt Blue, Meridian, Seal Grey, Slate Grey — factory disagrees, drop these from the v1 source counts.
- **M5W as a Lapis Blue alias** — not in factory doc. Likely vendor error or US-market reseller code. Keep as a note but don't treat as canonical.
- **987-era cross-pollination** on ATU's late-986 pages (Crystal Silver, Sand White, Malachite Green, Jarama Beige, Dark Sea Blue) — confirmed as not real 986 colors.

---

## Factory-confirmed color matrix (37 colors)

All factory-confirmed. Confidence is now ✅ across the board, with notes for English-name disputes and code edge cases.

| English (canonical) | German (factory) | Code(s) | Years | Finish | Notes |
|---|---|---|---|---|---|
| Arctic Silver Metallic | arktissilber-met. | 92U / 92T | 1997–2004 | metallic | |
| Arena Red Pearl | arenarot-met. | 84S / 84R | 1997–2000 | pearl | Factory system code WP2/P2 |
| Atlas Grey Metallic | atlasgrau met. | M7X | 2004 | metallic | |
| Basalt Black Metallic | basaltschwarz met. | C9Z | 2002–2004 | metallic | Succeeded 744/746 |
| Biarritz White | biarritzweiß | 9A2 / 9A3 | 2000–2001 | solid | |
| Black | schwarz | 741 / 747 / 041 | 1997–2004 | solid | 741/747 pre-MY02, 041 MY02+ |
| Black Metallic | schwarz-met. | 744 / 746 | 1997–2001 | metallic | Distinct from C9Z Basalt Black |
| Blue Turquoise | blautürkis | 3AS / 3AR | 1997–1998 | solid | Re-added 2026-05-10 |
| Carmona Red Metallic | carmonarot met. | M3W | 2004 | metallic | Name reverted from "Carmon" |
| Carrara White | carraraweiß | B9A | 2002–2004 | solid | |
| Cobalt Blue Metallic | cobaltblau-met. | 3C8 / 37U | 1999–2004 | metallic | |
| Dark Blue | dunkelblau | 3C7 / 347 | 1999–2001 | solid | |
| Dark Teal Metallic | lagogrün metallic | M6W | 2003–2004 | metallic | aka Lagoon Green (986porsche) |
| Fayence Yellow | fayencegelb | 1C1 | 2004 | solid | Re-added 2026-05-10 |
| Forest Green Metallic | tannengrün-met. | 2B4 / 22E | 1999–2004 | metallic | |
| GT Silver Metallic | GT-silber met. | M7Z | 2004 | metallic | LE-only confirmed |
| Guards Red | indischrot | 84A / 80K | 1997–2004 | solid | |
| Iris Blue Pearl | irisblau-met. | 39V / 39N | 1999–2000 | pearl | Years corrected |
| Lapis Blue Metallic | lapisblau-met. | 3A8 / 3A9 | 2001–2004 | pearl | Factory system code shows pearl despite "met." in name |
| Ocean Jade Metallic | libelltürkis-met. | 25K / 25H | 1997–1999 | metallic | Market English "Ocean Jade" per PCA + dealer sheet |
| Meridian Metallic | meridian-met. | 6A6 / 6A7 | 2001–2004 | metallic | |
| Midnight Blue Pearl | nachtblau-met. | 39C / 37W | 1999–2004 | pearl | aka Dark Blue Pearl, Nachtblau |
| Mirage Pearl | paladio-met. | 555 / 554 | 1998–2000 | pearl | Existence confirmed; English name editorial-only |
| Ocean Blue Metallic | oceanblau-met. | 3AZ / 3AY | 1997–2000 | metallic | Years corrected |
| Orient Red Metallic | orientrot-met. | 8A3 / 8A4 | 2002–2004 | metallic | Years corrected. NOT Zanzibar Red. |
| Pastel Yellow | pastellgelb | 12M / 12L | 1997–1999 | solid | |
| Polar Silver Metallic | polarsilber-met. | 92M / 92E | 1999–2004 | metallic | |
| Rainforest Green Metallic | dschungelgrün-met. | 2A1 / 2A2 | 2000–2002 | metallic | Factory German literally means "Jungle Green" |
| Seal Grey Metallic | sealgrau-met. | 6B4 / 6B5 | 2001–2004 | metallic | |
| Slate Grey Metallic | schiefer-met. | 23F / 22D | 1999–2004 | metallic | |
| Snow White | firnweiß | 3AU / 3AT | 1997–1999 | solid | aka Glacier White |
| Speed Yellow | speedgelb | 12H / 12G | 1999–2004 | solid | Years corrected from 1997 start |
| Vesuvio Metallic | vesuvio-met. | 40X / 40W | 1998–2000 | pearl | |
| Viola Metallic | viola-met. | 3AE / 39G | 1999–2001 | metallic | aka Violet Blue |
| Wimbledon Green Metallic | wimbledongrün-met. | 2B6 / 23I | 1999–2001 | metallic | |
| Zanzibar Red | orangerot-perlcolor | 1A8 / 1A9 | 2000–2003 | pearl | NOT Orient Red. Image search confuses these constantly. |
| Zenith Blue Metallic | zenitblau-met. | 3AX / 3AW | 1997–2000 | metallic | |

---

## What the factory doc doesn't settle

These are out-of-scope for the 2002 factory paint reference and still need other sources:

### 1. Market availability (LHD vs RHD, US-spec, regional restrictions)

The factory doc lists global production colors. It doesn't say which markets received which colors. Some colors may have been:

- US-spec only or US-excluded (emissions/import variance)
- LHD vs RHD market splits (UK, Australia, Japan, South Africa)
- Limited-run regional editions
- Paint-to-sample (PTS) special orders outside the standard catalog

**This is the next research arc.** Sources to investigate:
- US-spec dealer brochures by model year
- UK Porsche GB sales literature
- Japan/Australia/RHD-market dealer materials
- Owner registries with build sheets

### 2. Soft top colors

Stuttcars lists 4: Black, Cocoa Brown, Graphite Grey, Metropol Blue. Factory paint reference doesn't cover top/interior trim. Need a separate factory document or dealer sheet for top availability by year.

### 3. Interior color codes

A Stuttcars commenter (Nicola Cerreto, 2025) asks about interior code A1 on a 2002 Boxster S. No interior color reference document is available yet. Need the interior trim version of the factory doc.

### 4. Paint-to-sample (PTS) special orders

Factory doc is the production catalog. PTS cars exist outside this scope by definition. Anyone tracking PTS 986s needs registry-style enthusiast data.

### 5. English-name disputes

Where editorial sources disagree, the factory only resolves the German. Examples:
- Mirage Pearl vs Paladio Pearl (factory says "paladio-met.")
- Rainforest vs Jungle Green (factory says "dschungelgrün-met.", literally Jungle)
- Midnight Blue Metallic vs Dark Blue Pearl vs Nachtblau Pearl
- Snow White vs Glacier White
- Libel Turquoise vs Ocean Jade

These will stay as "primary + aliases" until US/UK market literature settles them.

---

## Methodology change-log

| Date | Event |
|---|---|
| 2026-05-01 | v1 published. 3-source-type triangulation. Demoted Fayence Yellow + Blue Turquoise to "not enough evidence." |
| **2026-05-10** | **Factory PDF acquired. v2 published. Re-promotions, year corrections, name reversion (Carmon → Carmona), vendor errors rejected. LHD/RHD market research opened as next arc.** |
