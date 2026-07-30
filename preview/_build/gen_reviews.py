import html as H

G_PROFILE = "https://g.page/r/CQPibJ1CNvd7EAE"
G_WRITE   = "https://g.page/r/CQPibJ1CNvd7EAE/review"

# name, meta, when, is_new, review, owner reply (None if none)
R = [
 ("Carla Quintana","Local Guide · 16 reviews · 8 photos","2 weeks ago",True,
  "Eric was great, I was doubtfull at first given he is in high school but the results spoke for themselves this young man is great at what he does, totally recommend for anyone looking for a detailer.",
  "Thanks for the kind words, I'm glad you were satisfied with the results and gained trust in my work, hope to see you soon 🙏"),
 ("Bruno DiDuca","3 reviews","2 weeks ago",True,
  "Highly recommenced. He did a marvelous job with attention to every detail. I own a dog my truck was a very challenging job. Eric took the time to make sure everything was perfect when the job was complete. Definitely would use them again.",
  "Thanks for the kind words, hope to see you soon 🙏"),
 ("Victor Ay","1 review · 1 photo","2 weeks ago",True,
  "Excellent service, I will definitely hire them again",
  "Thanks for taking the time to write a review, I'm glad you were happy with the service, hope to see you soon 🙏"),
 ("Chris Fremont","2 reviews · 1 photo","2 months ago",False,
  "Got the full interior and exterior package done by Eric and team, and im impressed, the car looks better than the day I got it. The mats came out incredible. I thought they were beyond saving, and Eric proved me wrong. Carpet, seats, dash, everything got real attention. The exterior is smooth and glossy. Eric also walked me through the maintenance plan, honestly a no-brainer if you want to keep the car looking like this.",
  "Thanks Mr. Fremont, those mats were a fun one to bring back. Glad the full interior detail and exterior came out the way you wanted. See you next time in Newton."),
 ("Li Anguo","8 reviews · 2 photos","2 months ago",False,
  "Eric is such a nice guy! Absolutely amazing service. The car looked brand new after the detail — super clean interior, spotless exterior, and great attention to detail. Very professional, friendly, and easy to work with. You can tell they really care about the quality of their work. Highly recommend Eurodetailing if you want your car looking perfect again!",
  "Thanks, that means a lot. Caring about the quality is the whole point, so it's good to hear it showed in both the interior and exterior. Appreciate the recommendation, and your car's welcome back anytime it needs that brand-new look again."),
 ("David Atsiliem","1 review · 2 photos","2 months ago",False,
  "Eric did an excellent job detailing my car. He came fully prepared with all equipment and clearly takes pride in his work. The results were impressive, my car looked showroom inside and out. He also set me up with a maintenance plan, so now it's getting detailed regularly each month, which has been a huge help. Highly recommend his services.",
  "Thanks, appreciate you taking the time. Coming prepared and taking pride in the work is the standard, so it's good to hear it showed. The monthly maintenance plan is the smart play — keeping it showroom all the time beats getting it back from the brink."),
 ("E. Fernando","4 reviews · 2 photos","a month ago",False, None,
  "Thanks for the great review, hope to see you soon"),
 ("Ma Lu","3 reviews · 3 photos","10 months ago",False,
  "Thank you Eurodetailing/Eric and team for your hard work! My car feels like new again! Getting the carpet, mats, and all the interior clean is so important given the amount of time you spend breathing in your car. Thank you so much for your meticulous work. I 100% recommend their services!",
  None),
 ("Jean DeBenedictis","1 review","a year ago",False,
  "Eric and team did a fantastic job on my car. It truly never looked so good. Every detail, inside and out, shines to perfection. They were a pleasure to work with. Highly recommend!",
  None),
 ("Vincent Forsythe","8 reviews · 3 photos","a year ago",False,
  "Eric and his team did a full reset of my MDX and I could not believe the results. They carefully detailed every nook, revived all of my black interior plastics and mats. They were perfectionists. Highly recommend!",
  None),
]

# measured in Chromium at a real column width, not estimated
MEASURED = {"Carla Quintana":337,"Bruno DiDuca":297,"Victor Ay":251,"Chris Fremont":425,
            "Li Anguo":421,"David Atsiliem":421,"E. Fernando":231,"Ma Lu":238,
            "Jean DeBenedictis":216,"Vincent Forsythe":216}
CTA_H = 285

def est(text, reply, name=None):
    return MEASURED.get(name, 260)

cards = []
for name, meta, when, new, text, reply in R:
    body = ('<p class="rv-text">%s</p>' % H.escape(text)) if text else \
           '<p class="rv-text rv-none">Left a 5-star rating on Google, without a written review.</p>'
    rep = ('<div class="rv-reply"><span class="rv-reply-h">Response from Eric</span><p>%s</p></div>' % H.escape(reply)) if reply else ""
    cards.append("""      <article class="rv">
        <div class="rv-top">
          <span class="rv-av" aria-hidden="true">%s</span>
          <span class="rv-who">
            <span class="rv-name">%s</span>
            <span class="rv-meta">%s</span>
          </span>
          <span class="g-logo" aria-label="Review from Google"></span>
        </div>
        <div class="rv-rate">
          <span class="rv-stars" aria-label="Rated 5 out of 5">★★★★★</span>
          <span class="rv-when">%s</span>%s
        </div>
        %s
        %s
      </article>""" % (name.strip()[0].upper(), H.escape(name), H.escape(meta), H.escape(when),
                       ' <span class="rv-new">New</span>' if new else "", body, rep))

CTA = """      <div class="rv-cta">
        <span class="sec-rule" aria-hidden="true"></span>
        <h2>Had your car detailed by us?</h2>
        <p>A review takes a minute and it genuinely helps a one-person shop.</p>
        <a href="%s" target="_blank" rel="noopener noreferrer" class="cta"><span>Write a review</span>
          <svg class="arw" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <a href="/preview#services" class="cta-ghost"><span>Book a detail</span></a>
      </div>""" % G_WRITE

# The middle column holds the CTA, so it gets the four shortest reviews: more
# cards there means finer placement, and with only three the nearest slot was
# 158px off centre.
by_h = sorted(range(len(R)), key=lambda i: est(R[i][4], R[i][5], R[i][0]))
mid_ids = set(by_h[:4])
rest = [i for i in by_h[4:]][::-1]                 # tallest first

cols = [[], sorted(mid_ids), []]
h_out = [0, 0]
for i in rest:                                      # balance the two outer columns
    j = 0 if h_out[0] <= h_out[1] else 1
    cols[0 if j == 0 else 2].append(i)
    h_out[j] += est(R[i][4], R[i][5], R[i][0]) + 16
cols[0] = sorted(cols[0]); cols[2] = sorted(cols[2])

mid = cols[1]
mid_h = [est(R[i][4], R[i][5], R[i][0]) for i in mid]
col_h = sum(mid_h) + 16 * len(mid_h) + CTA_H + 16
grid_h = max(max(h_out), col_h)
best, at = None, 0
for k in range(len(mid) + 1):
    run = sum(h + 16 for h in mid_h[:k])
    d = abs((run + CTA_H / 2) - grid_h / 2)
    if best is None or d < best:
        best, at = d, k
print("  outer columns %s | middle %d + CTA | CTA centred to within %.0fpx" % (h_out, col_h - CTA_H - 16, best))

mid_html = [cards[i] for i in mid]
mid_html.insert(at, CTA)

COLUMNS = "".join(
    '<div class="rv-col">%s</div>' % "\n".join(cards[i] for i in cols[0]) if False else "", )
COLUMNS = ('<div class="rv-col">%s</div><div class="rv-col">%s</div><div class="rv-col">%s</div>'
           % ("\n".join(cards[i] for i in cols[0]),
              "\n".join(mid_html),
              "\n".join(cards[i] for i in cols[2])))
print("  CTA sits at position %d of %d in the middle column" % (at, len(mid)))

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>if(window.matchMedia&&!matchMedia("(prefers-reduced-motion: reduce)").matches){document.documentElement.classList.add("js-anim")}</script>
<title>Reviews — Euro Detailing</title>
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="../styles.css">
<link rel="stylesheet" href="tpl.css">
<link rel="stylesheet" href="reviews.css">
</head>
<body>

<header class="site-header" id="top">
  <div class="container header-inner">
    <a href="/preview" class="brand">
      <img src="../images/logo.webp" alt="Euro Detailing logo" class="logo-image" width="72" height="72" decoding="async">
      <span class="brand-text">
        <span class="brand-name">Euro Detailing</span>
        <span class="brand-subtitle">Mobile car detailing in Newton, MA</span>
      </span>
    </a>
    <nav class="site-nav" aria-label="Primary">
      <a href="/preview#services">Services</a>
      <a href="/preview#faq">FAQ</a>
      <a href="/preview#contact">Contact</a>
    </nav>
    <div class="header-actions">
      <a href="tel:+17812903040" class="cta"><span>Call Eric</span></a>
    </div>
  </div>
</header>

<main>
<section class="rv-head">
  <div class="container rv-head-in">
    <div>
      <span class="sec-rule" aria-hidden="true"></span>
      <h1>What people say</h1>
      <p class="lede">Every review below is on our Google Business Profile. Nothing here is written by us,
         and nothing has been left out &mdash; this is all of them.</p>
    </div>

    <aside class="score">
      <div class="score-top">
        <span class="g-logo" aria-hidden="true"></span>
        <span class="score-src">Google reviews</span>
      </div>
      <div class="score-side">
        <p class="score-n">5.0</p>
        <p class="score-stars" aria-label="Average rating 5 out of 5">★★★★★</p>
        <p class="score-count">Based on %(n)d reviews</p>
      </div>

      <dl class="bars">%(bars)s</dl>

      <a class="cta-ghost score-link" href="%(profile)s" target="_blank" rel="noopener noreferrer">
        <span>See them on Google</span>
      </a>
    </aside>
  </div>
</section>

<section class="rv-body">
  <div class="container">
    <div class="rv-grid">%(cards)s</div>
  </div>
</section>

</main>

<footer class="ft">
  <div class="container ft-bottom">
    <p>&copy; <span id="footer-year">2026</span> Euro Detailing. All rights reserved.</p>
    <p class="ft-by">Owner-operated by Eric Salas</p>
  </div>
</footer>

<script src="../script.js" defer></script>
</body>
</html>
""" % dict(
  n=len(R), cards=COLUMNS, profile=G_PROFILE, write=G_WRITE,
  bars="".join('<div><dt>%d<span aria-hidden="true">★</span></dt><dd><span class="bar"><i style="width:%d%%"></i></span><b>%d</b></dd></div>'
               % (s, 100 if s == 5 else 0, len(R) if s == 5 else 0) for s in (5,4,3,2,1)))

open("preview/reviews.html","w",encoding="utf-8").write(html)
print("wrote preview/reviews.html — %d reviews, %d with an owner reply, %d rating-only"
      % (len(R), sum(1 for r in R if r[5]), sum(1 for r in R if not r[4])))
