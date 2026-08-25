"""Per-town facts for the service-area landing pages.

Every claim in here is checkable. Neighbourhood and landmark names were verified
against the city sites and Wikipedia before being written down — a landing page
that invents a local detail is worse than no landing page, because the one
reader who lives there instantly knows it was not written by a neighbour.

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
BASE = (42.3487, -71.2276)          # West Newton, 02465 — where the van starts

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
    "Eric grew up here and the van starts here, which means West Newton bookings "
    "get the earliest slots of the day and the shortest notice we can offer anywhere.",
    "The village centre along Washington Street is a National Register historic "
    "district, and the housing around it shows it — a lot of late-1800s and "
    "early-1900s homes with the short, narrow, often shared driveways that came "
    "with them. We work in that space every week and it is not a problem.",
  ],
  parking="Near West Newton Square, driveways are usually short and sometimes "
          "shared, so we set up compact and stay out of your neighbour's way. "
          "Further out toward Auburndale and Newtonville there is normally a full "
          "driveway to work in. Either way we bring our own water and power.",
  spots=["West Newton Square", "Washington Street", "Watertown Street",
         "Waltham Street", "Chestnut Street", "Elm Street", "Cherry Street",
         "Highland Street"],
  faq=[
    ("Do you charge extra to come to West Newton?",
     "No. West Newton is where Euro Detailing is based — 02465 — so there is no "
     "travel charge and no minimum. Prices on the service pages are what you pay."),
    ("My driveway near the square is tiny. Is that a problem?",
     "No. A lot of the housing around the West Newton historic district has short "
     "or shared driveways and we detail in them constantly. We only need roughly a "
     "car's width of clearance on one side to work."),
    ("Can you come the same day?",
     "Often, in West Newton specifically, because there is no drive time. Call or "
     "text +1 781-290-3040 and Eric will tell you straight away what is open."),
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
  lede="Waltham is a few minutes up Lexington Street from our base in West Newton, "
       "and it is one of the towns we are in most often.",
  local=[
    "Waltham is really several different parking situations wearing one name. "
    "Around Moody Street and the City Center it is apartments, condos and shared "
    "lots. Out in Piety Corner and Warrendale it is single-family homes with proper "
    "driveways and room to spare.",
    "There is also a real student population here between Bentley and Brandeis — "
    "cars that sit through a New England winter taking road salt and then get sold "
    "or handed on in spring. A detail before that sale is usually worth several "
    "times what it costs.",
  ],
  parking="If you are in a condo or apartment near Moody Street, all we need is a "
          "spot we are allowed to occupy for the length of the job — a numbered "
          "space or visitor spot is fine. In Piety Corner, Warrendale and North "
          "Waltham there is normally a driveway, which is ideal. We carry our own "
          "water and power either way, so no hookup is needed.",
  spots=["Moody Street", "Waltham City Center", "Piety Corner", "Warrendale",
         "North Waltham", "The Highlands", "Bleachery", "Bentley University area",
         "Brandeis University area", "Prospect Hill"],
  faq=[
    ("Do you come to apartment and condo buildings in Waltham?",
     "Yes, and it is a large share of what we do around Moody Street and the City "
     "Center. We just need a parking space we are permitted to use for the length "
     "of the appointment. A visitor or numbered spot works."),
    ("Do you need access to my water or an outlet?",
     "No. The van carries its own water and power, which is what makes condo lots "
     "and campus parking workable in the first place."),
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
         "Acura MDX covered in snow foam during a curbside mobile wash in Watertown, MA"),
  title="Mobile Car Detailing in Watertown, MA — We Come to You",
  desc="Mobile car detailing in Watertown, MA. Curbside or driveway, we bring our "
       "own water and power — interior, exterior and full details from $70. 5.0 stars.",
  lede="Watertown is a short run east along the river from West Newton, and the "
       "housing there asks a bit more of a mobile detailer than the suburbs do.",
  local=[
    "Between Watertown Square, Coolidge Square along Mount Auburn Street and the "
    "streets off Arsenal Yards in East Watertown, a lot of the housing is two- and "
    "three-family with no driveway to speak of. Plenty of detailers quietly will "
    "not work in that.",
    "We do, because the van is genuinely self-contained — our own water, our own "
    "power. If the only place your car lives is the street in front of your house, "
    "that is a place we can work.",
  ],
  parking="Curbside is completely normal here and we are set up for it. We need "
          "roughly one parking space plus enough room to open doors and move around "
          "the car. If you have a driveway or a spot behind the building, even "
          "better. Nothing needs to be plugged in and no hose is required.",
  spots=["Watertown Square", "Coolidge Square", "Mount Auburn Street",
         "East Watertown", "Arsenal Yards", "Bemis", "West End",
         "Charles River waterfront"],
  faq=[
    ("I only have street parking in Watertown. Can you still detail my car?",
     "Yes. Curbside is routine for us in Watertown and the van is fully "
     "self-contained — we bring our own water and power, so nothing has to run from "
     "your building. One parking space with room to walk around the car is enough."),
    ("Do I need to be home while you work?",
     "No. As long as we can get to the vehicle and the keys, you can go about your "
     "day. Eric sends updates and lets you know when it is done, and you pay after "
     "you have seen the result."),
    ("Is Watertown inside your service area?",
     "Yes. We travel up to 10 miles from Newton and Watertown is comfortably inside "
     "that, so there is no travel surcharge."),
  ]),
]
