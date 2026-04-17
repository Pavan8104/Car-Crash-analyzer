"""Predict injury risk and safety recommendations from crash inputs."""

from typing import Dict, List


def determine_risk_level(
    speed_kmh: float,
    collision_type: str,
    seatbelt: bool,
    airbags: bool,
    safety_bonus: int = 0,
) -> str:
    score = 0
    score += 2 if speed_kmh >= 60 else 1 if speed_kmh >= 30 else 0
    score += 2 if collision_type == "side" else 1 if collision_type == "rollover" else 0
    score += 1 if not seatbelt else 0
    score += 1 if not airbags else 0
    # vehicle safety systems (City Safety, BLIS, etc.) lower effective risk
    score = max(0, score - safety_bonus)

    if score >= 5:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def safety_suggestions(risk_level: str, seatbelt: bool, airbags: bool) -> List[str]:
    suggestions = []
    if not seatbelt:
        suggestions.append("Always wear a seatbelt to reduce ejection and head injury risk.")
    if not airbags:
        suggestions.append("Install or maintain airbags to protect the chest and head.")
    if risk_level == "High":
        suggestions.append("Seek immediate medical evaluation after a crash.")
    if risk_level in ["Medium", "High"]:
        suggestions.append("Check vehicle deformation and report pain in neck, chest, or abdomen.")
    if risk_level == "Low":
        suggestions.append("Monitor for delayed symptoms and get a professional inspection.")
    return suggestions


def format_report(payload: Dict) -> Dict:
    return {
        "summary": {
            "risk_level": payload["risk_level"],
            "impact_force_kN": payload["impact_force_kN"],
            "impact_energy_kJ": payload["impact_energy_kJ"],
        },
        "vehicle": payload.get("vehicle", {}),
        "injuries": payload["injuries"],
        "safety_suggestions": payload["safety_suggestions"],
    }
