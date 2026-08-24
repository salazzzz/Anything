"""sitemap.xml + llms.txt, generated so they can never drift from the real pages.

The old sitemap listed /testimonials (now a 301 to /reviews) and omitted the
membership and add-ons work entirely. Listing a URL that redirects wastes crawl
budget and muddies the signal, so redirect targets are listed, never sources.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo
from addondata import ADDONS

LASTMOD = "2026-07-30"

PAGES = [
    ("/",                   "weekly",  "1.0"),
    ("/services/interior",  "monthly", "0.9"),
    ("/services/exterior",  "monthly", "0.9"),
    ("/services/bundle",    "monthly", "0.9"),
    ("/membership",         "monthly", "0.9"),
    ("/addons",             "monthly", "0.8"),
    ("/gallery",            "monthly", "0.8"),
    ("/reviews",            "monthly", "0.8"),
]


def sitemap():
    urls = "".join(
        "  <url>\n"
        "    <loc>%s</loc>\n"
        "    <lastmod>%s</lastmod>\n"
        "    <changefreq>%s</changefreq>\n"
        "    <priority>%s</priority>\n"
        "  </url>\n" % (seo.url(p), LASTMOD, freq, pri)
        for p, freq, pri in PAGES)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            '%s</urlset>\n' % urls)


def llms():
    addons = "\n".join("- %s — %s. %s" % (name, price, note)
                       for _s, name, price, _p, note in ADDONS)
    return """# Euro Detailing

> Owner-operated mobile car detailing in Newton, Massachusetts. Eric Salas comes
> to you anywhere within %(radius)d miles of Newton. 5.0 stars across %(reviews)d Google reviews.

Contact: %(tel)s · %(email)s
Hours: Mon-Sun, 8am-8pm
Service area: %(area)s

## Services

Every service is priced by vehicle size (Sedan / SUV / Truck-XL) and comes in two
levels: Basic, for a car that is kept up, and Deep Clean — also called Premium —
for one that is not. Deep Clean/Premium always costs more than Basic; it is never
the same price. Prices below are for a Sedan; SUV and Truck/XL cost more. Full
per-size pricing is on each service page.

- Interior Detailing (%(interior)s) — Basic from $105, Deep Clean/Premium
  from $165. Steam clean, stain removal, leather conditioning, odor treatment.
- Exterior Detailing (%(exterior)s) — Basic from $70, Deep Clean/Premium
  from $105. Foam bath hand wash, clay bar decontamination, up to six months of sealant.
- Interior + Exterior (%(bundle)s) — Basic from $150, Deep Clean/Premium
  from $230. Both in a single visit, cheaper than booking them separately.

## Membership

Recurring detailing at a lower per-visit rate (%(membership)s). Three cadences:
every 2 weeks (from $209/month, 2 visits), monthly (from $119/month), and every
3 months (from $135/visit). No contract, cancel any time. Members get a standing
discount on every add-on.

## Add-ons

Any of these can be added to any package (%(addons)s):

%(addon_list)s

## Other pages

- Gallery (%(gallery)s) — real before/after photos and video from local jobs.
- Reviews (%(reviews_url)s) — all %(reviews)d Google reviews in full.

Booking is through Cal.com links on each service page, or by phone/text to %(tel)s.
""" % dict(
        radius=seo.BIZ["radius_mi"], reviews=seo.BIZ["review_count"],
        tel=seo.BIZ["tel"], email=seo.BIZ["email"], area=", ".join(seo.AREA),
        interior=seo.url("/services/interior"), exterior=seo.url("/services/exterior"),
        bundle=seo.url("/services/bundle"), membership=seo.url("/membership"),
        addons=seo.url("/addons"), gallery=seo.url("/gallery"),
        reviews_url=seo.url("/reviews"), addon_list=addons)


def robots():
    return """User-agent: *
Allow: /

# The retired design and the old preview build both 301 to the live pages.
Disallow: /project/

Sitemap: %s/sitemap.xml

# LLM crawlers
User-agent: GPTBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /
""" % seo.ORIGIN


if __name__ == "__main__":
    open("sitemap.xml", "w", encoding="utf-8").write(sitemap())
    open("llms.txt", "w", encoding="utf-8").write(llms())
    open("robots.txt", "w", encoding="utf-8").write(robots())
    print("wrote sitemap.xml (%d urls), llms.txt, robots.txt" % len(PAGES))
