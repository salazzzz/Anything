import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo, shell
from addondata import ADDONS, strip_html

SIZES = [("sedan","Sedan","Coupe, small car"),("suv","SUV","Crossover, wagon"),("xl","Truck / XL","3-row, van")]

SERVICES = {
"interior": dict(
  name="Interior Detailing", file="services/interior.html", path="/services/interior",
  title="Interior Car Detailing Newton MA — We Come to You",
  desc="Mobile interior detailing in Newton, MA. Steam clean, stain and odor removal, "
       "leather conditioned — in your driveway. From $105, 5.0 stars, pay after.",
  visual=("beforeafter", (("/images/after.webp", "Car interior after detailing"),
                          ("/images/before.webp", "The same interior before detailing"))),
  pitch=["A vacuum and a wipe-down moves dirt around. It doesn't take it out.",
         "The inside of a car is one of the dirtiest surfaces you touch all day &mdash; right behind the toilet seat. Bacteria sitting in the vents, dirt worked deep into the carpet, and smells that come straight back because nothing was ever actually pulled out.",
         "<strong>Basic</strong> is for a car that's already kept up. If it's been more than three months since the last detail, take the <strong>Deep Clean</strong>."],
  kicker="You don't deserve a dirty interior.",
  basic=dict(sizes={"sedan":(105,"~1.5–2 hrs","basic-interior-detail"),
                    "suv":(125,"~2–2.5 hrs","basic-interior-detail-suv"),
                    "xl":(145,"~2.5–3 hrs","basic-interior-detail-xl")},
             inc=["Full interior vacuum — seats, floors, trunk","Dashboard, console and vents wiped down",
                  "Door panels cleaned","Interior windows cleaned","Floor mats cleaned","Door jambs washed",
                  "Matte satin finish","Light fragrance finish"]),
  premium=dict(sizes={"sedan":(165,"~2.5–3 hrs","premium-interior-detail"),
                      "suv":(190,"~3–3.5 hrs","premium-interior-detail-suv"),
                      "xl":(215,"~3.5–4 hrs","premium-interior-detail-xl")},
             inc=["Spot and stain removal, cloth seats and carpets","Full steam clean",
                  "Leather cleaned and conditioned (if applicable)","Light pet hair removal",
                  "Plastic floor mat restoration","Deeper odor treatment and fragrance finish"])),

"exterior": dict(
  name="Exterior Detailing", file="services/exterior.html", path="/services/exterior",
  title="Exterior Car Detailing Newton MA — We Come to You",
  desc="Mobile exterior detailing in Newton, MA. Foam bath hand wash, clay bar "
       "decontamination, six months of sealant. From $70, 5.0 stars, pay after.",
  visual=("beforeafter", (("/images/gallery/bmw-x5m-matte-after.webp", "Matte black BMW X5 M after a full exterior detail"),
                          ("/images/gallery/bmw-x5m-matte-before.webp", "The same BMW X5 M before the detail, covered in road dust"))),
  pitch=["A wash gets the dirt off. It doesn't get the paint clean.",
         "Road film, brake dust and tree sap bond to the clear coat and stay there &mdash; you can feel it as roughness under your fingertips. Washing over it seals it in, and the shine you were after never quite arrives.",
         "<strong>Basic</strong> is a proper hand wash with four weeks of protection. If the paint feels rough, or it has been a season, take the <strong>Deep Clean</strong> &mdash; clay bar, decontamination and six months of sealant."],
  kicker="Your paint is the first thing anyone sees.",
  basic=dict(sizes={"sedan":(70,"~45 min – 1 hr","basic-exterior-detail-sedan"),
                    "suv":(85,"~1 hr","basic-exterior-detail-suv"),
                    "xl":(100,"~1 hr","basic-exterior-detail-xl")},
             inc=["Foam bath and hand wash","Wheels, tires and wheel wells cleaned","4 week protective sealant",
                  "Exterior windows cleaned","Tire shine dressing","Hand dried with soft microfiber"]),
  premium=dict(sizes={"sedan":(105,"~1 hr","permium-exterior-detail-sedan"),
                      "suv":(120,"~1.5 hrs","premium-exterior-detail-suv"),
                      "xl":(135,"~1–2 hrs","premium-exterior-detail-xl")},
             inc=["Clay bar treatment (paint decontamination)","Acid wash on wheels (if applicable)",
                  "6 month protective sealant","Basic tree sap removal","Trim restoration"])),

"bundle": dict(
  name="Interior + Exterior", file="services/bundle.html", path="/services/bundle",
  title="Full Car Detailing Newton MA, Inside and Out — We Come to You",
  desc="Interior and exterior detailing in one mobile visit in Newton, MA. Cheaper "
       "than booking both separately and it takes one afternoon. From $150, 5.0 stars, pay after the job.",
  visual=("duo", None),
  pitch=["Inside and out, in a single visit.",
         "Most people book one and then wish they had booked both. A spotless interior makes tired paint obvious, and fresh paint makes a dusty dash impossible to ignore. Together it costs less than two separate appointments and takes one afternoon instead of two.",
         "<strong>Basic</strong> covers a car that is kept up. If it has been more than three months, or it has never been detailed, take the <strong>Deep Clean</strong>."],
  kicker="One appointment. The whole car.",
  basic=dict(sizes={"sedan":(150,"~2.5–3 hrs","basic-bundle-detail-sedan"),
                    "suv":(180,"~3 hrs","basic-bundle-detail-suv"),
                    "xl":(210,"~3.5 hrs","basic-bundle-detail-xl")},
             inc=["Full interior vacuum and wipe down","Interior windows and door panels",
                  "Floor mats cleaned and dressed","Foam bath and exterior hand wash",
                  "Wheels, tires and wheel wells","Tire shine and hand dried finish"]),
  premium=dict(sizes={"sedan":(230,"~3.5–4 hrs","premium-bundle-detail-sedan"),
                      "suv":(265,"~4–4.5 hrs","premium-bundle-detail-suv"),
                      "xl":(300,"~5 hrs","premium-bundle-detail-xl")},
             inc=["Spot and stain removal, cloth seats and carpets","Leather cleaned and conditioned",
                  "Clay bar treatment (paint decontamination)","6 month protective sealant",
                  "Trim restoration and dressing","Professional finish and fragrance"])),
}

SIZE_LABEL = {"sedan": "Sedan", "suv": "SUV", "xl": "Truck / XL"}

ARROW = '<svg class="arw" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def slider(base, over, base_lbl, over_lbl, base_alt, over_alt, aria):
    """The overlay sits on the LEFT, so whatever belongs on the left goes in `over`."""
    return """<div class="ba" id="ba">
      <img class="ba-img" src="%s" alt="%s" width="1200" height="900" decoding="async">
      <div class="ba-after" id="baAfter">
        <img class="ba-img" src="%s" alt="%s" width="1200" height="900" decoding="async">
      </div>
      <span class="ba-tag ba-tag-l">%s</span>
      <span class="ba-tag ba-tag-r">%s</span>
      <div class="ba-divider" id="baDivider">
        <span class="ba-handle" id="baHandle" role="slider" tabindex="0"
              aria-label="%s" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
          <svg width="20" height="12" viewBox="0 0 22 12" fill="none" aria-hidden="true">
            <path d="M8 1.5 3.5 6 8 10.5M14 1.5 18.5 6 14 10.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </div>
      <span class="ba-hint">Drag</span>
    </div>""" % (base, base_alt, over, over_alt, over_lbl, base_lbl, aria)


def schema_for(S):
    """Service + OfferCatalog carrying all six real prices, plus breadcrumb."""
    offers = []
    for tier, label in (("basic", "Basic"), ("premium", "Deep Clean")):
        for key in ("sedan", "suv", "xl"):
            price, _time, _slug = S[tier]["sizes"][key]
            offers.append(seo.offer(
                "%s — %s, %s" % (S["name"], label, SIZE_LABEL[key]),
                price, S["path"],
                desc="; ".join(S[tier]["inc"][:4])))
    return seo.ld(
        seo.business(),
        seo.website(),
        seo.webpage(S["path"], S["title"].replace("&amp;", "&"), S["desc"]),
        seo.breadcrumb([("Home", "/"), ("Services", "/#services"),
                        (S["name"], S["path"])]),
        seo.service(S["name"], S["desc"], S["path"], offers))


def build(key, S):
    other = [(k, v) for k, v in SERVICES.items() if k != key]
    sizes = "".join('<button type="button" class="sz" role="radio" aria-checked="%s" data-size="%s"><strong>%s</strong><em>%s</em></button>'
                    % ("true" if k == "sedan" else "false", k, l, sub) for k, l, sub in SIZES)
    v = S["visual"][0]
    if v == "beforeafter":
        a, bfr = S["visual"][1]
        visual = slider(a[0], bfr[0], "After", "Before", a[1], bfr[1],
                        "Drag to compare before and after")
    elif v == "duo":
        visual = slider("/images/gallery/bmw-x5m-matte-after.webp",
                        "/images/gallery/mercedes-beige-interior-cleaned.webp",
                        "Exterior", "Interior",
                        "Matte black BMW X5 M after a full exterior detail",
                        "Cleaned Mercedes-Benz beige leather interior",
                        "Drag to see the interior and the exterior")
    else:
        visual = ('<img class="hero-a-shot" src="/images/%s" alt="%s by Euro Detailing" width="800" height="500" decoding="async">'
                  % (S["visual"][1], S["name"]))

    data = {t: {s: list(v) for s, v in S[t]["sizes"].items()} for t in ("basic", "premium")}

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
      <h1>%(name)s</h1>
      <div class="pitch">
        %(pitch)s
        <p class="pitch-kicker">%(kicker)s</p>
      </div>
    </div>
    %(visual)s
  </div>

  <a class="cue" href="#pick">
    <span class="cue-txt">Pick your size &amp; level</span>
    <span class="cue-rail"><span class="cue-dot"></span></span>
  </a>
</section>

%(trust)s

<section class="sec" id="pick">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Pick your size, then your level.</h2>

    <div class="sz-row">
      <span class="sz-lbl" id="szl">Your vehicle</span>
      <div class="sz-opts" role="radiogroup" aria-labelledby="szl">%(sizes)s</div>
    </div>

    <div class="tier-grid">
      <article class="tier">
        <span class="tier-lbl">Basic</span>
        <p class="tier-price"><sup>$</sup><span data-price="basic">%(bp)d</span></p>
        <p class="tier-time" data-time="basic">%(bt)s</p>
        <p class="tier-blurb">Kept up regularly? This is plenty.</p>
        <div class="tier-cols">
          <div>
            <span class="col-lbl">Included</span>
            <ul class="ticks">%(binc)s</ul>
          </div>
          <div>
            <span class="col-lbl col-lbl-no">Not included</span>
            <ul class="ticks nots">%(bexc)s</ul>
          </div>
        </div>
        <a class="cta-ghost tier-cta" data-book="basic" href="#"><span>Book Basic</span></a>
      </article>

      <article class="tier tier-best">
        <span class="tier-lbl">Deep Clean<i>Most booked</i></span>
        <p class="tier-price"><sup>$</sup><span data-price="premium">%(pp)d</span></p>
        <p class="tier-time" data-time="premium">%(pt)s</p>
        <p class="tier-blurb">Been a while, or you want it perfect.</p>
        <div class="tier-cols tier-cols-one">
          <div>
            <span class="col-lbl">Everything in Basic, plus</span>
            <ul class="ticks">%(pinc)s</ul>
          </div>
        </div>
        <a class="cta tier-cta" data-book="premium" href="#"><span>Book Deep Clean</span>%(arrow)s</a>
      </article>
    </div>

    <p class="foot-note">Not sure which? <a href="tel:+17812903040">Call Eric</a> and describe the car.</p>
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Add anything on.</h2>
    %(addons)s
  </div>
</section>

<section class="sec">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Booking more than once?</h2>
    <p class="lede">A membership keeps the car in this condition year-round and works out cheaper than booking each detail one at a time.</p>
    <p class="foot-note"><a href="/membership">See membership plans &rarr;</a></p>
  </div>
</section>

<section class="sec sec-last">
  <div class="container">
    <span class="sec-rule" aria-hidden="true"></span>
    <h2 class="sec-h">Looking at something else?</h2>
    <div class="xsell">%(xsell)s</div>
  </div>
</section>
</main>

%(footer)s

<script src="/script.js" defer></script>
<script>
var CAL = "https://cal.com/eric-salas/";
var DATA = %(data)s;
(function () {
  var size = "sedan";
  function paint() {
    ["basic","premium"].forEach(function (t) {
      var d = DATA[t][size];
      document.querySelectorAll('[data-price="'+t+'"]').forEach(function (e) { e.textContent = d[0]; });
      document.querySelectorAll('[data-time="'+t+'"]').forEach(function (e) { e.textContent = d[1]; });
      document.querySelectorAll('[data-book="'+t+'"]').forEach(function (e) { e.href = CAL + d[2]; });
    });
  }
  var group = document.querySelector(".sz-opts");
  var btns = [].slice.call(group.querySelectorAll(".sz"));
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

/* before / after — only on the page that has one */
(function () {
  var box = document.getElementById("ba");
  if (!box) return;
  var after = document.getElementById("baAfter"),
      divider = document.getElementById("baDivider"),
      handle = document.getElementById("baHandle"),
      pct = 50, dragging = false;
  function set(v) {
    pct = Math.max(0, Math.min(100, v));
    after.style.width = pct + "%%";
    divider.style.left = pct + "%%";
    handle.style.left = pct + "%%";
    handle.setAttribute("aria-valuenow", Math.round(pct));
    box.classList.add("touched");
  }
  function at(e) { var r = box.getBoundingClientRect(); return ((e.clientX - r.left) / r.width) * 100; }
  box.addEventListener("pointerdown", function (e) { dragging = true; box.setPointerCapture(e.pointerId); set(at(e)); e.preventDefault(); });
  box.addEventListener("pointermove", function (e) { if (dragging) set(at(e)); });
  box.addEventListener("pointerup",     function () { dragging = false; });
  box.addEventListener("pointercancel", function () { dragging = false; });
  handle.addEventListener("keydown", function (e) {
    var step = e.shiftKey ? 10 : 2, hit = true;
    if      (e.key === "ArrowLeft"  || e.key === "ArrowDown") set(pct - step);
    else if (e.key === "ArrowRight" || e.key === "ArrowUp")   set(pct + step);
    else if (e.key === "Home") set(0);
    else if (e.key === "End")  set(100);
    else hit = false;
    if (hit) e.preventDefault();
  });
})();
</script>
</body>
</html>
""" % dict(
    head=seo.head(S["title"], S["desc"], S["path"], css=("/styles.css", "/tpl.css")),
    schema=schema_for(S),
    skip=shell.SKIP, header=shell.header(), footer=shell.footer(), trust=shell.TRUST,
    name=S["name"],
    pitch="\n        ".join("<p>%s</p>" % p for p in S["pitch"]),
    kicker=S["kicker"], visual=visual, sizes=sizes, arrow=ARROW,
    bp=S["basic"]["sizes"]["sedan"][0], bt=S["basic"]["sizes"]["sedan"][1],
    pp=S["premium"]["sizes"]["sedan"][0], pt=S["premium"]["sizes"]["sedan"][1],
    binc="".join("<li>%s</li>" % b for b in S["basic"]["inc"]),
    bexc="".join('<li class="no">%s</li>' % b for b in S["premium"]["inc"]),
    pinc="".join("<li>%s</li>" % b for b in S["premium"]["inc"]),
    addons=strip_html(),
    xsell="".join('<a class="xs" href="%s"><span class="xs-name">%s</span><span class="xs-price">from $%d</span></a>'
                  % (v["path"], v["name"], v["basic"]["sizes"]["sedan"][0]) for k, v in other),
    data=json.dumps(data).replace('", "', '","'))


if __name__ == "__main__":
    os.makedirs("services", exist_ok=True)
    for k, S in SERVICES.items():
        open(S["file"], "w", encoding="utf-8").write(build(k, S))
        print("wrote %-26s  basic $%d  deep $%d  visual=%s" % (
            S["file"], S["basic"]["sizes"]["sedan"][0], S["premium"]["sizes"]["sedan"][0], S["visual"][0]))
