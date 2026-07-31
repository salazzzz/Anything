"""Shared SEO: head metadata and JSON-LD for every page.

One source of truth for the business facts. Every generator imports from here so
the schema can never drift page to page — mixed signals are what dilute ranking.

Canonical host is www. The old JSON-LD used the bare domain while the canonical
tags and sitemap used www; that inconsistency is fixed here.
"""

import json

ORIGIN = "https://www.eurodetailing.com"

BIZ = dict(
    name="Euro Detailing",
    legal="Euro Detailing",
    owner="Eric Salas",
    tel="+1-781-290-3040",
    tel_href="+17812903040",
    email="eurodetailinginfo@gmail.com",
    locality="Newton",
    region="MA",
    postal="02465",
    country="US",
    lat=42.3487,
    lon=-71.2276,
    radius_mi=10,
    price_range="$$",
    rating="5.0",
    review_count=10,
    social=["https://www.instagram.com/euro_detailingg",
            "https://www.tiktok.com/@eurodetailing"],
    google_review="https://g.page/r/CQPibJ1CNvd7EAE",
)

# Every town inside the 10 mile radius, verified by haversine from the centre
# coordinate above. Boston is 8.6 mi out, so it stays; Waltham, Weston and
# Dedham are inside too and were missing from the old schema.
AREA = ["Newton", "Waltham", "Watertown", "Brighton", "Weston", "Belmont",
        "Needham", "Wellesley", "Allston", "Brookline", "Dedham", "Boston"]

OG_IMAGE = "/images/og-euro-detailing.webp"
LOGO = "/images/logo.webp"

ID_BIZ = ORIGIN + "/#business"
ID_SITE = ORIGIN + "/#website"


def url(path):
    """'/gallery' -> absolute canonical. '/' -> origin + '/'."""
    if not path.startswith("/"):
        path = "/" + path
    return ORIGIN + path


def head(title, desc, path, og_image=OG_IMAGE, og_type="website", css=("/styles.css",)):
    """The full <head> block: title, description, canonical, OG, Twitter, geo."""
    canon = url(path)
    sheets = "\n".join('<link rel="stylesheet" href="%s">' % c for c in css)
    return """<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>if(window.matchMedia&&!matchMedia("(prefers-reduced-motion: reduce)").matches){document.documentElement.classList.add("js-anim")}</script>

<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canon)s">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="%(owner)s">

<meta property="og:type" content="%(og_type)s">
<meta property="og:site_name" content="%(name)s">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canon)s">
<meta property="og:image" content="%(origin)s%(og_image)s">
<meta property="og:image:alt" content="%(name)s — mobile car detailing in Newton, MA">
<meta property="og:locale" content="en_US">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(origin)s%(og_image)s">

<meta name="geo.region" content="US-MA">
<meta name="geo.placename" content="Newton, Massachusetts">
<meta name="geo.position" content="%(lat)s;%(lon)s">
<meta name="ICBM" content="%(lat)s, %(lon)s">

<link rel="icon" type="image/png" href="/images/favicon.png">
<link rel="apple-touch-icon" href="/images/favicon.png">
%(sheets)s""" % dict(
        title=title, desc=desc, canon=canon, og_type=og_type, og_image=og_image,
        origin=ORIGIN, name=BIZ["name"], owner=BIZ["owner"],
        lat=BIZ["lat"], lon=BIZ["lon"], sheets=sheets)


def ld(*nodes):
    """Wrap nodes in one @graph script tag. One block per page, not five."""
    graph = [n for n in nodes if n]
    return ('<script type="application/ld+json">\n%s\n</script>'
            % json.dumps({"@context": "https://schema.org", "@graph": graph},
                         indent=None, ensure_ascii=False, separators=(",", ":")))


def business(with_rating=True):
    """The LocalBusiness node. Referenced by @id from every other node."""
    n = {
        "@type": ["LocalBusiness", "AutomotiveBusiness"],
        "@id": ID_BIZ,
        "name": BIZ["name"],
        "description": ("Owner-operated mobile car detailing in Newton, Massachusetts. "
                        "Interior, exterior and full detailing packages, done at your home "
                        "or workplace within %d miles of Newton." % BIZ["radius_mi"]),
        "url": ORIGIN + "/",
        "telephone": BIZ["tel"],
        "email": BIZ["email"],
        "priceRange": BIZ["price_range"],
        "currenciesAccepted": "USD",
        "paymentAccepted": "Cash, Venmo, Zelle, Credit Card",
        "image": [ORIGIN + LOGO, ORIGIN + OG_IMAGE],
        "logo": {"@type": "ImageObject", "url": ORIGIN + LOGO},
        "founder": {"@type": "Person", "name": BIZ["owner"]},
        "address": {"@type": "PostalAddress", "addressLocality": BIZ["locality"],
                    "addressRegion": BIZ["region"], "postalCode": BIZ["postal"],
                    "addressCountry": BIZ["country"]},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lon"]},
        "areaServed": [{"@type": "City", "name": c} for c in AREA],
        "serviceArea": {"@type": "GeoCircle",
                        "geoMidpoint": {"@type": "GeoCoordinates",
                                        "latitude": BIZ["lat"], "longitude": BIZ["lon"]},
                        "geoRadius": str(int(BIZ["radius_mi"] * 1609.34))},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday",
                          "Friday", "Saturday", "Sunday"],
            "opens": "08:00", "closes": "20:00"}],
        "contactPoint": {"@type": "ContactPoint", "telephone": BIZ["tel"],
                         "contactType": "customer service",
                         "areaServed": "US", "availableLanguage": ["English", "Spanish"]},
        "sameAs": BIZ["social"],
    }
    if with_rating:
        n["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": BIZ["rating"],
                                "reviewCount": str(BIZ["review_count"]),
                                "bestRating": "5", "worstRating": "1"}
    return n


def website():
    return {"@type": "WebSite", "@id": ID_SITE, "url": ORIGIN + "/",
            "name": BIZ["name"], "publisher": {"@id": ID_BIZ},
            "inLanguage": "en-US"}


def webpage(path, title, desc, primary_image=None):
    n = {"@type": "WebPage", "@id": url(path) + "#webpage", "url": url(path),
         "name": title, "description": desc,
         "isPartOf": {"@id": ID_SITE}, "about": {"@id": ID_BIZ},
         "inLanguage": "en-US"}
    if primary_image:
        n["primaryImageOfPage"] = {"@type": "ImageObject", "url": ORIGIN + primary_image}
    return n


def breadcrumb(trail):
    """trail: [(name, path), ...] starting at Home."""
    return {"@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": nm, "item": url(p)}
                for i, (nm, p) in enumerate(trail)]}


def offer(name, price, path, desc=None, unit=None):
    o = {"@type": "Offer", "name": name, "price": "%.2f" % price,
         "priceCurrency": "USD", "availability": "https://schema.org/InStock",
         "url": url(path), "seller": {"@id": ID_BIZ}}
    if desc:
        o["description"] = desc
    if unit:
        o["priceSpecification"] = {"@type": "UnitPriceSpecification",
                                   "price": "%.2f" % price, "priceCurrency": "USD",
                                   "referenceQuantity": unit}
    return o


def service(name, desc, path, offers, service_type="Car detailing"):
    return {"@type": "Service", "@id": url(path) + "#service", "name": name,
            "description": desc, "serviceType": service_type,
            "provider": {"@id": ID_BIZ},
            "areaServed": [{"@type": "City", "name": c} for c in AREA],
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": name, "itemListElement": offers}}


def faq(pairs):
    return {"@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in pairs]}


def reviews(items, limit=None):
    """items: [(author, text), ...] — only reviews with real text."""
    out = []
    for author, text in (items[:limit] if limit else items):
        if not text:
            continue
        out.append({"@type": "Review", "itemReviewed": {"@id": ID_BIZ},
                    "author": {"@type": "Person", "name": author},
                    "reviewRating": {"@type": "Rating", "ratingValue": "5",
                                     "bestRating": "5", "worstRating": "1"},
                    "reviewBody": text})
    return out
