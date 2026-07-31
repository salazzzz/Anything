# Build scripts for /preview

These generate the pages under `preview/`. They were living in `/tmp` during
the first session, which is wiped when the container is reclaimed — they are
committed here so the work survives.

Run them from the **repo root**, not from this directory:

    python3 preview/_build/gen_services.py    # service-interior/exterior/bundle.html
    python3 preview/_build/gen_gallery.py     # gallery.html   (reads data/gallery.json)
    python3 preview/_build/gen_reviews.py     # reviews.html
    python3 preview/_build/vercelish.py       # local server on :8902 emulating cleanUrls

`preview/index.html` is hand-written, not generated.

## Why a local server matters

`vercel.json` sets `cleanUrls: true` with `trailingSlash: false`, so
`preview/index.html` is served at `/preview` with **no trailing slash**. A plain
`python3 -m http.server` does not emulate that, and relative links behave
differently under it than in production. `vercelish.py` resolves `/x` from
`x.html` and `/dir` from `dir/index.html`, which matches Vercel closely enough
to catch link bugs. All in-page links are root-absolute and extensionless
(`/preview/service-interior`) for the same reason.

## Hard-coded numbers worth knowing

`gen_reviews.py` holds `MEASURED`, the rendered pixel height of each review
card at real column width, taken from Chromium. The three-column balance and
the CTA's vertical placement are solved from those numbers. **Editing review
text changes the heights and the layout will drift** — re-measure with:

    document.querySelectorAll('.rv').forEach(c => console.log(
      c.querySelector('.rv-name').textContent.trim(),
      Math.round(c.getBoundingClientRect().height)))
