"""Command-line entrypoint for the Crash Analysis & Injury Prediction System."""

import argparse
import logging
from physics import summarize_physics
from predictor import determine_risk_level, safety_suggestions, format_report
from injury_model import generate_injury_scenarios
from utils import validate_inputs, print_report, logger


def analyze_crash(speed_kmh: float, collision_type: str, seatbelt: bool, airbags: bool) -> dict:
    validate_inputs(speed_kmh, collision_type, seatbelt, airbags)
    logger.info("Starting crash analysis")

    physics = summarize_physics(speed_kmh, collision_type)
    risk_level = determine_risk_level(speed_kmh, collision_type, seatbelt, airbags)
    injuries = generate_injury_scenarios(speed_kmh, collision_type, seatbelt, airbags)
    suggestions = safety_suggestions(risk_level, seatbelt, airbags)

    report = {
        "speed_kmh": speed_kmh,
        "collision_type": collision_type,
        "seatbelt": seatbelt,
        "airbags": airbags,
        "impact_force_kN": physics["impact_force_kN"],
        "impact_energy_kJ": physics["impact_energy_kJ"],
        "risk_level": risk_level,
        "injuries": injuries,
        "safety_suggestions": suggestions,
    }
    logger.info("Crash analysis complete")
    return format_report(report)


run_analysis = analyze_crash


def parse_args():
    parser = argparse.ArgumentParser(description="Crash Analysis & Injury Prediction System")
    parser.add_argument("--speed", type=float, default=50.0, help="Vehicle speed in km/h")
    parser.add_argument("--collision", type=str, default="frontal", choices=["frontal", "rear", "side", "rollover"], help="Type of collision")
    parser.add_argument("--seatbelt", action="store_true", help="Passenger is wearing a seatbelt")
    parser.add_argument("--airbags", action="store_true", help="Vehicle is equipped with airbags")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        report = analyze_crash(args.speed, args.collision, args.seatbelt, args.airbags)
        print_report({**report, "risk_level": report["summary"]["risk_level"], "injuries": report["injuries"], "safety_suggestions": report["safety_suggestions"]}, output_json=args.json)
    except ValueError as exc:
        logger.error("Input validation failed: %s", exc)
        print(f"Error: {exc}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
