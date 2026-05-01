# rank-986

A drag-and-rank tier list for the Porsche 986 Boxster (1997–2004) — every factory exterior color, every OEM wheel design, with live image search and provenance.

Built for fun. Triangulates color data across five source types (paint vendors, enthusiast archives, the Porsche Club of America, and a 1998 Porsche dealer options sheet) so each entry shows how confident you should be that it's real and named correctly.

## What it does

- **37 factory colors** with hex-approximation swatches, year ranges, paint codes, and source-confirmation badges
- **10 OEM wheel designs** with year + spec context
- **Drag to reorder** anything — saves to your browser's localStorage
- **Click "View gallery"** on any card to live-search photos via Bing — infinite scroll, in-page lightbox
- **Pin a photo** as a card's primary visual to replace the swatch with a real Boxster in that paint
- **Verified-only filter** hides single-sourced colors when you want to rank with confidence
- **Export ranking** as text, with pinned-photo URLs preserved

## Running locally

```bash
npm i -g vercel    # if you don't have it
vercel dev
```

Then open http://localhost:3000.

## Provenance

The full audit trail of which sources confirmed each color (and which conflicted) lives in [colors-provenance.md](./colors-provenance.md).

## Credits

- Color data: 986porsche.com, PaintScratch, AutomotiveTouchup, [PCA Unicorn Colors article](https://www.pca.org/news/unicorn-colors-the-porsche-986-996-edition), 1998 Porsche dealer options sheet via Autopedia
- Image search: Bing (scraped, no API key)
- Wordmark font: [911 Porscha](https://www.dafont.com/911porscha.font) by Daniel Zadorozny / Iconian Fonts (free for non-commercial use)
- Body type: EB Garamond + Satoshi
