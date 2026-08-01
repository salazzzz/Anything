"""Add-ons page.

The redesign shipped no add-ons page at all, and the seven add-ons appeared on
service pages as flat, unclickable text chips. Cards here are deliberately
small — the job is to let someone read the whole menu in one glance, not to
sell one item hard.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo, shell
from addondata import ADDONS

PATH = "/addons"
TITLE = "Detailing Add-ons Newton MA — Pet Hair, Clay Bar, Wax"
DESC = ("Pet hair removal, seat extraction, engine bay, mold removal, clay bar and waxing. Add any to an interior, exterior or full detail in Newton, MA. From $25.")

ARROW = '<svg class="arw" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'

XSELL = [("Interior Detailing", "/services/interior", 105),
         ("Exterior Detailing", "/services/exterior", 70),
         ("Interior + Exterior", "/services/bundle", 150)]


def cards():
    return "".join(
        '<article class="ao" id="%s">'
        '<span class="ao-top"><span class="ao-name">%s</span>'
        '<span class="ao-price">%s</span></span>'
        '<p class="ao-note">%s</p></article>'
        % (slug, name, price, note)
        for slug, name, price, _p, note in ADDONS)


def schema():
    offers = [seo.offer(name, price, PATH, desc=note)
              for _s, name, _pl, price, note in ADDONS]
    return seo.ld(
        seo.business(),
        seo.website(),
        seo.webpage(PATH, TITLE, DESC),
        seo.breadcrumb([("Home", "/"), ("Add-ons", PATH)]),
        seo.service("Car detailing add-ons", DESC, PATH, offers,
                    service_type="Car detailing add-on"))


PAGE = """<!DOCTYPE html>
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
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h1>Add-ons</h1>
    <p class="lede">Seven extras that go on top of any package. Add them when you book,
    or mention them when Eric arrives &mdash; nothing here needs a separate appointment.</p>
  </div>
</section>

%(trust)s

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">The full menu.</h2>
    <div class="ao-grid">%(cards)s</div>
    <p class="foot-note">Prices marked <strong>+</strong> depend on how bad it is.
    <a href="tel:+17812903040">Call Eric</a> and describe it, or send a photo.</p>
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Put them on a package.</h2>
    <p class="lede">Add-ons are cheapest alongside a detail, because the car is already
    stripped, lifted and open. Booked on their own they take a separate trip.</p>
    <div class="xsell">%(xsell)s</div>
  </div>
</section>

<section class="sec sec-last">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Getting it done regularly?</h2>
    <p class="lede">Members get every add-on at a standing discount, and the car
    never gets bad enough to need the expensive ones.</p>
    <p class="foot-note"><a href="/membership">See membership plans &rarr;</a></p>
  </div>
</section>
</main>

%(footer)s

<script src="/script.js" defer></script>
</body>
</html>
"""


def build():
    return PAGE % dict(
        head=seo.head(TITLE, DESC, PATH, css=("/styles.css", "/tpl.css")),
        schema=schema(),
        skip=shell.SKIP, header=shell.header(), footer=shell.footer(), trust=shell.TRUST,
        cards=cards(),
        xsell="".join('<a class="xs" href="%s"><span class="xs-name">%s</span>'
                      '<span class="xs-price">from $%d</span></a>' % (p, n, pr)
                      for n, p, pr in XSELL))


if __name__ == "__main__":
    open("addons.html", "w", encoding="utf-8").write(build())
    print("wrote addons.html  (%d add-ons)" % len(ADDONS))
