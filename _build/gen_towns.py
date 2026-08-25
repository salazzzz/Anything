"""Service-area landing pages — one per town, generated from towndata.py.

Why these exist: our only geographic page was the homepage, which targets Newton.
Every competitor ranking for "detailing Waltham" / "detailing Watertown" has a
dedicated page per town; we had none, so there was literally nothing of ours for
Google to rank on those queries.

URL shape is /mobile-car-detailing-<slug>-ma, which is the pattern the pages
already ranking for these queries use.

These pages reuse styles.css + tpl.css and add no CSS of their own — every class
below already exists in tpl.css. Check before inventing one; see the .faq-shell
collision noted in HANDOFF.md for what happens when you do not.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo
import shell
from towndata import BASE, TOWNS
from gen_services import SERVICES     # prices come from one place, never retyped

ARROW = ('<svg class="arw" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
         '<path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" stroke="currentColor" stroke-width="1.9" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')

# The three written reviews we quote on town pages. Real text, real names.
QUOTES = [
    ("Chris Fremont",
     "Got the full interior and exterior package done by Eric and team, and im "
     "impressed, the car looks better than the day I got it."),
    ("David Atsiliem",
     "He came fully prepared with all equipment and clearly takes pride in his work. "
     "The results were impressive, my car looked showroom inside and out."),
    ("Jean DeBenedictis",
     "Eric and team did a fantastic job on my car. It truly never looked so good. "
     "Every detail, inside and out, shines to perfection."),
]


def miles(a, b):
    """Great-circle miles between two (lat, lon) pairs."""
    r = 3958.7613
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def path_for(T):
    return "/mobile-car-detailing-%s-ma" % T["slug"]


def schema_for(T):
    """LocalBusiness + a Service scoped to THIS town + the town's own FAQ.

    areaServed is deliberately just this one town rather than the full 12-town
    list used site-wide: the whole point of the page is to be unambiguously about
    one place. The offers carry Basic and Deep Clean/Premium for all three
    services so the pricing here can never disagree with the service pages.
    """
    offers = []
    for key in ("interior", "exterior", "bundle"):
        S = SERVICES[key]
        for tier, label in (("basic", "Basic"), ("premium", "Deep Clean")):
            price = S[tier]["sizes"]["sedan"][0]
            offers.append(seo.offer(
                "%s in %s — %s" % (S["name"], T["town"], label),
                price, S["path"],
                alt_name=("%s in %s — Premium" % (S["name"], T["town"])
                          if tier == "premium" else None)))

    svc = {"@type": "Service",
           "@id": seo.url(path_for(T)) + "#service",
           "name": "Mobile Car Detailing in %s" % T["full"],
           "description": T["desc"],
           "serviceType": "Car detailing",
           "provider": {"@id": seo.ID_BIZ},
           "areaServed": {"@type": "City", "name": T["town"],
                          "address": {"@type": "PostalAddress",
                                      "addressLocality": T["town"],
                                      "addressRegion": "MA",
                                      "addressCountry": "US"}},
           "hasOfferCatalog": {"@type": "OfferCatalog",
                               "name": "Detailing packages in %s" % T["town"],
                               "itemListElement": offers}}

    return seo.ld(
        seo.business(),
        seo.website(),
        seo.webpage(path_for(T), T["title"], T["desc"],
                    primary_image=T["image"][0]),
        seo.breadcrumb([("Home", "/"), (T["town"], path_for(T))]),
        svc,
        seo.faq(T["faq"]),
        *seo.reviews(QUOTES))


def travel_line(T):
    """One honest sentence about distance. The base town gets a different one."""
    if T.get("home"):
        return ("<p>This is our home base, so there is no travel time, no travel "
                "charge and no minimum job size.</p>")
    d = miles(BASE, T["coord"])
    return ('<p>%s is about <strong>%.1f miles</strong> from our base in West Newton '
            '&mdash; well inside the 10 mile radius we serve, so there is no travel '
            'surcharge.</p>' % (T["town"], d))


def services_grid(T):
    cards = []
    for key in ("interior", "exterior", "bundle"):
        S = SERVICES[key]
        basic = S["basic"]["sizes"]["sedan"][0]
        deep = S["premium"]["sizes"]["sedan"][0]
        cards.append(
            '<a class="ao" href="%s">'
            '<span class="ao-top"><span class="ao-name">%s</span>'
            '<span class="ao-price">from $%d</span></span>'
            '<span class="ao-note">Basic $%d &middot; Deep Clean $%d &mdash; sedan pricing, '
            'in %s</span></a>'
            % (S["path"], S["name"], basic, basic, deep, T["town"]))
    return '<div class="ao-grid">%s</div>' % "".join(cards)


def spots_grid(T):
    """Neighbourhood names. Deliberately NOT links — they are labels, and an
    earlier version made each one a tel: link, which meant tapping a place name
    tried to dial Eric."""
    return '<div class="ao-grid">%s</div>' % "".join(
        '<div class="ao"><span class="ao-top">'
        '<span class="ao-name">%s</span></span></div>' % s
        for s in T["spots"])


def quotes_grid():
    return '<div class="ao-grid">%s</div>' % "".join(
        '<div class="ao"><span class="ao-note">&ldquo;%s&rdquo;</span>'
        '<span class="ao-top"><span class="ao-name">%s</span>'
        '<span class="ao-price">&#9733;&#9733;&#9733;&#9733;&#9733;</span></span></div>'
        % (text, name) for name, text in QUOTES)


def faq_list(T):
    return "".join(
        '<div class="ao"><span class="ao-top"><span class="ao-name">%s</span></span>'
        '<span class="ao-note">%s</span></div>' % (q, a) for q, a in T["faq"])


def others_grid(T):
    other = [x for x in TOWNS if x["slug"] != T["slug"]]
    return '<div class="xsell">%s</div>' % "".join(
        '<a class="xs" href="%s"><span class="xs-name">%s</span>'
        '<span class="xs-price">see page &rarr;</span></a>'
        % (path_for(o), o["town"]) for o in other)


def build(T):
    return """<!DOCTYPE html>
<html lang="en">
<head>
%(head)s
%(schema)s
</head>
<body>

%(skip)s
%(header)s

<main id="main-content">

<section class="hero-a">
  <div class="container hero-a-in">
    <div>
      <span class="sec-rule" aria-hidden="true"></span>
      <h1>Mobile Car Detailing in %(full)s</h1>
      <div class="pitch">
        <p>%(lede)s</p>
        %(travel)s
        <p class="pitch-kicker">We come to you. You pay after you have seen the car.</p>
      </div>
      <div class="xsell">
        <a class="cta" href="tel:%(tel)s"><span>Call Eric</span>%(arrow)s</a>
        <a class="cta-ghost" href="/#services"><span>Packages &amp; prices</span></a>
      </div>
    </div>
    <img class="hero-a-shot" src="%(img)s" alt="%(img_alt)s"
         width="%(img_w)d" height="%(img_h)d" decoding="async">
  </div>
</section>

%(trust)s

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Detailing in %(town)s, specifically.</h2>
    <div class="pitch">
      %(local)s
    </div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Where we work in %(town)s.</h2>
    <div class="pitch"><p>%(parking)s</p></div>
    %(spots)s
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">What you can book in %(town)s.</h2>
    %(services)s
    <p class="ao-more">Every package is priced by vehicle size and comes in Basic or
      Deep Clean. <a href="/addons">Add-ons</a> can go on any of them, and a
      <a href="/membership">membership</a> works out cheaper if you book more than once.</p>
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">What people say.</h2>
    %(quotes)s
    <p class="ao-more">5.0 stars across %(rc)d Google reviews.
      <a href="/reviews">Read them all &rarr;</a></p>
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Questions from %(town)s.</h2>
    <div class="ao-grid">%(faq)s</div>
  </div>
</section>

<section class="sec sec-last">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Not in %(town)s?</h2>
    <p class="lede">We cover everything within 10 miles of Newton. These are the
      other areas with a page of their own.</p>
    %(others)s
    <p class="foot-note">Anywhere else inside the radius, just
      <a href="tel:%(tel)s">call Eric</a> and ask.</p>
  </div>
</section>

</main>

%(footer)s

<script src="/script.js" defer></script>
</body>
</html>
""" % dict(
        head=seo.head(T["title"], T["desc"], path_for(T),
                      css=("/styles.css", "/tpl.css")),
        schema=schema_for(T),
        skip=shell.SKIP, header=shell.header(), footer=shell.footer(),
        trust=shell.TRUST,
        full=T["full"], town=T["town"], lede=T["lede"],
        travel=travel_line(T),
        local="\n      ".join("<p>%s</p>" % p for p in T["local"]),
        spots=spots_grid(T), parking=T["parking"],
        services=services_grid(T), quotes=quotes_grid(),
        faq=faq_list(T), others=others_grid(T),
        rc=seo.BIZ["review_count"],
        img=T["image"][0], img_w=T["image"][1], img_h=T["image"][2],
        img_alt=T["image"][3],
        tel=shell.TEL, tel_txt=shell.TEL_TXT, arrow=ARROW)


def outfile(T):
    return "mobile-car-detailing-%s-ma.html" % T["slug"]


if __name__ == "__main__":
    for T in TOWNS:
        open(outfile(T), "w", encoding="utf-8").write(build(T))
        d = 0.0 if T.get("home") else miles(BASE, T["coord"])
        print("wrote %-40s %-14s %4.1f mi  %d spots  %d faq"
              % (outfile(T), T["town"], d, len(T["spots"]), len(T["faq"])))
