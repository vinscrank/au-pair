DUTIES = [
    ("childcare", "Childcare"),
    ("school_runs", "School runs"),
    ("light_housework", "Light housework"),
    ("cooking", "Cooking and meals"),
    ("homework", "Homework help"),
    ("bedtime", "Bedtime routine"),
    ("evening_babysitting", "Evening babysitting"),
    ("laundry", "Laundry"),
    ("pet_care", "Pet care"),
]

AGE_BANDS = [
    ("newborn", "Newborn"),
    ("0_6_months", "0–6 months"),
    ("6_months_2", "6 months–2 years"),
    ("2_5", "2–5 years"),
    ("5_plus", "5 years and over"),
    ("teenagers", "Teenagers"),
]

CARE_WINDOWS = [
    ("mornings", "Mornings"),
    ("school_hours", "School hours"),
    ("afternoons", "Afternoons"),
    ("evenings", "Evenings"),
    ("weekends", "Weekends"),
    ("overnights", "Overnights"),
]

DAYS = [
    ("monday", "Mon"),
    ("tuesday", "Tue"),
    ("wednesday", "Wed"),
    ("thursday", "Thu"),
    ("friday", "Fri"),
    ("saturday", "Sat"),
    ("sunday", "Sun"),
]

MINDS_IN = [
    ("family_home", "In the family's home"),
    ("own_home", "In my home"),
]

ARRANGEMENTS = [
    ("live_in", "Live-in"),
    ("live_out", "Live-out"),
    ("either", "Live-in or live-out"),
]

START_TIMINGS = [
    ("asap", "As soon as possible"),
    ("few_weeks", "Within a few weeks"),
    ("exploring", "Just exploring options"),
]

PAY_BASIS = [
    ("weekly", "Weekly pocket money"),
    ("hourly", "Hourly"),
    ("monthly", "Monthly"),
]

GENDERS = [
    ("woman", "Woman"),
    ("man", "Man"),
    ("non_binary", "Non-binary"),
    ("prefer_not_to_say", "Prefer not to say"),
]

LEVELS = [
    ("native", "Native"),
    ("fluent", "Fluent"),
    ("intermediate", "Intermediate"),
    ("basic", "Basic"),
]

HOUSEHOLDS = [
    ("two_parents", "Two parents"),
    ("one_parent", "One parent"),
    ("guardian", "Guardian"),
]

LANGUAGES = [
    "English",
    "Irish",
    "Spanish",
    "Italian",
    "French",
    "German",
    "Portuguese",
    "Polish",
    "Romanian",
    "Lithuanian",
    "Latvian",
    "Russian",
    "Ukrainian",
    "Arabic",
    "Chinese",
    "Hindi",
    "Dutch",
    "Swedish",
    "Czech",
    "Hungarian",
]

AREA_GROUPS = [
    (
        "City centre and the canals",
        [
            "Dublin 1",
            "Dublin 2",
            "Dublin 4",
            "Dublin 6",
            "Dublin 6W",
            "Dublin 7",
            "Dublin 8",
            "Ballsbridge",
            "Rathmines",
            "Ranelagh",
            "Portobello",
            "Grand Canal Dock",
            "Sandymount",
            "Stoneybatter",
            "Smithfield",
            "Kilmainham",
            "Inchicore",
        ],
    ),
    (
        "Southside",
        [
            "Rathgar",
            "Rathfarnham",
            "Terenure",
            "Harold's Cross",
            "Donnybrook",
            "Milltown",
            "Dundrum",
            "Stillorgan",
            "Sandyford",
            "Leopardstown",
            "Blackrock",
            "Booterstown",
            "Dun Laoghaire",
            "Sandycove",
            "Dalkey",
            "Killiney",
            "Cherrywood",
            "Dublin 14",
            "Dublin 16",
            "Dublin 18",
        ],
    ),
    (
        "Northside",
        [
            "Drumcondra",
            "Phibsborough",
            "Glasnevin",
            "Cabra",
            "Dublin 3",
            "Dublin 9",
            "Clontarf",
            "Killester",
            "Raheny",
            "Sutton",
            "Howth",
            "Malahide",
            "Portmarnock",
            "Swords",
        ],
    ),
    (
        "West Dublin and commuter towns",
        [
            "Dublin 15",
            "Blanchardstown",
            "Castleknock",
            "Ashtown",
            "Lucan",
            "Clondalkin",
            "Tallaght",
            "Dublin 12",
            "Bray",
            "Greystones",
        ],
    ),
]


def pairs(items: list[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"value": value, "label": label} for value, label in items]


def labels(items: list[tuple[str, str]]) -> dict[str, str]:
    return {value: label for value, label in items}


def values(items: list[tuple[str, str]]) -> set[str]:
    return {value for value, _label in items}


DUTY_VALUES = values(DUTIES)
AGE_BAND_VALUES = values(AGE_BANDS)
CARE_WINDOW_VALUES = values(CARE_WINDOWS)
DAY_VALUES = values(DAYS)
MIND_VALUES = values(MINDS_IN)
ARRANGEMENT_VALUES = values(ARRANGEMENTS)
START_VALUES = values(START_TIMINGS)
PAY_VALUES = values(PAY_BASIS)
GENDER_VALUES = values(GENDERS)
LEVEL_VALUES = values(LEVELS)
HOUSEHOLD_VALUES = values(HOUSEHOLDS)
LANGUAGE_VALUES = set(LANGUAGES)
AREA_VALUES = {name for _group, names in AREA_GROUPS for name in names}

DUTY_LABELS = labels(DUTIES)
AGE_BAND_LABELS = labels(AGE_BANDS)
CARE_WINDOW_LABELS = labels(CARE_WINDOWS)
DAY_LABELS = labels(DAYS)
MIND_LABELS = labels(MINDS_IN)
ARRANGEMENT_LABELS = labels(ARRANGEMENTS)
START_LABELS = labels(START_TIMINGS)
PAY_LABELS = labels(PAY_BASIS)
GENDER_LABELS = labels(GENDERS)
LEVEL_LABELS = labels(LEVELS)
HOUSEHOLD_LABELS = labels(HOUSEHOLDS)


def meta() -> dict:
    return {
        "areas": [
            {"group": group, "options": [{"value": name, "label": name} for name in names]}
            for group, names in AREA_GROUPS
        ],
        "duties": pairs(DUTIES),
        "age_bands": pairs(AGE_BANDS),
        "care_windows": pairs(CARE_WINDOWS),
        "days": pairs(DAYS),
        "minds_in": pairs(MINDS_IN),
        "arrangements": pairs(ARRANGEMENTS),
        "start_timings": pairs(START_TIMINGS),
        "pay_basis": pairs(PAY_BASIS),
        "genders": pairs(GENDERS),
        "levels": pairs(LEVELS),
        "languages": [{"value": name, "label": name} for name in LANGUAGES],
        "households": pairs(HOUSEHOLDS),
    }
