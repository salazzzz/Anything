"""Membership page, rebuilt in the redesign language.

Restructured from the old single "2 visits a month" plan into three cadences:
every 3 months, monthly, and every 2 weeks.

PRICES BELOW ARE A PROPOSAL AND NEED ERIC'S SIGN-OFF BEFORE LAUNCH.
The biweekly column is the existing live pricing ($209/$249/$289) so the plan
that already sells is unchanged. The two new cadences are priced off the same
anchor — the one-off Basic Bundle — on a deliberate ladder: the more often you
book, the better the per-visit rate.

    biweekly   ~30% under the one-off rate
    monthly    ~22% under
    quarterly  ~11% under

Booking uses the existing sms: "claim a spot" flow, the same as the live page.
No Cal.com event exists for memberships, and inventing a slug would ship a dead
button.
"""

import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo, shell

PATH = "/membership"
TITLE = "Car Detailing Membership Newton MA — From $119/month"
DESC = ("Recurring mobile detailing in Newton, MA — every 2 weeks, monthly, or every 3 months. Save up to 30% a visit, no contract, cancel any time. We come to you.")

SIZES = [("sedan", "Sedan", "Coupe, small car"),
         ("suv", "SUV", "Crossover, wagon"),
         ("xl", "Truck / XL", "3-row, van")]
SIZE_LABEL = {"sedan": "Sedan", "suv": "SUV", "xl": "Truck / XL"}

# What the same work costs booked one at a time (Basic Bundle) — the honest
# comparison, and what the savings chip is computed against.
ONEOFF = {"sedan": 150, "suv": 180, "xl": 210}

BASE_PERKS = ["Full interior and exterior maintenance detail, every visit",
              "We come to you, anywhere within 10 miles of Newton",
              "No contract — pause or cancel any time",
              "Pay after each visit, never up front"]

PLANS = [
    dict(key="quarterly", name="Every 3 months", badge=None,
         cadence="One visit per quarter", per="per visit",
         prices={"sedan": 135, "suv": 159, "xl": 185}, visits_per_period=1,
         unit={"@type": "QuantitativeValue", "value": 1, "unitCode": "ANN",
               "unitText": "visit per quarter"},
         blurb="Seasonal reset. Enough to stop damage building up.",
         perks=BASE_PERKS + ["10% off any add-on"], nested=False),

    dict(key="monthly", name="Monthly", badge=None,
         cadence="One visit a month", per="per month",
         prices={"sedan": 119, "suv": 139, "xl": 159}, visits_per_period=1,
         unit={"@type": "QuantitativeValue", "value": 1, "unitCode": "MON",
               "unitText": "visit per month"},
         blurb="The car never actually gets dirty. Most people land here.",
         perks=["15% off any add-on", "Priority scheduling"], nested=True),

    dict(key="biweekly", name="Every 2 weeks", badge="Best value",
         cadence="Two visits a month", per="per month",
         prices={"sedan": 209, "suv": 249, "xl": 289}, visits_per_period=2,
         unit={"@type": "QuantitativeValue", "value": 2, "unitCode": "MON",
               "unitText": "visits per month"},
         blurb="Showroom condition, held there. The lowest rate per visit.",
         perks=["20% off any add-on", "First pick of every slot",
                "A complimentary wax each quarter"], nested=True),
]

# Real Google reviews that mention the plan by name — the strongest proof there
# is for this page, and they were already on the site.
PROOF = [
    ("Chris Fremont",
     "Eric also walked me through the maintenance plan, honestly a no-brainer if you "
     "want to keep the car looking like this. Thanks, Eric and team 10/10 already "
     "booked my next appointment."),
    ("David Atsiliem",
     "He also set me up with a maintenance plan, so now it's getting detailed regularly "
     "each month, which has been a huge help. Highly recommend his services."),
]

FAQ = [
    ("How does a detailing membership work?",
     "You pick how often you want the car done — every two weeks, every month, or every "
     "three months — and Eric comes to you on that schedule. Each visit is a full interior "
     "and exterior maintenance detail. You pay after each visit, and there is no contract."),
    ("Can I cancel or pause my membership?",
     "Any time, for any reason. There is no contract and no cancellation fee. If you are "
     "travelling or the car is off the road, pause it and pick back up when you are ready."),
    ("How much does a car detailing membership cost in Newton?",
     "From $135 per visit on the every-3-months plan, $119 a month on the monthly plan, and "
     "$209 a month for two visits on the every-2-weeks plan, for a sedan. SUVs and trucks are "
     "priced above that. Every plan works out cheaper per visit than booking one at a time."),
    ("What if my car needs more than a maintenance detail?",
     "Damage, heavy staining, mold or a car that has never been detailed is quoted separately "
     "at add-on rates. Members get a standing discount on every add-on."),
]

ARROW = '<svg class="arw" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def saving(plan, size):
    """Percent under the one-off Basic Bundle rate, per visit."""
    per_visit = plan["prices"][size] / plan["visits_per_period"]
    return round((1 - per_visit / ONEOFF[size]) * 100)


def size_buttons():
    return "".join(
        '<button type="button" class="sz" role="radio" aria-checked="%s" data-size="%s">'
        '<strong>%s</strong><em>%s</em></button>'
        % ("true" if k == "sedan" else "false", k, label, sub)
        for k, label, sub in SIZES)


def plan_cards():
    out = []
    for p in PLANS:
        badge = '<i>%s</i>' % p["badge"] if p["badge"] else ""
        cls = "pl pl-best" if p["badge"] else "pl"
        lead = "Everything above, plus" if p["nested"] else "Included"
        ticks = "".join("<li>%s</li>" % t for t in p["perks"])
        out.append("""<article class="%(cls)s">
        <span class="pl-name">%(name)s%(badge)s</span>
        <p class="pl-price"><sup>$</sup><span data-price="%(key)s">%(price)d</span><span class="per">%(per)s</span></p>
        <p class="pl-cadence">%(cadence)s</p>
        <span class="pl-save">Save <span data-save="%(key)s">%(save)d</span>%% a visit</span>
        <p class="pl-blurb">%(blurb)s</p>
        <span class="col-lbl">%(lead)s</span>
        <ul class="ticks">%(ticks)s</ul>
        <a class="%(btn)s pl-cta" href="sms:+17812903040"><span>Claim a spot</span>%(arrow)s</a>
      </article>""" % dict(
            cls=cls, name=p["name"], badge=badge, key=p["key"],
            price=p["prices"]["sedan"], per=p["per"], cadence=p["cadence"],
            save=saving(p, "sedan"), blurb=p["blurb"], lead=lead, ticks=ticks,
            btn="cta" if p["badge"] else "cta-ghost",
            arrow=ARROW if p["badge"] else ""))
    return "\n      ".join(out)


def schema():
    offers = []
    for p in PLANS:
        for size in ("sedan", "suv", "xl"):
            offers.append(seo.offer(
                "Membership — %s, %s" % (p["name"], SIZE_LABEL[size]),
                p["prices"][size], PATH,
                desc="%s. %s" % (p["cadence"], p["blurb"]),
                unit=p["unit"]))
    return seo.ld(
        seo.business(),
        seo.website(),
        seo.webpage(PATH, TITLE, DESC),
        seo.breadcrumb([("Home", "/"), ("Membership", PATH)]),
        seo.service("Car detailing membership", DESC, PATH, offers,
                    service_type="Recurring car detailing"),
        seo.faq(FAQ),
        *seo.reviews(PROOF))


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
    <h1>Membership</h1>
    <p class="lede">Pick how often you want the car done. Eric comes to you on that
    schedule, and every visit costs less than booking it one at a time. No contract &mdash;
    pause or cancel whenever you like.</p>
  </div>
</section>

%(trust)s

<section class="sec" id="plans">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Pick your size, then your rhythm.</h2>

    <div class="sz-row">
      <span class="sz-lbl" id="szl">Your vehicle</span>
      <div class="sz-opts" role="radiogroup" aria-labelledby="szl">%(sizes)s</div>
    </div>

    <div class="pl-grid">
      %(plans)s
    </div>

    <p class="foot-note">Savings are measured against the same work booked one visit at a
    time. Not sure which fits? <a href="tel:+17812903040">Call Eric</a>.</p>
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Why it works out cheaper.</h2>
    <p class="lede">A car that gets attention every few weeks never reaches the state that
    needs a deep clean. You are paying to keep it right instead of paying to fix it &mdash;
    and the maintenance visit is quicker, so it costs less.</p>
    <div class="ao-grid">%(proof)s</div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Questions.</h2>
    <div class="ao-grid">%(faq)s</div>
  </div>
</section>

<section class="sec sec-last">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Rather book once?</h2>
    <div class="xsell">%(xsell)s</div>
  </div>
</section>
</main>

%(footer)s

<script src="/script.js" defer></script>
<script>
var PRICES = %(prices)s;
var SAVE = %(saves)s;
(function () {
  var group = document.querySelector(".sz-opts");
  if (!group) return;
  var btns = [].slice.call(group.querySelectorAll(".sz"));
  var size = "sedan";
  function paint() {
    Object.keys(PRICES).forEach(function (k) {
      var el = document.querySelector('[data-price="' + k + '"]');
      if (el) el.textContent = PRICES[k][size];
      var s = document.querySelector('[data-save="' + k + '"]');
      if (s) s.textContent = SAVE[k][size];
    });
  }
  group.addEventListener("click", function (e) {
    var b = e.target.closest(".sz"); if (!b) return;
    size = b.dataset.size;
    btns.forEach(function (x) { x.setAttribute("aria-checked", x === b ? "true" : "false"); });
    paint();
  });
  group.addEventListener("keydown", function (e) {
    var i = btns.indexOf(document.activeElement); if (i < 0) return;
    var n = /Right|Down/.test(e.key) ? 1 : /Left|Up/.test(e.key) ? -1 : 0;
    if (!n) return;
    e.preventDefault();
    var next = btns[(i + n + btns.length) %% btns.length];
    next.focus(); next.click();
  });
  paint();
})();
</script>
</body>
</html>
"""


def build():
    proof = "".join(
        '<article class="ao"><p class="ao-note">&ldquo;%s&rdquo;</p>'
        '<span class="ao-top"><span class="ao-name">%s</span>'
        '<span class="ao-price">&#9733;&#9733;&#9733;&#9733;&#9733;</span></span></article>'
        % (text, name) for name, text in PROOF)
    faq = "".join(
        '<article class="ao"><span class="ao-name">%s</span>'
        '<p class="ao-note">%s</p></article>' % (q, a) for q, a in FAQ)
    return PAGE % dict(
        head=seo.head(TITLE, DESC, PATH, css=("/styles.css", "/tpl.css")),
        schema=schema(),
        skip=shell.SKIP, header=shell.header(), footer=shell.footer(), trust=shell.TRUST,
        sizes=size_buttons(), plans=plan_cards(), proof=proof, faq=faq,
        prices=json.dumps({p["key"]: p["prices"] for p in PLANS}),
        saves=json.dumps({p["key"]: {s: saving(p, s) for s in ("sedan", "suv", "xl")}
                          for p in PLANS}),
        xsell="".join('<a class="xs" href="%s"><span class="xs-name">%s</span>'
                      '<span class="xs-price">from $%d</span></a>' % (p, n, pr)
                      for n, p, pr in [("Interior Detailing", "/services/interior", 105),
                                       ("Exterior Detailing", "/services/exterior", 70),
                                       ("Interior + Exterior", "/services/bundle", 150)]))


if __name__ == "__main__":
    open("membership.html", "w", encoding="utf-8").write(build())
    for p in PLANS:
        print("  %-14s sedan $%-4d suv $%-4d xl $%-4d   saves %d%%/%d%%/%d%% a visit"
              % (p["name"], p["prices"]["sedan"], p["prices"]["suv"], p["prices"]["xl"],
                 saving(p, "sedan"), saving(p, "suv"), saving(p, "xl")))
    print("wrote membership.html")
