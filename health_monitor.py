from typing import Dict, List
from config import HEALTH_WEIGHTS, SPEED_HIGH

# vehicle health monitor
# scores how safe the car is before/after a crash
# score 0-100, higher = healthier / safer


def _score_ncap(stars) -> float:
    # 5 stars = perfect, 0 stars = very unsafe
    # None means no rating available — treat as average (3 stars)
    if stars is None:
        stars = 3
    return (stars / 5) * 100


def _score_speed_margin(speed_kmh: float, care_key_limit) -> float:
    # how far under the care-key speed limit is the car running
    # if no care-key limit, use global high-speed threshold
    limit = care_key_limit if care_key_limit else SPEED_HIGH
    if speed_kmh <= 0:
        return 100
    if speed_kmh >= limit:
        return 0
    return round(((limit - speed_kmh) / limit) * 100, 1)


def _score_crumple(crumple_time_s: float) -> float:
    # longer crumple time = better energy absorption = safer
    # 0.05s = poor, 0.15s+ = excellent
    if crumple_time_s >= 0.15:
        return 100
    if crumple_time_s <= 0.05:
        return 20
    return round(((crumple_time_s - 0.05) / 0.10) * 80 + 20, 1)


def calculate_health_score(
    ncap_stars: int,
    seatbelt: bool,
    airbags: bool,
    speed_kmh: float,
    crumple_time_s: float,
    care_key_limit=None,
) -> Dict:
    """
    Returns an overall vehicle safety health score 0-100
    and a breakdown of each component.
    """
    components = {
        "ncap_stars":      _score_ncap(ncap_stars),
        "airbag_ok":       100 if airbags  else 0,
        "crumple_quality": _score_crumple(crumple_time_s),
        "belt_status":     100 if seatbelt else 0,
        "speed_margin":    _score_speed_margin(speed_kmh, care_key_limit),
    }

    # weighted average using weights from config
    total = sum(
        components[k] * HEALTH_WEIGHTS[k]
        for k in HEALTH_WEIGHTS
    )
    overall = round(total, 1)

    return {
        "overall":    overall,
        "label":      _health_label(overall),
        "color":      _health_color(overall),
        "components": components,
        "alerts":     _health_alerts(components, speed_kmh, care_key_limit),
    }


def _health_label(score: float) -> str:
    if score >= 80:
        return "Good"
    if score >= 55:
        return "Fair"
    if score >= 30:
        return "Poor"
    return "Critical"


def _health_color(score: float) -> str:
    # returns css variable name so frontend can colour the badge
    if score >= 80:
        return "success"
    if score >= 55:
        return "warning"
    return "danger"


def _health_alerts(components: Dict, speed_kmh: float, care_key_limit) -> List[str]:
    # plain-language warnings for anything below a safe threshold
    alerts = []

    if components["airbag_ok"] == 0:
        alerts.append("Airbag system not active — get a workshop inspection before next drive.")

    if components["belt_status"] == 0:
        alerts.append("Seatbelt not worn — risk of ejection and fatal injury is very high.")

    if components["ncap_stars"] < 60:
        alerts.append("Low NCAP safety rating — consider upgrading to a 5-star rated vehicle.")

    if components["speed_margin"] == 0:
        limit = care_key_limit if care_key_limit else SPEED_HIGH
        alerts.append(f"Speed ({int(speed_kmh)} km/h) is at or above safe limit ({int(limit)} km/h).")

    if components["crumple_quality"] < 50:
        alerts.append("Older crumple zone design — impact energy absorption is below modern standards.")

    return alerts
