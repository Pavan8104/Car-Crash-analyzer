from typing import Dict
from config import KMH_TO_MS, GRAVITY_MS2, GFORCE_MINOR, GFORCE_MODERATE, GFORCE_SEVERE, GFORCE_FATAL_RISK

DEFAULT_MASS_KG       = 1500
DEFAULT_CRUMPLE_TIME_S = 0.10

# side and rollover transfer more energy to occupants
# because there is less crumple zone on those sides
COLLISION_FORCE_MULTIPLIER = {
    "frontal": 1.0,
    "rear":    0.8,
    "side":    1.2,
    "rollover":1.4,
}

COLLISION_ENERGY_MULTIPLIER = {
    "frontal": 1.0,
    "rear":    0.9,
    "side":    1.15,
    "rollover":1.3,
}


def calculate_impact_force(
    speed_kmh: float,
    collision_type: str,
    mass_kg: float = DEFAULT_MASS_KG,
    crumple_time_s: float = DEFAULT_CRUMPLE_TIME_S,
) -> float:
    # F = m * v / t  (impulse-momentum theorem)
    # longer crumple time spreads the force → lower peak
    speed_ms = speed_kmh * KMH_TO_MS
    base_force = mass_kg * speed_ms / crumple_time_s
    multiplier = COLLISION_FORCE_MULTIPLIER.get(collision_type, 1.0)
    return round((base_force * multiplier) / 1000, 1)  # return in kN


def calculate_impact_energy(
    speed_kmh: float,
    collision_type: str,
    mass_kg: float = DEFAULT_MASS_KG,
) -> float:
    # KE = 0.5 * m * v^2
    speed_ms = speed_kmh * KMH_TO_MS
    energy_j = 0.5 * mass_kg * (speed_ms ** 2)
    multiplier = COLLISION_ENERGY_MULTIPLIER.get(collision_type, 1.0)
    return round((energy_j * multiplier) / 1000, 1)  # return in kJ


def calculate_gforce(
    speed_kmh: float,
    crumple_time_s: float = DEFAULT_CRUMPLE_TIME_S,
) -> float:
    # deceleration in m/s^2, then convert to G
    # G = deceleration / 9.81
    speed_ms = speed_kmh * KMH_TO_MS
    deceleration = speed_ms / crumple_time_s
    return round(deceleration / GRAVITY_MS2, 1)


def calculate_stopping_distance(speed_kmh: float) -> float:
    # approximate stopping distance in metres
    # uses standard formula: d = v^2 / (2 * deceleration)
    # assumes 8 m/s^2 average deceleration (normal braking)
    speed_ms = speed_kmh * KMH_TO_MS
    return round((speed_ms ** 2) / (2 * 8), 1)


def gforce_label(gforce: float) -> str:
    # plain text label for the G-force value
    if gforce >= GFORCE_FATAL_RISK:
        return "Fatal Risk Zone"
    if gforce >= GFORCE_SEVERE:
        return "Life-Threatening"
    if gforce >= GFORCE_MODERATE:
        return "Severe Injury Risk"
    if gforce >= GFORCE_MINOR:
        return "Minor Injury Risk"
    return "Low Risk"


def summarize_physics(
    speed_kmh: float,
    collision_type: str,
    mass_kg: float = DEFAULT_MASS_KG,
    crumple_time_s: float = DEFAULT_CRUMPLE_TIME_S,
) -> Dict:
    gf = calculate_gforce(speed_kmh, crumple_time_s)
    return {
        "impact_force_kN":      calculate_impact_force(speed_kmh, collision_type, mass_kg, crumple_time_s),
        "impact_energy_kJ":     calculate_impact_energy(speed_kmh, collision_type, mass_kg),
        "gforce":               gf,
        "gforce_label":         gforce_label(gf),
        "stopping_distance_m":  calculate_stopping_distance(speed_kmh),
    }
