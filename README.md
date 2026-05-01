# rank-986

A drag-and-rank tier list for the Porsche 986 Boxster (1997–2004) — every factory exterior color, every OEM wheel design, with live image search and source-triangulated provenance.

**Try it: [rank-986.vercel.app](https://rank-986.vercel.app)**

Built for fun. Triangulates color data across five source types (paint vendors, enthusiast archives, the Porsche Club of America, and a 1998 Porsche dealer options sheet) so each entry shows how confident you should be that it's real and named correctly.

## What it does

- **37 factory colors** with hex-approximation swatches, year ranges, paint codes, and source-confirmation badges
- **10 OEM wheel designs** with year + spec context
- **Drag to reorder** anything — saves to your browser's localStorage
- **Click "View gallery"** on any card to live-search photos via Bing — infinite scroll, in-page lightbox
- **Pin a photo** as a card's primary visual to replace the swatch with a real Boxster in that paint
- **Verified-only filter** hides single-sourced colors when you want to rank with confidence
- **Export ranking** as text, with pinned-photo URLs preserved

## Run it locally

Two paths — pick whichever's friendlier.

### Option A: Plain Python (no extra tools)

```bash
git clone https://github.com/pollybagel-labs/rank-986.git
cd rank-986
python3 server.py
```

Open http://localhost:3849. Stdlib-only — no `pip install` needed.

### Option B: Vercel CLI (matches production exactly)

```bash
npm i -g vercel
vercel dev
```

Open http://localhost:3000.

## Adapt this for another Porsche

The whole thing is one HTML file + one Python function. Forking it for a 911, 944, Cayman, etc. is mostly a data swap.

### Where the data lives

Open [`index.html`](./index.html) and look for these two arrays:

```js
const colors = [
  { name: "Speed Yellow",
    code: "12H/12G",
    type: "solid",            // solid | metallic | pearl
    years: "1997–2004",
    hex: "#FFCE00",            // visual approximation; gallery shows real photos
    family: "yellow",
    sources: ["986p","PS01","PS02","PS03","PS04","ATU00","986F","PCA"],
    conflicts: []              // human-readable notes on disagreements
  },
  // ...
];

const wheels = [
  { name: "Boxster (16\")",
    years: "1997–1999 base",
    details: "Original 5-spoke star, 16-inch standard wheel."
  },
  // ...
];
```

`SOURCES` is a small dictionary just above that maps short slugs (`PS01`, `ATU00`, etc.) to human-readable source names that show up in tooltips. Add your own slugs as you collect new sources.

### What to change

1. **Replace the `colors` array** with your model's palette. Keep the schema identical — the badge math, the verified-only filter, and the search query templating all key off these field names.
2. **Replace the `wheels` array** with your model's OEM wheels.
3. **Update the wordmark** — search the file for `986` and `Boxster` and swap. The orange `<span class="wordmark">` uses the [911 Porscha](https://www.dafont.com/911porscha.font) font for the model name.
4. **Update the page title and intro copy** at the top of `<header>` and the `<section>` intros.
5. **Update `colors-provenance.md`** with your own sources and triangulation findings (or delete it and start fresh).

### Searching is automatic

The image search wraps the primary color name in quotes and prepends `Porsche [model] [name]`. If you're forking for a 911, change the prefix in `buildColorQuery()` and `buildWheelQuery()` — about 6 lines of JS.

## Methodology

The provenance system isn't decorative — it's the point.

The list of "37 colors" you find on a single Porsche enthusiast site is rarely fully right. Names get translated weirdly (German → English), paint codes get reused across years, vendor catalogs cross-pollinate later models. The fix is **triangulation across different source TYPES**, because they catch different failure modes:

1. **Paint vendor catalogs** (PaintScratch, AutomotiveTouchup) — commercial accountability for paint codes
2. **Editorial / enthusiast archives** (986porsche.com, Stuttcars, model-specific blogs) — narrative context
3. **Owner forums + clubs** (PCA articles, 986 Forum, Rennlist) — real-world confirmation, "unicorn color" callouts
4. **Original dealer brochures / options sheets** (when you can find them) — closest to ground truth

Confidence ratings: 3+ source types confirming = ✓✓✓. 2 = ✓✓. 1 = `!` (don't trust without further verification).

Full audit trail for the 986: [`colors-provenance.md`](./colors-provenance.md).

## Architecture

- **No framework, no build step.** One HTML file, vanilla JS, [SortableJS](https://github.com/SortableJS/Sortable) via CDN for drag-and-drop.
- **Image search** is a Python serverless function ([`api/images.py`](./api/images.py)) that scrapes Bing's HTML async endpoint. No API key, no auth. Stdlib-only — `urllib`, `re`, `json`, `html`. Returns 35 thumbnails per page.
- **State** lives entirely in `localStorage`: rank order, pinned photos. No backend database.
- **Hosting**: Vercel — static files served directly, function deployed as Python serverless.
- **Fonts**: EB Garamond (serif) + Satoshi (sans) for the body, [911 Porscha](https://www.dafont.com/911porscha.font) (Daniel Zadorozny / Iconian Fonts) for the wordmark.

If Bing eventually rate-limits the function, swap to Brave Search API or SerpAPI by editing `fetch_bing_images()` in `api/images.py` — about 30 lines.

## Credits

- **Color data**: 986porsche.com, [PaintScratch](https://www.paintscratch.com/touch_up_paint/Porsche/Boxster.html), [AutomotiveTouchup](https://www.automotivetouchup.com/touch-up-paint/porsche/), [PCA "Unicorn Colors"](https://www.pca.org/news/unicorn-colors-the-porsche-986-996-edition), 1998 Porsche dealer options sheet via Autopedia
- **Image search**: Bing (scraped HTML, no API key)
- **Wordmark font**: [911 Porscha](https://www.dafont.com/911porscha.font) — free for non-commercial use
- **Body type**: EB Garamond + Satoshi
- **Drag-and-drop**: [SortableJS](https://github.com/SortableJS/Sortable)

## License

MIT — see [LICENSE](./LICENSE). Fork it, adapt it, share it. If you build a `rank-911` or `rank-944`, drop the link in [Issues](https://github.com/pollybagel-labs/rank-986/issues) — I'd love to see it.
