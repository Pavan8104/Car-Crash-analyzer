import argparse
from physics import summarize_physics
from predictor import determine_risk_level, safety_suggestions, format_report
from injury_model import generate_injury_scenarios
from vehicle_data import get_vehicle, VOLVO_MODELS
from health_monitor import calculate_health_score
from utils import validate_inputs, print_report, logger


def analyze_crash(
    speed_kmh: float,
    collision_type: str,
    seatbelt: bool,
    airbags: bool,
    vehicle_model: str = "",
    generation: str = "",
) -> dict:
    validate_inputs(speed_kmh, collision_type, seatbelt, airbags)
    logger.info("Starting crash analysis")

    vehicle = get_vehicle(vehicle_model, generation)

    physics = summarize_physics(
        speed_kmh, collision_type,
        vehicle["mass_kg"], vehicle["crumple_time_s"],
    )
    risk_level = determine_risk_level(
        speed_kmh, collision_type, seatbelt, airbags,
        vehicle["safety_bonus"],
    )
    injuries = generate_injury_scenarios(
        speed_kmh, collision_type, seatbelt, airbags,
        risk_level,
        whips=vehicle["whips"],
        is_electric=vehicle["is_electric"],
    )
    suggestions = safety_suggestions(
        risk_level, seatbelt, airbags,
        on_call=vehicle["on_call"],
        post_crash_brake=vehicle["post_crash_brake"],
        care_key_speed_limit=vehicle["care_key_speed_limit"],
        speed_kmh=speed_kmh,
        is_electric=vehicle["is_electric"],
    )

    # Care Key overspeed warning surfaced separately in UI
    warnings = []
    if vehicle["care_key_speed_limit"] and speed_kmh > vehicle["care_key_speed_limit"]:
        warnings.append(
            f"Speed exceeds Care Key limit ({vehicle['care_key_speed_limit']} km/h). "
            "This scenario is outside Volvo's recommended safety envelope."
        )

    # calculate vehicle health score
    health = calculate_health_score(
        ncap_stars=vehicle["ncap_stars"],
        seatbelt=seatbelt,
        airbags=airbags,
        speed_kmh=speed_kmh,
        crumple_time_s=vehicle["crumple_time_s"],
        care_key_limit=vehicle["care_key_speed_limit"],
    )

    report = {
        "speed_kmh": speed_kmh,
        "collision_type": collision_type,
        "seatbelt": seatbelt,
        "airbags": airbags,
        "impact_force_kN": physics["impact_force_kN"],
        "impact_energy_kJ": physics["impact_energy_kJ"],
        "gforce": physics["gforce"],
        "gforce_label": physics["gforce_label"],
        "stopping_distance_m": physics["stopping_distance_m"],
        "risk_level": risk_level,
        "injuries": injuries,
        "safety_suggestions": suggestions,
        "warnings": warnings,
        "health": health,
        "vehicle": {
            "model": vehicle_model or "Generic",
            "generation": generation,
            "mass_kg": vehicle["mass_kg"],
            "ncap_stars": vehicle["ncap_stars"],
            "features": vehicle["features"],
            "is_electric": vehicle["is_electric"],
            "post_crash_brake": vehicle["post_crash_brake"],
            "whips": vehicle["whips"],
            "on_call": vehicle["on_call"],
        },
    }
    logger.info("Crash analysis complete")
    return format_report(report)


run_analysis = analyze_crash


def parse_args():
    parser = argparse.ArgumentParser(description="Crash Analysis & Injury Prediction System")
    parser.add_argument("--speed", type=float, default=50.0)
    parser.add_argument("--collision", type=str, default="frontal",
                        choices=["frontal", "rear", "side", "rollover"])
    parser.add_argument("--seatbelt", action="store_true")
    parser.add_argument("--airbags", action="store_true")
    parser.add_argument("--vehicle", type=str, default="", help="Volvo model, e.g. XC90")
    parser.add_argument("--generation", type=str, default="", help="Generation label")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        report = analyze_crash(
            args.speed, args.collision, args.seatbelt, args.airbags,
            args.vehicle, args.generation,
        )
        print_report({
            **report,
            "risk_level": report["summary"]["risk_level"],
            "injuries": report["injuries"],
            "safety_suggestions": report["safety_suggestions"],
        }, output_json=args.json)
    except ValueError as exc:
        logger.error("Input validation failed: %s", exc)
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
