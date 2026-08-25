"""Per-town facts for the service-area landing pages.

Neighbourhood and landmark names were verified against the city sites and
Wikipedia before being written down — a landing page that invents a local detail
is worse than no landing page, because the one reader who lives there instantly
knows it was not written by a neighbor.

HOW THE SERVICE ACTUALLY WORKS — read before editing any copy here.
The customer provides the water and the power. From the site's own FAQ, which is
the owner's wording and the authority: "Just a spot for your vehicle and access
to a water source and outdoor outlet if possible. If your location doesn't have
either, let us know in advance — we can usually work around it."

The first version of these pages claimed the opposite — that we carry our own
water and power and the vehicle is "self-contained" — across eight places
including three meta descriptions and two FAQ schema answers, and built the
whole Watertown page on it. None of it was true. Do not write a capability into
this file that is not already stated somewhere the owner wrote. That goes for
operational promises too: same-day availability, how often we work in a given
town, and what other detailers will or will not do are all things this file used
to assert and could not support.

The pages exist because every competitor that outranks us in the surrounding
towns has one page per town and we had none: our only geographic page was the
homepage, which targets Newton. Nothing can rank for "detailing Waltham" if
there is no page about Waltham.

What keeps these off Google's doorway-page radar is that `local`, `parking`,
`spots` and `faq` are genuinely different per town, not one paragraph with the
name swapped. If you add a town, write it real or do not add it.
"""

# Straight-line miles are computed from these in gen_towns.py, not hardcoded,
# so the numbers can never drift from the coordinate they claim to describe.
BASE = (42.3487, -71.2276)          # West Newton, 02465 — the base we travel from

# The standard answer to "what do you need from me", in the owner's own terms.
# Reused verbatim so it cannot drift town to town.
NEEDS = ("A spot for the vehicle, and access to a water source and an outdoor "
         "outlet if possible. If your place does not have either, let Eric know "
         "when you book rather than on the day — it can usually be worked around.")

TOWNS = [

dict(
  slug="west-newton",
  town="West Newton",
  full="West Newton, MA",
  coord=(42.3487, -71.2276),
  home=True,                        # this is the base; suppress the travel line
  # A different real photo per town, with town-specific alt text. Two reasons:
  # the pages must not look like one template three times, and local image alt
  # is a genuine ranking signal for image search.
  image=("/images/gallery/mobile-detailing-setup-driveway.webp", 1086, 1448,
         "Euro Detailing's mobile setup and equipment in a West Newton, MA driveway"),
  title="Mobile Car Detailing in West Newton, MA — We Come to You",
  desc="Mobile car detailing in West Newton, MA 02465 — we are based here. "
       "Interior, exterior and full details in your driveway, from $70. 5.0 stars, pay after.",
  lede="West Newton is home. Euro Detailing is run out of 02465, so this is the "
       "one place on the map where there is no travel time at all.",
  local=[
    "Being based in 02465 means West Newton is the shortest trip we make, and "
    "there is no travel charge on top of the prices you see.",
    "The village center along Washington Street is a National Register historic "
    "district, and the housing around it shows it — a lot of late-1800s and "
    "early-1900s homes with the short, narrow, often shared driveways that came "
    "with them. A tight driveway is not a problem; we set up compact.",
  ],
  parking="Near West Newton Square, driveways are usually short and sometimes "
          "shared, so we set up compact and stay out of your neighbor's way. "
          "Further out toward Auburndale and Newtonville there is normally a full "
          "driveway to work in. Either way, what helps most is a spot for the car "
          "plus access to an outside tap and an outdoor outlet.",
  spots=["West Newton Square", "Washington Street", "Watertown Street",
         "Waltham Street", "Chestnut Street", "Elm Street", "Cherry Street",
         "Highland Street"],
  faq=[
    ("Do you charge extra to come to West Newton?",
     "No. West Newton is where Euro Detailing is based — 02465 — so there is "
     "no travel charge. The prices on the service pages are what you pay."),
    ("My driveway near the square is tiny. Is that a problem?",
     "No. A lot of the housing around the West Newton historic district has short "
     "or shared driveways. We only need roughly a car's width of clearance on one "
     "side to work."),
    ("What do you need from me on the day?", NEEDS),
  ]),

dict(
  slug="waltham",
  town="Waltham",
  full="Waltham, MA",
  coord=(42.3765, -71.2356),
  image=("/images/gallery/audi-q8-black-exterior.webp", 1536, 1024,
         "Glossy black Audi Q8 after a mobile exterior detail in Waltham, MA"),
  title="Mobile Car Detailing in Waltham, MA — We Come to You",
  desc="Mobile car detailing in Waltham, MA. We come to your driveway, condo lot "
       "or campus parking — interior, exterior and full details from $70. 5.0 stars, pay after.",
  lede="Waltham sits just north of our base in West Newton — one of the "
       "shortest trips we make outside Newton itself.",
  local=[
    "Waltham is really several different parking situations wearing one name. "
    "Around Moody Street and the City Center it is apartments, condos and shared "
    "lots. Out in Piety Corner and Warrendale it is single-family homes with proper "
    "driveways and room to spare.",
    "There is also a real student population here between Bentley and Brandeis "
    "— cars that sit through a New England winter taking road salt and then "
    "get sold or handed on in spring. If that is your car, it is worth cleaning up "
    "properly before the photos go online.",
  ],
  parking="If you are in a condo or apartment near Moody Street, we need a spot you "
          "are allowed to give us for the length of the job — a numbered space "
          "or visitor spot is fine — and, where possible, an outside tap and "
          "outdoor outlet you can reach from it. In Piety Corner, Warrendale and "
          "North Waltham there is normally a driveway, which is easier on both "
          "counts. If you cannot get to water or power where you park, say so when "
          "you book.",
  spots=["Moody Street", "Waltham City Center", "Piety Corner", "Warrendale",
         "North Waltham", "The Highlands", "Bleachery", "Bentley University area",
         "Brandeis University area", "Prospect Hill"],
  faq=[
    ("Do you come to apartment and condo buildings in Waltham?",
     "Yes. We need a parking space you are permitted to use for the length of the "
     "appointment — a visitor or numbered spot works. Worth checking at the "
     "same time whether you can reach an outside tap and an outdoor outlet from it; "
     "if not, mention it when you book."),
    ("What do you need from me on the day?", NEEDS),
    ("I am a Bentley or Brandeis student selling my car. What should I book?",
     "For a car being sold, the Interior + Exterior bundle does the most for resale "
     "photos and walkarounds. If the paint has taken a winter of road salt, take the "
     "Deep Clean level — clay bar and sealant make the biggest visible difference."),
  ]),

dict(
  slug="watertown",
  town="Watertown",
  full="Watertown, MA",
  coord=(42.3709, -71.1828),
  image=("/images/gallery/acura-mdx-snow-foam-wash.webp", 1206, 1029,
         "Acura MDX covered in snow foam during a mobile wash in Watertown, MA"),
  title="Mobile Car Detailing in Watertown, MA — We Come to You",
  desc="Mobile car detailing in Watertown, MA — Watertown Square, Coolidge Square "
       "and East Watertown. Curbside or driveway, from $70. 5.0 stars, pay after the job.",
  lede="Watertown is a short run east along the river from West Newton, and the "
       "housing there asks a bit more planning than the suburbs do.",
  local=[
    "Between Watertown Square, Coolidge Square along Mount Auburn Street and the "
    "streets off Arsenal Yards in East Watertown, a lot of the housing is two- and "
    "three-family with no driveway to speak of.",
    "That does not rule out a detail — a car can be done at the curb. The part "
    "worth sorting before you book is not the parking, it is whether you can reach "
    "an outside tap and an outdoor outlet from where the car sits. That is the bit "
    "dense housing makes awkward, and it is much easier to plan for in advance than "
    "to discover on the day.",
  ],
  parking="Kerbside works here. We need roughly one parking space plus enough room "
          "to open doors and move around the car; a driveway or a spot behind the "
          "building is easier still. Alongside the space, access to an outside tap "
          "and an outdoor outlet is what makes the job straightforward — and "
          "if there is genuinely no way to reach either, tell Eric when you book and "
          "he will work around it.",
  spots=["Watertown Square", "Coolidge Square", "Mount Auburn Street",
         "East Watertown", "Arsenal Yards", "Bemis", "West End",
         "Charles River waterfront"],
  faq=[
    ("I only have street parking in Watertown. Can you still detail my car?",
     "Yes, a car can be detailed at the curb. We need one parking space with room to "
     "walk around it. Check at the same time whether you can reach an outside tap and "
     "an outdoor outlet from that spot — if not, mention it when you book so it "
     "can be planned for."),
    ("Do I need to be home while you work?",
     "No. As long as we can get to the vehicle and the keys, you can go about your "
     "day. Eric sends updates and lets you know when it is done, and you pay after "
     "you have seen the result."),
    ("Is Watertown inside your service area?",
     "Yes. We travel up to 10 miles from Newton and Watertown is comfortably inside "
     "that, so there is no travel surcharge."),
  ]),
]
