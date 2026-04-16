"""Crash physics calculations for a collision analysis system."""

from typing import Dict

# Typical average vehicle mass used for impact calculations (kg)
DEFAULT_VEHICLE_MASS_KG = 1500

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


def calculate_impact_force(speed_kmh: float, collision_type: str, mass_kg: float = DEFAULT_VEHICLE_MASS_KG) -> float:
    """Estimate impact force in kilonewtons based on speed and collision type."""
    speed_m_s = speed_kmh / 3.6
    base_force = mass_kg * speed_m_s / 0.1
    multiplier = COLLISION_FORCE_MULTIPLIER.get(collision_type, 1.0)
    force_newtons = base_force * multiplier
    return round(force_newtons / 1000, 1)


def calculate_impact_energy(speed_kmh: float, collision_type: str, mass_kg: float = DEFAULT_VEHICLE_MASS_KG) -> float:
    """Estimate kinetic energy in kilojoules based on speed and collision type."""
    speed_m_s = speed_kmh / 3.6
    energy_joules = 0.5 * mass_kg * (speed_m_s ** 2)
    multiplier = COLLISION_ENERGY_MULTIPLIER.get(collision_type, 1.0)
    energy_joules *= multiplier
    return round(energy_joules / 1000, 1)


def summarize_physics(speed_kmh: float, collision_type: str) -> Dict[str, float]:
    """Return a dictionary with calculated impact metrics."""
    return {
        "impact_force_kN": calculate_impact_force(speed_kmh, collision_type),
        "impact_energy_kJ": calculate_impact_energy(speed_kmh, collision_type),
    }
