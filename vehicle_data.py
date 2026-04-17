from typing import Dict, List, Optional

VOLVO_MODELS: Dict[str, Dict] = {
    "XC90": {
        "generations": {
            "2nd Gen (2015–present)": {
                "mass_kg": 2100,
                "crumple_time_s": 0.16,
                "safety_bonus": 2,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": True,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": False,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Pilot Assist",
                    "Run-off Road Protection",
                    "Cross Traffic Alert",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                    "WHIPS (Whiplash Protection)",
                ],
            },
            "1st Gen (2002–2014)": {
                "mass_kg": 2050,
                "crumple_time_s": 0.12,
                "safety_bonus": 0,
                "ncap_stars": 4,
                "post_crash_brake": False,
                "whips": True,
                "on_call": False,
                "care_key_speed_limit": None,
                "is_electric": False,
                "features": [
                    "WHIPS (Whiplash Protection)",
                    "Side Curtain Airbags",
                    "Roll Stability Control (RSC)",
                    "DSTC (Dynamic Stability)",
                ],
            },
        }
    },
    "XC60": {
        "generations": {
            "2nd Gen (2017–present)": {
                "mass_kg": 1950,
                "crumple_time_s": 0.15,
                "safety_bonus": 2,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": True,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": False,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Pilot Assist",
                    "Oncoming Lane Mitigation",
                    "Cross Traffic Alert",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                    "WHIPS (Whiplash Protection)",
                ],
            },
            "1st Gen (2008–2016)": {
                "mass_kg": 1800,
                "crumple_time_s": 0.12,
                "safety_bonus": 1,
                "ncap_stars": 5,
                "post_crash_brake": False,
                "whips": True,
                "on_call": False,
                "care_key_speed_limit": None,
                "is_electric": False,
                "features": [
                    "City Safety (low-speed, <50 km/h)",
                    "WHIPS (Whiplash Protection)",
                    "Lane Keeping Aid",
                    "Side Curtain Airbags",
                ],
            },
        }
    },
    "XC40": {
        "generations": {
            "1st Gen (2017–present)": {
                "mass_kg": 1725,
                "crumple_time_s": 0.14,
                "safety_bonus": 1,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": False,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": False,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Run-off Road Protection",
                    "Cross Traffic Alert",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                ],
            },
        }
    },
    "S90": {
        "generations": {
            "Current Gen (2016–present)": {
                "mass_kg": 1850,
                "crumple_time_s": 0.15,
                "safety_bonus": 2,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": True,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": False,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Pilot Assist",
                    "Large Animal Detection",
                    "Cross Traffic Alert",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                    "WHIPS (Whiplash Protection)",
                ],
            },
        }
    },
    "S60": {
        "generations": {
            "3rd Gen (2018–present)": {
                "mass_kg": 1590,
                "crumple_time_s": 0.14,
                "safety_bonus": 2,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": True,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": False,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Pilot Assist",
                    "Lane Keeping Aid",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                    "WHIPS (Whiplash Protection)",
                ],
            },
            "2nd Gen (2010–2018)": {
                "mass_kg": 1550,
                "crumple_time_s": 0.12,
                "safety_bonus": 1,
                "ncap_stars": 5,
                "post_crash_brake": False,
                "whips": True,
                "on_call": False,
                "care_key_speed_limit": None,
                "is_electric": False,
                "features": [
                    "City Safety (low-speed, <50 km/h)",
                    "WHIPS (Whiplash Protection)",
                    "Lane Keeping Aid",
                    "Side Curtain Airbags",
                ],
            },
            "1st Gen (2000–2009)": {
                "mass_kg": 1460,
                "crumple_time_s": 0.10,
                "safety_bonus": 0,
                "ncap_stars": 4,
                "post_crash_brake": False,
                "whips": True,
                "on_call": False,
                "care_key_speed_limit": None,
                "is_electric": False,
                "features": [
                    "WHIPS (Whiplash Protection)",
                    "Front & Side Airbags",
                    "ABS + EBD",
                ],
            },
        }
    },
    "V60": {
        "generations": {
            "2nd Gen (2018–present)": {
                "mass_kg": 1650,
                "crumple_time_s": 0.14,
                "safety_bonus": 2,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": True,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": False,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Lane Keeping Aid",
                    "Cross Traffic Alert",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                    "WHIPS (Whiplash Protection)",
                ],
            },
            "1st Gen (2010–2018)": {
                "mass_kg": 1600,
                "crumple_time_s": 0.12,
                "safety_bonus": 1,
                "ncap_stars": 5,
                "post_crash_brake": False,
                "whips": True,
                "on_call": False,
                "care_key_speed_limit": None,
                "is_electric": False,
                "features": [
                    "City Safety (low-speed, <50 km/h)",
                    "WHIPS (Whiplash Protection)",
                    "Lane Keeping Aid",
                    "Side Curtain Airbags",
                ],
            },
        }
    },
    "EX90": {
        "generations": {
            "1st Gen (2024–present)": {
                "mass_kg": 2736,
                "crumple_time_s": 0.17,
                "safety_bonus": 3,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": True,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": True,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Pilot Assist",
                    "360-degree Radar",
                    "Driver Understanding System",
                    "Cross Traffic Alert",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                    "WHIPS (Whiplash Protection)",
                    "EV Battery Protection System",
                ],
            },
        }
    },
    "C40": {
        "generations": {
            "1st Gen (2021–present)": {
                "mass_kg": 1800,
                "crumple_time_s": 0.14,
                "safety_bonus": 1,
                "ncap_stars": 5,
                "post_crash_brake": True,
                "whips": False,
                "on_call": True,
                "care_key_speed_limit": 130,
                "is_electric": True,
                "features": [
                    "City Safety",
                    "Blind Spot Information (BLIS)",
                    "Cross Traffic Alert",
                    "Lane Keeping Aid",
                    "Post-Crash Brake",
                    "Volvo On Call",
                    "Care Key (130 km/h limit)",
                    "EV Battery Protection System",
                ],
            },
        }
    },
}

GENERIC_VEHICLE = {
    "mass_kg": 1500,
    "crumple_time_s": 0.10,
    "safety_bonus": 0,
    "ncap_stars": None,
    "post_crash_brake": False,
    "whips": False,
    "on_call": False,
    "care_key_speed_limit": None,
    "is_electric": False,
    "features": [],
}


def get_generations(model: str) -> List[str]:
    """Return ordered list of generation labels for a given model."""
    model_data = VOLVO_MODELS.get(model)
    if not model_data:
        return []
    return list(model_data["generations"].keys())


def get_vehicle(model: str, generation: str = "") -> dict:
    model_data = VOLVO_MODELS.get(model)
    if not model_data:
        return GENERIC_VEHICLE
    gens = model_data["generations"]
    if generation and generation in gens:
        return gens[generation]
    # default to first (newest) generation
    return next(iter(gens.values()))


def get_all_frontend_data() -> dict:
    """Return structured data for the frontend JS — models, generations, specs."""
    result = {}
    for model, data in VOLVO_MODELS.items():
        result[model] = {}
        for gen_label, specs in data["generations"].items():
            result[model][gen_label] = {
                "mass_kg": specs["mass_kg"],
                "ncap_stars": specs["ncap_stars"],
                "features": specs["features"],
                "care_key_speed_limit": specs["care_key_speed_limit"],
                "is_electric": specs["is_electric"],
                "post_crash_brake": specs["post_crash_brake"],
                "whips": specs["whips"],
                "on_call": specs["on_call"],
            }
    return result
