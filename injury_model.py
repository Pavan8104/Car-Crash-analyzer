from typing import List, Dict


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
) -> Dict[str, List[str]]:
    injuries: Dict[str, List[str]] = {"Minor": [], "Moderate": [], "Severe": []}
    tokens = _collision_injury_tokens(collision_type)

    if speed_kmh <= 30:
        injuries["Minor"] = [tokens[0], "bruising", "minor lacerations"]
        if not seatbelt:
            injuries["Moderate"].append("soft tissue strain")
    elif speed_kmh <= 60:
        injuries["Minor"] = [tokens[0], "sprain", "abrasions"]
        injuries["Moderate"] = [tokens[1], "concussion symptoms"]
        if not airbags:
            injuries["Moderate"].append("chest impact")
        if not seatbelt:
            injuries["Severe"].append("head trauma")
    else:
        injuries["Moderate"] = [tokens[1], "rib fracture", "disorientation"]
        injuries["Severe"] = [tokens[2], "organ damage", "spinal injury"]
        if not seatbelt:
            injuries["Severe"].append("ejection risk")
        if not airbags:
            injuries["Severe"].append("severe chest injury")

    if collision_type == "side" and speed_kmh > 40:
        injuries["Severe"].append("pelvis fracture")
    if collision_type == "rear" and not seatbelt:
        injuries["Moderate"].append("whiplash")
    if collision_type == "rollover" and not airbags:
        injuries["Severe"].append("roof intrusion injury")

    # WHIPS reduces rear-collision neck and whiplash severity
    if whips and collision_type == "rear":
        injuries["Severe"] = [i for i in injuries["Severe"] if i not in ("neck strain", "whiplash")]
        injuries["Moderate"] = [i for i in injuries["Moderate"] if i != "whiplash"]
        if speed_kmh > 30:
            injuries["Minor"].append("mild neck stiffness (WHIPS active)")

    # EV-specific: battery intrusion risk on severe side/rollover crashes
    if is_electric and risk_level == "High":
        if collision_type in ("side", "rollover"):
            injuries["Severe"].append("battery intrusion risk")
        injuries["Moderate"].append("high-voltage system exposure risk")

    # cap severity to match risk level
    if risk_level == "Low":
        injuries["Severe"] = []
        injuries["Moderate"] = injuries["Moderate"][:1]
    elif risk_level == "Medium":
        injuries["Severe"] = injuries["Severe"][:1]

    for severity in injuries:
        injuries[severity] = list(dict.fromkeys(injuries[severity]))
    return injuries


def summarize_injuries(injuries: Dict[str, List[str]]) -> List[str]:
    summary = []
    for category in ["Severe", "Moderate", "Minor"]:
        if injuries.get(category):
            summary.append(f"{category} injuries: {', '.join(injuries[category])}")
    return summary
