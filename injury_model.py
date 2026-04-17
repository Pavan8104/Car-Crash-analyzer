from typing import List, Dict, Any

INJURY_META: Dict[str, Dict[str, Any]] = {
    "head trauma":                       {"part": "Head",    "base_pct": 55},
    "head injury":                       {"part": "Head",    "base_pct": 65},
    "chest compression":                 {"part": "Chest",   "base_pct": 60},
    "chest impact":                      {"part": "Chest",   "base_pct": 55},
    "severe chest injury":               {"part": "Chest",   "base_pct": 70},
    "knee impact":                       {"part": "Legs",    "base_pct": 45},
    "bruising":                          {"part": "Body",    "base_pct": 35},
    "minor lacerations":                 {"part": "Skin",    "base_pct": 40},
    "soft tissue strain":                {"part": "Muscle",  "base_pct": 45},
    "sprain":                            {"part": "Joints",  "base_pct": 50},
    "abrasions":                         {"part": "Skin",    "base_pct": 40},
    "neck strain":                       {"part": "Neck",    "base_pct": 65},
    "whiplash":                          {"part": "Neck",    "base_pct": 70},
    "lower back injury":                 {"part": "Spine",   "base_pct": 55},
    "concussion symptoms":               {"part": "Head",    "base_pct": 50},
    "pelvis injury":                     {"part": "Pelvis",  "base_pct": 60},
    "pelvis fracture":                   {"part": "Pelvis",  "base_pct": 50},
    "rib fracture":                      {"part": "Chest",   "base_pct": 55},
    "arm fracture":                      {"part": "Arms",    "base_pct": 45},
    "spinal stress":                     {"part": "Spine",   "base_pct": 60},
    "spinal injury":                     {"part": "Spine",   "base_pct": 45},
    "limb bruising":                     {"part": "Limbs",   "base_pct": 65},
    "disorientation":                    {"part": "Head",    "base_pct": 50},
    "organ damage":                      {"part": "Torso",   "base_pct": 40},
    "ejection risk":                     {"part": "Body",    "base_pct": 55},
    "roof intrusion injury":             {"part": "Head",    "base_pct": 55},
    "mild neck stiffness (WHIPS active)":{"part": "Neck",    "base_pct": 25},
    "battery intrusion risk":            {"part": "Body",    "base_pct": 35},
    "high-voltage system exposure risk": {"part": "Body",    "base_pct": 40},
}


def _enrich(name: str, speed_kmh: float, seatbelt: bool, airbags: bool) -> Dict[str, Any]:
    meta = INJURY_META.get(name, {"part": "Body", "base_pct": 45})
    pct = meta["base_pct"]
    if speed_kmh > 100:
        pct = min(95, pct + 25)
    elif speed_kmh > 60:
        pct = min(90, pct + 15)
    elif speed_kmh > 30:
        pct = min(85, pct + 5)
    if not seatbelt:
        pct = min(95, pct + 10)
    if not airbags:
        pct = min(95, pct + 8)
    return {"name": name, "part": meta["part"], "pct": pct}


def _collision_injury_tokens(collision_type: str) -> List[str]:
    mapping = {
        "frontal": ["head trauma", "chest compression", "knee impact"],
        "rear":    ["neck strain", "whiplash", "lower back injury"],
        "side":    ["pelvis injury", "rib fracture", "arm fracture"],
        "rollover":["head injury", "spinal stress", "limb bruising"],
    }
    return mapping.get(collision_type, ["soft tissue injury"])


def generate_injury_scenarios(
    speed_kmh: float,
    collision_type: str,
    seatbelt: bool,
    airbags: bool,
    risk_level: str = "Low",
    whips: bool = False,
    is_electric: bool = False,
) -> Dict[str, List[Dict[str, Any]]]:
    raw: Dict[str, List[str]] = {"Minor": [], "Moderate": [], "Severe": []}
    tokens = _collision_injury_tokens(collision_type)

    if speed_kmh <= 30:
        raw["Minor"] = [tokens[0], "bruising", "minor lacerations"]
        if not seatbelt:
            raw["Moderate"].append("soft tissue strain")
    elif speed_kmh <= 60:
        raw["Minor"] = [tokens[0], "sprain", "abrasions"]
        raw["Moderate"] = [tokens[1], "concussion symptoms"]
        if not airbags:
            raw["Moderate"].append("chest impact")
        if not seatbelt:
            raw["Severe"].append("head trauma")
    else:
        raw["Moderate"] = [tokens[1], "rib fracture", "disorientation"]
        raw["Severe"] = [tokens[2], "organ damage", "spinal injury"]
        if not seatbelt:
            raw["Severe"].append("ejection risk")
        if not airbags:
            raw["Severe"].append("severe chest injury")

    if collision_type == "side" and speed_kmh > 40:
        raw["Severe"].append("pelvis fracture")
    if collision_type == "rear" and not seatbelt:
        raw["Moderate"].append("whiplash")
    if collision_type == "rollover" and not airbags:
        raw["Severe"].append("roof intrusion injury")

    if whips and collision_type == "rear":
        raw["Severe"] = [i for i in raw["Severe"] if i not in ("neck strain", "whiplash")]
        raw["Moderate"] = [i for i in raw["Moderate"] if i != "whiplash"]
        if speed_kmh > 30:
            raw["Minor"].append("mild neck stiffness (WHIPS active)")

    if is_electric and risk_level == "High":
        if collision_type in ("side", "rollover"):
            raw["Severe"].append("battery intrusion risk")
        raw["Moderate"].append("high-voltage system exposure risk")

    if risk_level == "Low":
        raw["Severe"] = []
        raw["Moderate"] = raw["Moderate"][:1]
    elif risk_level == "Medium":
        raw["Severe"] = raw["Severe"][:1]

    for sev in raw:
        raw[sev] = list(dict.fromkeys(raw[sev]))

    return {
        sev: [_enrich(name, speed_kmh, seatbelt, airbags) for name in names]
        for sev, names in raw.items()
    }


def summarize_injuries(injuries: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    summary = []
    for category in ["Severe", "Moderate", "Minor"]:
        items = injuries.get(category, [])
        if items:
            names = ", ".join(i["name"] if isinstance(i, dict) else i for i in items)
            summary.append(f"{category} injuries: {names}")
    return summary
