"""The seven add-ons, in one place.

Previously this list was duplicated in gen_services.py and svcdata.py with no
descriptions at all — seven flat chips. Both generators now read from here, so
a price change lands everywhere at once.

Spelling note: "Mould"/"tyre"/"odour"/"microfibre" were British throughout.
Changed to US spellings — the customers are in Massachusetts and they search
"mold removal" and "tire shine", not the British forms. That is a real ranking
difference, not a style preference.
"""

# slug, name, price label, price for schema, one-line description
ADDONS = [
    ("pet-hair", "Pet hair removal", "$35+", 35.00,
     "Embedded hair pulled from carpet and upholstery, not just vacuumed over."),
    ("seat-extraction", "Seat extraction", "$49.99+", 49.99,
     "Hot-water extraction that pulls dirt and staining up out of the foam."),
    ("engine-bay", "Engine bay detail", "$49.99", 49.99,
     "Degreased, rinsed and dressed so the bay looks as clean as the paint."),
    ("mold-removal", "Mold removal", "$49.99", 49.99,
     "Treated at the source and neutralized, not perfumed over."),
    ("clay-bar", "Clay bar treatment", "$49.99", 49.99,
     "Lifts bonded road film and sap so the paint is genuinely smooth again."),
    ("wax", "Car waxing", "$34.99", 34.99,
     "A hand-applied wax layer for depth of gloss and a few months of protection."),
    ("mat-restoration", "Plastic mat restoration", "$25+", 25.00,
     "Faded plastic mats brought back to a clean, even finish."),
]

# The short label used in the compact strip at the foot of each service page.
SHORT = {
    "pet-hair": "Pet hair removal",
    "seat-extraction": "Seat extraction",
    "engine-bay": "Engine bay",
    "mold-removal": "Mold removal",
    "clay-bar": "Clay bar",
    "wax": "Wax",
    "mat-restoration": "Mat restoration",
}


def strip_html():
    """Compact linked cards for the foot of a service page."""
    cards = "".join(
        '<a class="ao" href="/addons#%s">'
        '<span class="ao-top"><span class="ao-name">%s</span>'
        '<span class="ao-price">%s</span></span></a>'
        % (slug, SHORT[slug], price)
        for slug, _n, price, _p, _d in ADDONS)
    return ('<div class="ao-grid ao-strip">%s</div>'
            '<p class="ao-more">Any add-on can go on any package. '
            '<a href="/addons">See what each one involves &rarr;</a></p>' % cards)
