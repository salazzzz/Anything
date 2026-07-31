# Euro Detailing — new site build, handoff

**Status: staged for launch, not yet live.** The new design now sits at the repo
root on this branch and is wired to the real URLs. `main` and eurodetailing.com
are still untouched — merging this branch is what makes it live.

- **Branch:** `claude/hello-gddz2h`
- **PR:** [salazzzz/Anything#1](https://github.com/salazzzz/Anything/pull/1) (draft)
- **Preview:** the branch preview URL now serves the new site at its **root**
  (`/`, `/services/interior`, `/membership`, …), not under `/preview`.
- **Vercel project:** `website` under `eric-salas-projects`, connected to this
  repo via the Git integration, so any push to the branch redeploys the preview
  automatically.

### Before you merge

**Confirm the membership prices.** The three cadences in `_build/gen_membership.py`
are a proposal, not Eric's numbers. The every-2-weeks column is the existing live
pricing; monthly and every-3-months are new. See the module docstring for how they
were derived.

**Check the exterior Deep Clean durations.** Sedan still reads `~1 hr`, the same as
Basic SUV/XL, despite adding clay bar, acid wash, decontamination and a 6-month
sealant. This was deliberately left alone — only Eric knows the real process time,
and a wrong number here misplans his day.

---

## Pages

All at the root, on the URLs that already rank.

| Page | URL | File | Notes |
|---|---|---|---|
| Home | `/` | `index.html` | Hand-written. Not generated. |
| Interior | `/services/interior` | `services/interior.html` | Generated |
| Exterior | `/services/exterior` | `services/exterior.html` | Generated |
| Bundle | `/services/bundle` | `services/bundle.html` | Generated |
| Membership | `/membership` | `membership.html` | Generated |
| Add-ons | `/addons` | `addons.html` | Generated |
| Gallery | `/gallery` | `gallery.html` | Generated from `data/gallery.json` |
| Reviews | `/reviews` | `reviews.html` | Generated. `/testimonials` 301s here |

Stylesheets: `tpl.css` (service pages + shared shell), `gallery.css`,
`reviews.css`. The homepage keeps its CSS inline in a `<style>` block.

Every page links the **real** `/styles.css` and `/script.js`, so the header,
buttons and reveal animations are the genuine components rather than copies.

### The build modules

| Module | Owns |
|---|---|
| `_build/seo.py` | Every business fact, the `<head>` block, and all JSON-LD. One source of truth. |
| `_build/shell.py` | Skip link, header, footer. Shared by every generated page. |
| `_build/addondata.py` | The seven add-ons, used by both the service pages and `/addons`. |
| `_build/gen_sitemap.py` | `sitemap.xml`, `llms.txt`, `robots.txt`. |

Regenerate everything:

    python3 _build/gen_services.py && python3 _build/gen_addons.py \
      && python3 _build/gen_membership.py && python3 _build/gen_gallery.py \
      && python3 _build/gen_reviews.py && python3 _build/gen_sitemap.py

---

## Home page, top to bottom

1. **Header** — real site header. Nav trimmed to Services · FAQ · Contact.
   Membership, Gallery, Reviews and Service Area were all removed, and the
   mobile "More" dropdown went with them since Reviews was all it held.
   Book Now is the "wet gloss" button (variant B of four that were shown).
2. **Hero** — full container width so it lines up with the header. Left: accent
   rule, locality eyebrow, `.location-pill`, headline, subtitle, then
   *View Services* and *View Gallery* stacked as bar buttons. Right: the
   vertical clip autoplaying muted on loop in a 4:5 card with a wet-look
   gradient border, mute toggle in the corner.
3. **Reviews + service area** — rating badge, three-card white carousel
   (arrows on the flanks, wraps the short way round), *See all reviews* bar.
   Right: service-area map and the radius checker.
4. **Services** — three full-bleed cards with price chips, linking to the
   service pages.
5. **Story + Why Euro Detailing** — Eric's introduction with a signature block;
   three numbered reasons opposite.
6. **FAQ + contact** — seven question pills opening a popup; contact rows,
   hours, payment, CTA and socials.
7. **Footer** — four columns over a bottom bar: brand, Services, Explore, and
   Get in touch. Shared with every other page via `_build/shell.py`. Gallery,
   Reviews, Add-ons and Membership had no site-wide links before this and were
   effectively orphaned; the footer is now the internal link graph.

---

## Things that will bite you if you don't know them

### 1. `cleanUrls` breaks relative links
`vercel.json` sets `cleanUrls: true` and `trailingSlash: false`, so
`services/interior.html` is served at `/services/interior` — **no trailing
slash and no extension**. A relative link like `bundle.html` then resolves
against `/services/`, which is not what you expect, and a relative `../images/…`
from a page one directory deep resolves differently than from the root. Every
in-page link and asset path is therefore **root-absolute**: `/`,
`/services/interior`, `/gallery`, `/images/logo.webp`. Keep it that way.

`python3 -m http.server` does not emulate this. Use
`python3 _build/vercelish.py` (port 8902) instead.

### 2. Images and videos are cached immutably
`vercel.json` serves `/images/*` and `/videos/*` with
`max-age=31536000, immutable`. Browsers will not revalidate. **Replacing a
file's contents without changing its filename ships nothing to anyone who has
already visited.** The hero video is `videos/hero-vertical-v2.mp4` for exactly
this reason. Version the filename on every swap.

### 3. Don't reuse class names from `styles.css`
`styles.css` already defines `.faq-shell` with `max-width: 920px`. Naming a
section that capped it at 920px inside a 1920px viewport while every sibling
sat at 1200 — it presented as a mystery empty band on the right. It is now
`.qa-shell`. Before inventing a class, check:

```bash
grep -nE '^\.your-name' styles.css
```

Deliberate reuse: `.container`, `.g-logo`, `.header-actions`, `.is-visible`.

### 4. `[hidden]` loses to an author `display` rule
The gallery filter set `hidden` on tiles and nothing happened, because
`.tile { display: block }` outranks the UA sheet's `[hidden] { display: none }`.
`.tile[hidden] { display: none }` is declared explicitly. Same trap applies to
any new filter.

### 5. Autoplay and `opacity: 0` don't mix
The reveal system sets `opacity: 0` on every child of a `[data-reveal-group]`.
No browser starts a muted autoplay video that isn't visible, and `opacity: 0`
counts — the hero clip silently never played. `.hero-right > .frame-stack` now
keeps `opacity: 1` and only scales. If autoplay ever stops again, check that
first.

Safari can still refuse (Low Power Mode, or a per-site auto-play setting). That
is not a bug in the page — `play()` rejecting adds `.needs-tap` to the frame,
which fades in a blue play control instead of Safari's grey placeholder.

### 6. Review card heights are measured, not computed
`_build/gen_reviews.py` holds a `MEASURED` dict of each card's rendered pixel height
from Chromium. The three-column balance and the CTA's vertical position are
solved from those numbers. **Editing review text drifts the layout.** Re-measure
in the console:

```js
document.querySelectorAll('.rv').forEach(c => console.log(
  c.querySelector('.rv-name').textContent.trim(),
  Math.round(c.getBoundingClientRect().height)))
```

### 7. Animations replay on scroll-up via a second observer
`script.js` reveals once then unobserves — correct for the live site, and it is
a **shared file, so it was not modified**. A second observer in
`index.html` toggles the class both ways. Entering staggers 80ms per
child; leaving clears the delay so a block exits together.

---

## Data, verified

- **18 Cal.com slugs** across the service pages, checked identical to the live
  site. This includes `permium-exterior-detail-sedan` — the misspelling appears
  to be the real event name on Cal.com. **Worth confirming in the Cal.com
  account**; if it is wrong, fix it there and in the pages.
- **Prices** match the live site: interior 105/125/145 and 165/190/215,
  exterior 70/85/100 and 105/120/135, bundle 150/180/210 and 230/265/300.
- **Radius is 10 miles**, down from 15. That value appears in four places — the
  constant, the map caption, the modal copy and the fallback message. Note
  `llms.txt` and the schema still list Boston as served, which 10 miles mostly
  excludes.
- **Radius centre** is `42.3487, -71.2276`, the coordinate pair already in the
  site's schema. **Deliberately not 24 Lill Avenue** — client-side JS ships to
  every visitor. The distance maths is identical either way.
- **Geocoding** runs in the visitor's browser against OpenStreetMap's
  Nominatim. No key, no server. Fine at this traffic; swap for a paid geocoder
  if the site takes off.
- **10 Google reviews**, full text, plus Eric's seven replies. Three
  (Carla Quintana, Victor Ay, Bruno DiDuca) are **not on the live site yet**.
  Google links are the real ones: `g.page/r/CQPibJ1CNvd7EAE`.

---

## Open items

- **Mobile is untouched by instruction.** Desktop-only so far; the owner wants
  to do mobile deliberately.
- **The Porsche before/after composite** never arrived as a file — it rendered
  in chat but did not land on disk. Exterior uses the matte X5 M pair instead,
  which works better as a real slider anyway.
- **Membership is out of this build entirely** — nav, FAQ and footer.
  `membership.html` still exists and is still a real offering.
- **Add-ons page** is not part of this build; add-ons appear as chips only.
- **No decision yet on how this replaces the live homepage.** Options: move
  `index.html` to the root, or point the domain at `/preview`. Either
  way the root-absolute `/preview/...` links need rewriting.

---

## The matte X5 M images

`images/gallery/bmw-x5m-matte-{before,after}.webp`, 1200×900 each. No image
tooling exists in the sandbox — no ffmpeg, ImageMagick or PIL — so these were
produced through headless Chromium: canvas scanned each row for near-black to
find the letterbox bars on the source (106px top, 56px bottom), cropped them,
cover-fitted both to a common 1200×900, and exported WebP at q0.86. With the
bars removed the two sources measure 1206×874 and 1206×875, which is why the
wipe lands cleanly rather than making the car jump.

The same Chromium-as-image-processor trick is available for any future
conversion.
