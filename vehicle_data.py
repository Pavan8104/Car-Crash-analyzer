VOLVO_MODELS = {
    "XC90": {
        "mass_kg": 2100,
        "crumple_time_s": 0.16,
        "safety_bonus": 2,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Pilot Assist",
            "Run-off Road Protection",
            "Cross Traffic Alert",
        ],
    },
    "XC60": {
        "mass_kg": 1950,
        "crumple_time_s": 0.15,
        "safety_bonus": 2,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Pilot Assist",
            "Oncoming Lane Mitigation",
            "Cross Traffic Alert",
        ],
    },
    "XC40": {
        "mass_kg": 1725,
        "crumple_time_s": 0.14,
        "safety_bonus": 1,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Run-off Road Protection",
            "Cross Traffic Alert",
        ],
    },
    "S90": {
        "mass_kg": 1850,
        "crumple_time_s": 0.15,
        "safety_bonus": 2,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Pilot Assist",
            "Large Animal Detection",
            "Cross Traffic Alert",
        ],
    },
    "S60": {
        "mass_kg": 1590,
        "crumple_time_s": 0.14,
        "safety_bonus": 1,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Pilot Assist",
            "Lane Keeping Aid",
        ],
    },
    "V60": {
        "mass_kg": 1650,
        "crumple_time_s": 0.14,
        "safety_bonus": 1,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Lane Keeping Aid",
            "Cross Traffic Alert",
        ],
    },
    "EX90": {
        "mass_kg": 2736,
        "crumple_time_s": 0.17,
        "safety_bonus": 3,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Pilot Assist",
            "360-degree Radar",
            "Driver Understanding System",
            "Cross Traffic Alert",
        ],
    },
    "C40": {
        "mass_kg": 1800,
        "crumple_time_s": 0.14,
        "safety_bonus": 1,
        "ncap_stars": 5,
        "features": [
            "City Safety",
            "Blind Spot Information (BLIS)",
            "Cross Traffic Alert",
            "Lane Keeping Aid",
        ],
    },
}

GENERIC_VEHICLE = {
    "mass_kg": 1500,
    "crumple_time_s": 0.10,
    "safety_bonus": 0,
    "ncap_stars": None,
    "features": [],
}


def get_vehicle(model: str) -> dict:
    return VOLVO_MODELS.get(model, GENERIC_VEHICLE)
