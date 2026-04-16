"""Utility helpers for validation, formatting, and logging."""

import json
import logging
from typing import Dict

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("crash_analysis")

VALID_COLLISION_TYPES = ["frontal", "rear", "side", "rollover"]


def validate_inputs(speed_kmh: float, collision_type: str, seatbelt: bool, airbags: bool) -> None:
    if speed_kmh < 0 or speed_kmh > 250:
        raise ValueError("Speed must be a number between 0 and 250 km/h.")
    if collision_type not in VALID_COLLISION_TYPES:
        raise ValueError(f"Collision type must be one of: {', '.join(VALID_COLLISION_TYPES)}.")
    if not isinstance(seatbelt, bool) or not isinstance(airbags, bool):
        raise ValueError("Seatbelt and airbags must be boolean values.")


def print_report(report: Dict, output_json: bool = False) -> None:
    if output_json:
        print(json.dumps(report, indent=2))
        return

    summary = report.get("summary", report)
    risk_level = summary.get("risk_level")
    impact_force = summary.get("impact_force_kN")
    impact_energy = summary.get("impact_energy_kJ")

    print("Crash Analysis Report")
    print("----------------------")
    print(f"Risk level: {risk_level}")
    print(f"Impact force: {impact_force} kN")
    print(f"Impact energy: {impact_energy} kJ")
    print("\nInjury scenarios:")
    for category, injuries in report.get("injuries", {}).items():
        if injuries:
            print(f"  {category}:")
            for injury in injuries:
                print(f"   - {injury}")
    print("\nSafety suggestions:")
    for suggestion in report.get("safety_suggestions", []):
        print(f" - {suggestion}")
