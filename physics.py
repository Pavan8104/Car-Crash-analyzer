from typing import Dict

DEFAULT_MASS_KG = 1500
DEFAULT_CRUMPLE_TIME_S = 0.10

COLLISION_FORCE_MULTIPLIER = {
    "frontal": 1.0,
    "rear": 0.8,
    "side": 1.2,
    "rollover": 1.4,
}

COLLISION_ENERGY_MULTIPLIER = {
    "frontal": 1.0,
    "rear": 0.9,
    "side": 1.15,
    "rollover": 1.3,
}


def calculate_impact_force(
    speed_kmh: float,
    collision_type: str,
    mass_kg: float = DEFAULT_MASS_KG,
    crumple_time_s: float = DEFAULT_CRUMPLE_TIME_S,
) -> float:
    speed_m_s = speed_kmh / 3.6
    # longer crumple time = force spread over more time = lower peak force
    base_force = mass_kg * speed_m_s / crumple_time_s
    multiplier = COLLISION_FORCE_MULTIPLIER.get(collision_type, 1.0)
    return round((base_force * multiplier) / 1000, 1)


def calculate_impact_energy(
    speed_kmh: float,
    collision_type: str,
    mass_kg: float = DEFAULT_MASS_KG,
) -> float:
    speed_m_s = speed_kmh / 3.6
    energy_j = 0.5 * mass_kg * (speed_m_s ** 2)
    multiplier = COLLISION_ENERGY_MULTIPLIER.get(collision_type, 1.0)
    return round((energy_j * multiplier) / 1000, 1)


def summarize_physics(
    speed_kmh: float,
    collision_type: str,
    mass_kg: float = DEFAULT_MASS_KG,
    crumple_time_s: float = DEFAULT_CRUMPLE_TIME_S,
) -> Dict[str, float]:
    return {
        "impact_force_kN": calculate_impact_force(speed_kmh, collision_type, mass_kg, crumple_time_s),
        "impact_energy_kJ": calculate_impact_energy(speed_kmh, collision_type, mass_kg),
    }
