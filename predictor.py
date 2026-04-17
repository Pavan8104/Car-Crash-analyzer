from typing import Dict, List, Optional


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
    score = max(0, score - safety_bonus)

    if score >= 5:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


def safety_suggestions(
    risk_level: str,
    seatbelt: bool,
    airbags: bool,
    on_call: bool = False,
    post_crash_brake: bool = False,
    care_key_speed_limit: Optional[int] = None,
    speed_kmh: float = 0,
    is_electric: bool = False,
) -> List[str]:
    suggestions = []

    if not seatbelt:
        suggestions.append("Seatbelt was not worn — ejection and head injury risk is significantly higher.")
    if not airbags:
        suggestions.append("No airbags detected — ensure the vehicle's airbag system is serviced.")

    # Volvo On Call replaces generic "call emergency services"
    if risk_level == "High":
        if on_call:
            suggestions.append("Volvo On Call has automatically alerted emergency services. Stay calm, stay in the vehicle if safe.")
        else:
            suggestions.append("Call emergency services immediately. Do not move the casualty unless there is immediate danger.")

    if risk_level in ("Medium", "High"):
        suggestions.append("Check for deformation around doors and pillars. Report any pain in neck, chest, or abdomen.")

    if risk_level == "Low":
        suggestions.append("Monitor for delayed symptoms over the next 24–48 hours. Get a workshop inspection.")

    # Post-Crash Brake note
    if post_crash_brake:
        suggestions.append("Post-Crash Brake is active — the vehicle has automatically applied brakes to prevent secondary collisions.")

    # Care Key overspeed warning
    if care_key_speed_limit and speed_kmh > care_key_speed_limit:
        suggestions.append(
            f"Speed ({int(speed_kmh)} km/h) exceeded this model's Care Key limit ({care_key_speed_limit} km/h). "
            "Use Care Key to enforce speed limits for young or inexperienced drivers."
        )

    # EV-specific
    if is_electric:
        if risk_level in ("Medium", "High"):
            suggestions.append("Do not touch exposed wiring or the underfloor battery pack. Wait for emergency responders trained in EV safety.")
        suggestions.append("Inform emergency services this is an electric vehicle — high-voltage systems require specific handling.")

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
        "warnings": payload.get("warnings", []),
    }
