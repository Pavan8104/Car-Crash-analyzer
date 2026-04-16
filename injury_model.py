"""Rule-based injury scenario generation based on crash parameters."""

from typing import List, Dict


def _seatbelt_modifier(seatbelt: bool) -> int:
    return 0 if seatbelt else 2


def _airbag_modifier(airbags: bool) -> int:
    return 0 if airbags else 1


def _collision_injury_tokens(collision_type: str) -> List[str]:
    mapping = {
        "frontal": ["head trauma", "chest compression", "knee impact"],
        "rear": ["neck strain", "whiplash", "lower back injury"],
        "side": ["pelvis injury", "rib fracture", "arm fracture"],
        "rollover": ["head injury", "spinal stress", "limb bruising"],
    }
    return mapping.get(collision_type, ["soft tissue injury"])


def generate_injury_scenarios(speed_kmh: float, collision_type: str, seatbelt: bool, airbags: bool) -> Dict[str, List[str]]:
    """Return categorized injury scenarios based on the crash profile."""
    injuries = {
        "Minor": [],
        "Moderate": [],
        "Severe": [],
    }
    collision_tokens = _collision_injury_tokens(collision_type)
    risk_factor = int(speed_kmh / 30) + _seatbelt_modifier(seatbelt) + _airbag_modifier(airbags)

    if speed_kmh <= 30:
        injuries["Minor"] = [collision_tokens[0], "bruising", "minor lacerations"]
        if not seatbelt:
            injuries["Moderate"].append("soft tissue strain")
    elif speed_kmh <= 60:
        injuries["Minor"] = [collision_tokens[0], "sprain", "abrasions"]
        injuries["Moderate"] = [collision_tokens[1], "concussion symptoms"]
        if not airbags:
            injuries["Moderate"].append("chest impact")
        if not seatbelt:
            injuries["Severe"].append("head trauma")
    else:
        injuries["Moderate"] = [collision_tokens[1], "rib fracture", "disorientation"]
        injuries["Severe"] = [collision_tokens[2], "organ damage", "spinal injury"]
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

    for severity in injuries:
        injuries[severity] = list(dict.fromkeys(injuries[severity]))
    return injuries


def summarize_injuries(injuries: Dict[str, List[str]]) -> List[str]:
    """Flatten selected injury list into readable bullets for the report."""
    summary = []
    for category in ["Severe", "Moderate", "Minor"]:
        if injuries.get(category):
            summary.append(f"{category} injuries: {', '.join(injuries[category])}")
    return summary
