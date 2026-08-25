"""Shared page shell: skip link, header, footer.

The generated pages used to ship a bottom bar only — no contact details, no
socials, and no links to gallery, reviews, add-ons or membership. Those pages
were reachable from two homepage buttons and nothing else, which is a dead end
for a visitor and a dead end for a crawler. The footer here is the internal
link graph for the whole site.

Header stays at three items by instruction. Everything else lives in the footer.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo

TEL = "+17812903040"
TEL_TXT = "+1 781-290-3040"

SKIP = '<a class="skip-link" href="#main-content">Skip to content</a>'


def header(home=False):
    h = "/" if not home else "#top"
    return """<header class="site-header" id="top">
  <div class="container header-inner">
    <a href="%(brand_href)s" class="brand">
      <img src="/images/logo.webp" alt="Euro Detailing logo" class="logo-image" width="72" height="72" decoding="async">
      <span class="brand-text">
        <span class="brand-name">Euro Detailing</span>
        <span class="brand-subtitle">Mobile car detailing in Newton, MA</span>
      </span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      <a href="%(p)s#services">Services</a>
      <a href="/membership">Membership</a>
      <a href="/addons">Add-ons</a>
      <a href="%(p)s#faq">FAQ</a>
      <a href="%(p)s#contact">Contact</a>
    </nav>
    <div class="header-actions">
      <a href="tel:%(tel)s" class="cta"><span>Call Eric</span></a>
    </div>
  </div>
</header>""" % dict(brand_href=h, p="" if home else "/", tel=TEL)


def footer(home=False):
    p = "" if home else "/"
    return """<footer class="ft">
  <div class="container ft-inner">

    <div class="ft-brand">
      <a class="ft-mark" href="%(top)s">
        <img src="/images/logo.webp" alt="" width="40" height="40" loading="lazy" decoding="async">
        <span>Euro Detailing</span>
      </a>
      <p class="ft-note">Mobile car detailing in Newton, MA 02465 &mdash; we come to you.</p>
      <p class="ft-area">Serving <a href="/mobile-car-detailing-west-newton-ma">West Newton</a>, the rest of Newton, <a href="/mobile-car-detailing-waltham-ma">Waltham</a>, <a href="/mobile-car-detailing-watertown-ma">Watertown</a>, Brighton, Weston, Belmont, Needham, Wellesley, Allston, Brookline, Dedham and Boston.</p>
    </div>

    <nav class="ft-col" aria-label="Services">
      <span class="ft-head">Services</span>
      <a href="/services/interior">Interior Detailing</a>
      <a href="/services/exterior">Exterior Detailing</a>
      <a href="/services/bundle">Interior + Exterior</a>
      <a href="/addons">Add-ons</a>
      <a href="/membership">Membership</a>
    </nav>

    <nav class="ft-col" aria-label="Explore">
      <span class="ft-head">Explore</span>
      <a href="/gallery">Gallery</a>
      <a href="/reviews">Reviews</a>
      <a href="%(p)s#faq">FAQ</a>
      <a href="%(p)s#contact">Contact</a>
    </nav>

    <div class="ft-col">
      <span class="ft-head">Get in touch</span>
      <a href="tel:%(tel)s">%(tel_txt)s</a>
      <a href="#" class="js-email" data-e="eurodetailinginfo" data-d="gmail.com">Email Us</a>
      <span class="ft-hours">Mon&ndash;Sun, 8am&ndash;8pm</span>
      <div class="ft-social">
        <a href="https://www.instagram.com/euro_detailingg" target="_blank" rel="noopener noreferrer" aria-label="Euro Detailing on Instagram">
          <img src="/images/instagram.webp" alt="" width="22" height="22" loading="lazy" decoding="async">
        </a>
        <a href="https://www.tiktok.com/@eurodetailing" target="_blank" rel="noopener noreferrer" aria-label="Euro Detailing on TikTok">
          <img src="/images/tiktok.webp" alt="" width="22" height="22" loading="lazy" decoding="async">
        </a>
      </div>
    </div>

  </div>

  <div class="container ft-bottom">
    <p>&copy; <span id="footer-year">2026</span> Euro Detailing. All rights reserved.</p>
    <p class="ft-by">Owner-operated by Eric Salas</p>
  </div>
</footer>""" % dict(top="#top" if home else "/", p=p, tel=TEL, tel_txt=TEL_TXT)


TRUST = """<div class="trust-strip">
  <div class="container">
    <span class="g-logo" aria-hidden="true"></span>
    <b>5.0</b><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
    <span>%d Google reviews</span><span class="dot"></span>
    <span>We come to you</span><span class="dot"></span>
    <span>Pay after the job</span>
  </div>
</div>""" % seo.BIZ["review_count"]
