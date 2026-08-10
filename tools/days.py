# Trip data for Run.Ride the Alps, 14-23 July 2026.
# Every figure here is taken from alps-run.html / alps-ride.html so the journal,
# the gallery and the route pages can never drift apart.
#
# ig_url: paste the Instagram permalink for each day's carousel as it goes up.
# Empty string falls back to the profile link.

PROFILE = "https://instagram.com/thesouthend.co"

TOTALS = {
    "distance": "339km",
    "ascent": "+11,960m",
    "days": "11 days",
    "high": "2,804m",
}

DAYS = [
    {
        "slug": "day0",
        "part": "Prologue",
        "date": "Monday 13 July",
        "date_iso": "2026-07-13",
        "title": "Bressanone",
        "where": "South Tyrol, Italy",
        "kind": "travel",
        "blurb": "Bikes stashed in Bolzano, packs weighed, an early night in Brixen. "
                 "Nothing had started yet.",
        "stats": [],
        "chain": ["Bolzano / Bozen", "bike drop", "Bressanone / Brixen"],
        "notes": [
            "The bikes and road kit were dropped at the Bolzano Youth Hostel on the way "
            "through, to be collected six days later on the far side of the run.",
            "Packs down to hut weight: liner, one spare layer, waterproof, 1.5L, "
            "and enough cash for four nights. The huts take nothing else.",
        ],
        "ig_url": "",
    },
    {
        "slug": "run1",
        "part": "The Run · Stage 1",
        "date": "Tuesday 14 July",
        "date_iso": "2026-07-14",
        "title": "Plose → Rifugio Puez",
        "where": "Puez-Odle",
        "kind": "run",
        "blurb": "A gondola does the first 1,000 metres. Everything after that is earned.",
        # 29km, not the ~25km still shown on alps-run.html; corrected on the v10
        # title and map cards in e4c0ac9.
        "stats": [("29km", "Distance"), ("+1,250m", "Ascent"), ("2,475m", "Night at")],
        # v10 supersedes run1_1_title.jpg / run1_9_map.jpg; the v9_pick_* frames are
        # the hand-picked shots added for this post.
        "title_img": "v10_run1_title.jpg",
        "map_img": "v10_run1_map.jpg",
        "extra_shots": ["v9_pick_tower.jpg", "v9_pick_photographer.jpg",
                        "v9_pick_hut.jpg", "v9_pick_runners.jpg",
                        "v9_pick_meadow.jpg", "v9_pick_wildflower.jpg"],
        "chain": ["Bressanone", "gondola ↑ Plose", "Schlüterhütte", "Rifugio Puez (2,475m)"],
        "notes": [
            "Bus from Bressanone station to the gondola base, first cabin at 8:45, free "
            "on the Brixen guest card. Running starts at the top station, around 2,050m.",
            "The Seceda ridgeline opens up almost immediately, and the Odle stay on your "
            "shoulder for most of the day.",
            "Night at Rifugio Puez, 2,475m.",
        ],
        "ig_url": "",
    },
    {
        "slug": "run2",
        "part": "The Run · Stage 2",
        "date": "Wednesday 15 July",
        "date_iso": "2026-07-15",
        "title": "Puez → Castiglioni Marmolada",
        "where": "Sella & Langkofel",
        "kind": "run",
        "blurb": "The longest climbing day of the run, and the one with cables on it.",
        "stats": [("25.5km", "Distance"), ("+1,310m", "Ascent"), ("5–6h", "Moving")],
        "chain": ["Rifugio Puez", "Passo Gardena", "Val Setus", "Pisciadu", "Rifugio Boè",
                  "Passo Pordoi", "Viel dal Pan", "Castiglioni"],
        "notes": [
            "Val Setus is a short cabled section. Walked, not run. Early, spaced out, "
            "with rockfall overhead the whole way up.",
            "Out of the Sella the Viel dal Pan traverse runs straight at the Marmolada, "
            "with Lake Fedaia below.",
            "Night at Castiglioni Marmolada. Strict 08:00 to 09:00 check-out, so packed "
            "the night before.",
        ],
        "ig_url": "",
    },
    {
        "slug": "run3",
        "part": "The Run · Stage 3",
        "date": "Thursday 16 July",
        "date_iso": "2026-07-16",
        "title": "Castiglioni → Passo Valles",
        "where": "Forca Rossa",
        "kind": "run",
        "blurb": "The biggest distance of the four, and the only cash machine on the route.",
        "stats": [("27.4km", "Distance"), ("+1,410m", "Ascent"), ("4–5h", "Moving")],
        "chain": ["Castiglioni", "Malga Ciapela", "Forca Rossa", "Passo San Pellegrino",
                  "Capanna Passo Valles"],
        "notes": [
            "Passo San Pellegrino has the only ATM on the whole traverse. Every hut is "
            "cash only, so this is the stop that makes the rest of the week work.",
            "Forca Rossa is the high point of the day and the colour changes with it. "
            "Red scree the whole way over.",
            "Night at Capanna Passo Valles, 2,032m.",
        ],
        "ig_url": "",
    },
    {
        "slug": "run4",
        "part": "The Run · Stage 4",
        "date": "Friday 17 July",
        "date_iso": "2026-07-17",
        "title": "Passo Valles → San Martino",
        "where": "Pale di San Martino",
        "kind": "run",
        "blurb": "The shortest stage, the highest point, and a gondola down to the finish.",
        "stats": [("10.5km", "Distance"), ("+530m", "Ascent"), ("2,804m", "Max altitude")],
        "chain": ["Capanna Passo Valles", "Passo Farangole (2,548m)",
                  "Rifugio Rosetta (2,581m)", "Col Verde gondola ↓", "San Martino"],
        "notes": [
            "Farangole first, then out onto the Rosetta plateau, a white limestone "
            "desert sitting at 2,600m, and the highest ground of the whole trip at 2,804m.",
            "Down on the Col Verde gondola into San Martino di Castrozza. Four days, "
            "four huts, 103km and +4,510m behind us.",
            "Private minibus to Bolzano, about an hour and a quarter. The bikes were "
            "where we left them.",
        ],
        "ig_url": "",
    },
    {
        "slug": "stelvio",
        "part": "The Ride · Stage 1",
        "date": "Saturday 18 – Sunday 19 July",
        "date_iso": "2026-07-18",
        "title": "Bolzano → Stelvio → Bormio",
        "where": "Passo dello Stelvio",
        "kind": "ride",
        "blurb": "Forty-eight hairpins to 2,758m, on legs that had just run for four days.",
        "stats": [("~96km", "Distance"), ("+2,560m", "Ascent"), ("2,758m", "Summit")],
        "chain": ["Bolzano", "train → Merano", "Vinschgau path", "Prato allo Stelvio",
                  "48 hairpins ↑ 2,758m", "Bormio ↓"],
        "notes": [
            "Regional train Bolzano → Merano with the bikes, €7.50, early enough to get "
            "bike spaces. Then the Vinschgau cycle path all the way to Prato allo Stelvio, "
            "which is where the climb actually starts.",
            "Forty-eight numbered hairpins, counting down. Bags went ahead to Bormio with "
            "Bormio Driver.",
            "Sunday was the rest day, with the Mortirolo and Gavia loop on the table for "
            "anyone who wanted 111km more. The thermal baths at Bagni di Bormio were the "
            "other option.",
        ],
        "ig_url": "",
    },
    {
        "slug": "gavia",
        "part": "The Ride · Stage 3",
        "date": "Monday 20 – Tuesday 21 July",
        "date_iso": "2026-07-20",
        "title": "Bormio → Gavia → Lake Como",
        "where": "Passo di Gavia",
        "kind": "ride",
        "blurb": "Narrower, quieter and meaner than the Stelvio. Then a lake, and a day off.",
        "stats": [("~55km", "Riding"), ("+1,400m", "Ascent"), ("2,621m", "Summit")],
        "chain": ["Bormio", "Santa Caterina", "Passo di Gavia (2,621m)", "Ponte di Legno",
                  "Edolo / Tirano", "train → Lake Como"],
        "notes": [
            "The Gavia is half the road and twice the atmosphere of the Stelvio. No "
            "hairpin numbers, no souvenir stands, just a single-track road to 2,621m.",
            "Down to Ponte di Legno, across to Edolo and Tirano, then the train to Como.",
            "Tuesday 21st was the rest day on the lake. Swim, eat, do nothing, before France.",
        ],
        "ig_url": "",
    },
    {
        "slug": "echelle",
        "part": "The Ride · Stage 4",
        "date": "Wednesday 22 July",
        "date_iso": "2026-07-22",
        "title": "Como → Oulx → Briançon",
        "where": "Col de Montgenèvre",
        "kind": "ride",
        "blurb": "A travel day with one alpine col bolted onto the end of it.",
        "stats": [("~35km", "Riding"), ("1,860m", "Montgenèvre"), ("Italy → France", "Border")],
        "chain": ["Ferry ↑ Lake Como", "train → Oulx", "Col de Montgenèvre (1,860m)",
                  "Briançon"],
        "notes": [
            "Ferry up the lake, train across to Oulx, then over the Col de Montgenèvre "
            "and down into Briançon, the highest town in France.",
            "Night at the Logis Hôtel de la Chaussée.",
        ],
        "ig_url": "",
    },
    {
        "slug": "finale",
        "part": "The Ride · Stage 5",
        "date": "Thursday 23 July",
        "date_iso": "2026-07-23",
        "title": "Briançon → Alpe d'Huez",
        "where": "Col du Lautaret",
        "kind": "ride",
        "blurb": "Over the Lautaret, down to Bourg d'Oisans, and stop at the bottom.",
        "stats": [("~50km", "Distance"), ("~+900m", "Ascent"), ("2,058m", "Lautaret")],
        "chain": ["Briançon", "Col du Lautaret (2,058m)", "descent ↓",
                  "Bourg d'Oisans", "watch the Tour"],
        "notes": [
            "La Meije the whole way up the Lautaret, then a long descent to Bourg d'Oisans "
            "at the foot of the twenty-one hairpins.",
            "We finished at the bottom on purpose. The Tour rode the rest of it, and we "
            "watched from the base. Each of those bends is named after someone who won there.",
        ],
        "ig_url": "",
    },
    {
        "slug": "closer",
        "part": "Epilogue",
        "date": "Thursday 23 July",
        "date_iso": "2026-07-23",
        "title": "Earn the view",
        "where": "Bourg d'Oisans",
        "kind": "closer",
        "blurb": "Eleven days, two disciplines, one line drawn across the Alps.",
        "stats": [("339km", "Total distance"), ("+11,960m", "Total ascent"),
                  ("2,804m", "High point")],
        "chain": ["Bressanone", "San Martino", "Bolzano", "Bormio", "Lake Como",
                  "Briançon", "Bourg d'Oisans"],
        "notes": [
            "103km and +4,510m on foot across the Dolomites. 236km and +7,450m on the "
            "road to the French Alps. One continuous line from Bressanone to the bottom "
            "of Alpe d'Huez.",
            "Cohort 01. The trips we wanted to do and couldn't book anywhere.",
        ],
        "ig_url": "",
    },
]
