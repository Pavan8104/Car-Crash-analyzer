import hashlib
import datetime
from typing import Dict, List, Optional
from config import CHANNEL_4G, CHANNEL_SMS, CHANNEL_SATELLITE

# alert payload builder
# builds the structured message that would be sent to each
# recipient (hospital, police, caretaker, manufacturer)
# in a real system this would be AES-256 encrypted before sending


def _vehicle_id_hash(model: str, generation: str) -> str:
    # anonymised vehicle identifier — never exposes real VIN
    raw = f"{model}-{generation}-demo"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()


def _timestamp() -> str:
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def build_hospital_payload(
    risk_level: str,
    injuries: Dict[str, List],
    speed_kmh: float,
    seatbelt: bool,
    airbags: bool,
    vehicle_model: str,
    is_electric: bool,
) -> Dict:
    """
    Hospital gets: injury prediction, severity, airbag status,
    occupant protection status, and EV flag.
    Allows pre-positioning of the right trauma team.
    """
    severe_count = len(injuries.get("Severe", []))
    return {
        "recipient":      "Nearest Trauma Centre",
        "channel":        CHANNEL_4G,
        "priority":       "IMMEDIATE" if risk_level == "High" else "URGENT",
        "timestamp":      _timestamp(),
        "risk_level":     risk_level,
        "predicted_severe_injuries": severe_count,
        "top_injuries":   [i["name"] for i in injuries.get("Severe", [])[:3]],
        "airbags_deployed": airbags,
        "seatbelt_worn":  seatbelt,
        "impact_speed_kmh": speed_kmh,
        "is_electric_vehicle": is_electric,
        "recommended_response": _hospital_response(risk_level, severe_count, is_electric),
    }


def build_police_payload(
    risk_level: str,
    collision_type: str,
    speed_kmh: float,
    vehicle_model: str,
    is_electric: bool,
    gforce: float,
) -> Dict:
    """
    Police / emergency services get: location info, collision type,
    speed, EV flag (special tools needed), and road-clear priority.
    """
    return {
        "recipient":      "Local Emergency Services",
        "channel":        CHANNEL_4G,
        "priority":       "IMMEDIATE" if risk_level == "High" else "STANDARD",
        "timestamp":      _timestamp(),
        "collision_type": collision_type,
        "impact_speed_kmh": speed_kmh,
        "peak_gforce":    gforce,
        "risk_level":     risk_level,
        "vehicle_model":  vehicle_model or "Unknown",
        "is_electric_vehicle": is_electric,
        "road_clearance_needed": risk_level in ("Medium", "High"),
        "ev_specialist_needed":  is_electric,
        "notes": _police_notes(collision_type, is_electric, risk_level),
    }


def build_caretaker_payload(
    risk_level: str,
    speed_kmh: float,
    collision_type: str,
    vehicle_model: str,
) -> Dict:
    """
    Caretaker / next-of-kin gets: plain-language summary only.
    No raw sensor data, no medical jargon.
    """
    return {
        "recipient":   "Registered Caretaker",
        "channel":     CHANNEL_SMS,
        "priority":    "HIGH",
        "timestamp":   _timestamp(),
        "message":     (
            f"ALERT: A crash has been detected involving a {vehicle_model or 'vehicle'} "
            f"at approximately {int(speed_kmh)} km/h. "
            f"Risk level: {risk_level}. "
            "Emergency services have been contacted. "
            "You will receive a follow-up message with hospital details."
        ),
        "risk_level":  risk_level,
        "collision_type": collision_type,
    }


def build_manufacturer_payload(
    vehicle_model: str,
    generation: str,
    speed_kmh: float,
    collision_type: str,
    seatbelt: bool,
    airbags: bool,
    impact_force_kn: float,
    impact_energy_kj: float,
    gforce: float,
    risk_level: str,
) -> Dict:
    """
    Manufacturer gets: anonymised telemetry only.
    Used for fleet safety analysis and model improvements.
    No personal data included.
    """
    return {
        "recipient":         "Vehicle Manufacturer",
        "channel":           CHANNEL_SATELLITE,
        "priority":          "STANDARD",
        "timestamp":         _timestamp(),
        "vehicle_id_hash":   _vehicle_id_hash(vehicle_model, generation),
        "model":             vehicle_model or "Generic",
        "generation":        generation or "Unknown",
        "collision_type":    collision_type,
        "delta_v_kmh":       speed_kmh,
        "impact_force_kn":   impact_force_kn,
        "impact_energy_kj":  impact_energy_kj,
        "peak_gforce":       gforce,
        "airbags_deployed":  airbags,
        "seatbelt_worn":     seatbelt,
        "risk_outcome":      risk_level,
        "data_use":          "Fleet safety analytics only. No personal identification.",
    }


def build_all_payloads(report: Dict) -> Dict:
    """
    Takes the full crash analysis report and builds
    all four alert payloads at once.
    """
    v     = report.get("vehicle", {})
    s     = report.get("summary", {})
    inj   = report.get("injuries", {})
    phys  = report.get("physics", {})

    return {
        "hospital":     build_hospital_payload(
            s.get("risk_level", "Low"),
            inj,
            s.get("speed_kmh", 0),
            v.get("seatbelt", False),
            v.get("airbags", False),
            v.get("model", ""),
            v.get("is_electric", False),
        ),
        "police":       build_police_payload(
            s.get("risk_level", "Low"),
            s.get("collision_type", "frontal"),
            s.get("speed_kmh", 0),
            v.get("model", ""),
            v.get("is_electric", False),
            phys.get("gforce", 0),
        ),
        "caretaker":    build_caretaker_payload(
            s.get("risk_level", "Low"),
            s.get("speed_kmh", 0),
            s.get("collision_type", "frontal"),
            v.get("model", ""),
        ),
        "manufacturer": build_manufacturer_payload(
            v.get("model", ""),
            v.get("generation", ""),
            s.get("speed_kmh", 0),
            s.get("collision_type", "frontal"),
            v.get("seatbelt", False),
            v.get("airbags", False),
            s.get("impact_force_kN", 0),
            s.get("impact_energy_kJ", 0),
            phys.get("gforce", 0),
            s.get("risk_level", "Low"),
        ),
    }


def _hospital_response(risk_level: str, severe_count: int, is_electric: bool) -> str:
    if risk_level == "High" or severe_count >= 2:
        base = "Activate Level 1 Trauma Team. Prepare OR."
    elif risk_level == "Medium":
        base = "Prepare trauma bay. Ortho and neurology on standby."
    else:
        base = "Standard emergency intake."
    if is_electric:
        base += " EV protocol required — chemical burn team on standby."
    return base


def _police_notes(collision_type: str, is_electric: bool, risk_level: str) -> List[str]:
    notes = []
    if collision_type == "rollover":
        notes.append("Rollover detected — possible ejection, check perimeter.")
    if is_electric:
        notes.append("Electric vehicle — do not cut orange HV cables.")
    if risk_level == "High":
        notes.append("High severity — close road in both directions.")
    return notes
