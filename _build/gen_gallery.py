import json, html as H, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo, shell

PATH = "/gallery"
TITLE = "Before &amp; After Detailing Photos — Newton, MA"
DESC = ("Real before and after photos and video from mobile detailing jobs around "
        "Newton, MA — interiors, paint correction and wheels, all by Eric Salas.")

d = json.load(open("data/gallery.json"))
items = [i for i in d["items"] if i.get("src")]


def schema():
    """ImageGallery with every tile, plus VideoObject for the clips."""
    imgs, vids = [], []
    for i in items:
        node = {"@type": "ImageObject", "contentUrl": seo.ORIGIN + "/" + i["src"],
                "url": seo.ORIGIN + "/" + i["src"], "caption": i["alt"],
                "width": i.get("w"), "height": i.get("h")}
        imgs.append(node)
        if i.get("video"):
            vids.append({"@type": "VideoObject", "name": i["alt"],
                         "description": i["alt"],
                         "thumbnailUrl": seo.ORIGIN + "/" + i["src"],
                         "contentUrl": seo.ORIGIN + "/" + i["video"],
                         "uploadDate": d.get("uploadDate", "2026-01-01"),
                         "duration": i.get("duration"),
                         "publisher": {"@id": seo.ID_BIZ}})
    gallery = {"@type": "ImageGallery", "@id": seo.url(PATH) + "#gallery",
               "name": "Euro Detailing before and after gallery",
               "description": DESC, "url": seo.url(PATH),
               "associatedMedia": imgs}
    return seo.ld(seo.business(), seo.website(),
                  seo.webpage(PATH, TITLE.replace("&amp;", "&"), DESC),
                  seo.breadcrumb([("Home", "/"), ("Gallery", PATH)]),
                  gallery, *vids)

def iso_to_secs(s):
    m = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", s or "")
    if not m: return None
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)

cats = ["interior", "exterior", "wheels"]
counts = {c: sum(1 for i in items if i.get("category") == c) for c in cats}

chips = '<button type="button" class="fchip is-on" data-cat="all">All <i>%d</i></button>' % len(items)
chips += "".join('<button type="button" class="fchip" data-cat="%s">%s <i>%d</i></button>'
                 % (c, c.capitalize(), counts[c]) for c in cats if counts[c])

tiles = []
for n, it in enumerate(items):
    vid = it.get("video")
    secs = iso_to_secs(it.get("duration"))
    badge = ('<span class="tile-vid">'
             '<svg width="9" height="11" viewBox="0 0 17 19" fill="none" aria-hidden="true">'
             '<path d="M2 1.7v15.6a1 1 0 0 0 1.53.85l12.5-7.8a1 1 0 0 0 0-1.7L3.53.85A1 1 0 0 0 2 1.7Z" fill="currentColor"/></svg>'
             '%s</span>') % ("0:%02d" % secs if secs is not None else "Video") if vid else ""
    tiles.append(
      '<button type="button" class="tile" data-i="%d" data-cat="%s"%s aria-label="%s">'
      '<img src="/%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">%s</button>'
      % (n, it.get("category", ""), ' data-video="/%s"' % vid if vid else "",
         H.escape(it["alt"], True), it["src"], H.escape(it["alt"], True), it["w"], it["h"], badge))

DATA = json.dumps([{"src": "/" + i["src"], "alt": i["alt"],
                    "video": ("/" + i["video"]) if i.get("video") else None,
                    "cat": i.get("category", "")} for i in items], separators=(",", ":"))

html = """<!DOCTYPE html>
<html lang="en">
<head>
%(head)s
%(schema)s
</head>
<body>

%(skip)s
%(header)s

<main id="main-content">
<section class="gal-head">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h1>The work</h1>
    <p class="lede">Every car on this page is one we detailed in Newton or nearby. No stock photography.</p>
    <div class="filters" role="group" aria-label="Filter the gallery">%(chips)s</div>
  </div>
</section>

<section class="gal-body">
  <div class="container">
    <div class="grid" id="grid">%(tiles)s</div>
    <p class="gal-empty" id="empty" hidden>Nothing in that category yet.</p>
  </div>
</section>

<section class="sec sec-last">
  <div class="container gal-cta">
    <div>
      <span class="sec-rule" aria-hidden="true"></span>
      <h2 class="sec-h">Want yours in here?</h2>
      <p class="lede">Pick a package and we'll come to you.</p>
    </div>
    <div class="gal-cta-btns">
      <a href="/#services" class="cta"><span>View services</span>
        <svg class="arw" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
      <a href="tel:+17812903040" class="cta-ghost"><span>Call Eric</span></a>
    </div>
  </div>
</section>
</main>

<div class="lb" id="lb" hidden>
  <button type="button" class="lb-x" id="lbX" aria-label="Close">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="m1 1 12 12M13 1 1 13" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
  </button>
  <button type="button" class="lb-nav lb-prev" id="lbPrev" aria-label="Previous">
    <svg width="17" height="17" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13 8H4M7.5 3.5 4 8l3.5 4.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
  <button type="button" class="lb-nav lb-next" id="lbNext" aria-label="Next">
    <svg width="17" height="17" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h9M8.5 3.5 12 8l-3.5 4.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>
  <figure class="lb-stage" id="lbStage"></figure>
  <figcaption class="lb-cap"><span id="lbAlt"></span><span class="lb-count" id="lbCount"></span></figcaption>
</div>

%(footer)s

<script src="/script.js" defer></script>
<script>
var ITEMS = %(data)s;

/* ---------- filter ---------- */
(function () {
  var grid = document.getElementById("grid");
  var empty = document.getElementById("empty");
  var chips = [].slice.call(document.querySelectorAll(".fchip"));
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      var cat = c.dataset.cat;
      chips.forEach(function (x) { x.classList.toggle("is-on", x === c); });
      var shown = 0;
      [].forEach.call(grid.children, function (t) {
        var on = cat === "all" || t.dataset.cat === cat;
        t.hidden = !on;
        if (on) shown++;
      });
      empty.hidden = shown > 0;
    });
  });
})();

/* ---------- lightbox ---------- */
(function () {
  var lb = document.getElementById("lb"), stage = document.getElementById("lbStage"),
      alt = document.getElementById("lbAlt"), count = document.getElementById("lbCount"),
      x = document.getElementById("lbX"), prev = document.getElementById("lbPrev"), next = document.getElementById("lbNext");
  var cur = 0, last = null;

  function visible() {
    return [].filter.call(document.getElementById("grid").children, function (t) { return !t.hidden; })
             .map(function (t) { return +t.dataset.i; });
  }
  var ring = [];

  function show(i) {
    cur = (i + ring.length) %% ring.length;
    var it = ITEMS[ring[cur]];
    stage.innerHTML = it.video
      ? '<video src="' + it.video + '" controls autoplay playsinline preload="metadata"></video>'
      : '<img src="' + it.src + '" alt="' + it.alt.replace(/"/g, "&quot;") + '">';
    alt.textContent = it.alt;
    count.textContent = (cur + 1) + " / " + ring.length;
  }
  function open(i) {
    ring = visible();
    var at = ring.indexOf(i);
    if (at < 0) return;
    last = document.activeElement;
    lb.hidden = false;
    document.body.style.overflow = "hidden";
    show(at);
    x.focus();
  }
  function close() {
    var v = stage.querySelector("video"); if (v) v.pause();
    stage.innerHTML = "";
    lb.hidden = true;
    document.body.style.overflow = "";
    if (last && last.focus) last.focus();
  }

  document.getElementById("grid").addEventListener("click", function (e) {
    var t = e.target.closest(".tile"); if (t) open(+t.dataset.i);
  });
  x.addEventListener("click", close);
  prev.addEventListener("click", function () { show(cur - 1); });
  next.addEventListener("click", function () { show(cur + 1); });
  lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
  document.addEventListener("keydown", function (e) {
    if (lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft")  show(cur - 1);
    if (e.key === "ArrowRight") show(cur + 1);
  });
})();
</script>
</body>
</html>
""" % dict(chips=chips, tiles="".join(tiles), data=DATA,
           head=seo.head(TITLE, DESC, PATH, css=("/styles.css", "/tpl.css", "/gallery.css")),
           schema=schema(), skip=shell.SKIP, header=shell.header(), footer=shell.footer())

open("gallery.html", "w", encoding="utf-8").write(html)
print("wrote gallery.html")
print("wrote gallery.html — %d tiles (%d video), filters: %s" % (
    len(items), sum(1 for i in items if i.get("video")), counts))
